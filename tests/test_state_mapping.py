"""A deadline marks unfinished sections budget_exhausted; only invalid input is a submission_error."""
import json

from tests.test_identity_first import deadline_run
from tests.test_registry import config, execute, numbers

COMPANIES = 20


def test_deadline_sections_are_failed_and_the_envelope_stays_complete(tmp_path):
    orgs = numbers(COMPANIES)
    _, rows = deadline_run(tmp_path, orgs, orgs)
    cut = [r for r in rows if any(e['code'] == 'deadline' for e in r['errors'])]
    assert cut, 'the deadline must have unfinished sections'
    for row in cut:
        assert row['state'] == 'complete', row['organisation_number']
        unfinished = [e['section'] for e in row['errors'] if e['code'] == 'deadline']
        for section in unfinished:
            assert row['run']['sections'][section] == 'failed'
            assert row['modules'][section]['state'] == 'budget_exhausted'
            # An honest, explicit claim for the section, never silently empty.
            assert any(c['family'] == section for c in row['claims'])
        expected = 'complete' if row['run']['sections']['identity'] == 'available' else 'budget_exhausted'
        assert row['modules']['identity']['state'] == expected


def test_invalid_input_remains_the_submission_error(tmp_path):
    _, rows = execute(config(tmp_path, ['923609016', 'bad']))
    by_org = {r['organisation_number']: r for r in rows}
    assert by_org['bad']['state'] == 'submission_error'
    assert all(m['state'] == 'submission_error' for m in by_org['bad']['modules'].values())
    assert by_org['923609016']['state'] == 'complete'


def test_state_contract_values_stay_in_the_closed_sets(tmp_path):
    allowed_availability = {'available', 'not_available', 'blocked', 'not_applicable', 'ambiguous', 'failed'}
    allowed_terminal = {'complete', 'not_applicable', 'not_found', 'blocked_policy', 'blocked_robots',
                        'source_error', 'budget_exhausted', 'submission_error'}
    _, rows = deadline_run(tmp_path, numbers(COMPANIES), numbers(COMPANIES))
    for row in rows:
        assert row['state'] in allowed_terminal
        assert {c['availability'] for c in row['claims']} <= allowed_availability
        assert {m['state'] for m in row['modules'].values()} <= allowed_terminal
        json.dumps(row)
