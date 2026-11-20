"""Prepare one disjoint 500 cohort and clean clone; never runs pytest."""
import csv,gzip,hashlib,json,os,random,shutil,subprocess,sys,time
from pathlib import Path
from signalpost.identity.orgnr import valid
from signalpost.portable_paths import portable_text
ROOT=Path(__file__).resolve().parents[3]
DEST=Path(__file__).resolve().parent
BASE=ROOT/'.data/r5-final500e'
CLONE=BASE/'repo'
SEED=20261126
UNIVERSE=ROOT/'.data/r5/inputs/universe-20261116/universe.jsonl.gz'
BULK=ROOT/'.data/r5/inputs/brreg-enheter-20261116/enheter_2026-11-16T04-25-21.340365166.csv.gz'
GIB=1024**3


def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def save(name,data):(DEST/name).write_text(portable_text(json.dumps(data,ensure_ascii=False,indent=2))+'\n',encoding='utf8',newline='\n')
def env():
 e={k:v for k,v in os.environ.items() if not any(t in k.upper() for t in ('TOKEN','SECRET','PASSWORD','API_KEY','CREDENTIAL','AWS_','AZURE_','OPENAI_','ANTHROPIC_','BRAVE_'))}
 e.update(PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',SIGNALPOST_SEARCH_PROVIDER='disabled',SIGNALPOST_SEARCH_MOCK='0');e.pop('SIGNALPOST_WEBSITE_SEEDS',None);return e

def command(args,cwd):
 r=subprocess.run([str(a) for a in args],cwd=cwd,env=env(),capture_output=True,text=True,encoding='utf8',errors='replace')
 assert r.returncode==0,portable_text(r.stdout+r.stderr)[-4000:]
 return r.stdout

def extract_numbers(obj):
 result=set()
 if isinstance(obj,dict):
  for key,value in obj.items():
   if key in {'organisation_number','organisasjonsnummer','org','orgnr'} and isinstance(value,(str,int)):
    x=str(value)
    if valid(x):result.add(x)
   elif isinstance(value,(dict,list)):result.update(extract_numbers(value))
 elif isinstance(obj,list):
  for value in obj:
   if isinstance(value,str) and valid(value):result.add(value)
   elif isinstance(value,(dict,list)):result.update(extract_numbers(value))
 return result

def setup():
 assert not BASE.exists(),'Fresh clean clone only; preserve any existing attempt'
 before=shutil.disk_usage(ROOT).free
 save('initial-disk.json',{'free_bytes':before,'minimum_required_bytes':15*GIB,'stop_below_bytes':3*GIB})
 assert before>=15*GIB,'Free disk below 15 GiB'
 excluded=set();sources={}
 ledger=ROOT/'reports/r5/gaps/prior-sample-exclusions.json'
 frozen=json.loads(ledger.read_text(encoding='utf8'));excluded.update(frozen['organisation_numbers'])
 sources[str(ledger.relative_to(ROOT))]={'sha256':sha(ledger),'numbers':len(excluded)}
 candidates=[]
 for top in [ROOT/'reports',ROOT/'out',ROOT/'.data/r5/inputs']:
  for directory,dirs,files in os.walk(top):
   dirs[:]=[d for d in dirs if d not in {'repo','state','blobs','site','.venv','.git','__pycache__','tmp','node_modules'} and not d.startswith(('pytest','test_'))]
   for name in files:
    low=name.lower()
    if not any(t in low for t in ('compan','batch','selection','sample','seed','probe')):continue
    p=Path(directory)/name
    if p.is_symlink() or p.suffix.lower() not in {'.json','.jsonl','.txt','.csv'} or p.stat().st_size>8*1024**2:continue
    if DEST in p.parents:continue
    candidates.append(p)
 for p in sorted(set(candidates)):
  try:
   text=p.read_text(encoding='utf-8-sig');numbers=set()
   if p.suffix=='.json':numbers=extract_numbers(json.loads(text))
   elif p.suffix=='.jsonl':
    for line in text.splitlines():
     if line.strip():numbers.update(extract_numbers(json.loads(line)))
   elif p.suffix=='.csv':
    for row in csv.DictReader(text.splitlines()):numbers.update(extract_numbers(row))
   else:numbers={l.strip() for l in text.splitlines() if valid(l.strip())}
   if numbers:excluded.update(numbers);sources[p.relative_to(ROOT).as_posix()]={'sha256':sha(p),'numbers':len(numbers)}
  except (OSError,UnicodeError,ValueError,csv.Error):continue
 assert sha(UNIVERSE)=='1c89710e5b01f8617e86d09fbdff4a52f2f8dbbba297e74f7164b5984f5a0384'
 content=hashlib.sha256();eligible=[];seen=set();rows=0
 with gzip.open(UNIVERSE,'rb') as stream:
  for line in stream:
   content.update(line);rows+=1;record=json.loads(line);org=str(record['organisation_number'])
   if org not in seen and org not in excluded and valid(org):eligible.append(org)
   seen.add(org)
 assert rows==411160 and content.hexdigest()=='b82d6a3e7231d1759a958c282bc4366b80ec2fab8095053d8ed7fa9cd01bc838'
 sample=random.Random(SEED).sample(eligible,500)
 assert len(set(sample))==500 and not set(sample)&excluded
 inputs=DEST/'companies500.jsonl';inputs.write_text(''.join(json.dumps({'organisation_number':x})+'\n' for x in sample),encoding='utf8',newline='\n')
 snapshot=sha(BULK);assert snapshot=='56922f51839e7ed3f3c9adde50dbcfa375202d7bc5aa998d9572158e228693e1'
 found=set();wanted=set(sample)
 with gzip.open(BULK,'rt',encoding='utf-8-sig',newline='') as source,(DEST/'registry500.csv').open('w',encoding='utf8',newline='') as target:
  reader=csv.DictReader(source);writer=csv.DictWriter(target,fieldnames=reader.fieldnames);writer.writeheader()
  for row in reader:
   if row['organisasjonsnummer'] in wanted:
    writer.writerow(row);found.add(row['organisasjonsnummer'])
    if len(found)==500:break
 save('exclusions.json',{'organisation_numbers':sorted(excluded),'unique_numbers':len(excluded),'sources':sources})
 save('sampling.json',{'seed':SEED,'universe_rows':rows,'eligible':len(eligible),'excluded':len(excluded),'overlap':0,'inputs_sha256':sha(inputs),'bulk_sha256':sha(DEST/'registry500.csv'),'bulk_rows':len(found),'live_identity_fallback_numbers':sorted(wanted-found),'universe_sha256':sha(UNIVERSE),'universe_content_sha256':content.hexdigest(),'registry_snapshot_sha256':snapshot})
 BASE.mkdir()
 head=command(['git','rev-parse','HEAD'],ROOT).strip()
 command(['git','clone','--no-hardlinks','--no-tags','--single-branch','--branch','revision/r5',ROOT,CLONE],ROOT)
 command(['git','config','user.name','Nethra Venkat'],CLONE);command(['git','config','user.email','nethravenkat510@gmail.com'],CLONE)
 assert command(['git','rev-parse','HEAD'],CLONE).strip()==head
 assert not command(['git','status','--porcelain'],CLONE).strip()
 install=command(['uv','sync','--frozen','--no-dev','--python',sys.executable],CLONE)
 py=CLONE/'.venv/Scripts/python.exe'
 meta=json.loads(command([py,'-c',"import sys,json,signalpost,importlib.util;print(json.dumps({'module':signalpost.__file__,'prefix':sys.prefix,'python':sys.version,'pytest_installed':importlib.util.find_spec('pytest') is not None}))"],CLONE))
 assert Path(meta['prefix']).resolve()==(CLONE/'.venv').resolve() and not meta['pytest_installed']
 proof=command([py,CLONE/'reports/r5/precision-sample/replay.py','check'],CLONE)
 save('P1-clone-replay.json',{'exit_code':0,'results':json.loads(proof),'network_disabled':True,'local_run_directories_present':False,'pytest_in_clone':False})
 assert not command(['git','status','--porcelain'],CLONE).strip(),'Clone changed after P1 replay'
 after=shutil.disk_usage(ROOT).free
 metadata={'head':head,'clone_clean':True,'pytest_in_clone':False,'installation':meta,'free_before_bytes':before,'free_after_setup_bytes':after,'minimum_required_bytes':15*GIB,'source_tree_sha256':{str(p.relative_to(CLONE)):sha(p) for p in (CLONE/'src/signalpost').rglob('*.py')}}
 save('clean-clone.json',metadata)
 assert after>=15*GIB,'Free disk below 15 GiB after setup'
 print(json.dumps({'head':head,'free_after':after,'excluded':len(excluded),'sample':500,'bulk':len(found),'P1_clone_replay':'passed'}),flush=True)

if __name__=='__main__':setup()
