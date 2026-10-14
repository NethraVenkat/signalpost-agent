"""Optional paid discovery. Search results never become evidence or facts."""
import asyncio,json,os,time,httpx
from typing import Protocol
from urllib.parse import urlsplit
from .candidates import Candidate,legal_name
from .policy import normalize_url,domain,SOCIAL,DIRECTORIES,FREE_MAIL
from ..budget import SourceFailure
from ..workers import offload

ENDPOINT='https://api.search.brave.com/res/v1/web/search'
MARKETPLACES={'amazon.com','amazon.no','amazon.co.uk','ebay.com','ebay.no','etsy.com',
              'alibaba.com','aliexpress.com','mittanbud.no','anbudstorget.no','kompass.com',
              'europages.com','crunchbase.com','yelp.com','tripadvisor.com'}
GENERIC_DOMAINS={'gulesider.no','proff.no','purehelp.no','1881.no','180.no',
                 'ratsit.no','regnskapstall.no','allabolag.se','eniro.no',
                 'linkedin.com','facebook.com','instagram.com','twitter.com','x.com',
                 'youtube.com','tiktok.com','finn.no','mittanbud.no','anbudstorget.no',
                 'yellowpages.no','kompass.com','europages.com','crunchbase.com'}

class Provider(Protocol):
    async def search(self,query:str,timeout:float)->list[dict|str]: ...

class Brave:
    def __init__(self,client,key):self.client,self.key=client,key
    async def search(self,query,timeout):
        async with self.client.stream('GET',ENDPOINT,params={'q':query,'count':5},
                headers={'X-Subscription-Token':self.key,'Accept':'application/json'},
                timeout=timeout,follow_redirects=False) as response:
            if response.status_code!=200:
                raise SearchError(response.status_code,response.headers.get('Retry-After'))
            chunks=[];size=0
            async for chunk in response.aiter_bytes():
                size+=len(chunk)
                if size>512_000:raise SourceFailure('search_body_cap')
                chunks.append(chunk)
            data=await offload(json.loads,b''.join(chunks))
        results=[]
        for x in data.get('web',{}).get('results',[]):
            if isinstance(x,dict) and isinstance(x.get('url'),str):
                results.append({'url':x['url'],'title':x.get('title') or '','description':x.get('description') or ''})
        return results

class SearchError(Exception):
    def __init__(self,status,retry_after=None):self.status,self.retry_after=status,retry_after

import re
from .candidates import GENERIC

def score_identity(result,org,context):
    if isinstance(result,str):
        raw_url,title,snippet=result,'',''
    elif isinstance(result,dict):
        raw_url,title,snippet=result.get('url') or '',result.get('title') or '',result.get('description') or ''
    else:
        raw_url,title,snippet=getattr(result,'url',str(result)),getattr(result,'title',''),getattr(result,'description','')
    norm_url=normalize_url(raw_url)
    host=domain(norm_url) if norm_url else ''
    if not host or not norm_url:return 0,[]
    full_text=f"{raw_url} {title} {snippet}".casefold()
    host_clean=host.casefold().split('.')[0]
    host_compact=re.sub(r'[^a-z0-9]','',host_clean)
    name=legal_name(context.get('name'))
    brand=(context.get('brand') or '').casefold().strip()
    if not brand and name:
        tokens=[t for t in name.split() if t not in GENERIC and len(t)>=2]
        brand=tokens[0] if tokens else name
    score=0;signals=[];instant_win=False
    org_digits=re.sub(r'\D','',str(org or ''))
    if org_digits and len(org_digits)==9:
        pattern=r'\b'+r'[\s.]*'.join(list(org_digits))+r'\b'
        if re.search(pattern,snippet) or org_digits in re.sub(r'\D','',snippet):
            score+=50;signals.append('orgnr_in_snippet');instant_win=True
    if name:
        name_compact=re.sub(r'[^a-z0-9]','',name)
        name_match=(re.search(r'\b'+re.escape(name)+r'\b',full_text) or
                    (len(name_compact)>=4 and (name_compact in host_compact or host_compact in name_compact)))
        if name_match:
            score+=40;signals.append('legal_name_match')
    if brand:
        brand_compact=re.sub(r'[^a-z0-9]','',brand)
        title_clean=title.casefold()
        brand_match=(re.search(r'\b'+re.escape(brand)+r'\b',title_clean) or
                     (len(brand_compact)>=3 and brand_compact in host_compact))
        if brand_match:
            score+=30;signals.append('brand_match')
    if (host in GENERIC_DOMAINS or host in SOCIAL or host in DIRECTORIES or host in MARKETPLACES or host in FREE_MAIL or
        any(g in host for g in ('gulesider','proff','purehelp','1881','linkedin','facebook'))):
        score-=30;signals.append('generic_domain_penalty');instant_win=False
    if instant_win and score<60:
        score=60
    return score,signals

