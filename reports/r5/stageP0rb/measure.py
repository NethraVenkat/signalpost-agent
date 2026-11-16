"""P0 re-baseline on new machine: one fresh exact-seven-flag sample per call.

Old run outputs did not survive the move to a new machine, so this records a new
local reference for later stages. It is NOT compared with lost folders: no
before/after diff. Inputs are the committed frozen cohort files named in the X2
settings, verified against their recorded SHA-256 before use.
"""
from signalpost.portable_paths import expand, portable_text, sanitize_file  # saved paths stay repo-relative
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEST = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'reports/r5/stageX'))
from measure import counts, identities  # noqa: E402  (same counting definitions as stage X)

SEEDS = (20261017, 20261113, 20261114, 20261115, 20261116, 20261117)


def save(path, value):
    path.write_text(portable_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n'), encoding='utf8', newline='\n')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def manifest():
    out = {}
    for p in sorted((ROOT / 'src').rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts:
            raw = p.read_bytes()
            out[p.relative_to(ROOT).as_posix()] = {'worktree_sha256': hashlib.sha256(raw).hexdigest(),
                                                   'lf_sha256': hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest()}
    return out


def main():
    seed = int(sys.argv[1]); assert seed in SEEDS
    label = os.environ.get('SIGNALPOST_MEASUREMENT_LABEL', 'final')
    assert label in {'final', 'retry'}
    DEST.mkdir(parents=True, exist_ok=True)
    source = manifest()
    if (DEST / 'source_manifest.json').exists():
        assert json.loads((DEST / 'source_manifest.json').read_text(encoding='utf8')) == source, 'runtime source changed between samples'
    else:
        save(DEST / 'source_manifest.json', source)
    old = json.loads((ROOT / f'reports/r5/stageX/X2/seed{seed}/settings.json').read_text(encoding='utf8'))
    a = old['command_argv']
    orgs = Path(expand(a[a.index('--organisations') + 1])); bulk = Path(expand(a[a.index('--bulk') + 1]))
    assert sha(orgs) == old['input_sha256'] and sha(bulk) == old['bulk_sha256'], 'frozen input hash mismatch'
    env = os.environ.copy(); env.update(PYTHONUTF8='1', SIGNALPOST_SEARCH_PROVIDER='disabled', SIGNALPOST_SEARCH_MOCK='0')
    work = ROOT / '.data/r5' / f'stageP0rb-{seed}-{label}'; work.mkdir(parents=True, exist_ok=False)
    output = DEST / f'seed{seed}' if label == 'final' else DEST / 'trials' / f'seed{seed}-{label}'
    output.mkdir(parents=True, exist_ok=False)
    argv = [sys.executable, '-m', 'signalpost.cli', 'run']
    for key, value in {'organisations': orgs, 'bulk': bulk, 'output': work / 'envelopes.jsonl',
                       'profiles-output': work / 'profiles.jsonl', 'report': work / 'report.json',
                       'run-id': f'r5-stageP0rb-seed{seed}-{label}', 'expected-count': 100}.items():
        argv.extend(['--' + key, str(value)])
    assert sum(x.startswith('--') for x in argv) == 7
    save(output / 'settings.json', {
        'seed': seed, 'stage': 'P0 re-baseline on new machine', 'working_directory': str(work), 'command_argv': argv,
        'exact_seven_flags': True, 'input_sha256': sha(orgs), 'bulk_sha256': sha(bulk),
        'source_manifest_sha256': sha(DEST / 'source_manifest.json'),
        'parent_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'comparison': 'none (new local reference; earlier run folders were not transferred)'})
    print('Starting', seed, flush=True); started = time.monotonic()
    with (output / 'execution.txt').open('w', encoding='utf8', newline='\n') as log:
        executed = subprocess.run(argv, cwd=work, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=2160)
    sanitize_file(output / 'execution.txt')  # keep captured paths repo-relative
    save(output / 'execution.json', {'exit_code': executed.returncode, 'wall_seconds': time.monotonic() - started,
                                     'argv': argv, 'cwd': str(work)})
    assert executed.returncode == 0
    checked = subprocess.run([sys.executable, str(ROOT / 'scripts/check_live_run.py'), '--output', str(work / 'envelopes.jsonl'),
                              '--organisations', str(orgs), '--state', str(work / 'state'), '--report', str(work / 'report.json'),
                              '--site', str(work / 'site'), '--count', '100'],
                             cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf8')
    (output / 'verification.txt').write_text(portable_text(checked.stdout + checked.stderr), encoding='utf8', newline='\n')
    assert checked.returncode == 0, 'check_live_run failed'
    save(output / 'verification.json', json.loads(checked.stdout))
    shutil.copyfile(work / 'report.json', output / 'report.json'); sanitize_file(output / 'report.json')
    rows = [json.loads(s) for s in (work / 'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
    report = json.loads((work / 'report.json').read_text(encoding='utf8'))
    assert report['site']['state'] == 'available' and report['site']['largest_profile_bytes'] < 250000, 'site gate failed'
    items = identities(rows)
    save(output / 'counts.json', {
        'seed': seed, 'counts': counts(rows), 'HTTP': report['requests'],
        'CLI_runtime_seconds': json.loads((output / 'execution.json').read_text(encoding='utf8'))['wall_seconds'],
        'cost_usd': report['total_cost_usd'], 'site': report['site'],
        'identity_items': sorted([{k: v for k, v in i.items() if k != 'evidence'} for i in items.values()],
                                 key=lambda i: (i['orgnr'], i['kind'], str(i['identity']))),
        'envelopes_sha256': sha(work / 'envelopes.jsonl'), 'profiles_sha256': sha(work / 'profiles.jsonl')})
    assert source == manifest(), 'runtime source changed during measurement'
    print('Completed', seed, json.dumps({'counts': counts(rows), 'HTTP': report['requests'], 'site': report['site']['state']}), flush=True)


if __name__ == '__main__':
    main()
