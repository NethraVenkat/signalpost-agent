from signalpost.portable_paths import expand, portable, portable_text  # saved paths stay repo-relative
import json,datetime,sys,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[3]
if str(root) not in sys.path:sys.path.insert(0,str(root))
from signalpost.models.envelope import Envelope
from signalpost.refresh.diff import apply
from signalpost.sources.blobstore import BlobStore
from signalpost.synthesis.template import generate
from signalpost.site import generate_site
from scripts.verify_output import verify
a=root/'.data/r5/stageE-frozen-run-final';b=root/'.data/r5/stageE-frozen-live-refresh'
out=Path(expand(sys.argv[1])).resolve() if len(sys.argv)>1 else root/'.data/r5/stageE-fullpair-offline';out.mkdir(exist_ok=False)
old={r['organisation_number']:r for r in map(json.loads,(a/'envelopes.jsonl').read_text(encoding='utf8').splitlines())}
rows=list(map(json.loads,(b/'envelopes.jsonl').read_text(encoding='utf8').splitlines()))
original=[c for r in rows for c in r['changes']]
for c in original:
 assert c['field'].startswith('registry_change.')
 x=dict(c['old_value']);y=dict(c['new_value']);xd=x.pop('date');yd=y.pop('date')
 assert x==y and datetime.datetime.fromisoformat(xd.replace('Z','+00:00'))==datetime.datetime.fromisoformat(yd.replace('Z','+00:00'))
fixed=[]
for row in rows:
 env=Envelope.model_validate(row);env.changes=[]
 apply(env,old[env.organisation_number],BlobStore(b/'state'))
 env.run.synthesis=generate(env);env.profile.synthesis=env.run.synthesis
 fixed.append(env.model_dump(mode='json'))
assert not any(r['changes'] for r in fixed)
output=out/'envelopes.jsonl';output.write_text(portable_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in fixed)),encoding='utf8')
site=generate_site(output,out/'site')
verification=verify(output,b/'state',100,root/'reports/r5/baseline/companies.jsonl',b/'report.json')
result={'scope':'Offline re-comparison of the exact saved 100-company live pair; no network, no edited publisher bytes',
 'input_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (a/'envelopes.jsonl',b/'envelopes.jsonl')},'previous':str(a/'envelopes.jsonl'),'current':str(b/'envelopes.jsonl'),'original_false_minor_changes':len(original),'all_original_differences_are_equivalent_aware_instants':True,
 'corrected_changes':0,'coverage_observations':sum(len(r['run']['refresh']['observation_changes']) for r in fixed),'site':site,'verification':verification}
(root/'reports/r5/stageE/saved_live_pair_replay.json').write_text(portable_text(json.dumps(result,indent=2)+'\n'),encoding='utf8')
print(json.dumps(result))
