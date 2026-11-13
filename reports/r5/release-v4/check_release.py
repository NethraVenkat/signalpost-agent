"""Reproduce the clean-clone release smoke checks without extra evaluator flags."""
import hashlib,importlib.metadata,json,os,subprocess,sys,time
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
import signalpost
from signalpost.identity.orgnr import valid

ROOT=Path(__file__).resolve().parents[3]
DEST=ROOT/'reports/r5/release-v4'
ENV=os.environ.copy();ENV.update(SIGNALPOST_SEARCH_PROVIDER='disabled',SIGNALPOST_SEARCH_MOCK='0',PYTHONUTF8='1')


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def save(name,value): (DEST/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')


def command(name,args,cwd=ROOT):
    began=time.perf_counter()
    with (DEST/(name+'.txt')).open('w',encoding='utf8') as log:
        result=subprocess.run([str(a) for a in args],cwd=cwd,env=ENV,stdout=log,stderr=subprocess.STDOUT)
    info={'argv':[str(a) for a in args],'cwd':str(cwd),'exit_code':result.returncode,
          'wall_seconds':time.perf_counter()-began,'finished_at_utc':datetime.now(timezone.utc).isoformat()}
    save(name+'.json',info);result.check_returncode()
    return info


def prepare():
    assert Path(signalpost.__file__).resolve().is_relative_to(ROOT/'src')
    assert Path(sys.prefix).resolve()==(ROOT/'.venv').resolve()
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    assert not subprocess.check_output(['git','diff','HEAD','--','src','pyproject.toml','uv.lock'],cwd=ROOT,text=True).strip()
    base=json.loads((ROOT/'reports/r5/baseline/settings.json').read_text(encoding='utf8'))
    universe=base['inputs']['universe_archive'];bulk=base['inputs']['registry_snapshot']
    assert sha(universe['path'])==universe['sha256'] and sha(bulk['path'])==bulk['sha256']
    command('sync-frozen',['uv','sync','--frozen'])
    command('sample',[sys.executable,'scripts/sample_universe.py','--universe',universe['path'],
        '--output',DEST/'companies100.jsonl','--count','100','--seed','20261113'])
    command('extract',[sys.executable,'scripts/extract_bulk.py','--bulk',bulk['path'],
        '--batch',DEST/'companies100.jsonl','--output',DEST/'registry100.csv'])
    rows=[json.loads(line)['organisation_number'] for line in (DEST/'companies100.jsonl').read_text(encoding='utf8').splitlines()]
    assert len(rows)==len(set(rows))==100 and all(valid(org) for org in rows)
    old={json.loads(line)['organisation_number'] for line in (ROOT/'reports/r5/baseline/companies.jsonl').read_text(encoding='utf8').splitlines()}
    edge=[rows[0],'123456789',rows[1],rows[2],rows[0],rows[3],'923609017',rows[4],rows[5],rows[6]]
    assert sum(not valid(org) for org in edge)==2 and len(edge)-len(set(edge))==1
    (DEST/'companies10.jsonl').write_text(''.join(json.dumps({'organisation_number':org})+'\n' for org in edge),encoding='utf8')
    save('clean_clone.json',{'tested_source_commit':head,'clone_directory':str(ROOT),'python_executable':sys.executable,
        'python_prefix':sys.prefix,'loaded_signalpost_module':signalpost.__file__,
        'installed_version_at_smoke':importlib.metadata.version('signalpost-agent'),
        'uv_lock_sha256':sha(ROOT/'uv.lock'),'universe':universe,'registry_snapshot':bulk,
        'sample_seed':20261113,'sample_sha256':sha(DEST/'companies100.jsonl'),
        'subset_sha256':sha(DEST/'registry100.csv'),'overlap_with_frozen100':len(set(rows)&old),
        'environment_overrides':{k:ENV[k] for k in ['SIGNALPOST_SEARCH_PROVIDER','SIGNALPOST_SEARCH_MOCK','PYTHONUTF8']}})
    save('source_manifest.json',{p.relative_to(ROOT).as_posix():sha(p) for p in sorted((ROOT/'src').rglob('*'))
        if p.is_file() and '__pycache__' not in p.parts})
    licenses=[]
    for dist in sorted(importlib.metadata.distributions(),key=lambda d:d.metadata.get('Name','')):
        m=dist.metadata
        licenses.append({'name':m.get('Name'),'version':dist.version,'license_expression':m.get('License-Expression'),
            'license':m.get('License'),'license_classifiers':[s for s in m.get_all('Classifier',[]) if s.startswith('License ::')],
            'project_urls':m.get_all('Project-URL',[])})
    save('dependency_licenses.json',licenses)
    print(json.dumps({'prepared':100,'edge_rows':10,'sample_overlap':len(set(rows)&old),'source_commit':head}))


def run_smoke(kind,summarize_only=False):
    count=100 if kind=='daily' else 10
    batch=DEST/('companies100.jsonl' if kind=='daily' else 'companies10.jsonl')
    work=ROOT/'.data/release-v4'/kind
    if not summarize_only:
        if work.exists():raise ValueError('Fresh state required; preserve prior run')
        work.mkdir(parents=True)
    flags={'organisations':batch,'bulk':DEST/'registry100.csv','output':work/'envelopes.jsonl',
           'profiles-output':work/'profiles.jsonl','report':work/'report.json',
           'run-id':'release-v4-'+kind+'-seed20261113','expected-count':count}
    args=[sys.executable,'-m','signalpost.cli','run']
    for key,value in flags.items():args.extend(['--'+key,value])
    assert sum(str(a).startswith('--') for a in args)==7
    execution=(json.loads((DEST/(kind+'.json')).read_text(encoding='utf8')) if summarize_only else command(kind,args,work))
    verify=[sys.executable,'scripts/verify_output.py','--first',work/'envelopes.jsonl',
        '--organisations',batch,'--count',str(count),'--state-dir',work/'state','--report',work/'report.json']
    command(kind+'-verify',verify)
    checked=json.loads((DEST/(kind+'-verify.txt')).read_text(encoding='utf8'))
    report=json.loads((work/'report.json').read_text(encoding='utf8'))
    rows=[json.loads(line) for line in (work/'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
    expected=[json.loads(line)['organisation_number'] for line in batch.read_text(encoding='utf8').splitlines()]
    assert len(rows)==count and [r['organisation_number'] for r in rows]==expected
    assert all(r['run']['terminal_status'] in {'completed','failed'} for r in rows)
    assert not any(e['code']=='not_started' for r in rows for e in r['errors'])
    assert report['requests']<=report['limits']['max_requests']<=1850
    assert execution['wall_seconds']<45*60
    assert report['completion']['within_requested_time_budget'] and report['completion']['within_effective_time_budget']
    # All inputs in these two batches are filename-safe nine-digit numbers.
    # Invalid checksums retain explicitly failed placeholder profiles.
    assert report['site']['state']=='available' and report['site']['companies']==len(set(expected))
    assert report['total_cost_usd']==report['search']['queries']==report['llm']['calls']==0
    assert checked['synthesis_unverified_values']==checked['briefing_unverified_values']==0
    assert checked['complete_briefing_contracts']==count
    assert all(report['enrichment'][f] for f in ['websites','hiring','public_activity'])
    if kind=='edge':
        assert report['duplicates']==1 and len(report['invalid_inputs'])==2 and rows[0]==rows[4]
        assert report['site']['skipped_invalid_identifiers']==0
        invalid={org for org in expected if not valid(org)}
        assert all(r['run']['terminal_status']=='failed' and all(c['availability']!='available' for c in r['claims'])
                   for r in rows if r['organisation_number'] in invalid)
        assert not any(e['organisation_number'] in invalid for e in report['request_log'])
    claims=[c for r in rows for c in r['claims'] if c['availability']=='available']
    summary={'input_rows':count,'unique_inputs':len(set(expected)),'terminal_envelopes':len(rows),'input_order_verified':True,
        'duplicate_rows':report['duplicates'],'invalid_inputs':report['invalid_inputs'],
        'exit_code':execution['exit_code'],'http_requests':report['requests'],'http_cap':report['limits']['max_requests'],
        'wall_seconds':execution['wall_seconds'],'runtime_seconds':report['runtime_ms']/1000,'completion':report['completion'],
        'site':report['site'],'total_cost_usd':report['total_cost_usd'],'verification':checked,
        'websites':sum(c['field']=='official_website' for c in claims),
        'social_urls':sum(c['field'].startswith('social_profile.') for c in claims),
        'contacts':sum(c['field'].startswith('contact.') for c in claims),
        'jobs':sum(c['field'].startswith('hiring.job.') for c in claims),'activity_claims':sum(c['family']=='activity' for c in claims),
        'facts':len(claims),'section_states':{family:dict(Counter(r['run']['sections'].get(family,'not_recorded') for r in rows))
            for family in ['identity','roles','subunits','accounts','website','hiring','activity']},
        'artifacts':{name:sha(work/name) for name in ['envelopes.jsonl','profiles.jsonl','report.json']}}
    save(kind+'-summary.json',summary)
    (DEST/(kind+'-report.json')).write_bytes((work/'report.json').read_bytes())
    print(json.dumps({'kind':kind,**{k:summary[k] for k in ['terminal_envelopes','http_requests','wall_seconds','websites','social_urls','total_cost_usd']}}))


if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    else:run_smoke(sys.argv[1],'--summarize-only' in sys.argv[2:])
