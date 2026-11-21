"""Bounded official-source outage retries; no identity or evidence relaxation."""
import asyncio,time,math,email.utils
from collections import Counter
from urllib.parse import urlsplit
from ..budget import SourceFailure

BACKOFF=(5.0,20.0)
OFFICIAL_ROBOTS_BACKOFF=(*BACKOFF,40.0,60.0)
DNS_FAILURES={'no_such_domain','dns_error','dns_timeout','dns_unavailable'}
OFFICIAL={'data.brreg.no','pam-stilling-feed.nav.no','api.gleif.org','api.ted.europa.eu',
          'api.finanstilsynet.no','stottetiltak-registerinfo-api.app.brreg.no'}

def retry_after(value):
    if not value:return 0.0
    try:delay=float(value)
    except (TypeError,ValueError):
        try:delay=email.utils.parsedate_to_datetime(value).timestamp()-time.time()
        except (TypeError,ValueError,OverflowError):return 0.0
    return max(0.0,delay) if math.isfinite(delay) else 0.0


async def pause(budget,event,attempt,minimum=0,deadline=None,backoff=BACKOFF):
    budget.check()
    if len(budget.events)>=budget.cap:raise SourceFailure('budget_exhausted')
    delay=max(backoff[attempt],minimum)
    event['official_retry_backoff_seconds']=delay
    if time.monotonic()+delay>=min(budget.deadline,deadline if deadline is not None else budget.deadline):
        event['official_retry_state']='deadline_before_retry'
        raise SourceFailure('deadline')
    await asyncio.sleep(delay)
    budget.check()
    event['official_retry_state']='retrying'

def summary(events,health):
    outages=[];counts=Counter()
    for i,e in enumerate(events):
        if e['host'] not in OFFICIAL:continue
        status=e.get('status')
        if not (e.get('official_transient') or isinstance(status,int) and status>=500):continue
        later=[x for x in events[i+1:] if x['url']==e['url'] and x['organisation_number']==e['organisation_number'] and x.get('method','GET')==e.get('method','GET')]
        recovery=any(x.get('status') is not None and x['status']<500 and x['status']!=429 and not x.get('error') for x in later)
        counts['transient_attempts']+=1
        counts['recovered_attempts' if recovery else 'unrecovered_attempts']+=1
        outages.append({'host':e['host'],'url':e['url'],'organisation_number':e['organisation_number'],'status':status,'error':e.get('error'),'recovered_by_later_attempt':recovery,'retry_state':e.get('official_retry_state')})
    return {'health_checks':health,'counts':dict(counts),'attempts':outages,'policy':'Official data requests: up to two transient retries (5/20 seconds). Official API robots GETs where required: up to four (5/20/40/60 seconds). Original request and time limits apply.','recovery_definition':'A later same URL/org/method response below500(excluding429), without transport error; not proof of company-data availability or identity'}


def check_source(budget,url):
    for prefix,reason in getattr(budget,'source_outages',{}).items():
        if url.startswith(prefix):raise SourceFailure('source_outage_'+reason)


async def health_check(client,config,budget):
    """Bounded reachability checks, not company proof; never persist NAV tokens."""
    import httpx
    specs=[('enhetsregisteret','https://data.brreg.no/enhetsregisteret/','https://data.brreg.no/enhetsregisteret/api/enheter?size=1'),
           ('accounts','https://data.brreg.no/regnskapsregisteret/','https://data.brreg.no/regnskapsregisteret/regnskap')]
    if config.hiring:specs.append(('nav','https://pam-stilling-feed.nav.no/','https://pam-stilling-feed.nav.no/api/publicToken'))
    if config.gleif:specs.append(('gleif','https://api.gleif.org/','https://api.gleif.org/robots.txt'))
    budget.source_outages={}
    end=min(budget.deadline,time.monotonic()+45)
    async def probe(name,prefix,url):
        result={'source':name,'url':url,'method':'HEAD','state':'pending','attempts':0,'note':'Reachability only; 404/405 is reachable, not evidence of usable company data'}
        # A robots HEAD probe is diagnostic. The authoritative GET has its own
        # retry policy and must decide access before any dependent request.
        gate_source = not url.endswith('/robots.txt')
        for attempt in range(3):
            event=None
            try:
                budget.check()
                if time.monotonic()>=end:raise SourceFailure('health_deadline')
                event=budget.reserve(url,urlsplit(url).hostname,'__official_source_health__')
                event.update(section='official_source_health',method='HEAD')
                result['attempts']+=1;begin=time.monotonic()
                try:
                    timeout=min(5,config.request_timeout,max(.001,end-time.monotonic()))
                    async with asyncio.timeout(timeout):
                        r=await client.head(url,timeout=timeout,follow_redirects=False)
                    event['status']=r.status_code;result['status']=r.status_code
                    if r.status_code<500 and r.status_code not in {401,403,429}:
                        result['state']='reachable';return result
                    if r.status_code in {401,403,429}:
                        result['state']='refused_or_rate_limited';result['reason']='http_'+str(r.status_code)
                        if gate_source:budget.source_outages[prefix]=name
                        return result
                    event['official_transient']=True;result['reason']='http_'+str(r.status_code)
                except (TimeoutError,httpx.TimeoutException,httpx.NetworkError,httpx.ProtocolError) as exc:
                    event.update(error=type(exc).__name__,official_transient=True);result['reason']=type(exc).__name__
                except SourceFailure as exc:
                    event['error']=exc.code
                    if exc.code not in DNS_FAILURES:raise
                    event['official_transient']=True;result['reason']=exc.code
                finally:event['runtime_ms']=round((time.monotonic()-begin)*1000)
                if attempt<2:await pause(budget,event,attempt,minimum=retry_after(r.headers.get('Retry-After')) if event.get('status') else 0,deadline=end)
            except SourceFailure as exc:
                result.update(state='cut_off',reason=exc.code)
                if gate_source and event is not None and event.get('official_transient'):budget.source_outages[prefix]=name
                return result
        result['state']='unavailable'
        if gate_source:budget.source_outages[prefix]=name
        return result
    return await asyncio.gather(*(probe(*s) for s in specs))
