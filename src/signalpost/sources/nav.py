"""Shared NAV feed ingestion; exact identifiers only, no per-company search."""
from ..workers import nav_offload

import asyncio
import json
import os
import re
import time
import unicodedata
import math
import hashlib
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime, parsedate_to_datetime
from pathlib import Path
from urllib.parse import urljoin, urlsplit, parse_qs
from uuid import UUID
import httpx
from ..budget import SourceFailure
from ..identity.orgnr import valid
from ..models.evidence import utc_now
from ..models.envelope import Error
from .extract import Section, Source, add

BASE='https://pam-stilling-feed.nav.no'

# Broad discovery only: exact detail employer.orgnr remains mandatory.
GENERIC_NAMES={'as','asa','enk','ans','da','sa','ba','nuf','ltd','limited','inc','llc',
               'company','firma','selskap','services','service','group','gruppen',
               'holding','holdings','norge','norway','kommune','kommunen'}
LEGAL_SUFFIXES={'as','asa','enk','ans','da','sa','ba','nuf','ltd','limited','inc','llc'}
COMMON_BUSINESS={'bygg','service','eiendom','holding','transport','invest','consult','regnskap',
                 'drift','handel','norge','norway','group','gruppen'}


def rarity_limit(active_headers):
    return max(3,min(50,math.floor(.005*active_headers)))


def distinctive_tokens(value,frequency,active_headers):
    return {token for token in name_tokens(value)-COMMON_BUSINESS
            if frequency.get(token,0)<=rarity_limit(active_headers)}


def discovery_text(value):
    text=str(value or '').casefold().replace('æ','ae').replace('ø','o').replace('å','a')
    # Alternate ASCII spellings converge for discovery only, never identity.
    text=text.replace('oe','o').replace('aa','a')
    text=unicodedata.normalize('NFKD',text)
    return ''.join(c for c in text if not unicodedata.combining(c))


def name_tokens(value):
    text=discovery_text(value)
    text=''.join(c for c in text if not unicodedata.combining(c))
    return {word for word in re.findall(r'[^\W\d_]+',text) if len(word)>=4 and word not in GENERIC_NAMES}


def normal_name(value):
    text=discovery_text(value)
    text=''.join(c for c in text if not unicodedata.combining(c))
    words=re.findall(r'[^\W_]+',text)
    while words and words[-1] in LEGAL_SUFFIXES: words.pop()
    return ' '.join(words)


def name_matches(header,candidate):
    header=normal_name(header); candidate=normal_name(candidate)
    return bool(name_tokens(candidate) and candidate and
                (header==candidate or (' '+candidate+' ') in (' '+header+' ')))


def candidate_score(header, candidate, frequency):
    common=name_tokens(header) & name_tokens(candidate)
    return sum(1 / max(1, frequency.get(token, 1)) for token in sorted(common))


def time_cap(config):
    return config.nav_time_cap_seconds if config.nav_time_cap_seconds is not None else min(900, .40 * config.time_budget_seconds)


def company_names(envelopes,previous=None):
    names={}
    for envelope in envelopes:
        tokens=set()
        def remember(value):
            if name_tokens(value): tokens.add(normal_name(value))
        for claim in envelope.claims:
            if claim.availability!='available': continue
            if claim.field=='identity.legal_name': remember(claim.value)
            elif claim.family=='subunits' and isinstance(claim.value,dict):
                remember(claim.value.get('name'))
            elif claim.family=='website' and 'brand' in claim.field:
                value=claim.value
                remember(value.get('name') if isinstance(value,dict) else value)
        prior=(previous or {}).get(envelope.organisation_number,{})
        for claim in prior.get('claims',prior.get('profile',{}).get('claims',[])):
            if claim.get('availability')=='available' and claim.get('family')=='website' and 'brand' in claim.get('field',''):
                value=claim.get('value')
                remember(value.get('name') if isinstance(value,dict) else value)
        names[envelope.organisation_number]=tokens
    return names


def header_name(item):
    entry=item.get('_feed_entry') or {}
    employer=entry.get('employer') or item.get('employer') or {}
    return entry.get('businessName') or entry.get('employerName') or (employer.get('name') if isinstance(employer,dict) else None)


def timestamp(value):
    try:
        date=datetime.fromisoformat(str(value).replace('Z','+00:00'))
        return date.astimezone(timezone.utc) if date.tzinfo else None
    except (TypeError,ValueError): return None


def token_from(value):
    match=re.search(r'\be[y]J[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b',str(value or ''))
    return match.group() if match else None


