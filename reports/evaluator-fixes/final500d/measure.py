"""Single fresh 500-company run; prepare, run and finish are separate phases."""
import argparse
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import random
import shutil
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone

from signalpost.portable_paths import portable_text
from signalpost.identity.orgnr import valid

ROOT = Path(__file__).resolve().parents[3]
DEST = Path(__file__).resolve().parent
BASE = ROOT / '.data/evaluator-fixes-final500d'
CLONE = BASE / 'repo'
WORK = BASE / 'run'
PY = CLONE / '.venv/Scripts/python.exe'
SEED = 20261124
ENV = {k: v for k, v in os.environ.items() if not any(x in k.upper() for x in
       ('TOKEN', 'SECRET', 'PASSWORD', 'API_KEY', 'CREDENTIAL', 'AWS_', 'AZURE_', 'OPENAI_', 'ANTHROPIC_', 'BRAVE_'))}
ENV.pop('VIRTUAL_ENV', None)
ENV.update(PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1', SIGNALPOST_SEARCH_PROVIDER='disabled', SIGNALPOST_SEARCH_MOCK='0')


def save(name, value):
    (DEST / name).write_text(portable_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n'), encoding='utf8')


def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def git(*args, cwd=ROOT):
    return subprocess.check_output(['git', '-c', 'safe.directory='+str(cwd), *args], cwd=cwd, text=True).strip()


def command(name, args, cwd=ROOT, required=True):
    start = time.monotonic()
    p = subprocess.run(list(map(str, args)), cwd=cwd, env=ENV, capture_output=True, text=True, encoding='utf8', errors='replace')
    (DEST / (name+'.txt')).write_text(portable_text(p.stdout+p.stderr), encoding='utf8')
    result = dict(exit_code=p.returncode, wall_seconds=time.monotonic()-start, argv=list(map(str,args)), cwd=str(cwd))
    save(name+'.json', result)
    if required:assert p.returncode == 0, name+' failed; see receipt'
    return p.stdout


def prepare():
    assert not BASE.exists(), 'Fresh setup only; no reuse'
    free = shutil.disk_usage(ROOT).free
    save('disk_preflight.json', dict(free_bytes=free, required_bytes=15*1024**3, stop_below_bytes=3*1024**3,
         measured_at_utc=datetime.now(timezone.utc).isoformat()))
    assert free >= 15*1024**3, 'STOP: less than 15 GiB free'
    import httpx
    probes = []
    for url in ('https://data.brreg.no/enhetsregisteret/api/enheter?size=1',
                'https://data.brreg.no/regnskapsregisteret/regnskap',
                'https://pam-stilling-feed.nav.no/api/publicToken'):
        start = time.monotonic()
        try:
            with httpx.Client(timeout=15) as client:
                r = client.head(url)
            probes.append(dict(url=url, status=r.status_code, reachable=True, seconds=time.monotonic()-start))
        except httpx.HTTPError as e:
            probes.append(dict(url=url, error=type(e).__name__, reachable=False, seconds=time.monotonic()-start))
    save('network_preflight.json', probes)
    assert all(p['reachable'] for p in probes), 'STOP: network preflight failed'
    head = git('rev-parse','HEAD')
    BASE.mkdir()
    command('clone', ['git','clone','--no-local','--depth','1','--single-branch','--branch','revision/r5',ROOT,CLONE])
    assert git('rev-parse','HEAD',cwd=CLONE) == head
    assert not git('status','--porcelain',cwd=CLONE)
    command('uv-sync', ['uv','sync','--frozen'], CLONE)
    installation = json.loads(command('import-check',[PY,'-c',
        'import sys,json,signalpost;print(json.dumps(dict(module=signalpost.__file__,prefix=sys.prefix,python=sys.version)))'],CLONE))
    assert Path(installation['module']).is_relative_to(CLONE/'src')
    assert Path(installation['prefix']) == CLONE/'.venv'
    assert not git('status','--porcelain',cwd=CLONE)
    sample()


def sample():
    assert not WORK.exists(), 'No sampling after a run starts'
    head=git('rev-parse','HEAD')
    assert git('rev-parse','HEAD',cwd=CLONE)==head and not git('status','--porcelain',cwd=CLONE)
    installation=json.loads((DEST/'import-check.txt').read_text(encoding='utf8'))
    spec = importlib.util.spec_from_file_location('old_qualification', ROOT/'reports/r5/final500c/qualify.py')
    q = importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
    q.WORK = BASE;q.DEST = DEST
    per_file, excluded = q.excluded_sample_numbers()
    s = q.scale
    assert sha(s.UNIVERSE) == s.UNIVERSE_SHA
    assert sha(s.SNAPSHOT) == s.SNAPSHOT_SHA
    corpus=[];digest=hashlib.sha256();total=0
    with gzip.open(s.UNIVERSE,'rb') as f:
        for line in f:
            digest.update(line);total+=1
            org=str(json.loads(line)['organisation_number'])
            if valid(org) and org not in excluded:corpus.append(org)
    assert total == 411160 and digest.hexdigest() == s.UNIVERSE_CONTENT_SHA
    sample=random.Random(SEED).sample(corpus,500)
    assert len(set(sample)) == 500 and not set(sample)&excluded
    (DEST/'companies500.jsonl').write_text(''.join(json.dumps(dict(organisation_number=o))+'\n' for o in sample),encoding='utf8')
    extraction=json.loads(command('extract',[PY,CLONE/'scripts/extract_bulk.py','--bulk',s.SNAPSHOT,
        '--batch',DEST/'companies500.jsonl','--output',DEST/'registry500.csv'],CLONE).strip().splitlines()[-1])
    # A universe member absent from the newer snapshot stays in the random draw;
    # the normal CLI performs its live identity lookup instead of replacing it.
    assert extraction['rows']+len(extraction['missing_organisation_numbers'])==500
    save('clean_clone.json',dict(head=head,installation=installation,seed=SEED,pytest_in_clone=False,
        clone_clean=True,source_tree_sha256={p.relative_to(CLONE).as_posix():sha(p) for p in (CLONE/'src').rglob('*') if p.is_file()},
        excluded_files=per_file,excluded_unique_numbers=len(excluded),overlap=0,eligible_count=len(corpus),
        sample_sha256=sha(DEST/'companies500.jsonl'),bulk_sha256=sha(DEST/'registry500.csv'),
        universe_sha256=s.UNIVERSE_SHA,universe_content_sha256=digest.hexdigest(),registry_snapshot_sha256=s.SNAPSHOT_SHA,
        extraction=extraction,free_after_setup_bytes=shutil.disk_usage(ROOT).free))
    print(json.dumps(dict(head=head,seed=SEED,excluded=len(excluded),overlap=0,free_bytes=shutil.disk_usage(ROOT).free)),flush=True)


def run():
    meta=json.loads((DEST/'clean_clone.json').read_text(encoding='utf8'))
    assert git('rev-parse','HEAD',cwd=CLONE)==meta['head'] and not git('status','--porcelain',cwd=CLONE)
    assert sha(DEST/'companies500.jsonl')==meta['sample_sha256'] and sha(DEST/'registry500.csv')==meta['bulk_sha256']
    assert shutil.disk_usage(ROOT).free>=15*1024**3, 'STOP: less than 15 GiB before run'
    WORK.mkdir(exist_ok=False)
    args=[PY,'-m','signalpost.cli','run','--organisations',DEST/'companies500.jsonl','--bulk',DEST/'registry500.csv',
          '--output',WORK/'envelopes.jsonl','--profiles-output',WORK/'profiles.jsonl','--report',WORK/'report.json',
          '--run-id','evaluator-fixes-final500d-seed20261124','--expected-count','500']
    assert sum(str(x).startswith('--') for x in args)==7
    start=time.monotonic();minimum=shutil.disk_usage(ROOT).free;stopped=False;samples=[]
    with (DEST/'run.txt').open('w',encoding='utf8') as log:
        p=subprocess.Popen(list(map(str,args)),cwd=WORK,env=ENV,stdout=log,stderr=subprocess.STDOUT)
        while p.poll() is None:
            free=shutil.disk_usage(ROOT).free;minimum=min(minimum,free)
            samples.append(dict(seconds=time.monotonic()-start,free_bytes=free))
            if free<3*1024**3:
                stopped=True
                subprocess.run(['taskkill','/PID',str(p.pid),'/T','/F'],capture_output=True)
                p.wait();break
            time.sleep(2)
    wall=time.monotonic()-start
    save('disk_guard.json',dict(threshold_bytes=3*1024**3,interval_seconds=2,minimum_free_bytes=minimum,
        stopped_for_low_space=stopped,samples=samples))
    save('run.json',dict(exit_code=p.returncode,wall_seconds=wall,argv=list(map(str,args)),cwd=str(WORK),
        run_count=1,automatic_retry=False))
    path=DEST/'run.txt';path.write_text(portable_text(path.read_text(encoding='utf8')),encoding='utf8')
    print(json.dumps(dict(exit_code=p.returncode,wall_seconds=wall,stopped_for_low_space=stopped)),flush=True)
    if stopped or p.returncode:raise SystemExit('Run stopped/failed; no retry')


def finish():
    execution=json.loads((DEST/'run.json').read_text(encoding='utf8'))
    assert execution['exit_code']==0
    check_text=command('check_live_run',[PY,CLONE/'scripts/check_live_run.py',
       '--output',WORK/'envelopes.jsonl','--organisations',DEST/'companies500.jsonl','--state',WORK/'state',
       '--report',WORK/'report.json','--site',WORK/'site','--count','500'],CLONE,required=False)
    check_exit=json.loads((DEST/'check_live_run.json').read_text(encoding='utf8'))['exit_code']
    checked=json.loads(check_text.strip().splitlines()[-1]) if check_exit==0 else {'failed':True}
    report=json.loads((WORK/'report.json').read_text(encoding='utf8'))
    rows=[json.loads(line) for line in (WORK/'envelopes.jsonl').read_text(encoding='utf8').split('\n') if line.strip()]
    claims=[c for r in rows for c in r['claims'] if c['availability']=='available']
    sections={f:dict(Counter(r['run']['sections'].get(f,'not_recorded') for r in rows))
        for f in sorted({f for r in rows for f in r['run']['sections']})}
    families=dict(Counter(c['family'] for c in claims))
    unfinished=sum(any(e['code']=='not_started' for e in r['errors']) for r in rows)
    placeholders=sum(r['state']=='budget_exhausted' for r in rows)
    assert placeholders==len(report['output_limited_companies'])
    summary=dict(head=json.loads((DEST/'clean_clone.json').read_text())['head'],seed=SEED,
        wall_seconds=execution['wall_seconds'],margin_seconds=2100-execution['wall_seconds'],
        deadline_hits=report['deadline_hits'],section_states=sections,available_claims=len(claims),
        websites=sum(c['field']=='official_website' for c in claims),social_urls=sum(c['field'].startswith('social_profile.') for c in claims),
        placeholders=placeholders,unfinished_sections=unfinished,terminal_envelopes=len(rows),
        largest_profile_bytes=report['site'].get('largest_profile_bytes'),check_live_run_exit_code=check_exit,
        run_status=report['run_status'],cost_usd=report['total_cost_usd'],http_requests=report['requests'],
        families=families,stage_s_claims={f:families.get(f,0) for f in ('state_aid','research','licences','inspections')},
        state_aid_data_requests=sum('stottetiltak-registerinfo-api.app.brreg.no/api/' in e['url'] for e in report['request_log']),
        verification=checked,artifact_sha256={n:sha(WORK/n) for n in ('envelopes.jsonl','profiles.jsonl','report.json')},
        local_source_state=str(WORK/'state'),pytest_in_clone=False)
    summary['stage_s_total_claims']=sum(summary['stage_s_claims'].values())
    summary['all_gates_pass']=(check_exit==0 and summary['wall_seconds']<2100 and summary['cost_usd']==0
        and placeholders==0 and unfinished==0 and len(rows)==500)
    save('state_aid_requests.json',[e for e in report['request_log'] if 'stottetiltak-registerinfo-api.app.brreg.no' in e['url']])
    pass2=report['adaptive_websites']['pass2']
    save('deadline_losses.json',dict(deadline_hits=report['deadline_hits'],
        pass2={k:v for k,v in pass2.items() if k!='per_company'},
        companies={org:value for org,value in pass2['per_company'].items() if value['state']=='deadline'}))
    save('summary.json',summary)
    print(json.dumps(summary),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase',choices=['prepare','sample','run','finish'])
    globals()[parser.parse_args().phase]()
