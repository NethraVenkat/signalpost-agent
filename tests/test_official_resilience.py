import asyncio,importlib.util,time
from pathlib import Path
from types import SimpleNamespace
import httpx,pytest
from signalpost.budget import SourceFailure
from signalpost.sources import official_resilience as m
class FakeBudget:
    def __init__(self,cap=50,remaining=100):self.start=time.monotonic();self.cap=cap;self.events=[];self.deadline=self.start+remaining
    def check(self):
        if time.monotonic()>=self.deadline:raise SourceFailure('deadline')
    def reserve(self,url,host,org):
        self.check()
        if len(self.events)>=self.cap:raise SourceFailure('budget_exhausted')
        e={'url':url,'host':host,'organisation_number':org,'error':None,'status':None};self.events.append(e);return e
CFG=SimpleNamespace(hiring=False,gleif=False,request_timeout=1)
def test_dns_recovery_and_exact_backoff(monkeypatch):
    waits=[];seen={}
    async def sleep(seconds):waits.append(seconds)
    monkeypatch.setattr(m.asyncio,'sleep',sleep)
    def handler(request):
        key=str(request.url);seen[key]=seen.get(key,0)+1
        if 'enhetsregisteret' in key and seen[key]<3:raise SourceFailure('dns_error')
        return httpx.Response(200)
    async def run():
        b=FakeBudget()
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:r=await m.health_check(client,CFG,b)
        assert all(x['state']=='reachable' for x in r)
        assert waits==[5,20] and len(b.events)==4 and not b.source_outages
        assert m.summary(b.events,r)['counts']['recovered_attempts']==2
    asyncio.run(run())
def test_down_source_bounded_and_scoped(monkeypatch):
    waits=[]
    async def sleep(seconds):waits.append(seconds)
    monkeypatch.setattr(m.asyncio,'sleep',sleep)
    async def run():
        b=FakeBudget()
        async with httpx.AsyncClient(transport=httpx.MockTransport(lambda r:httpx.Response(503))) as client:r=await m.health_check(client,CFG,b)
        assert len(b.events)==6 and all(x['attempts']==3 and x['state']=='unavailable' for x in r)
        assert sorted(waits)==[5,5,20,20]
        with pytest.raises(SourceFailure,match='source_outage_enhetsregisteret'):m.check_source(b,'https://data.brreg.no/enhetsregisteret/api/enheter/123')
        m.check_source(b,'https://example.no/')
    asyncio.run(run())
def test_budget_stop_no_extra_attempt(monkeypatch):
    async def sleep(seconds):raise AssertionError('No sleeping once requests exhausted')
    monkeypatch.setattr(m.asyncio,'sleep',sleep)
    async def run():
        b=FakeBudget(cap=1)
        async with httpx.AsyncClient(transport=httpx.MockTransport(lambda r:httpx.Response(503))) as client:r=await m.health_check(client,CFG,b)
        assert len(b.events)==1 and all(x['state']=='cut_off' for x in r)
    asyncio.run(run())
def test_refusal_not_retried_or_secret_persisted():
    async def run():
        b=FakeBudget()
        async with httpx.AsyncClient(transport=httpx.MockTransport(lambda r:httpx.Response(403,content=b'credential-must-not-persist'))) as client:r=await m.health_check(client,CFG,b)
        assert len(b.events)==2 and all(x['state']=='refused_or_rate_limited' for x in r)
        assert 'credential' not in str(b.events)+str(r)
    asyncio.run(run())
def test_deadline_does_not_start_probe():
    async def run():
        b=FakeBudget(remaining=-1)
        def fail(r):raise AssertionError('Request beyond deadline')
        async with httpx.AsyncClient(transport=httpx.MockTransport(fail)) as client:r=await m.health_check(client,CFG,b)
        assert not b.events and all(x['state']=='cut_off' for x in r)
    asyncio.run(run())

@pytest.mark.parametrize('exc',[httpx.ConnectError,httpx.ReadTimeout,httpx.RemoteProtocolError])
def test_connect_timeout_protocol_recovery(monkeypatch,exc):
    seen={};waits=[]
    async def sleep(seconds):waits.append(seconds)
    monkeypatch.setattr(m.asyncio,'sleep',sleep)
    def handler(request):
        key=str(request.url);seen[key]=seen.get(key,0)+1
        if seen[key]==1:raise exc('simulated failure',request=request)
        return httpx.Response(200)
    async def run():
        b=FakeBudget()
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:r=await m.health_check(client,CFG,b)
        assert len(b.events)==4 and waits==[5,5] and all(x['state']=='reachable' for x in r)
    asyncio.run(run())