def allowed(raw):
    url=urljoin(BASE+'/',raw)
    p=urlsplit(url)
    if p.scheme!='https' or p.hostname!='pam-stilling-feed.nav.no' or p.port not in {None,443} or p.username or p.password or p.fragment:
        raise SourceFailure('nav_url_refused')
    if not re.fullmatch(r'/api/(?:publicToken|v1/feed(?:/[0-9a-fA-F-]{36})?|v1/feedentry/[0-9a-fA-F-]{36})',p.path):
        raise SourceFailure('nav_url_refused')
    if set(parse_qs(p.query,keep_blank_values=True))-{'last','pageSize'}:
        raise SourceFailure('nav_url_refused')
    return url


@dataclass
class Ad:
    value: dict
    sha: str
    url: str
    retrieved_at: str
    page_sha: str
    page_url: str
    page_locator: str
    page_retrieved_at: str
    discovery: dict | None = None


@dataclass
class Index:
    ads: dict = field(default_factory=dict)
    closed: set = field(default_factory=set)
    live_closed: set = field(default_factory=set)
    closure_proofs: dict = field(default_factory=dict)
    complete: bool = False
    blocked: bool = False
    reason: str = 'not_started'
    coverage_ready: bool = False
    incomplete_orgs: set = field(default_factory=set)
    metrics: dict = field(default_factory=lambda: {'pages':0,'items':0,'bytes':0,'details':0,'requests':0,'runtime_ms':0})

    def company_complete(self,org):
        return self.complete or (self.coverage_ready and org not in self.incomplete_orgs)


