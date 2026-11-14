import asyncio
import httpx
import pytest
from signalpost.web.fetcher import WebsiteHttp,REQUEST_SECONDS
from signalpost.web.candidates import Candidate
from signalpost.budget import Budget,SourceFailure
from signalpost.sources.blobstore import BlobStore
from tests.test_registry import config

@pytest.mark.parametrize('origin,expected',[('registry_website',[8,16]),('registry_email',[8])])
def test_declared_timeout_gets_one_longer_retry_only(tmp_path,origin,expected):
    async def run():
        cfg=config(tmp_path,['923609016']);seen=[]
        async with httpx.AsyncClient() as client:
            http=WebsiteHttp(client,cfg,Budget(cfg),BlobStore(tmp_path))
            async def precheck(*a):pass
            async def get(*a,**k):
                seen.append(REQUEST_SECONDS.get());raise SourceFailure('website_timeout')
            http.precheck=precheck;http.get=get
            with pytest.raises(SourceFailure):await http.candidate(Candidate('https://example.no/','example.no',origin),'923609016')
            assert seen==expected and REQUEST_SECONDS.get()==8
    asyncio.run(run())

def test_retry_never_runs_after_budget_exhaustion(tmp_path):
    async def run():
        cfg=config(tmp_path,['923609016']);seen=[]
        async with httpx.AsyncClient() as client:
            http=WebsiteHttp(client,cfg,Budget(cfg),BlobStore(tmp_path))
            async def get(*a,**k):seen.append(REQUEST_SECONDS.get());raise SourceFailure('website_budget_exhausted')
            http.get=get
            with pytest.raises(SourceFailure):await http.candidate(Candidate('https://example.no/','example.no','registry_website'),'923609016')
            assert seen==[8]
    asyncio.run(run())
