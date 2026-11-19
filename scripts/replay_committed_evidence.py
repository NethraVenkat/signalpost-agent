"""Check the committed replay bundle without network or local research state."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.verify_output import verify
from signalpost.models.shapes import validate


def replay(bundle):
    with tempfile.TemporaryDirectory(prefix='signalpost-committed-replay-') as directory:
        root = Path(directory)
        with zipfile.ZipFile(bundle) as archive:
            manifest = json.loads(archive.read('manifest.json'))
            assert set(archive.namelist()) == set(manifest['files']) | {'manifest.json'}
            for name, expected in manifest['files'].items():
                target = (root / name).resolve()
                assert target.is_relative_to(root.resolve()), 'Unsafe archive member'
                data = archive.read(name)
                assert len(data) == expected['bytes']
                assert hashlib.sha256(data).hexdigest() == expected['sha256']
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
        full = [json.loads(line) for line in (root / 'run/envelopes.jsonl').read_text(encoding='utf8').splitlines()]
        inputs = [json.loads(line)['organisation_number'] for line in (root / 'run/inputs.jsonl').read_text(encoding='utf8').splitlines()]
        assert [row['organisation_number'] for row in full] == inputs
        families = Counter()
        websites = social = 0
        for row in full:
            validate(row, 'union')
            for claim in row['claims']:
                if claim['availability'] != 'available':
                    assert claim['value'] is None
                    continue
                assert claim['evidence_ids']
                families[claim['family']] += 1
                websites += claim['field'] == 'official_website'
                social += claim['field'].startswith('social_profile.')
        actual = {'envelopes': len(full), 'available_claims': sum(families.values()),
                  'available_by_family': dict(sorted(families.items())), 'websites': websites, 'social_urls': social}
        assert actual == manifest['counts'], 'Saved-output metrics differ from manifest'
        receipt = json.loads((root / 'run/report-receipt.json').read_text(encoding='utf8'))
        assert receipt['available_claims'] == actual['available_claims']
        assert receipt['requests'] == len(receipt['request_log'])
        assert dict(Counter(event['host'] for event in receipt['request_log'])) == receipt['requests_by_host']
        by_org = {row['organisation_number']: row for row in full}
        assert receipt['deadline_hits'] == sum(any(e['code'] == 'deadline' for e in row['errors']) for row in by_org.values())
        assert receipt['successful_http_responses'] == sum(isinstance(e.get('status'), int) and 200 <= e['status'] < 300 for e in receipt['request_log'])
        assert dict(Counter(row['state'] for row in full)) == receipt['counts_by_state']
        exact = verify(root / 'extract/envelopes.jsonl', root / 'extract/state',
                       len(manifest['source_replay_companies']), root / 'extract/inputs.jsonl')
        return {'network_required': False, 'saved_output_counts': actual, 'official_source_replay': exact,
                'saved_request_counts': {'http_attempts': receipt['requests'], 'deadline_hits': receipt['deadline_hits'],
                                         'run_status': receipt['run_status']},
                'scope': manifest['scope'], 'bundle_sha256': hashlib.sha256(bundle.read_bytes()).hexdigest()}


if __name__ == '__main__':
    def refuse_network(event, arguments):
        if event in {'socket.connect', 'socket.getaddrinfo', 'socket.gethostbyname', 'socket.sendto'}:
            raise RuntimeError('Committed-evidence replay must not access the network')
    sys.addaudithook(refuse_network)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, default=ROOT / 'reports/evaluator-fixes/evidence.zip')
    args = parser.parse_args()
    print(json.dumps(replay(args.bundle), ensure_ascii=False, indent=2))
