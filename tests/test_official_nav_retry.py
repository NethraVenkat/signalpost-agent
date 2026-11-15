import asyncio,hashlib,importlib.util,sys
from pathlib import Path
from types import SimpleNamespace
import httpx,pytest
from signalpost.budget import SourceFailure
from tests.test_official_resilience import FakeBudget
from signalpost.sources import nav as m
from signalpost.sources import official_resilience as retry
class Blobs:
    def __init__(self,path):self.directory=path;self.bodies=[]
    def put(self,body):self.bodies.append(body);return hashlib.sha256(body).hexdigest()
def cfg(path):return SimpleNamespace(state_dir=path,nav_concurrency=1,nav_max_details=300,website_user_agent='Test',nav_request_timeout=1,nav_body_cap_mb=2)
@pytest.mark.parametrize('exc',[SourceFailure('dns_error'),httpx.ConnectError('x'),httpx.RemoteProtocolError('x'),httpx.ReadTimeout('x')])
def test_nav_recovers_twice(tmp_path,monkeypatch,exc):
    calls=[];waits=[]
    async def sleep(s):waits.append(s)
    monkeypatch.setattr(retry.asyncio,'sleep',sleep)
    def handler(r):
        calls.append(str(r.url))
        if len(calls)<3:raise exc
        return httpx.Response(200,json={'items':[]})
    async def run():
        b=FakeBudget();blobs=Blobs(tmp_path)
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:r=await m.NavHttp(client,cfg(tmp_path),b,blobs,m.Index()).get(m.BASE+'/api/v1/feed')
        assert r[0]==200 and len(b.events)==3 and waits==[5,20]
    asyncio.run(run())
def test_nav_secret_retries_never_persist_bodies(tmp_path,monkeypatch):
    calls=[];waits=[]
    async def sleep(s):waits.append(s)
    monkeypatch.setattr(retry.asyncio,'sleep',sleep)
    def handler(r):
        calls.append(str(r.url));return httpx.Response(503 if len(calls)<3 else 200,content=b'credential-must-not-persist')
    async def run():
        b=FakeBudget();blobs=Blobs(tmp_path)
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:r=await m.NavHttp(client,cfg(tmp_path),b,blobs,m.Index()).get(m.BASE+'/api/publicToken',secret=True)
        assert r[0]==200 and len(b.events)==3 and waits==[5,20] and not blobs.bodies
        assert 'credential-must-not-persist' not in str(b.events)
    asyncio.run(run())
def test_nav_http_5xx_final_explicit(tmp_path,monkeypatch):
    waits=[]
    async def sleep(s):waits.append(s)
    monkeypatch.setattr(retry.asyncio,'sleep',sleep)
    async def run():
        b=FakeBudget()
        async with httpx.AsyncClient(transport=httpx.MockTransport(lambda r:httpx.Response(503))) as client:
            with pytest.raises(SourceFailure,match='nav_http_503'):await m.NavHttp(client,cfg(tmp_path),b,Blobs(tmp_path),m.Index()).get(m.BASE+'/api/v1/feed')
        assert len(b.events)==3 and waits==[5,20]
    asyncio.run(run())
def test_nav_budget_stops_retry(tmp_path,monkeypatch):
    async def sleep(s):raise AssertionError('No wait with exhausted request budget')
    monkeypatch.setattr(retry.asyncio,'sleep',sleep)
    async def run():
        b=FakeBudget(cap=1)
        async with httpx.AsyncClient(transport=httpx.MockTransport(lambda r:httpx.Response(503))) as client:
            with pytest.raises(SourceFailure,match='budget_exhausted'):await m.NavHttp(client,cfg(tmp_path),b,Blobs(tmp_path),m.Index()).get(m.BASE+'/api/v1/feed')
        assert len(b.events)==1
    asyncio.run(run())

@pytest.mark.parametrize('status',[401,403])
def test_nav_credential_refusal_stays_blocked_reason(tmp_path,status):
    async def run():
        b=FakeBudget();blobs=Blobs(tmp_path)
        async with httpx.AsyncClient(transport=httpx.MockTransport(lambda r:httpx.Response(status,content=b'private-error'))) as client:
            h=m.NavHttp(client,cfg(tmp_path),b,blobs,m.Index());assert await h.public_token() is None
            assert h.token_failure=='token_unavailable' and len(b.events)==1 and not blobs.bodies
    asyncio.run(run())
