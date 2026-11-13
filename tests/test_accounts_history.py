import asyncio,copy,json
from types import SimpleNamespace
from pathlib import Path
import httpx,pytest
from signalpost.sources import accounts_years,regnskap
from signalpost.sources.http import Response,Http
from signalpost.sources.blobstore import BlobStore
from signalpost.models.evidence import utc_now
from signalpost.models.envelope import Envelope
from signalpost.synthesis.template import generate
from signalpost.budget import Budget
from scripts.verify_output import verify_filing_years,verify
from tests.test_registry import config,execute,handler
from tests.test_r5_stage_s_history import response_factory

ORG='923609016'

def response(body,blobs,url=None):
    raw=json.dumps(body).encode()
    return Response(raw,200,url or accounts_years.YEARS.format(org=ORG),utc_now(),blobs.put(raw))

def test_filed_year_list_exact_scope_dedup_and_saved_verification(tmp_path):
    blobs=BlobStore(tmp_path);r=response(['2024','2025','2024','2010'],blobs)
    section=accounts_years.extract(ORG,r)
    assert section.claims[0].value==['2025','2024','2010']
    assert len(section.claims)==4
    data={'claims':[c.model_dump() for c in section.claims]};evidence={e.id:e.model_dump() for e in section.evidence}
    assert verify_filing_years({'organisation_number':ORG},data,evidence,lambda sha:blobs.read(sha).decode())==4
    data['claims'][0]['value'].append('2026')
    with pytest.raises(AssertionError,match='differs'):verify_filing_years({'organisation_number':ORG},data,evidence,lambda sha:blobs.read(sha).decode())

@pytest.mark.parametrize('body',[[2025],['2025-12-31'],{'years':['2025']},['twenty'],['２０２５']])
def test_bad_year_list_withheld(tmp_path,body):
    from signalpost.budget import SourceFailure
    blobs=BlobStore(tmp_path)
    with pytest.raises(SourceFailure):accounts_years.extract(ORG,response(body,blobs))

def test_year_list_wrong_endpoint_withheld(tmp_path):
    from signalpost.budget import SourceFailure
    blobs=BlobStore(tmp_path)
    with pytest.raises(SourceFailure,match='differs'):accounts_years.extract(ORG,response(['2025'],blobs,accounts_years.YEARS.format(org='993578843')))

def test_all_returned_history_has_independent_periods_and_no_unit_inference(tmp_path):
    base=response_factory()(httpx.Request('GET',regnskap.URL+ORG)).json()[0]
    rows=[]
    for year,unit,currency in [(2025,None,'NOK'),(2024,'THOUSAND_EUR','EUR'),(2023,None,'NOK')]:
        row=copy.deepcopy(base);row['regnskapsperiode']={'fraDato':f'{year}-01-01','tilDato':f'{year}-12-31'}
        row['enhet']=unit;row['valuta']=currency;rows.append(row)
    rows.append(copy.deepcopy(rows[-1]))
    blobs=BlobStore(tmp_path);section=regnskap.extract(ORG,response(rows,blobs,regnskap.URL+ORG),blobs)
    claims={c.field:c for c in section.claims}
    assert claims['accounts.revenue'].reporting_period['unit'] is None
    assert claims['accounts.history.2024-12-31.revenue'].reporting_period['unit']=='THOUSAND_EUR'
    assert claims['accounts.history.2024-12-31.revenue'].reporting_period['currency']=='EUR'
    assert claims['accounts.history.2023-12-31.revenue'].reporting_period['unit'] is None
    assert len({c.id for c in section.claims})==len(section.claims)
    assert not any(e.source_class=='company_report' for e in section.evidence)

def test_filed_years_feed_newer_flag_and_yoy_only_comparable(tmp_path):
    def dispatch(request):
        if '/aarsregnskap/kopi/' in str(request.url):return httpx.Response(200,json=['2024','2025','2027'])
        return response_factory()(request)
    cfg=config(tmp_path,[ORG]);report,rows=execute(cfg,dispatch)
    row=rows[0];check=row['run']['synthesis']['financial_year_check']
    assert check['newer_filing_exists'] and check['registry_year']=='2027'
    year_claim=next(c for c in row['claims'] if c['field']=='accounts.filed_years')
    assert year_claim['id'] in check['claim_ids']
    assert any(m['formula']=='revenue_yoy' and m['value']=='20.00' for m in row['run']['synthesis']['financial_metrics'])
    assert verify(cfg.output,cfg.state_dir,1,cfg.organisations,cfg.report)['filing_year_facts_verified']==4
    env=Envelope.model_validate(row);next(c for c in env.claims if c.field=='accounts.revenue').reporting_period['unit']=None
    assert not any(m.formula=='revenue_yoy' for m in generate(env).financial_metrics)


def test_year_failure_preserves_figures_and_is_explicit(tmp_path):
    def dispatch(request):
        if '/aarsregnskap/kopi/' in str(request.url):return httpx.Response(403,text='not permitted')
        return response_factory()(request)
    cfg=config(tmp_path,[ORG]);_,rows=execute(cfg,dispatch)
    assert next(c['value'] for c in rows[0]['claims'] if c['field']=='accounts.revenue')==1200
    assert any(e['code']=='filing_years_http_blocked' for e in rows[0]['errors'])


