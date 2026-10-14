"""Concurrent feed producer and bounded, ranked NAV detail consumers."""
import asyncio
import heapq
import json
import os
import time
import threading
from functools import wraps
from concurrent.futures import ThreadPoolExecutor
from collections import Counter,defaultdict
from datetime import datetime,timedelta,timezone
from email.utils import format_datetime
from uuid import UUID
from ..budget import SourceFailure
from ..identity.orgnr import valid
from .nav import (BASE,NavHttp,Ad,allowed,time_cap,token_from,timestamp,header_name,
                  name_tokens,name_matches,distinctive_tokens,rarity_limit,COMMON_BUSINESS)


def version(record):
    return (record[0],record[1]['_feed_entry']['status'],header_name(record[1]))


def locked(fn):
    @wraps(fn)
    def wrapped(self,*args,**kwargs):
        with self.lock:return fn(self,*args,**kwargs)
    return wrapped


class Stream:
    def __init__(self,http,index,config,previous,began,unfiltered):
        self.lock=threading.RLock();self.loop=asyncio.get_running_loop()
        self.http,self.index,self.config,self.previous,self.began=http,index,config,previous or {},began
        self.unfiltered=unfiltered;self.names=None;self.token_orgs=defaultdict(set)
        self.latest={};self.active={};self.frequency=Counter();self.discovered=set()
        self.pending={};self.heap=[];self.checked={};self.failed={};self.capped=set();self.inflight=0;self.serial=0
        self.changed=asyncio.Event();self.waiters=[];self.done=False;self.page_complete=False;self.names_complete=False;self.errors=[]

    def wake(self):
        for event in list(self.waiters):self.loop.call_soon_threadsafe(event.set)

    @locked
    def classify(self,record):
        name=header_name(record[1])
        if self.unfiltered or not name:return 0,set(self.names or {})
        if not self.config.nav_rank_candidates:
            return 0,{org for org,known in self.names.items() if any(name_matches(name,c) for c in known)}
        tokens=distinctive_tokens(name,self.frequency,len(self.active))
        possible=set().union(*(self.token_orgs[t] for t in tokens)) if tokens else set()
        affected={org for org in possible if any(name_matches(name,c) for c in self.names[org])}
        score=max((sum(1/max(1,self.frequency[t]) for t in sorted(tokens & name_tokens(c)))
                   for org in affected for c in self.names[org]),default=0)
        return score,affected

    @locked
    def drop_ad(self,uuid):
        for org,ads in self.index.ads.items():self.index.ads[org]=[a for a in ads if a.value['uuid']!=uuid]

    @locked
    def offer(self,uuid):
        if self.names is None:return
        record=self.latest[uuid]
        if uuid not in self.active:
            self.pending.pop(uuid,None);return
        score,affected=self.classify(record)
        if not self.unfiltered and header_name(record[1]) and not affected:
            self.pending.pop(uuid,None);return
        self.discovered.add(uuid)
        self.index.metrics['detail_request_cap']=(self.config.nav_max_details if self.config.nav_max_details is not None
            else min(len(self.discovered),max(300,2*len(self.names))))
        v=version(record)
        if self.checked.get(uuid)==v or self.failed.get(uuid)==v:return
        if uuid in self.pending and version(self.pending[uuid][0])==v:return
        self.pending[uuid]=(record,affected);self.serial+=1
        heapq.heappush(self.heap,(-score,uuid,self.serial,v))
        self.wake()

    @locked
    def ready(self,names):
        self.names=names
        self.token_orgs.clear()
        for org,known in names.items():
            for name in known:
                for token in name_tokens(name)-COMMON_BUSINESS:self.token_orgs[token].add(org)
        for uuid in sorted(self.active):self.offer(uuid)
        self.refresh_pending()
        self.wake()

    @locked
    def refresh_pending(self):
        heap=[]
        for uuid,(record,_) in sorted(self.pending.items()):
            score,affected=self.classify(record)
            if uuid not in self.active or (not self.unfiltered and header_name(record[1]) and not affected):
                self.pending.pop(uuid,None);continue
            self.pending[uuid]=(record,affected);self.serial+=1
            heap.append((-score,uuid,self.serial,version(record)))
        heapq.heapify(heap);self.heap=heap

    @locked
    def page(self,items,sha,url,retrieved):
        old_limit=rarity_limit(len(self.active));changed=set();recheck=False
        for n,item in enumerate(items):
            entry=item.get('_feed_entry') or {};status=entry.get('status')
            if status not in {'ACTIVE','INACTIVE','DELETED'}:raise SourceFailure('nav_unknown_status')
            try:uuid=str(UUID(entry.get('uuid') or item.get('id')))
            except (ValueError,TypeError,AttributeError):raise SourceFailure('nav_invalid_uuid') from None
            at=timestamp(item.get('date_modified') or entry.get('sistEndret'))
            if at is None:raise SourceFailure('nav_invalid_modified_date')
            old=self.latest.get(uuid)
            if old and at<old[0]:continue
            if old and old[1]==item:continue
            if old and uuid in self.active:
                for t in name_tokens(header_name(old[1])):
                    self.frequency[t]-=1
                    if self.frequency[t]==old_limit:recheck=True
            record=(at,item,sha,url,'/items/'+str(n),retrieved)
            self.latest[uuid]=record;changed.add(uuid)
            if uuid in self.checked and self.checked[uuid]!=version(record):self.drop_ad(uuid)
            if status=='ACTIVE':
                self.active[uuid]=record;self.index.closed.discard(uuid)
                self.frequency.update(name_tokens(header_name(item)))
            else:
                self.active.pop(uuid,None);self.index.closed.add(uuid)
                if uuid in self.discovered:self.drop_ad(uuid)
        # A threshold increase or token-frequency fall may make an earlier header eligible.
        if recheck or rarity_limit(len(self.active))!=old_limit:changed.update(self.active)
        for uuid in sorted(changed):self.offer(uuid)
        if self.names is not None:self.refresh_pending()

    async def detail(self,uuid,record,affected):
        _,item,page_sha,page_url,locator,page_retrieved=record
        try:
            if 'first_detail_seconds' not in self.index.metrics:
                self.index.metrics['first_detail_seconds']=time.monotonic()-self.began
                self.index.metrics['first_detail_page_number']=self.index.metrics['pages']
                self.index.metrics['details_started_before_feed_complete']=not self.page_complete
            url=allowed(item['url'])
            _,body,sha,retrieved=await self.http.get(url,self.token,companies=affected)
            self.index.metrics['details']+=1;entry=await asyncio.to_thread(json.loads,body)
            if str(entry.get('uuid'))!=uuid:raise SourceFailure('nav_wrong_ad')
            if entry.get('status') not in {'ACTIVE','INACTIVE','DELETED'}:raise SourceFailure('nav_unknown_status')
            if entry['status']!='ACTIVE':await asyncio.to_thread(self.record_closed,uuid);return True
            ad=entry.get('ad_content')
            if not isinstance(ad,dict) or str(ad.get('uuid'))!=uuid:raise SourceFailure('nav_malformed_ad')
            expires=timestamp(ad.get('expires'));published=timestamp(ad.get('published'))
            if expires is None or published is None:raise SourceFailure('nav_invalid_dates')
            now=datetime.now(timezone.utc)
            if expires<=now or published>now:await asyncio.to_thread(self.record_closed,uuid);return True
            org=str((ad.get('employer') or {}).get('orgnr') or '').strip()
            if not valid(org):return True
            value={'uuid':uuid,'employer_orgnr':org,'title':ad.get('title') or None,
                   'location':[{'municipality':x.get('municipal'),'city':x.get('city')} for x in ad.get('workLocations',[])] or None,
                   'published':ad['published'],'expires':ad['expires'],'occupation_categories':ad.get('occupationCategories') or None,
                   'url':'https://arbeidsplassen.nav.no/stillinger/stilling/'+uuid}
            value['availability']={'location':'available' if value['location'] else 'not_available',
                                   'occupation_categories':'available' if value['occupation_categories'] else 'not_available'}
            if not value['title']:raise SourceFailure('nav_missing_title')
            # A newer feed version can arrive during this request. Never label an older proof fresh.
            await asyncio.to_thread(self.record_ad,uuid,record,org,Ad(value,sha,url,retrieved,page_sha,page_url,locator,page_retrieved))
            return True
        except asyncio.CancelledError:raise
        except Exception as exc:
            if isinstance(exc,SourceFailure) and exc.code=='nav_detail_cap':self.capped.add(uuid)
            self.errors.append(exc.code if isinstance(exc,SourceFailure) else type(exc).__name__)
            return False

    @locked
    def record_closed(self,uuid):self.index.closed.add(uuid)

    @locked
    def record_ad(self,uuid,record,org,ad):
        if version(self.latest[uuid])==version(record):
            self.drop_ad(uuid);self.index.ads.setdefault(org,[]).append(ad)

    @locked
    def take(self):
        cap=self.index.metrics.get('detail_request_cap',0)
        if self.names is not None and self.index.metrics.get('detail_requests',0)+self.inflight<cap:
            while self.heap:
                _,uuid,_,v=heapq.heappop(self.heap);current=self.pending.get(uuid)
                if current is not None and version(current[0])==v:
                    record,affected=self.pending.pop(uuid);self.inflight+=1
                    return (uuid,record,affected),False
        return None,self.done and self.names_complete

    @locked
    def checked_detail(self,uuid,record,good):
        self.inflight-=1
        if uuid not in self.capped:(self.checked if good else self.failed)[uuid]=version(record)
        self.wake()

    async def worker(self):
        event=asyncio.Event();self.waiters.append(event)
        while True:
            event.clear()
            job,done=await asyncio.to_thread(self.take)
            if job:
                uuid,record,affected=job;good=await self.detail(uuid,record,affected)
                await asyncio.to_thread(self.checked_detail,uuid,record,good)
            elif done:return
            else:await event.wait()

    @locked
    def settle(self):
        index=self.index;incomplete=set();active_candidates=[]
        if self.names is not None:
            if self.active and not self.unfiltered:
                incomplete.update(org for org,names in self.names.items()
                    if not any(distinctive_tokens(n,self.frequency,len(self.active)) for n in names))
            unusable=set(incomplete)
            for uuid,record in self.active.items():
                _,affected=self.classify(record)
                if self.unfiltered or not header_name(record[1]) or affected:
                    active_candidates.append(uuid)
                    if self.checked.get(uuid)!=version(record):incomplete.update(affected)
            for org,row in self.previous.items():
                for c in row.get('claims',row.get('profile',{}).get('claims',[])):
                    if c.get('family')=='hiring' and c.get('availability')=='available' and isinstance(c.get('value'),dict):
                        uuid=c['value'].get('uuid')
                        if uuid in self.active and org not in self.classify(self.active[uuid])[1]:incomplete.add(org)
            index.metrics['name_unusable_companies']=len(unusable)
            index.metrics['companies_with_unchecked_candidates']=len(incomplete-unusable)
        index.incomplete_orgs=incomplete
        index.coverage_ready=self.page_complete and self.names_complete and self.config.nav_lookback_days>=185
        unchecked=[u for u in active_candidates if self.checked.get(u)!=version(self.active[u])]
        cap_exhausted=self.index.metrics.get('detail_requests',0)>=self.index.metrics.get('detail_request_cap',0)
        capped=[u for u in unchecked if self.failed.get(u)!=version(self.active[u])] if cap_exhausted else []
        index.complete=index.coverage_ready and not incomplete and not unchecked and not self.errors
        if unchecked and self.index.metrics.get('detail_requests',0)>=self.index.metrics.get('detail_request_cap',0):
            self.errors.append('nav_detail_cap')
        index.metrics.update({'active_headers':len(self.active),'candidate_headers':len(active_candidates),
            'distinct_candidate_ads':len(self.discovered),'active_candidate_ads':len(active_candidates),
            'cap_hits':len(capped),'failed_detail_ads':len(self.failed),'rare_token_max_headers':rarity_limit(len(self.active)),
            'headers_with_employer_name':sum(bool(header_name(r[1])) for r in self.active.values()),
            'headers_without_employer_name':sum(not header_name(r[1]) for r in self.active.values()),
            'name_prefilter':not self.unfiltered,'ranking_enabled':self.config.nav_rank_candidates,
            'coverage_scope':'batch_legal_brand_subunit_name_candidates' if not self.unfiltered else 'all_active_headers',
            'detail_concurrency':self.config.nav_concurrency})


