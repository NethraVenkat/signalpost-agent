"""Explicit user-authorized --previous exception to the seven-flag live check."""
import json,os,subprocess,sys,time,hashlib
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[3]

def main():
    dest=ROOT/'reports/r5/stageE/live_refresh';dest.mkdir(parents=True,exist_ok=True)
    previous_settings=json.loads((ROOT/'reports/r5/stageE/frozen/settings.json').read_text(encoding='utf8'))
    previous=Path(previous_settings['working_directory'])/'envelopes.jsonl'
    assert previous.exists()
    attempt=sys.argv[1] if len(sys.argv)>1 else None
    if attempt:assert attempt.isalnum()
    out=ROOT/('.data/r5/stageE-frozen-live-refresh'+('-'+attempt if attempt else ''))
    if out.exists():raise ValueError('Fresh state required')
    out.mkdir(parents=True)
    argv=[sys.executable,'-m','signalpost.cli','run']
    flags={'organisations':ROOT/'reports/r5/baseline/companies.jsonl','bulk':ROOT/'reports/r5/baseline/registry100.csv',
        'output':out/'envelopes.jsonl','profiles-output':out/'profiles.jsonl','report':out/'report.json',
        'run-id':'r5-stageE-frozen-live-refresh'+('-'+attempt if attempt else ''),'expected-count':100,'previous':previous}
    for k,v in flags.items():argv+=['--'+k,str(v)]
    env=os.environ.copy();env.update(PYTHONUTF8='1',SIGNALPOST_SEARCH_PROVIDER='disabled',SIGNALPOST_SEARCH_MOCK='0')
    metadata={'argv':argv,'cwd':str(out),'previous':str(previous),'previous_sha256':hashlib.sha256(previous.read_bytes()).hexdigest(),
        'flag_exception':'Seven evaluator flags plus --previous, explicitly requested for live refresh; no feature/cap/time flags',
        'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()}
    source_manifest={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'src').rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
    (dest/'source_manifest.json').write_text(json.dumps(source_manifest,indent=2)+'\n',encoding='utf8')
    metadata['source_manifest_sha256']=hashlib.sha256((dest/'source_manifest.json').read_bytes()).hexdigest()
    (dest/'settings.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf8')
    began=time.perf_counter()
    with (dest/'process.txt').open('w',encoding='utf8') as log:r=subprocess.run(argv,cwd=out,env=env,stdout=log,stderr=subprocess.STDOUT)
    execution={'exit_code':r.returncode,'wall_seconds':time.perf_counter()-began}
    (dest/'execution.json').write_text(json.dumps(execution,indent=2)+'\n',encoding='utf8');r.check_returncode()
    # Archived proof bodies are immutable verification inputs, not current
    # runtime caches. Add only missing evidence bodies after the live run.
    rows=[json.loads(x) for x in (out/'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
    copied=0
    for row in rows:
        for e in row['evidence']:
            sha=e['content_sha256'];target=out/'state/blobs'/sha;source=previous.parent/'state/blobs'/sha
            if not target.exists() and source.exists():
                body=source.read_bytes();assert hashlib.sha256(body).hexdigest()==sha;target.write_bytes(body);copied+=1
    cmd=[sys.executable,'scripts/verify_output.py','--first',str(out/'envelopes.jsonl'),'--organisations',str(flags['organisations']),
         '--count','100','--state-dir',str(out/'state'),'--report',str(out/'report.json')]
    v=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True,check=True);verified=json.loads(v.stdout)
    (dest/'verification.json').write_text(json.dumps({'argv':cmd,'exit_code':0,**verified},indent=2)+'\n',encoding='utf8')
    report=json.loads((out/'report.json').read_text(encoding='utf8'));assert report['requests']<=1850 and report['total_cost_usd']==0
    assert report['site']['state']=='available' and report['completion']['within_effective_time_budget']
    assert len(rows)==100 and execution['exit_code']==0
    changes=[{'orgnr':row['organisation_number'],**c} for row in rows for c in row['changes']]
    observations=[{'orgnr':row['organisation_number'],**c} for row in rows for c in row['run']['refresh'].get('observation_changes',[])]
    result={'http':report['requests'],'wall_seconds':execution['wall_seconds'],'cost_usd':0,'rows':100,
        'changes':len(changes),'material_changes':sum(c['materiality']=='material' for c in changes),
        'minor_changes':sum(c['materiality']=='minor' for c in changes),'change_types':dict(Counter(c['type'] for c in changes)),
        'coverage_observations':len(observations),'material_change_events':[c for c in changes if c['materiality']=='material'],
        'all_changes':changes,'observations':observations,'carried_claims':sum(c['carried_forward'] for row in rows for c in row['claims']),
        'previous_evidence_blobs_added_after_run_for_verification':copied,'verification':verified}
    (dest/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    (dest/'report.json').write_bytes((out/'report.json').read_bytes())
    print(json.dumps({k:v for k,v in result.items() if k not in ('all_changes','observations','material_change_events','verification')}))

if __name__=='__main__':main()
