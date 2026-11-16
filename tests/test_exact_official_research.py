"""S3 bundled Research Council / SkatteFUNN projects: exact project-owner orgnr only."""
import hashlib
import json
from datetime import datetime, timezone

import pytest

from signalpost.sources import exact_official as eo

ORG = '923609016'
NOW = datetime(2026, 11, 16, tzinfo=timezone.utc)
RCN = {'source': 'rcn', 'row': 7, 'fields': {
    'prosjektnummer': '334455', 'prosjekttittel': 'Hydrogen storage pilot', 'prosjektfase': 'Bevilgning',
    'prosjektstart': '2025', 'prosjektslutt': '2028', 'prosjektansvarlig_type': 'Organisasjon',
    'prosjektansvarlig_navn': 'EXAMPLE AS', 'organisasjonsnummer': ORG, 'aktivitet': 'ENERGIX',
    'virkemiddel': 'Innovasjonsprosjekt', 'tildelt_belop': '12500000.0'}}
SF_NEW = {'source': 'skattefunn_2024_2026', 'row': 3, 'fields': {
    'Søknadsnummer': '10', 'Prosjektnummer': '25', 'Prosjektansvarlig': 'EXAMPLE AS', 'Prosjekttittel': 'Sensor platform',
    'Organisasjonsnr': ORG, 'Godkjent': 'JA', 'Fra-år': '45292', 'Til-år': '46387', 'Vedtaksdato': '45534'}}
SF_OLD = {'source': 'skattefunn_2002_2024', 'row': 9, 'fields': {
    'Prosjektnummer': '356338', 'Bedriftsnavn': 'EXAMPLE AS', 'Prosjekttittel': 'Quick change', 'Organisasjonsnummer': ORG,
    'Søknad godkjent': 'JA', 'Søknad avslått': 'NEI', 'Prosjektets fra-år': '2024', 'Prosjektets til-år': '2027',
    'Vedtaksdato': '45597.634224537003'}}


def with_fields(record, **changes):
    return {**record, 'fields': {**record['fields'], **changes}}


def test_rcn_project_values_are_copied_with_year_precision_and_no_unit_invention():
    value, paths = eo.research_value(RCN, ORG, NOW)
    assert value['date'] == '2025' and value['date_precision'] == 'year' and value['phase'] == 'granted'
    assert value['programme'] == 'ENERGIX' and value['amount'] == 12500000.0
    assert 'currency' not in value and 'unit not stated' in value['amount_note']
    assert '/fields/organisasjonsnummer' in paths and '/fields/tildelt_belop' in paths


def test_skattefunn_decision_date_is_decoded_from_the_published_serial():
    value, _ = eo.research_value(SF_NEW, ORG, NOW)
    assert value['date'] == '2024-08-30' and value['date_precision'] == 'day' and value['decision_date_serial'] == '45534'
    old, _ = eo.research_value(SF_OLD, ORG, NOW)
    assert old['date'] == '2024-11-01' and old['project_id'] == '356338'
    assert 'amount' not in value and 'amount' not in old  # SkatteFUNN lists publish no amount


@pytest.mark.parametrize('record', [
    with_fields(RCN, organisasjonsnummer='974760673'),
    with_fields(RCN, prosjektfase='Avslag'),
    with_fields(RCN, prosjektfase='Vurderes'),
    with_fields(RCN, prosjektansvarlig_type='Person'),
    with_fields(RCN, prosjektslutt='2021'),                 # ended before the 36-month window
    with_fields(RCN, prosjektstart='2027'),                 # not started
    with_fields(SF_NEW, Godkjent='NEI'),
    with_fields(SF_NEW, Godkjent=None),                     # pending
    with_fields(SF_NEW, Vedtaksdato='not-a-serial'),
    with_fields(SF_OLD, **{'Søknad godkjent': 'NEI', 'Søknad avslått': 'JA'}),
    with_fields(SF_OLD, Vedtaksdato='43000'),               # 2017 decision, outside window
    {'source': 'unknown', 'fields': {}},
])
def test_non_owner_rejected_pending_or_out_of_window_projects_abstain(record):
    assert eo.research_value(record, ORG, NOW) is None