def brave_search_mock(company_name, brand=None, orgnr=None, limit=5):
    if not company_name:
        return []
    clean = re.sub(r' site:\.no\b', '', str(company_name)).strip()
    words = re.findall(r'[a-z0-9æøå]+', clean.lower())
    if not words:
        return []
    slug = ''.join(words)
    hyphen_slug = '-'.join(words)
    brand_str = brand or (words[0] if words else '')
    brand_slug = re.sub(r'[^a-z0-9æøå]', '', brand_str.lower())
    orgnr_str = str(orgnr or '')

    candidates_raw = [
        {
            'domain': f"{slug}.no",
            'url': f"https://{slug}.no",
            'title': clean,
            'snippet': f"Offisiell nettside for {clean}. Org nr {orgnr_str} registrert i Enhetsregisteret." if orgnr_str else f"Offisiell nettside for {clean}."
        },
        {
            'domain': f"{hyphen_slug}.no",
            'url': f"https://{hyphen_slug}.no",
            'title': f"{clean} - {brand_str}",
            'snippet': f"{clean} og {brand_str} virksomhet, tjenester og kontaktinformasjon."
        },
        {
            'domain': f"{brand_slug}.no" if brand_slug else f"{slug}-holding.no",
            'url': f"https://{brand_slug}.no" if brand_slug else f"https://{slug}-holding.no",
            'title': brand_str or clean,
            'snippet': f"{clean} merkevare og produktportal."
        },
        {
            'domain': "proff.no",
            'url': f"https://proff.no/selskap/{slug}",
            'title': f"Proff: {clean}",
            'snippet': f"Regnskapstall og roller for {clean}."
        },
        {
            'domain': "dagensnyheter.no",
            'url': "https://dagensnyheter.no/article/123",
            'title': "Dagens Næringsliv",
            'snippet': "Næringslivsnyheter og børsoppdateringer."
        },
        {
            'domain': f"{slug}-as.no",
            'url': f"https://{slug}-as.no",
            'title': f"{clean} AS",
            'snippet': f"Nettsted for {clean}. Foretaksnummer {orgnr_str}." if orgnr_str else f"Nettsted for {clean} AS."
        },
        {
            'domain': f"{slug}-gruppen.no",
            'url': f"https://{slug}-gruppen.no",
            'title': f"{clean} Gruppen",
            'snippet': f"Konsernportal for {clean} og datterselskaper."
        },
        {
            'domain': f"mitt-{slug}.no",
            'url': f"https://mitt-{slug}.no",
            'title': f"Portalside for {clean}",
            'snippet': f"Kontakt og informasjon om {clean}."
        }
    ]

    context = {'name': clean, 'brand': brand_str}
    results = []
    for cand in candidates_raw:
        score, signals = score_identity(
            {'url': cand['url'], 'title': cand['title'], 'description': cand['snippet']},
            orgnr_str, context
        )
        if score >= 60:
            results.append({
                'domain': cand['domain'],
                'title': cand['title'],
                'snippet': cand['snippet'],
                'url': cand['url'],
                'score': score,
                'signals': signals
            })
            if len(results) >= limit:
                break
    return results

class MockBraveProvider:
    async def search(self, query: str, timeout: float) -> list[dict]:
        clean = re.sub(r' site:\.no\b', '', query).strip()
        words = re.findall(r'[a-z0-9æøå]+', clean.lower())
        brand = words[0] if words else ''
        mocked = brave_search_mock(clean, brand=brand, limit=15)
        return [{'url': m.get('url', f"https://{m['domain']}"), 'title': m['title'], 'description': m['snippet']} for m in mocked]

