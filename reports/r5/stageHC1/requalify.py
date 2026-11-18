"""Repeat the clean, disjoint F2 qualification after the two HC1 commits."""

import argparse
import importlib.util
import json
import sys
from pathlib import Path

from signalpost.io.input_adapter import read

DEST = Path(__file__).resolve().parent / 'F2'
ROOT = DEST.parents[3]
WORK = ROOT / '.data/r5/hc1-f2-clean'

spec = importlib.util.spec_from_file_location(
    'f2_qualification', ROOT / 'reports/r5/final500/qualify.py')
qualification = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qualification)
qualification.DEST = DEST
qualification.WORK = WORK
scale = qualification.scale
scale.DEST = DEST
scale.CLONE = WORK / 'checkout/repo'
scale.CLONE_PY = scale.CLONE / '.venv/Scripts/python.exe'


def bulk_preflight():
    """Exercise the frozen input loader and receipt writes outside timed state."""
    probe = '''
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace

from signalpost.io.input_adapter import read
from signalpost.sources import bulk_registry
from signalpost.sources.blobstore import BlobStore

batch, bulk, scratch = (Path(arg) for arg in sys.argv[1:])
wanted = set(read(batch).unique)
with TemporaryDirectory(prefix='bulk-preflight-', dir=scratch) as state:
    blobs = BlobStore(Path(state))
    found, digest = bulk_registry.load(bulk, wanted, blobs, SimpleNamespace(check=lambda: None))
    assert sum(1 for path in blobs.directory.iterdir() if path.is_file()) == len(found)
print(json.dumps({'rows': len(found), 'missing_organisation_numbers': sorted(wanted - found.keys()), 'sha256': digest}))
'''
    run = scale.command('bulk-preflight', [
        scale.CLONE_PY, '-c', probe, DEST / 'companies500.jsonl', DEST / 'registry500.csv', WORK,
    ], cwd=scale.CLONE)
    assert run['exit_code'] == 0
    receipt = json.loads((DEST / 'bulk-preflight.txt').read_text(encoding='utf8'))
    prepared = json.loads((DEST / 'clean_clone.json').read_text(encoding='utf8'))
    assert receipt['sha256'] == prepared['subset_sha256']
    assert receipt['rows'] == prepared['extraction']['rows']
    assert receipt['missing_organisation_numbers'] == prepared['extraction']['missing_organisation_numbers']


def verify_saved_outputs(label):
    """Check required artifacts independently when the optional site gate fails."""
    work = scale.work_dir(label)
    prefix = '' if label == 'final' else 'trials/retry/'
    batch = DEST / 'companies500.jsonl'
    report_path = work / 'report.json'
    run = scale.command(prefix + 'verify_output', [
        scale.CLONE_PY, scale.CLONE / 'scripts/verify_output.py', '--first', work / 'envelopes.jsonl',
        '--state-dir', work / 'state', '--count', qualification.COUNT, '--organisations', batch,
        '--report', report_path,
    ], cwd=scale.CLONE)
    assert run['exit_code'] == 0
    receipt = json.loads((DEST / prefix / 'verify_output.txt').read_text(encoding='utf8'))
    assert receipt['complete_briefing_contracts'] == qualification.COUNT
    assert receipt['synthesis_unverified_values'] == receipt['briefing_unverified_values'] == 0
    report = json.loads(report_path.read_text(encoding='utf8'))
    profiles = work / 'profiles.jsonl'
    with profiles.open(encoding='utf8') as stream:
        profile_ids = [json.loads(line)['organisation_number'] for line in stream]
    assert profile_ids == read(batch).rows
    assert report['profiles_output'] == {'state': 'available', 'rows': len(profile_ids), 'bytes': profiles.stat().st_size}
    summary = json.loads((DEST / prefix / 'summary.json').read_text(encoding='utf8'))
    assert {name: scale.sha(work / name) for name in summary['artifacts']} == summary['artifacts']
    receipt.update(profiles_rows=len(profile_ids), artifacts=summary['artifacts'])
    scale.save(prefix + 'required_outputs.json', receipt)
    print(f'Verified {receipt["lines"]} envelopes and {len(profile_ids)} profiles', flush=True)


