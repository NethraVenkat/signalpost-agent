"""Shared NAV feed ingestion; exact identifiers only, no per-company search."""
import asyncio
import json
import os
import re
import time
import unicodedata
import math
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
    return config.nav_time_cap_seconds if config.nav_time_cap_seconds is not None else min(600, .35 * config.time_budget_seconds)


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


@dataclass
class Index:
    ads: dict = field(default_factory=dict)
    closed: set = field(default_factory=set)
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
        self.cache_path=config.state_dir/'nav-cache.json'
        try: self.cache=json.loads(self.cache_path.read_text(encoding='utf8'))
        except (OSError,ValueError): self.cache={}

    async def get(self,raw,token=None,headers=None,secret=False,companies=()):
        url=allowed(raw)
        supplied=dict(headers or {})
        key=url+'|'+supplied.get('If-Modified-Since','')
        cached=self.cache.get(key)
        if cached and (self.blobs.directory/cached['sha']).exists(): supplied['If-None-Match']=cached['etag']
        if token: supplied['Authorization']='Bearer '+token
        supplied['Accept']='text/plain' if secret else 'application/json'
        supplied['User-Agent']=self.config.website_user_agent
        async with self.semaphore:
            for attempt in range(2):
                if '/feedentry/' in url and self.index.metrics.get('detail_requests',0)>=self.index.metrics.get('detail_request_cap', self.config.nav_max_details if self.config.nav_max_details is not None else 300):
                    raise SourceFailure('nav_detail_cap')
                event=self.budget.reserve(url,'pam-stilling-feed.nav.no','__nav_prefetch__')
                if '/feedentry/' in url:
                    self.index.metrics['detail_requests']=self.index.metrics.get('detail_requests',0)+1
                    by_company=self.index.metrics.setdefault('detail_requests_by_company',{})
                    for org in companies: by_company[org]=by_company.get(org,0)+1
                event['section']='hiring_prefetch'
                self.index.metrics['requests']+=1
                began=time.monotonic()
                try:
                    remaining=self.budget.deadline-time.monotonic()
                    async with asyncio.timeout(min(self.config.nav_request_timeout,max(.001,remaining))):
                        async with self.client.stream('GET',url,headers=supplied,follow_redirects=False,timeout=min(self.config.nav_request_timeout,max(.001,remaining))) as response:
                            event['status']=response.status_code
                            chunks=[]; size=0
                            async for chunk in response.aiter_bytes():
                                size+=len(chunk)
                                if size>self.config.nav_body_cap_mb*1024*1024: raise SourceFailure('nav_body_cap')
                                chunks.append(chunk)
                            body=b''.join(chunks)
                            self.index.metrics['bytes']+=len(body)
                            if response.status_code in {301,302,303,307,308}: raise SourceFailure('nav_redirect_refused')
                            if secret:
                                # Credential bodies are the deliberate blob-store exception.
                                return response.status_code,body,None,utc_now()
                            if token and token.encode() in body: raise SourceFailure('credential_echo_refused')
                            if response.status_code==304:
                                if not cached or not (self.blobs.directory/cached['sha']).exists(): raise SourceFailure('nav_cache_missing')
                                body=(self.blobs.directory/cached['sha']).read_bytes()
                                sha=cached['sha']; event['content_sha256']=sha
                                return 200,body,sha,utc_now()
                            sha=self.blobs.put(body); event['content_sha256']=sha
                            if response.status_code in {401,403}: raise SourceFailure('token_unavailable')
                            if response.status_code==429 or response.status_code>=500:
                                if attempt==0:
                                    retry=response.headers.get('Retry-After','0')
                                    try: delay=float(retry)
                                    except ValueError:
                                        try: delay=parsedate_to_datetime(retry).timestamp()-time.time()
                                        except (ValueError,TypeError,OverflowError): delay=.2
                                    if time.monotonic()+max(.2,delay)>=self.budget.deadline: raise SourceFailure('deadline')
                                    await asyncio.sleep(max(.2,delay)); continue
                                raise SourceFailure('nav_http_'+str(response.status_code))
                            if response.status_code!=200: raise SourceFailure('nav_http_'+str(response.status_code))
                            if response.headers.get('etag'):
                                self.cache[key]={'etag':response.headers['etag'],'sha':sha}
                            return 200,body,sha,utc_now()
                except (TimeoutError,httpx.HTTPError) as exc:
                    event['error']=type(exc).__name__
                    if attempt: raise SourceFailure('nav_network_error') from None
                except SourceFailure as exc:
                    event['error']=exc.code
                    raise
                finally: event['runtime_ms']=round((time.monotonic()-began)*1000)
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
    began=time.monotonic(); http=NavHttp(client,config,budget,blobs,index)
    paging_began=None
    index.metrics.update({'feed_complete':False,'time_cap_seconds':time_cap(config)})
    errors=[]
    try:
        async with asyncio.timeout(time_cap(config)):
            token=token_from(os.environ.get('NAV_API_TOKEN'))
            from_environment=bool(token)
            token=token or await http.public_token()
            if not token:
                index.blocked=True; index.reason='token_unavailable'; return index
            cutoff=datetime.now(timezone.utc)-timedelta(days=config.nav_lookback_days)
            cutoff=cutoff.replace(hour=0,minute=0,second=0,microsecond=0)
            url=BASE+'/api/v1/feed'; headers={'If-Modified-Since':format_datetime(cutoff,usegmt=True)}
            latest={}; seen=set(); page_complete=False
            paging_began=time.monotonic()
            while url:
                if index.metrics['pages']>=config.nav_max_pages:
                    errors.append('nav_page_cap'); break
                url=allowed(url)
                if url in seen: raise SourceFailure('nav_paging_loop')
                seen.add(url)
                try: _,body,sha,retrieved=await http.get(url,token,headers)
                except SourceFailure as exc:
                    if exc.code=='token_unavailable' and from_environment:
                        token=await http.public_token(); from_environment=False
                        if not token: raise
                        _,body,sha,retrieved=await http.get(url,token,headers)
                    else: raise
                data=json.loads(body)
                if not isinstance(data,dict) or not isinstance(data.get('items'),list): raise SourceFailure('nav_malformed_page')
                index.metrics['pages']+=1; index.metrics['items']+=len(data['items'])
                for n,item in enumerate(data['items']):
                    entry=item.get('_feed_entry') or {}
                    if entry.get('status') not in {'ACTIVE','INACTIVE','DELETED'}: raise SourceFailure('nav_unknown_status')
                    uuid=entry.get('uuid') or item.get('id')
                    try: uuid=str(UUID(uuid))
                    except (ValueError,TypeError,AttributeError): raise SourceFailure('nav_invalid_uuid') from None
                    changed=timestamp(item.get('date_modified') or entry.get('sistEndret'))
                    if changed is None: raise SourceFailure('nav_invalid_modified_date')
                    if uuid not in latest or changed>=latest[uuid][0]:
                        latest[uuid]=(changed,item,sha,url,'/items/'+str(n),retrieved)
                next_url=data.get('next_url')
                if not next_url and data.get('next_id'): raise SourceFailure('nav_missing_next_url')
                if not next_url: page_complete=True; break
                url=next_url; headers={}
            index.metrics['feed_runtime_ms']=round((time.monotonic()-paging_began)*1000)
            index.metrics['feed_complete']=page_complete and config.nav_lookback_days>=185
            if page_complete:
                index.closed.update(uuid for uuid,record in latest.items() if record[1].get('_feed_entry',{}).get('status')!='ACTIVE')
            active=[(uuid,record) for uuid,record in latest.items() if record[1].get('_feed_entry',{}).get('status')=='ACTIVE']
            index.metrics['active_headers']=len(active)
            names=await names_ready() if names_ready else {}
            all_orgs=set(names)
            with_names=sum(bool(header_name(record[1])) for _,record in active)
            frequency=Counter(token for _,record in active for token in name_tokens(header_name(record[1])))
            detail_cap=config.nav_max_details if config.nav_max_details is not None else max(300, math.ceil(.5*len(names)))
            index.metrics['detail_request_cap']=detail_cap
            candidates=[]
            scores={}
            known_tokens={org:[name_tokens(candidate) for candidate in known] for org,known in names.items()}
            token_orgs=defaultdict(set)
            for org,sets in known_tokens.items():
                for tokens in sets:
                    for distinctive_token in tokens:token_orgs[distinctive_token].add(org)
            old_jobs={}
            for org,row in (previous or {}).items():
                for claim in row.get('claims',row.get('profile',{}).get('claims',[])):
                    if claim.get('family')=='hiring' and claim.get('availability')=='available' and isinstance(claim.get('value'),dict):
                        old_jobs.setdefault(claim['value'].get('uuid'),set()).add(org)
            for uuid,record in active:
                name=header_name(record[1])
                header_tokens=name_tokens(name)
                possible=set().union(*(token_orgs[token] for token in header_tokens)) if header_tokens else set()
                ranked={org:max((sum(1/max(1,frequency[token]) for token in sorted(header_tokens & candidate)) for candidate in known_tokens[org]),default=0) for org in possible}
                affected={org for org,score in ranked.items() if score>0} if name and config.nav_rank_candidates else {org for org,known in names.items() if any(name_matches(name,candidate) for candidate in known)} if name else all_orgs
                scores[uuid]=max(ranked.values(),default=0)
                if not names_ready or not name or affected: candidates.append((uuid,record,affected))
                elif uuid in old_jobs:
                    index.incomplete_orgs.update(old_jobs[uuid])
                    errors.append('nav_existing_ad_name_unmatched')
            if config.nav_rank_candidates:
                candidates.sort(key=lambda entry: (-scores[entry[0]], entry[0]))
            index.metrics.update({'headers_with_employer_name':with_names,
                'headers_without_employer_name':len(active)-with_names,
                'name_prefilter':bool(names_ready and with_names),
                'coverage_scope':'batch_legal_brand_subunit_name_candidates' if names_ready and with_names else 'all_active_headers',
                'candidate_headers':len(candidates),'skipped_name_nonmatches':len(active)-len(candidates),
                'detail_request_cap':detail_cap, 'ranking_enabled':config.nav_rank_candidates,
                'cap_hits':0})
            if names_ready and with_names:
                index.incomplete_orgs.update(org for org,tokens in names.items() if not tokens)
            async def detail(uuid,record,affected):
                _,item,page_sha,page_url,locator,page_retrieved=record
                try:
                    url=allowed(item['url'])
                    _,body,sha,retrieved=await http.get(url,token,companies=affected)
                    index.metrics['details']+=1
                    entry=json.loads(body)
                    if str(entry.get('uuid'))!=uuid: raise SourceFailure('nav_wrong_ad')
                    if entry.get('status') not in {'ACTIVE','INACTIVE','DELETED'}: raise SourceFailure('nav_unknown_status')
                    if entry.get('status')!='ACTIVE': index.closed.add(uuid); return
                    ad=entry.get('ad_content')
                    if not isinstance(ad,dict) or str(ad.get('uuid'))!=uuid: raise SourceFailure('nav_malformed_ad')
                    expires=timestamp(ad.get('expires')); published=timestamp(ad.get('published'))
                    if expires is None or published is None: raise SourceFailure('nav_invalid_dates')
                    now=datetime.now(timezone.utc)
                    if expires<=now or published>now: index.closed.add(uuid); return
                    org=str((ad.get('employer') or {}).get('orgnr') or '').strip()
                    if not valid(org): return  # Missing identifiers never become name matches.
                    value={'uuid':uuid,'employer_orgnr':org,'title':ad.get('title') or None,
                           'location':[{'municipality':x.get('municipal'),'city':x.get('city')} for x in ad.get('workLocations',[])] or None,
                           'published':ad['published'],'expires':ad['expires'],
                           'occupation_categories':ad.get('occupationCategories') or None,
                           'url':'https://arbeidsplassen.nav.no/stillinger/stilling/'+uuid}
                    value['availability']={'location':'available' if value['location'] else 'not_available',
                                           'occupation_categories':'available' if value['occupation_categories'] else 'not_available'}
                    if not value['title']: raise SourceFailure('nav_missing_title')
                    index.ads.setdefault(org,[]).append(Ad(value,sha,url,retrieved,page_sha,page_url,locator,page_retrieved))
                except asyncio.CancelledError: raise
                except Exception as exc:
                    if isinstance(exc,SourceFailure) and exc.code=='nav_detail_cap':
                        index.metrics['cap_hits']+=1
                    errors.append(exc.code if isinstance(exc,SourceFailure) else type(exc).__name__)
                    index.incomplete_orgs.update(affected)
            # Bounded workers: never create tens of thousands of pending tasks.
            queue=asyncio.Queue()
            for entry in candidates: queue.put_nowait(entry)
            async def worker():
                while True:
                    try: uuid,record,affected=queue.get_nowait()
                    except asyncio.QueueEmpty: return
                    await detail(uuid,record,affected)
            # A single ranked detail worker preserves request order, including retries.
            await asyncio.gather(*(worker() for _ in range(1 if config.nav_rank_candidates else config.nav_concurrency)))
            index.complete=page_complete and not errors and not index.incomplete_orgs and config.nav_lookback_days>=185
            index.coverage_ready=page_complete and config.nav_lookback_days>=185
            index.metrics['feed_complete']=page_complete and config.nav_lookback_days>=185
            index.reason='complete' if index.complete else ','.join(sorted(set(errors))) or ('nav_name_unusable' if index.incomplete_orgs else 'nav_window_incomplete')
    except asyncio.CancelledError:
        index.reason='deadline'; raise
    except TimeoutError: index.reason='nav_time_cap'
    except Exception as exc:
        index.reason=exc.code if isinstance(exc,SourceFailure) else type(exc).__name__
        index.blocked=index.reason=='token_unavailable'
    finally:
        if paging_began is not None and 'feed_runtime_ms' not in index.metrics:
            index.metrics['feed_runtime_ms']=round((time.monotonic()-paging_began)*1000)
        index.metrics['average_seconds_per_page']=index.metrics.get('feed_runtime_ms',0)/1000/index.metrics['pages'] if index.metrics['pages'] else None
        index.metrics['runtime_ms']=round((time.monotonic()-began)*1000)
        index.metrics['runtime_seconds']=index.metrics['runtime_ms']/1000
        index.metrics['feed_seconds']=index.metrics.get('feed_runtime_ms',0)/1000
        index.metrics.update({'complete':index.complete,'blocked':index.blocked,'reason':index.reason,
                              'lookback_days':config.nav_lookback_days,'indexed_ads':sum(map(len,index.ads.values()))})
        index.metrics['incomplete_companies']=sorted(index.incomplete_orgs)
        index.metrics['detail_requests']=index.metrics.get('detail_requests',0)
        http.save()
    return index


