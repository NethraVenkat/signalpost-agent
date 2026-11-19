"""Bounded replay: all field counts and full saved evidence for new gap claims.

Legacy claim values, role responses and company HTML are deliberately excluded.
The new consolidated/state-aid claims and their complete source bodies are kept.
"""
import argparse
import base64
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def categories(field):
    yield 'all_available'
    for name, prefixes in (
        ('signature_prokura', ('roles.authority.', 'signature.', 'prokura.')),
        ('group_relationships', ('group.relationship.',)),
        ('consolidated_accounts', ('accounts.consolidated.',)),
        ('state_aid', ('state_aid.award.',)),
    ):
        if field.startswith(prefixes):
            yield name


def inventory_counts(inventory):
    claims = Counter()
    companies = {k: set() for k in ('all_available', 'signature_prokura', 'group_relationships',
                                   'consolidated_accounts', 'state_aid')}
    for org, fields in inventory.items():
        for field in fields:
            for name in categories(field):
                claims[name] += 1
                companies[name].add(org)
    return {k: {'companies_covered': len(v), 'claims': claims[k]} for k, v in companies.items()}


def build(runs, output):
    packet = {'schema': 1, 'runs': {}, 'bodies': {},
              'scope': 'All available-field counts; full source replay for consolidated and state-aid claims only. '
                       'Legacy values, timings, precision and historical sampling-universe bytes are not reverified.'}
    for name, directory in runs:
        directory = Path(directory)
        raw = (directory / 'envelopes.jsonl').read_bytes()
        rows = [json.loads(s) for s in raw.decode('utf8').splitlines() if s.strip()]
        saved = {'source_envelopes_sha256': digest(raw), 'inputs': [r['organisation_number'] for r in rows],
                 'inventory': {}, 'new_rows': []}
        for row in rows:
            available = [c for c in row['claims'] if c['availability'] == 'available' and not c.get('carried_forward')]
            saved['inventory'][row['organisation_number']] = [c['field'] for c in available]
            selected = [c for c in available if c['field'].startswith(('accounts.consolidated.', 'state_aid.award.'))]
            if not selected:
                continue
            refs = {ref for c in selected for ref in c['evidence_ids']}
            evidence = [e for e in row['evidence'] if e['id'] in refs]
            for e in evidence:
                sha = e['content_sha256']
                if sha not in packet['bodies']:
                    body = (directory / 'state/blobs' / sha).read_bytes()
                    assert digest(body) == sha
                    packet['bodies'][sha] = base64.b64encode(body).decode('ascii')
            saved['new_rows'].append({'organisation_number': row['organisation_number'],
                'run': {'completed_at': row['run']['completed_at'], 'synthesis': {'contract_version': 'r5-S'}},
                'claims': selected, 'evidence': evidence})
        saved['counts'] = inventory_counts(saved['inventory'])
        packet['runs'][name] = saved
    # No role birth dates or local user paths may enter a committed packet.
    from signalpost.portable_paths import HOME_PATH_PATTERNS
    texts = [json.dumps(packet, ensure_ascii=False)]
    texts += [base64.b64decode(v).decode('utf8') for v in packet['bodies'].values()]
    for text in texts:
        assert not any(p.search(text) for p in HOME_PATH_PATTERNS)
        assert not any(k in text.casefold() for k in ('fodselsdato', 'foedselsdato', 'fødselsdato'))
    encoded = json.dumps(packet, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf8')
    output.write_bytes(gzip.compress(encoded, mtime=0))
    return {'bytes': output.stat().st_size, 'sha256': digest(output.read_bytes()),
            'source_bodies': len(packet['bodies']), 'scope': packet['scope']}


def replay(path):
    import signalpost
    # Bind the verifier to the installed checkout, also when this helper and its
    # packet are passed as input files to the clean verification clone.
    repo = Path(signalpost.__file__).resolve().parents[2]
    sys.path.insert(0, str(repo))
    from scripts.verify_output import verify_financial_sources, verify_exact_official
    packet = json.loads(gzip.decompress(path.read_bytes()))
    assert packet['schema'] == 1
    bodies = {sha: base64.b64decode(text) for sha, text in packet['bodies'].items()}
    assert all(digest(body) == sha for sha, body in bodies.items())
    text = lambda sha: bodies[sha].decode('utf8')
    result = {}
    for name, run in packet['runs'].items():
        assert len(run['inputs']) == len(set(run['inputs'])) == len(run['inventory'])
        assert set(run['inputs']) == set(run['inventory'])
        counts = inventory_counts(run['inventory'])
        assert counts == run['counts']
        financial = official = expected = 0
        for row in run['new_rows']:
            evidence = {e['id']: e for e in row['evidence']}
            expected += len(row['claims'])
            for c in row['claims']:
                assert c['evidence_ids']
                for ref in c['evidence_ids']:
                    e = evidence[ref]
                    assert len(e['claim_span']) <= 300 and e['claim_span'] in text(e['content_sha256'])
            f, _ = verify_financial_sources(row, row, evidence, text)
            financial += f
            official += verify_exact_official(row, row, evidence, text)
        assert financial + official == expected
        assert financial == counts['consolidated_accounts']['claims']
        assert official == counts['state_aid']['claims']
        result[name] = {'envelopes': len(run['inputs']), 'counts': counts, 'consolidated_claims_verified': financial,
                        'state_aid_claims_verified': official, 'unsupported_new_claims': 0}
    return {'network_required': False, 'source_bodies_verified': len(bodies), 'runs': result,
            'scope': packet['scope'], 'sha256': digest(path.read_bytes())}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['build', 'replay'])
    p.add_argument('--run', action='append', default=[], help='name=directory')
    p.add_argument('--bundle', required=True, type=Path)
    a = p.parse_args()
    if a.action == 'replay':
        def no_network(event, args):
            if event in {'socket.connect', 'socket.getaddrinfo', 'socket.gethostbyname', 'socket.sendto'}:
                raise RuntimeError('Evidence replay must not access network')
        sys.addaudithook(no_network)
        result = replay(a.bundle)
    else:
        result = build([s.split('=', 1) for s in a.run], a.bundle)
    print(json.dumps(result, ensure_ascii=False, indent=2))
