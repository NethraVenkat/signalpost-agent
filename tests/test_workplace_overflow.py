import gzip
import hashlib
import json
from pathlib import Path

from signalpost import site

FIXTURE = Path(__file__).parent / 'fixtures/r5_gaps/workplaces-968360302.json.gz'


def saved_company():
    return json.loads(gzip.decompress(FIXTURE.read_bytes()))


def test_saved_968360302_defers_workplaces_without_losing_facts_or_receipts(tmp_path):
    row = saved_company()
    meta = json.loads(FIXTURE.with_suffix('.source.json').read_text())
    assert hashlib.sha256(FIXTURE.read_bytes()).hexdigest() == meta['fixture_sha256']
    assert meta['original_rendered_html_bytes'] == 262692 and meta['workplaces'] == 42
    assert hashlib.sha256(json.dumps(row['claims'], sort_keys=True, ensure_ascii=False).encode()).hexdigest() == meta['claims_sha256']
    source = tmp_path / 'saved.jsonl'
    source.write_text(json.dumps(row, ensure_ascii=False) + '\n', encoding='utf8')
    before = source.read_bytes()
    result = site.generate_site(source, tmp_path / 'site')
    assert result['companies'] == 1 and result['largest_profile_bytes'] < 250000
    assert source.read_bytes() == before
    payload_text = (tmp_path / 'site/c/968360302.data.js').read_text(encoding='utf8')
    payload = json.loads(payload_text.split(' = ', 1)[1].rstrip(';\n'))
    facts = {c['id']: c for c in payload['facts']}
    expected = [c for c in row['claims'] if c['evidence_ids'] or c['availability'] == 'available']
    assert set(facts) == {c['id'][:16] for c in expected}
    refs = {ref for c in expected for ref in c['evidence_ids']}
    id_column = 1 + payload['evidence_fields'].index('id')
    assert {e[id_column] for e in payload['records']} == refs
    workplaces = [c for c in row['claims'] if c['field'].startswith('subunits.unit.')]
    deferred = [c for c in payload['registry_details'] if c['field'].startswith('subunits.unit.')]
    assert len(deferred) >= len(workplaces) - site.WORKPLACE_INLINE
    by_id = {c['id'][:16]: c for c in workplaces}
    for detail in deferred:
        original = by_id[detail['id']]
        assert detail['group'] == 'locations' and detail['value'] == original['value']
        assert facts[detail['id']]['evidence_ids'] == original['evidence_ids']


def test_zero_inline_workplaces_keeps_every_workplace_in_local_data():
    row = saved_company()
    payload = site.company_payload(row, workplace_inline=0)
    workplaces = [c for c in row['claims'] if c['field'].startswith('subunits.unit.')]
    deferred = [c for c in payload['registry_details'] if c['field'].startswith('subunits.unit.')]
    assert len(deferred) == len(workplaces) == 42
    assert all(c['id'] in site.deferred_claims(row['claims'], workplace_inline=0) for c in workplaces)
