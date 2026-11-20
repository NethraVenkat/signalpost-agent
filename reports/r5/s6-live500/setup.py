import hashlib,json,shutil,subprocess,sys,os
from pathlib import Path
from signalpost.portable_paths import portable_text
ROOT=Path(__file__).resolve().parents[3];DEST=Path(__file__).resolve().parent;BASE=ROOT/'.data/r5-s6-live500';CLONE=BASE/'repo'
def command(args,cwd):
 r=subprocess.run([str(a) for a in args],cwd=cwd,capture_output=True,text=True,encoding='utf8',errors='replace');assert r.returncode==0,portable_text(r.stdout+r.stderr);return r.stdout
def main():
 assert not BASE.exists()
 assert shutil.disk_usage(ROOT).free>=15_000_000_000
 baseline=ROOT/'reports/r5/final500e';meta=json.loads((baseline/'sampling.json').read_text())
 for name,key in [('companies500.jsonl','inputs_sha256'),('registry500.csv','bulk_sha256')]:
  raw=(baseline/name).read_bytes();assert hashlib.sha256(raw).hexdigest()==meta[key];(DEST/name).write_bytes(raw)
 (DEST/'sampling.json').write_text(json.dumps(meta,indent=2)+'\n')
 BASE.mkdir();head=command(['git','rev-parse','HEAD'],ROOT).strip()
 command(['git','clone','--config','core.autocrlf=false','--no-hardlinks','--no-tags','--single-branch','--branch','revision/r5',ROOT,CLONE],ROOT)
 for key in ['user.name','user.email']:command(['git','config',key,command(['git','config','--local',key],ROOT).strip()],CLONE)
 assert command(['git','rev-parse','HEAD'],CLONE).strip()==head
 command(['uv','sync','--frozen','--no-dev','--python',sys.executable],CLONE)
 assert not command(['git','status','--porcelain'],CLONE).strip()
 py=CLONE/'.venv/Scripts/python.exe';command([py,'-c',"import importlib.util;assert importlib.util.find_spec('pytest') is None"],CLONE)
 free=shutil.disk_usage(ROOT).free;assert free>=15_000_000_000
 (DEST/'clean-clone.json').write_text(json.dumps(dict(head=head,clean=True,pytest_in_clone=False,free_after_setup_bytes=free,cohort_identical_to_final500e=True),indent=2)+'\n')
 print(head,free)
if __name__=='__main__':main()
