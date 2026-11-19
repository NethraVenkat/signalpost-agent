import copy
import hashlib
import json
from pathlib import Path

import httpx
import pytest

from signalpost.sources import regnskap
from signalpost.sources.http import Response
from scripts.verify_output import verify
from scripts.accuracy_audit import audit_accounts_claim
from tests.test_registry import config, execute, handler

ORG = '991835423'
FIXTURE = Path(__file__).parent / 'fixtures/r5_gaps/accounts-991835423.json'


def response(data=None):
    body = FIXTURE.read_bytes() if data is None else json.dumps(data).encode()
    return Response(body, 200, regnskap.URL + ORG, '2026-11-19T00:00:00Z', hashlib.sha256(body).hexdigest())


def test_real_response_keeps_entity_and_consolidated_filings_separate():
    meta = json.loads(FIXTURE.with_suffix('.source.json').read_text())
    assert hashlib.sha256(FIXTURE.read_bytes()).hexdigest() == meta['content_sha256']
    r = response()
    section = regnskap.extract(ORG, r, None)
    groups = [c for c in section.claims if c.field.startswith('accounts.consolidated.') and c.availability == 'available']
    assert {c.reporting_period['filing_id'] for c in groups} == {6290461, 7105229}
    assert all(c.reporting_period['account_type'] == 'KONSERN' for c in groups)
    assert next(c for c in section.claims if c.field == 'accounts.revenue').reporting_period['account_type'] == 'SELSKAP'
    evidence = {e.id: e for e in section.evidence}
    for c in groups:
        e = evidence[c.evidence_ids[0]]
        assert e.claim_span in r.body.decode()
        assert audit_accounts_claim(ORG, c.model_dump(), e.model_dump(), r.body.decode())[0] == 'CORRECT'
    from signalpost.site import fact
    html = fact(groups[0].model_dump(), {})
    assert 'Consolidated group' in html and 'filing ID:' in html


@pytest.mark.parametrize('mutation', ['owner', 'period', 'filing', 'amount'])
def test_bad_group_filing_does_not_remove_entity_values(mutation):
    data = json.loads(FIXTURE.read_bytes())
    for row in data:
        if row['regnskapstype'] != 'KONSERN':
            continue
        if mutation == 'owner': row['virksomhet']['organisasjonsnummer'] = '923609016'
        elif mutation == 'period': row['regnskapsperiode']['tilDato'] = 'bad'
        elif mutation == 'filing': row['id'] = None
        else: row['resultatregnskapResultat']['aarsresultat'] = True
    section = regnskap.extract(ORG, response(data), None)
    assert not any(c.field.startswith('accounts.consolidated.') for c in section.claims)
    assert any(c.field == 'accounts.revenue' and c.availability == 'available' for c in section.claims)
    assert any(e.code.startswith('consolidated_') for e in section.errors)


def test_real_consolidated_sources_verify_and_tampering_is_rejected(tmp_path):
    def serve(request):
        if str(request.url) == regnskap.URL + ORG:
            return httpx.Response(200, content=FIXTURE.read_bytes())
        return handler()(request)
    cfg = config(tmp_path, [ORG])
    _, rows = execute(cfg, serve)
    assert verify(cfg.output, cfg.state_dir, 1, cfg.organisations, cfg.report)['financial_inputs_verified'] > 0
    group = next(c for c in rows[0]['claims'] if c['field'].startswith('accounts.consolidated.') and c['availability'] == 'available')
    group['reporting_period']['filing_id'] = 1
    cfg.output.write_text(json.dumps(rows[0]) + '\n')
    with pytest.raises(AssertionError):
        verify(cfg.output, cfg.state_dir, 1, cfg.organisations, cfg.report)


def test_group_currency_and_year_never_label_entity_summary_and_details_keep_scope(tmp_path):
    def serve(request):
        if str(request.url) == regnskap.URL + ORG:
            data = json.loads(FIXTURE.read_bytes())
            for r in data:
                if r['regnskapstype'] == 'KONSERN':
                    r['valuta'] = 'USD'
                    r['enhet'] = 'thousands'
            return httpx.Response(200, json=data)
        return handler()(request)
    _, rows = execute(config(tmp_path, [ORG]), serve)
    from signalpost.site import index_record, company_payload, official_overflow
    record = index_record(rows[0])
    assert record['currency'] == 'NOK' and record['unit'] is None and record['fiscal_year'] == '2025'
    overflow = official_overflow(rows[0]['claims'], 0)
    groups = [c for c in rows[0]['claims'] if c['field'].startswith('accounts.consolidated.')]
    assert all(c['id'] in overflow for c in groups)
    details = company_payload(rows[0], official_inline=0)['registry_details']
    group_details = [c for c in details if c['field'].startswith('accounts.consolidated.')]
    assert len(group_details) == len(groups)
    assert all(c['group'] == 'financials' and c['reporting_period']['account_type'] == 'KONSERN'
               and c['reporting_period']['currency'] == 'USD' for c in group_details)