def replay_site(label):
    """Render the measured envelopes offline and preserve the original run report."""
    work = scale.work_dir(label)
    site = WORK / f'site-replay-{label}'
    prefix = '' if label == 'final' else 'trials/retry/'
    assert not site.exists(), 'Site replay requires a fresh output directory'
    output = work / 'envelopes.jsonl'
    run = scale.command(prefix + 'offline-site', [
        sys.executable, '-m', 'signalpost.cli', 'site', '--input', output, '--out', site,
    ], cwd=ROOT)
    assert run['exit_code'] == 0
    metrics = json.loads((DEST / prefix / 'offline-site.txt').read_text(encoding='utf8'))
    expected = set(read(DEST / 'companies500.jsonl').unique)
    html = list((site / 'c').glob('*.html'))
    assert {path.stem for path in html} == expected
    assert {path.name.removesuffix('.data.js') for path in (site / 'c').glob('*.data.js')} == expected
    assert (site / 'index.html').is_file() and (site / 'compare.html').is_file()
    assert metrics['companies'] == len(expected)
    assert metrics['largest_profile_bytes'] == max(path.stat().st_size for path in html) < 250_000
    scale.save(prefix + 'site_replay.json', {
        **metrics, 'offline_wall_seconds': run['wall_seconds'], 'envelopes_sha256': scale.sha(output),
        'generator_sha256': scale.sha(ROOT / 'src/signalpost/site.py'), 'site': str(site),
    })
    print(f'Checked {len(html)} offline profile pages under the size cap', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=('prepare', 'preflight', 'tests', 'run', 'verify', 'replay-site', 'audit'))
    parser.add_argument('label', nargs='?', choices=('final', 'retry'), default='final')
    options = parser.parse_args()
    if options.phase == 'prepare':
        assert not scale.CLONE.exists(), 'Requalification requires a fresh checkout'
        DEST.mkdir(exist_ok=True)
        scale.prepare()
        bulk_preflight()
    elif options.phase == 'preflight':
        bulk_preflight()
    elif options.phase == 'tests':
        raise SystemExit(qualification.tests())
    elif options.phase == 'run':
        qualification.measure(options.label, run_id_prefix='r5-hc1-f2')
    elif options.phase == 'verify':
        verify_saved_outputs(options.label)
    elif options.phase == 'replay-site':
        replay_site(options.label)
    else:
        directory = DEST if options.label == 'final' else DEST / 'trials/retry'
        receipt_path = directory / 'required_outputs.json'
        verified = receipt_path.is_file()
        if verified:
            saved = json.loads(receipt_path.read_text(encoding='utf8'))
            measured = json.loads((directory / 'summary.json').read_text(encoding='utf8'))
            assert saved['artifacts'] == measured['artifacts']
            assert saved['schema_valid'] and saved['lines'] == qualification.COUNT
        summary = qualification.audit(options.label, saved_output_verified=verified)
        if verified:
            summary['required_output_verification'] = receipt_path.name
        replay_path = directory / 'site_replay.json'
        if replay_path.is_file():
            replay = json.loads(replay_path.read_text(encoding='utf8'))
            assert replay['envelopes_sha256'] == summary['artifacts']['envelopes.jsonl']
            summary['offline_site_verification'] = replay_path.name
        scale.save((directory / 'summary.json').relative_to(DEST), summary)
        print({key: summary[key] for key in (
            'all_gates_pass', 'wall_seconds', 'margin_seconds', 'placeholders', 'websites', 'social_urls',
            'http_requests', 'deadline_companies_by_section', 'url_inventory_categories',
        )})
