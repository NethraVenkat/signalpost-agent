import asyncio,copy,hashlib,json
from pathlib import Path
from types import SimpleNamespace
import httpx
import pytest
from signalpost.sources import status_events as se
from signalpost.sources.http import Response
from signalpost.sources.extract import Section
from signalpost.budget import SourceFailure,Budget
from signalpost.sources.blobstore import BlobStore
from tests.test_registry import config,execute,handler
ORG='923609016'
URL=se.ENDPOINT+'?organisasjonsnummer='+ORG+'&includeChanges=true'


def event(code='Endring',**extra):
 return {'organisasjonsnummer':ORG,'oppdateringsid':123,'dato':'2026-11-19T12:01:02Z','endringstype':code,**extra}


def response(doc):
 raw=json.dumps(doc,ensure_ascii=False,separators=(',',':')).encode()
 return Response(raw,200,URL,'2026-11-20T00:00:00Z',hashlib.sha256(raw).hexdigest())


@pytest.mark.parametrize('code,label',list(se.LABELS.items()))
def test_documented_code_labels_and_own_scalar_receipts(code,label):
 raw=event(code);r=response({'event':raw});s=se.extract(ORG,raw,r,'/event');c=s.claims[0]
 assert c.value['label']==label and c.value['change_type']==code
 assert c.value['date_scope']=='API publication time; not legal effective date'
 assert len(c.evidence_ids)==4 and all(e.extraction_method==se.METHOD for e in s.evidence)
 for e in s.evidence:
  assert e.source_url==URL and e.retrieved_at.endswith('Z') and e.content_sha256==r.sha
  assert e.locator.startswith('/event/') and e.claim_span in r.body.decode()
 assert se.verify(ORG,{'claims':[c.model_dump(mode='json')]},{e.id:e.model_dump(mode='json') for e in s.evidence},lambda h:r.body.decode())==1


def test_unknown_code_remains_neutral_no_dissolution_inference():
 raw=event('UNPUBLISHED_CODE');s=se.extract(ORG,raw,response({'event':raw}),'/event')
 assert s.claims[0].value['label']=='Registry change event (undocumented code)'
 assert s.claims[0].value['documented_type'] is False
 assert s.claims[0].value['change_type']=='UNPUBLISHED_CODE'


def test_status_patch_values_are_explicit_and_do_not_copy_names_or_text():
 raw=event(endringer=[{'op':'replace','path':'/underAvvikling','value':True},
                      {'op':'replace','path':'/konkursdato','value':'2026-11-19'},
                      {'op':'replace','path':'/navn','value':'PRIVATE TEXT'},
                      {'op':'replace','path':'/slettedato','value':'PRIVATE TEXT'}])
 s=se.extract(ORG,raw,response({'event':raw}),'/event');c=s.claims[0]
 assert len(c.value['status_field_changes'])==2 and 'PRIVATE TEXT' not in json.dumps(c.value)
 assert all(x['label']=='Registered status field changed' for x in c.value['status_field_changes'])
 assert len(c.evidence_ids)==10


def test_wrong_owner_and_tampered_status_or_receipts_are_rejected():
 raw=event();r=response({'event':raw});s=se.extract(ORG,raw,r,'/event')
 with pytest.raises(SourceFailure):se.extract('984851006',raw,r,'/event')
 c=s.claims[0].model_dump(mode='json');ev={e.id:e.model_dump(mode='json') for e in s.evidence}
 c['value']['label']='Dissolution announced'
 with pytest.raises(AssertionError):se.verify(ORG,{'claims':[c]},ev,lambda h:r.body.decode())
 c=s.claims[0].model_dump(mode='json');c['evidence_ids']=c['evidence_ids'][:-1]
 with pytest.raises(AssertionError):se.verify(ORG,{'claims':[c]},ev,lambda h:r.body.decode())


def test_saved_projection_reuses_blobs_no_http_and_marks_upstream_failure(tmp_path):
 from signalpost.sources.registry_changes import extract
 raw=event('Sletting');r=response({'event':raw});section=extract(raw,r,'/event',ORG,'enheter')
 blobs=BlobStore(tmp_path);blobs.put(r.body)
 result=se.from_activity(ORG,section,blobs)
 assert result.state=='available' and len(result.claims)==1
 assert result.claims[0].value['status_scope'].startswith('Registry deletion')
 section.state='failed';result=se.from_activity(ORG,section,blobs)
 assert result.state=='failed' and result.claims and result.errors[0].code=='status_event_upstream_incomplete'
 missing=se.from_activity(ORG,section,SimpleNamespace(read=lambda h:None))
 assert missing.state=='failed' and not missing.claims


