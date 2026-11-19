"""Spend only unused cumulative website allowance on ranked, untried nominations."""
import asyncio
import heapq
import json
import time
import traceback
from collections import Counter
from datetime import datetime, timezone
from urllib.parse import urlsplit

from ..budget import SourceFailure
from ..models.envelope import Error
from ..portable_paths import portable_text
from ..sources.extract import missing
from . import collector
from .candidates import generate, candidate_key
from .policy import normalize_url
from .fetcher import STRONG

ORIGIN_SCORE = {'registry_website':100, 'registry_email':95,
    'subunit_registry_website':90, 'subunit_registry_email':88,
    'seed_commoncrawl':87, 'seed_openstreetmap':86,
    'nav_employer_homepage':85, 'legal_name_slug':70, 'brand_variant':60,
    'registry_subunit_name':50}


def priority(candidate):
    return ORIGIN_SCORE.get(candidate.origin, 0) + int(candidate.domain.endswith('.no'))


def exact(envelope):
    return any(c.field=='official_website' and c.availability=='available'
               and not c.carried_forward and c.value.get('identity_level')=='VERIFIED'
               for c in envelope.claims)


def discard_stale_activity(envelope):
    """A replacement website proof cannot authorize the previous site's facts."""
    parents={c.id for c in envelope.claims if c.field=='official_website' and c.availability=='available'}
    envelope.claims=[c for c in envelope.claims if not (
        c.family=='activity' and c.field.startswith('dated_item.') and c.availability=='available'
        and (not isinstance(c.value,dict) or c.value.get('identity_claim_id') not in parents))]


def nav_homepages(envelope, index, blobs):
    """Saved live detail employer.homepage nominates only; cache/header names do not."""
    from ..sources.nav import timestamp
    scope={envelope.organisation_number} | {c.value['organisation_number'] for c in envelope.claims
        if c.field.startswith('subunits.unit.') and c.availability=='available'
        and isinstance(c.value,dict) and c.value.get('organisation_number')}
    result={}; now=datetime.now(timezone.utc)
    for owner in sorted(scope):
        for ad in index.ads.get(owner,[]):
            try:
                if ad.value['uuid'] in index.closed: continue
                body=blobs.read(ad.sha)
                entry=json.loads(body) if body else {}
                if not isinstance(entry,dict):continue
                raw=entry.get('ad_content') or {}
                if not isinstance(raw,dict):continue
                employer=raw.get('employer') or {}
                if not isinstance(employer,dict):continue
                if (entry.get('status')!='ACTIVE' or entry.get('uuid')!=ad.value['uuid']
                        or raw.get('uuid')!=ad.value['uuid']
                        or str(employer.get('orgnr'))!=owner
                        or ad.value.get('employer_orgnr')!=owner): continue
                if not timestamp(raw.get('expires')) or timestamp(raw['expires'])<=now: continue
                if not timestamp(raw.get('published')) or timestamp(raw['published'])>now: continue
                homepage=employer.get('homepage')
                if not isinstance(homepage,str): continue
                url=normalize_url(homepage)
                if url: result[url]={'url':url, 'subunit_orgnr':owner if owner!=envelope.organisation_number else None,
                    'source_url':ad.url, 'content_sha256':ad.sha, 'locator':'/ad_content/employer/homepage'}
            except (KeyError,TypeError,ValueError): continue
    return [result[key] for key in sorted(result)]


def room(http, org):
    if hasattr(http,'company_cap'):return max(0,http.company_cap(org)-http.counts.get(org,0))
    nonweb=sum(e['organisation_number']==org and e.get('section')!='website' for e in http.budget.events)
    return max(0,min(8,http.config.website_request_cap,http.config.website_total_request_cap-nonweb)-http.counts.get(org,0))


def dns_room(http, org, candidate):
    host=urlsplit(candidate.url).hostname
    return (candidate.origin=='registry_website' or not http.config.dns_precheck
            or host in http.dns_cache or (org,host.removeprefix('www.')) in http.dns_nominations
            or http.dns_counts.get(org,0)<(http.dns_limit(org) if hasattr(http,'dns_limit') else 8))


def company_io_failure(envelope, record, exc, update, family, phase, url=None):
    """An OS/network/storage failure closes this company's pass, not the batch."""
    code = 'adaptive_os_error'
    message = portable_text(str(exc))[:1000]
    record['state'] = 'failed'
    record['error'] = {'code': code, 'type': type(exc).__name__, 'section': family,
                       'phase': phase, 'url': url, 'message': message,
                       'errno': exc.errno, 'winerror': getattr(exc, 'winerror', None),
                       'traceback': portable_text(''.join(traceback.format_exception(type(exc), exc, exc.__traceback__)))[-6000:]}
    update(envelope, family, missing(family, code, f'Adaptive {phase} failed: {message}'))


