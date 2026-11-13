"""Independently recount the audit from hash-checked official response pointers."""
import gzip
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit
from audit import ROOT, DEST, DOWNLOADS, load_runs
from signalpost.identity.orgnr import valid


def pointer(value, path):
    for part in path.strip('/').split('/'):
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def main():
    result = json.loads((DEST / 'nav_parent_join.json').read_text(encoding='utf8'))
    index_path = ROOT / 'src/signalpost/data/nav_index.json.gz'
    assert hashlib.sha256(index_path.read_bytes()).hexdigest() == result['index_sha256']
    index = json.loads(gzip.decompress(index_path.read_bytes())); employers = {a['employer_orgnr'] for a in index['ads']}
    assert len(employers) == result['indexed_employers']
    universe_path = DOWNLOADS / 'universe.jsonl.gz'
    assert hashlib.sha256(universe_path.read_bytes()).hexdigest() == result['universe_archive_sha256']
    with gzip.open(universe_path, 'rt', encoding='utf8') as f:
        universe = {json.loads(line)['organisation_number'] for line in f}
    documents, raw_texts = {}, {}
    for receipt in result['receipts']:
        if not receipt.get('content_sha256'):
            continue
        parts = urlsplit(receipt['url'])
        assert parts.scheme == 'https' and parts.hostname == 'data.brreg.no'
        assert parts.path == '/enhetsregisteret/api/underenheter' or re.fullmatch(r'/enhetsregisteret/api/(?:under)?enheter/\d{9}', parts.path)
        raw = Path(receipt['body_path']).read_bytes(); digest = hashlib.sha256(raw).hexdigest()
        assert digest == receipt['content_sha256']
        if receipt['status'] == 200:
            documents[digest] = json.loads(raw); raw_texts[digest] = raw.decode('utf8')
    seen, parents = set(), set()
    for relation in result['relationships']:
        org, parent, digest = relation['employer_orgnr'], relation['parent_orgnr'], relation['content_sha256']
        assert org in employers and org not in seen and valid(org) and valid(parent)
        assert pointer(documents[digest], relation['employer_locator']) == org
        assert pointer(documents[digest], relation['parent_locator']) == parent
        assert relation['employer_locator'].rsplit('/', 1)[0] == relation['parent_locator'].rsplit('/', 1)[0]
        for key in ('employer_exact_excerpt', 'parent_exact_excerpt'):
            assert relation[key] and relation[key] in raw_texts[digest]
        seen.add(org); parents.add(parent)
    represented = (parents | employers) & universe
    classified = set(seen)
    for item in result.get('confirmed_main_employers', []):
        org, digest = item['employer_orgnr'], item['content_sha256']
        assert org in employers and org not in classified and pointer(documents[digest], item['locator']) == org
        assert item['exact_excerpt'] in raw_texts[digest]
        classified.add(org)
    deleted = []
    for item in result.get('deleted_unmapped_employers', []):
        org, digest = item['employer_orgnr'], item['content_sha256']; record = documents[digest]
        assert org in employers and org not in classified and record['organisasjonsnummer'] == org
        assert record['respons_klasse'] == item['response_class'] == 'SlettetUnderEnhet'
        assert record['slettedato'] == item['registry_deleted_at'] and not record.get('overordnetEnhet')
        assert item['exact_excerpt'] in raw_texts[digest]
        classified.add(org); deleted.append(org)
    assert result['mapped_employers'] == len(seen)
    assert result['unique_index_companies_in_universe'] == len(represented)
    complete = seen == employers and not result['failures'] and not result['missing_employers']
    assert result['complete'] == complete
    expected = len(represented) / len(universe) * 1000 if complete else None
    assert result['expected_rate_per_1000'] == expected
    observed = sum(any(c['field'].startswith('hiring.job.') and c['availability'] == 'available' for c in row['claims']) for _, _, _, rows, _ in load_runs() for row in rows)
    assert result['measured_job_companies'] == observed and result['measured_rate_per_1000'] == observed / 600 * 1000
    assert result['cost_usd'] == 0 and result['http_requests'] == len(result['receipts']) <= 40
    verification = {'hashes_and_exact_record_pairings_valid': True, 'unsupported_parent_values': 0,
                    'mapped_employers': len(seen), 'parent_companies_in_universe': len(parents & universe),
                    'unique_expected_companies': len(represented), 'expected_rate_per_1000': expected,
                    'complete_expected_rate_proven': complete, 'measured_job_companies': observed, 'measured_rate_per_1000': observed / 600 * 1000,
                    'classified_employers': len(classified), 'deleted_units_without_parent': deleted,
                    'confirmed_rate_per_1000': len(represented) / len(universe) * 1000,
                    'possible_upper_rate_per_1000': (len(represented) + len(result['missing_employers'])) / len(universe) * 1000,
                    'http_requests': result['http_requests'], 'cost_usd': 0}
    matched_samples = []
    for seed, _, _, rows, _ in load_runs():
        for row in rows:
            if row['organisation_number'] in represented:
                matched_samples.append({'seed': seed, 'orgnr': row['organisation_number'], 'name': row['run']['legal_identity']['legal_name'],
                    'job_published': any(c['field'].startswith('hiring.job.') and c['availability'] == 'available' for c in row['claims'])})
    verification['sample_index_matched_companies'] = matched_samples
    (DEST / 'nav_parent_verification.json').write_text(json.dumps(verification, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(verification))


if __name__ == '__main__':
    main()
