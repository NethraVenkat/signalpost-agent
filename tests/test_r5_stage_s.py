import copy
import json
import pytest
from signalpost.models.envelope import Envelope
from signalpost.synthesis.template import generate
from signalpost.synthesis.validate import sentence_error, validate_synthesis, SECTIONS
from signalpost.synthesis.financial import analyze, metric_sentence
from signalpost.synthesis.overview import TOPICS, contract_errors
from scripts.verify_output import verify_synthesis, verify
from tests.test_synthesis import envelope
from tests.test_synthesis_readability import available
from tests.test_registry import config,execute,handler


def period(year=2025, **extra):
    return {'fiscal_year':str(year),'period_start':f'{year}-01-01','period_end':f'{year}-12-31',
            'currency':'NOK','unit':'NOK','account_type':'SELSKAP',**extra}


def financial_row(tmp_path):
    row,_=envelope(tmp_path)
    for field,value in [('revenue',1200),('operating_result',-120),('equity',300),('total_assets',1000)]:
        available(row,'accounts.'+field,value,reporting_period=period())
    available(row,'accounts.history.2024-12-31.revenue',1000,reporting_period=period(2024))
    available(row,'identity.latest_submitted_accounts','2026')
    original=row.evidence[0]
    for c in row.claims:
        if c.family!='accounts' or not c.reporting_period:continue
        receipt=original.model_copy(update={'id':c.id,'source_url':'https://data.brreg.no/regnskapsregisteret/regnskap/'+row.organisation_number,
            'content_sha256':'d'*64,'locator':('/1/' if c.field.startswith('accounts.history.') else '/0/')+c.field,
            'extraction_method':'signalpost.registry.v1'})
        from signalpost.models.evidence import digest
        receipt.id=digest([receipt.source_url,receipt.content_sha256,receipt.locator,receipt.extraction_method])
        c.evidence_ids=[receipt.id];row.evidence.append(receipt)
    return row


def test_all_five_elements_are_present_cited_and_mirrored(tmp_path):
    row=financial_row(tmp_path); result=generate(row)
    assert result.contract_version=='r5-S' and not contract_errors(result,row)
    assert set(TOPICS) <= {s.topic for s in result.briefing}
    assert all((s.claim_ids or s.observation_ids) and sentence_error(s,row) is None for s in result.briefing)
    assert all(s.text in result.summary for s in result.briefing if s.topic)
    assert 'First run' in result.summary and 'Partner-screening takeaway' in result.summary
    assert 'Newer filing exists' in result.summary
    row.run.synthesis=result;row.profile.synthesis=result
    verify_synthesis(row.model_dump(mode='json'))


def test_ratios_and_yoy_are_exact_and_cite_both_inputs(tmp_path):
    row=financial_row(tmp_path);metrics,check,gaps=analyze(row)
    assert {m.formula:m.value for m in metrics}=={'operating_margin':'-10.00','equity_ratio':'30.00','revenue_yoy':'20.00'}
    assert not gaps and check['newer_filing_exists']
    for m in metrics:
        assert len(m.input_claim_ids)==2 and sentence_error(metric_sentence(m),row) is None
        bad=metric_sentence(m).model_copy(update={'text':'Derived operating margin: 99.00%.'})
        assert sentence_error(bad,row)


@pytest.mark.parametrize('mutation', ['currency','unit','consolidated','short_period','nonconsecutive','zero_prior','missing_unit'])
def test_yoy_abstains_without_comparability(tmp_path,mutation):
    row=financial_row(tmp_path)
    prior=next(c for c in row.claims if c.field.startswith('accounts.history.'))
    if mutation=='currency':prior.reporting_period['currency']='EUR'
    elif mutation=='unit':prior.reporting_period['unit']='THOUSAND_NOK'
    elif mutation=='consolidated':prior.reporting_period['account_type']='KONSERN'
    elif mutation=='short_period':prior.reporting_period['period_start']='2024-06-01'
    elif mutation=='nonconsecutive':prior.reporting_period=period(2023)
    elif mutation=='zero_prior':prior.value=0
    elif mutation=='missing_unit':prior.reporting_period['unit']=None
    assert not any(m.formula=='revenue_yoy' for m in analyze(row)[0])
    assert 'revenue_yoy' in analyze(row)[2]


@pytest.mark.parametrize('field,formula',[('revenue','operating_margin'),('total_assets','equity_ratio')])
def test_zero_denominators_never_become_zero_ratios(tmp_path,field,formula):
    row=financial_row(tmp_path);next(c for c in row.claims if c.field=='accounts.'+field).value=0
    assert not any(m.formula==formula for m in analyze(row)[0])


def test_missing_activity_and_all_source_failures_are_honest_context_not_fake_facts(tmp_path):
    row,_=envelope(tmp_path);row.claims=[];row.evidence=[]
    row.run.sections={key:'failed' for key in row.run.sections}
    result=generate(row)
    assert len(result.briefing)==5 and not contract_errors(result,row)
    assert 'unknown' in result.briefing[0].text
    assert all(not s.claim_ids and s.observation_ids for s in result.briefing)
    assert all(sentence_error(s,row) is None for s in result.briefing)


@pytest.mark.parametrize('part', ['value','input','state','observation','topic'])
def test_verifier_rejects_tampered_required_topics_and_derived_metadata(tmp_path,part):
    row=financial_row(tmp_path);result=generate(row)
    if part=='value':result.financial_metrics[0].value='999.00'
    elif part=='input':result.financial_metrics[0].input_claim_ids=[result.financial_metrics[0].input_claim_ids[0]]*2
    elif part=='state':row.run.sections['website']='available'
    elif part=='observation':result.observations[0].data['state']='invented'
    elif part=='topic':result.briefing=[s for s in result.briefing if s.topic!='takeaway']
    row.run.synthesis=result;row.profile.synthesis=result
    with pytest.raises(AssertionError):verify_synthesis(row.model_dump(mode='json'))


def test_refresh_with_failed_checks_never_asserts_nothing_changed_everywhere(tmp_path):
    row,_=envelope(tmp_path);row.run.refresh['mode']='refresh';row.run.sections['website']='failed'
    result=generate(row);change=next(s for s in result.briefing if s.topic=='change')
    assert 'compared source scope' in change.text and 'failed' in change.text and change.observation_ids
    assert 'First run' not in change.text


def test_history_is_coverage_not_a_new_business_change():
    from signalpost.refresh.diff import newly_supported_field
    assert newly_supported_field('accounts.history.2024-12-31.revenue')


@pytest.mark.parametrize('mutation',['period','currency','unit','scope','missing_scope','nan','boolean','negative_denominator'])
def test_operating_margin_refuses_unverified_or_incompatible_inputs(tmp_path,mutation):
    row=financial_row(tmp_path)
    top=next(c for c in row.claims if c.field=='accounts.operating_result')
    bottom=next(c for c in row.claims if c.field=='accounts.revenue')
    if mutation=='period':top.reporting_period=period(2024)
    elif mutation=='currency':top.reporting_period['currency']='EUR'
    elif mutation=='unit':top.reporting_period['unit']='THOUSAND_NOK'
    elif mutation=='scope':top.reporting_period['account_type']='KONSERN'
    elif mutation=='missing_scope':top.reporting_period.pop('account_type')
    elif mutation=='nan':top.value=float('nan')
    elif mutation=='boolean':top.value=True
    elif mutation=='negative_denominator':bottom.value=-1
    assert not any(m.formula=='operating_margin' for m in analyze(row)[0])
