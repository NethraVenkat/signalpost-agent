"""Clean-clone, disjoint-seed daily qualification. No paid source or push."""
import gzip,hashlib,json,os,random,subprocess,sys,time
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter

ROOT=Path(__file__).resolve().parents[3]
DEST=ROOT/'reports/r5/stageH'
CLONE=ROOT/'.data/r5/stageH-clean/repo'
SEEDS=(20261115,20261116,20261117)


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def validate_subset(extraction,sample):
    missing=extraction['missing_organisation_numbers']
    assert len(missing)==len(set(missing)) and set(missing)<=set(sample)
    assert extraction['expected']==len(sample) and extraction['rows']+len(missing)==len(sample)
    return missing
def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')


def execution_environment(test_mode=False):
    env=os.environ.copy();env.pop('PYTHONPATH',None)
    env.update(SIGNALPOST_SEARCH_PROVIDER='disabled',SIGNALPOST_SEARCH_MOCK='0',PYTHONUTF8='1')
    if test_mode:
        # Offline search tests choose their own fake adapter/key with monkeypatch.
        # A live-run disabled-provider override otherwise suppresses those mocks.
        for key in ('SIGNALPOST_SEARCH_PROVIDER','SIGNALPOST_SEARCH_MOCK','BRAVE_SEARCH_API_KEY'):env.pop(key,None)
    return env


def command(folder,name,argv,cwd,check=True):
    folder.mkdir(parents=True,exist_ok=True)
    env=execution_environment(test_mode=name=='pytest')
    started=time.perf_counter()
    with (folder/(name+'.txt')).open('w',encoding='utf8') as log:
        result=subprocess.run([str(a) for a in argv],cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT)
    receipt={'argv':[str(a) for a in argv],'cwd':str(cwd),'exit_code':result.returncode,
        'wall_seconds':time.perf_counter()-started,'completed_at_utc':datetime.now(timezone.utc).isoformat(),
        'environment_overrides':{k:env.get(k,'unset') for k in ('SIGNALPOST_SEARCH_PROVIDER','SIGNALPOST_SEARCH_MOCK','PYTHONUTF8')},'PYTHONPATH':'unset'}
    save(folder/(name+'.json'),receipt)
    if check:result.check_returncode()
    return receipt


