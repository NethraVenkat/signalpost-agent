"""Build our non-personal, three-year exact-recipient extract from official CSV.

Download URL and NLOD attribution are in docs/SOURCES.md. This script makes no
network requests; inputs must be our own first-party downloads.
"""
import argparse
import csv
import gzip
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from signalpost.sources import state_aid_bulk as bulk
from signalpost.identity.orgnr import valid


def build(source, output, retrieved_at, build_day):
    source, output = Path(source), Path(output)
    at = datetime.fromisoformat(build_day + 'T23:59:59+00:00')
    retrieved = datetime.fromisoformat(retrieved_at.replace('Z', '+00:00'))
    if not retrieved_at.endswith('Z') or retrieved.utcoffset().total_seconds() != 0:
        raise ValueError('retrieved-at must be UTC Z')
    records = {}
    count = kept = 0
    with source.open(encoding='utf-16-le', newline='') as f:
        reader = csv.DictReader(f, delimiter=';')
        if not set(bulk.COLUMNS) <= set(reader.fieldnames or []):
            raise ValueError('Official CSV columns changed')
        for count, row in enumerate(reader, 1):
            org = row.get('Organisasjonsnummer støttemottaker', '')
            if not isinstance(org, str) or not valid(org):
                continue
            record = {'source': bulk.KEY, 'row': count, 'fields': {k: row[k] for k in bulk.COLUMNS}}
            if bulk.derive(record, org, at) is None:
                continue
            text = json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
            records.setdefault(org, []).append(text)
            kept += 1
    with source.open('rb') as f:
        sha = hashlib.file_digest(f, 'sha256').hexdigest()
    meta = {'key': bulk.KEY, 'source_url': bulk.URL, 'retrieved_at': retrieved_at,
            'sha256': sha, 'bytes': source.stat().st_size, 'licence': 'NLOD 2.0; Brønnøysundregistrene',
            'columns': list(bulk.COLUMNS), 'rows_total': count, 'rows_kept': kept}
    payload = {'schema': 1, 'family': 'state_aid', 'build_day': build_day,
               'sources': [meta], 'records': {o: sorted(set(v)) for o, v in sorted(records.items())}}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(gzip.compress(json.dumps(payload, ensure_ascii=False, sort_keys=True,
                                               separators=(',', ':')).encode('utf8'), mtime=0))
    return {'source': meta, 'companies': len(records), 'records': kept, 'bytes': output.stat().st_size,
            'sha256': hashlib.sha256(output.read_bytes()).hexdigest()}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--csv', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--retrieved-at', required=True)
    p.add_argument('--build-day', required=True)
    a = p.parse_args()
    print(json.dumps(build(a.csv, a.out, a.retrieved_at, a.build_day), ensure_ascii=False, indent=2))
