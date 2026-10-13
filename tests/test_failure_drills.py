import json
from pathlib import Path
import httpx
import pytest
from tests.test_registry import config,execute,handler,numbers
from scripts.verify_output import verify


def checked(cfg,report,rows,count):
    assert len(rows)==count
    assert report['emitted_envelopes']==count and report['unhandled_exceptions']==0
    assert json.loads(cfg.report.read_text(encoding='utf8'))['schema_validated']
    verify(cfg.output,cfg.state_dir,count,cfg.organisations,cfg.report)


def test_thirty_percent_503_isolated(tmp_path):
    orgs=numbers(10);broken=set(orgs[:3])
    def response(request):
        if any('/'+org in request.url.path for org in broken):return httpx.Response(503)
        return handler()(request)
    cfg=config(tmp_path,orgs);report,rows=execute(cfg,response)
    checked(cfg,report,rows,10)
    assert all(row['run']['sections']['identity']=='failed' for row in rows[:3])
    assert all(row['run']['sections']['identity']=='available' for row in rows[3:])


def test_registry_unreachable_with_bulk_identity(tmp_path):
    cfg=config(tmp_path,['923609016'])
    bulk=tmp_path/'bulk.csv';bulk.write_text('organisasjonsnummer,navn\n923609016,Known AS\n',encoding='utf8');cfg.bulk=bulk
    def failed(request):raise httpx.ConnectError('synthetic',request=request)
    report,rows=execute(cfg,failed);checked(cfg,report,rows,1)
    assert rows[0]['run']['sections']['identity']=='available'
    assert all(rows[0]['run']['sections'][f]=='failed' for f in ['roles','accounts','subunits'])


@pytest.mark.parametrize('kind',['missing','unreadable','columns'])
def test_bad_bulk_falls_back_without_losing_rows(tmp_path,kind):
    cfg=config(tmp_path,['923609016']);cfg.bulk=tmp_path/'bulk.csv'
    if kind=='unreadable':cfg.bulk.mkdir()
    if kind=='columns':cfg.bulk.write_text('unexpected\nvalue\n',encoding='utf8')
    report,rows=execute(cfg);checked(cfg,report,rows,1)
    assert rows[0]['run']['sections']['identity']=='available'
    assert any('bulk unavailable' in w for w in report['warnings'])


def test_nav_token_down_and_truncated_feed(tmp_path):
    from tests.test_nav import execute as nav_run
    for label,kw,state in [('token',{'token_ok':False},'blocked'),('partial',{'partial':True},'failed')]:
        report,row,cfg,_=nav_run(tmp_path/label,**kw)
        checked(cfg,report,[row],1)
        assert row['run']['sections']['hiring']==state
        assert report['hiring_prefetch']['feed_complete'] is False
        assert row['run']['sections']['identity']=='available'


def test_websites_timeout_registry_survives(tmp_path,monkeypatch):
    from tests.test_websites import execute_web
    def timeout(request):
        if request.url.path=='/robots.txt':return httpx.Response(200,text='User-agent: *\nAllow: /')
        raise httpx.ReadTimeout('synthetic',request=request)
    report,row,_,cfg=execute_web(tmp_path,monkeypatch,response=timeout,public_activity=True)
    checked(cfg,report,[row],1)
    assert row['run']['sections']['website']==row['run']['sections']['activity']=='failed'
    assert row['run']['sections']['identity']=='available'


def test_tiny_request_cap_and_deadline_preserve_membership(tmp_path):
    orgs=numbers(100)
    cfg=config(tmp_path/'cap',orgs,max_requests=50)
    report,rows=execute(cfg);checked(cfg,report,rows,100)
    assert report['requests']<=50
    assert any(e['code']=='budget_exhausted' for row in rows for e in row['errors'])
    cfg=config(tmp_path/'deadline',orgs,time_budget_seconds=.01,deadline_fraction=.3)
    report,rows=execute(cfg);checked(cfg,report,rows,100)
    assert report['deadline_hits']>0


def test_site_unwritable_isolated(tmp_path):
    cfg=config(tmp_path,['923609016']);cfg.site_dir=tmp_path/'site';cfg.site_dir.write_text('file blocks directory',encoding='utf8')
    report,rows=execute(cfg);checked(cfg,report,rows,1)
    assert report['site']['state']=='failed'
    assert rows[0]['run']['sections']['identity']=='available'


def test_state_unwritable_yields_valid_failure_envelopes(tmp_path):
    cfg=config(tmp_path,['923609016','bad']);cfg.state_dir=tmp_path/'state-file';cfg.state_dir.write_text('file blocks directory',encoding='utf8')
    report,rows=execute(cfg);checked(cfg,report,rows,2)
    assert report['requests']==0 and any('state storage unavailable' in w for w in report['warnings'])
    assert all(state=='failed' for state in rows[0]['run']['sections'].values())
    assert any(e['code']=='state_unavailable' for e in rows[0]['errors'])


def test_malformed_previous_baseline_with_warning(tmp_path):
    cfg=config(tmp_path,['923609016']);cfg.previous=tmp_path/'previous.jsonl';cfg.previous.write_text('{broken',encoding='utf8')
    report,rows=execute(cfg);checked(cfg,report,rows,1)
    assert report['warnings'] and rows[0]['run']['refresh']['mode']=='baseline'