def prepare(resume=False,reuse_passed_tests=False):
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    if CLONE.exists() and not resume:raise ValueError('Preserve earlier clone; use explicit resume only for preparation failures')
    if not resume:command(DEST,'clone',['git','clone','--no-hardlinks','--branch','revision/r5',ROOT,CLONE],ROOT)
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=CLONE,text=True).strip()==head
    assert not subprocess.check_output(['git','status','--porcelain'],cwd=CLONE,text=True).strip()
    command(DEST,'sync-frozen',['uv','sync','--frozen'],CLONE)
    python=CLONE/'.venv/Scripts/python.exe' if os.name=='nt' else CLONE/'.venv/bin/python'
    inspect="import signalpost,sys,json,importlib.metadata;print(json.dumps({'python':sys.executable,'prefix':sys.prefix,'module':signalpost.__file__,'version':importlib.metadata.version('signalpost-agent')}))"
    command(DEST,'installation',[python,'-c',inspect],CLONE)
    installation=json.loads((DEST/'installation.txt').read_text(encoding='utf8'))
    assert Path(installation['prefix']).resolve()==(CLONE/'.venv').resolve()
    assert Path(installation['module']).resolve().is_relative_to(CLONE/'src')
    if reuse_passed_tests:
        receipt=json.loads((DEST/'pytest.json').read_text(encoding='utf8'))
        assert receipt['exit_code']==0 and Path(receipt['cwd']).resolve()==CLONE.resolve()
    else:command(DEST,'pytest',[python,'reports/r5/stage4_7/run_tests.py','-q','-p','no:cacheprovider'],CLONE)
    baseline=json.loads((CLONE/'reports/r5/baseline/settings.json').read_text(encoding='utf8'))
    universe=baseline['inputs']['universe_archive'];bulk=baseline['inputs']['registry_snapshot']
    assert sha(universe['path'])==universe['sha256'] and sha(bulk['path'])==bulk['sha256']
    prior={}
    # Include every retained named sample/batch input in reports, plus CI inputs.
    # Output envelopes and the complete universe are not used as exclusions.
    for p in sorted((CLONE/'reports').rglob('*.jsonl')):
        if any(word in p.name.lower() for word in ('companies','sample','batch')):
            ids=set()
            for line in p.read_text(encoding='utf-8-sig').splitlines():
                if line.strip():
                    row=json.loads(line)
                    if isinstance(row,dict) and 'organisation_number' in row:ids.add(str(row['organisation_number']))
            if ids:prior[p.relative_to(CLONE).as_posix()]={'ids':ids,'sha256':sha(p)}
    p=CLONE/'tests/fixtures/ci20.jsonl'
    prior['tests/fixtures/ci20.jsonl']={'ids':{json.loads(x)['organisation_number'] for x in p.read_text(encoding='utf8').splitlines()},'sha256':sha(p)}
    required=['reports/r5/baseline/companies.jsonl','reports/r5/release-v4/companies100.jsonl','reports/r5/release-v4b/companies100.jsonl']
    assert all(p in prior for p in required)
    excluded=set().union(*(p['ids'] for p in prior.values()));original_excluded=set(excluded)
    corpus=[];digest=hashlib.sha256();total=0
    with gzip.open(universe['path'],'rb') as f:
        for line in f:
            digest.update(line);total+=1;corpus.append(str(json.loads(line)['organisation_number']))
    assert total==411160 and digest.hexdigest()==baseline['universe_content_sha256']
    sampling={};from signalpost.identity.orgnr import valid
    for seed in SEEDS:
        sample_name='seed'+str(seed);folder=DEST/sample_name;folder.mkdir(parents=True,exist_ok=True)
        if (folder/'settings.json').exists():raise ValueError('A live run exists; preserve its preparation and use explicit rerun')
        eligible=[o for o in corpus if o not in excluded]
        sample=random.Random(seed).sample(eligible,100)
        assert len(set(sample))==100 and all(valid(o) for o in sample) and not (set(sample)&excluded)
        batch=folder/'companies100.jsonl'
        sample_bytes=''.join(json.dumps({'organisation_number':o})+'\n' for o in sample).encode('utf8')
        if batch.exists():assert batch.read_bytes()==sample_bytes,'Do not silently change a drawn sample'
        else:batch.write_bytes(sample_bytes)
        command(folder,'extract',[python,'scripts/extract_bulk.py','--bulk',bulk['path'],'--batch',batch,'--output',folder/'registry100.csv'],CLONE)
        result=json.loads((folder/'extract.txt').read_text(encoding='utf8'));missing=validate_subset(result,sample)
        sampling[sample_name]={'seed':seed,'eligible_count':len(eligible),'excluded_count':len(excluded),
            'sample_sha256':sha(batch),'registry_sha256':sha(folder/'registry100.csv'),
            'registry_rows_found':result['rows'],'missing_snapshot_rows':missing,
            'overlap_with_prior_samples':{name:len(set(sample)&p['ids']) for name,p in prior.items()},
            'overlap_with_all_preceding_inputs':len(set(sample)&excluded),'input_order':sample}
        excluded.update(sample)
    manifest={p.relative_to(CLONE).as_posix():sha(p) for p in sorted((CLONE/'src').rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
    save(DEST/'source_manifest.json',manifest)
    meta={'tested_commit':head,'clone':str(CLONE),'uv_lock_sha256':sha(CLONE/'uv.lock'),'installation':installation,
        'universe':universe,'bulk':bulk,'universe_count':total,'universe_content_sha256':digest.hexdigest(),
        'sampling':'Independent Random(seed).sample over corpus order after excluding retained prior named sample/batch inputs and preceding Stage H batches',
        'original_excluded_unique':len(original_excluded),'prior_input_files':{k:{'count':len(v['ids']),'sha256':v['sha256']} for k,v in prior.items()},
        'samples':sampling,'source_manifest_sha256':sha(DEST/'source_manifest.json')}
    save(DEST/'clean_clone.json',meta)
    return python,meta


def run_batch(seed,attempt='first'):
    folder=DEST/('seed'+str(seed));meta=json.loads((DEST/'clean_clone.json').read_text(encoding='utf8'))
    python=CLONE/'.venv/Scripts/python.exe' if os.name=='nt' else CLONE/'.venv/bin/python'
    out=CLONE/'.data'/('stageH-'+str(seed)+'-'+attempt)
    out.mkdir(parents=True,exist_ok=False)
    settings={'organisations':folder/'companies100.jsonl','bulk':folder/'registry100.csv','output':out/'envelopes.jsonl',
        'profiles-output':out/'profiles.jsonl','report':out/'report.json','run-id':'stageH-'+str(seed)+'-'+attempt,'expected-count':100}
    argv=[python,'-m','signalpost.cli','run']
    for key,value in settings.items():argv+=['--'+key,str(value)]
    assert sum(str(a).startswith('--') for a in argv)==7
    save(folder/'settings.json',{'working_directory':str(out),'resolved_config':{'run_id':settings['run-id']},
        'command_argv':[str(a) for a in argv],'exact_seven_flags':True,'tested_commit':meta['tested_commit'],
        'source_manifest_sha256':meta['source_manifest_sha256'],'input_sha256':sha(settings['organisations']),'registry_sha256':sha(settings['bulk'])})
    execution=command(folder,'execution',argv,out)
    assert execution['wall_seconds']<=2100,'Process wall exceeds 35 minutes'
    command(folder,'verification',[python,'scripts/check_live_run.py','--output',out/'envelopes.jsonl',
        '--organisations',settings['organisations'],'--count','100','--state',out/'state',
        '--report',out/'report.json','--site',out/'site'],CLONE)
    verification=json.loads((folder/'verification.txt').read_text(encoding='utf8'));save(folder/'verification.json',verification)
    rows=[json.loads(x) for x in (out/'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
    report=json.loads((out/'report.json').read_text(encoding='utf8'))
    assert execution['exit_code']==0 and len(rows)==100
    assert report['requests']<=1850 and report['total_cost_usd']==0
    assert report['llm']['calls']==report['search']['queries']==0
    claims=[[c for c in row['claims'] if c['availability']=='available'] for row in rows]
    metrics={'verified_websites':sum(any(c['field']=='official_website' for c in cs) for cs in claims),
        'social_profile_companies':sum(any(c['field'].startswith('social_profile.') for c in cs) for cs in claims),
        'job_ad_companies':sum(any(c['field'].startswith('hiring.job.') for c in cs) for cs in claims),
        'job_claims':sum(c['field'].startswith('hiring.job.') for cs in claims for c in cs),
        'activity_companies':sum(any(c['family'] in {'activity','procurement'} for c in cs) for cs in claims),
        'activity_claims':sum(c['family'] in {'activity','procurement'} for cs in claims for c in cs),
        'total_facts':sum(map(len,claims)),'http_requests':report['requests'],'runtime_seconds':report['runtime_ms']/1000,
        'process_wall_seconds':execution['wall_seconds'],'cost_usd':0}
    save(folder/'counts.json',{'metrics':metrics,'section_states':{s:dict(Counter(r['run']['sections'].get(s) for r in rows)) for s in rows[0]['run']['sections']},
        'artifacts':{p:sha(out/p) for p in ('envelopes.jsonl','profiles.jsonl','report.json')}})
    (folder/'report.json').write_bytes((out/'report.json').read_bytes())
    print(json.dumps({'seed':seed,'metrics':metrics,'complete_briefings':verification['complete_briefing_contracts']}),flush=True)


def main():
    if len(sys.argv)>1 and sys.argv[1]=='rerun':
        run_batch(int(sys.argv[2]),sys.argv[3]);return
    mode=sys.argv[1] if len(sys.argv)>1 else ''
    prepare(resume=mode in {'resume','resume-after-tests'},reuse_passed_tests=mode=='resume-after-tests')
    for seed in SEEDS:run_batch(seed)
    save(DEST/'ledger_runs.json',[{'sample':'seed'+str(seed),'seed':seed,'folder':str(DEST/('seed'+str(seed)))} for seed in SEEDS])
    command(DEST,'ledger',[sys.executable,'scripts/precision_ledger.py','--runs',DEST/'ledger_runs.json','--destination',DEST/'precision'],ROOT)
    ledger=json.loads((DEST/'precision/ledger.json').read_text(encoding='utf8'))
    doubtful=[i for i in ledger['items'] if i['verdict']!='correct']
    save(DEST/'doubtful_items.json',doubtful)
    text='# Stage H items needing hand review\n\nAutomated saved-evidence verdicts; every flagged item stays in the output. Human verdicts for prior Stage T sample/value pairs are not transferred to these new runs. Full excerpts: precision/LEDGER.md.\n\n'
    for item in doubtful:
        text+='## '+str(item['seed'])+' / '+item['organisation_number']+' / '+item['company']+' / '+item['kind']+'\n\n'
        text+='Automated verdict: **'+item['verdict']+'**. '+('; '.join(item['reasons']))+'\n\n'
        text+='```json\n'+json.dumps(item['value'],ensure_ascii=False,indent=2)+'\n```\n\n'
        for e in item['evidence']:
            text+='Source: '+e['source_url']+'; retrieval '+e['retrieved_at']+'; SHA-256 `'+e['content_sha256']+'`; locator `'+e['locator']+'`.\n\n```text\n'+e['claim_span']+'\n```\n\n'
    if not doubtful:text+='No doubtful or wrong published items under the automated saved-evidence rules. This is not independent human-labelled precision.\n'
    (DEST/'doubtful_items.md').write_text(text,encoding='utf8',newline='')
    print(json.dumps({'ledger_counts':ledger['counts'],'flagged_items':len(doubtful)}),flush=True)


if __name__=='__main__':main()