def test_no_amount_when_not_given_for_the_project():
    value, paths = eo.research_value(with_fields(RCN, tildelt_belop=''), ORG, NOW)
    assert 'amount' not in value and '/fields/tildelt_belop' not in paths


class Blobs:
    def __init__(self):
        self.saved = {}

    def put(self, raw):
        sha = hashlib.sha256(raw).hexdigest()
        self.saved[sha] = raw
        return sha


def fake_bundle(records):
    texts = [json.dumps(r, ensure_ascii=False, sort_keys=True, separators=(',', ':')) for r in records]
    sources = [{'key': k, 'source_url': f'https://example.test/{k}.csv', 'retrieved_at': '2026-11-16T11:11:51Z'}
               for k in ('rcn', 'skattefunn_2024_2026', 'skattefunn_2002_2024')]
    return {'schema': 1, 'sources': sources, 'records': {ORG: texts}}


def test_record_section_uses_exact_bundled_bytes_as_evidence_and_dedupes(monkeypatch):
    bundle = fake_bundle([RCN, RCN, SF_NEW])
    blobs = Blobs()
    section = eo.record_section('research', 'research.project.', bundle, ORG, NOW, eo.research_value, blobs, 'official_research', 'project_id')
    assert sorted(c.field for c in section.claims) == ['research.project.rcn.334455', 'research.project.skattefunn_2024_2026.25']
    bodies = {e.content_sha256 for e in section.evidence}
    assert all(blobs.saved[sha].decode() in bundle['records'][ORG] for sha in bodies)
    span = next(e.claim_span for e in section.evidence if e.locator == '/fields/organisasjonsnummer')
    assert ORG in span
    empty = eo.record_section('research', 'research.project.', fake_bundle([]), ORG, NOW, eo.research_value, blobs, 'official_research', 'project_id')
    assert empty.state == 'not_available' and not empty.claims


def test_verifier_requires_the_exact_bundled_record(monkeypatch):
    from scripts import verify_output
    bundle = fake_bundle([RCN])
    monkeypatch.setattr(eo, 'load_bundle', lambda path: bundle)
    blobs = Blobs()
    section = eo.record_section('research', 'research.project.', bundle, ORG, NOW, eo.research_value, blobs, 'official_research', 'project_id')
    claims = [c.model_dump(mode='json') for c in section.claims]
    evidence = {e.id: e.model_dump(mode='json') for e in section.evidence}
    row = {'organisation_number': ORG, 'run': {'completed_at': '2026-11-16T12:00:00Z'}}
    stored = lambda sha: blobs.saved[sha].decode()
    assert verify_output.verify_exact_official(row, {'claims': claims}, evidence, stored) == 1
    forged = {sha: raw.replace(b'Hydrogen', b'Helium') for sha, raw in blobs.saved.items()}
    with pytest.raises(AssertionError):  # a body not present in the bundle is rejected
        verify_output.verify_exact_official(row, {'claims': claims}, evidence, lambda sha: forged[sha].decode())
    claims[0]['value']['title'] = 'Something else'
    with pytest.raises(AssertionError):
        verify_output.verify_exact_official(row, {'claims': claims}, evidence, stored)


def test_shipped_bundle_is_bounded_and_records_belong_to_their_org():
    bundle = eo.load_bundle(eo.RESEARCH_BUNDLE)
    assert {s['key'] for s in bundle['sources']} == {'rcn', 'skattefunn_2024_2026', 'skattefunn_2002_2024'}
    assert all(s['retrieved_at'].endswith('Z') and len(s['sha256']) == 64 for s in bundle['sources'])
    for org, texts in list(bundle['records'].items())[:300]:
        for text in texts:
            f = json.loads(text)['fields']
            assert org in (f.get('organisasjonsnummer'), f.get('Organisasjonsnr'), f.get('Organisasjonsnummer'))
            assert 'prosjektleder' not in f and 'Populærvitenskapelig sammendrag' not in f  # no personal/free-text fields
