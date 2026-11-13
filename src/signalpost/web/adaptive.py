"""Spend only unused cumulative website allowance on ranked, untried nominations."""
import heapq
import json
import time
from collections import Counter
from datetime import datetime, timezone
from urllib.parse import urlsplit

from ..budget import SourceFailure
from ..models.envelope import Error
from . import collector
from .candidates import generate, candidate_key
from .policy import normalize_url

ORIGIN_SCORE = {'registry_website':100, 'registry_email':95,
    'subunit_registry_website':90, 'subunit_registry_email':88,
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
    nonweb=sum(e['organisation_number']==org and e.get('section')!='website' for e in http.budget.events)
    return max(0,min(8,http.config.website_request_cap,http.config.website_total_request_cap-nonweb)-http.counts.get(org,0))


def dns_room(http, org, candidate):
    host=urlsplit(candidate.url).hostname
    return (candidate.origin=='registry_website' or not http.config.dns_precheck
            or host in http.dns_cache or (org,host.removeprefix('www.')) in http.dns_nominations
            or http.dns_counts.get(org,0)<8)


async def run(envelopes, http, index, bulk, previous, update, refresh_activity):
    """Pass 1 finishes globally before this deterministic priority queue starts.

    Neither HTTP counters, nomination counters, caches nor the original deadline
    are reset. A per-company slice is a cumulative ceiling, not a new allowance.
    """
    began=time.monotonic(); budget=http.budget
    start=len(budget.events); pass1_websites=sum(exact(e) for e in envelopes.values())
    records={}; heap=[]; queued=set()
    for org,envelope in sorted(envelopes.items()):
        record=records[org]={'state':'already_verified' if exact(envelope) else 'no_pending_candidates',
                            'candidates':0,'attempts':0,'requests':0,'websites_gained':0}
        if exact(envelope): continue
        session=http.discovery_sessions.get(org)
        if not session:
            record['state']='pass1_not_prepared'; continue
        context=dict(session['context'])
        context['nav_homepages']=nav_homepages(envelope,index,http.blobs)
        for candidate in generate(context,limit=32):
            key=candidate_key(candidate)
            if key in session['attempted'] or candidate.domain in session['vetoed']: continue
            if (org,key) in queued: continue
            queued.add((org,key)); record['candidates']+=1
            heapq.heappush(heap,(-priority(candidate),org,candidate.url,candidate))
        if record['candidates']:record['state']='queued'
    budget.phase='pass2'
    stop=None
    try:
        while heap:
            _,org,_,candidate=heapq.heappop(heap)
            envelope=envelopes[org];record=records[org]
            if exact(envelope):continue
            if candidate.domain in http.discovery_sessions[org]['vetoed']:continue
            try:budget.check()
            except SourceFailure:stop='deadline'
            if len(budget.events)>=budget.cap:stop='budget_exhausted'
            if stop:
                record['state']=stop
                for _,other,_,_ in heap:
                    if not exact(envelopes[other]):records[other]['state']=stop
                break
            if room(http,org)<=0:
                record['state']='website_budget_exhausted';continue
            if not dns_room(http,org,candidate):
                record['state']='dns_budget_exhausted';continue
            before=len(budget.events)
            record['attempts']+=1
            try:
                section=await collector.fetch(org,envelope,bulk.get(org),http,previous.get(org),
                                              resume=True,candidates_override=[candidate])
                update(envelope,'website',section)
                record['state']='verified' if exact(envelope) else 'checked_no_gain'
                if exact(envelope):
                    record['websites_gained']=1
                    if http.config.public_activity:await refresh_activity(org,envelope)
            except SourceFailure as exc:
                record['state']=exc.code
            record['requests']+=len(budget.events)-before
        for org,record in records.items():
            if record['state'] in {'deadline','budget_exhausted','website_budget_exhausted','dns_budget_exhausted'}:
                envelope=envelopes[org]
                envelope.errors.append(Error(section='website',code=record['state'],
                    message='Adaptive pass left nominations unchecked at the cumulative safety limit'))
                # Planning a wider pass does not rewrite pass 1's completed
                # checked scope. An attempted check still records its own
                # failure through collector.fetch/update above.
        return {'state':'completed' if not stop else 'cut_off','stop_reason':stop,
            'pass1':{'requests':start,'website_requests':sum(e.get('section')=='website' for e in budget.events[:start]),
                     'verified_websites':pass1_websites,'websites_gained':pass1_websites},
            'pass2':{'requests':len(budget.events)-start,
                     'website_requests':sum(e.get('section')=='website' for e in budget.events[start:]),
                     'websites_gained':sum(exact(e) for e in envelopes.values())-pass1_websites,
                     'runtime_seconds':round(time.monotonic()-began,3),
                     'states':dict(Counter(r['state'] for r in records.values())), 'per_company':records},
            'policy':'same cumulative 8/13 HTTP and eight DNS nominations; no reset; unchanged proof/robots/politeness'}
    finally:budget.phase='pass1'
