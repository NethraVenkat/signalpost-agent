import asyncio
import copy
import json
import httpx
import pytest
from signalpost.runner import run
from signalpost.models.envelope import Envelope
from signalpost.sources import registry_changes as rc
from scripts.verify_output import verify
from tests.test_registry import config,handler
from tests.test_registry_changes import ORG,OTHER,NOW,event,response,envelope,extract


@pytest.mark.parametrize('kind,title',[('Ny','Registry record created'),('Endring','Registry record updated'),
    ('Sletting','Registry record deleted'),('Ukjent','Registry record updated')])
def test_every_event_type_has_honest_date_and_plain_label(kind,title):
    result=extract(event(endringstype=kind,endringer=[]))
    assert len(result.claims)==1
    c=result.claims[0];assert c.value['title']==title and c.value['event_type']==kind
    assert 'effective date' in rc.sentence(c.value) and c.value['date']==event()['dato']
    assert 'new_value' not in c.value and not c.value['changed_fields']


def test_one_claim_per_event_preserves_every_supplied_changed_field():
    changes=[{'path':'/navn','op':'replace','value':'Name'},
             {'path':'/antallAnsatte','op':'replace','value':17},
             {'path':'/postadresse','op':'remove'}]
    s=extract(event(endringer=changes));assert len(s.claims)==1
    value=s.claims[0].value
    assert value['changed_fields']==[{'path':c['path'],'operation':c['op']} for c in changes]
    assert value['new_value']=='Name' and 'old_value' not in value
    assert len(s.claims[0].evidence_ids)==11


@pytest.mark.parametrize('kind',['Ny','Endring','Sletting'])
def test_subunit_events_require_current_exact_parent_for_all_types(kind):
    e=event(organisasjonsnummer=OTHER,endringstype=kind,endringer=[])
    proof=extract(event()).evidence[0]
    s=rc.extract(e,response({'event':e}),' /event'.strip(),ORG,'underenheter',
        {OTHER:({'overordnetEnhet':ORG},proof)})
    assert s.claims[0].value['subunit_orgnr']==OTHER and proof.id in s.claims[0].evidence_ids
    assert not rc.extract(e,response(e),'/event',ORG,'underenheter',{}).claims
    with pytest.raises(Exception,match='registry_change_wrong_parent'):
        rc.extract(e,response(e),'/event',ORG,'underenheter',{OTHER:({'overordnetEnhet':OTHER},proof)})


def execute_events(tmp_path,total=65,previous=None,subunit=False):
    cfg=config(tmp_path,[ORG],registry_changes=True,previous=previous)
    requests=[]
    def source(request):
        requests.append(str(request.url))
        if '/oppdateringer/' in request.url.path:
            is_sub=request.url.path.endswith('/underenheter')
            records=([event(organisasjonsnummer=OTHER,oppdateringsid=100,dato='2026-10-01T12:30:00Z',endringstype='Endring',endringer=[])] if is_sub else
                [event(oppdateringsid=i+1,dato=f'2026-09-{1+i%28:02}T12:30:00Z',endringer=[] if i%2 else
                    [{'op':'replace','path':'/antallAnsatte','value':i}]) for i in range(total)])
            return httpx.Response(200,json={'page':{'number':0,'size':1000,'totalElements':len(records),'totalPages':1 if records else 0},
                '_embedded':{'oppdaterteUnderenheter' if is_sub else 'oppdaterteEnheter':records}})
        if subunit and '/underenheter' in request.url.path:
            return httpx.Response(200,json={'page':{'totalPages':1},'_embedded':{'underenheter':[
                {'organisasjonsnummer':OTHER,'overordnetEnhet':ORG,'navn':'Branch'}]}})
        return handler()(request)
    async def go():
        async with httpx.AsyncClient(transport=httpx.MockTransport(source)) as client:
            return await run(cfg,client)
    report=asyncio.run(go())
    row=json.loads(cfg.output.read_text(encoding='utf8').splitlines()[0])
    return cfg,report,row,requests