def test_year_request_consumes_global_budget_without_overrun(tmp_path):
    cfg=config(tmp_path,[ORG],max_requests=1);budget=Budget(cfg);blobs=BlobStore(cfg.state_dir)
    calls=[]
    def dispatch(request):
        calls.append(str(request.url));return response_factory()(request)
    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(dispatch)) as client:
            return await regnskap.fetch(ORG,Http(client,cfg,budget,blobs))
    section=asyncio.run(run())
    assert len(calls)==len(budget.events)==1
    assert any(c.field=='accounts.revenue' and c.value==1200 for c in section.claims)
    assert any(e.code=='filing_years_budget_exhausted' for e in section.errors)


def test_history_failure_and_recovery_are_observations_not_filing_deletions(tmp_path):
    first=config(tmp_path/'first',[ORG]);execute(first,response_factory())
    def dispatch(request):
        if '/aarsregnskap/kopi/' in str(request.url):return httpx.Response(403,text='blocked')
        return response_factory()(request)
    second=config(tmp_path/'second',[ORG],previous=first.output)
    report,rows=execute(second,dispatch)
    assert report['changes']==0
    assert next(c for c in rows[0]['claims'] if c['field']=='accounts.filed_years')['availability']=='blocked'
    third=config(tmp_path/'third',[ORG],previous=second.output)
    report,rows=execute(third,response_factory())
    assert report['changes']==0 and report['observation_changes']>0


def test_site_labels_undeclared_units_and_filed_years(tmp_path):
    from signalpost.site import fact
    cfg=config(tmp_path,[ORG]);_,rows=execute(cfg,response_factory())
    claim=next(c for c in rows[0]['claims'] if c['field']=='accounts.revenue')
    claim['reporting_period']['unit']=None
    assert 'Unit: unknown (not declared by source)' in fact(claim,{})
    filed=next(c for c in rows[0]['claims'] if c['field']=='accounts.filed_years')
    assert 'Filed accounting years (copies available)' in fact(filed,{})
    year=next(c for c in rows[0]['claims'] if c['field']=='accounts.filed_year.2025')
    from signalpost.site import anchor
    compact=fact(year,{},filed)
    assert anchor(year) in compact and 'href="#'+anchor(filed)+'"' in compact
    assert 'Year-list evidence' in compact and '2025' in compact


def test_removed_copy_year_cites_complete_current_list(tmp_path):
    first=config(tmp_path/'first',[ORG]);execute(first,response_factory())
    def dispatch(request):
        if '/aarsregnskap/kopi/' in str(request.url):return httpx.Response(200,json=['2025','2026'])
        return response_factory()(request)
    second=config(tmp_path/'second',[ORG],previous=first.output)
    _,rows=execute(second,dispatch)
    removed=next(c for c in rows[0]['changes'] if c['field']=='accounts.filed_year.2024')
    assert removed['type']=='removed' and removed['old_evidence_ids'] and removed['new_evidence_ids']
    evidence={e['id']:e for e in rows[0]['evidence']}
    assert all(evidence[eid]['extraction_method']=='signalpost.accounts_years.v1' for eid in removed['new_evidence_ids'])


def test_filing_year_rate_limit_pacing_and_shared_cooldown(tmp_path,monkeypatch):
    monkeypatch.setattr('signalpost.sources.http.FILING_YEAR_INTERVAL',2.1)
    cfg=config(tmp_path,[ORG],time_budget_seconds=1000)
    budget=Budget(cfg);budget.deadline+=1000
    starts=[];waits=[];clock=[0.0]
    def dispatch(request):
        starts.append(clock[0])
        return httpx.Response(429,headers={'Retry-After':'90'},text='limited') if len(starts)==2 else httpx.Response(200,json=['2025'])
    async def pause(delay):waits.append(delay);clock[0]+=delay
    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(dispatch)) as client:
            http=Http(client,cfg,budget,BlobStore(cfg.state_dir));http.year_clock=lambda:clock[0];http.year_sleep=pause
            for _ in range(3):await http.get(accounts_years.YEARS.format(org=ORG),ORG)
    asyncio.run(run())
    assert starts==pytest.approx([0,2.1,92.1])
    assert waits==pytest.approx([2.1,90])
    assert len(budget.events)==3  # no hidden immediate retry on 429
    assert budget.events[1]['rate_limit_backoff_seconds']==90


def test_legacy_inferred_unit_cannot_return_on_source_outage(tmp_path):
    def unscaled(request):
        result=response_factory()(request)
        if '/regnskap/'+ORG in str(request.url):
            data=result.json()
            for record in data:record.pop('enhet',None)
            return httpx.Response(200,json=data)
        return result
    first=config(tmp_path/'first',[ORG]);_,rows=execute(first,unscaled)
    old=Envelope.model_validate(rows[0])
    for claim in old.claims:
        if claim.family=='accounts' and claim.reporting_period and not claim.field.startswith('accounts.history.'):
            claim.reporting_period.update(unit='NOK',source_unit=None,unit_basis='four_exact_parent_2025_ratios_within_0.995_1.005')
    old.run.synthesis=generate(old);old.profile.synthesis=old.run.synthesis
    first.output.write_text(json.dumps(old.model_dump(mode='json'))+'\n',encoding='utf8')
    def outage(request):
        if '/regnskapsregisteret/' in str(request.url):return httpx.Response(503,text='unavailable')
        return response_factory()(request)
    second=config(tmp_path/'second',[ORG],previous=first.output)
    second.state_dir=first.state_dir  # Keep the historical hashed bodies for independent verification.
    _,rows=execute(second,outage)
    current=next(c for c in rows[0]['claims'] if c['field']=='accounts.revenue')
    assert current['carried_forward'] and current['reporting_period']['unit'] is None
    assert 'unit_basis' not in current['reporting_period']
    assert verify(second.output,second.state_dir,1,second.organisations,second.report)['derived_financial_metrics_verified']==3
