"""One fresh standard-seed smoke run and saved-proof verification."""
import json
import os
import sys
from collections import Counter
from pathlib import Path

import qualify as q
from signalpost.portable_paths import expand


def main():
    s = q.scale
    attempt = os.environ.get('FINAL500C_SMOKE_ATTEMPT', '')
    dest = q.DEST / ('smoke100' + attempt)
    dest.mkdir(exist_ok=False)
    settings = json.loads((q.ROOT / 'reports/r5/stageT/frozen/settings.json').read_text(encoding='utf8'))
    original = settings['command_argv']
    batch = Path(expand(original[original.index('--organisations') + 1]))
    bulk = Path(expand(original[original.index('--bulk') + 1]))
    work = q.ROOT / ('.data/r5/final500c-smoke100' + attempt)
    work.mkdir(exist_ok=False)
    s.DEST = dest
    argv = [sys.executable, '-m', 'signalpost.cli', 'run',
            '--organisations', batch, '--bulk', bulk,
            '--output', work / 'envelopes.jsonl', '--profiles-output', work / 'profiles.jsonl',
            '--report', work / 'report.json', '--run-id', 'r5-final500c-seed20261017', '--expected-count', 100]
    assert sum(str(a).startswith('--') for a in argv) == 7
    execution = s.command('run', argv, cwd=work)
    assert execution['exit_code'] == 0
    check = s.command('check_live_run', [sys.executable, q.ROOT / 'scripts/check_live_run.py',
                      '--output', work / 'envelopes.jsonl', '--organisations', batch,
                      '--state', work / 'state', '--report', work / 'report.json',
                      '--site', work / 'site', '--count', 100])
    assert check['exit_code'] == 0
    rows = s.jsonl(work / 'envelopes.jsonl')
    report = json.loads((work / 'report.json').read_text(encoding='utf8'))
    summary = dict(seed=20261017, wall_seconds=execution['wall_seconds'],
                   activity=dict(Counter(r['run']['sections']['activity'] for r in rows)),
                   websites=sum(c['field'] == 'official_website' and c['availability'] == 'available'
                                for r in rows for c in r['claims']),
                   verification=json.loads((dest / 'check_live_run.txt').read_text(encoding='utf8')),
                   cost_usd=report['total_cost_usd'])
    s.save('summary.json', summary)
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
