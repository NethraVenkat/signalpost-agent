"""Exact declared-index candidates, forward-feed refresh and mandatory live proof."""
from ..workers import offload,nav_offload

import asyncio,heapq,json,os,time
from collections import defaultdict
from datetime import datetime,timezone
from uuid import UUID
from ..budget import SourceFailure
from ..identity.orgnr import valid
from .nav import BASE,Ad,NavHttp,allowed,header_name,name_matches,name_tokens,timestamp,time_cap,token_from


class Candidates:
    def __init__(self,data,index,config,previous,pre_loaded_subunit_map=None):
        self.data,self.index,self.config=data,index,config
        self.pre_loaded_subunit_map=pre_loaded_subunit_map or {}
        self.members={a['uuid']:a for a in data['ads']}
        self.ads_by_employer=defaultdict(list)
        for a in data['ads']:
            self.ads_by_employer[a['employer_orgnr']].append(a['uuid'])
        self.headers={};self.names={};self.scopes={};self.owners=defaultdict(set)
        self.pending={};self.heap=[];self.discovered=set();self.checked={};self.failed={};self.inflight=set();self.affected=defaultdict(set)
        self.events=[];self.done=False;self.ready=False;self.previous=previous or {};self.new_unknown=False
    def wake(self):
        for event in self.events:event.set()
    def version(self,uuid):
        return self.headers[uuid][0] if uuid in self.headers else (self.members.get(uuid,{}).get('last_modified') or 'index:'+self.data['index_version'])
    def candidate(self,uuid,affected,origin):
        if not affected:return
        self.affected[uuid].update(affected)
        self.discovered.add(uuid);v=self.version(uuid)
        self.index.metrics['detail_request_cap']=(self.config.nav_max_details if self.config.nav_max_details is not None else (0 if not self.discovered else min(len(self.discovered)+10,max(300,2*len(self.scopes)))))
        if self.checked.get(uuid)==v or self.failed.get(uuid)==v:return
        if self.pending.get(uuid,(None,None,None))[0]==v:
            self.pending[uuid][1].update(affected)
            return
        self.pending[uuid]=(v,set(affected),origin)
        heapq.heappush(self.heap,(0 if origin=='declared_cache' else 1,uuid,v));self.wake()
    def set_scopes(self,scopes,names):
        self.scopes=scopes;self.names=names;self.owners=defaultdict(set)
        for parent,ids in scopes.items():
            for org in ids:self.owners[org].add(parent)
        for uuid,ad in self.members.items():self.candidate(uuid,self.owners.get(ad['employer_orgnr'],set()),'declared_cache')
        for parent,row in self.previous.items():
            if parent not in scopes:continue
            for c in row.get('claims',row.get('profile',{}).get('claims',[])):
                if c.get('family')=='hiring' and c.get('availability')=='available' and isinstance(c.get('value'),dict):
                    uuid=c['value'].get('uuid')
                    try:uuid=str(UUID(uuid))
                    except (ValueError,TypeError,AttributeError):continue
                    self.candidate(uuid,{parent},'previous_live_ad')
        self.wake()
    def add_company_scope(self,parent,subunits,names=None,pre_loaded_subunit_map=None):
        pre_map = pre_loaded_subunit_map or self.pre_loaded_subunit_map
        if pre_map:
            parents = getattr(pre_map, 'parents', {})
            parent_subunits = getattr(pre_map, 'parent_subunits', {})
            if parent in parent_subunits:
                subunits = set(subunits) | parent_subunits[parent]
            for emp, p in parents.items():
                if p == parent:
                    subunits = set(subunits)
                    subunits.add(emp)
                    if emp in pre_map:
                        vals = pre_map[emp]
                        if isinstance(vals, (list, tuple)):
                            extra_names = [v for v in vals if v]
                            if extra_names:
                                names = (set(names) if names else set()) | set(extra_names)
        self.scopes.setdefault(parent,{parent}).update(subunits)
        if names:
            self.names.setdefault(parent,set()).update(names)
        for unit in subunits:
            self.owners[unit].add(parent)
            for uuid in self.ads_by_employer.get(unit,()):
                self.candidate(uuid,{parent},'declared_cache')
        if parent in self.previous:
            row=self.previous[parent]
            for c in row.get('claims',row.get('profile',{}).get('claims',[])):
                if c.get('family')=='hiring' and c.get('availability')=='available' and isinstance(c.get('value'),dict):
                    uuid=c['value'].get('uuid')
                    try:uuid=str(UUID(uuid))
                    except (ValueError,TypeError,AttributeError):continue
                    self.candidate(uuid,{parent},'previous_live_ad')
        for uuid,(at,item) in list(self.headers.items()):
            entry=item.get('_feed_entry') or {}
            employer=entry.get('employer') or item.get('employer') or {}
            employer_org=str(employer.get('orgnr') or '') if isinstance(employer,dict) else ''
            if employer_org in subunits:
                self.candidate(uuid,{parent},'forward_feed')
            elif names and not employer_org:
                h_name=header_name(item)
                if h_name and any(name_matches(h_name,n) for n in names):
                    self.candidate(uuid,{parent},'forward_feed')
        self.wake()
    async def inspect(self,uuid):
        at,item=self.headers[uuid];entry=item['_feed_entry'];status=entry['status']
        if status!='ACTIVE':
            self.index.closed.add(uuid)
            # Feed status alone never creates a closed_job event.
        member=self.members.get(uuid)
        if member:
            self.candidate(uuid,self.owners.get(member['employer_orgnr'],set()),'declared_cache')
            return
        if status!='ACTIVE':return
        employer=entry.get('employer') or item.get('employer') or {}
        employer_org=str(employer.get('orgnr') or '') if isinstance(employer,dict) else ''
        if valid(employer_org):
            # FIRST: lookup in pre_loaded_subunit_map (O(1), instant)
            parents = self.owners.get(employer_org)
            if not parents and self.pre_loaded_subunit_map and employer_org in self.pre_loaded_subunit_map:
                p = getattr(self.pre_loaded_subunit_map, 'parents', {}).get(employer_org)
                if p:
                    self.owners[employer_org].add(p)
                    self.scopes.setdefault(p, {p}).add(employer_org)
                    parents = {p}
            # SECOND: fall back to live registry if no match
            self.candidate(uuid,parents or self.owners.get(employer_org,set()),'forward_feed')
            return
        self.new_unknown=True
        name=header_name(item)
        if not name:affected=set(self.scopes)
        else:
            affected=await nav_offload(lambda:{org for org,known in self.names.items() if any(name_matches(name,n) for n in known)})
        self.candidate(uuid,affected,'forward_feed')
    async def page(self,items):
        for item in items:
            entry=item.get('_feed_entry') or {}
            if entry.get('status') not in {'ACTIVE','INACTIVE','DELETED'}:raise SourceFailure('nav_unknown_status')
            try:uuid=str(UUID(entry.get('uuid') or item.get('id')))
            except (ValueError,TypeError,AttributeError):raise SourceFailure('nav_invalid_uuid') from None
            stamp=timestamp(item.get('date_modified') or entry.get('sistEndret'))
            if stamp is None:raise SourceFailure('nav_invalid_modified_date')
            at=stamp.isoformat();old=self.headers.get(uuid)
            if old and timestamp(old[0])>stamp:continue
            self.headers[uuid]=(at,item)
            if entry['status']=='ACTIVE':self.index.closed.discard(uuid)
            await self.inspect(uuid)
    def take(self):
        if self.index.metrics.get('detail_requests',0)+len(self.inflight)>=self.index.metrics.get('detail_request_cap',0):return None
        while self.heap:
            _,uuid,v=heapq.heappop(self.heap);record=self.pending.get(uuid)
            if record is None or record[0]!=v or uuid in self.inflight:continue
            # Scope/header discovery can enqueue a version while its detail is
            # in flight. Completion has already verified that exact version;
            # do not spend another HTTP attempt (or a scarce cap slot) on it.
            if self.checked.get(uuid)==v or self.failed.get(uuid)==v:
                self.pending.pop(uuid)
                self.index.metrics['redundant_detail_jobs_skipped']=self.index.metrics.get('redundant_detail_jobs_skipped',0)+1
                continue
            self.pending.pop(uuid);self.inflight.add(uuid);return uuid,record
        return None


