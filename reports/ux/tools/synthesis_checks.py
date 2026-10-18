"""Check cited synthesis and missing-state coverage on the frozen sample."""
import json
from collections import Counter
from pathlib import Path

UX = Path(__file__).resolve().parents[1]
rows = [json.loads(line) for line in (UX / 'sample/out/envelopes.jsonl').open(encoding='utf8')]
result = {'companies': len(rows), 'section_sentence_count': 0, 'uncited_section_sentences': [],
          'unresolved_citations': [], 'unknown_sentence_count': 0, 'unknowns_with_claim_ids': 0,
          'unknown_texts': Counter(), 'examples': {}, 'no_change_phrase_count': 0}
for row in rows:
    org = row['organisation_number']
    syn = row['run'].get('synthesis') or {}
    valid = {c['id'] for c in row['claims']} | {c['id'] for c in syn.get('change_claims', [])}
    sections = syn.get('sections', {})
    for area in ('what_it_does', 'scale', 'leadership', 'changes'):
        for sentence in sections.get(area, []):
            result['section_sentence_count'] += 1
            if not sentence.get('claim_ids'):
                result['uncited_section_sentences'].append([org, area, sentence['text']])
            for claim_id in sentence.get('claim_ids', []):
                if claim_id not in valid:
                    result['unresolved_citations'].append([org, area, claim_id])
            if 'no changes found in sources checked' in sentence['text'].lower():
                result['no_change_phrase_count'] += 1
    for sentence in sections.get('unknowns', []):
        result['unknown_sentence_count'] += 1
        result['unknown_texts'][sentence.get('text') or sentence['reason']] += 1
        if sentence.get('claim_ids'):
            result['unknowns_with_claim_ids'] += 1
    if org in {'923609016', '932525070', '991853995', '820042182'}:
        result['examples'][org] = {k: [{'text': s.get('text'), 'claim_ids': s.get('claim_ids', []),
                                       'reason': s.get('reason')} for s in sections.get(k, [])[:3]]
                                    for k in ('what_it_does', 'changes', 'unknowns')}
result['unknown_texts'] = dict(result['unknown_texts'])
(UX / 'synthesis-checks.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf8')
print(json.dumps({k: result[k] for k in ('companies', 'section_sentence_count',
                                         'unknown_sentence_count', 'unknowns_with_claim_ids',
                                         'no_change_phrase_count')}))