class Search:
    def __init__(self,client,config,budget,provider=None):
        self.config,self.budget=config,budget;self.provider=provider;self.seen=set();self.lock=asyncio.Lock();self.sem=asyncio.Semaphore(2);self.next_start=0
        name=(os.environ.get('SIGNALPOST_SEARCH_PROVIDER') or 'brave').lower()
        key=os.environ.get('BRAVE_SEARCH_API_KEY')
        if provider is None and name=='brave' and key:self.provider=Brave(client,key)
        elif provider is None and (name in ('mock', 'mock_search') or os.environ.get('SIGNALPOST_SEARCH_MOCK')=='1'):
            self.provider=MockBraveProvider()
        self.metrics={'status':'configured' if self.provider else 'not configured','provider':name if self.provider else None,
            'queries':0,'companies_queried':0,'estimated_usd':0.,'unit_price_usd':config.search_unit_price_usd,
            'price_note':'verify before use; retries count as billable queries; no free credit assumed',
            'errors':0,'cap_skips':0,'result_domains':0}
        from ..io.input_adapter import read
        self.cap=config.search_max_queries if config.search_max_queries is not None else len(read(config.organisations).unique)
    def room(self,org,http):
        total=sum(e['organisation_number']==org for e in self.budget.events)
        # Keep room for a query plus robots and a proof page. Never raise caps.
        return (self.provider is not None and len(self.budget.events)+3<=self.budget.cap and
            total+3<=self.config.website_total_request_cap and
            http.counts.get(org,0)+2<=self.config.website_request_cap and
            http.dns_counts.get(org,0)<8)
    async def nominate(self,org,context,http):
        if org in self.seen or not self.room(org,http):return []
        name=legal_name(context.get('name'))
        if not name:return []
        self.seen.add(org);self.metrics['companies_queried']+=1
        brand=(context.get('brand') or '').strip()
        query=f"{name} {brand} site:.no".strip() if (brand and brand!=name) else f"{name} site:.no".strip()
        results=[]
        async with self.sem:
            for attempt in range(2):
                async with self.lock:
                    if (self.metrics['queries']>=self.cap or
                        (self.metrics['queries']+1)*self.config.search_unit_price_usd>self.config.search_max_cost_usd or
                        not self.room(org,http)):
                        self.metrics['cap_skips']+=1;return []
                    await asyncio.sleep(max(0,self.next_start-time.monotonic()))
                    try:event=self.budget.reserve(ENDPOINT,urlsplit(ENDPOINT).hostname,org)
                    except SourceFailure:return []
                    event['section']='search';self.metrics['queries']+=1
                    self.metrics['estimated_usd']=self.metrics['queries']*self.config.search_unit_price_usd
                    began=time.monotonic();self.next_start=began+1
                    try:
                        remaining=min(8,max(.001,self.budget.deadline-time.monotonic()))
                        async with asyncio.timeout(remaining):results=await self.provider.search(query,remaining)
                        event['status']=200;break
                    except Exception as exc:
                        self.metrics['errors']+=1;event['error']='search_provider_error'
                        status=exc.status if isinstance(exc,SearchError) else None;event['status']=status
                        retryable=status in {429,500,502,503,504} or isinstance(exc,(TimeoutError,httpx.TimeoutException,httpx.NetworkError))
                        if attempt or not retryable:return []
                        delay=1.
                        if isinstance(exc,SearchError) and exc.retry_after:
                            from email.utils import parsedate_to_datetime
                            from datetime import datetime,timezone
                            try:delay=max(delay,float(exc.retry_after))
                            except ValueError:
                                try:delay=max(delay,(parsedate_to_datetime(exc.retry_after)-datetime.now(timezone.utc)).total_seconds())
                                except (ValueError,TypeError):return []
                        if delay>8 or time.monotonic()+delay>=self.budget.deadline:return []
                        self.next_start=max(self.next_start,time.monotonic()+delay)
                    finally:event['runtime_ms']=round((time.monotonic()-began)*1000)
        scored=[];seen=set()
        for raw in results:
            score,sigs=score_identity(raw,org,context)
            if score<60:continue
            raw_url=raw.get('url') if isinstance(raw,dict) else (raw if isinstance(raw,str) else getattr(raw,'url',''))
            url=normalize_url(raw_url);host=domain(url) if url else ''
            if not host or host in seen or host in SOCIAL|DIRECTORIES|FREE_MAIL|MARKETPLACES:continue
            seen.add(host);cand=Candidate(url,host,'search_brave')
            scored.append((score,cand))
        scored.sort(key=lambda x:x[0],reverse=True)
        output=[cand for _,cand in scored[:15]]
        self.metrics['result_domains']+=len(output)
        return output
