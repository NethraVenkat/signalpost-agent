from signalpost.budget import Budget
from signalpost.sources.nav import time_cap
from tests.test_registry import config,execute


def test_derived_budget_uses_unique_inputs_and_override(tmp_path):
    cfg=config(tmp_path/'auto',['923609016','923609016','bad'])
    assert Budget(cfg).cap==37 and cfg.time_budget_seconds==2100
    assert time_cap(cfg)==840
    report,rows=execute(cfg)
    assert len(rows)==3 and report['limits']['max_requests']==37
    assert report['request_budget_basis']=='1850 per 100 unique normalized inputs; explicit overrides only lower the ceiling'
    assert report['measured_request_projection']['projected_http']==12
    assert Budget(config(tmp_path/'override',['923609016'],max_requests=7)).cap==7


def numbers(n):
    from signalpost.identity.orgnr import valid
    out, x = [], 923609016
    while len(out) < n:
        if valid(str(x)): out.append(str(x))
        x += 1
    return out


def test_default_time_budget_does_not_grow_with_batch_size(tmp_path):
    # P3f: fixed evaluator budget. 100 and 500 inputs get the same 2,100 s total.
    small = Budget(config(tmp_path/'s',numbers(100)))
    large = Budget(config(tmp_path/'l',numbers(500)))
    assert small.total_seconds == large.total_seconds == 2100
    assert large.deadline - large.start <= 2100 * 0.85 + 1e-6


def test_scaled_time_budget_is_explicit_opt_in(tmp_path):
    assert Budget(config(tmp_path/'o',numbers(500),scaled_time_budget=True)).total_seconds == 10500
    assert Budget(config(tmp_path/'d',numbers(3))).total_seconds == 63  # small batches stay at 21 s each
