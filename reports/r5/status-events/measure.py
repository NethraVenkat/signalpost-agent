"""Measure S1 on original final500e outputs offline; originals stay unchanged."""
import gzip,hashlib,json,socket,sys,time
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
from signalpost.models.envelope import Envelope
from signalpost.sources.extract import Section
from signalpost.sources.blobstore import BlobStore
from signalpost.sources import status_events as se
from signalpost.runner import update
from signalpost.site import generate_site

ROOT=Path(__file__).resolve().parents[3]
DEST=Path(__file__).resolve().parent
RUN=ROOT/'.data/r5-final500e/run'
WORK=ROOT/'out/status-events-500'


def main():
 assert not WORK.exists(),'One offline measurement destination; preserve prior results'
 WORK.mkdir()
 def offline(event,args):
  if event in {'socket.connect','socket.getaddrinfo','socket.sendto','socket.gethostbyname'}:raise RuntimeError('Offline S1 measurement')
 sys.addaudithook(offline)
 raw=(RUN/'envelopes.jsonl').read_bytes();original=hashlib.sha256(raw).hexdigest()
 assert original=='217314e5ec17ff29b13905ac264ee3a9fe2a8ff0051975670f825cfc61a27da9'
 rows=[Envelope.model_validate_json(line) for line in raw.decode('utf8').splitlines()]
 blobs=BlobStore(RUN/'state');cache={};counts=Counter();states=Counter();gained=[];per_company={};headers=[];header_ids=set();new_claims=0; specific=[]; status_paths=Counter()
 started=time.perf_counter()
 for envelope in rows:
  original_section=Section(state=envelope.run.sections.get('activity','failed'),
     claims=[c for c in envelope.claims if c.family=='activity'],evidence=envelope.evidence)
  result=se.from_activity(envelope.organisation_number,original_section,blobs,cache)
  states[result.state]+=1
  if result.claims:gained.append(envelope.organisation_number)
  per_company[envelope.organisation_number]=len(result.claims);new_claims+=len(result.claims)
  for c in result.claims:
   counts[c.value['change_type']]+=1
   if c.value['change_type'] in {'Sletting','Fjernet'} or c.value.get('status_field_changes'):specific.append((envelope.organisation_number,c.value['event_id']))
   for change in c.value.get('status_field_changes',[]):status_paths[change['path']]+=1
   e=next(e for e in result.evidence if e.id in c.evidence_ids and e.locator.endswith('/endringstype'))
   _,document=cache[e.content_sha256];event=se.pointer(document,e.locator.rsplit('/',1)[0])
   # Bounded saved-real-response header fixture: retain no names/addresses or
   # non-status change values. This is a projection, not original response bytes.
   if event['oppdateringsid'] not in header_ids and len(headers)<12:
    minimal={k:event[k] for k in ('organisasjonsnummer','oppdateringsid','dato','endringstype')}
    minimal['endringer']=[x for x in event.get('endringer',[]) if x.get('path') in se.STATUS_PATHS and (type(x.get('value'))is bool or x.get('op')=='remove' or isinstance(x.get('value'),str) and __import__('re').fullmatch(r'\d{4}-\d{2}-\d{2}',x['value']))]
    headers.append({'event':minimal,'original_source_url':e.source_url,'original_response_sha256':e.content_sha256,'retrieved_at':e.retrieved_at,'original_locator':e.locator.rsplit('/',1)[0]});header_ids.add(event['oppdateringsid'])
  update(envelope,se.FAMILY,result)
 projection_wall=time.perf_counter()-started
 verified=0;verify_started=time.perf_counter()
 for row in rows:
  data={'claims':[c.model_dump(mode='json') for c in row.claims if c.family==se.FAMILY]}
  evidence={e.id:e.model_dump(mode='json') for e in row.evidence}
  verified+=se.verify(row.organisation_number,data,evidence,lambda h:cache[h][0].decode('utf8'))
 verify_wall=time.perf_counter()-verify_started
 output=WORK/'envelopes.jsonl'
 output.write_text(''.join(row.model_dump_json()+'\n' for row in rows),encoding='utf8',newline='\n')
 rendered=time.perf_counter();site=generate_site(output,WORK/'site');render_wall=time.perf_counter()-rendered
 assert site['companies']==500 and site['largest_profile_bytes']<250000
 assert hashlib.sha256((RUN/'envelopes.jsonl').read_bytes()).hexdigest()==original
 metrics={'source_run_commit':'40813fe','source_envelopes_sha256':original,'original_unchanged':True,'network_disabled':True,'additional_http_requests':0,'companies':500,'companies_gaining_status_events':len(gained),'new_claims':new_claims,'specific_status_event_claims':len(specific),'companies_with_specific_status_events':len({org for org,ident in specific}),'status_path_counts':dict(status_paths),'verified_new_claims':verified,'change_type_counts':dict(counts),'section_states':dict(states),'per_company_claims':per_company,'gained_company_numbers':gained,'projection_wall_seconds':projection_wall,'new_claim_source_replay_seconds':verify_wall,'full_offline_render_seconds':render_wall,'site':site,'runtime_scope':'Projection-only wall is the measured extra transformation cost, not a live end-to-end runtime delta. No live rerun; no budget/finalisation changes.'}
 (DEST/'measurement.json').write_text(json.dumps(metrics,indent=2)+'\n',encoding='utf8',newline='\n')
 fixture=ROOT/'tests/fixtures/status_events_headers.json'
 fixture.write_text(json.dumps({'scope':'Saved real final500e header/status-field projections only; original hashes/locators retained for provenance, fixture is not a byte-identical publisher response','items':headers},indent=2)+'\n',encoding='utf8',newline='\n')
 print(json.dumps({k:v for k,v in metrics.items() if k not in {'per_company_claims','gained_company_numbers'}}),flush=True)

if __name__=='__main__':main()
