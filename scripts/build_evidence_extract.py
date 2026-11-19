"""Create a bounded, privacy-conscious replay bundle from an already saved run."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import zipfile

from signalpost.models.claim import Claim
from signalpost.models.envelope import Error
from signalpost.models.evidence import Evidence
from signalpost.runner import placeholder, update, finalize
from signalpost.sources.blobstore import BlobStore
from signalpost.sources.extract import Section
from signalpost.synthesis.template import generate
from signalpost.io.envelope_writer import write
from signalpost.portable_paths import HOME_PATH_PATTERNS


def counts(rows):
    families = Counter()
    for row in rows:
        families.update(c['family'] for c in row['claims'] if c['availability'] == 'available')
    return {'envelopes': len(rows), 'available_claims': sum(families.values()),
            'available_by_family': dict(sorted(families.items())),
            'websites': sum(c['field'] == 'official_website' and c['availability'] == 'available' for r in rows for c in r['claims']),
            'social_urls': sum(c['field'].startswith('social_profile.') and c['availability'] == 'available' for r in rows for c in r['claims'])}


def build(envelopes, state, output):
    raw = envelopes.read_bytes()
    rows = [json.loads(line) for line in raw.decode('utf8').splitlines()]
    candidates = [r for r in rows if all(r['run']['sections'].get(f) == 'available' for f in ('identity', 'accounts'))]
    assert len(candidates) >= 3, 'Need three supported identity/accounts examples'
    selected = candidates[:3]
    files = {'run/envelopes.jsonl': raw,
             'run/inputs.jsonl': ''.join(json.dumps({'organisation_number': r['organisation_number']})+'\n' for r in rows).encode()}
    report = json.loads((envelopes.parent / 'report.json').read_text(encoding='utf8'))
    receipt_keys = ('requests', 'request_log', 'requests_by_host', 'deadline_hits', 'runtime_ms', 'completion',
                    'counts_by_state', 'successful_http_responses', 'available_claims', 'warnings', 'limits', 'run_status')
    files['run/report-receipt.json'] = json.dumps({k: report[k] for k in receipt_keys}, ensure_ascii=False).encode()
    with tempfile.TemporaryDirectory(prefix='signalpost-evidence-build-') as temp:
        root = Path(temp)
        blobs = BlobStore(root / 'state')
        extracted = []
        for row in selected:
            env = placeholder(row['organisation_number'], 'committed-official-extract', row['run']['started_at'], ('identity', 'accounts'))
            for family in ('identity', 'accounts'):
                claims = [Claim.model_validate(c) for c in row['claims'] if c['family'] == family]
                refs = {ref for c in claims for ref in c.evidence_ids}
                evidence = [Evidence.model_validate(e) for e in row['evidence'] if e['id'] in refs]
                # Restrict raw-body redistribution to official registry/filing data.
                assert all(e.source_url.startswith('https://data.brreg.no/') for e in evidence)
                for evidence_row in evidence:
                    body = (state / 'blobs' / evidence_row.content_sha256).read_bytes()
                    assert hashlib.sha256(body).hexdigest() == evidence_row.content_sha256
                    assert blobs.put(body) == evidence_row.content_sha256
                errors = [Error.model_validate(e) for e in row['errors'] if e['section'] == family]
                update(env, family, Section(state=row['run']['sections'][family], claims=claims, evidence=evidence, errors=errors))
            finalize(env, None, blobs, SimpleNamespace(events=[]), 0)
            env.run.synthesis = generate(env)
            env.profile.synthesis = env.run.synthesis
            extracted.append(env)
        write(root / 'extract.jsonl', extracted, 'union', blobs)
        files['extract/envelopes.jsonl'] = (root / 'extract.jsonl').read_bytes()
        files['extract/inputs.jsonl'] = ''.join(json.dumps({'organisation_number': e.organisation_number})+'\n' for e in extracted).encode()
        for blob in (root / 'state' / 'blobs').iterdir():
            files['extract/state/blobs/' + blob.name] = blob.read_bytes()
    for name, body in files.items():
        text = body.decode('utf8', errors='replace')
        assert not any(pattern.search(text) for pattern in HOME_PATH_PATTERNS), 'Local home path in '+name
        if name.startswith('extract/state/blobs/'):
            assert 'foedselsdato' not in text, 'Unexpected personal birth-date field in official extract'
    manifest = {'schema_version': 1, 'counts': counts(rows),
                'source_replay_companies': [r['organisation_number'] for r in selected],
                'files': {name: {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()} for name, body in sorted(files.items())},
                'scope': 'All saved-output membership/counts; exact original-source replay for three identity/accounts extracts only. Other source bodies and historical final500c runs are not bundled.',
                'licences': 'Official raw extracts: Bronnoysundregistrene, NLOD 2.0. Other published facts/excerpts retain the original source URLs, attribution and terms described in docs/SOURCES.md. No raw company HTML or role birth dates are bundled.'}
    files['manifest.json'] = json.dumps(manifest, ensure_ascii=False, indent=2).encode()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, body in sorted(files.items()):
            archive.writestr(name, body)
    print(json.dumps({'archive_bytes': output.stat().st_size, 'sha256': hashlib.sha256(output.read_bytes()).hexdigest(), **manifest['counts']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--envelopes', type=Path, required=True)
    parser.add_argument('--state', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    build(args.envelopes, args.state, args.output)
