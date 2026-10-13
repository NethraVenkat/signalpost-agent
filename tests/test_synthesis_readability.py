import json
from pathlib import Path
import pytest
from signalpost.models.synthesis import Sentence
from signalpost.synthesis.nace import TABLE, english_title
from signalpost.synthesis.readability import money, unknown_text, nace_sentence
from signalpost.synthesis.template import generate
from signalpost.synthesis.validate import sentence_error
from tests.test_synthesis import envelope


def available(row, field, value, **extra):
    # Synthetic claims keep valid evidence links; IDs identify each test field.
    original = next(c for c in row.claims if c.field == 'identity.legal_name')
    claim = original.model_copy(deep=True)
    claim.field = field
    claim.id = __import__('hashlib').sha256(field.encode()).hexdigest()
    claim.value = value
    claim.family = field.split('.')[0]
    for key, val in extra.items():
        setattr(claim, key, val)
    row.claims = [c for c in row.claims if c.field != field] + [claim]
    return claim


def test_klass_saved_sources_and_all_subclass_parents():
    root = Path(__file__).parents[1] / 'src/signalpost/synthesis/data'
    for version in TABLE['versions']:
        raw = json.loads((root / f"ssb-{version['standard'].lower()}-en-2026-10-13.json").read_text(encoding='utf8'))
        assert raw['id'] == version['version_id']
        assert version['classes'] == {x['code']: x['name'] for x in raw['classificationItems'] if x['level'] == '4'}
        assert version['titles'] == {x['code']: x['name'] for x in raw['classificationItems'] if x['level'] in ('4','5')}
        assert {k: v['parent'] for k, v in version['subclasses'].items()} == {x['code']: x['parentCode'] for x in raw['classificationItems'] if x['level'] == '5'}
        assert all(v['parent'] in version['classes'] for v in version['subclasses'].values())
    newer, older = TABLE['versions']
    assert newer['classes']['46.64'] == 'Wholesale of other machinery and equipment'
    assert older['classes']['62.01'] == 'Computer programming activities'
    assert newer['subclasses']['69.201']['parent'] == '69.20'
    assert english_title({'kode': '46.640', 'beskrivelse': newer['subclasses']['46.640']['registered_title']}) == newer['titles']['46.640']
    assert english_title({'kode': '46.640', 'beskrivelse': older['subclasses']['46.640']['registered_title']}) == older['titles']['46.640']
    assert english_title({'kode': '46.640', 'beskrivelse': 'Unknown label'}) is None
    assert english_title({'kode': '99.999', 'beskrivelse': 'Unknown'}) is None


def test_headline_has_every_clause_cited_and_exact_amount(tmp_path):
    row, _ = envelope(tmp_path)
    staff = available(row, 'identity.employees', 55)
    revenue = available(row, 'accounts.revenue', 424327000, reporting_period={'currency': 'NOK', 'fiscal_year': '2025'})
    nace = next(c for c in row.claims if c.field == 'identity.nace1')
    nace.value = {'kode': '46.640', 'beskrivelse': 'Engroshandel med maskiner og utstyr ellers'}
    result = generate(row)
    opening = result.sections.what_it_does[0]
    assert opening.text == 'Example AS is based in Oslo and registered under Wholesale of other machinery and equipment (NACE 46.640), with 55 registered employees and NOK 424,327,000 in revenue in FY2025.'
    assert not sentence_error(opening.model_copy(update={'text': opening.text.replace('Oslo','OSLO')}),row)
    assert sentence_error(opening.model_copy(update={'text': opening.text.replace('Oslo','Bergen')}),row)
    assert set(opening.claim_ids) == {staff.id, revenue.id, nace.id, *(c.id for c in row.claims if c.field in {'identity.legal_name', 'identity.municipality'})}
    assert not sentence_error(opening, row)
    for key in opening.claim_ids:
        assert sentence_error(opening.model_copy(update={'claim_ids': [x for x in opening.claim_ids if x != key]}), row)
    for altered in ('424,327,001', '424 million', '424,327,000.0'):
        assert sentence_error(opening.model_copy(update={'text': opening.text.replace('424,327,000', altered)}), row)
    assert sentence_error(opening.model_copy(update={'text': opening.text.replace('FY2025', 'FY2024')}), row)
    assert result.checks.dropped_sentences == 0