class NavHttp:
    def __init__(self,client,config,budget,blobs,index):
        self.client,self.config,self.budget,self.blobs,self.index=client,config,budget,blobs,index
        self.semaphore=asyncio.Semaphore(config.nav_concurrency)
        self.feed_semaphore=asyncio.Semaphore(1)
        self.polite_backoff=False;self.pause_until=0;self.throttle_count=0
        self.cache_path=config.state_dir/'nav-cache.json'
        try: self.cache=json.loads(self.cache_path.read_text(encoding='utf8'))
        except (OSError,ValueError): self.cache={}

    async def get(self,raw,token=None,headers=None,secret=False,companies=(),persist=True):
        url=allowed(raw)
        supplied=dict(headers or {})
        key=url+'|'+supplied.get('If-Modified-Since','')
        cached=self.cache.get(key)
        if cached and (self.blobs.directory/cached['sha']).exists(): supplied['If-None-Match']=cached['etag']
        if token: supplied['Authorization']='Bearer '+token
        supplied['Accept']='text/plain' if secret else 'application/json'
        supplied['User-Agent']=self.config.website_user_agent
        async with (self.semaphore if '/feedentry/' in url else self.feed_semaphore):
            for attempt in range(2):
                if self.polite_backoff and self.pause_until>time.monotonic():
                    await asyncio.sleep(self.pause_until-time.monotonic())
                if '/feedentry/' in url and self.index.metrics.get('detail_requests',0)>=self.index.metrics.get('detail_request_cap', self.config.nav_max_details if self.config.nav_max_details is not None else 300):
                    raise SourceFailure('nav_detail_cap')
                event=self.budget.reserve(url,'pam-stilling-feed.nav.no','__nav_prefetch__')
                if '/feedentry/' in url:
                    self.index.metrics['detail_requests']=self.index.metrics.get('detail_requests',0)+1
                    by_company=self.index.metrics.setdefault('detail_requests_by_company',{})
                    for org in companies: by_company[org]=by_company.get(org,0)+1
                event['section']='hiring_prefetch'
                self.index.metrics['requests']+=1
                if hasattr(self.index,'started'):self.index.started.set()
                began=time.monotonic()
                is_feed='/api/v1/feed' in url and '/feedentry/' not in url
                async def trace(name,info):
                    if name.endswith('send_request_headers.complete'):
                        sent=time.monotonic()-self.budget.start
                        event['request_sent_seconds']=sent
                        if is_feed and getattr(self,'last_feed_response_complete',None) is not None:
                            event['inter_request_gap_ms']=max(0,(sent-self.last_feed_response_complete)*1000)
                            event['gap_preceded_by']=getattr(self,'last_feed_finish_kind','response_complete')
                            self.last_feed_response_complete=None
                try:
                    remaining=self.budget.deadline-time.monotonic()
                    async with asyncio.timeout(min(self.config.nav_request_timeout,max(.001,remaining))):
                        async with self.client.stream('GET',url,headers=supplied,follow_redirects=False,timeout=min(self.config.nav_request_timeout,max(.001,remaining)),extensions={'trace':trace}) as response:
                            event['status']=response.status_code
                            event['response_headers_ms']=round((time.monotonic()-began)*1000)
                            if response.headers.get('Retry-After'):
                                try:retry_seconds=float(response.headers['Retry-After'])
                                except ValueError:
                                    try:retry_seconds=parsedate_to_datetime(response.headers['Retry-After']).timestamp()-time.time()
                                    except (ValueError,TypeError,OverflowError):retry_seconds=None
                                event['retry_after_seconds']=retry_seconds
                            chunks=[]; size=0
                            async for chunk in response.aiter_bytes():
                                size+=len(chunk)
                                if size>self.config.nav_body_cap_mb*1024*1024: raise SourceFailure('nav_body_cap')
                                chunks.append(chunk)
                            body=b''.join(chunks)
                            event['decoded_body_bytes']=len(body)
                            completed=time.monotonic()-self.budget.start
                            event['response_complete_seconds']=completed
                            if is_feed:
                                self.last_feed_response_complete=completed
                                self.last_feed_finish_kind='response_complete'
                            event['response_read_ms']=round((time.monotonic()-began)*1000)
                            self.index.metrics['bytes']+=len(body)
                            if response.status_code in {301,302,303,307,308}: raise SourceFailure('nav_redirect_refused')
                            if secret:
                                # Credential bodies are the deliberate blob-store exception.
                                return response.status_code,body,None,utc_now()
                            if token and token.encode() in body: raise SourceFailure('credential_echo_refused')
                            if response.status_code==304:
                                if not cached or not (self.blobs.directory/cached['sha']).exists(): raise SourceFailure('nav_cache_missing')
                                body=await nav_offload((self.blobs.directory/cached['sha']).read_bytes)
                                sha=cached['sha']; event['content_sha256']=sha
                                return 200,body,sha,utc_now()
                            stored=time.monotonic()
                            sha=await nav_offload(self.blobs.put,body) if persist else await nav_offload(lambda:hashlib.sha256(body).hexdigest())
                            if persist:event['content_sha256']=sha
                            else:event['response_sha256']=sha
                            event['blob_store_ms']=round((time.monotonic()-stored)*1000)
                            if response.status_code in {401,403}: raise SourceFailure('token_unavailable')
                            if response.status_code==429 or response.status_code>=500:
                                if self.polite_backoff:
                                    self.throttle_count+=1
                                    retry_seconds=event.get('retry_after_seconds')
                                    retry_seconds=retry_seconds if isinstance(retry_seconds,(int,float)) and math.isfinite(retry_seconds) else 0
                                    pause=max(retry_seconds,min(60,2**min(self.throttle_count,6)))
                                    self.pause_until=max(self.pause_until,time.monotonic()+pause)
                                    event['retry_backoff_seconds']=pause
                                if attempt==0:
                                    retry=response.headers.get('Retry-After','0')
                                    try: delay=float(retry)
                                    except ValueError:
                                        try: delay=parsedate_to_datetime(retry).timestamp()-time.time()
                                        except (ValueError,TypeError,OverflowError): delay=.2
                                    if self.polite_backoff:delay=max(delay,event['retry_backoff_seconds'])
                                    if time.monotonic()+max(.2,delay)>=self.budget.deadline: raise SourceFailure('deadline')
                                    await asyncio.sleep(max(.2,delay)); continue
                                raise SourceFailure('nav_http_'+str(response.status_code))
                            if response.status_code!=200: raise SourceFailure('nav_http_'+str(response.status_code))
                            if persist and response.headers.get('etag'):
                                self.cache[key]={'etag':response.headers['etag'],'sha':sha}
                            return 200,body,sha,utc_now()
                except (TimeoutError,httpx.HTTPError) as exc:
                    event['error']=type(exc).__name__
                    if attempt: raise SourceFailure('nav_network_error') from None
                except SourceFailure as exc:
                    event['error']=exc.code
                    raise
                finally:
                    event['runtime_ms']=round((time.monotonic()-began)*1000)
                    if is_feed and event.get('error') and 'response_complete_seconds' not in event and 'request_sent_seconds' in event:
                        self.last_feed_response_complete=time.monotonic()-self.budget.start
                        self.last_feed_finish_kind='request_error_complete'
        raise SourceFailure('nav_network_error')

    async def public_token(self):
        try:
            status,body,_,_=await self.get(BASE+'/api/publicToken',secret=True)
            return token_from(body.decode('utf8',errors='replace')) if status==200 else None
        except Exception: return None

    def save(self):
        try:
            self.cache_path.parent.mkdir(parents=True,exist_ok=True)
            self.cache_path.write_text(json.dumps(self.cache),encoding='utf8')
        except OSError: pass


