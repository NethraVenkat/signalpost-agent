"""Stage S site re-render: rebuild each sample's static site from its SAVED envelopes
with the final site code, then re-run check_live_run. No recrawl, no union of runs.

Why: seed 20261117's single run completed (exit 0, 100 envelopes) but site generation
raised the 250 KB profile gate (company 948039958 gained 27 inspections + 9 state-aid
records on a page already at 249 KB). The fix defers older official records to the
local data file. Rendering changed for every sample, so all six sites are rebuilt.
The run's own report.json is preserved as report-run.json.
"""
from signalpost.portable_paths import expand, portable_text, sanitize_file
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEST = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'reports/r5/stageX'))
from measure import counts  # noqa: E402

SEEDS = (20261017, 20261113, 20261114, 20261115, 20261116, 20261117)


def save(path, value):
    path.write_text(portable_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n'), encoding='utf8', newline='\n')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    seed = int(sys.argv[1]); assert seed in SEEDS
    out = DEST / f'seed{seed}'; work = ROOT / '.data/r5' / f'stageS-{seed}-final'
    settings = json.loads((out / 'settings.json').read_text(encoding='utf8'))
    a = settings['command_argv']; orgs = expand(a[a.index('--organisations') + 1])
    env = os.environ.copy(); env.update(PYTHONUTF8='1')
    report = json.loads((work / 'report.json').read_text(encoding='utf8'))
    if not (work / 'report-run.json').exists():
        shutil.copyfile(work / 'report.json', work / 'report-run.json')
    run_report = json.loads((work / 'report-run.json').read_text(encoding='utf8'))
    if (work / 'site').exists():
        if (work / 'site-run').exists():
            shutil.rmtree(work / 'site')  # an earlier re-render; the run's own site is already kept
        else:
            shutil.move(str(work / 'site'), str(work / 'site-run'))
    built = subprocess.run([sys.executable, '-m', 'signalpost.cli', 'site', '--input', str(work / 'envelopes.jsonl'),
                            '--out', str(work / 'site')], cwd=work, env=env, capture_output=True, text=True, encoding='utf8')
    assert built.returncode == 0, built.stderr
    report['site'] = {'state': 'available', **json.loads(built.stdout)}
    save(work / 'report.json', report)
    checked = subprocess.run([sys.executable, str(ROOT / 'scripts/check_live_run.py'), '--output', str(work / 'envelopes.jsonl'),
                              '--organisations', orgs, '--state', str(work / 'state'), '--report', str(work / 'report.json'),
                              '--site', str(work / 'site'), '--count', '100'],
                             cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf8')
    (out / 'verification-resite.txt').write_text(portable_text(checked.stdout + checked.stderr), encoding='utf8', newline='\n')
    assert checked.returncode == 0, 'check_live_run failed'
    assert report['site']['largest_profile_bytes'] < 250000, 'site gate failed'
    save(out / 'verification-resite.json', json.loads(checked.stdout))
    shutil.copyfile(work / 'report-run.json', out / 'report-run.json'); sanitize_file(out / 'report-run.json')
    shutil.copyfile(work / 'report.json', out / 'report.json'); sanitize_file(out / 'report.json')
    with open(work / 'envelopes.jsonl', encoding='utf8', newline='') as handle:
        rows = [json.loads(s) for s in handle.read().split(chr(10)) if s.strip()]
    save(out / 'resite.json', {'seed': seed, 'envelopes_sha256': sha(work / 'envelopes.jsonl'), 'run_site': run_report['site'],
                               'site': report['site'], 'site_module_sha256': sha(ROOT / 'src/signalpost/site.py'),
                               'counts': counts(rows), 'HTTP': run_report['requests'],
                               'parent_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()})
    print(seed, json.dumps(report['site']))


if __name__ == '__main__':
    main()
