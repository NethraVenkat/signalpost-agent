"""Isolated live runner with external load sampling; psutil is a tool-only extra."""
import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from datetime import datetime,timezone
from pathlib import Path
import psutil


def sample_tree(process,observed):
    members=[]
    try:tree=[process]+process.children(recursive=True)
    except (psutil.NoSuchProcess,psutil.AccessDenied):tree=[process]
    for member in tree:
        try:
            identity=(member.pid,member.create_time())
            rss=member.memory_info().rss
            record={'pid':member.pid,'created_at':identity[1],'role':'launched_root' if member.pid==process.pid else 'pipeline_descendant',
                    'rss_bytes':rss,'cpu_seconds':sum(member.cpu_times()[:2])}
            members.append(record)
            prior=observed.setdefault(identity,{**record,'peak_rss_bytes':0})
            prior['peak_rss_bytes']=max(prior['peak_rss_bytes'],rss)
        except (psutil.NoSuchProcess,psutil.AccessDenied):pass
    return members


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,required=True);parser.add_argument('--bulk',type=Path)
    parser.add_argument('--output-dir',type=Path,required=True);parser.add_argument('--count',type=int,required=True)
    parser.add_argument('--input-sha256');parser.add_argument('--time-budget',type=int,default=2400)
    parser.add_argument('--max-requests',type=int,default=2000)
    args=parser.parse_args();sha=hashlib.sha256(args.input.read_bytes()).hexdigest()
    if args.input_sha256 and sha!=args.input_sha256:raise ValueError('Input hash mismatch')
    if args.output_dir.exists():raise ValueError('Use a new output directory and state')
    # Guard against this project's test/browser jobs. Never terminate processes.
    conflicts=[];unknown=0
    for proc in psutil.process_iter(['pid','name','cmdline']):
        try:
            command=' '.join(proc.info['cmdline'] or [])
            if proc.pid!=os.getpid() and 'Signalpost' in command and any(x in command for x in ['-m pytest','pytest --cov','scripts/browser_verify.py']):conflicts.append(proc.pid)
        except (psutil.AccessDenied,psutil.NoSuchProcess):unknown+=1
    if conflicts:raise RuntimeError(f'Concurrent test/browser jobs: {conflicts}')
    out=args.output_dir;out.mkdir(parents=True)
    cmd=[sys.executable,'-m','signalpost.cli','run','--organisations',str(args.input),
        '--output',str(out/'envelopes.jsonl'),'--profiles-output',str(out/'profiles.jsonl'),
        '--report',str(out/'report.json'),'--site-dir',str(out/'site'),'--state-dir',str(out/'state'),
        '--websites','--hiring','--public-activity','--max-cost-usd','0','--search-max-queries','0',
        '--max-requests',str(args.max_requests),
        '--time-budget-seconds',str(args.time_budget),'--expected-count',str(args.count)]
    if args.bulk:cmd+=['--bulk',str(args.bulk)]
    env=os.environ.copy()
    for name in ['BRAVE_SEARCH_API_KEY','SIGNALPOST_SEARCH_PROVIDER']:env.pop(name,None)
    env['PYTHONUTF8']='1'
    metadata={'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        'input_sha256':sha,'bulk_sha256':hashlib.sha256(args.bulk.read_bytes()).hexdigest() if args.bulk else None,
        'command':cmd,'observation_start':datetime.now(timezone.utc).isoformat(),'python':sys.version,
        'platform':platform.platform(),'processor':platform.processor(),'logical_cpus':os.cpu_count(),
        'ram_bytes':psutil.virtual_memory().total,'unknown_process_inspections':unknown,
        'conditions':'Fresh empty runtime state; shipped declared NAV index; paid search disabled; no evaluation test/browser job detected. Unrelated processes preserved.'}
    samples=[];observed={};psutil.cpu_percent();began=time.perf_counter()
    with (out/'process.log').open('wb') as log:
        process=psutil.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,env=env)
        while True:
            sample={'elapsed_seconds':time.perf_counter()-began,'system_cpu_percent':psutil.cpu_percent(),
                'available_ram_bytes':psutil.virtual_memory().available,'memory_percent':psutil.virtual_memory().percent}
            try:
                sample.update(process_rss_bytes=process.memory_info().rss,process_cpu_seconds=sum(process.cpu_times()[:2]),
                    process_threads=process.num_threads())
                io=process.io_counters();sample.update(process_read_bytes=io.read_bytes,process_write_bytes=io.write_bytes)
            except (psutil.NoSuchProcess,psutil.AccessDenied):pass
            members=sample_tree(process,observed)
            sample['process_tree']=members
            sample['process_tree_rss_bytes']=sum(m['rss_bytes'] for m in members)
            disk=psutil.disk_io_counters()
            if disk:sample.update(disk_read_bytes=disk.read_bytes,disk_write_bytes=disk.write_bytes,disk_read_ms=disk.read_time,disk_write_ms=disk.write_time)
            samples.append(sample)
            try:code=process.wait(timeout=1);break
            except psutil.TimeoutExpired:pass
    metadata.update(wall_seconds=time.perf_counter()-began,exit_code=code,observation_end=datetime.now(timezone.utc).isoformat(),samples=samples,
                    memory={'sampling_interval_seconds':1,'observed_peak_tree_rss_bytes':max((s['process_tree_rss_bytes'] for s in samples),default=0),
                            'observed_processes':list(observed.values()),
                            'scope':'Launched root plus recursive descendants, including actual Python pipeline behind Windows launchers; summed RSS may double count shared pages; brief peaks/exited children between samples may be missed. Not system available RAM.'})
    (out/'measurement.json').write_text(json.dumps(metadata,ensure_ascii=True,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in metadata.items() if k not in ['samples','command']}))
    raise SystemExit(code)


if __name__=='__main__':main()
