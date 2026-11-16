import asyncio
import copy
import json
from datetime import datetime,timezone
import httpx
import pytest
from signalpost.sources import exact_public as ep
from signalpost.sources.http import Response
from signalpost.sources.blobstore import BlobStore
from signalpost.budget import Budget,SourceFailure
from tests.test_registry import config,execute,handler

ORG='923609016'
LEI='5967007LIEEXZXEW2W49'
PARENT='549300BUEC6313YZHX74'
NOW=datetime(2026,11,13,tzinfo=timezone.utc)


def record(org=ORG):
    return {'id':LEI,'attributes':{'lei':LEI,'entity':{'registeredAs':org[:3]+' '+org[3:6]+' '+org[6:],
        'registeredAt':{'id':'RA000472'},'jurisdiction':'NO','legalAddress':{'country':'NO'},'status':'ACTIVE','legalForm':{'id':'YI42'}},
        'registration':{'initialRegistrationDate':'2020-01-01T00:00:00Z','nextRenewalDate':'2027-01-01T00:00:00Z','status':'ISSUED'}},
        'relationships':{'direct-parent':{'links':{'relationship-record':ep.GLEIF+'lei-records/'+LEI+'/direct-parent-relationship'}}}}


def relationship():
    return {'attributes':{'relationship':{'startNode':{'id':LEI,'type':'LEI'},'endNode':{'id':PARENT,'type':'LEI'},
        'type':'IS_DIRECTLY_CONSOLIDATED_BY','status':'ACTIVE'},'registration':{'status':'PUBLISHED'}}}


@pytest.mark.parametrize('path,value',[('registeredAs','923609017'),('registeredAs','NO923609016MVA'),
    ('registeredAt',{'id':'RA000473'}),('jurisdiction','SE'),('legalAddress',{'country':'SE'})])
def test_gleif_wrong_country_registry_and_id_rejected(path,value):
    item=record();item['attributes']['entity'][path]=value
    assert ep.lei_record(item,ORG) is None


@pytest.mark.parametrize('path,value',[('status','INACTIVE'),('status',None),('type','IS_ULTIMATELY_CONSOLIDATED_BY'),
    ('startNode',{'id':PARENT,'type':'LEI'}),('endNode',{'id':PARENT,'type':'OTHER'})])
def test_parent_requires_active_exact_child_and_kind(path,value):
    item=relationship();item['attributes']['relationship'][path]=value
    assert ep.parent_record(item,LEI,'direct') is None


def test_exact_formats_and_live_status_is_not_assumed():
    assert ep.org_id(ORG)==ep.org_id('923 609 016')==ORG
    assert ep.org_id('9236090160') is None
    item=record();item['attributes']['entity']['status']='INACTIVE'
    assert ep.lei_record(item,ORG)['entity_status']=='INACTIVE'
    assert ep.parent_record(relationship(),LEI,'direct')['parent_lei']==PARENT


def xml(org=ORG,country='NOR',day='2026-10-01',winners='ORG-0002',amount='999999'):
    return f'''<ContractAwardNotice xmlns="urn:oasis:names:specification:ubl:schema:xsd:ContractAwardNotice-2"
     xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
     xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
     xmlns:efac="http://data.europa.eu/p27/eforms-ubl-extension-aggregate-components/1">
     <cac:ProcurementProject><cbc:Name>Supported lot title</cbc:Name></cac:ProcurementProject>
     <cac:ContractingParty><cac:Party><cac:PartyIdentification><cbc:ID>ORG-0001</cbc:ID></cac:PartyIdentification></cac:Party></cac:ContractingParty>
     <efac:Organizations>
     <efac:Organization><efac:Company><cac:PartyIdentification><cbc:ID>ORG-0001</cbc:ID></cac:PartyIdentification><cac:PartyName><cbc:Name>Other buyer</cbc:Name></cac:PartyName><cac:PartyLegalEntity><cbc:RegistrationName>Other buyer</cbc:RegistrationName><cbc:CompanyID>993578843</cbc:CompanyID></cac:PartyLegalEntity><cac:PostalAddress><cac:Country><cbc:IdentificationCode>NOR</cbc:IdentificationCode></cac:Country></cac:PostalAddress></efac:Company></efac:Organization>
     <efac:Organization><efac:Company><cac:PartyIdentification><cbc:ID>ORG-0002</cbc:ID></cac:PartyIdentification><cac:PartyLegalEntity><cbc:RegistrationName>Fixture winner</cbc:RegistrationName><cbc:CompanyID>{org}</cbc:CompanyID></cac:PartyLegalEntity><cac:PostalAddress><cac:Country><cbc:IdentificationCode>{country}</cbc:IdentificationCode></cac:Country></cac:PostalAddress></efac:Company></efac:Organization>
     </efac:Organizations><efac:LotTender><cbc:ID>TEN-0001</cbc:ID><efac:TenderLot><cbc:ID>LOT-0001</cbc:ID></efac:TenderLot><efac:TenderingParty><cbc:ID>TPA-0001</cbc:ID></efac:TenderingParty><cbc:PayableAmount currencyID="NOK">{amount}</cbc:PayableAmount></efac:LotTender>
     <efac:SettledContract><cbc:ID>CON-0001</cbc:ID><cbc:AwardDate>{day}</cbc:AwardDate><efac:LotTender><cbc:ID>TEN-0001</cbc:ID></efac:LotTender></efac:SettledContract>
     <efac:TenderingParty><cbc:ID>TPA-0001</cbc:ID><efac:Tenderer><cbc:ID>{winners}</cbc:ID></efac:Tenderer></efac:TenderingParty>
     <efac:LotResult><cbc:TenderResultCode>selec-w</cbc:TenderResultCode><efac:LotTender><cbc:ID>TEN-0001</cbc:ID></efac:LotTender><efac:SettledContract><cbc:ID>CON-0001</cbc:ID></efac:SettledContract><efac:TenderLot><cbc:ID>LOT-0001</cbc:ID></efac:TenderLot></efac:LotResult>
     <cbc:TotalAmount currencyID="NOK">999999999</cbc:TotalAmount></ContractAwardNotice>'''.encode()


