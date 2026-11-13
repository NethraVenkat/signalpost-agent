import copy,json
import httpx,pytest
from tests.test_r5_stage_s import financial_row
from tests.test_r5_stage_s_history import response_factory
from tests.test_registry import config,execute
from signalpost.synthesis.financial import analyze
from signalpost.synthesis.template import generate
from signalpost.synthesis.validate import sentence_error
from signalpost.models.synthesis import Sentence
from scripts.verify_output import verify


def test_absent_units_cancel_with_same_statement_and_schema(tmp_path):
    row=financial_row(tmp_path)
    for c in row.claims:
        if c.reporting_period:c.reporting_period['unit']=None
    metrics=analyze(row)[0]
    assert {m.formula:m.value for m in metrics}=={'operating_margin':'-10.00','equity_ratio':'30.00','revenue_yoy':'20.00'}
    assert all(m.reporting_period['unit'] is None for m in metrics)


def test_equal_periods_do_not_authorize_cross_statement_ratio(tmp_path):
    row=financial_row(tmp_path)
    c=next(c for c in row.claims if c.field=='accounts.operating_result')
    e=next(e for e in row.evidence if e.id==c.evidence_ids[0]);e.locator='/2/operating_result'
    assert not any(m.formula=='operating_margin' for m in analyze(row)[0])


def test_absent_units_require_same_approved_schema_for_yoy(tmp_path):
    row=financial_row(tmp_path)
    for c in row.claims:
        if c.reporting_period:c.reporting_period['unit']=None
    prior=next(c for c in row.claims if c.field.startswith('accounts.history.'))
    e=next(e for e in row.evidence if e.id==prior.evidence_ids[0]);e.extraction_method='other.schema.v1'
    assert not any(m.formula=='revenue_yoy' for m in analyze(row)[0])


def test_real_receipts_restore_ratios_yoy_without_absolute_scale(tmp_path):
    def response(request):
        result=response_factory()(request)
        if '/regnskap/923609016' in str(request.url):
            body=result.json()
            for record in body:record.pop('enhet',None)
            return httpx.Response(200,json=body)
        return result
    cfg=config(tmp_path,['923609016']);_,rows=execute(cfg,response)
    raw=rows[0]['run']['synthesis']
    assert {m['formula']:m['value'] for m in raw['financial_metrics']}=={'operating_margin':'10.00','equity_ratio':'30.00','revenue_yoy':'20.00'}
    assert verify(cfg.output,cfg.state_dir,1,cfg.organisations,cfg.report)['derived_financial_metrics_verified']==3
    assert 'NOK 1,200' not in raw['summary']
    from signalpost.models.envelope import Envelope
    row=Envelope.model_validate(rows[0]);revenue=next(c for c in row.claims if c.field=='accounts.revenue')
    assert sentence_error(Sentence(text='Reported revenue: NOK 1,200.',claim_ids=[revenue.id]),row)
