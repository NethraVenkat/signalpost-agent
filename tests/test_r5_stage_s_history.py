import copy,json
import httpx
import pytest
from signalpost.models.envelope import Envelope
from signalpost.synthesis.template import generate
from scripts.verify_output import verify
from tests.test_registry import config,execute,handler,entity

ORG='923609016'
OTHER='993578843'


def response_factory(kind='valid'):
    def response(request):
        if '/aarsregnskap/kopi/' in str(request.url):return httpx.Response(200,json=['2024','2025','2026'])
        if '/regnskapsregisteret/' in str(request.url):
            current={'regnskapstype':'SELSKAP','virksomhet':{'organisasjonsnummer':ORG},'valuta':'NOK','enhet':'NOK',
                     'regnskapsperiode':{'fraDato':'2025-01-01','tilDato':'2025-12-31'},
                     'resultatregnskapResultat':{'driftsresultat':{'driftsinntekter':{'sumDriftsinntekter':1200},'driftsresultat':120},'aarsresultat':100},
                     'egenkapitalGjeld':{'egenkapital':{'sumEgenkapital':300}},'eiendeler':{'sumEiendeler':1000}}
            old=copy.deepcopy(current);old['regnskapsperiode']={'fraDato':'2024-01-01','tilDato':'2024-12-31'}
            old['resultatregnskapResultat']['driftsresultat']['driftsinntekter']['sumDriftsinntekter']=1000
            if kind=='wrong_owner':old['virksomhet']['organisasjonsnummer']=OTHER
            elif kind=='missing_unit':old.pop('enhet')
            elif kind=='consolidated':old['regnskapstype']='KONSERN'
            elif kind=='malformed':old['resultatregnskapResultat']['aarsresultat']='not a number'
            return httpx.Response(200,json=[current,old])
        if request.url.path.endswith('/enheter/'+ORG):
            data=entity(ORG);data['sisteInnsendteAarsregnskap']='2026'
            return httpx.Response(200,json=data)
        return handler()(request)
    return response


def test_history_and_ratios_use_one_response_and_all_values_verify(tmp_path):
    cfg=config(tmp_path,[ORG]);report,rows=execute(cfg,response_factory())
    row=rows[0];s=row['run']['synthesis']
    assert any(c['field']=='accounts.history.2024-12-31.revenue' and c['value']==1000 for c in row['claims'])
    assert {m['formula']:m['value'] for m in s['financial_metrics']}=={'operating_margin':'10.00','equity_ratio':'30.00','revenue_yoy':'20.00'}
    assert s['financial_year_check']['newer_filing_exists']
    assert sum('/regnskapsregisteret/' in e['url'] for e in report['request_log'])==2
    result=verify(cfg.output,cfg.state_dir,1,cfg.organisations,cfg.report)
    assert result['financial_inputs_verified']>7 and result['derived_financial_metrics_verified']==3


@pytest.mark.parametrize('kind',['wrong_owner','consolidated','malformed','missing_unit'])
def test_bad_or_unscaled_history_never_authorizes_yoy(tmp_path,kind):
    cfg=config(tmp_path,[ORG]);_,rows=execute(cfg,response_factory(kind));row=rows[0]
    assert next(c['value'] for c in row['claims'] if c['field']=='accounts.revenue')==1200
    assert not any(m['formula']=='revenue_yoy' for m in row['run']['synthesis']['financial_metrics'])
    if kind in {'wrong_owner','consolidated','malformed'}:
        assert not any(c['field'].startswith('accounts.history.') for c in row['claims'])
    else:
        c=next(c for c in row['claims'] if c['field'].endswith('.revenue') and c['field'].startswith('accounts.history.'))
        assert c['reporting_period']['unit'] is None
    verify(cfg.output,cfg.state_dir,1,cfg.organisations,cfg.report)


def test_raw_financial_value_tampering_is_detected_even_with_regenerated_summary(tmp_path):
    cfg=config(tmp_path,[ORG]);_,rows=execute(cfg,response_factory());row=Envelope.model_validate(rows[0])
    next(c for c in row.claims if c.field=='accounts.revenue').value=9999
    row.run.synthesis=generate(row);row.profile.synthesis=row.run.synthesis
    cfg.output.write_text(json.dumps(row.model_dump(mode='json'))+'\n',encoding='utf8')
    with pytest.raises(AssertionError,match='Financial value differs'):
        verify(cfg.output,cfg.state_dir,1,cfg.organisations,cfg.report)


def test_raw_registry_year_tampering_is_detected_even_with_regenerated_summary(tmp_path):
    cfg=config(tmp_path,[ORG]);_,rows=execute(cfg,response_factory());row=Envelope.model_validate(rows[0])
    next(c for c in row.claims if c.field=='identity.latest_submitted_accounts').value='2027'
    row.run.synthesis=generate(row);row.profile.synthesis=row.run.synthesis
    cfg.output.write_text(json.dumps(row.model_dump(mode='json'))+'\n',encoding='utf8')
    with pytest.raises(AssertionError,match='Registry filing year differs'):
        verify(cfg.output,cfg.state_dir,1,cfg.organisations,cfg.report)
