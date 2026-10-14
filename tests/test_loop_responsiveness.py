import asyncio,json,threading
import httpx
from signalpost.sources.nav import Index,prefetch
from signalpost.sources.nav_stream import Stream
from signalpost.sources.blobstore import BlobStore
from signalpost.sources.excerpt import excerpt,document_bounds
from signalpost.budget import Budget
from tests.test_registry import config
from tests.test_nav import ORG,TOKEN,UUID
from tests.test_nav_streaming import header,ad


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
