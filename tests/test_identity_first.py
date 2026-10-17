"""Registry identity comes from the bulk CSV before any network work, so a deadline cannot remove it."""
import asyncio

from tests.test_hybrid_registry import bulk_file
from tests.test_registry import config, execute, handler, numbers

COMPANIES = 20


def identity_ids(row):
    return {c['id'] for c in row['claims'] if c['family'] == 'identity' and c['availability'] == 'available'}


def deadline_run(tmp_path, orgs, csv_orgs):
    async def slow(request):
        await asyncio.sleep(1)  # Every live registry call outlasts the remaining budget.
        return handler()(request)
    cfg = config(tmp_path / 'deadline', orgs, bulk=bulk_file(tmp_path, csv_orgs), workers=1, time_budget_seconds=4)
    return execute(cfg, slow)


def test_csv_identity_survives_a_deadline_for_every_company(tmp_path):
    orgs = numbers(COMPANIES + 1)
    csv_orgs, live_only = orgs[:COMPANIES], orgs[COMPANIES]
    reference_cfg = config(tmp_path / 'reference', orgs, bulk=bulk_file(tmp_path, csv_orgs))
    _, reference = execute(reference_cfg)
    report, rows = deadline_run(tmp_path, orgs, csv_orgs)
    assert [r['organisation_number'] for r in rows] == orgs
    assert report['deadline_hits'] > 0  # The deadline really cut work short.
    expected = {r['organisation_number']: identity_ids(r) for r in reference}
    for row in rows:
        org = row['organisation_number']
        if org in csv_orgs:
            assert row['run']['sections']['identity'] == 'available', org
            assert identity_ids(row) == expected[org] and expected[org], org
    # Only the company missing from the CSV may lose identity to the deadline.
    live = next(r for r in rows if r['organisation_number'] == live_only)
    assert live['run']['sections']['identity'] in {'available', 'failed'}