async def prefetch(client,config,budget,blobs,index,names_ready=None,previous=None):
    began=time.monotonic();http=NavHttp(client,config,budget,blobs,index)
    state=Stream(http,index,config,previous,began,names_ready is None);tasks=[];paging_began=None
    page_pool=ThreadPoolExecutor(max_workers=1,thread_name_prefix='nav-headers');page_jobs=[]
    index.metrics.update({'feed_complete':False,'time_cap_seconds':time_cap(config),
                          'detail_request_cap':config.nav_max_details if config.nav_max_details is not None else 0})
    try:
        async with asyncio.timeout(time_cap(config)):
            token=token_from(os.environ.get('NAV_API_TOKEN'));from_environment=bool(token)
            state.token=token or await http.public_token()
            if not state.token:index.blocked=True;index.reason='token_unavailable';return index
            if names_ready is not None and hasattr(names_ready,'initial_names'):
                await asyncio.to_thread(state.ready,names_ready.initial_names)
            async def prepare():
                await asyncio.to_thread(state.ready,await names_ready() if names_ready else {})
                state.names_complete=True
                state.wake()
            tasks=[asyncio.create_task(prepare())]+[asyncio.create_task(state.worker()) for _ in range(config.nav_concurrency)]
            cutoff=(datetime.now(timezone.utc)-timedelta(days=config.nav_lookback_days)).replace(hour=0,minute=0,second=0,microsecond=0)
            url=BASE+'/api/v1/feed';next_url=url;headers={'If-Modified-Since':format_datetime(cutoff,usegmt=True)};seen=set()
            paging_began=time.monotonic()
            while url:
                if index.metrics['pages']>=config.nav_max_pages:state.errors.append('nav_page_cap');break
                url=allowed(url)
                if url in seen:raise SourceFailure('nav_paging_loop')
                seen.add(url)
                try:_,body,sha,retrieved=await http.get(url,state.token,headers)
                except SourceFailure as exc:
                    if exc.code!='token_unavailable' or not from_environment:raise
                    state.token=await http.public_token();from_environment=False
                    if not state.token:raise
                    _,body,sha,retrieved=await http.get(url,state.token,headers)
                data=await asyncio.to_thread(json.loads,body)
                if not isinstance(data,dict) or not isinstance(data.get('items'),list):raise SourceFailure('nav_malformed_page')
                index.metrics['pages']+=1;index.metrics['items']+=len(data['items'])
                # Header scoring has its own serial worker; the pager never
                # waits for scoring or for company extraction to finish.
                page_jobs.append(asyncio.get_running_loop().run_in_executor(page_pool,state.page,data['items'],sha,url,retrieved))
                next_url=data.get('next_url')
                if not next_url and data.get('next_id'):raise SourceFailure('nav_missing_next_url')
                if not next_url:break
                url=next_url;headers={}
                await asyncio.sleep(0)  # Yield to ready consumers; no rate delay.
            index.metrics['feed_runtime_ms']=round((time.monotonic()-paging_began)*1000)
            index.metrics['feed_transport_complete']=not next_url
            await asyncio.gather(*page_jobs)
            state.page_complete=not next_url
            index.metrics['header_processing_complete']=True
            state.done=True;state.wake()
            await asyncio.gather(*tasks)
            await asyncio.to_thread(state.settle)
            index.reason='complete' if index.complete else ','.join(sorted(set(state.errors))) or 'nav_name_unusable'
    except asyncio.CancelledError:index.reason='deadline';raise
    except TimeoutError:index.reason='nav_time_cap'
    except Exception as exc:
        index.reason=exc.code if isinstance(exc,SourceFailure) else type(exc).__name__
        index.blocked=index.reason=='token_unavailable'
    finally:
        for job in page_jobs:
            if not job.done():job.cancel()
        await asyncio.to_thread(page_pool.shutdown,wait=True,cancel_futures=True)
        for task in tasks:
            if not task.done():task.cancel()
        if tasks:await asyncio.gather(*tasks,return_exceptions=True)
        await asyncio.to_thread(state.settle)
        if paging_began is not None and 'feed_runtime_ms' not in index.metrics:index.metrics['feed_runtime_ms']=round((time.monotonic()-paging_began)*1000)
        index.metrics.update({'feed_complete':state.page_complete and config.nav_lookback_days>=185,
            'average_seconds_per_page':index.metrics.get('feed_runtime_ms',0)/1000/index.metrics['pages'] if index.metrics['pages'] else None,
            'runtime_ms':round((time.monotonic()-began)*1000),'runtime_seconds':time.monotonic()-began,
            'feed_seconds':index.metrics.get('feed_runtime_ms',0)/1000,'complete':index.complete,
            'blocked':index.blocked,'reason':index.reason,'lookback_days':config.nav_lookback_days,
            'indexed_ads':sum(map(len,index.ads.values())),'incomplete_companies':sorted(index.incomplete_orgs),
            'detail_requests':index.metrics.get('detail_requests',0)})
        http.save()
    return index