@pytest.mark.parametrize('kwargs',[{'org':'993578843'},{'country':'SWE'},{'day':'2022-10-01'},
    {'day':'2027-01-01'},{'winners':'ORG-9999'}])
def test_ted_rejects_wrong_id_country_date_and_unlinked_winner(kwargs):
    assert not ep.ted_xml(xml(**kwargs),ORG,'123-2026',NOW)


def test_ted_amount_is_never_notice_total_or_unproven_lot_allocation():
    items=ep.ted_xml(xml(),ORG,'123-2026',NOW)
    assert len(items)==1 and items[0]['matched_role']=='winner'
    assert items[0]['buyer']=='Other buyer' and items[0]['lot_id']=='LOT-0001'
    assert not any('amount' in k or 'value' in k for k in items[0])
    assert not ep.ted_xml(b'<!DOCTYPE x>'+xml(),ORG,'123-2026',NOW)
    assert not ep.ted_xml(xml().replace(b'selec-w',b'non-aw'),ORG,'123-2026',NOW)
    assert not ep.ted_xml(xml().replace(b'<cbc:ID>CON-0001</cbc:ID>',b'<cbc:ID>CON-0002</cbc:ID>',1),ORG,'123-2026',NOW)


def test_seven_evaluator_flags_enable_both_new_exact_sources(tmp_path,monkeypatch):
    import sys
    from signalpost import cli
    from signalpost.config import Config
    async def capture(cfg):
        assert cfg.gleif and cfg.procurement
        assert cfg.state_aid and cfg.research  # Stage S default-on with the seven evaluator flags
        assert cfg.websites and cfg.hiring and cfg.public_activity
        assert (cfg.website_request_cap,cfg.website_total_request_cap)==(8,13)
        return dict(emitted_envelopes=100,invalid_inputs=[],requests=0,runtime_ms=0,changes=0,
            observation_changes=0,deadline_hits=0,warnings=[])
    monkeypatch.setattr(cli,'run',capture)
    monkeypatch.setattr(sys,'argv',['signalpost','run','--organisations','batch','--bulk','registry',
        '--output',str(tmp_path/'o'),'--profiles-output',str(tmp_path/'p'),'--report',str(tmp_path/'r'),
        '--run-id','T-seven','--expected-count','100'])
    assert cli.main()==0
    assert Config(organisations='batch',output='o',report='r').gleif


class Stub:
    def __init__(self,bodies):self.bodies=iter(bodies);self.urls=[]
    async def request(self,url,org,payload=None):
        self.urls.append((url,payload));item=next(self.bodies)
        if isinstance(item,Exception):raise item
        body=json.dumps(item).encode();return Response(body,200,url,'2026-11-13T00:00:00Z',__import__('hashlib').sha256(body).hexdigest())


def test_gleif_pagination_batch_both_id_formats_and_parent_evidence():
    http=Stub([{'data':[],'links':{'next':ep.GLEIF+'lei-records?page[number]=2'}},
        {'data':[record()],'links':{}},{'data':relationship()}])
    result=asyncio.run(ep.gleif_batch([ORG],http))[ORG]
    assert [c.field for c in result.claims]==['gleif.record','gleif.parent.direct']
    assert set(result.claims[0].evidence_ids)<=set(result.claims[1].evidence_ids)
    assert '923609016%2C923+609+016' in http.urls[0][0]
    assert len(http.urls)==3


def test_gleif_cycle_and_budget_failure_stay_explicit():
    for response in [SourceFailure('budget_exhausted'),{'data':[],'links':{'next':'https://foreign.test/x'}}]:
        result=asyncio.run(ep.gleif_batch([ORG],Stub([response])))[ORG]
        assert result.state=='failed' and not result.claims


