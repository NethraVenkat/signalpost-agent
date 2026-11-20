"""Lossless, verified archival of explicit completed historical run directories."""
import hashlib,json,os,sys,time,zipfile
from pathlib import Path
from signalpost.portable_paths import portable_text
ROOT=Path(__file__).resolve().parents[3]
name=sys.argv[1]
assert '/' not in name and '\\' not in name and name not in {'.','..','inputs'}
source=(ROOT/'.data/r5'/name).resolve();assert source.parent==(ROOT/'.data/r5').resolve()
assert source.exists() and not source.is_symlink() and not source.is_junction()
dest=ROOT/'.data/reclaimed-evidence';dest.mkdir(exist_ok=True)
archive=dest/(name+'.zip');entries=[];total=0
for directory,dirs,files in os.walk(source,followlinks=False):
 for n in dirs+files:
  p=Path(directory)/n;assert not p.is_symlink() and not p.is_junction(),str(p)
 for n in files:
  p=Path(directory)/n
  with p.open('rb') as stream:h=hashlib.file_digest(stream,'sha256').hexdigest()
  entries.append((p,p.relative_to(source.parent).as_posix(),h));total+=p.stat().st_size
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
 for p,n,h in entries:z.write(p,n)
 for directory,dirs,files in os.walk(source):
  if not dirs and not files:z.writestr(Path(directory).relative_to(source.parent).as_posix()+'/',b'')
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for p,n,h in entries:
  with z.open(n) as stream:assert hashlib.file_digest(stream,'sha256').hexdigest()==h,n
  with p.open('rb') as stream:assert hashlib.file_digest(stream,'sha256').hexdigest()==h,'Original changed: '+n
with archive.open('rb') as stream:archive_sha=hashlib.file_digest(stream,'sha256').hexdigest()
manifest={'directory':name,'files':len(entries),'original_bytes':total,'archive_bytes':archive.stat().st_size,'archive_sha256':archive_sha,'all_original_and_archived_file_hashes_match':True,'verified':True,'restore':'Extract '+archive.name+' into <REPO>/.data/r5','file_hashes':[[n,h] for p,n,h in entries]}
(dest/(name+'.manifest.json')).write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8',newline='\n')
summary={k:v for k,v in manifest.items() if k!='file_hashes'}
out=Path(__file__).with_name('archival.json');existing=json.loads(out.read_text()) if out.exists() else []
existing.append(summary);out.write_text(portable_text(json.dumps(existing,indent=2))+'\n',encoding='utf8',newline='\n')
print(json.dumps(summary),flush=True)
