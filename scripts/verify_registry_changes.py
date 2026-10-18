"""Independent source-pointer audit of new registry activity; no production extractor use."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit, parse_qs


def pointer(document, path):
    for token in path.strip('/').split('/'):
        token = token.replace('~1', '/').replace('~0', '~')
        document = document[int(token)] if isinstance(document, list) else document[token]
    return document


def check(row, claim, blobs):
    org = row['organisation_number']
    value = claim['value']
    evidence = {e['id']: e for e in row['evidence']}
    sources = []
    for eid in claim['evidence_ids']:
        ev = evidence[eid]
        raw = (blobs / ev['content_sha256']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == ev['content_sha256'], 'Hash mismatch'
        assert ev['claim_span'] in raw.decode('utf8'), 'Non-verbatim excerpt'
        assert ev['retrieved_at'].endswith('Z'), 'Missing UTC retrieval time'
        sources.append((ev, json.loads(raw)))
    ev, document = sources[0]
    assert ev['extraction_method'] == 'registry change feed'
    assert ev['effective_at'] is None, 'Publication mislabelled effective'
    assert value['date_source'] == 'registry publication time (not effective date)'
    assert value['company_orgnr'] == org, 'Wrong company'
    parsed = urlsplit(ev['source_url'])
    assert parsed.scheme == 'https' and parsed.netloc == 'data.brreg.no'
    root = ev['locator'].split('/endringer/')[0]
    event = pointer(document, root)
    assert event['oppdateringsid'] == value['event_id'] and event['dato'] == value['date']
    assert 'old_value' not in value and 'effective_date' not in value
    if 'changed_field' in value:
        assert parsed.path.endswith('/oppdateringer/enheter')
        assert event['organisasjonsnummer'] == org and event['endringstype'] == 'Endring'
        change = pointer(document, ev['locator'])
        path = change['path']
        assert path in {'/navn', '/kapital/belop', '/forretningsadresse', '/postadresse'} or path.startswith(('/forretningsadresse/', '/postadresse/'))
        assert value['changed_field'] == path and value['operation'] == change['op']
        assert change['op'] in {'add', 'replace', 'remove'}
        if change['op'] == 'remove': assert 'new_value' not in value
        else: assert value['new_value'] == change['value']
    else:
        assert parsed.path.endswith('/oppdateringer/underenheter')
        assert event['organisasjonsnummer'] == value['subunit_orgnr']
        assert event['endringstype'] == value['event_type'] in {'Ny', 'Sletting'}
        mappings = [pointer(doc, proof['locator']) for proof, doc in sources[1:]
                    if urlsplit(proof['source_url']).path.endswith('/api/underenheter')]
        matches = [m for m in mappings if m.get('organisasjonsnummer') == value['subunit_orgnr'] and m.get('overordnetEnhet') == org]
        assert matches, 'No exact-parent source proof'
        if 'start_date' in value:
            assert value['event_type'] == 'Ny' and any(m.get('oppstartsdato') == value['start_date'] for m in matches)
    assert parse_qs(urlsplit(value['url']).query)['oppdateringsid'] == [str(event['oppdateringsid'])]
    return {'org': org, 'claim_id': claim['id'], 'event_id': event['oppdateringsid'],
            'publication_time': event['dato'], 'source_url': ev['source_url'],
            'sha256': ev['content_sha256'], 'result': 'verified'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--envelopes', type=Path, required=True)
    parser.add_argument('--state-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    checks = []
    for line in args.envelopes.read_text(encoding='utf8').split('\n'):
        if not line.strip(): continue
        row = json.loads(line)
        for claim in row['claims']:
            if claim['availability'] == 'available' and claim['field'].startswith('registry_change.'):
                checks.append(check(row, claim, args.state_dir / 'blobs'))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result = {'checked': len(checks), 'mismatches': 0, 'checks': checks}
    args.output.write_text(json.dumps(result, indent=2), encoding='utf8')
    print(json.dumps({'checked': len(checks), 'mismatches': 0}))


if __name__ == '__main__': main()