@pytest.mark.parametrize('value,expected', [(424327000, '424,327,000'), (424327000.0, '424,327,000'), (-1200, '-1,200'), (1234.56, '1,234.56'), (0, '0')])
def test_exact_money(value, expected, tmp_path):
    assert money(value) == expected
    row, _ = envelope(tmp_path)
    claim = available(row, 'accounts.net_result', value, reporting_period={'currency': 'NOK', 'fiscal_year': '2025'})
    assert sentence_error(Sentence(text='Annual result: NOK ' + expected + ' (fiscal year 2025).', claim_ids=[claim.id]), row) is None
    assert sentence_error(Sentence(text='Annual result: NOK 2025 (fiscal year 2025).', claim_ids=[claim.id]), row)


def test_normalised_activity_and_dual_role_are_bound(tmp_path):
    row, _ = envelope(tmp_path)
    activity = available(row, 'identity.registered_activity', ['Develop  software.'])
    purpose = available(row, 'identity.statutory_purpose', 'Develop\nsoftware.')
    row.claims = [c for c in row.claims if c.family != 'roles']
    ceo = available(row, 'roles.role.ceo', {'name': 'Person One', 'role_type': {'kode': 'DAGL'}, 'inactive': False})
    chair = available(row, 'roles.role.chair', {'name': 'Person One', 'role_type': {'kode': 'LEDE'}, 'group_type': {'kode': 'STYR'}, 'inactive': False})
    result = generate(row)
    merged = next(s for s in result.sections.what_it_does if s.text.startswith('Registered activity and purpose'))
    assert merged.text == 'Registered activity and purpose: «Develop software.».'
    assert set(merged.claim_ids) == {activity.id, purpose.id}
    dual = next(s for s in result.sections.leadership if 'both CEO and chair' in s.text)
    assert dual.text == 'Person One is both CEO and chair.' and set(dual.claim_ids) == {ceo.id, chair.id}
    assert not any(s.record_type == 'board_members' for s in result.sections.leadership)
    assert sentence_error(dual.model_copy(update={'claim_ids': [ceo.id]}), row)
    assert sentence_error(merged.model_copy(update={'claim_ids': [activity.id]}), row)


def test_unknowns_preserve_reasons_and_unspecified_industry(tmp_path):
    row, _ = envelope(tmp_path)
    prior = generate(row)
    nace = next(c for c in row.claims if c.field == 'identity.nace1')
    nace.value = {'kode': '00.000', 'beskrivelse': 'Uoppgitt'}
    row.run.refresh['mode'] = 'refresh'
    current = generate(row)
    assert 'Uoppgitt' not in current.summary and 'NACE 00.000' not in current.summary
    assert current.sections.changes[0].text == 'No changes since the previous run.'
    assert any(u.text == 'Industry code not specified.' for u in current.sections.unknowns)
    for old in prior.sections.unknowns:
        new = next(u for u in current.sections.unknowns if (u.family, u.field) == (old.family, old.field))
        assert (new.state, new.reason) == (old.state, old.reason)
        assert new.text == unknown_text(new, row)


def test_single_duplicate_workplace_has_no_count(tmp_path):
    row, _ = envelope(tmp_path)
    row.run.sections['subunits'] = 'available'
    available(row, 'subunits.unit.one', {'name': 'Example AS', 'address': {'kommune': 'OSLO'}})
    result = generate(row)
    assert not any(s.record_type == 'workplaces' for s in result.sections.scale)
    assert not any('Registered workplace:' in s.text for s in result.sections.scale)
    available(row, 'subunits.unit.two', {'name': 'Branch', 'address': {'kommune': 'OSLO'}})
    assert next(s for s in generate(row).sections.scale if s.record_type == 'workplaces').count == 2


