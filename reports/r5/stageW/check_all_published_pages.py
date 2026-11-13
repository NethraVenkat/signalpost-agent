"""Replay every fetched page on previously published website candidates."""
import hashlib
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit
from audit import ROOT, DEST, load_runs
from signalpost.web.candidates import context_from_bulk
from signalpost.web.html import Page
from signalpost.web.policy import domain
from signalpost.web.publisher_veto import conflict


def main():
    checks = []
    for seed, work, registry, rows, report in load_runs():
        for row in rows:
            site = next((c['value'] for c in row['claims'] if c['field'] == 'official_website' and c['availability'] == 'available'), None)
            if not site:
                continue
            org = row['organisation_number']; context = context_from_bulk(registry.get(org, {}))
            context['subunits'] = [{'orgnr': c['field'].split('.')[-1]} for c in row['claims'] if c['field'].startswith('subunits.unit.') and c['availability'] == 'available']
            seen = set()
            for event in report['request_log']:
                sha = event.get('content_sha256')
                if event.get('organisation_number') != org or event.get('section') != 'website' or not sha or event.get('status') != 200 or domain(event['url']) != domain(site['final_url']):
                    continue
                if urlsplit(event['url']).path.endswith(('robots.txt', '.xml')) or (event['url'], sha) in seen:
                    continue
                seen.add((event['url'], sha))
                body = (work / 'state/blobs' / sha).read_bytes()
                assert hashlib.sha256(body).hexdigest() == sha
                page = Page(body, event['url']); rule, foreign = conflict(page, org, context)
                checks.append({'seed': seed, 'orgnr': org, 'name': context['name'], 'url': event['url'],
                               'sha256': sha, 'rule': rule, 'foreign_orgnrs': foreign})
    output = {'method': 'All saved fetched pages on the 29 historically published website candidates, including follow-up contact/about pages, not just selected proof pages.',
              'pages_checked': len(checks), 'rules': dict(Counter(c['rule'] or 'no_new_veto' for c in checks)), 'checks': checks}
    (DEST / 'r4_all_published_pages.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps({'pages_checked': len(checks), 'vetoes': [c for c in checks if c['rule']]}, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    main()