async def prefetch(client,config,budget,blobs,index,data,age,path,names_ready,previous):
    began=time.monotonic();http=NavHttp(client,config,budget,blobs,index)
    pre_loaded=getattr(names_ready,'pre_loaded_subunit_map',None)
    state=Candidates(data,index,config,previous,pre_loaded_subunit_map=pre_loaded)
    tasks=[];feed_done=False;header_done=False;feed_began=None
    page_queue=asyncio.Queue()
    async def headers():
        while True:
            page=await page_queue.get()
            try:
                if page is None:return
                await state.page(page)
            finally:page_queue.task_done()
    token=None;from_environment=False;token_lock=asyncio.Lock()
    async def authenticated_get(url,**kwargs):
        nonlocal token,from_environment
        attempted=token
        try:return await http.get(url,attempted,**kwargs)
        except SourceFailure as exc:
            if exc.code!='token_unavailable':raise
            async with token_lock:
                if token==attempted and from_environment:
                    token=await http.public_token();from_environment=False
            if not token or token==attempted:
                index.blocked=True;index.reason='token_unavailable';raise
            try:return await http.get(url,token,**kwargs)
            except SourceFailure as retry:
                if retry.code=='token_unavailable':index.blocked=True;index.reason='token_unavailable'
                raise
    index.metrics.update({'source_mode':'declared_index','index_version':data['index_version'],'index_built_at':data['built_at'],
        'index_age_days':age,'index_compressed_bytes':path.stat().st_size,'index_ads':data['ads_count'],
        'seeded_from_disk':data['seeded_from_disk'],'fresh_fetched_ads':data['fresh_fetched_ads'],
        'time_cap_seconds':time_cap(config),'feed_complete':False,'detail_request_cap':0,
        'coverage_scope':'declared_orgnr_index_plus_completed_forward_feed_and_live_candidate_details'})
    async def detail(uuid,record):
        version,affected,origin=record;url=BASE+'/api/v1/feedentry/'+uuid
        provenance={'index_version':data['index_version'],'index_built_at':data['built_at'],'candidate_origin':origin}
        if 'first_detail_seconds' not in index.metrics:
            index.metrics.update({'first_detail_seconds':time.monotonic()-began,'first_detail_page_number':index.metrics['pages'],
                                  'details_started_before_feed_complete':not feed_done})
        try:
            _,body,sha,retrieved=await authenticated_get(url,companies=affected)
            index.metrics['last_detail_seconds']=time.monotonic()-began
            entry=await nav_offload(json.loads,body);index.metrics['details']+=1
            if entry.get('uuid')!=uuid:raise SourceFailure('nav_wrong_ad')
            if entry.get('status') not in {'ACTIVE','INACTIVE','DELETED'}:raise SourceFailure('nav_unknown_status')
            if entry['status']!='ACTIVE':
                index.live_closed.add(uuid);index.closed.add(uuid)
                index.closure_proofs[uuid]=(sha,url,retrieved,'/status',entry['status'],provenance);return True
            ad=entry.get('ad_content')
            if not isinstance(ad,dict) or ad.get('uuid')!=uuid:raise SourceFailure('nav_malformed_ad')
            expiry=timestamp(ad.get('expires'));published=timestamp(ad.get('published'));now=datetime.now(timezone.utc)
            if expiry is None or published is None:raise SourceFailure('nav_invalid_dates')
            if expiry<=now:
                index.live_closed.add(uuid);index.closed.add(uuid)
                index.closure_proofs[uuid]=(sha,url,retrieved,'/ad_content/expires',ad['expires'],provenance);return True
            if published>now:raise SourceFailure('nav_invalid_dates')
            org=str((ad.get('employer') or {}).get('orgnr') or '').strip()
            if not valid(org):return True
            if not ad.get('title'):raise SourceFailure('nav_missing_title')
            value={'uuid':uuid,'employer_orgnr':org,'title':ad['title'],
                'location':[{'municipality':x.get('municipal'),'city':x.get('city')} for x in ad.get('workLocations',[])] or None,
                'published':ad['published'],'expires':ad['expires'],'occupation_categories':ad.get('occupationCategories') or None,
                'url':'https://arbeidsplassen.nav.no/stillinger/stilling/'+uuid}
            value['availability']={'location':'available' if value['location'] else 'not_available',
                'occupation_categories':'available' if value['occupation_categories'] else 'not_available'}
            if state.version(uuid)==version:
                for key,ads in index.ads.items():index.ads[key]=[a for a in ads if a.value['uuid']!=uuid]
                index.closed.discard(uuid)
                ad_obj = Ad(value,sha,url,retrieved,None,None,None,None,provenance)
                index.ads.setdefault(org,[]).append(ad_obj)
                for parent in state.owners.get(org, ()):
                    if parent != org and ad_obj not in index.ads.get(parent, ()):
                        index.ads.setdefault(parent,[]).append(ad_obj)
                if pre_loaded:
                    p = getattr(pre_loaded, 'parents', {}).get(org)
                    if p and p != org and ad_obj not in index.ads.get(p, ()):
                        index.ads.setdefault(p,[]).append(ad_obj)
            return True
        except asyncio.CancelledError:raise
        except Exception as exc:
            code=exc.code if isinstance(exc,SourceFailure) else type(exc).__name__
            state.failed[uuid]=version;index.metrics.setdefault('detail_failures',{}).setdefault(code,0)
            index.metrics['detail_failures'][code]+=1;return False
    async def worker():
        event=asyncio.Event();state.events.append(event)
        while True:
            event.clear();job=state.take()
            if job:
                uuid,record=job
                try:
                    if await detail(uuid,record):state.checked[uuid]=record[0]
                finally:
                    state.inflight.discard(uuid)
                    if uuid in state.pending:
                        v,_,origin=state.pending[uuid]
                        heapq.heappush(state.heap,(0 if origin=='declared_cache' else 1,uuid,v))
                    state.wake()
            elif state.done and state.ready:return
            else:await event.wait()
    async def prepare():
        if hasattr(names_ready,'subunit_queue') and names_ready.subunit_queue is not None:
            queue=names_ready.subunit_queue
            while True:
                item=await queue.get()
                try:
                    if item is None:break
                    org,subunits,names=item
                    state.add_company_scope(org,subunits,names,pre_loaded_subunit_map=pre_loaded)
                finally:queue.task_done()
            if callable(names_ready):
                final_names=await names_ready()
                for org,n_set in (final_names or {}).items():state.names.setdefault(org,set()).update(n_set)
            for uuid in list(state.headers):await state.inspect(uuid)
            state.ready=True;state.wake()
        else:
            names=await names_ready() if names_ready else {}
            scopes=await names_ready.scopes_ready() if names_ready and hasattr(names_ready,'scopes_ready') else {org:{org} for org in names}
            state.set_scopes(scopes,names)
            for uuid in list(state.headers):await state.inspect(uuid)
            state.ready=True;state.wake()
    try:
        async with asyncio.timeout(time_cap(config)):
            token=token_from(os.environ.get('NAV_API_TOKEN'));from_environment=bool(token)
            token=token or await http.public_token()
            if not token:index.blocked=True;index.reason='token_unavailable';return index
            initial=getattr(names_ready,'initial_names',{}) if names_ready else {}
            scopes={org:{org} for org in initial}
            if pre_loaded:
                for parent, subs in getattr(pre_loaded, 'parent_subunits', {}).items():
                    if parent in scopes:
                        scopes[parent].update(subs)
            state.set_scopes(scopes,initial)
            if pre_loaded:
                for parent, subs in getattr(pre_loaded, 'parent_subunits', {}).items():
                    if parent in scopes:
                        state.add_company_scope(parent, subs, pre_loaded_subunit_map=pre_loaded)
            header_task=asyncio.create_task(headers())
            tasks=[header_task,asyncio.create_task(prepare())]+[asyncio.create_task(worker()) for _ in range(config.nav_concurrency)]
            url=data['cursor'];seen=set();feed_began=time.monotonic()
            while url:
                url=allowed(url)
                if url in seen:raise SourceFailure('nav_paging_loop')
                if index.metrics['pages']>=config.nav_max_pages:raise SourceFailure('nav_page_cap')
                seen.add(url);_,body,_,_=await authenticated_get(url,persist=False)
                page=await nav_offload(json.loads,body)
                if not isinstance(page,dict) or not isinstance(page.get('items'),list):raise SourceFailure('nav_malformed_page')
                index.metrics['pages']+=1;index.metrics['items']+=len(page['items'])
                page_queue.put_nowait(page['items'])
                url=page.get('next_url')
                if not url and page.get('next_id'):raise SourceFailure('nav_missing_next_url')
            feed_done=True;index.metrics['feed_runtime_ms']=round((time.monotonic()-feed_began)*1000)
            index.metrics['feed_complete']=True
            page_queue.put_nowait(None)
            await header_task
            header_done=True
            state.done=True;state.wake()
            await asyncio.gather(*tasks)
            if not index.blocked:index.reason='complete'
    except asyncio.CancelledError:index.reason='deadline';raise
    except TimeoutError:index.reason='nav_time_cap'
    except Exception as exc:
        index.reason=exc.code if isinstance(exc,SourceFailure) else type(exc).__name__
        index.blocked=index.reason=='token_unavailable'
    finally:
        for task in tasks:
            if not task.done():task.cancel()
        if tasks:await asyncio.gather(*tasks,return_exceptions=True)
        incomplete=set()
        for uuid in state.discovered:
            if state.checked.get(uuid)!=state.version(uuid):
                member=state.members.get(uuid)
                affected=state.affected.get(uuid,set()) | (state.owners.get(member['employer_orgnr'],set()) if member else set())
                if uuid in state.headers and state.headers[uuid][1]['_feed_entry']['status']=='ACTIVE':
                    name=header_name(state.headers[uuid][1])
                    affected=affected | ({org for org,names in state.names.items() if any(name_matches(name,n) for n in names)} if name else set(state.scopes))
                if uuid in state.pending:affected=affected|state.pending[uuid][1]
                incomplete.update(affected)
        unusable={org for org,names in state.names.items() if not any(name_tokens(n) for n in names)} if state.new_unknown else set()
        # The declared baseline is orgnr-keyed. Name usability is diagnostic for
        # forward nomination, not an extra cache-mode qualification condition.
        index.incomplete_orgs=incomplete
        index.coverage_ready=feed_done and header_done and state.ready
        index.complete=index.coverage_ready and not incomplete and not index.blocked
        if not index.blocked and not feed_done:
            index.metrics['failure_cause']=index.reason;index.reason='forward_feed_incomplete'
        elif not index.blocked and not index.complete:
            index.metrics['failure_cause']=index.reason;index.reason='detail_unverified'
        total=time.monotonic()-began
        feed_ms=index.metrics.get('feed_runtime_ms',round((time.monotonic()-feed_began)*1000) if feed_began else 0)
        index.metrics.update({'runtime_ms':round(total*1000),'runtime_seconds':total,'feed_runtime_ms':feed_ms,
            'feed_seconds':feed_ms/1000,'average_seconds_per_page':feed_ms/1000/index.metrics['pages'] if index.metrics['pages'] else None,
            'last_detail_seconds':index.metrics.get('last_detail_seconds'),
            'feed_complete':feed_done,'complete':index.complete,'blocked':index.blocked,'reason':index.reason,
            'header_processing_complete':header_done,
            'candidate_headers':len(state.discovered),'distinct_candidate_ads':len(state.discovered),
            'indexed_ads':sum(map(len,index.ads.values())),'detail_concurrency':config.nav_concurrency,
            'incomplete_companies':sorted(incomplete),'name_unusable_companies':0,
            'fallback_name_unusable_companies':len(unusable),
            'forward_name_fallback_scope':'known legal/brand/subunit names; unknown trading names remain a discovery risk',
            'companies_with_unchecked_candidates':len(incomplete),
            'cap_hits':len(state.discovered-state.checked.keys()) if index.metrics.get('detail_requests',0)>=index.metrics['detail_request_cap'] else 0,
            'lookback_days':config.nav_lookback_days})
        await offload(http.save)
    return index
