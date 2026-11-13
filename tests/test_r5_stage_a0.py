import sys
import pytest
from signalpost import cli
from signalpost.budget import Budget, SourceFailure
from signalpost.config import Config
from tests.test_registry import config, numbers, execute


@pytest.mark.parametrize('flags,enabled', [([], True),
    (['--websites','--hiring','--public-activity'], True),
    (['--no-websites','--no-hiring','--no-public-activity'], False)])
def test_evaluator_features_and_optouts(tmp_path, monkeypatch, flags, enabled):
    async def capture(cfg):
        assert (cfg.websites,cfg.hiring,cfg.public_activity)==(enabled,)*3
        assert (cfg.website_request_cap,cfg.website_total_request_cap)==(8,13)
        return dict(emitted_envelopes=100,invalid_inputs=[],requests=0,runtime_ms=0,
                    changes=0,observation_changes=0,deadline_hits=0,warnings=[])
    monkeypatch.setattr(cli,'run',capture)
    monkeypatch.setattr(sys,'argv',['signalpost','run','--organisations','batch',
        '--bulk','registry','--output',str(tmp_path/'out'),
        '--profiles-output',str(tmp_path/'profiles'),'--report',str(tmp_path/'report'),
        '--run-id','a0-seven','--expected-count','100',*flags])
    assert cli.main()==0


def test_library_enrichment_defaults():
    cfg=Config(organisations='batch',output='out',report='report')
    assert cfg.websites and cfg.hiring and cfg.public_activity
    assert (cfg.website_request_cap,cfg.website_total_request_cap)==(8,13)


@pytest.mark.parametrize('count,cap',[(1,18),(2,37),(100,1850),(200,3700)])
def test_hard_http_and_time_ceiling_scales_and_overrides_only_lower(tmp_path,count,cap):
    cfg=config(tmp_path,numbers(count),max_requests=100000,time_budget_seconds=100000)
    budget=Budget(cfg)
    assert budget.cap==cap and budget.total_seconds==21*count
    for _ in range(cap): budget.reserve('https://data.brreg.no/test','data.brreg.no','__shared__')
    with pytest.raises(SourceFailure,match='budget_exhausted'):
        budget.reserve('https://data.brreg.no/test','data.brreg.no',numbers(1)[0])
    assert len(budget.events)==cap
    cfg.max_requests=3;cfg.time_budget_seconds=2
    assert Budget(cfg).cap==3 and Budget(cfg).total_seconds==2


def test_duplicate_inputs_cannot_inflate_safety_budget(tmp_path):
    org=numbers(1)[0]
    budget=Budget(config(tmp_path,[org]*100,max_requests=9999))
    assert budget.cap==18 and budget.total_seconds==21


def test_deadline_is_hard_and_cannot_be_extended(tmp_path,monkeypatch):
    import signalpost.budget as module
    clock=[100.0];monkeypatch.setattr(module.time,'monotonic',lambda:clock[0])
    budget=Budget(config(tmp_path,numbers(100),time_budget_seconds=100000))
    assert budget.deadline <= 100+2100 and budget.crawl_limit==budget.deadline
    clock[0]=budget.deadline
    with pytest.raises(SourceFailure,match='deadline'):
        budget.reserve('https://data.brreg.no/test','data.brreg.no','org')
    assert not budget.events


def test_budget_cutoff_keeps_outputs_and_site_inside_requested_time(tmp_path):
    cfg=config(tmp_path,numbers(3),max_requests=1,time_budget_seconds=20,
               site_dir=tmp_path/'site',profiles_output=tmp_path/'profiles.jsonl')
    report,rows=execute(cfg)
    assert report['requests']==1 and len(rows)==3
    assert all(any(e['code']=='budget_exhausted' for e in row['errors']) for row in rows)
    assert report['site']['state']=='available' and (cfg.site_dir/'index.html').exists()
    assert cfg.output.exists() and cfg.profiles_output.exists() and cfg.report.exists()
    assert report['completion']['within_requested_time_budget']
