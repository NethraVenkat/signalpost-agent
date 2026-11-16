from signalpost.budget import Budget
from signalpost.sources.nav import time_cap
from tests.test_registry import config,execute


def test_derived_budget_uses_unique_inputs_and_override(tmp_path):
    cfg=config(tmp_path/'auto',['923609016','923609016','bad'])
    # Default time is the scaled limit itself (35 min per 100 unique inputs): 2 unique -> 42 s.
    assert Budget(cfg).cap==37 and cfg.time_budget_seconds is None and Budget(cfg).total_seconds==42
    assert time_cap(cfg)==840
    report,rows=execute(cfg)
    assert len(rows)==3 and report['limits']['max_requests']==37
    assert report['request_budget_basis']=='1850 per 100 unique normalized inputs; explicit overrides only lower the ceiling'
    assert report['measured_request_projection']['projected_http']==12
    assert Budget(config(tmp_path/'override',['923609016'],max_requests=7)).cap==7


def test_default_time_scales_with_inputs_and_flag_only_lowers(tmp_path):
    orgs=['923609016','974760673','981405099']
    assert Budget(config(tmp_path/'a',orgs)).total_seconds==63
    assert Budget(config(tmp_path/'b',orgs,time_budget_seconds=30)).total_seconds==30
    assert Budget(config(tmp_path/'c',orgs,time_budget_seconds=9999)).total_seconds==63
