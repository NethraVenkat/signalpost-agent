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

class Provider(Protocol):
    async def search(self,query:str,timeout:float)->list[str]: ...

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
        return [x['url'] for x in data.get('web',{}).get('results',[]) if isinstance(x,dict) and isinstance(x.get('url'),str)]

class SearchError(Exception):
    def __init__(self,status,retry_after=None):self.status,self.retry_after=status,retry_after

class Search:
    def __init__(self,client,config,budget,provider=None):
        self.config,self.budget=config,budget;self.provider=provider;self.seen=set();self.lock=asyncio.Lock();self.next_start=0
        name=(os.environ.get('SIGNALPOST_SEARCH_PROVIDER') or 'brave').lower()
        key=os.environ.get('BRAVE_SEARCH_API_KEY')
        if provider is None and name=='brave' and key:self.provider=Brave(client,key)
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
        query='"'+name+'" '+str(context.get('municipality') or '')
        urls=[]
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
                    async with asyncio.timeout(remaining):urls=await self.provider.search(query,remaining)
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
        output=[];seen=set()
        for raw in urls:
            url=normalize_url(raw);host=domain(url) if url else ''
            if not host or host in seen or host in SOCIAL|DIRECTORIES|FREE_MAIL|MARKETPLACES:continue
            seen.add(host);output.append(Candidate(url,host,'search_brave'))
            if len(output)==5:break
        self.metrics['result_domains']+=len(output)
        return output
