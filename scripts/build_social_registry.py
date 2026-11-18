"""Build veto-only name and shared-homepage keys from the frozen Brønnøysund CSV."""

import argparse
import csv
import gzip
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from signalpost.identity.orgnr import valid
from signalpost.portable_paths import portable_text
from signalpost.web.policy import DIRECTORIES, FREE_MAIL, MARKETPLACES, SOCIAL, domain, normalize_url
from signalpost.web.social_registry import DEFAULT_PATH, LEGAL_FORMS, MAX_WORDS, fingerprint, legal_words

BRREG = 'https://data.brreg.no/enhetsregisteret/api/enheter/lastned/csv'
LICENCE = 'https://data.norge.no/nlod/no/2.0'


def build(snapshot, snapshot_date):
    with snapshot.open('rb') as stream:
        source_hash = hashlib.file_digest(stream, 'sha256').hexdigest()
    names = set()
    websites = defaultdict(dict)
    max_words = 0
    with gzip.open(snapshot, 'rt', encoding='utf-8-sig', newline='') as handle:
        for row in csv.DictReader(handle):
            org, name = row['organisasjonsnummer'], row['navn']
            if not valid(org) or row.get('slettedato') or not name:
                continue
            words = legal_words(name)
            if not 2 <= len(words) <= MAX_WORDS or words[-1] not in LEGAL_FORMS:
                continue
            names.add(fingerprint(words))
            max_words = max(max_words, len(words))
            if not row['hjemmeside']:
                continue
            try:
                url = normalize_url(row['hjemmeside'])
                registered_domain = domain(url) if url else ''
            except ValueError:
                continue
            if registered_domain and registered_domain not in DIRECTORIES | FREE_MAIL | MARKETPLACES | SOCIAL:
                websites[registered_domain][org] = (len(words) - 1, fingerprint(words[:-1]).hex())
    shared = {
        root: [[org, size, key] for org, (size, key) in sorted(entities.items())]
        for root, entities in sorted(websites.items()) if len(entities) >= 2
    }
    metadata = {
        'version': 1, 'name_count': len(names), 'max_words': max_words,
        'shared_domains': len(shared), 'source_url': BRREG, 'snapshot_date': snapshot_date,
        'source_sha256': source_hash, 'attribution': 'Brønnøysundregistrene / Enhetsregisteret',
        'licence_url': LICENCE,
    }
    payload = (json.dumps(metadata, sort_keys=True, ensure_ascii=False).encode('utf8') + b'\n'
               + b''.join(sorted(names))
               + json.dumps(shared, separators=(',', ':')).encode('utf8'))
    return metadata, gzip.compress(payload, mtime=0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot', type=Path, required=True)
    parser.add_argument('--snapshot-date', required=True)
    parser.add_argument('--output', type=Path, default=DEFAULT_PATH)
    parser.add_argument('--receipt', type=Path, required=True)
    args = parser.parse_args()
    metadata, bundle = build(args.snapshot, args.snapshot_date)
    args.output.write_bytes(bundle)
    result = {**metadata, 'bundle_sha256': hashlib.sha256(bundle).hexdigest(), 'bytes': len(bundle)}
    args.receipt.write_text(portable_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n'),
                            encoding='utf8', newline='\n')


if __name__ == '__main__':
    main()
