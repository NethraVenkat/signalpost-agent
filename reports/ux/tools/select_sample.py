"""Choose reproducible controls from the saved R3b 1,000-company run."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SOURCE = ROOT / 'out/r3b-retry/default1000/envelopes.jsonl'
BULK = ROOT / 'out/capacity-inputs/bulk1000.csv'
rows = [json.loads(x) for x in SOURCE.read_text(encoding='utf8').split('\n') if x.strip()]
bulk = {r['organisasjonsnummer'] for r in csv.DictReader(BULK.open(encoding='utf-8-sig'))}


def has(row, predicate):
    return any(c['availability'] == 'available' and predicate(c) for c in row['claims'])


chosen = ['923609016', '988330752']
special = {'923609016': 'Equinor large-company layout',
           '988330752': 'FILMTEK known main/subunit website ambiguity'}


def pick(predicate, reason):
    for row in rows:
        org = row['organisation_number']
        if org in bulk and org not in chosen and predicate(row):
            chosen.append(org)
            special[org] = reason
            return
    raise RuntimeError('No eligible control in the saved cohort')


pick(lambda r: has(r, lambda c: c['field'].startswith('registry_change.')),
     'registry activity in the saved default 1,000 run')
pick(lambda r: has(r, lambda c: c['family'] == 'hiring'),
     'exact-company NAV hiring in the saved default 1,000 run')
pick(lambda r: has(r, lambda c: c['field'] == 'official_website'
                   and isinstance(c['value'], dict)
                   and c['value'].get('identity_level') == 'VERIFIED'),
     'exact-proof verified website in the saved default 1,000 run')
near_empty = [r for r in rows if r['organisation_number'] in bulk
              and r['organisation_number'] not in chosen
              and not has(r, lambda c: c['family'] in ('hiring', 'activity', 'website'))]
row = min(near_empty, key=lambda r: sum(c['availability'] == 'available' for c in r['claims']))
org = row['organisation_number']
chosen.append(org)
special[org] = 'near-empty external coverage and few available facts in the saved run'
chosen.append('12345678')
special['12345678'] = 'invalid identifier for terminal-envelope and site-notice audit'
for row in rows:
    if len(chosen) == 50:
        break
    org = row['organisation_number']
    if org in bulk and org not in chosen:
        chosen.append(org)
assert len(chosen) == len(set(chosen)) == 50
folder = Path(__file__).resolve().parents[1] / 'sample'
folder.mkdir(parents=True, exist_ok=True)
(folder / 'batch.jsonl').write_text(''.join(json.dumps({'organisation_number': org}) + '\n' for org in chosen), encoding='utf8')
(folder / 'selection.json').write_text(json.dumps({
    'source': str(SOURCE), 'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'bulk': str(BULK), 'bulk_sha256': hashlib.sha256(BULK.read_bytes()).hexdigest(),
    'special_cases': special,
    'remaining': 'first unused input-order valid companies in frozen 1,000-company bulk cohort',
    'count': len(chosen)}, indent=2), encoding='utf8')
print(json.dumps({'special_cases': special, 'count': len(chosen)}))
