"""Build frequency counts from the project's own official registry snapshots."""
import argparse
import csv
import gzip
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from signalpost.identity.orgnr import valid
from signalpost.web.rarity import DEFAULT_PATH, KINDS, keys


def build(paths):
    counts = {k: Counter() for k in KINDS}
    seen_pairs = set()
    entities = set()
    sources = []
    for kind, path in paths:
        path = Path(path)
        digest = hashlib.sha256()
        with path.open('rb') as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b''):
                digest.update(chunk)
        with path.open('rb') as f:
            compressed = f.read(2) == b'\x1f\x8b'
        opener = gzip.open if compressed else open
        rows = 0
        with opener(path, 'rt', encoding='utf-8-sig', newline='') as f:
            sample = f.read(16384); f.seek(0)
            dialect = csv.Sniffer().sniff(sample, delimiters=',;\t')
            for row in csv.DictReader(f, dialect=dialect):
                org = str(row.get('organisasjonsnummer') or '')
                if not valid(org):
                    continue
                rows += 1; entities.add(org)
                for category, values in keys(row).items():
                    for value in values:
                        pair = (category, value, org)
                        if pair not in seen_pairs:
                            counts[category][value] += 1
                            seen_pairs.add(pair)
        sources.append({'kind': kind, 'source_url': f'https://data.brreg.no/enhetsregisteret/api/{kind}/lastned/csv',
                        'file': path.name, 'sha256': digest.hexdigest(), 'valid_rows': rows,
                        'local_file_modified_at': datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()})
    return {'schema_version': 1, 'built_at': datetime.now(timezone.utc).isoformat(), 'entity_count': len(entities),
            'attribution': 'Brønnøysundregistrene / Enhetsregisteret; NLOD 2.0',
            'licence_url': 'https://data.norge.no/nlod/no/2.0', 'sources': sources,
            'definition': 'Distinct registered orgnrs per normalized key; duplicate phone/mobile/rows count once. Counts describe only the included snapshots, not the entire current registry. No ownership inference.',
            'counts': {k: dict(sorted(v.items())) for k, v in counts.items()}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--enheter', type=Path, required=True)
    parser.add_argument('--underenheter', type=Path)
    parser.add_argument('--output', type=Path, default=DEFAULT_PATH)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    paths = [('enheter', args.enheter)] + ([('underenheter', args.underenheter)] if args.underenheter else [])
    data = build(paths)
    body = (json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n').encode()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(gzip.compress(body, mtime=0))
    report = {k: v for k, v in data.items() if k != 'counts'}
    report['table_sha256'] = hashlib.sha256(args.output.read_bytes()).hexdigest()
    report['bytes'] = args.output.stat().st_size
    report['distribution'] = {kind: dict(Counter('1' if n == 1 else '2' if n == 2 else '3–4' if n < 5 else '≥5' for n in values.values())) for kind, values in data['counts'].items()}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(report, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    main()
