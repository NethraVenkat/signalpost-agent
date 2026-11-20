"""Offline claim-only S2 replay over the S1 derived final500e envelopes."""
import hashlib,json,statistics,sys,time
from pathlib import Path
from signalpost.synthesis.timeline import for_row,DATED_FIELDS
from signalpost.site import generate_site
ROOT=Path(__file__).resolve().parents[3]
DEST=Path(__file__).resolve().parent
SOURCE=ROOT/'out/status-events-500/envelopes.jsonl'
OUT=ROOT/'out/dated-timeline-500'
assert not OUT.exists();OUT.mkdir()
def offline(event,args):
 if event in {'socket.connect','socket.getaddrinfo','socket.sendto','socket.gethostbyname'}:raise RuntimeError('Timeline replay cannot access network')
sys.addaudithook(offline)
raw=SOURCE.read_bytes();original=hashlib.sha256(raw).hexdigest();rows=[json.loads(l) for l in raw.decode('utf8').splitlines()];start=time.perf_counter();sizes=[]
for row in rows:
 claim_before=json.dumps(row['claims'],sort_keys=True,ensure_ascii=False);evidence_before=json.dumps(row['evidence'],sort_keys=True,ensure_ascii=False)
 timeline=for_row(row);sizes.append(len(timeline))
 synthesis=row['run'].get('synthesis')
 if synthesis:synthesis.setdefault('sections',{})['timeline']=timeline
 assert json.dumps(row['claims'],sort_keys=True,ensure_ascii=False)==claim_before
 assert json.dumps(row['evidence'],sort_keys=True,ensure_ascii=False)==evidence_before
projection=time.perf_counter()-start
p=OUT/'envelopes.jsonl';p.write_text(''.join(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n' for row in rows),encoding='utf8',newline='\n')
start=time.perf_counter();site=generate_site(p,OUT/'site');render=time.perf_counter()-start
assert site['largest_profile_bytes']<250000 and original==hashlib.sha256(SOURCE.read_bytes()).hexdigest()
result={'source_scope':'S1 offline derived final500e cohort; not a new live measurement','source_sha256':original,'original_unchanged':True,'companies':len(rows),'companies_with_timeline':sum(n>0 for n in sizes),'median_entries_all_companies':statistics.median(sizes),'median_entries_with_timeline':statistics.median([n for n in sizes if n]),'entry_counts':sizes,'total_entries':sum(sizes),'projection_seconds':projection,'offline_render_seconds':render,'site':site,'additional_http_requests':0,'additional_claims':0,'additional_evidence':0,'network_disabled':True,'dated_fields':DATED_FIELDS}
(DEST/'measurement.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n');print(json.dumps({k:v for k,v in result.items() if k not in {'entry_counts','dated_fields'}}),flush=True)
