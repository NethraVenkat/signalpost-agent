import asyncio,json
import httpx
from signalpost.config import Config
from signalpost.runner import run
from signalpost.budget import SourceFailure
from signalpost.sources import official_resilience as resilience
from tests.test_registry import config,handler,entity
ORG='923609016'
def test_library_health_default_is_on(tmp_path):
    cfg=Config(organisations=tmp_path/'in',output=tmp_path/'out',report=tmp_path/'report')
    assert cfg.official_source_health is True

def test_runner_health_probes_counted_and_no_secret_bodies(tmp_path):
    cfg=config(tmp_path,[ORG],official_source_health=True)
    calls=[]
    def dispatch(request):
        calls.append((request.method,str(request.url)))
        if request.method=='HEAD':return httpx.Response(200,content=b'not-company-proof')
        return handler()(request)
    async def execute():
        async with httpx.AsyncClient(transport=httpx.MockTransport(dispatch)) as client:return await run(cfg,client=client)
    report=asyncio.run(execute())
    assert len([c for c in calls if c[0]=='HEAD'])==2
    assert report['requests']==len(calls)<=report['limits']['max_requests']
    assert all(x['state']=='reachable' for x in report['official_source_outages']['health_checks'])
    assert not report['official_source_outages']['attempts']
    row=json.loads(cfg.output.read_text(encoding='utf8'))
    assert row['run']['terminal_status']=='completed'
    assert not any('not-company-proof' in e['claim_span'] for e in row['evidence'])

def test_down_source_gates_calls_and_keeps_terminal_output(tmp_path,monkeypatch):
    cfg=config(tmp_path,[ORG],official_source_health=True)
    calls=[];waits=[]
    async def retry_wait(budget,event,attempt,minimum=0,deadline=None):waits.append(resilience.BACKOFF[attempt])
    monkeypatch.setattr(resilience,'pause',retry_wait)
    def dispatch(request):
        url=str(request.url);calls.append((request.method,url))
        if '/enhetsregisteret/' in url:raise SourceFailure('dns_error')
        if request.method=='HEAD':return httpx.Response(200)
        return handler()(request)
    async def execute():
        async with httpx.AsyncClient(transport=httpx.MockTransport(dispatch)) as client:return await run(cfg,client=client)
    report=asyncio.run(execute())
    assert not any(method=='GET' and '/enhetsregisteret/' in url for method,url in calls)
    assert report['requests']==len(calls)<=report['limits']['max_requests']
    assert waits==[5,20]
    assert any(x['source']=='enhetsregisteret' and x['state']=='unavailable' for x in report['official_source_outages']['health_checks'])
    row=json.loads(cfg.output.read_text(encoding='utf8'))
    assert row['run']['terminal_status']=='failed'
    assert any(e['code']=='source_outage_enhetsregisteret' for e in row['errors'])

def test_all_invalid_batch_makes_no_health_requests(tmp_path):
    from signalpost.identity.orgnr import valid
    assert not valid('123456789') and not valid('923609017')
    cfg=config(tmp_path,['123456789','923609017'],official_source_health=True)
    def dispatch(request):raise AssertionError('Invalid identifiers must not trigger source probes')
    async def execute():
        async with httpx.AsyncClient(transport=httpx.MockTransport(dispatch)) as client:return await run(cfg,client=client)
    report=asyncio.run(execute())
    assert report['requests']==0
    assert report['official_source_outages']['health_checks'][0]['state']=='not_applicable'