@pytest.mark.parametrize('statuses,allow',[(['reset',200],True),(['reset']*5,False),([404],True),([503]*5,False),([200],False)])
def test_direct_live_preflight_robots_rfc9309_and_outage_abort(tmp_path,monkeypatch,statuses,allow):
 from signalpost.sources import exact_public
 async def no_wait(*a,**k):pass
 monkeypatch.setattr(exact_public,'pause',no_wait)
 cfg=config(tmp_path,[ORG],registry_changes=False);budget=Budget(cfg);blobs=BlobStore(tmp_path/'blobs-root');calls=[];robots=[]
 def dispatch(req):
  calls.append(str(req.url))
  if req.url.path=='/robots.txt':
   value=statuses[min(len(robots),len(statuses)-1)];robots.append(value)
   if value=='reset':raise httpx.ConnectError('reset',request=req)
   return httpx.Response(value,text='User-agent: *\nAllow: /' if allow else 'User-agent: *\nDisallow: /')
  return httpx.Response(200,json={'_embedded':{'oppdaterteEnheter':[event()]}})
 async def run():
  async with httpx.AsyncClient(transport=httpx.MockTransport(dispatch)) as client:
   return await se.fetch_live(ORG,SimpleNamespace(client=client,config=cfg,budget=budget,blobs=blobs))
 result=asyncio.run(run())
 assert result.state==('available' if allow else 'blocked')
 assert all(x.startswith('https://data.brreg.no/') for x in calls)
 assert sum('/oppdateringer/' in x for x in calls)==int(allow)
 assert len(robots)==len(statuses)
 if not allow:assert result.errors and not result.claims


def test_runner_projects_entity_events_without_additional_requests(tmp_path):
 baseline=handler();calls=[]
 def dispatch(req):
  calls.append(str(req.url))
  if '/oppdateringer/enheter' in req.url.path:
   return httpx.Response(200,json={'_embedded':{'oppdaterteEnheter':[event()]},'page':{'number':0,'totalPages':1,'totalElements':1,'size':1000}})
  if '/oppdateringer/roller' in req.url.path:return httpx.Response(200,json=[])
  if '/oppdateringer/' in req.url.path:
   key='oppdaterteUnderenheter' if req.url.path.endswith('underenheter') else 'oppdaterteRoller'
   return httpx.Response(200,json={'_embedded':{key:[]},'page':{'number':0,'totalPages':0,'totalElements':0,'size':1000}})
  return baseline(req)
 cfg=config(tmp_path,[ORG],registry_changes=True)
 report,rows=execute(cfg,dispatch);r=rows[0]
 assert r['run']['sections']['status_events']=='available'
 assert len([c for c in r['claims'] if c['family']=='status_events' and c['availability']=='available'])==1
 assert len([u for u in calls if '/oppdateringer/enheter' in u])==1
 assert not any('/robots.txt' in u for u in calls) # no direct status HTTP


def test_failed_feed_never_leaves_status_complete(tmp_path):
 baseline=handler()
 def dispatch(req):
  if '/oppdateringer/' in req.url.path:raise SourceFailure('network_error')
  return baseline(req)
 report,rows=execute(config(tmp_path,[ORG],registry_changes=True),dispatch)
 assert rows[0]['run']['sections']['status_events']=='failed'
 assert rows[0]['modules']['status_events']['state']!='complete'
 assert report['run_status']!='complete'


def test_saved_real_header_projections_replay_without_names():
 fixture=json.loads((Path(__file__).parent/'fixtures/status_events_headers.json').read_text(encoding='utf8'))
 assert fixture['items']
 for item in fixture['items']:
  raw=item['event'];org=raw['organisasjonsnummer'];body=json.dumps({'event':raw},ensure_ascii=False,separators=(',',':')).encode()
  r=Response(body,200,item['original_source_url'],item['retrieved_at'],hashlib.sha256(body).hexdigest())
  result=se.extract(org,raw,r,'/event')
  assert result.claims[0].value['change_type']==raw['endringstype']
  assert result.claims[0].value['date']==raw['dato']
  for e in result.evidence:
   # Every new evidence span is exactly one scalar token, never neighbouring
   # company/person names from the saved source record.
   assert json.loads(e.claim_span) in [org,raw['oppdateringsid'],raw['dato'],raw['endringstype']] or '/endringer/' in e.locator


def test_status_facts_always_defer_to_local_payload_without_loss(tmp_path):
 from signalpost.site import generate_site,company_payload,deferred_claims
 from signalpost.runner import placeholder,update
 from signalpost.models.evidence import utc_now
 envelope=placeholder(ORG,'s1-test',utc_now(),families=('status_events',))
 section=Section()
 for i in range(100):
  raw=event(oppdateringsid=i+1);part=se.extract(ORG,raw,response({'event':raw}),'/event')
  section.claims.extend(part.claims);section.evidence.extend(part.evidence)
 update(envelope,'status_events',section);envelope.run.terminal_status='completed'
 row=envelope.model_dump(mode='json')
 assert deferred_claims(row['claims'])=={c['id'] for c in row['claims']}
 payload=company_payload(row)
 assert len(payload['registry_details'])==100 and all(x['group']=='activity' for x in payload['registry_details'])
 assert {x['id'] for x in payload['facts']}=={c['id'][:16] for c in row['claims']}
 path=tmp_path/'saved.jsonl';path.write_text(envelope.model_dump_json()+'\n',encoding='utf8')
 result=generate_site(path,tmp_path/'site')
 assert result['largest_profile_bytes']<250000
