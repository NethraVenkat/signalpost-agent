"""Finalisation time is reserved inside the budget; the optional site yields first."""
import json
from types import SimpleNamespace

import pytest

from signalpost.budget import (
    Budget, FINALISE_SECONDS_PER_COMPANY, WEBSITE_FINALISATION_SECONDS, WEBSITE_MARGIN_SECONDS,
    SITE_SECONDS_PER_COMPANY, SLOW_SITE_SECONDS_PER_COMPANY,
)
from signalpost.sources.blobstore import BlobStore
from tests.test_registry import config, execute, numbers


def budget_for(tmp_path, companies, seconds, site=True):
    cfg = config(tmp_path, numbers(companies), time_budget_seconds=seconds)
    if site:
        cfg.site_dir = tmp_path / 'site'
    return Budget(cfg)


def crawl_seconds(budget):
    return budget.deadline - budget.start


def test_reserve_covers_finalisation_and_site_for_a_comfortable_budget(tmp_path):
    budget = budget_for(tmp_path, 1000, 600)
    reserve = 600 - crawl_seconds(budget)
    assert budget.site_reserved
    assert reserve >= 1000 * (FINALISE_SECONDS_PER_COMPANY + SITE_SECONDS_PER_COMPANY) - 0.01
    assert reserve >= 60 - 1e-6  # Never below 10 percent.


def test_small_budget_drops_the_site_reserve_but_still_crawls(tmp_path):
    budget = budget_for(tmp_path, 1000, 30)
    assert not budget.site_reserved
    assert 5 <= crawl_seconds(budget) <= 15 + 1e-6  # Float subtraction of two clock readings is not exact.


@pytest.mark.parametrize('clock', [0.0, 40.5, 63.86063473633481, 524281.25896297226])
def test_deadline_arithmetic_does_not_depend_on_the_clock_value(tmp_path, monkeypatch, clock):
    """A freshly booted CI runner has a monotonic clock of ~60 s; 63.86063473633481 gave
    deadline subtraction once broke an exact comparison on a freshly booted runner."""
    import signalpost.budget as budget_module
    monkeypatch.setattr(budget_module.time, 'monotonic', lambda: clock)
    assert crawl_seconds(budget_for(tmp_path, 1000, 30)) == pytest.approx(12, abs=1e-9)
    assert crawl_seconds(budget_for(tmp_path / 'b', 1000, 600)) == pytest.approx(510, abs=1e-9)


def test_no_site_means_no_site_reserve(tmp_path):
    with_site = budget_for(tmp_path / 'a', 1000, 600, site=True)
    without = budget_for(tmp_path / 'b', 1000, 600, site=False)
    assert without.site_estimate == 0 and with_site.site_estimate > 0


def test_site_is_skipped_when_it_cannot_fit_but_required_outputs_exist(tmp_path, monkeypatch):
    import signalpost.budget as budget_module
    monkeypatch.setattr(budget_module, 'SITE_SECONDS_PER_COMPANY', 1000.0)
    cfg = config(tmp_path, numbers(3), time_budget_seconds=60)
    cfg.site_dir = tmp_path / 'site'
    report, rows = execute(cfg)
    assert len(rows) == 3 and cfg.profiles_output is None
    assert report['site']['state'] == 'skipped' and report['site']['reason'] == 'time_budget'
    assert not (tmp_path / 'site' / 'index.html').exists()  # progress.json alone may live there
    saved = json.loads(cfg.report.read_text(encoding='utf8'))
    assert saved['site']['state'] == 'skipped' and saved['emitted_envelopes'] == 3
    assert 'outputs_seconds' in saved['finalisation']


def test_blob_reads_come_from_memory_after_a_write(tmp_path):
    store = BlobStore(tmp_path)
    sha = store.put(b'hello')
    (store.directory / sha).unlink()  # A re-read from disk would now fail.
    assert store.read(sha) == b'hello'
    assert store.read('0' * 64) is None


def test_fixed_500_budget_covers_twice_the_measured_finalisation(tmp_path):
    cfg = config(tmp_path, numbers(500), site_dir=tmp_path / 'site')
    budget = Budget(cfg)
    assert budget.total_seconds == 2100
    assert crawl_seconds(budget) == pytest.approx(1785)
    # P3g's measured cutoff includes crawl cancellation. Double mandatory and
    # optional finalisation, and allow ten seconds for completion/CLI overhead.
    site_estimate = SLOW_SITE_SECONDS_PER_COMPANY * budget.companies
    assert site_estimate >= 2 * 38.91
    assert 1786.02 + 2 * 63.59 + site_estimate + 10 < budget.total_seconds


@pytest.mark.parametrize(('companies', 'cutoff'), [(100, 1700), (500, 1700), (750, 1700)])
def test_website_cutoff_reserves_time_without_moving_global_deadline(tmp_path, companies, cutoff):
    budget = budget_for(tmp_path, companies, 2100)
    assert budget.total_seconds == 2100
    assert crawl_seconds(budget) == pytest.approx(1785)
    assert budget.website_deadline - budget.start == pytest.approx(cutoff)
    assert cutoff + WEBSITE_FINALISATION_SECONDS <= budget.total_seconds - WEBSITE_MARGIN_SECONDS
    assert crawl_seconds(budget) == pytest.approx(1785)


def test_website_uses_original_deadline_for_small_custom_and_scaled_runs(tmp_path):
    small = budget_for(tmp_path / 'small', 20, 2100)
    custom = budget_for(tmp_path / 'custom', 100, 600)
    scaled = Budget(config(tmp_path / 'scaled', numbers(500), scaled_time_budget=True))
    for budget in (small, custom, scaled):
        assert budget.website_deadline == budget.deadline
    assert scaled.total_seconds == 10_500


def test_site_that_runs_out_of_time_keeps_all_required_outputs(tmp_path, monkeypatch):
    from signalpost import site

    orgs = numbers(2)
    cfg = config(tmp_path, orgs, time_budget_seconds=60,
                 profiles_output=tmp_path / 'profiles.jsonl', site_dir=tmp_path / 'site')
    original = site.profile
    rendered = []

    def overrun(row, *args, **kwargs):
        rendered.append(row['organisation_number'])
        html = original(row, *args, **kwargs)
        monkeypatch.setattr(site, 'monotonic', lambda: float('inf'))
        return html

    monkeypatch.setattr(site, 'profile', overrun)
    report, rows = execute(cfg)
    assert len(rendered) == 1
    assert report['site']['state'] == 'skipped' and report['site']['reason'] == 'time_budget'
    assert not (cfg.site_dir / 'index.html').exists()
    assert [row['organisation_number'] for row in rows] == orgs
    profiles = [json.loads(line) for line in cfg.profiles_output.read_text(encoding='utf8').splitlines()]
    assert [row['organisation_number'] for row in profiles] == orgs
    saved = json.loads(cfg.report.read_text(encoding='utf8'))
    assert saved['emitted_envelopes'] == len(orgs) and saved['site']['state'] == 'skipped'
