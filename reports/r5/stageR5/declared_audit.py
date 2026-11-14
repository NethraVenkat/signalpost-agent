"""Offline declared-homepage gaps from the six accepted R4 runs, before R5."""
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

from signalpost.web.candidates import context_from_bulk
from signalpost.web.html import Page
from signalpost.web.policy import domain
from signalpost.web.publisher import extract_publisher
from signalpost.web.publisher_veto import conflict
from signalpost.web.challenge import detected

ROOT = Path(__file__).resolve().parents[3]
DEST = Path(__file__).resolve().parent
SEEDS = (20261017, 20261113, 20261114, 20261115, 20261116, 20261117)


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')


def records(stage, seed):
    settings = json.loads((ROOT / f'reports/r5/{stage}/seed{seed}/settings.json').read_text(encoding='utf8'))
    work = Path(settings['working_directory'])
    argv = settings['command_argv']
    with open(argv[argv.index('--bulk') + 1], encoding='utf-8-sig', newline='') as f:
        registry = {r['organisasjonsnummer']: r for r in csv.DictReader(f)}
    rows = [json.loads(line) for line in (work / 'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
    return settings, work, registry, rows, json.loads((work / 'report.json').read_text(encoding='utf8'))


def sites(row):
    return [c for c in row['claims'] if c['field'] == 'official_website' and c['availability'] == 'available']


def audit():
    gaps, totals, provenance = [], Counter(), []
    for seed in SEEDS:
        settings, work, registry, rows, report = records('stageW', seed)
        provenance.append({'seed': seed, 'work': str(work), 'envelopes_sha256': hashlib.sha256((work/'envelopes.jsonl').read_bytes()).hexdigest(),
                           'report_sha256': hashlib.sha256((work/'report.json').read_bytes()).hexdigest()})
        for row in rows:
            org = row['organisation_number']; identity = row['run'].get('legal_identity') or {}
            reg = registry.get(org) or {'navn':identity.get('legal_name'),'hjemmeside':identity.get('registered_website')}
            if not reg.get('hjemmeside'):
                continue
            totals['declared_homepages'] += 1
            if sites(row):
                totals['published_among_declared'] += 1
                continue
            context = context_from_bulk(reg)
            context['subunits'] = [{'orgnr': c['value']['organisation_number']} for c in row['claims'] if c['field'].startswith('subunits.unit.') and c['availability']=='available']
            attempts = [a for e in row['errors'] if e['section']=='website' and e['code']=='website_candidates' for a in json.loads(e['message'])]
            declared_attempts = [a for a in attempts if a.get('origin')=='registry_website' or a.get('domain')==domain(reg['hjemmeside'])]
            # Request ledger preserves redirects in request order. Include targets
            # only when the saved successful nomination explicitly identifies them.
            final_urls = {a['url'] for a in declared_attempts if a.get('url')}
            relevant_domains = {domain(reg['hjemmeside'])} | {domain(u) for u in final_urls}
            events = [e for e in report['request_log'] if e.get('organisation_number')==org and e.get('section')=='website' and domain(e['url']) in relevant_domains]
            pages = []
            for event in events:
                sha = event.get('content_sha256'); url = event['url']
                path = work / 'state/blobs' / str(sha)
                if not sha or not path.exists() or urlsplit(url).path.endswith(('robots.txt', '.xml')):
                    continue
                body = path.read_bytes()
                assert hashlib.sha256(body).hexdigest()==sha
                if b'<' not in body[:2048]:
                    continue
                page = Page(body, url); veto, others = conflict(page, org, context)
                pages.append({'url': url, 'status': event.get('status'), 'content_sha256': sha, 'title': page.title,
                              'publisher': [vars(f) for f in extract_publisher(page).fragments], 'r4_conflict': veto,
                              'foreign_orgnrs': others, 'challenge': detected(page)})
            reasons = {a.get('reason') for a in declared_attempts}
            cause = ('conflict' if any(p['r4_conflict'] for p in pages) else
                     'challenge' if any(p['challenge'] for p in pages) else
                     'fetched_without_proof' if any(p['status'] and 200<=p['status']<300 for p in pages) else
                     'robots' if reasons & {'robots','robots_unavailable'} else
                     'DNS' if reasons & {'no_such_domain','dns_timeout','dns_error','dns_unavailable'} else
                     'connect_timeout' if reasons & {'website_timeout','website_connect_error'} else
                     'redirect_refused' if 'url_refused' in reasons and any(e.get('status') in {301,302,303,307,308} for e in events) else
                     'HTTP' if any(e.get('status',0) and e['status']>=400 for e in events) else
                     'budget' if reasons & {'website_budget_exhausted','budget_exhausted','deadline'} else 'not_fetched_or_unknown')
            final_url = next((a['url'] for a in reversed(declared_attempts) if a.get('url') and a.get('status') and 200<=a['status']<300), None)
            final_url = final_url or next((p['url'] for p in reversed(pages) if p['status'] and 200<=p['status']<300),None)
            homepage = next(c for c in row['claims'] if c['field']=='identity.registered_website' and c['availability']=='available')
            receipts = [e for e in row['evidence'] if e['id'] in homepage['evidence_ids']]
            gaps.append({'seed': seed, 'orgnr': org, 'legal_name': reg['navn'], 'declared_url': reg['hjemmeside'], 'cause': cause,
                         'fetch_attempts': declared_attempts, 'request_chain': events, 'final_url': final_url,
                         'final_host': urlsplit(final_url).hostname if final_url else None,
                         'cross_registrable_redirect': domain(final_url)!=domain(reg['hjemmeside']) if final_url else None,
                         'registry_homepage_receipts': receipts, 'pages': pages,
                         'limitation': 'Saved-response diagnosis only. A missing final URL/redirect Location is unknown, never reconstructed from a name.'})
    assert totals['declared_homepages']==72 and totals['published_among_declared']==13 and len(gaps)==59
    result = {'baseline':dict(totals), 'gap_count':len(gaps), 'cause_counts':dict(Counter(g['cause'] for g in gaps)), 'provenance':provenance,'companies':gaps}
    save(DEST/'declared_gap.json',result)
    lines = ['# Declared-homepage gap before R5', '', 'Six accepted R4 runs; saved responses only, no new HTTP. 13/72 companies with registry homepages publish a site; 59 gaps. Registry declarations are recall labels, not independent current ownership proof.', '', 'Primary causes (exclusive): '+json.dumps(result['cause_counts']), '']
    for g in gaps:
        lines += [f"## {g['seed']} / {g['orgnr']} / {g['legal_name']}", '', f"Declared: {g['declared_url']}; cause: {g['cause']}; final host: {g['final_host']}; cross-domain redirect: {g['cross_registrable_redirect']}", '', '```json', json.dumps(g,ensure_ascii=False,indent=2),'```','']
    (DEST/'declared_gap.md').write_text('\n'.join(lines),encoding='utf8',newline='\n')
    print(json.dumps({'baseline':dict(totals),'gaps':len(gaps),'causes':result['cause_counts']}))


if __name__=='__main__':
    audit()
