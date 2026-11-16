"""S5 Mattilsynet Smilefjes: inspections at our orgnr or a registry-proven subunit only."""
import hashlib
import json
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from signalpost.sources import exact_official as eo

ORG = '923609016'
UNIT = '974760673'
OTHER = '981405099'
NOW = datetime(2026, 11, 16, tzinfo=timezone.utc)


def rec(org, tilsynid='T1', dato='05012026', grade='1', row=1):
    return {'source': 'smilefjes', 'row': row, 'fields': {
        'tilsynsobjektid': 'Z1', 'orgnummer': org, 'navn': 'Kantina', 'postnr': '0162', 'poststed': 'Oslo', 'tilsynid': tilsynid,
        'status': '0', 'dato': dato, 'total_karakter': grade, 'tilsynsbesoektype': '0'}}


def text(r):
    return json.dumps(r, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def test_direct_inspection_with_published_grade_meaning():
    value, paths = eo.inspection_value(rec(ORG), ORG, NOW)
    assert value['date'] == '2026-01-05' and value['matched_as'] == 'company' and value['grade'] == 1
    assert value['result'] == 'Minor breaches not requiring follow-up (big smile)' and value['visit_type_code'] == '0'
    assert '/fields/orgnummer' in paths and '/fields/total_karakter' in paths


@pytest.mark.parametrize('record,units', [
    (rec(OTHER), {}),                      # someone else's workplace
    (rec(UNIT), {}),                       # a subunit that the registry did not prove
    (rec(ORG, dato='31022026'), {}),       # impossible date
    (rec(ORG, dato='2026-01-05'), {}),     # unexpected format
    (rec(ORG, dato='01012021'), {}),       # outside the 36-month window
    (rec(ORG, grade='5'), {}),             # outside the published 0-3 scale
    (rec(ORG, tilsynid=''), {}),
])
def test_unattributed_or_malformed_inspections_abstain(record, units):
    assert eo.inspection_value(record, ORG, NOW, units) is None


class Blobs:
    def __init__(self):
        self.saved = {}

    def put(self, raw):
        sha = hashlib.sha256(raw).hexdigest()
        self.saved[sha] = raw
        return sha


def envelope_with_unit():
    unit = SimpleNamespace(field='subunits.unit.' + UNIT, availability='available', carried_forward=False,
                           value={'organisation_number': UNIT, 'name': 'Kantina'}, evidence_ids=['unit-evidence'])
    return SimpleNamespace(claims=[unit])


def bundle(records):
    out = {}
    for r in records:
        out.setdefault(r['fields']['orgnummer'], []).append(text(r))
    return {'schema': 1, 'sources': [{'key': 'smilefjes', 'source_url': 'https://smilefjes.mattilsynet.no/api/tilsyn.csv',
                                      'retrieved_at': '2026-11-16T11:01:01Z'}], 'records': out}


def test_subunit_inspection_cites_the_registry_subunit_evidence(monkeypatch):
    data = bundle([rec(ORG, 'T1'), rec(UNIT, 'T2', grade='2'), rec(OTHER, 'T3')])
    monkeypatch.setattr(eo, 'load_bundle', lambda path: data)
    section = eo.inspections_section(ORG, envelope_with_unit(), NOW, Blobs())
    by_field = {c.field: c for c in section.claims}
    assert sorted(by_field) == ['inspections.inspection.smilefjes.T1', 'inspections.inspection.smilefjes.T2']
    sub = by_field['inspections.inspection.smilefjes.T2']
    assert sub.value['matched_as'] == 'registered_subunit' and sub.value['workplace_orgnr'] == UNIT
    assert 'unit-evidence' in sub.evidence_ids
    assert 'unit-evidence' not in by_field['inspections.inspection.smilefjes.T1'].evidence_ids


def test_none_found_is_explicit(monkeypatch):
    monkeypatch.setattr(eo, 'load_bundle', lambda path: bundle([rec(OTHER)]))
    section = eo.inspections_section(ORG, SimpleNamespace(claims=[]), NOW, Blobs())
    assert section.state == 'not_available' and not section.claims


def test_shipped_bundle_keeps_only_listed_columns():
    data = eo.load_bundle(eo.INSPECTIONS_BUNDLE)
    assert [s['key'] for s in data['sources']] == ['smilefjes'] and data['sources'][0]['retrieved_at'].endswith('Z')
    for org, texts in list(data['records'].items())[:300]:
        for t in texts:
            f = json.loads(t)['fields']
            assert f['orgnummer'] == org and set(f) == set(eo.INSPECTION_COLUMNS)


def test_verifier_checks_subunit_parent_proof_and_exact_bundled_record(monkeypatch):
    from scripts.verify_output import verify_exact_official
    data = bundle([rec(UNIT, 'T2', grade='2')])
    monkeypatch.setattr(eo, 'load_bundle', lambda path: data)
    blobs = Blobs()
    section = eo.inspections_section(ORG, envelope_with_unit(), NOW, blobs)
    sub_url = 'https://data.brreg.no/enhetsregisteret/api/underenheter?overordnetEnhet=' + ORG
    def registry(parent):
        return json.dumps({'_embedded': {'underenheter': [{'organisasjonsnummer': UNIT, 'overordnetEnhet': parent}]}})
    def run(parent=ORG, cite_unit=True, value_change=None):
        claims = [c.model_dump(mode='json') for c in section.claims]
        if not cite_unit:
            claims[0]['evidence_ids'] = [e for e in claims[0]['evidence_ids'] if e != 'unit-evidence']
        if value_change:
            claims[0]['value'].update(value_change)
        claims.append({'field': 'subunits.unit.' + UNIT, 'availability': 'available', 'family': 'subunits',
                       'value': {'organisation_number': UNIT}, 'evidence_ids': ['unit-evidence']})
        evidence = {e.id: e.model_dump(mode='json') for e in section.evidence}
        evidence['unit-evidence'] = {'source_url': sub_url, 'locator': '/_embedded/underenheter/0', 'content_sha256': 'u' * 64,
                                     'extraction_method': 'signalpost.registry.v1'}
        bodies = {**{k: v.decode() for k, v in blobs.saved.items()}, 'u' * 64: registry(parent)}
        row = {'organisation_number': ORG, 'run': {'completed_at': '2026-11-16T12:00:00Z'}}
        return verify_exact_official(row, {'claims': claims}, evidence, lambda sha: bodies[sha])
    assert run() == 1
    with pytest.raises(AssertionError):
        run(parent=OTHER)                 # the registry does not make it our subunit
    with pytest.raises(AssertionError):
        run(cite_unit=False)              # the parent-link dependency must be cited
    with pytest.raises(AssertionError):
        run(value_change={'grade': 0})    # value must re-derive from the bundled record
