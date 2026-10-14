import asyncio,json,threading
import httpx
from signalpost.sources.nav import Index,prefetch
from signalpost.sources.nav_stream import Stream
from signalpost.sources.blobstore import BlobStore
from signalpost.sources.excerpt import excerpt,document_bounds
from signalpost.budget import Budget
from tests.test_registry import config
from tests.test_nav import ORG,TOKEN,UUID
from tests.test_nav_streaming import header,ad,SECOND


def test_cached_pointer_map_preserves_exact_excerpts():
    body=json.dumps({'a/b':{'~key':[{'value':'Nordisk æøå'},None,0,False]},'other':['x','y']},ensure_ascii=False).encode()
    text=body.decode();document=(text,document_bounds(text))
    for pointer in ['/a~1b','/a~1b/~0key/0/value','/a~1b/~0key/1','/a~1b/~0key/2','/a~1b/~0key/3','/other/1','/missing','/']:
        assert excerpt(body,locator=pointer)==excerpt(body,locator=pointer,document=document)


def test_pager_does_not_wait_for_cpu_header_worker(tmp_path,monkeypatch):
    cfg=config(tmp_path,[ORG],hiring=True);index=Index();next_sent=threading.Event()
    original=Stream.page
    def slow(self,*args):
        assert next_sent.wait(1),'Pager waited for header CPU work'
        return original(self,*args)
    monkeypatch.setattr(Stream,'page',slow)
    async def names():return {ORG:{'Rareone AS'}}
    async def respond(request):
        if request.url.path=='/api/publicToken':return httpx.Response(200,text=TOKEN)
        if '/feedentry/' in request.url.path:return httpx.Response(200,json=ad(UUID,ORG))
        if request.url.path.endswith(UUID):
            next_sent.set();return httpx.Response(200,json={'items':[],'next_url':None})
        return httpx.Response(200,json={'items':[header(UUID,'Rareone AS')],'next_url':'/api/v1/feed/'+UUID})
    async def gate():
        async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
            await prefetch(client,cfg,Budget(cfg),BlobStore(cfg.state_dir),index,names)
    asyncio.run(gate())
    assert index.complete and index.metrics['pages']==2


def test_registry_extraction_runs_outside_event_loop(tmp_path,monkeypatch):
    from signalpost.sources import brreg_roller
    from signalpost.sources.http import Response
    from signalpost.runner import run
    from tests.test_registry import handler
    entered=threading.Event();release=threading.Event();original=brreg_roller.extract
    def extract(*args):
        entered.set();assert release.wait(1),'Loop did not get a chance to release extraction'
        return original(*args)
    monkeypatch.setattr(brreg_roller,'extract',extract)
    cfg=config(tmp_path,[ORG])
    async def gate():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler())) as client:
            task=asyncio.create_task(run(cfg,client))
            while not entered.is_set():await asyncio.sleep(.001)
            release.set();report=await task
            assert report['emitted_envelopes']==1 and 'event_loop' in report
    asyncio.run(gate())


def test_cpu_process_preserves_native_header_scores(tmp_path):
    from collections import Counter,defaultdict
    from signalpost.sources.nav_scoring import POOL,score_many
    from signalpost.sources.nav import name_tokens
    cfg=config(tmp_path,[ORG]);names={ORG:{'rareone ventures','rareone'},'other':{'common ventures'}}
    frequency=Counter({'rareone':1,'ventures':60,'common':2})
    rows=[(UUID,'Rareone Ventures AS'),(SECOND,'Common Ventures AS'),('none',None)]
    token_orgs=defaultdict(set)
    for org,known in names.items():
        for name in known:
            for token in name_tokens(name):token_orgs[token].add(org)
    async def gate():
        state=Stream(None,Index(),cfg,None,0,False);state.names=names
        state.token_orgs=token_orgs;state.frequency=frequency;state.active={str(i):None for i in range(1000)}
        expected={uuid:state.classify((None,{'id':uuid,'_feed_entry':{'businessName':name}})) for uuid,name in rows}
        actual=await asyncio.get_running_loop().run_in_executor(None,lambda:POOL.submit(score_many,rows,names,dict(token_orgs),frequency,1000,False,True).result())
        assert actual==expected
    asyncio.run(gate())


def test_website_wait_does_not_hold_next_company_registry_slot(tmp_path,monkeypatch):
    from signalpost.runner import run
    from signalpost.sources.extract import Section
    from tests.test_nav import OTHER
    from tests.test_registry import handler
    ready=asyncio.Event();base=handler()
    async def website(org,*args):
        if org==ORG:await asyncio.wait_for(ready.wait(),2)
        return Section(state='not_available')
    def response(request):
        if request.url.path.endswith(OTHER+'/roller'):ready.set()
        return base(request)
    monkeypatch.setattr('signalpost.runner.collector.fetch',website)
    cfg=config(tmp_path,[ORG,OTHER],workers=1,websites=True)
    async def gate():
        async with httpx.AsyncClient(transport=httpx.MockTransport(response)) as client:return await run(cfg,client)
    report=asyncio.run(gate())
    assert report['handled_exceptions']==report['unhandled_exceptions']==0
    assert report['emitted_envelopes']==2
