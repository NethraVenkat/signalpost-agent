"""Comparable published-claim counts, independent of optional source availability."""
import argparse
import json
from collections import Counter
from pathlib import Path


def counts(path):
    rows = [json.loads(line) for line in Path(path).read_text(encoding='utf8').splitlines() if line.strip()]
    tests = {
        'signature_prokura': lambda c: c['field'].startswith(('roles.authority.', 'signature.', 'prokura.')),
        'group_relationships': lambda c: c['field'].startswith('group.relationship.'),
        'consolidated_accounts': lambda c: c['field'].startswith('accounts.consolidated.'),
        'state_aid': lambda c: c['field'].startswith('state_aid.award.'),
        'all_available': lambda c: True,
    }
    result = {name: {'companies': [], 'claims': 0} for name in tests}
    families = Counter()
    for row in rows:
        data = row if 'claims' in row else row['profile']
        available = [c for c in data['claims'] if c['availability'] == 'available' and not c.get('carried_forward')]
        families.update(c['family'] for c in available)
        for name, matches in tests.items():
            found = [c for c in available if matches(c)]
            if found:
                result[name]['companies'].append(row['organisation_number'])
                result[name]['claims'] += len(found)
    for item in result.values():
        item['companies'] = sorted(set(item['companies']))
        item['companies_covered'] = len(item['companies'])
    return {'envelopes': len(rows), 'information_types': result, 'families': dict(sorted(families.items()))}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('envelopes', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.write_text(json.dumps(counts(args.envelopes), ensure_ascii=False, indent=2) + '\n', encoding='utf8')
