import json

import pytest

from signalpost.models.synthesis import Sentence
from signalpost.models.envelope import Envelope
from signalpost.synthesis.template import generate
from signalpost.synthesis.validate import sentence_error, validate_synthesis
from signalpost.synthesis.brief import LIMITATION, EMPLOYEE_GAP, build, select
from scripts.verify_output import verify_synthesis
from tests.test_synthesis import envelope
from tests.test_synthesis_readability import available
from tests.test_registry_changes import event, extract


def rich(tmp_path):
    row, _ = envelope(tmp_path)
    available(row, 'identity.registered_activity', ['Utvikling av programvare.'])
    available(row, 'identity.registered_in_vat', False)
    available(row, 'identity.foreign_register_name', 'Reported Register')
    available(row, 'accounts.revenue', 0, reporting_period={
        'period_start': '2025-01-01', 'period_end': '2025-12-31', 'fiscal_year': '2025', 'currency': 'EUR'})
    section = extract(event())
    row.claims.extend(section.claims)
    row.evidence.extend(section.evidence)
    row.run.sections['activity'] = 'available'
    return row


def test_four_to_six_cited_sentences_cover_all_topics_and_new_depth(tmp_path):
    row = rich(tmp_path)
    result = generate(row)
    assert 4 <= len(result.briefing) <= 6
    assert all(s.claim_ids and sentence_error(s, row) is None for s in result.briefing)
    claims = {c.id: c for c in row.claims}
    fields = {claims[cid].field for s in result.briefing for cid in s.claim_ids}
    assert 'identity.registered_activity' in fields
    assert 'accounts.revenue' in fields
    assert any(f.startswith('roles.role.') for f in fields)
    assert any(f.startswith('registry_change.') for f in fields)
    assert any(s.text == LIMITATION for s in result.briefing)
    assert 'identity.foreign_register_name' in fields
    assert any(s.text == 'Foreign registration authority as reported: Reported Register.' for s in result.briefing)
    assert select(result.model_dump(mode='json'), [c.model_dump(mode='json') for c in row.claims]) == [s.model_dump(mode='json') for s in result.briefing]


@pytest.mark.parametrize('mutation', ['uncited', 'invented', 'wrong_claim'])
def test_briefing_validator_and_independent_verifier_reject_unsupported_sentences(tmp_path, mutation):
    row = rich(tmp_path); result = generate(row)
    original = result.briefing[0]
    bad = original.model_copy(deep=True)
    if mutation == 'uncited': bad.claim_ids = []
    elif mutation == 'invented': bad.text = 'Reported revenue: EUR 999999999.'
    else: bad.claim_ids = [next(c.id for c in row.claims if c.field=='identity.legal_name')]
    result.briefing = [bad]
    row.run.synthesis = result; row.profile.synthesis = result
    with pytest.raises(AssertionError, match='Unverified briefing'):
        verify_synthesis(row.model_dump(mode='json'))
    checked = validate_synthesis(result, row)
    assert not checked.briefing
    assert any(r['section']=='briefing' for r in checked.checks.rejections)


def test_no_sentence_can_lack_a_citation(tmp_path):
    row = rich(tmp_path); result = generate(row)
    sentences = [s for key in ('what_it_does','scale','leadership','changes') for s in getattr(result.sections,key)] + result.briefing
    assert sentences and all(s.claim_ids for s in sentences)
    for sentence in sentences:
        assert sentence_error(sentence.model_copy(update={'claim_ids': []}), row) == 'uncited_sentence'


def test_sparse_companies_are_not_padded(tmp_path):
    row, _ = envelope(tmp_path)
    row.claims = [c for c in row.claims if c.field=='identity.legal_name']
    result = generate(row)
    assert len(result.briefing) < 4
    assert any(u.family=='briefing' and 'no unsupported padding' in u.reason for u in result.sections.unknowns)
    assert all(s.claim_ids and sentence_error(s,row) is None for s in result.briefing)


def test_gap_cannot_invent_missing_employee_or_financial_history(tmp_path):
    row = rich(tmp_path)
    flag = available(row, 'identity.employees_reported', False)
    result = generate(row)
    employee = Sentence(text=EMPLOYEE_GAP, claim_ids=[flag.id])
    assert sentence_error(employee, row) is None
    count = available(row, 'identity.employees', 0)
    assert sentence_error(employee, row) == 'unverified_employee_gap'
    row.claims = [c for c in row.claims if c.id != count.id]
    flag.value = True
    assert sentence_error(employee, row) == 'unverified_employee_gap'
    limitation = next(s for s in result.sections.scale if s.text==LIMITATION)
    available(row, 'accounts.net_result', 2, reporting_period={'period_end':'2024-12-31','fiscal_year':'2024'})
    assert sentence_error(limitation,row) == 'unverified_reporting_limitation'


def test_registry_depth_is_field_bound_and_template_only(tmp_path):
    row = rich(tmp_path); result = generate(row)
    frame = next(s for s in result.sections.scale if s.text.startswith('Foreign registration authority'))
    assert sentence_error(frame, row) is None
    other = next(c for c in row.claims if c.field=='identity.legal_name')
    assert sentence_error(frame.model_copy(update={'claim_ids':[other.id]}),row) == 'misbound_registry_depth'
    assert result.mode=='template' and result.generator.model is None


def test_briefing_is_lossless_across_envelope_shapes(tmp_path):
    from signalpost.models.shapes import serialize
    row = rich(tmp_path); row.run.synthesis = generate(row); row.profile.synthesis = row.run.synthesis
    expected = [s.model_dump(mode='json') for s in row.run.synthesis.briefing]
    for shape in ('contract','reference','union'):
        data = serialize(row,shape)
        synthesis = data['run']['synthesis'] if 'run' in data else data['profile']['synthesis']
        assert synthesis['briefing'] == expected
        assert verify_synthesis(data)[0] == 1
