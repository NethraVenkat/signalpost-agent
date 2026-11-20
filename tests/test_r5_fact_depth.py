import json

import pytest

from signalpost.sources import brreg_enhet, brreg_underenheter, bulk_registry
from signalpost.sources.extract import Section, Source
from signalpost.sources.registry_fields import ADDITIONAL, SUBUNIT_ADDITIONAL
from signalpost.models.evidence import utc_now
from signalpost.budget import SourceFailure
from signalpost.site import fact
from tests.test_registry_coverage import response
from tests.test_nav import ORG, SUB

# One explicit fixture value for every newly retained source field.
VALUES = {
    'slettedato': '2025-01-02', 'tvangsavvikletPgaManglendeSlettingDato': '2025-01-03',
    'registreringsnummerIHjemlandet': '00001234', 'utenlandskRegisterNavn': 'Reported register',
    'utenlandskRegisterAdresse': {'land': 'Danmark', 'poststed': 'Reported city'},
    'underlagtLovgivningLand': 'Danmark', 'underlagtLovgivningLandKode': 'DK',
    'foretaksformIHjemlandet': {'kode': 'AB', 'beskrivelse': 'Reported form'},
    'frivilligMvaRegistrertBeskrivelser': ['Utleier av bygg eller anlegg'],
    'historiskeNavn': [{'navn': 'Previous AS', 'fraDato': '2020-01-01 00:00:00', 'tilDato': '2021-01-01 00:00:00'}],
    'paategninger': [{'infotype': 'NAVN', 'tekst': 'Reported annotation', 'innfoertDato': '2025-01-01'}],
    'beliggenhetsadresse': {'adresse': ['Reported road 1'], 'landkode': 'NO'},
    'naeringskode1': {'kode': '62.100', 'beskrivelse': 'Reported primary'},
    'naeringskode2': {'kode': '63.100', 'beskrivelse': 'Reported secondary'},
    'naeringskode3': {'kode': '64.100', 'beskrivelse': 'Reported tertiary'},
    'antallAnsatte': 0, 'nedleggelsesdato': '2025-02-01',
    'registreringsdatoMerverdiavgiftsregisteret': '2024-01-01',
    'registreringsdatoMerverdiavgiftsregisteretEnhetsregisteret': '2024-01-02',
    'registreringsdatoFrivilligMerverdiavgiftsregisteret': '2024-01-03',
}
CASES = [('identity', name, path, kind) for name, (path, kind) in ADDITIONAL.items()] + [
         ('subunits', name, path, kind) for name, (path, kind) in SUBUNIT_ADDITIONAL.items()]


def extract(tmp_path, family, fields):
    if family == 'identity':
        result, _ = response(tmp_path, {'organisasjonsnummer': ORG, 'navn': 'Example AS', **fields})
        return brreg_enhet.extract_response(ORG, result)
    result, _ = response(tmp_path, {'_embedded': {'underenheter': [
        {'organisasjonsnummer': SUB, 'overordnetEnhet': ORG, **fields}]}})
    section = Section()
    brreg_underenheter.extract_page(ORG, result, section, 0)
    return section


@pytest.mark.parametrize('family,name,path,kind', CASES)
@pytest.mark.parametrize('mode', ['reported', 'absent', 'null', 'odd'])
def test_each_new_field_has_provenance_or_explicit_abstention(tmp_path, family, name, path, kind, mode):
    # Employee count's existing core record rejects malformed data as a source
    # failure; all new optional fields isolate malformed values locally.
    if mode == 'odd' and kind == 'employees':
        with pytest.raises(ValueError): extract(tmp_path, family, {path: True})
        return
    value = VALUES[path] if mode == 'reported' else None if mode == 'null' else True
    section = extract(tmp_path, family, {} if mode == 'absent' else {path: value})
    field = 'identity.'+name if family == 'identity' else f'subunits.detail.{SUB}.{name}'
    claim = next((c for c in section.claims if c.field == field), None)
    if mode == 'absent':
        assert claim is None
        return
    assert claim is not None
    if mode == 'reported': assert claim.value == VALUES[path] and claim.availability == 'available'
    else: assert claim.value is None and claim.availability in {'not_available', 'failed'}
    evidence = next(e for e in section.evidence if e.id in claim.evidence_ids)
    assert evidence.locator.endswith('/'+path)
    assert evidence.retrieved_at.endswith('Z') and len(evidence.content_sha256) == 64
    assert evidence.source_url and evidence.extraction_method == 'signalpost.registry_fields.v2'
    assert len(evidence.claim_span) <= 300


@pytest.mark.parametrize('name,spec', ADDITIONAL.items())
def test_csv_fields_match_json_and_preserve_leading_zero(tmp_path, name, spec):
    path, kind = spec
    if kind == 'object':
        row = {'organisasjonsnummer': ORG, 'navn': 'Example AS', **{path+'.'+k: str(v) for k,v in VALUES[path].items()}}
    else:
        value = VALUES[path]
        row = {'organisasjonsnummer': ORG, 'navn': 'Example AS', path: json.dumps(value) if isinstance(value,list) else value}
    body = json.dumps(row).encode()
    import hashlib
    source = Source('https://data.brreg.no/enhetsregisteret/api/enheter/lastned/csv', body, hashlib.sha256(body).hexdigest(), utc_now())
    section = bulk_registry.extract(ORG, row, source)
    claim = next(c for c in section.claims if c.field == 'identity.'+name)
    assert claim.value == VALUES[path]
    assert claim.availability == 'available' and claim.evidence_ids


