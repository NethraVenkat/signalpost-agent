"""Audit the rebuilt local-data payload against every unchanged saved envelope."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / '.data/r5-gaps-final500/run/envelopes.jsonl'
SITE = ROOT / 'out/r5-site-fixes/offline500/site'


def main():
    def block(event, args):
        if event in {'socket.connect', 'socket.getaddrinfo', 'socket.gethostbyname', 'socket.sendto'}:
            raise RuntimeError('Local payload audit must not access network')
    sys.addaudithook(block)
    totals = {'companies': 0, 'facts': 0, 'available_claims': 0, 'evidence_records': 0,
              'workplace_claims': 0, 'deferred_workplace_claims': 0}
    target = None
    for line in SOURCE.read_text(encoding='utf8').splitlines():
        row = json.loads(line)
        org = row['organisation_number']
        raw = (SITE / 'c' / (org + '.data.js')).read_text(encoding='utf8')
        payload = json.loads(raw.split(' = ', 1)[1].rstrip(';\n'))
        claims = {c['id'][:16]: c for c in row['claims'] if c['evidence_ids'] or c['availability'] == 'available'}
        facts = {c['id']: c for c in payload['facts']}
        assert facts.keys() == claims.keys(), org
        for cid, c in claims.items():
            for key in ('field', 'family', 'availability', 'value', 'reporting_period', 'confidence', 'evidence_ids'):
                assert facts[cid].get(key) == c.get(key), (org, cid, key)
        refs = {eid for c in claims.values() for eid in c['evidence_ids']}
        originals = {e['id']: e for e in row['evidence']}
        decoded = {}
        for record in payload['records']:
            evidence = dict(zip(payload['source_fields'], payload['sources'][record[0]]))
            evidence.update(zip(payload['evidence_fields'], record[1:]))
            decoded[evidence['id']] = evidence
            assert all(evidence[k] == originals[evidence['id']].get(k) for k in evidence), org
        assert decoded.keys() == refs, org
        workplaces = [c for c in row['claims'] if c['field'].startswith('subunits.unit.')]
        deferred = [c for c in payload['registry_details'] if c['field'].startswith('subunits.unit.')]
        for d in deferred:
            assert d['value'] == claims[d['id']]['value'] and d['group'] == 'locations', org
        size = (SITE / 'c' / (org + '.html')).stat().st_size
        assert size < 250000, org
        totals['companies'] += 1
        totals['facts'] += len(facts)
        totals['available_claims'] += sum(c['availability'] == 'available' for c in row['claims'])
        totals['evidence_records'] += len(refs)
        totals['workplace_claims'] += len(workplaces)
        totals['deferred_workplace_claims'] += len(deferred)
        if org == '968360302':
            target = {'organisation_number': org, 'html_bytes': size, 'workplaces': len(workplaces),
                      'deferred_workplaces': len(deferred), 'facts': len(facts), 'evidence_records': len(refs)}
    assert totals['companies'] == 500
    result = dict(totals, target=target, all_fact_values_and_evidence_preserved=True, network_blocked=True)
    Path(__file__).with_name('payload-integrity.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
