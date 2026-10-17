"""Scope handoff to NAV must never block terminal output (capacity check P0).

The subunit queue holds 100 items. If the NAV reader exits early or stops
reading, more than 100 producers used to wait for queue space forever, so no
envelope was ever written. Each run is executed in a daemon thread so a
regression fails the test instead of hanging the suite.
"""
import asyncio
import json
import threading
import time

import respx

from signalpost.runner import run
from signalpost.sources import nav
from tests.test_registry import config, handler, numbers

COMPANIES = 150  # Above the queue's maxsize of 100.


def bounded(cfg, limit):
    outcome = {}

    def target():
        with respx.mock(assert_all_called=False) as router:
            router.get(url__regex=r"https://data\.brreg\.no/.*").mock(side_effect=handler())
            try:
                outcome['report'] = asyncio.run(run(cfg))
            except BaseException as exc:  # Reported by the assertion below.
                outcome['error'] = exc
    began = time.monotonic()
    worker = threading.Thread(target=target, daemon=True)
    worker.start()
    worker.join(limit)
    assert not worker.is_alive(), f'run did not finish within {limit}s (scope handoff deadlock)'
    assert 'error' not in outcome, outcome.get('error')
    rows = [json.loads(x) for x in cfg.output.read_text(encoding='utf-8').splitlines()]
    return outcome['report'], rows, time.monotonic() - began


def membership(cfg, rows, orgs):
    assert [r['organisation_number'] for r in rows] == orgs
    assert json.loads(cfg.report.read_text(encoding='utf8'))['emitted_envelopes'] == len(orgs)


def test_early_nav_exit_with_full_queue_emits_every_envelope(tmp_path, monkeypatch):
    async def early_exit(client, config, budget, blobs, index, names_ready=None, previous=None):
        index.started.set()
        index.reason = 'nav_time_cap'
        return index  # Never reads names_ready.subunit_queue.
    monkeypatch.setattr(nav, 'prefetch', early_exit)
    orgs = numbers(COMPANIES)
    cfg = config(tmp_path, orgs, hiring=True, workers=16, time_budget_seconds=600)
    report, rows, _ = bounded(cfg, 60)
    membership(cfg, rows, orgs)
    assert report['deadline_hits'] == 0
    # Registry facts survive; hiring is explicitly failed, never silently empty.
    assert all(r['run']['sections']['identity'] == 'available' for r in rows)
    assert all(r['run']['sections']['hiring'] == 'failed' for r in rows)
    codes = {e['code'] for r in rows for e in r['errors'] if e['section'] == 'hiring'}
    assert 'nav_consumer_stopped' in codes


def test_forced_deadline_with_stalled_nav_reader_finishes(tmp_path, monkeypatch):
    async def stalled(client, config, budget, blobs, index, names_ready=None, previous=None):
        index.started.set()
        await asyncio.sleep(3600)  # Alive but never reads the queue.
        return index
    monkeypatch.setattr(nav, 'prefetch', stalled)
    orgs = numbers(COMPANIES)
    cfg = config(tmp_path, orgs, hiring=True, workers=16, time_budget_seconds=2, deadline_fraction=1)
    report, rows, elapsed = bounded(cfg, 60)
    membership(cfg, rows, orgs)
    assert elapsed < 2 + 15, elapsed  # Deadline plus bounded cancellation grace and output.
    # Identity is either extracted or honestly marked as cut off by the deadline.
    assert any(r['run']['sections']['identity'] == 'available' for r in rows)
    for r in rows:
        if r['run']['sections']['identity'] != 'available':
            assert any(e['section'] == 'identity' and e['code'] == 'deadline' for e in r['errors'])
    assert all(r['run']['sections']['hiring'] == 'failed' for r in rows)
    stuck = [r for r in rows if any(e['code'] == 'deadline' and e['section'] == 'hiring' for e in r['errors'])]
    assert stuck, 'companies whose scope could not be handed over must report deadline'
