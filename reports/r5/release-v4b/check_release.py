"""Authored release-only checks: isolated clone, disjoint sample, seven flags."""
from signalpost.portable_paths import expand, portable, portable_text, sanitize_file  # saved paths stay repo-relative
import gzip,hashlib,importlib.metadata,json,os,random,subprocess,sys,time
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
import signalpost
from signalpost.identity.orgnr import valid

ROOT=Path(__file__).resolve().parents[3]
DEST=ROOT/'reports/r5/release-v4b'
ENV=os.environ.copy();ENV.update(SIGNALPOST_SEARCH_PROVIDER='disabled',SIGNALPOST_SEARCH_MOCK='0',PYTHONUTF8='1')

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def save(name,value):
    DEST.mkdir(parents=True,exist_ok=True)
    (DEST/name).write_text(portable_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n'),encoding='utf8')

def command(name,args,cwd=ROOT,env=None):
    began=time.perf_counter()
    with (DEST/(name+'.txt')).open('w',encoding='utf8') as log:
        result=subprocess.run([str(a) for a in args],cwd=cwd,env=ENV if env is None else env,stdout=log,stderr=subprocess.STDOUT)
    sanitize_file(DEST/(name+'.txt'))  # keep captured paths repo-relative
    info={'argv':[str(a) for a in args],'cwd':str(cwd),'exit_code':result.returncode,
          'wall_seconds':time.perf_counter()-began,'completed_at_utc':datetime.now(timezone.utc).isoformat()}
    save(name+'.json',info);result.check_returncode();return info

def installation(name):
    assert Path(signalpost.__file__).resolve().is_relative_to(ROOT/'src')
    assert Path(sys.prefix).resolve()==(ROOT/'.venv').resolve()
    licenses=[]
    for dist in sorted(importlib.metadata.distributions(),key=lambda d:d.metadata.get('Name','')):
        m=dist.metadata
        licenses.append({'name':m.get('Name'),'version':dist.version,'license_expression':m.get('License-Expression'),
            'license':m.get('License'),'license_classifiers':[s for s in m.get_all('Classifier',[]) if s.startswith('License ::')],
            'project_urls':m.get_all('Project-URL',[])})
    save(name,{'python_executable':sys.executable,'python_prefix':sys.prefix,'loaded_signalpost_module':signalpost.__file__,
        'installed_version':importlib.metadata.version('signalpost-agent'),'uv_lock_sha256':sha(ROOT/'uv.lock'),'dependencies':licenses})

def prepare():
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    assert not subprocess.check_output(['git','diff','HEAD','--','src','pyproject.toml','uv.lock'],cwd=ROOT,text=True).strip()
    base=json.loads((ROOT/'reports/r5/baseline/settings.json').read_text(encoding='utf8'))
    universe=base['inputs']['universe_archive'];bulk=base['inputs']['registry_snapshot']
    assert sha(universe['path'])==universe['sha256'] and sha(bulk['path'])==bulk['sha256']
    prior={label:{json.loads(line)['organisation_number'] for line in (ROOT/path).read_text(encoding='utf8').splitlines()}
        for label,path in [('seed20261017','reports/r5/baseline/companies.jsonl'),('seed20261113','reports/r5/release-v4/companies100.jsonl')]}
    excluded=set().union(*prior.values());corpus=[];digest=hashlib.sha256();total=0
    with gzip.open(expand(universe['path']),'rb') as f:
        for line in f:
            digest.update(line);total+=1;row=json.loads(line);org=str(row['organisation_number'])
            if org not in excluded:corpus.append(org)
    assert total==411160 and digest.hexdigest()=='b82d6a3e7231d1759a958c282bc4366b80ec2fab8095053d8ed7fa9cd01bc838'
    sample=random.Random(20261114).sample(corpus,100)
    assert len(set(sample))==100 and all(valid(org) for org in sample)
    assert all(not (set(sample)&old) for old in prior.values())
    DEST.mkdir(parents=True,exist_ok=True)
    (DEST/'companies100.jsonl').write_text(portable_text(''.join(json.dumps({'organisation_number':org})+'\n' for org in sample)),encoding='utf8')
    command('extract',[sys.executable,'scripts/extract_bulk.py','--bulk',bulk['path'],'--batch',DEST/'companies100.jsonl','--output',DEST/'registry100.csv'])
    extraction=json.loads((DEST/'extract.txt').read_text(encoding='utf8'));assert extraction['rows']==100 and not extraction['missing_organisation_numbers']
    prior_edge=ROOT/'reports/r5/release-v4/companies10.jsonl'
    edge=[json.loads(line)['organisation_number'] for line in prior_edge.read_text(encoding='utf8').splitlines()]
    assert sum(not valid(org) for org in edge)==2 and len(edge)-len(set(edge))==1
    (DEST/'companies10.jsonl').write_bytes(prior_edge.read_bytes())
    metadata={'tested_source_commit':head,'clone_directory':str(ROOT),'universe':universe,'registry_snapshot':bulk,
        'universe_content_sha256':digest.hexdigest(),'universe_count':total,'sample_seed':20261114,
        'sampling':'Uniform random.Random(20261114).sample of corpus order after excluding both prior 100-company cohorts',
        'excluded_unique_companies':len(excluded),'eligible_count':len(corpus),'sample_sha256':sha(DEST/'companies100.jsonl'),
        'subset_sha256':sha(DEST/'registry100.csv'),'overlap_with_prior_samples':{k:len(set(sample)&old) for k,old in prior.items()},
        'environment_overrides':{k:ENV[k] for k in ('SIGNALPOST_SEARCH_PROVIDER','SIGNALPOST_SEARCH_MOCK','PYTHONUTF8')},
        'prepared_at_utc':datetime.now(timezone.utc).isoformat()}
    save('clean_clone.json',metadata)
    save('source_manifest.json',{p.relative_to(ROOT).as_posix():sha(p) for p in sorted((ROOT/'src').rglob('*')) if p.is_file() and '__pycache__' not in p.parts})
    installation('installation-smoke.json');print(json.dumps(metadata))

def smoke(kind,summarize_only=False):
    assert kind in {'daily','edge'}
    count=100 if kind=='daily' else 10;batch=DEST/('companies100.jsonl' if kind=='daily' else 'companies10.jsonl')
    work=ROOT/'.data/release-v4b'/('edge-repeat' if kind=='edge' else kind)
    if not summarize_only:
        if work.exists():raise ValueError('Fresh state required; preserve previous evidence')
        work.mkdir(parents=True)
    bulk=DEST/'registry100.csv' if kind=='daily' else ROOT/'reports/r5/release-v4/registry100.csv'
    if kind=='edge':assert sha(bulk)==json.loads((ROOT/'reports/r5/release-v4/clean_clone.json').read_text(encoding='utf8'))['subset_sha256']
    flags={'organisations':batch,'bulk':bulk,'output':work/'envelopes.jsonl','profiles-output':work/'profiles.jsonl',
           'report':work/'report.json','run-id':'release-v4b-daily-seed20261114' if kind=='daily' else 'release-v4b-edge-repeat-prior','expected-count':count}
    args=[sys.executable,'-m','signalpost.cli','run']
    for key,value in flags.items():args.extend(['--'+key,str(value)])
    assert len([v for v in args if v.startswith('--')])==7
    execution=json.loads((DEST/(kind+'.json')).read_text(encoding='utf8')) if summarize_only else command(kind,args,work)
    quote=lambda v:"'"+str(v).replace("'","''")+"'"
    (DEST/(kind+'-run.ps1')).write_text(portable_text('# Run from '+str(work)+' with recorded environment overrides.\n& '+' '.join(map(quote,args))+'\n'),encoding='utf8')
    verify=[sys.executable,'scripts/verify_output.py','--first',work/'envelopes.jsonl','--organisations',batch,'--count',str(count),'--state-dir',work/'state','--report',work/'report.json']
    command(kind+'-verify',verify);checked=json.loads((DEST/(kind+'-verify.txt')).read_text(encoding='utf8'))
    save(kind+'-verification.json',checked)
    report=json.loads((work/'report.json').read_text(encoding='utf8'))
    rows=[json.loads(x) for x in (work/'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
    expected=[json.loads(x)['organisation_number'] for x in batch.read_text(encoding='utf8').splitlines()]
    assert len(rows)==count and [r['organisation_number'] for r in rows]==expected
    assert all(r['run']['terminal_status'] in {'completed','failed'} for r in rows)
    assert not any(e['code']=='not_started' for r in rows for e in r['errors'])
    assert report['requests']<=report['limits']['max_requests']<=1850 and execution['wall_seconds']<45*60
    assert report['completion']['within_requested_time_budget'] and report['completion']['within_effective_time_budget']
    assert report['site']['state']=='available' and report['site']['companies']==len(set(expected))
    assert report['total_cost_usd']==report['search']['queries']==report['llm']['calls']==0
    assert checked['synthesis_unverified_values']==checked['briefing_unverified_values']==0 and checked['complete_briefing_contracts']==count
    assert all(report['enrichment'].values())
    for row in rows:
        topics={s['topic'] for s in row['run']['synthesis']['briefing']}
        assert {'activity','change','unknown','financial','takeaway'}<=topics
        assert row['profile']['synthesis']==row['run']['synthesis']
    if kind=='edge':
        invalid={org for org in expected if not valid(org)}
        assert report['duplicates']==1 and len(report['invalid_inputs'])==2 and rows[0]==rows[4]
        assert not any(e['organisation_number'] in invalid for e in report['request_log'])
        assert all(r['run']['terminal_status']=='failed' and not any(c['availability']=='available' for c in r['claims']) for r in rows if r['organisation_number'] in invalid)
    claims=[c for r in rows for c in r['claims'] if c['availability']=='available'];formulas=Counter(m['formula'] for r in rows for m in r['run']['synthesis']['financial_metrics'])
    summary={'input_rows':count,'unique_inputs':len(set(expected)),'terminal_envelopes':len(rows),'ordered':True,'exit_code':execution['exit_code'],
        'invalid_inputs':report['invalid_inputs'],'duplicates':report['duplicates'],'http_requests':report['requests'],'http_cap':report['limits']['max_requests'],
        'wall_seconds':execution['wall_seconds'],'runtime_seconds':report['runtime_ms']/1000,'total_cost_usd':report['total_cost_usd'],
        'websites':sum(c['field']=='official_website' for c in claims),'social_urls':sum(c['field'].startswith('social_profile.') for c in claims),
        'social_companies':sum(any(c['field'].startswith('social_profile.') and c['availability']=='available' for c in r['claims']) for r in rows),
        'jobs':sum(c['field'].startswith('hiring.job.') for c in claims),'job_companies':sum(any(c['field'].startswith('hiring.job.') and c['availability']=='available' for c in r['claims']) for r in rows),
        'contacts':sum(c['field'].startswith('contact.') for c in claims),'facts':len(claims),'activity_claims':sum(c['family']=='activity' for c in claims),
        'accounts_facts':sum(c['family']=='accounts' for c in claims),'formulas':dict(formulas),'site':report['site'],
        'section_states':{family:dict(Counter(r['run']['sections'].get(family,'not_recorded') for r in rows)) for family in sorted({f for r in rows for f in r['run']['sections']})},
        'verification':checked,'artifacts':{name:sha(work/name) for name in ('envelopes.jsonl','profiles.jsonl','report.json')}}
    save(kind+'-summary.json',summary);(DEST/(kind+'-report.json')).write_bytes((work/'report.json').read_bytes())
    print(json.dumps(summary))

if __name__=='__main__':
    action=sys.argv[1]
    if action=='prepare':prepare()
    elif action=='installation':installation('installation-final.json')
    elif action in {'tests','tests-version'}:
        test_env=dict(ENV)
        for name in ('SIGNALPOST_SEARCH_PROVIDER','SIGNALPOST_SEARCH_MOCK','BRAVE_SEARCH_API_KEY'):test_env.pop(name,None)
        command('pytest-version' if action=='tests-version' else 'pytest',[sys.executable,'reports/r5/stage4_7/run_tests.py','-q'],env=test_env)
    else:smoke(action,'--summarize-only' in sys.argv[2:])