async def run(envelopes, http, index, bulk, previous, update, refresh_activity):
    """Pass 1 finishes globally before this deterministic priority queue starts.

    Neither HTTP counters, nomination counters, caches nor the original deadline
    are reset. A per-company slice is a cumulative ceiling, not a new allowance.
    """
    began=time.monotonic(); budget=http.budget
    pass1_websites=sum(exact(e) for e in envelopes.values())
    cutoff = min(budget.deadline, budget.pass2_cutoff)
    stop = None
    records={}; heap=[]; queued=set()
    for org,envelope in sorted(envelopes.items()):
        record=records[org]={'state':'already_verified' if exact(envelope) else 'no_pending_candidates',
                            'candidates':0,'attempts':0,'requests':0,'websites_gained':0,'retry_outcomes':[],'legal_page_resumes':0,'legal_requests':0,'legal_websites_gained':0,'extra_allowance':{'http':0,'dns':0}}
        if exact(envelope): continue
        session=http.discovery_sessions.get(org)
        if not session:
            record['state']='pass1_not_prepared'; continue
        if time.monotonic() >= cutoff:
            stop = record['state'] = 'deadline'
            continue
        context=dict(session['context'])
        try:
            context['nav_homepages']=nav_homepages(envelope,index,http.blobs)
        except OSError as exc:
            company_io_failure(envelope, record, exc, update, 'website', 'nomination')
            continue
        retry_candidates=[]
        if http.config.adaptive_extra_budget:
            retry_candidates=[(item['candidate'],item['reason']) for item in session.get('transient_failures',{}).values()
                              if item['candidate'].origin in STRONG]
        current_site=any(c.field=='official_website' and c.availability=='available' and not c.carried_forward for c in envelope.claims)
        retry_keys={candidate_key(c) for c,_ in retry_candidates}
        legal_candidates=[] if current_site else [(c,'legal_pages') for key,c in getattr(http,'legal_resumable',{}).get(org,{}).items() if key not in retry_keys]
        for candidate,retry_reason in legal_candidates+retry_candidates+[(c,None) for c in generate(context,limit=32)]:
            key=candidate_key(candidate)
            if (key in session['attempted'] and not retry_reason) or candidate.domain in session['vetoed']: continue
            if (org,key) in queued: continue
            queued.add((org,key)); record['candidates']+=1
            heapq.heappush(heap,(-1000 if retry_reason=='legal_pages' else -priority(candidate)-int(bool(retry_reason))*10,org,candidate.url,candidate,retry_reason))
        if record['candidates']:record['state']='queued'
    budget.phase='pass2'
    try:
        while heap and not stop:
            _,org,_,candidate,retry_reason=heapq.heappop(heap)
            envelope=envelopes[org];record=records[org]
            if 'error' in record:continue
            if exact(envelope):continue
            if candidate.domain in http.discovery_sessions[org]['vetoed']:continue
            try:budget.check_website()
            except SourceFailure:stop='deadline'
            if len(budget.events)>=budget.cap:stop='budget_exhausted'
            if stop:
                record['state']=stop
                break
            if http.config.adaptive_extra_budget and org not in http.pass2_allowances:
                grant={'http':min(5,max(0,budget.cap-len(budget.events))),'dns':4}
                http.pass2_allowances[org]=grant
                record['extra_allowance']=dict(grant)
            if room(http,org)<=0:
                record['state']='website_budget_exhausted';continue
            if not dns_room(http,org,candidate):
                record['state']='dns_budget_exhausted';continue
            before=len(budget.events)
            retry=None
            legal_resume=retry_reason=='legal_pages'
            if legal_resume:record['legal_page_resumes']+=1
            if retry_reason and not legal_resume:
                cache_action=http.prepare_retry(candidate,org,http.discovery_sessions[org].get('proved',()))
                if cache_action=='not_allowed':continue
                http.discovery_sessions[org]['attempted'].discard(candidate_key(candidate))
                http.discovery_sessions[org].get('transient_failures',{}).pop(candidate_key(candidate),None)
                retry={'url':candidate.url,'origin':candidate.origin,'pass1_reason':retry_reason,'cache_action':cache_action}
                record['retry_outcomes'].append(retry)
            record['attempts']+=1
            timeout = asyncio.timeout(max(0, budget.website_deadline - time.monotonic()))
            discovery_end = None
            error_family, error_phase = 'website', 'discovery'
            try:
                async with timeout:
                    section=await collector.fetch(org,envelope,bulk.get(org),http,previous.get(org),
                                                  resume=True,candidates_override=[candidate],**({'legal_resume':True} if legal_resume else {}))
                    discovery_end = len(budget.events)
                    update(envelope,'website',section)
                    record['state']='verified' if exact(envelope) else 'checked_no_gain'
                    if exact(envelope):
                        record['websites_gained']=1
                        if http.config.public_activity:
                            error_family, error_phase = 'activity', 'public_activity'
                            await refresh_activity(org,envelope)
                        if http.config.hiring:
                            error_family, error_phase = 'hiring', 'careers'
                            from . import careers
                            section=await careers.fetch(org,envelope,http,http.accepted_pages.get(org,[]))
                            update(envelope,'hiring',careers.merge(envelope,section))
            except SourceFailure as exc:
                record['state']=exc.code
            except TimeoutError as exc:
                if not timeout.expired():
                    company_io_failure(envelope, record, exc, update, error_family, error_phase, candidate.url)
            except OSError as exc:
                company_io_failure(envelope, record, exc, update, error_family, error_phase, candidate.url)
                # Preserve an otherwise unfinished request receipt as a failure.
                for event in budget.events[before:]:
                    if event.get('organisation_number') == org and event.get('error') is None and 'runtime_ms' not in event:
                        event['error'] = type(exc).__name__
            if timeout.expired() or time.monotonic() >= cutoff:
                stop = 'deadline'
                if not exact(envelope) and 'error' not in record:
                    record['state'] = stop
            requests = sum(e.get('pass') == 'pass2' for e in budget.events[before:])
            record['requests'] += requests
            if legal_resume:
                record['legal_requests'] += sum(e.get('pass') == 'pass2' and e.get('section') == 'website'
                                                for e in budget.events[before:discovery_end])
                if exact(envelope):record['legal_websites_gained']=1
            if retry is not None:
                failure=http.discovery_sessions[org].get('transient_failures',{}).get(candidate_key(candidate))
                outcome='verified' if exact(envelope) else failure['reason'] if failure else envelope.run.sections.get('website')
                retry.update(outcome='deadline' if record['state'] == 'deadline' else outcome, requests=requests)
        if stop:
            for _, org, _, _, _ in heap:
                if not exact(envelopes[org]) and 'error' not in records[org]:
                    records[org]['state'] = stop
        for org,record in records.items():
            if record['state'] in {'deadline','budget_exhausted','website_budget_exhausted','dns_budget_exhausted'}:
                envelope=envelopes[org]
                envelope.errors.append(Error(section='website',code=record['state'],
                    message='Adaptive pass left nominations unchecked at the cumulative safety limit'))
                # Planning a wider pass does not rewrite pass 1's completed
                # checked scope. An attempted check still records its own
                # failure through collector.fetch/update above.
        finished = time.monotonic()
        company_errors = sum('error' in r for r in records.values())
        return {'state':('completed_with_errors' if company_errors else 'completed') if not stop else 'cut_off','stop_reason':stop,
            'company_errors': company_errors,
            'pass1':{'requests':0,'website_requests':0,
                     'verified_websites':pass1_websites,'websites_gained':pass1_websites},
            'pass2':{'requests':sum(r['requests'] for r in records.values()),
                     'website_requests':sum(e.get('pass')=='pass2' and e.get('section')=='website' for e in budget.events),
                     'websites_gained':sum(exact(e) for e in envelopes.values())-pass1_websites,
                     'runtime_seconds':round(finished-began,3),
                     'started_seconds':round(began-budget.start,3),
                     'finished_seconds':round(finished-budget.start,3),
                     'cutoff_seconds':round(cutoff-budget.start,3),
                     'states':dict(Counter(r['state'] for r in records.values())),
                     'retry_attempts':sum(t['cache_action']=='retried' for r in records.values() for t in r['retry_outcomes']),
                     'retry_outcomes':dict(Counter(t['outcome'] for r in records.values() for t in r['retry_outcomes'])),
                     'legal_priority':{'resumes':sum(r['legal_page_resumes'] for r in records.values()),'requests':sum(r['legal_requests'] for r in records.values()),'websites_gained':sum(r['legal_websites_gained'] for r in records.values())},
                     'per_company':records},
            'policy':'Pass 1 8/13 HTTP and 8 DNS; pass 2 up to +5 HTTP/+4 DNS from remaining global budget within a website-only cutoff; no counter reset; unchanged proof/robots/politeness; unvisited legal pages on unproved fetched sites precede new guesses'}
    finally:budget.phase='pass1'
