"""Finalisation time is reserved inside the budget; the optional site yields first."""
import json
from types import SimpleNamespace

from signalpost.budget import Budget, FINALISE_SECONDS_PER_COMPANY, SITE_SECONDS_PER_COMPANY
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
    assert reserve >= 60  # Never below 10 percent.


def test_small_budget_drops_the_site_reserve_but_still_crawls(tmp_path):
    budget = budget_for(tmp_path, 1000, 30)
    assert not budget.site_reserved
    assert 5 <= crawl_seconds(budget) <= 15


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
