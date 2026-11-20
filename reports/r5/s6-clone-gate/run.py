"""Run final500e in the clean clone; same-run offline repair on a site failure."""
import hashlib,json,os,shutil,subprocess,sys,time
from pathlib import Path
from signalpost.portable_paths import portable_text
ROOT=Path(__file__).resolve().parents[3]
DEST=Path(__file__).resolve().parent
BASE=ROOT/'.data/r5-s6-clone-gate'
CLONE=BASE/'repo'
PY=CLONE/'.venv/Scripts/python.exe'
GIB=1024**3


def save(name,obj):(DEST/name).write_text(portable_text(json.dumps(obj,ensure_ascii=False,indent=2))+'\n',encoding='utf8',newline='\n')
def clean_env():
 e={k:v for k,v in os.environ.items() if not any(t in k.upper() for t in ('TOKEN','SECRET','PASSWORD','API_KEY','CREDENTIAL','AWS_','AZURE_','OPENAI_','ANTHROPIC_','BRAVE_'))}
 e.update(PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',SIGNALPOST_SEARCH_PROVIDER='disabled',SIGNALPOST_SEARCH_MOCK='0');e.pop('SIGNALPOST_WEBSITE_SEEDS',None);return e

def preflight():
 program='''import asyncio,json,hashlib
import httpx
from signalpost.web.policy import safe_transport
async def main():
 out=[]
 async with httpx.AsyncClient(transport=safe_transport(10,{}),trust_env=False,headers={'User-Agent':'SignalpostAgent/1.0','Accept':'application/json'}) as c:
  for url in ['https://data.brreg.no/enhetsregisteret/api/enheter/923609016','https://pam-stilling-feed.nav.no/api/publicToken','https://spedify.no/robots.txt']:
   try:
    r=await c.request('HEAD' if 'publicToken' in url else 'GET',url,timeout=20,follow_redirects=False)
    out.append({'url':url,'status':r.status_code,'bytes':len(r.content),'sha256':hashlib.sha256(r.content).hexdigest()})
   except httpx.HTTPError as e:out.append({'url':url,'error':type(e).__name__})
 print(json.dumps(out))
asyncio.run(main())'''
 for attempt in range(2):
  p=subprocess.run([str(PY),'-c',program],cwd=CLONE,env=clean_env(),capture_output=True,text=True,encoding='utf8')
  result={'attempt':attempt+1,'exit_code':p.returncode,'observations':json.loads(p.stdout) if p.returncode==0 else [],'stderr':p.stderr,'execution_scope':'normal network / production safe transport'}
  save(f'preflight-{attempt+1}.json',result)
  if p.returncode==0 and result['observations'][0].get('status')==200:return
  if attempt==0:time.sleep(15)
 raise RuntimeError('Network preflight failed twice; do not start live 500')


def run_once(attempt):
 work=BASE/('run' if attempt==0 else 'run-retry');assert not work.exists();work.mkdir()
 assert shutil.disk_usage(ROOT).free>=15_000_000_000,'Less than 15 GB immediately before live run'
 args=[str(PY),'-m','signalpost.cli','run','--organisations',str(DEST/'companies500.jsonl'),'--bulk',str(DEST/'registry500.csv'),'--output',str(work/'envelopes.jsonl'),'--profiles-output',str(work/'profiles.jsonl'),'--report',str(work/'report.json'),'--run-id','r5-s6-clone-gate-20261126-s6b','--expected-count','500']
 assert sum(x.startswith('--') for x in args)==7
 started=time.monotonic();samples=[];stopped=None
 with (work/'run-raw.txt').open('wb') as stream:
  p=subprocess.Popen(args,cwd=work,env=clean_env(),stdout=stream,stderr=subprocess.STDOUT)
  while p.poll() is None:
   free=shutil.disk_usage(ROOT).free;elapsed=time.monotonic()-started;samples.append({'elapsed_seconds':round(elapsed,3),'free_bytes':free})
   if free<3*GIB or elapsed>2160:
    stopped='disk_below_3_GiB' if free<3*GIB else 'outer_timeout'
    subprocess.run(['taskkill','/PID',str(p.pid),'/T','/F'],capture_output=True);break
   time.sleep(2)
  exit_code=p.wait()
 wall=time.monotonic()-started;prefix='attempt1' if attempt==0 else 'attempt2'
 (DEST/(prefix+'-run.txt')).write_text(portable_text((work/'run-raw.txt').read_text(encoding='utf8',errors='replace')),encoding='utf8',newline='\n')
 save(prefix+'-execution.json',{'argv':args,'exit_code':exit_code,'process_wall_seconds':wall,'margin_seconds':2100-wall,'stopped':stopped,'fresh_state':True,'flags':7,'code_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=CLONE,text=True).strip(),'work':str(work)})
 save(prefix+'-disk-guard.json',{'minimum_free_bytes':min(x['free_bytes'] for x in samples),'stop_below_bytes':3*GIB,'stopped':stopped,'samples':samples})
 return work,exit_code,wall,stopped


def checked(work,prefix,report=None,site=None):
 args=[str(PY),str(CLONE/'scripts/check_live_run.py'),'--output',str(work/'envelopes.jsonl'),'--organisations',str(DEST/'companies500.jsonl'),'--state',str(work/'state'),'--report',str(report or work/'report.json'),'--site',str(site or work/'site'),'--count','500']
 start=time.monotonic();p=subprocess.run(args,cwd=CLONE,env=clean_env(),capture_output=True,text=True,encoding='utf8')
 (DEST/(prefix+'-check.txt')).write_text(portable_text(p.stdout+p.stderr),encoding='utf8',newline='\n')
 save(prefix+'-check-execution.json',{'argv':args,'exit_code':p.returncode,'wall_seconds':time.monotonic()-start})
 if p.returncode==0:save(prefix+'-check.json',json.loads(p.stdout.strip().splitlines()[-1]))
 return p.returncode


def finish(work,exit_code,wall,checked_exit,attempt):
 report=json.loads((work/'report.json').read_text(encoding='utf8'))
 rows=[json.loads(l) for l in (work/'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
 selectors={'signature':lambda c:c['family']=='signature','signature_rule':lambda c:c['field']=='signature.rule','prokura':lambda c:c['family']=='prokura','prokura_rule':lambda c:c['field']=='prokura.rule','group':lambda c:c['family']=='group','consolidated':lambda c:c['field'].startswith('accounts.consolidated.'),'state_aid':lambda c:c['family']=='state_aid','websites':lambda c:c['field']=='official_website','social':lambda c:c['field'].startswith('social_profile.'),'all_available':lambda c:True}
 counts={k:{'companies':[],'claims':0} for k in selectors}
 for row in rows:
  for k,select in selectors.items():
   matched=[c for c in row['claims'] if c['availability']=='available' and select(c)]
   if matched:counts[k]['companies'].append(row['organisation_number'])
   counts[k]['claims']+=len(matched)
 for x in counts.values():x['companies_covered']=len(x['companies'])
 result={'attempt':attempt+1,'code_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=CLONE,text=True).strip(),'exit_code':exit_code,'checker_exit':checked_exit,'wall_seconds':wall,'margin_seconds':2100-wall,'envelopes':len(rows),'profiles':sum(1 for l in (work/'profiles.jsonl').open(encoding='utf8') if l.strip()),'placeholders':sum(e['code']=='not_started' for row in rows for e in row['errors']),'deadline_hits':report['deadline_hits'],'run_status':report['run_status'],'site':report['site'],'cost_usd':report['total_cost_usd'],'counts':counts,'warnings':report['warnings'],'http_requests':report['requests'],'successful_http_responses':sum(isinstance(e.get('status'),int) and 200<=e['status']<300 for e in report['request_log']),'section_states':{family:{state:sum(row['run']['sections'].get(family)==state for row in rows) for state in sorted({row['run']['sections'].get(family) for row in rows if family in row['run']['sections']})} for family in sorted({f for row in rows for f in row['run']['sections']})},'output_sha256':{name:hashlib.sha256((work/name).read_bytes()).hexdigest() for name in ('envelopes.jsonl','profiles.jsonl','report.json')}}
 save('summary.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('counts','section_states')}) ,flush=True)


def main():
 assert not subprocess.check_output(['git','status','--porcelain'],cwd=CLONE,text=True).strip()
 work,code,wall,stopped=run_once(0)
 if stopped:raise RuntimeError('Guard stopped run: '+stopped)
 check_exit=checked(work,'attempt1')
 finish(work,code,wall,check_exit,0)
if __name__=='__main__':main()