def test_organisation_number_is_a_claim_with_exact_csv_evidence(tmp_path):
    import hashlib
    row={'organisasjonsnummer':ORG,'navn':'Example AS'}
    body=json.dumps(row).encode()
    source=Source('https://data.brreg.no/enhetsregisteret/api/enheter/lastned/csv',body,
        hashlib.sha256(body).hexdigest(),utc_now())
    section=bulk_registry.extract(ORG,row,source)
    claim=next(c for c in section.claims if c.field=='identity.organisation_number')
    evidence=next(e for e in section.evidence if e.id in claim.evidence_ids)
    assert claim.value==ORG
    assert evidence.locator==f'row:{ORG}/column:organisasjonsnummer'
    assert ORG in evidence.claim_span


def test_wrong_csv_organisation_number_is_rejected(tmp_path):
    import hashlib
    row={'organisasjonsnummer':SUB,'navn':'Example AS'}
    body=json.dumps(row).encode()
    source=Source('https://data.brreg.no/enhetsregisteret/api/enheter/lastned/csv',body,
        hashlib.sha256(body).hexdigest(),utc_now())
    with pytest.raises(SourceFailure):
        bulk_registry.extract(ORG,row,source)


def test_subunit_addresses_are_distinct_and_no_nace_fallback(tmp_path):
    section = extract(tmp_path, 'subunits', {'beliggenhetsadresse': {'poststed': 'Physical'},
        'postadresse': {'poststed': 'Postal'}, 'naeringskode1': VALUES['naeringskode1'],
        'antallAnsatte': 0, 'harRegistrertAntallAnsatte': False})
    claims = {c.field.rsplit('.',1)[-1]: c for c in section.claims if c.field.startswith('subunits.detail.')}
    assert claims['physical_address'].value != claims['postal_address'].value
    assert 'nace2' not in claims and 'nace3' not in claims
    assert claims['employees'].value is None
    assert 'physical address' in fact(claims['physical_address'].model_dump(), {})


def test_refresh_new_fields_are_observations():
    from signalpost.refresh.diff import newly_supported_field
    assert all(newly_supported_field('identity.'+name) for name in ADDITIONAL)


@pytest.mark.parametrize('reported,expected', [(False, None), ('false', None), (True, 0), (None, 0)])
def test_employee_zero_requires_reported_count_not_false_flag(tmp_path, reported, expected):
    section = extract(tmp_path, 'identity', {'antallAnsatte': 0, 'harRegistrertAntallAnsatte': reported})
    assert next(c for c in section.claims if c.field=='identity.employees').value == expected


def test_subunit_parent_orgnr_is_its_own_exact_evidenced_claim(tmp_path):
    r,_=response(tmp_path,{'_embedded':{'underenheter':[{'organisasjonsnummer':SUB,
        'navn':'Example unit','overordnetEnhet':ORG}]}})
    s=Section();brreg_underenheter.extract_page(ORG,r,s,0)
    claim=next(c for c in s.claims if c.field==f'subunits.detail.{SUB}.parent_organisation_number')
    assert claim.value==ORG and claim.availability=='available'
    evidence=next(e for e in s.evidence if e.id in claim.evidence_ids)
    assert evidence.locator=='/_embedded/underenheter/0/overordnetEnhet'
    assert evidence.claim_span and ORG in evidence.claim_span
    assert evidence.source_url==r.url and evidence.content_sha256==r.sha
    assert evidence.retrieved_at.endswith('Z')


@pytest.mark.parametrize('parent',[None,SUB])
def test_subunit_parent_orgnr_missing_or_mismatched_abstains(tmp_path,parent):
    r,_=response(tmp_path,{'_embedded':{'underenheter':[{'organisasjonsnummer':SUB,
        'navn':'Example unit','overordnetEnhet':parent}]}})
    s=Section()
    with pytest.raises(SourceFailure):
        brreg_underenheter.extract_page(ORG,r,s,0)
    assert not any(c.field.endswith('.parent_organisation_number') for c in s.claims)


def test_undocumented_sector_code_is_kept_raw_without_inferred_meaning(tmp_path):
    r,_=response(tmp_path,{'organisasjonsnummer':ORG,'navn':'Example AS',
        'institusjonellSektorkode':{'kode':'X999'}})
    s=brreg_enhet.extract_response(ORG,r)
    claim=next(c for c in s.claims if c.field=='identity.institutional_sector')
    assert claim.value=={'kode':'X999'}
    evidence=next(e for e in s.evidence if e.id in claim.evidence_ids)
    assert 'X999' in evidence.claim_span
    assert 'beskrivelse' not in claim.value
