"""Sequential fresh-state six-sample R4 qualification with seven flags only."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from audit import ROOT, DEST, load_runs


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    env = os.environ.copy()
    env.update(PYTHONUTF8='1', SIGNALPOST_SEARCH_PROVIDER='disabled', SIGNALPOST_SEARCH_MOCK='0')
    manifest = {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted((ROOT / 'src').rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
    save(DEST / 'r4_source_manifest.json', manifest)
    chosen = set(map(int, sys.argv[1:]))
    for seed, previous, registry, before_rows, before_report in load_runs():
        if chosen and seed not in chosen:
            continue
        folder = DEST / ('seed' + str(seed)); folder.mkdir(exist_ok=True)
        settings_folder = ROOT / 'reports/r5' / ({20261017: 'stageT/frozen', 20261113: 'stageT/daily', 20261114: 'stageT/mock'}.get(seed) or f'stageH/seed{seed}')
        previous_settings = json.loads((settings_folder / 'settings.json').read_text(encoding='utf8'))
        original = previous_settings['command_argv']
        organisations = Path(original[original.index('--organisations') + 1]); bulk = Path(original[original.index('--bulk') + 1])
        out = ROOT / '.data/r5' / ('stageR4-' + str(seed) + '-release')
        out.mkdir(exist_ok=False)
        argv = [sys.executable, '-m', 'signalpost.cli', 'run']
        arguments = {'organisations': organisations, 'bulk': bulk, 'output': out / 'envelopes.jsonl', 'profiles-output': out / 'profiles.jsonl',
                     'report': out / 'report.json', 'run-id': 'r5-stageR4-seed' + str(seed) + '-release', 'expected-count': 100}
        for key, value in arguments.items():
            argv.extend(['--' + key, str(value)])
        assert sum(a.startswith('--') for a in argv) == 7
        save(folder / 'settings.json', {'seed': seed, 'working_directory': str(out), 'command_argv': argv, 'exact_seven_flags': True,
                                      'input_sha256': sha(organisations), 'bulk_sha256': sha(bulk), 'source_manifest_sha256': sha(DEST / 'r4_source_manifest.json'),
                                      'parent_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(), 'previous_working_directory': str(previous)})
        print('Starting', seed, datetime.now(timezone.utc).isoformat(), flush=True)
        started = time.monotonic()
        with (folder / 'execution.txt').open('w', encoding='utf8', newline='\n') as log:
            result = subprocess.run(argv, cwd=out, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=2160)
        execution = {'exit_code': result.returncode, 'wall_seconds': time.monotonic() - started, 'argv': argv, 'cwd': str(out)}
        save(folder / 'execution.json', execution)
        if result.returncode:
            raise RuntimeError(f'{seed} exit {result.returncode}; trial retained')
        verify = [sys.executable, str(ROOT / 'scripts/check_live_run.py'), '--output', str(out / 'envelopes.jsonl'), '--organisations', str(organisations),
                  '--state', str(out / 'state'), '--report', str(out / 'report.json'), '--site', str(out / 'site'), '--count', '100']
        checked = subprocess.run(verify, cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf8')
        (folder / 'verification.txt').write_text(checked.stdout + checked.stderr, encoding='utf8', newline='\n')
        if checked.returncode:
            raise RuntimeError(f'{seed} independent verification failed; trial retained')
        save(folder / 'verification.json', json.loads(checked.stdout))
        shutil.copyfile(out / 'report.json', folder / 'report.json')
        rows = [json.loads(line) for line in (out / 'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
        report = json.loads((out / 'report.json').read_text(encoding='utf8'))
        def sites(records):
            return {r['organisation_number']: c['value'] for r in records for c in r['claims'] if c['field'] == 'official_website' and c['availability'] == 'available'}
        old, new = sites(before_rows), sites(rows)
        changed = {'added': {o: new[o] for o in new.keys() - old.keys()}, 'removed': {o: old[o] for o in old.keys() - new.keys()},
                   'url_changed': {o: {'before': old[o], 'after': new[o]} for o in old.keys() & new.keys() if old[o]['final_url'] != new[o]['final_url']}}
        counts = {'seed': seed, 'websites_before': len(old), 'websites_after': len(new), 'http_before': before_report['requests'], 'http_after': report['requests'],
                  'runtime_seconds': execution['wall_seconds'], 'cost_usd': report['total_cost_usd'],
                  'website_states': dict(Counter(r['run']['sections']['website'] for r in rows)),
                  'section_availability_counts': report['counts_by_availability'],
                  'changes': changed, 'envelopes_sha256': sha(out / 'envelopes.jsonl'), 'profiles_sha256': sha(out / 'profiles.jsonl')}
        save(folder / 'counts.json', counts)
        print('Completed', seed, json.dumps(counts, ensure_ascii=True), flush=True)


if __name__ == '__main__':
    main()
