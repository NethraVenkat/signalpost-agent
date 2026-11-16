"""Check whether the existing main-entity snapshot can supply NAV parents."""
from signalpost.portable_paths import portable, portable_text  # saved paths stay repo-relative
import csv
import gzip
import hashlib
import json
from pathlib import Path
from audit import DOWNLOADS, DEST


def main():
    path = DOWNLOADS / 'registry.csv'
    nav = json.loads(gzip.decompress((Path('src/signalpost/data/nav_index.json.gz')).read_bytes()))
    employers = {a['employer_orgnr'] for a in nav['ads']}
    matched = []
    rows = 0
    with path.open('rb') as f:
        opener = gzip.open if f.read(2) == b'\x1f\x8b' else open
    with opener(path, 'rt', encoding='utf-8-sig', newline='') as f:
        for row in csv.DictReader(f):
            rows += 1
            if row['organisasjonsnummer'] in employers:
                matched.append({key: row.get(key) for key in ('organisasjonsnummer', 'navn', 'organisasjonsform.kode', 'overordnetEnhet')})
    result = {'source_file': path.name, 'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
              'rows_scanned': rows, 'index_employers': len(employers), 'employers_found_in_main_entity_snapshot': len(matched),
              'employers_with_parent_field': sum(bool(r.get('overordnetEnhet')) for r in matched), 'matches': matched,
              'method': 'Exact orgnr lookup only; no company-name matching; existing official bulk only; zero network requests.'}
    (DEST / 'nav_bulk_join.json').write_text(portable_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n'), encoding='utf8', newline='\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'matches'}))


if __name__ == '__main__':
    main()
