"""One offline site rebuild/check from the unchanged measured 500-run outputs."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from signalpost.portable_paths import portable_text
from signalpost.site import generate_site

ROOT = Path(__file__).resolve().parents[4]
DEST = Path(__file__).resolve().parent
SOURCE = ROOT / '.data/r5-gaps-final500/run'
WORK = ROOT / 'out/r5-site-fixes/offline500'


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def save(name, value):
    (DEST / name).write_text(portable_text(json.dumps(value, ensure_ascii=False, indent=2)) + '\n',
                            encoding='utf8', newline='\n')


def main():
    assert not WORK.exists(), 'Fresh offline rebuild only; never an automatic live retry'
    code = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    before = {name: sha(SOURCE / name) for name in ('envelopes.jsonl', 'profiles.jsonl', 'report.json')}
    original = json.loads((SOURCE / 'report.json').read_text(encoding='utf8'))
    WORK.mkdir()
    def no_network(event, values):
        if event in {'socket.connect', 'socket.getaddrinfo', 'socket.gethostbyname', 'socket.sendto'}:
            raise RuntimeError('Offline site rebuild must not access network')
    sys.addaudithook(no_network)
    began = time.monotonic()
    site = generate_site(SOURCE / 'envelopes.jsonl', WORK / 'site')
    wall = time.monotonic() - began
    derived = dict(original)
    derived['site'] = dict(site, state='available')
    derived['offline_site_rebuild'] = {'code_commit': code, 'source_run_commit': 'f740933',
        'source_sha256': before, 'wall_seconds': wall, 'research_rerun': False,
        'original_site': original['site'], 'original_warnings_retained': True,
        'note': 'Original CLI wall/coverage and warnings are retained; site results are from a separate offline rebuild.'}
    derived_path = WORK / 'report.json'
    derived_path.write_text(portable_text(json.dumps(derived, ensure_ascii=False, indent=2)) + '\n',
                            encoding='utf8', newline='\n')
    save('rebuild.json', {'code_commit': code, 'source_run_commit': 'f740933', 'source_sha256': before,
        'wall_seconds': wall, 'site': site, 'network_blocked': True, 'research_rerun': False,
        'original_site': original['site'], 'historical_adaptive_warning': original['warnings']})
    blocker = WORK / 'no-network'
    blocker.mkdir()
    (blocker / 'sitecustomize.py').write_text(
        "import sys\ndef block(event,args):\n"
        " if event in {'socket.connect','socket.getaddrinfo','socket.gethostbyname','socket.sendto'}:"
        "raise RuntimeError('Saved-output check must not access network')\n"
        "sys.addaudithook(block)\n", encoding='utf8')
    env = {k: v for k, v in os.environ.items() if not any(x in k.upper() for x in
           ('TOKEN', 'SECRET', 'PASSWORD', 'API_KEY', 'CREDENTIAL', 'AWS_', 'AZURE_', 'OPENAI_', 'ANTHROPIC_'))}
    env.update(PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(blocker),
               SIGNALPOST_SEARCH_PROVIDER='disabled', SIGNALPOST_SEARCH_MOCK='0')
    args = [str(ROOT / '.venv/Scripts/python.exe'), str(ROOT / 'scripts/check_live_run.py'),
            '--output', str(SOURCE / 'envelopes.jsonl'), '--organisations', str(DEST.parent / 'final500/companies500.jsonl'),
            '--state', str(SOURCE / 'state'), '--report', str(derived_path), '--site', str(WORK / 'site'), '--count', '500']
    began = time.monotonic()
    result = subprocess.run(args, cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf8')
    (DEST / 'check_live_run.txt').write_text(portable_text(result.stdout + result.stderr), encoding='utf8', newline='\n')
    save('check-execution.json', {'exit_code': result.returncode, 'wall_seconds': time.monotonic()-began,
        'argv': args, 'network_blocked': True, 'research_rerun': False})
    after = {name: sha(SOURCE / name) for name in before}
    assert before == after, 'Original measured outputs changed'
    save('original-output-integrity.json', {'before': before, 'after': after, 'unchanged': True})
    if result.returncode:
        raise SystemExit('Offline check failed; preserve receipt before considering the authorized live fallback')
    checked = json.loads(result.stdout.strip().splitlines()[-1])
    save('check_live_run.json', checked)
    print(json.dumps({'check_exit_code': 0, 'site': site, 'offline_rebuild_seconds': wall}), flush=True)


if __name__ == '__main__':
    main()
