"""Check R4 against all historically published sites using exact saved bytes."""
from signalpost.portable_paths import portable, portable_text  # saved paths stay repo-relative
import hashlib
import json
from pathlib import Path
from audit import DEST, load_runs
from signalpost.web.candidates import context_from_bulk
from signalpost.web.html import Page
from signalpost.web.publisher import extract_publisher
from signalpost.web.publisher_veto import conflict


def main():
    items = []
    for seed, work, registry, rows, report in load_runs():
        for row in rows:
            org = row['organisation_number']
            context = context_from_bulk(registry.get(org, {}))
            context['subunits'] = [{'orgnr': c['field'].split('.')[-1]} for c in row['claims'] if c['field'].startswith('subunits.unit.') and c['availability'] == 'available']
            refs = {e['id']: e for e in row['evidence']}
            for claim in row['claims']:
                if claim['field'] != 'official_website' or claim['availability'] != 'available':
                    continue
                value = claim['value']
                seen = set()
                for ref in claim['evidence_ids']:
                    e = refs[ref]
                    if e['source_class'] != 'company_owned':
                        continue
                    if e['content_sha256'] in seen or e['source_url'] != value['proof_page_url']:
                        continue
                    seen.add(e['content_sha256'])
                    raw = (work / 'state/blobs' / e['content_sha256']).read_bytes()
                    assert hashlib.sha256(raw).hexdigest() == e['content_sha256']
                    page = Page(raw, e['source_url'])
                    reason, foreign = conflict(page, org, context)
                    items.append({'seed': seed, 'orgnr': org, 'name': context['name'], 'website': value['final_url'],
                                  'tier': value['identity_level'], 'proof_page': e['source_url'], 'sha256': e['content_sha256'],
                                  'rule': reason, 'foreign_orgnrs': foreign,
                                  'publisher': [{'location': f.location, 'text': f.text} for f in extract_publisher(page).fragments]})
    result = {'method': 'New conflict guard applied to exact historically published proof-page receipts; no re-fetch or output edits',
              'published_sites_checked': len(items), 'vetoes': sum(bool(i['rule']) for i in items), 'items': items}
    (DEST / 'r4_published_replay.json').write_text(portable_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n'), encoding='utf8', newline='\n')
    print(json.dumps({'checked': len(items), 'vetoes': [{k: v for k, v in i.items() if k != 'publisher'} for i in items if i['rule']]}, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    main()
