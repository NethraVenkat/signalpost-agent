import asyncio
import copy
import csv
import gzip
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from signalpost.sources import exact_official as eo, state_aid_bulk as bulk
from signalpost.sources.blobstore import BlobStore
from scripts.build_state_aid_snapshot import build
from scripts.verify_output import verify_exact_official

FIXTURE = Path(__file__).parent / 'fixtures/r5_gaps/state-aid-records.json'
NOW = datetime(2026, 11, 19, tzinfo=timezone.utc)
RETRIEVED = '2026-11-19T15:51:59.277685Z'


def records():
    return json.loads(FIXTURE.read_text(encoding='utf8'))


def fixture_csv(tmp_path):
    path = tmp_path / 'official-extract.csv'
    with path.open('w', encoding='utf-16-le', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=bulk.COLUMNS, delimiter=';')
        writer.writeheader()
        writer.writerows(r['fields'] for r in records())
    return path


def test_saved_real_exact_and_interval_awards_have_exact_registered_recipient():
    values = []
    for record in records():
        org = record['fields']['Organisasjonsnummer støttemottaker']
        value, pointers = bulk.derive(record, org, NOW)
        values.append(value)
        assert value['company_orgnr'] == org and value['award_id'] == record['fields']['Støttetiltaksnummer']
        assert value['granting_authority'] == record['fields']['Navn støttegiver']
        assert '/fields/Organisasjonsnummer støttemottaker' in pointers
        assert bulk.derive(record, '923609016', NOW) is None
    assert values[0]['amount'] == 1406546 and values[0]['currency'] == 'NOK'
    assert values[0]['specified_recipient_orgnr'] == '972345954'
    assert any('amount_range' in v and 'amount' not in v for v in values)


@pytest.mark.parametrize('field,value', [
    ('Status', 'Slettet'), ('Støttetiltakstype', 'Støtteordning'),
    ('Organisasjonsnummer støttemottaker', '989649605'),
    ('Organisasjonsnummer støttegiver', 'unknown'), ('Navn støttegiver', None),
    ('Tildelingsdato', '31.12.2027'), ('Tildelingsdato', '01.01.2020'),
    ('Støttetiltaksnummer', None), ('Organisasjonsnummer spesifisert støttemottaker', 'unproven'),
])
def test_bad_or_unattributable_real_response_mutations_abstain(field, value):
    record = copy.deepcopy(records()[0])
    org = record['fields']['Organisasjonsnummer støttemottaker']
    record['fields'][field] = value
    assert bulk.derive(record, org, NOW) is None


@pytest.mark.parametrize('value', ['1 000,00', '-1', 'NaN', 'Infinity', '', None, '1.000,00'])
def test_amount_does_not_guess_separators_or_nonfinite_values(value):
    assert bulk.amount(value) is None


def test_builder_is_deterministic_and_keeps_only_nonpersonal_columns(tmp_path):
    source = fixture_csv(tmp_path)
    one, two = tmp_path / 'one.gz', tmp_path / 'two.gz'
    first = build(source, one, RETRIEVED, '2026-11-19')
    second = build(source, two, RETRIEVED, '2026-11-19')
    assert one.read_bytes() == two.read_bytes()
    assert first['records'] == second['records'] == 3
    assert first['source']['sha256'] == hashlib.sha256(source.read_bytes()).hexdigest()
    data = json.loads(gzip.decompress(one.read_bytes()))
    assert not any('Fødselsdato' in k or k == 'Navn støttemottaker' for k in bulk.COLUMNS)
    assert data['sources'][0]['source_url'] == bulk.URL


def test_registered_range_briefing_retains_its_source_currency():
    record = next(r for r in records() if r['fields']['Beløpsintervall fra beløp'])
    org = record['fields']['Organisasjonsnummer støttemottaker']
    value, _ = bulk.derive(record, org, NOW)
    claim = SimpleNamespace(field='state_aid.award.' + value['award_id'], value=value, id='award',
                            availability='available', carried_forward=False)
    [sentence] = eo.briefing_sentences(SimpleNamespace(claims=[claim]))
    assert f" {value['currency']} (registered range)" in sentence.text


def test_bulk_runtime_makes_no_api_request_and_all_receipts_reverify(tmp_path, monkeypatch):
    source = fixture_csv(tmp_path)
    bundle = tmp_path / 'state-aid.gz'
    build(source, bundle, RETRIEVED, '2026-11-19')
    monkeypatch.setattr(bulk, 'BUNDLE', bundle)
    class FrozenDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return NOW
    monkeypatch.setattr(eo, 'datetime', FrozenDateTime)
    blobs = BlobStore(tmp_path / 'state')
    org = records()[0]['fields']['Organisasjonsnummer støttemottaker']
    envelopes = {org: SimpleNamespace(run=SimpleNamespace(sections={'identity': 'available'}), claims=[])}
    sections = []
    cfg = SimpleNamespace(state_aid=True, research=False, licences=False, inspections=False)
    class NoNetwork:
        async def request(self, *args, **kwargs):
            pytest.fail('Bundled state aid must never request the blocked API')
    asyncio.run(eo.enrich(envelopes, NoNetwork(), cfg, None, blobs, lambda e, f, s: sections.append((f, s))))
    assert len(sections) == 1 and sections[0][0] == 'state_aid'
    section = sections[0][1]
    assert section.state == 'available' and len(section.claims) == 1
    data = {'claims': [c.model_dump() for c in section.claims]}
    evidence = {e.id: e.model_dump() for e in section.evidence}
    row = {'organisation_number': org, 'completed_at': '2026-11-19T23:59:59Z'}
    body = lambda sha: blobs.read(sha).decode('utf8')
    assert verify_exact_official(row, data, evidence, body) == 1
    data['claims'][0]['value']['amount'] += 1
    with pytest.raises(AssertionError, match='Unsupported'):
        verify_exact_official(row, data, evidence, body)
