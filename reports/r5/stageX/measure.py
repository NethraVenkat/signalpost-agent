"""Sequential, fresh seven-flag qualification for X and R6 items."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
SEEDS=(20261017,20261113,20261114,20261115,20261116,20261117)
ORDER=('X1','X4','R6','R7','X2')


def save(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def folder(stage):return ROOT/'reports/r5'/('stage'+stage if stage in {'R6','R7'} else 'stageX')/stage


def manifest():
    return {p.relative_to(ROOT).as_posix():sha(p) for p in sorted((ROOT/'src').rglob('*')) if p.is_file() and '__pycache__' not in p.parts}


def counts(rows):
    available=lambda r:[c for c in r['claims'] if c['availability']=='available']
    isbrand=lambda c:c['field']=='public_brand' or c['field'].startswith('brand.')
    sites={r['organisation_number'] for r in rows if any(c['field']=='official_website' for c in available(r))}
    declared={r['organisation_number'] for r in rows if any(c['field']=='identity.registered_website' for c in available(r))}
    return {'websites':len(sites),'declared_homepage_recall':len(sites&declared),'declared_homepages':len(declared),
        'social_companies':sum(any(c['field'].startswith('social_profile.') for c in available(r)) for r in rows),
        'social_claims':sum(c['field'].startswith('social_profile.') for r in rows for c in available(r)),
        'activity_companies':sum(any(c['family']=='activity' for c in available(r)) for r in rows),
        'activity_claims':sum(c['family']=='activity' for r in rows for c in available(r)),
        'brand_companies':sum(any(isbrand(c) for c in available(r)) for r in rows),
        'brand_claims':sum(isbrand(c) for r in rows for c in available(r)),
        'role_change_claims':sum(c['field'].startswith('registry_change.roles.') for r in rows for c in available(r)),
        'facts':sum(len(available(r)) for r in rows),
        'families':dict(Counter(c['family'] for r in rows for c in available(r)))}


def identities(rows):
    items={}
    for row in rows:
        name=next((c['value'] for c in row['claims'] if c['field']=='identity.legal_name' and c['availability']=='available'),None)
        evidence={e['id']:e for e in row['evidence']}
        for c in row['claims']:
            if c['availability']!='available':continue
            field=c['field'];v=c['value']
            kind='website' if field=='official_website' else 'social' if field.startswith('social_profile.') else 'brand' if field=='public_brand' or field.startswith('brand.') else None
            if not kind:continue
            key=v['final_url'] if kind=='website' else v['url'] if kind=='social' else v if isinstance(v,str) else v.get('name') or v.get('brand')
            stable=(row['organisation_number'],kind,str(key))
            items[stable]={'orgnr':row['organisation_number'],'legal_name':name,'kind':kind,'identity':key,'field':field,'value':v,
                'evidence':[evidence[e] for e in c['evidence_ids']]}
    return items


def main():
    stage=sys.argv[1];assert stage in ORDER
    chosen=set(map(int,sys.argv[2:]))
    label=os.environ.get('SIGNALPOST_MEASUREMENT_LABEL','final')
    assert label in {'final','source-recovery','resume-final','unattended','unattended-retry','outage-retry','qualification-final'}
    dest=folder(stage);dest.mkdir(parents=True,exist_ok=True)
    source=manifest();save(dest/'source_manifest.json',source)
    env=os.environ.copy();env.update(PYTHONUTF8='1',SIGNALPOST_SEARCH_PROVIDER='disabled',SIGNALPOST_SEARCH_MOCK='0')
    previous=ORDER[ORDER.index(stage)-1] if stage!='X1' else None
    for seed in SEEDS:
        if chosen and seed not in chosen:continue
        oldfolder=folder(previous)/f'seed{seed}' if previous else ROOT/f'reports/r5/stageR3/seed{seed}'
        oldsettings=json.loads((oldfolder/'settings.json').read_text(encoding='utf8'));oldargv=oldsettings['command_argv']
        orgs=Path(oldargv[oldargv.index('--organisations')+1]);bulk=Path(oldargv[oldargv.index('--bulk')+1])
        oldwork=Path(oldsettings['working_directory']);oldrows=[json.loads(s) for s in (oldwork/'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
        work=ROOT/'.data/r5'/f'stage{stage}-{seed}-{label}';work.mkdir(exist_ok=False)
        output=dest/f'seed{seed}';output.mkdir(exist_ok=label!='final')
        argv=[sys.executable,'-m','signalpost.cli','run']
        for key,value in {'organisations':orgs,'bulk':bulk,'output':work/'envelopes.jsonl','profiles-output':work/'profiles.jsonl',
            'report':work/'report.json','run-id':f'r5-stage{stage}-seed{seed}-{label}','expected-count':100}.items():argv.extend(['--'+key,str(value)])
        assert sum(a.startswith('--') for a in argv)==7
        save(output/'settings.json',{'seed':seed,'stage':stage,'working_directory':str(work),'command_argv':argv,'exact_seven_flags':True,
            'input_sha256':sha(orgs),'bulk_sha256':sha(bulk),'previous_working_directory':str(oldwork),'source_manifest_sha256':sha(dest/'source_manifest.json'),
            'parent_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()})
        print('Starting',stage,seed,flush=True);started=time.monotonic()
        with (output/'execution.txt').open('w',encoding='utf8',newline='\n') as log:
            executed=subprocess.run(argv,cwd=work,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=2160)
        save(output/'execution.json',{'exit_code':executed.returncode,'wall_seconds':time.monotonic()-started,'argv':argv,'cwd':str(work)})
        assert executed.returncode==0
        checked=subprocess.run([sys.executable,str(ROOT/'scripts/check_live_run.py'),'--output',str(work/'envelopes.jsonl'),'--organisations',str(orgs),
            '--state',str(work/'state'),'--report',str(work/'report.json'),'--site',str(work/'site'),'--count','100'],cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf8')
        (output/'verification.txt').write_text(checked.stdout+checked.stderr,encoding='utf8',newline='\n');assert checked.returncode==0
        verification=json.loads(checked.stdout);save(output/'verification.json',verification)
        shutil.copyfile(work/'report.json',output/'report.json')
        rows=[json.loads(s) for s in (work/'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
        report=json.loads((work/'report.json').read_text(encoding='utf8'))
        assert report['site']['state']=='available' and report['site']['largest_profile_bytes']<250000,'Site size gate failed'
        old,new=identities(oldrows),identities(rows)
        result={'stage':stage,'seed':seed,'before':counts(oldrows),'after':counts(rows),'HTTP':report['requests'],
            'runtime_seconds':time.monotonic()-started,'CLI_runtime_seconds':json.loads((output/'execution.json').read_text())['wall_seconds'],
            'cost_usd':report['total_cost_usd'],'site':report['site'],
            'changes':{'added':[new[k] for k in new.keys()-old.keys()],'removed':[old[k] for k in old.keys()-new.keys()]},
            'envelopes_sha256':sha(work/'envelopes.jsonl'),'profiles_sha256':sha(work/'profiles.jsonl')}
        save(output/'counts.json',result)
        assert source==manifest(),'Runtime source changed during measurement'
        print('Completed',stage,seed,json.dumps({k:result[k] for k in ('after','HTTP','CLI_runtime_seconds','site')}),flush=True)


if __name__=='__main__':main()