def test_quoted_headline_words_stay_verbatim(tmp_path):
    row, _ = envelope(tmp_path)
    claim = available(row, 'identity.registered_activity', 'Example AS is a 1 person company.')
    result = generate(row)
    quoted = next(s for s in result.sections.what_it_does if s.claim_ids == [claim.id])
    assert quoted.text == 'Registered activity: «Example AS is a 1 person company.».'
    assert sentence_error(quoted, row) is None and result.checks.dropped_sentences == 0


def test_housing_cooperative_never_uses_parent_title(tmp_path,monkeypatch):
    import copy
    from signalpost.synthesis import nace as module
    row,_=envelope(tmp_path)
    claim=next(c for c in row.claims if c.field=='identity.nace1')
    claim.value={'kode':'97.001','beskrivelse':'Aktiviteter i borettslag og boligsameier'}
    assert english_title(claim.value,version_id=3218)=='Activities of housing cooperatives'
    assert english_title(claim.value,version_id=30) is None
    result=generate(row)
    forbidden='Activities of households as employers of domestic personnel'
    assert forbidden.casefold() not in result.summary.casefold()
    assert 'Activities of housing cooperatives (NACE 97.001)' in result.summary
    assert sentence_error(Sentence(text='NACE 97.001: '+forbidden+' (Aktiviteter i borettslag og boligsameier).',claim_ids=[claim.id]),row)
    saved=copy.deepcopy(TABLE)
    for version in saved['versions']:version['titles'].pop('97.001',None)
    monkeypatch.setattr(module,'TABLE',saved)
    assert english_title(claim.value) is None
    assert nace_sentence(claim)=='NACE 97.001: Aktiviteter i borettslag og boligsameier.'
    assert forbidden.casefold() not in generate(row).summary.casefold()


def test_workplace_examples_cite_all_records_and_reject_tampering(tmp_path):
    row,_=envelope(tmp_path)
    for i in range(4):available(row,f'subunits.unit.{i}',{'name':f'Branch {i}','address':{'kommune':'OSLO'}})
    row.run.sections['subunits']='available'
    before=[c.model_dump() for c in row.claims]
    result=generate(row)
    sentence=next(s for s in result.sections.scale if s.record_type=='workplaces')
    assert sentence.text=='4 registered workplaces, including Branch 0 (OSLO), Branch 1 (OSLO) and Branch 2 (OSLO).'
    assert len(sentence.claim_ids)==4 and sentence.count==4
    assert [c.model_dump() for c in row.claims]==before
    assert sentence_error(sentence,row) is None
    assert sentence_error(sentence.model_copy(update={'claim_ids':sentence.claim_ids[:-1],'count':3,'text':sentence.text.replace('4 registered','3 registered')}),row)
    assert sentence_error(sentence.model_copy(update={'text':sentence.text.replace('Branch 2','Invented')}),row)
    assert not any(s.text.startswith('Registered workplace:') for s in result.sections.scale)


def test_single_different_workplace_and_all_listed_ads(tmp_path):
    row,_=envelope(tmp_path)
    available(row,'subunits.unit.one',{'name':'Branch','address':{'kommune':'OSLO'}})
    available(row,'hiring.job.one',{'title':'Developer'})
    result=generate(row)
    assert any(s.text=='Registered workplace: Branch, OSLO.' for s in result.sections.scale)
    assert any(s.text=='Verified active ad: Developer.' for s in result.sections.scale)
    assert not any(s.record_type=='active_ads' for s in result.sections.scale)
    for i in range(3):available(row,f'hiring.job.{i}',{'title':f'Job {i}'})
    result=generate(row)
    assert next(s for s in result.sections.scale if s.record_type=='active_ads').count==4