async def prefetch(client,config,budget,blobs,index,names_ready=None,previous=None):
    from .nav_index import load,DEFAULT_PATH
    path=config.nav_index_path or DEFAULT_PATH
    try:data,age=await nav_offload(load,path,config.nav_index_max_age_days)
    except SourceFailure as exc:
        index.metrics.update({'source_mode':'full_feed_fallback','index_fallback_reason':exc.code})
    else:
        from .nav_cached import prefetch as cached_prefetch
        return await cached_prefetch(client,config,budget,blobs,index,data,age,path,names_ready,previous)
    from .nav_stream import prefetch as streaming_prefetch
    return await streaming_prefetch(client,config,budget,blobs,index,names_ready,previous)


def section(envelope,index,blobs,previous=None):
    complete=index.company_complete(envelope.organisation_number)
    state='blocked' if index.blocked else 'failed' if not complete else 'not_available'
    result=Section(state=state)
    parents={envelope.organisation_number:None}
    for claim in envelope.claims:
        if claim.family=='subunits' and claim.availability=='available' and isinstance(claim.value,dict):
            org=claim.value.get('organisation_number')
            if org: parents[org]='subunit '+org
    seen_uuids = set()
    for org,via in parents.items():
        for ad in sorted(index.ads.get(org,[]), key=lambda a: a.value['uuid']):
            if timestamp(ad.value['expires'])<=datetime.now(timezone.utc) or ad.value['uuid'] in index.closed or ad.value['uuid'] in seen_uuids: continue
            seen_uuids.add(ad.value['uuid'])
            actual_emp = ad.value.get('employer_orgnr')
            match_via = ('subunit ' + actual_emp) if (actual_emp and actual_emp != envelope.organisation_number) else (via or 'organisation ' + org)
            value={**ad.value,'matched_via':match_via}
            body=(blobs.directory/ad.sha).read_bytes()
            add(result,Source(ad.url,body,ad.sha,ad.retrieved_at),envelope.organisation_number,'hiring','hiring.job.'+ad.value['uuid'],
                value,'/ad_content',effective=ad.value['published'],source_class='official_nav',method='signalpost.nav.v1')
            # The detail is mandatory; the feed page also anchors the item.
            if ad.page_sha:
                page_source=Source(ad.page_url,(blobs.directory/ad.page_sha).read_bytes(),ad.page_sha,ad.page_retrieved_at)
                temporary=Section()
                add(temporary,page_source,envelope.organisation_number,'hiring','hiring.page',ad.value['uuid'],ad.page_locator,source_class='official_nav',method='signalpost.nav.v1')
                result.evidence.extend(temporary.evidence); result.claims[-1].evidence_ids.extend(e.id for e in temporary.evidence)
            elif ad.discovery:
                result.evidence[-1].source_identifier=json.dumps(ad.discovery,sort_keys=True,separators=(',',':'))
    if result.claims and not index.blocked and (complete or index.metrics.get('source_mode')=='declared_index'): result.state='available'
    if not complete: result.errors.append(Error(section='hiring',code=index.reason if index.reason!='complete' else 'nav_name_unusable',message='NAV candidate coverage is incomplete; absence and closure are not established'))
    if complete and not result.claims and envelope.run.sections.get('subunits') not in {'available','not_available','not_applicable'}:
        result.state='failed'; result.errors.append(Error(section='hiring',code='subunit_index_incomplete',message='Legal-entity match checked; branch coverage is unknown'))
    old=previous.get('claims',previous.get('profile',{}).get('claims',[])) if previous else []
    old_jobs=[c['value']['uuid'] for c in old if c.get('family')=='hiring' and c.get('availability')=='available' and isinstance(c.get('value'),dict)]
    cached=index.metrics.get('source_mode')=='declared_index'
    closure_evidence={}
    for uuid in old_jobs:
        if uuid not in index.closure_proofs:continue
        proof=index.closure_proofs[uuid];sha,url,retrieved,locator,value=proof[:5]
        temporary=Section();body=(blobs.directory/sha).read_bytes()
        add(temporary,Source(url,body,sha,retrieved),envelope.organisation_number,'hiring','hiring.closed.'+uuid,None,
            locator,availability='not_available',span=Source(url,body,sha,retrieved).excerpt(value,locator),
            source_class='official_nav',method='signalpost.nav.live_closure.v1')
        result.evidence.extend(temporary.evidence);closure_evidence[uuid]=[e.id for e in temporary.evidence]
        if len(proof)>5:
            temporary.evidence[0].source_identifier=json.dumps(proof[5],sort_keys=True,separators=(',',':'))
    envelope.run.refresh['hiring']={'index_complete':complete,'reason':index.reason,
        'closure_requires_live_detail':True,'closure_evidence':closure_evidence,
        'known_closed_jobs':[uuid for uuid in old_jobs if uuid in closure_evidence]}
    if cached:
        envelope.run.refresh['hiring'].update({k:index.metrics[k] for k in ('index_version','index_built_at')})
    return result
