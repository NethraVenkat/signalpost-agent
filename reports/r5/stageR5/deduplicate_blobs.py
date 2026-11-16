"""Lossless workspace-only saved-blob deduplication after disk exhaustion."""
from signalpost.portable_paths import portable, portable_text  # saved paths stay repo-relative
import hashlib
import json
import os
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parents[3]
BASE=(ROOT/'.data/r5').resolve()


def main():
    before=shutil.disk_usage(ROOT).free
    canonical={};linked=0;logical=0;checked=0
    # Existing evidence is immutable. Never import another workspace's files.
    for run in sorted(BASE.iterdir()):
        folder=run/'state/blobs'
        if not folder.is_dir():continue
        assert folder.resolve().is_relative_to(BASE)
        for path in folder.iterdir():
            if not path.is_file() or len(path.name)!=64:continue
            size=path.stat().st_size
            if size<4096:continue
            if path.name not in canonical:
                canonical[path.name]=path
                continue
            other=canonical[path.name]
            if os.path.samefile(path,other):continue
            assert path.resolve().is_relative_to(BASE) and other.resolve().is_relative_to(BASE)
            assert path.read_bytes()==other.read_bytes(),'Hash name collision/corrupt blob'
            assert hashlib.sha256(path.read_bytes()).hexdigest()==path.name
            checked+=1
            temporary=path.with_name(path.name+'.dedup-link')
            assert not temporary.exists()
            os.link(other,temporary)
            os.replace(temporary,path)
            assert os.path.samefile(path,other)
            linked+=1;logical+=size
    result={'method':'Verified identical bytes and SHA-256, atomic hard-link replacement; all original paths and bytes retained, workspace .data/r5 only.',
        'linked_blobs':linked,'bytes_deduplicated':logical,'checked_blobs':checked,'free_before':before,'free_after':shutil.disk_usage(ROOT).free}
    (Path(__file__).parent/'blob_deduplication.json').write_text(portable_text(json.dumps(result,indent=2)+'\n'),encoding='utf8')
    print(json.dumps(result))


if __name__=='__main__':main()
