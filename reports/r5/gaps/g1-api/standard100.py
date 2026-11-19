"""One fresh standard-100 run and saved-output check, with seven evaluator flags."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
from signalpost.portable_paths import portable_text

ROOT=Path(__file__).resolve().parents[4]
DEST=Path(__file__).resolve().parent
WORK=ROOT/'out/g1-api-standard100'
PYTHON=ROOT/'.venv/Scripts/python.exe'
INPUT=ROOT/'reports/r5/baseline/companies.jsonl'
BULK=ROOT/'reports/r5/baseline/registry100.csv'
BASELINE=ROOT/'out/r5-gaps/standard100/envelopes.jsonl'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(name, obj):
    (DEST/name).write_text(portable_text(json.dumps(obj,ensure_ascii=False,indent=2))+'\n',encoding='utf8',newline='\n')


def census(path):
    rows=[json.loads(line) for line in path.read_text(encoding='utf8').splitlines()]
    out={key:{'companies':[],'claims':0} for key in ('signature','prokura','group','total')}
    for row in rows:
        claims=[c for c in row['claims'] if c['availability']=='available']
        for key in out:
            matched=claims if key=='total' else [c for c in claims if c['family']==key]
            if matched:out[key]['companies'].append(row['organisation_number'])
            out[key]['claims']+=len(matched)
    for val in out.values():val['companies_covered']=len(val['companies'])
    return out


def main():
    assert not WORK.exists(), 'One fresh-state run only; inspect existing receipts before retrying'
    baseline_execution=json.loads((ROOT/'reports/r5/gaps/standard100/execution.json').read_text(encoding='utf8'))
    assert sha(INPUT)==baseline_execution['input_sha256'], 'Standard cohort membership changed'
    WORK.mkdir()
    code=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    env={k:v for k,v in os.environ.items() if not any(x in k.upper() for x in ('TOKEN','SECRET','PASSWORD','API_KEY','CREDENTIAL','AWS_','AZURE_','OPENAI_','ANTHROPIC_'))}
    env.update(PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',SIGNALPOST_SEARCH_PROVIDER='disabled',SIGNALPOST_SEARCH_MOCK='0')
    env.pop('SIGNALPOST_WEBSITE_SEEDS',None)
    args=[str(PYTHON),'-m','signalpost.cli','run','--organisations',str(INPUT),'--bulk',str(BULK),'--output',str(WORK/'envelopes.jsonl'),'--profiles-output',str(WORK/'profiles.jsonl'),'--report',str(WORK/'report.json'),'--run-id','g1-api-standard100','--expected-count','100']
    assert sum(x.startswith('--') for x in args)==7
    minimum=shutil.disk_usage(ROOT).free
    assert minimum>=3*1024**3, 'Insufficient free disk'
    began=time.monotonic();stopped=False
    with (WORK/'run-raw.txt').open('wb') as stream:
        process=subprocess.Popen(args,cwd=WORK,env=env,stdout=stream,stderr=subprocess.STDOUT)
        while process.poll() is None:
            minimum=min(minimum,shutil.disk_usage(ROOT).free)
            if minimum<3*1024**3 or time.monotonic()-began>2160:
                process.terminate();stopped=True;break
            time.sleep(2)
        code_exit=process.wait()
    wall=time.monotonic()-began
    (DEST/'standard100-run.txt').write_text(portable_text((WORK/'run-raw.txt').read_text(encoding='utf8',errors='replace')),encoding='utf8',newline='\n')
    save('standard100-execution.json',{'code_commit':code,'baseline_commit':'ac88ab0','argv':args,'exit_code':code_exit,'wall_seconds':wall,'margin_seconds':2100-wall,'minimum_free_bytes':minimum,'stopped':stopped,'flags':7,'fresh_state':True,'input_sha256':sha(INPUT),'bulk_sha256':sha(BULK),'baseline_saved_envelopes_sha256':sha(BASELINE),'baseline_scope':'Original standard-100 measurement at f740933 retained by ac88ab0; ac88ab0 fixes only site overflow and adaptive I/O isolation; no newly measured baseline live run.'})
    assert code_exit==0 and not stopped, 'Live run did not complete normally'
    check=[str(PYTHON),str(ROOT/'scripts/check_live_run.py'),'--output',str(WORK/'envelopes.jsonl'),'--organisations',str(INPUT),'--state',str(WORK/'state'),'--report',str(WORK/'report.json'),'--site',str(WORK/'site'),'--count','100']
    began=time.monotonic();checked=subprocess.run(check,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf8')
    (DEST/'standard100-check.txt').write_text(portable_text(checked.stdout+checked.stderr),encoding='utf8',newline='\n')
    save('standard100-check-execution.json',{'argv':check,'exit_code':checked.returncode,'wall_seconds':time.monotonic()-began})
    report=json.loads((WORK/'report.json').read_text(encoding='utf8'))
    rows=[json.loads(line) for line in (WORK/'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
    placeholders=sum(e['code']=='not_started' for row in rows for e in row['errors'])
    result={'baseline':census(BASELINE),'current':census(WORK/'envelopes.jsonl'),'run_status':report['run_status'],'exit_code':code_exit,'checker_exit':checked.returncode,'wall_seconds':wall,'margin_seconds':2100-wall,'deadline_hits':report['deadline_hits'],'placeholders':placeholders,'envelopes':len(rows),'site':report['site'],'cost_usd':report['total_cost_usd'],'corporate_section_states':{family:{state:sum(row['run']['sections'][family]==state for row in rows) for state in sorted({row['run']['sections'][family] for row in rows})} for family in ('signature','prokura','group')}}
    save('standard100-counts.json',result)
    if checked.returncode==0:
        save('standard100-check.json',json.loads(checked.stdout.strip().splitlines()[-1]))
    print(json.dumps({'checker_exit':checked.returncode,'wall_seconds':wall,'counts':result['current'],'largest_profile_bytes':report['site'].get('largest_profile_bytes')}),flush=True)
    assert checked.returncode==0 and placeholders==0


if __name__=='__main__':
    main()