def section(envelope,index,blobs,previous=None):
    complete=index.company_complete(envelope.organisation_number)
    state='blocked' if index.blocked else 'failed' if not complete else 'not_available'
    result=Section(state=state)
    parents={envelope.organisation_number:None}
    for claim in envelope.claims:
        if claim.family=='subunits' and claim.availability=='available' and isinstance(claim.value,dict):
            org=claim.value.get('organisation_number')
            if org: parents[org]='subunit '+org
    for org,via in parents.items():
        for ad in index.ads.get(org,[]):
            if timestamp(ad.value['expires'])<=datetime.now(timezone.utc) or ad.value['uuid'] in index.closed: continue
            value={**ad.value,'matched_via':via or 'organisation '+org}
            body=(blobs.directory/ad.sha).read_bytes()
            add(result,Source(ad.url,body,ad.sha,ad.retrieved_at),envelope.organisation_number,'hiring','hiring.job.'+ad.value['uuid'],
                value,'/ad_content',effective=ad.value['published'],source_class='official_nav',method='signalpost.nav.v1')
            # The detail is mandatory; the feed page also anchors the item.
            page_source=Source(ad.page_url,(blobs.directory/ad.page_sha).read_bytes(),ad.page_sha,ad.page_retrieved_at)
            temporary=Section()
            add(temporary,page_source,envelope.organisation_number,'hiring','hiring.page',ad.value['uuid'],ad.page_locator,source_class='official_nav',method='signalpost.nav.v1')
            result.evidence.extend(temporary.evidence); result.claims[-1].evidence_ids.extend(e.id for e in temporary.evidence)
    if complete and result.claims: result.state='available'
    if not complete: result.errors.append(Error(section='hiring',code=index.reason if index.reason!='complete' else 'nav_name_unusable',message='NAV candidate coverage is incomplete; absence and closure are not established'))
    if complete and not result.claims and envelope.run.sections.get('subunits') not in {'available','not_available','not_applicable'}:
        result.state='failed'; result.errors.append(Error(section='hiring',code='subunit_index_incomplete',message='Legal-entity match checked; branch coverage is unknown'))
    old=previous.get('claims',previous.get('profile',{}).get('claims',[])) if previous else []
    old_jobs=[c['value']['uuid'] for c in old if c.get('family')=='hiring' and c.get('availability')=='available' and isinstance(c.get('value'),dict)]
    envelope.run.refresh['hiring']={'index_complete':complete,'reason':index.reason,
        'known_closed_jobs':[uuid for uuid in old_jobs if uuid in index.closed]}
    return result