def test_cap_newest_order_no_extra_requests_full_raw_verification(tmp_path):
    cfg,report,row,requests=execute_events(tmp_path,subunit=True)
    events=[c for c in row['claims'] if c['field'].startswith(rc.PREFIX)]
    assert len(events)==50
    assert [c['value']['date'] for c in events]==sorted((c['value']['date'] for c in events),reverse=True)
    assert row['run']['refresh']['registry_activity']['events_returned']==66
    assert row['run']['refresh']['registry_activity']['truncated']
    assert sum('/oppdateringer/' in u for u in requests)==2
    assert any(c['value'].get('subunit_orgnr')==OTHER for c in events)
    assert verify(cfg.output,cfg.state_dir,1,cfg.organisations,cfg.report)['registry_events_verified']==50


def test_refresh_idempotence_with_full_event_cap(tmp_path):
    first,_,a,_=execute_events(tmp_path/'first')
    second,report,b,_=execute_events(tmp_path/'second',previous=first.output)
    assert report['changes']==report['observation_changes']==0
    assert [c['id'] for c in a['claims']]==[c['id'] for c in b['claims']]
    assert verify(second.output,second.state_dir,1,second.organisations,second.report)['registry_events_verified']==50


@pytest.mark.parametrize('target',['event_type','title','changed_fields'])
def test_generic_events_are_not_upgraded_to_specific_change_and_raw_tampering_fails(tmp_path,target):
    cfg,_,row,_=execute_events(tmp_path,total=1)
    c=next(c for c in row['claims'] if c['field'].startswith(rc.PREFIX))
    assert c['value']['title']=='Registry record updated'
    c['value'][target]={'event_type':'Sletting','title':'Registered name changed',
        'changed_fields':[{'path':'/invented','operation':'remove'}]}[target]
    from signalpost.synthesis.template import generate
    model=Envelope.model_validate(row);model.run.synthesis=generate(model);model.profile.synthesis=model.run.synthesis
    cfg.output.write_text(json.dumps(model.model_dump(mode='json'))+'\n',encoding='utf8')
    with pytest.raises(AssertionError):
        verify(cfg.output,cfg.state_dir,1,cfg.organisations,cfg.report)


def test_significant_recent_prefers_substantive_event_without_inventing_date():
    generic=extract(event(oppdateringsid=1,dato='2026-10-15T00:00:00Z',endringer=[])).claims[0]
    material=extract(event(oppdateringsid=2,dato='2026-10-01T00:00:00Z')).claims[0]
    old=extract(event(oppdateringsid=3,dato='2025-01-01T00:00:00Z',endringstype='Sletting')).claims[0]
    assert rc.significant_recent([generic,material,old])==material
    assert material.value['date']=='2026-10-01T00:00:00Z'


def test_partial_refresh_cannot_exceed_cap_or_duplicate_events():
    env=envelope()
    sections=[extract(event(oppdateringsid=i+1)) for i in range(60)]
    env.claims=[c for section in sections for c in section.claims]
    rc.cap_envelope(env)
    assert len(env.claims)==50 and len({c.field for c in env.claims})==50
    assert [c.value['event_id'] for c in env.claims]==list(range(60,10,-1))


def test_event_cards_keep_receipts_in_local_payload_without_repeating_long_batch_urls(tmp_path):
    from signalpost.site import fact,company_payload,normalize
    cfg,_,row,_=execute_events(tmp_path,total=1)
    claim=next(c for c in row['claims'] if c['field'].startswith(rc.PREFIX))
    records={e['id']:e for e in row['evidence']}
    page=fact(claim,records)
    assert 'Registry event' in page and 'Check the evidence' in page
    assert claim['value']['url'] in page.replace('&amp;','&')
    payload=company_payload(normalize(row))
    item=next(f for f in payload['facts'] if f['id']==claim['id'][:16])
    assert item['evidence_ids']==claim['evidence_ids']
    assert len(payload['records'])>=len(claim['evidence_ids'])


def test_partial_refresh_prefers_current_complete_event_over_carried_legacy_field_frames():
    env=envelope();current=extract(event()).claims[0]
    old=current.model_copy(deep=True)
    old.field=rc.PREFIX+'legacy-field';old.id='legacy-id';old.carried_forward=True
    old.value.pop('changed_fields');old.value.pop('record_orgnr')
    env.claims=[old,current]
    rc.cap_envelope(env)
    assert env.claims==[current]
