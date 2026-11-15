"""One fresh normal P0 sample, exact seven flags, full verification and diff."""
import hashlib,json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reports/r5/stageX'))
from measure import counts,identities,manifest,save,sha
DEST=ROOT/'reports/r5/stageP0'

def main():
    label=sys.argv[1] if len(sys.argv)>1 else 'final'
    base=ROOT/'reports/r5/stageX/X2/seed20261017'
    old=json.loads((base/'settings.json').read_text(encoding='utf8'));oldargv=old['command_argv'];previous=Path(old['working_directory'])
    orgs=Path(oldargv[oldargv.index('--organisations')+1]);bulk=Path(oldargv[oldargv.index('--bulk')+1])
    work=ROOT/'.data/r5'/('stageP0-20261017-'+label);work.mkdir(exist_ok=False)
    DEST.mkdir(parents=True,exist_ok=True);source=manifest();save(DEST/'source_manifest.json',source)
    save(DEST/'verification_manifest.json',{str(p):sha(p) for p in (ROOT/'scripts').glob('verify*.py')})
    flags={'organisations':orgs,'bulk':bulk,'output':work/'envelopes.jsonl','profiles-output':work/'profiles.jsonl','report':work/'report.json','run-id':'r5-stageP0-seed20261017-'+label,'expected-count':100}
    argv=[sys.executable,'-m','signalpost.cli','run']
    for k,v in flags.items():argv.extend(['--'+k,str(v)])
    assert sum(a.startswith('--') for a in argv)==7
    save(DEST/'settings.json',{'seed':20261017,'working_directory':str(work),'previous_working_directory':str(previous),'command_argv':argv,'exact_seven_flags':True,'input_sha256':sha(orgs),'bulk_sha256':sha(bulk),'parent_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()})
    env=os.environ.copy();env.update(PYTHONUTF8='1',SIGNALPOST_SEARCH_PROVIDER='disabled',SIGNALPOST_SEARCH_MOCK='0')
    start=time.monotonic();print('Starting P0 normal frozen sample',flush=True)
    with (DEST/'execution.txt').open('w',encoding='utf8') as log:p=subprocess.run(argv,cwd=work,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=2160)
    save(DEST/'execution.json',{'argv':argv,'cwd':str(work),'exit_code':p.returncode,'wall_seconds':time.monotonic()-start});assert p.returncode==0
    v=subprocess.run([sys.executable,str(ROOT/'scripts/check_live_run.py'),'--output',str(work/'envelopes.jsonl'),'--organisations',str(orgs),'--state',str(work/'state'),'--report',str(work/'report.json'),'--site',str(work/'site'),'--count','100'],cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf8')
    (DEST/'verification.txt').write_text(v.stdout+v.stderr,encoding='utf8');assert v.returncode==0
    verification=json.loads(v.stdout);save(DEST/'verification.json',verification)
    report=json.loads((work/'report.json').read_text(encoding='utf8'));save(DEST/'report.json',report)
    rows=list(map(json.loads,(work/'envelopes.jsonl').read_text(encoding='utf8').splitlines()));prior=list(map(json.loads,(previous/'envelopes.jsonl').read_text(encoding='utf8').splitlines()))
    before,after=identities(prior),identities(rows)
    result={'before':counts(prior),'after':counts(rows),'HTTP':report['requests'],'wall_seconds':json.loads((DEST/'execution.json').read_text())['wall_seconds'],'cost_usd':report['total_cost_usd'],
        'site':report['site'],'outages':report['official_source_outages'],'changes':{'added':[after[k] for k in after.keys()-before.keys()],'removed':[before[k] for k in before.keys()-after.keys()]},'envelopes_sha256':sha(work/'envelopes.jsonl')}
    assert source==manifest() and report['site']['largest_profile_bytes']<250000
    save(DEST/'counts.json',result);print(json.dumps(result,ensure_ascii=True)[:3500],flush=True)
if __name__=='__main__':main()
