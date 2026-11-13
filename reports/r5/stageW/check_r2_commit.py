"""Verify the committed R2 tree independently of pending R4 working files."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from audit import ROOT, DEST


def main():
    work = ROOT / '.data/r5/stageR2-commit-check'
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=work, text=True).strip()
    assert head.startswith('81a76b8d')
    assert not subprocess.check_output(['git', 'status', '--porcelain'], cwd=work, text=True).strip()
    env = os.environ.copy()
    env.update(PYTHONUTF8='1', PYTHONPATH=str(work / 'src') + os.pathsep + str(work))
    for key in ('SIGNALPOST_SEARCH_PROVIDER', 'SIGNALPOST_SEARCH_MOCK'):
        env.pop(key, None)
    module = subprocess.check_output([sys.executable, '-c', 'import signalpost;print(signalpost.__file__)'], cwd=work, env=env, text=True).strip()
    assert Path(module).resolve().is_relative_to((work / 'src').resolve())
    argv = [sys.executable, 'reports/r5/stage4_7/run_tests.py', '-q', '-p', 'no:cacheprovider']
    started = time.monotonic()
    with (DEST / 'pytest-R2-committed-tree.txt').open('w', encoding='utf8', newline='\n') as log:
        result = subprocess.run(argv, cwd=work, env=env, stdout=log, stderr=subprocess.STDOUT)
    receipt = {'commit': head, 'working_directory': str(work), 'module': module, 'command_argv': argv,
               'exit_code': result.returncode, 'wall_seconds': time.monotonic() - started,
               'dependencies': 'Existing local environment; PYTHONPATH and module receipt prove this exact worktree supplies application code. No network install or paid service.'}
    (DEST / 'r2_committed_tree_check.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(receipt))
    raise SystemExit(result.returncode)


if __name__ == '__main__':
    main()
