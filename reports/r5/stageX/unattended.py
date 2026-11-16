"""One fresh-state retry per failed sample, preserving every attempt."""
from signalpost.portable_paths import portable, portable_text, sanitize_file  # saved paths stay repo-relative
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from measure import ROOT,SEEDS,folder


def main():
    stage=sys.argv[1];dest=folder(stage);dest.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy();env['PYTHONUTF8']='1'
    records=[]
    for seed in SEEDS:
        for attempt,label in enumerate(('unattended','unattended-retry')):
            env['SIGNALPOST_MEASUREMENT_LABEL']=label
            print('Starting',stage,seed,label,flush=True)
            start=time.monotonic()
            with (dest/f'{seed}-{label}.txt').open('w',encoding='utf8') as log:
                result=subprocess.run([sys.executable,str(ROOT/'reports/r5/stageX/measure.py'),stage,str(seed)],cwd=ROOT,env=env,
                    stdout=log,stderr=subprocess.STDOUT)
            sanitize_file(dest/f'{seed}-{label}.txt')  # keep captured paths repo-relative
            output=dest/f'seed{seed}'
            counts_path=output/'counts.json'
            outage=False
            if result.returncode==0 and counts_path.exists():
                counts=json.loads(counts_path.read_text(encoding='utf8'))
                outage=counts['before']['websites']>0 and counts['after']['websites']==0 and counts['after']['activity_claims']==0
            record={'seed':seed,'attempt':attempt+1,'label':label,'exit_code':result.returncode,'wall_seconds':time.monotonic()-start,'source_outage':outage}
            records.append(record)
            (dest/'unattended_attempts.json').write_text(portable_text(json.dumps(records,indent=2)+'\n'),encoding='utf8')
            if result.returncode==0 and not outage:break
            trial=dest/'trials'/f'{seed}-{label}';trial.mkdir(parents=True,exist_ok=True)
            if output.exists():shutil.copytree(output,trial/'receipts',dirs_exist_ok=True)
            if attempt:raise RuntimeError(f'{seed}: one allowed retry failed; retained checkpoint evidence')
        print('Completed',stage,seed,flush=True)


if __name__=='__main__':main()
