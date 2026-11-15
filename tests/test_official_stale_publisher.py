import asyncio,json,shutil,copy
import pytest
import httpx
from tests.test_websites import execute_web,html,OUR
from tests.test_registry import config
from signalpost.runner import run
from signalpost.sources import official_resilience
from scripts.verify_output import verify

def test_official_outage_keeps_high_publisher_original_evidence_stale(tmp_path,monkeypatch):
    _,old,_,prior=execute_web(tmp_path/'before',monkeypatch,body=html('Example AS'))
    website=next(c for c in old['claims'] if c['field']=='official_website')
    assert website['value']['identity_level']=='HIGH'
    cfg=config(tmp_path/'after',[OUR],websites=True,official_source_health=True,previous=prior.output,site_dir=tmp_path/'after/site')
    # Retain immutable historical evidence only; no HTTP/result cache is reused.
    shutil.copytree(prior.state_dir/'blobs',cfg.state_dir/'blobs',dirs_exist_ok=True)
    async def wait(budget,event,attempt,minimum=0,deadline=None):budget.check()
    monkeypatch.setattr(official_resilience,'pause',wait)
    async def execute():
        async with httpx.AsyncClient(transport=httpx.MockTransport(lambda r:httpx.Response(503))) as client:return await run(cfg,client=client)
    report=asyncio.run(execute())
    row=json.loads(cfg.output.read_text(encoding='utf8'))
    carried=next(c for c in row['claims'] if c['field']=='official_website')
    assert row['run']['sections']['website']=='failed' and carried['carried_forward']
    assert carried['evidence_ids']==website['evidence_ids']
    assert 'Previously supported' in (cfg.site_dir/'c'/f'{OUR}.html').read_text(encoding='utf8')
    assert report['site']['state']=='available' and report['requests']==6
    assert verify(cfg.output,cfg.state_dir,1)['briefing_unverified_values']==0

    # Marking this historical claim fresh must not make stale identity current.
    from scripts.verify_publisher_identity import verify as verify_publisher
    from signalpost.sources.text import decode_body
    forged=copy.deepcopy(row)
    next(c for c in forged['claims'] if c['field']=='official_website')['carried_forward']=False
    with pytest.raises(AssertionError,match='Unsupported publisher identity receipt'):
        verify_publisher(OUR,forged,{e['id']:e for e in forged['evidence']},lambda sha:decode_body((cfg.state_dir/'blobs'/sha).read_bytes()))
