import asyncio,hashlib,importlib.util,sys
from pathlib import Path
from types import SimpleNamespace
import httpx,pytest
from signalpost.budget import SourceFailure
from tests.test_official_resilience import FakeBudget
from signalpost.sources import exact_public as m
from signalpost.sources import official_resilience as retry
class Blobs:
    def put(self,body):return hashlib.sha256(body).hexdigest()
CFG=SimpleNamespace(request_timeout=1,website_user_agent='SignalpostTest')
URL='https://api.gleif.org/api/v1/lei-records?filter=x'
@pytest.mark.parametrize('exc',[SourceFailure('dns_error'),httpx.ConnectError('x'),httpx.RemoteProtocolError('x')])
def test_public_transient_recovery(monkeypatch,exc):
    calls=[];waits=[]
    async def sleep(s):waits.append(s)
    monkeypatch.setattr(retry.asyncio,'sleep',sleep);monkeypatch.setattr(m,'POLITENESS_SECONDS',0)
    def handler(r):
        calls.append(str(r.url))
        if len(calls)<3:raise exc
        return httpx.Response(200,json={'data':[]})
    async def run():
        b=FakeBudget()
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:r=await m.PublicHttp(client,CFG,b,Blobs()).raw(URL,'986464492')
        assert r.status==200 and len(b.events)==3 and waits==[5,20]
    asyncio.run(run())
def test_public_5xx_retry_after_and_final_failure(monkeypatch):
    waits=[]
    async def sleep(s):waits.append(s)
    monkeypatch.setattr(retry.asyncio,'sleep',sleep);monkeypatch.setattr(m,'POLITENESS_SECONDS',0)
    async def run():
        b=FakeBudget(remaining=240)
        async with httpx.AsyncClient(transport=httpx.MockTransport(lambda r:httpx.Response(503,headers={'Retry-After':'12'}))) as client:
            h=m.PublicHttp(client,CFG,b,Blobs())
            with pytest.raises(SourceFailure,match='public_robots_unavailable_http503'):await h.request(URL,'986464492')
        assert len(b.events)==5 and waits==[12,20,40,60]
    asyncio.run(run())
def test_public_rate_refusal_no_retry(monkeypatch):
    monkeypatch.setattr(m,'POLITENESS_SECONDS',0)
    async def run():
        b=FakeBudget()
        async with httpx.AsyncClient(transport=httpx.MockTransport(lambda r:httpx.Response(429))) as client:r=await m.PublicHttp(client,CFG,b,Blobs()).raw(URL,'986464492')
        assert r.status==429 and len(b.events)==1
    asyncio.run(run())


def test_crawled_notice_host_fails_closed_on_robots_timeout(monkeypatch):
    async def sleep(_):
        pass

    monkeypatch.setattr(retry.asyncio, 'sleep', sleep)
    monkeypatch.setattr(m, 'POLITENESS_SECONDS', 0)
    budget = FakeBudget()

    def handler(request):
        assert request.url.path == '/robots.txt'
        raise httpx.ConnectTimeout('robots unavailable')

    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            http = m.PublicHttp(client, CFG, budget, Blobs())
            for _ in range(2):
                with pytest.raises(SourceFailure, match='robots.txt unavailable|public_robots_unavailable'):
                    await http.request('https://ted.europa.eu/en/notice/123/xml', '986464492')

    asyncio.run(run())
    assert len(budget.events) == 3
