"""Fresh six-sample seven-flag measurements; preserves all raw run state."""
from signalpost.portable_paths import expand, portable, portable_text, sanitize_file  # saved paths stay repo-relative
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone

from declared_audit import ROOT, SEEDS, records, save, sites


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    stage=sys.argv[1]
    assert stage in {'stageR5','stageR3'}
    dest=ROOT/'reports/r5'/stage;dest.mkdir(exist_ok=True)
    manifest={p.relative_to(ROOT).as_posix():sha(p) for p in sorted((ROOT/'src').rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
    save(dest/'source_manifest.json',manifest)
    env=os.environ.copy();env.update(PYTHONUTF8='1',SIGNALPOST_SEARCH_PROVIDER='disabled',SIGNALPOST_SEARCH_MOCK='0')
    chosen=set(map(int,sys.argv[2:]))
    for seed in SEEDS:
        if chosen and seed not in chosen:continue
        old_settings,old_work,registry,before,old_report=records('stageW' if stage=='stageR5' else 'stageR5',seed)
        original=old_settings['command_argv']
        organisations=Path(expand(original[original.index('--organisations')+1]));bulk=Path(expand(original[original.index('--bulk')+1]))
        label='release-proof-final'
        out=ROOT/'.data/r5'/f'{stage}-{seed}-{label}';out.mkdir(exist_ok=False)
        folder=dest/f'seed{seed}';folder.mkdir(exist_ok=True)
        argv=[sys.executable,'-m','signalpost.cli','run']
        for key,value in {'organisations':organisations,'bulk':bulk,'output':out/'envelopes.jsonl','profiles-output':out/'profiles.jsonl',
                          'report':out/'report.json','run-id':f'r5-{stage}-seed{seed}-{label}','expected-count':100}.items():
            argv.extend(['--'+key,str(value)])
        assert sum(a.startswith('--') for a in argv)==7
        save(folder/'settings.json',{'seed':seed,'working_directory':str(out),'command_argv':argv,'exact_seven_flags':True,
            'input_sha256':sha(organisations),'bulk_sha256':sha(bulk),'source_manifest_sha256':sha(dest/'source_manifest.json'),
            'parent_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'previous_working_directory':str(old_work)})
        print('Starting',stage,seed,datetime.now(timezone.utc).isoformat(),flush=True)
        started=time.monotonic()
        with (folder/'execution.txt').open('w',encoding='utf8',newline='\n') as log:
            result=subprocess.run(argv,cwd=out,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=2160)
        sanitize_file(folder/'execution.txt')  # keep captured paths repo-relative
        execution={'exit_code':result.returncode,'wall_seconds':time.monotonic()-started,'argv':argv,'cwd':str(out)}
        save(folder/'execution.json',execution)
        if result.returncode:raise RuntimeError(f'{seed}: CLI exit {result.returncode}')
        checked=subprocess.run([sys.executable,str(ROOT/'scripts/check_live_run.py'),'--output',str(out/'envelopes.jsonl'),'--organisations',str(organisations),
            '--state',str(out/'state'),'--report',str(out/'report.json'),'--site',str(out/'site'),'--count','100'],cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf8')
        (folder/'verification.txt').write_text(portable_text(checked.stdout+checked.stderr),encoding='utf8',newline='\n')
        if checked.returncode:raise RuntimeError(f'{seed}: independent verification failed')
        save(folder/'verification.json',json.loads(checked.stdout))
        shutil.copyfile(out/'report.json',folder/'report.json')
        rows=[json.loads(s) for s in (out/'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
        report=json.loads((out/'report.json').read_text(encoding='utf8'))
        def values(rs):return {r['organisation_number']:sites(r)[0]['value'] for r in rs if sites(r)}
        old,new=values(before),values(rows)
        declared={r['organisation_number'] for r in rows if any(c['field']=='identity.registered_website' and c['availability']=='available' for c in r['claims'])}
        counts={'seed':seed,'websites_before':len(old),'websites_after':len(new),
            'declared_homepages':len(declared),'declared_recall_before':len(declared&old.keys()),'declared_recall_after':len(declared&new.keys()),
            'tier_counts':dict(Counter(v['proof_type'] for v in new.values())),
            'http_before':old_report['requests'],'http_after':report['requests'],'runtime_seconds':execution['wall_seconds'],'cost_usd':report['total_cost_usd'],
            'changes':{'added':{o:new[o] for o in new.keys()-old.keys()},'removed':{o:old[o] for o in old.keys()-new.keys()},
                'url_changed':{o:{'before':old[o],'after':new[o]} for o in old.keys()&new.keys() if old[o]['final_url']!=new[o]['final_url']}},
            'envelopes_sha256':sha(out/'envelopes.jsonl'),'profiles_sha256':sha(out/'profiles.jsonl')}
        save(folder/'counts.json',counts)
        assert manifest=={p.relative_to(ROOT).as_posix():sha(p) for p in sorted((ROOT/'src').rglob('*')) if p.is_file() and '__pycache__' not in p.parts},'Source changed during measurement'
        print('Completed',stage,seed,json.dumps(counts,ensure_ascii=True),flush=True)


if __name__=='__main__':main()
