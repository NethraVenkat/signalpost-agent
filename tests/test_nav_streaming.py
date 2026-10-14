import asyncio
import hashlib
from types import SimpleNamespace
from datetime import datetime,timezone
import httpx
from signalpost.sources.nav import BASE,Index,NavHttp,prefetch
from signalpost.sources.blobstore import BlobStore
from signalpost.budget import Budget
from tests.test_registry import config
from tests.test_nav import ORG,OTHER,TOKEN,UUID

SECOND='00000000-0000-4000-8000-000000000002'


def warm_scorer():
    # These short synthetic deadlines test streaming/coverage ordering, not
    # Windows process startup. Live cold gates include startup in their timing.
    from signalpost.sources.nav_scoring import POOL,score_many
    POOL.submit(score_many,[],{},{},{},0,False,True).result(timeout=15)


def header(uuid,name):
    return {'id':uuid,'url':'/api/v1/feedentry/'+uuid,'date_modified':'2026-10-01T00:00:00Z',
            '_feed_entry':{'uuid':uuid,'status':'ACTIVE','businessName':name}}


def ad(uuid,org):
    return {'uuid':uuid,'status':'ACTIVE','ad_content':{'uuid':uuid,'title':'Reported vacancy',
        'published':'2026-10-01T00:00:00Z','expires':'2099-01-01T00:00:00Z','employer':{'orgnr':org}}}


def test_nav_requests_do_not_enter_website_politeness_gate(tmp_path,monkeypatch):
    cfg=config(tmp_path,[ORG],website_politeness_seconds=60)
    def forbidden(*args,**kwargs):raise AssertionError('NAV entered WebsiteHttp.raw')
    monkeypatch.setattr('signalpost.web.fetcher.WebsiteHttp.raw',forbidden)
    blobs=SimpleNamespace(directory=tmp_path,put=lambda body:hashlib.sha256(body).hexdigest())
    calls=[]
    def response(request):calls.append(str(request.url));return httpx.Response(200,json={})
    async def gate():
        async with httpx.AsyncClient(transport=httpx.MockTransport(response)) as client:
            nav=NavHttp(client,cfg,Budget(cfg),blobs,Index())
            await asyncio.wait_for(nav.get(BASE+'/api/v1/feed',TOKEN),.5)
            await asyncio.wait_for(nav.get(BASE+'/api/v1/feed/'+UUID,TOKEN),.5)
    asyncio.run(gate());assert len(calls)==2


def test_details_start_before_next_feed_page_is_released(tmp_path):
    warm_scorer()
    cfg=config(tmp_path,[ORG],hiring=True);index=Index();started=asyncio.Event()
    async def names():
        # Registry subunits may finish later; legal-name discovery must not wait.
        await asyncio.wait_for(started.wait(),.5)
        return {ORG:{'Rareone AS'}}
    names.initial_names={ORG:{'Rareone AS'}}
    async def response(request):
        if request.url.path=='/api/publicToken':return httpx.Response(200,text=TOKEN)
        if '/feedentry/' in request.url.path:
            started.set();return httpx.Response(200,json=ad(UUID,ORG))
        if request.url.path.endswith(UUID):
            await asyncio.wait_for(started.wait(),.5)
            return httpx.Response(200,json={'items':[],'next_url':None,'next_id':None})
        return httpx.Response(200,json={'items':[header(UUID,'Rareone AS')],
            'next_url':'/api/v1/feed/'+UUID,'next_id':UUID})
    async def gate():
        async with httpx.AsyncClient(transport=httpx.MockTransport(response)) as client:
            await prefetch(client,cfg,Budget(cfg),BlobStore(cfg.state_dir),index,names)
    asyncio.run(gate())
    assert index.metrics['pages']==2 and index.metrics['details']==1 and index.complete
    assert index.metrics['details_started_before_feed_complete']
    assert index.metrics['first_detail_page_number']==1


def test_completed_scope_survives_detail_timeout_after_complete_feed(tmp_path):
    warm_scorer()
    cfg=config(tmp_path,[ORG,OTHER],hiring=True,nav_time_cap_seconds=.15);index=Index()
    async def names():return {ORG:{'Rareone AS'},OTHER:{'Raretwo AS'}}
    async def response(request):
        if request.url.path=='/api/publicToken':return httpx.Response(200,text=TOKEN)
        if '/feedentry/' in request.url.path:
            uuid=request.url.path.split('/')[-1]
            if uuid==SECOND:await asyncio.sleep(1)
            return httpx.Response(200,json=ad(uuid,ORG if uuid==UUID else OTHER))
        return httpx.Response(200,json={'items':[header(UUID,'Rareone AS'),header(SECOND,'Raretwo AS')],
            'next_url':None,'next_id':None})
    async def gate():
        async with httpx.AsyncClient(transport=httpx.MockTransport(response)) as client:
            await prefetch(client,cfg,Budget(cfg),BlobStore(cfg.state_dir),index,names)
    asyncio.run(gate())
    assert index.metrics['feed_complete'] and index.reason=='nav_time_cap'
    assert index.company_complete(ORG) and not index.company_complete(OTHER)
    assert index.metrics['companies_with_unchecked_candidates']==1


def test_retry_wait_is_not_counted_as_inter_request_idle(tmp_path):
    cfg=config(tmp_path,[ORG]);index=Index();calls=[];budget=Budget(cfg)
    async def respond(request):
        calls.append(request.url.path)
        await request.extensions['trace']('http11.send_request_headers.complete',{})
        if len(calls)==2:
            await asyncio.sleep(.5)
            raise httpx.ReadTimeout('simulated timeout')
        return httpx.Response(200,json={})
    async def gate():
        async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
            http=NavHttp(client,cfg,budget,BlobStore(cfg.state_dir),index)
            await http.get(BASE+'/api/v1/feed',TOKEN)
            await http.get(BASE+'/api/v1/feed/'+UUID,TOKEN)
    asyncio.run(gate())
    assert budget.events[1]['error']=='ReadTimeout' and budget.events[1]['runtime_ms']>=400
    assert budget.events[2]['gap_preceded_by']=='request_error_complete'
    assert budget.events[2]['inter_request_gap_ms']<300
