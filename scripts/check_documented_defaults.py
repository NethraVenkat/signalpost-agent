"""Check current documentation against code and inventory historical numeric mentions."""
import argparse
import gzip
import json
from pathlib import Path
import re
import subprocess

from signalpost.config import Config
from signalpost.budget import HTTP_PER_100, WEBSITE_MARGIN_SECONDS, WEBSITE_FINALISATION_SECONDS

ROOT = Path(__file__).resolve().parents[1]


def check():
    readme = (ROOT / 'README.md').read_text(encoding='utf8')
    submission = (ROOT / 'SUBMISSION.md').read_text(encoding='utf8')
    evaluation = (ROOT / 'docs/EVAL.md').read_text(encoding='utf8')
    sources = (ROOT / 'docs/SOURCES.md').read_text(encoding='utf8')
    nav = ROOT / 'src/signalpost/data/nav_index.json.gz'
    metadata = json.loads(gzip.decompress(nav.read_bytes()))
    current_index = sources.split('### Declared NAV official-feed index', 1)[1].split('\n\n', 2)[1]
    seconds = Config.model_fields['time_budget_seconds'].default
    cutoff = seconds - WEBSITE_MARGIN_SECONDS - WEBSITE_FINALISATION_SECONDS
    assert f'The default time budget is {seconds:,}' in readme
    assert f'{seconds:,} seconds' in submission
    assert 'The default time budget is 2,400' not in readme
    assert f'{cutoff:,} seconds for both 100-company' in readme
    assert f'{HTTP_PER_100:,}' in evaluation
    for value in (metadata['index_version'], metadata['built_at'], f"{metadata['ads_count']:,}",
                  f"{metadata['employer_count']:,}", f'{nav.stat().st_size:,}'):
        assert value in current_index, 'Stale current NAV index declaration: ' + value
    assert 'pypdf' in readme and 'has one pass' in readme
    assert '--nav-concurrency 4' in (ROOT / 'docs/AGENT.md').read_text(encoding='utf8')
    names = subprocess.check_output(['git', '-C', str(ROOT), 'ls-files', '-z', '--cached', '--others',
                                     '--exclude-standard', '--', '*.md']).decode().split('\0')
    patterns = (r'9,015|403,768|nav-20261014T042640', r'310 seconds|1,550 seconds',
                r'default[^.\n]{0,80}2,400', r'default 6 requests|cap of 9 per company')
    mentions = []
    for name in sorted(set(names) - {''}):
        path = ROOT / name
        if not path.is_file():
            continue
        for line_number, line in enumerate(path.read_text(encoding='utf8', errors='replace').splitlines(), 1):
            for pattern in patterns:
                if re.search(pattern, line, re.I):
                    mentions.append({'path': name, 'line': line_number,
                                     'scope': 'historical report' if name.startswith('reports/') else 'reviewed dated measurement or code description',
                                     'pattern': pattern})
    return {'current_defaults_verified': True, 'markdown_files_scanned': len(set(names) - {''}),
            'time_budget_seconds': seconds, 'website_cutoff_default_100_plus': cutoff,
            'http_per_100': HTTP_PER_100, 'nav_ads': metadata['ads_count'],
            'nav_employers': metadata['employer_count'], 'nav_compressed_bytes': nav.stat().st_size,
            'historical_mentions_retained': mentions,
            'policy': 'Correct current instructions; retain dated measurements as historical rather than falsifying their old settings.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check()
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2)+'\n', encoding='utf8')
    print(json.dumps({k: v for k, v in result.items() if k != 'historical_mentions_retained'}))
