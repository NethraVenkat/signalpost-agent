import asyncio
from signalpost.sources.nav import Index
from signalpost.sources.nav_cached import Candidates
from tests.test_nav_index import artifact
from tests.test_registry import config
from tests.test_nav import ORG,UUID,SUB
from tests.test_nav_streaming import header


def test_inflight_scope_renomination_does_not_spend_another_detail_attempt(tmp_path):
    _,data=artifact(tmp_path)
    state=Candidates(data,Index(),config(tmp_path,[ORG]),{})
    state.set_scopes({ORG:{ORG}},{ORG:{'Rareone AS'}})
    uuid,record=state.take()
    state.candidate(uuid,{ORG},'declared_cache')
    state.checked[uuid]=record[0];state.inflight.remove(uuid)
    assert state.take() is None
    assert state.index.metrics['redundant_detail_jobs_skipped']==1


def test_newer_header_still_requires_detail_after_inflight_old_version(tmp_path):
    _,data=artifact(tmp_path)
    state=Candidates(data,Index(),config(tmp_path,[ORG]),{})
    state.set_scopes({ORG:{ORG}},{ORG:{'Rareone AS'}})
    uuid,record=state.take()
    item=header(UUID,'Rareone AS');item['date_modified']='2026-10-15T12:00:00Z'
    asyncio.run(state.page([item]))
    state.checked[uuid]=record[0];state.inflight.remove(uuid)
    second=state.take()
    assert second and second[1][0]!=record[0]


def test_failed_version_is_not_retried_until_source_version_changes(tmp_path):
    _,data=artifact(tmp_path)
    state=Candidates(data,Index(),config(tmp_path,[ORG]),{})
    state.set_scopes({ORG:{ORG}},{ORG:{'Rareone AS'}})
    uuid,record=state.take();state.failed[uuid]=record[0];state.inflight.remove(uuid)
    state.candidate(uuid,{ORG},'declared_cache')
    assert state.take() is None
    item=header(UUID,'Rareone AS');item['date_modified']='2026-10-15T12:00:00Z'
    asyncio.run(state.page([item]))
    assert state.take()[0]==UUID


def test_production_prefetch_coalesces_scope_added_during_live_detail(tmp_path):
    import httpx
    from signalpost.sources.nav import prefetch
    from signalpost.sources.blobstore import BlobStore
    from signalpost.budget import Budget
    from tests.test_nav import TOKEN
    from tests.test_nav_streaming import ad
    path,_=artifact(tmp_path)
    cfg=config(tmp_path,[ORG],hiring=True,nav_index_path=path,nav_max_details=2)
    async def execute():
        started=asyncio.Event();ready=asyncio.Event();calls=[]
        async def names():
            await started.wait();ready.set();return {ORG:{'Rareone AS'}}
        names.initial_names={ORG:{'Rareone AS'}}
        async def dispatch(request):
            if request.url.path=='/api/publicToken':return httpx.Response(200,text=TOKEN)
            if '/feedentry/' in request.url.path:
                calls.append(str(request.url));started.set();await ready.wait()
                return httpx.Response(200,json=ad(UUID,ORG))
            return httpx.Response(200,json={'items':[],'next_url':None})
        index=Index()
        async with httpx.AsyncClient(transport=httpx.MockTransport(dispatch)) as client:
            await prefetch(client,cfg,Budget(cfg),BlobStore(cfg.state_dir),index,names)
        return index,calls
    index,calls=asyncio.run(execute())
    assert len(calls)==index.metrics['detail_requests']==1
    assert index.complete and len(index.ads[ORG])==1
    assert index.metrics['redundant_detail_jobs_skipped']==1
