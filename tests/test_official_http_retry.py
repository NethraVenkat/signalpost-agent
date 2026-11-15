import asyncio,hashlib,importlib.util,sys
from pathlib import Path
from types import SimpleNamespace
import httpx,pytest
from signalpost.budget import SourceFailure
from tests.test_official_resilience import FakeBudget
from signalpost.sources import http as m
from signalpost.sources import official_resilience as retry
class Blobs:
    def put(self,body):return hashlib.sha256(body).hexdigest()
URL='https://data.brreg.no/enhetsregisteret/api/enheter/986464492'
CFG=SimpleNamespace(request_timeout=1,host_concurrency=1)
@pytest.mark.parametrize('exc',[SourceFailure('dns_error'),httpx.ConnectError('x'),httpx.ReadTimeout('x'),httpx.RemoteProtocolError('x')])
def test_real_http_client_recovers_twice(monkeypatch,exc):
    calls=[];waits=[]
    async def sleep(s):waits.append(s)
    monkeypatch.setattr(retry.asyncio,'sleep',sleep)
    def handler(r):
        calls.append(str(r.url))
        if len(calls)<3:raise exc
        return httpx.Response(200,json={'organisasjonsnummer':'986464492'})
    async def run():
        b=FakeBudget()
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:response=await m.Http(client,CFG,b,Blobs()).get(URL,'986464492')
        assert response.status==200 and len(calls)==len(b.events)==3 and waits==[5,20]
    asyncio.run(run())
def test_5xx_stops_after_three_and_stays_explicit(monkeypatch):
    waits=[]
    async def sleep(s):waits.append(s)
    monkeypatch.setattr(retry.asyncio,'sleep',sleep)
    async def run():
        b=FakeBudget()
        async with httpx.AsyncClient(transport=httpx.MockTransport(lambda r:httpx.Response(503))) as client:r=await m.Http(client,CFG,b,Blobs()).get(URL,'986464492')
        assert r.status==503 and len(b.events)==3 and waits==[5,20]
    asyncio.run(run())
def test_filing_years_shared_429_cooldown_preserved():
    async def run():
        b=FakeBudget()
        async with httpx.AsyncClient(transport=httpx.MockTransport(lambda r:httpx.Response(429,headers={'Retry-After':'70'}))) as client:
            h=m.Http(client,CFG,b,Blobs());r=await h.get('https://data.brreg.no/regnskapsregisteret/aarsregnskap/kopi/986464492/aar','986464492')
            assert r.status==429 and len(b.events)==1 and b.events[0]['rate_limit_backoff_seconds']==70
    asyncio.run(run())
def test_nonfiling_429_still_only_one_retry(monkeypatch):
    waits=[]
    async def sleep(s):waits.append(s)
    monkeypatch.setattr(retry.asyncio,'sleep',sleep)
    async def run():
        b=FakeBudget()
        async with httpx.AsyncClient(transport=httpx.MockTransport(lambda r:httpx.Response(429,headers={'Retry-After':'12'}))) as client:r=await m.Http(client,CFG,b,Blobs()).get(URL,'986464492')
        assert r.status==429 and len(b.events)==2 and waits==[12]
    asyncio.run(run())
def test_permanent_source_refusal_not_retried():
    async def run():
        b=FakeBudget()
        def handler(r):raise SourceFailure('ssrf')
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            with pytest.raises(SourceFailure,match='ssrf'):await m.Http(client,CFG,b,Blobs()).get(URL,'986464492')
        assert len(b.events)==1
    asyncio.run(run())
