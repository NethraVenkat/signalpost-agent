"""One seven-flag standard-cohort run, with fresh state and saved verification."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

from signalpost.portable_paths import portable_text

ROOT = Path(__file__).resolve().parents[3]
DEST = Path(__file__).resolve().parent / 'standard100'
WORK = ROOT / 'out/r5-gaps/standard100'
PY = ROOT / '.venv/Scripts/python.exe'
ENV = {k: v for k, v in os.environ.items() if not any(x in k.upper() for x in
       ('TOKEN', 'SECRET', 'PASSWORD', 'API_KEY', 'CREDENTIAL', 'AWS_', 'AZURE_', 'OPENAI_', 'ANTHROPIC_', 'BRAVE_'))}
ENV.update(PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1', SIGNALPOST_SEARCH_PROVIDER='disabled', SIGNALPOST_SEARCH_MOCK='0')


def save(name, value):
    (DEST / name).write_text(portable_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n'), encoding='utf8')


def main():
    assert not WORK.exists(), 'Only one fresh standard-cohort run is authorized'
    DEST.mkdir(exist_ok=True)
    WORK.mkdir()
    companies = ROOT / 'reports/r5/baseline/companies.jsonl'
    bulk = ROOT / 'reports/r5/baseline/registry100.csv'
    args = [str(PY), '-m', 'signalpost.cli', 'run', '--organisations', str(companies),
            '--bulk', str(bulk), '--output', str(WORK / 'envelopes.jsonl'),
            '--profiles-output', str(WORK / 'profiles.jsonl'), '--report', str(WORK / 'report.json'),
            '--run-id', 'r5-gaps-standard100', '--expected-count', '100']
    assert sum(x.startswith('--') for x in args) == 7
    start = time.monotonic()
    minimum = shutil.disk_usage(ROOT).free
    stopped = False
    with (DEST / 'run.txt').open('w', encoding='utf8') as log:
        p = subprocess.Popen(args, cwd=WORK, env=ENV, stdout=log, stderr=subprocess.STDOUT)
        while p.poll() is None:
            free = shutil.disk_usage(ROOT).free
            minimum = min(minimum, free)
            if free < 3 * 1024**3:
                stopped = True
                subprocess.run(['taskkill', '/PID', str(p.pid), '/T', '/F'], capture_output=True)
                p.wait()
                break
            time.sleep(2)
    wall = time.monotonic() - start
    save('execution.json', {'exit_code': p.returncode, 'wall_seconds': wall, 'argv': args,
                           'run_count': 1, 'minimum_free_bytes': minimum, 'stopped_for_low_space': stopped,
                           'code_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                           'input_sha256': hashlib.sha256(companies.read_bytes()).hexdigest()})
    if p.returncode or stopped:
        raise SystemExit('Run failed/stopped; no automatic retry')
    check = subprocess.run([str(PY), str(ROOT / 'scripts/check_live_run.py'), '--output', str(WORK / 'envelopes.jsonl'),
        '--organisations', str(companies), '--state', str(WORK / 'state'), '--report', str(WORK / 'report.json'),
        '--site', str(WORK / 'site'), '--count', '100'], cwd=ROOT, env=ENV, capture_output=True, text=True, encoding='utf8')
    (DEST / 'check_live_run.txt').write_text(portable_text(check.stdout + check.stderr), encoding='utf8')
    save('check_live_run.json', {'exit_code': check.returncode})
    spec = importlib.util.spec_from_file_location('gap_counts', Path(__file__).with_name('counts.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    counts = module.counts(WORK / 'envelopes.jsonl')
    report = json.loads((WORK / 'report.json').read_text(encoding='utf8'))
    save('counts.json', counts)
    save('summary.json', {'wall_seconds': wall, 'margin_seconds': 2100-wall, 'exit_code': p.returncode,
        'envelopes': counts['envelopes'], 'deadline_hits': report['deadline_hits'], 'run_status': report['run_status'],
        'largest_profile_bytes': report['site']['largest_profile_bytes'], 'cost_usd': report['total_cost_usd'],
        'counts': counts['information_types'], 'check_live_run_exit_code': check.returncode})
    print(json.dumps({'exit_code': p.returncode, 'wall_seconds': wall, 'check_exit_code': check.returncode}), flush=True)
    if check.returncode:
        raise SystemExit('Verification failed; no automatic retry')


if __name__ == '__main__':
    main()