def test_ted_pagination_does_not_silently_truncate():
    class Pages:
        def __init__(self):self.pages=[]
        async def request(self,url,org,payload=None):
            self.pages.append(payload['page']);page=payload['page']
            notices=[{'publication-number':str(n+1)+'-2026'} for n in range(100)] if page==1 else []
            return Response(json.dumps({'notices':notices}).encode(),200,url,'2026-11-13T00:00:00Z','0'*64)
    http=Pages();result=asyncio.run(ep.ted_batch([ORG],http,NOW))
    assert http.pages==[1,2] and result[ORG].state=='not_available'


def test_http_global_stop_robots_refusal_and_no_redirect(tmp_path,monkeypatch):
    async def go():
        cfg=config(tmp_path,[ORG],max_requests=1);budget=Budget(cfg);calls=[]
        def source(r):calls.append(str(r.url));return httpx.Response(200,text='User-agent: *\nDisallow: /api/')
        async with httpx.AsyncClient(transport=httpx.MockTransport(source)) as client:
            http=ep.PublicHttp(client,cfg,budget,BlobStore(cfg.state_dir))
            with pytest.raises(SourceFailure,match='public_robots_blocked'):await http.request(ep.GLEIF+'lei-records',ORG)
            assert len(calls)==len(budget.events)==1
            with pytest.raises(SourceFailure,match='budget_exhausted'):await http.raw('https://api.gleif.org/other',ORG)
            with pytest.raises(SourceFailure,match='public_url_refused'):await http.raw('https://foreign.test',ORG)
    asyncio.run(go())


def test_integration_defaults_separate_failures_and_independent_tamper_check(tmp_path,monkeypatch):
    from scripts.verify_output import verify
    monkeypatch.setattr(ep,'POLITENESS_SECONDS',0)
    def source(request):
        if request.url.host=='api.gleif.org':
            if request.url.path=='/robots.txt':return httpx.Response(200,text='User-agent: *\nDisallow:')
            if request.url.path.endswith('direct-parent-relationship'):return httpx.Response(200,json={'data':relationship()})
            return httpx.Response(200,json={'data':[record()],'links':{}})
        if request.url.host=='api.ted.europa.eu':
            if request.url.path=='/robots.txt':return httpx.Response(404)
            return httpx.Response(503)
        return handler()(request)
    cfg=config(tmp_path,[ORG],gleif=True,procurement=True)
    async def go():
        from signalpost.runner import run
        async with httpx.AsyncClient(transport=httpx.MockTransport(source)) as client:
            return await run(cfg,client)
    report=asyncio.run(go());row=json.loads(cfg.output.read_text(encoding='utf8'))
    assert row['run']['sections']['gleif']=='available' and row['run']['sections']['procurement']=='failed'
    assert row['run']['sections']['identity']=='available'
    assert any(LEI in s['text'] and PARENT in s['text'] for s in row['run']['synthesis']['briefing'])
    assert verify(cfg.output,cfg.state_dir,1,cfg.organisations,cfg.report)['exact_public_items_verified']==2
    row['claims'][next(i for i,c in enumerate(row['claims']) if c['field']=='gleif.record')]['value']['legal_form']='invented'
    with pytest.raises(AssertionError):
        from scripts.verify_output import verify_exact_public
        verify_exact_public(row,row,{e['id']:e for e in row['evidence']},lambda sha:(cfg.state_dir/'blobs'/sha).read_text(encoding='utf8'))


def test_ted_xml_receipts_verify_and_site_has_dated_award(tmp_path,monkeypatch):
    from scripts.verify_output import verify
    from signalpost.runner import run
    monkeypatch.setattr(ep,'POLITENESS_SECONDS',0)
    def source(request):
        if request.url.host=='api.ted.europa.eu':
            if request.url.path=='/robots.txt':return httpx.Response(404)
            return httpx.Response(200,json={'notices':[{'publication-number':'123-2026','winner-identifier':[ORG]}]})
        if request.url.host=='ted.europa.eu':
            if request.url.path=='/robots.txt':return httpx.Response(200,text='User-agent: *\nDisallow:')
            return httpx.Response(200,content=xml(),headers={'content-type':'application/xml'})
        return handler()(request)
    cfg=config(tmp_path,[ORG],gleif=False,procurement=True,site_dir=tmp_path/'site')
    async def go():
        async with httpx.AsyncClient(transport=httpx.MockTransport(source)) as client:return await run(cfg,client)
    report=asyncio.run(go());row=json.loads(cfg.output.read_text(encoding='utf8'))
    assert report['site']['state']=='available'
    assert row['run']['sections']['procurement']=='available'
    assert verify(cfg.output,cfg.state_dir,1,cfg.organisations,cfg.report)['exact_public_items_verified']==1
    assert 'Public procurement award' in (cfg.site_dir/'c'/f'{ORG}.html').read_text(encoding='utf8')
