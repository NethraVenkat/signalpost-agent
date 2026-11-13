"""Saved-response W0 audit. No publication or runtime behavior changes."""
import csv
import gzip
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

from signalpost.web.candidates import legal_name
from signalpost.web.html import Page
from signalpost.web.proof import orgnrs, phone, owner_identifiers, IDENTIFIER_META
from signalpost.web.policy import domain as registrable
from signalpost.web.publisher import extract_publisher

ROOT = Path(__file__).resolve().parents[3]
DEST = ROOT / 'reports/r5/stageW'
DOWNLOADS = Path('C:/Users/<USER>/Downloads/Signalpost/state/downloads')
SAMPLES = [(20261017, 'stageT/frozen'), (20261113, 'stageT/daily'),
           (20261114, 'stageT/mock')] + [(s, f'stageH/seed{s}') for s in range(20261115, 20261118)]


def folded(value):
    return ' '.join(re.findall(r'\w+', unicodedata.normalize('NFKC', str(value or '')).casefold()))


def literal(value):
    # Full legal-name audit is literal apart from case/Unicode/whitespace;
    # preserve punctuation and legal suffix, unlike the separate stem signal.
    return ' '.join(unicodedata.normalize('NFKC', str(value or '')).casefold().split())


class Regions(HTMLParser):
    """Audit locations retain body mentions, including explicitly excluded contexts."""
    def __init__(self, raw, url):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.regions = defaultdict(list)
        self.contact_page = bool(re.search(r'kontakt|contact|impressum|personvern|om[-/]?oss|about', urlsplit(url).path, re.I))
        self.feed(raw)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        marker = str(a.get('class', '')) + ' ' + str(a.get('id', ''))
        hidden = tag in {'script', 'style', 'template', 'noscript'} or 'hidden' in a or a.get('aria-hidden') == 'true' or bool(re.search(r'display\s*:\s*none|visibility\s*:\s*hidden', a.get('style') or '', re.I))
        if tag not in {'meta', 'link', 'img', 'br', 'hr', 'input', 'source', 'wbr', 'area', 'base', 'embed'}:
            self.stack.append((tag, marker, hidden, a.get('role')))
        if tag == 'meta' and a.get('property') == 'og:site_name':
            self.regions['og:site_name'].append(a.get('content') or '')
        if tag == 'img' and a.get('alt') and ('logo' in marker.lower() or any(t[0] == 'header' for t in self.stack)):
            self.regions['header/logo'].append(a['alt'])

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        text = ' '.join(data.split())
        if not text or any(t[2] for t in self.stack):
            return
        tags = {t[0] for t in self.stack}
        markers = ' '.join(t[1] for t in self.stack).lower()
        roles = {t[3] for t in self.stack}
        if 'title' in tags:
            self.regions['title'].append(text)
            return
        self.regions['body'].append(text)
        for location, yes in [('header', 'header' in tags or 'banner' in roles or 'header' in markers),
                              ('footer', 'footer' in tags or 'contentinfo' in roles or 'footer' in markers),
                              ('copyright', bool(re.search(r'©|copyright', text, re.I))),
                              ('imprint-kontakt', self.contact_page or 'address' in tags or bool(re.search(r'contact|kontakt|imprint', markers)))]:
            if yes:
                self.regions[location].append(text)


def contexts(page, registry, org):
    regions = {k: ' '.join(v) for k, v in Regions(page.raw, page.url).regions.items()}
    publisher = extract_publisher(page)
    # R1 now lets the final audit distinguish an actual contact block from
    # an arbitrary body mention on a contact page. Body/header locations remain
    # location observations, including third-party lists; they are not proof.
    regions['imprint-kontakt'] = ' '.join(f.text for f in publisher.fragments if f.location == 'imprint-kontakt')
    for location in ('header', 'footer'):
        regions[location] = ' '.join(f.text for f in publisher.fragments if f.location == location)
    regions['header/logo'] = ' '.join(f.text for f in publisher.fragments if f.location == 'logo')
    copyright_blocks = [f.text for f in publisher.fragments if f.location == 'copyright' or f.location == 'footer' and re.search(r'©|copyright', f.text, re.I)]
    regions['copyright'] = ' '.join(copyright_blocks)
    full = literal(registry.get('navn'))
    stem = legal_name(registry.get('navn'))
    locations = [k for k, v in regions.items() if full and re.search(r'(?<!\w)' + re.escape(full) + r'(?!\w)', literal(v))]
    body = regions.get('body', '')
    email = str(registry.get('epostadresse') or '').strip().casefold()
    expected_phone = phone(registry.get('telefon')) or phone(registry.get('mobil'))
    phones = {phone(m.group()) for m in re.finditer(r'(?:\+47|0047)?(?:\d[ .()-]*){8,12}', body)}
    phones.update(phone(link.href[4:]) for link in page.links if link.href.startswith('tel:'))
    streets = [s.strip() for s in str(registry.get('forretningsadresse.adresse') or '').split('\n') if s.strip() and not s.strip().casefold().startswith('c/o')]
    postcode = registry.get('forretningsadresse.postnummer')
    own = publisher.text
    id_locations = {'body': orgnrs(body),
                    'identifier_meta': orgnrs(' '.join(v for k, v in page.meta.items() if k.casefold() in IDENTIFIER_META)),
                    'owner_jsonld': set()}
    for document in page.jsonld:
        for value in owner_identifiers(document):
            id_locations['owner_jsonld'].update(orgnrs(value))
    other_ids = set().union(*id_locations.values()) - {org}
    forms = sorted(set(re.findall(r'(?<!\w)' + re.escape(stem) + r'\s+(AS|ASA|IKS|SA|ANS|DA|NUF|BA|KS|ENK)(?!\w)', folded(body), re.I))) if stem else []
    return {'full_legal_name_locations': locations, 'name_without_suffix': bool(stem and stem in legal_name(body)),
            'registry_phone': bool(expected_phone and expected_phone in phones),
            'registry_full_email': bool(email and email in page.raw.casefold()),
            'registry_email_domain': bool(email and '@' in email and email.rsplit('@', 1)[1] in page.raw.casefold()),
            'exact_street_and_postcode': bool(postcode and str(postcode) in body and any(s and folded(s) in folded(body) for s in streets)),
            'registry_declared_domain': host(registry.get('hjemmeside')) == host(page.url) if registry.get('hjemmeside') else False,
            'other_orgnrs': sorted(other_ids),
            'other_orgnr_locations': {number: [location for location, ids in id_locations.items() if number in ids] for number in sorted(other_ids)},
            'same_stem_legal_forms': forms,
            'other_legal_forms': [f for f in forms if f.upper() != str(registry.get('organisasjonsform.kode') or '').upper()],
            'group_parent_markers': re.findall(r'\b(?:group|gruppen|konsern|holding|parent|our companies|våre selskaper)\b', own, re.I),
            'publisher_role_markers': re.findall(r'\b(?:regnskap\w*|accountant\w*|advokat\w*|webbyrå\w*|web agency|eiendomsforvalt\w*)\b', own, re.I),
            'agency_credit_lines': [m.group() for m in re.finditer(r'.{0,80}(?:design|levert|utviklet)\s+av.{0,120}', body, re.I)][:3],
            'regions': regions}


def host(url):
    if not url:
        return None
    return (urlsplit(str(url) if '://' in str(url) else 'https://' + str(url)).hostname or '').lower().removeprefix('www.')


def load_runs():
    for seed, folder in SAMPLES:
        settings_path = ROOT / 'reports/r5' / folder / 'settings.json'
        settings = json.loads(settings_path.read_text(encoding='utf8'))
        work = Path(settings['working_directory'])
        argv = settings['command_argv']
        bulk = Path(argv[argv.index('--bulk') + 1])
        with bulk.open(encoding='utf-8-sig', newline='') as f:
            registry = {r['organisasjonsnummer']: r for r in csv.DictReader(f)}
        rows = [json.loads(line) for line in (work / 'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
        report = json.loads((work / 'report.json').read_text(encoding='utf8'))
        yield seed, work, registry, rows, report


def audit():
    DEST.mkdir(parents=True, exist_ok=True)
    rejections, dns, summaries, provenance = [], [], [], []
    proven_parents = {}
    nav = json.loads(gzip.decompress((ROOT / 'src/signalpost/data/nav_index.json.gz').read_bytes()))
    employers = {a['employer_orgnr'] for a in nav['ads']}
    with gzip.open(DOWNLOADS / 'universe.jsonl.gz', 'rt', encoding='utf8') as f:
        universe = {json.loads(line)['organisation_number'] for line in f}
    for seed, work, registry, rows, report in load_runs():
        counts = Counter()
        events = defaultdict(list)
        for event in report['request_log']:
            if event.get('section') == 'website':
                events[event.get('organisation_number')].append(event)
        for row in rows:
            org = row['organisation_number']
            identity = row['run'].get('legal_identity') or {}
            reg = registry.get(org) or {'navn': identity.get('legal_name'), 'hjemmeside': identity.get('registered_website')}
            claims = row['claims']
            sites = [c for c in claims if c['field'] == 'official_website' and c['availability'] == 'available']
            counts['companies'] += 1
            counts['websites'] += bool(sites)
            counts['exact_verified_websites'] += any(c['value']['identity_level'] == 'VERIFIED' for c in sites)
            counts['high_websites'] += any(c['value']['identity_level'] == 'HIGH' for c in sites)
            counts['job_companies'] += any(c['field'].startswith('hiring.job.') and c['availability'] == 'available' for c in claims)
            if reg.get('hjemmeside'):
                counts['declared_homepage'] += 1
                counts['declared_homepage_published'] += bool(sites)
                counts['declared_domain_published'] += any(host(c['value'].get('final_url')) == host(reg['hjemmeside']) for c in sites)
                for tier in ('VERIFIED', 'HIGH'):
                    counts['declared_domain_' + tier] += any(c['value']['identity_level'] == tier and host(c['value'].get('final_url')) == host(reg['hjemmeside']) for c in sites)
            for c in claims:
                if c['field'].startswith('subunits.unit.') and c['availability'] == 'available':
                    proven_parents[c['field'].split('.')[-1]] = org
            attempts = []
            for e in row['errors']:
                if e.get('section') == 'website' and e['code'] == 'website_candidates':
                    attempts.extend(json.loads(e['message']))
            categories = set()
            for a in attempts:
                reason = a.get('reason', '')
                if a.get('level') == 'REJECT':
                    categories.add('veto')
                if a.get('level') in {'LOW', 'MEDIUM', 'HIGH', 'REGISTRY_DECLARED'} and reason in {'corroboration', 'short_or_js_shell', 'registry_contact_missing', 'registry_and_live_corroboration'}:
                    categories.add('fetched-without-proof')
                if reason in {'no_such_domain', 'dns_unavailable', 'dns_timeout', 'dns_error'}:
                    dns.append({'seed': seed, 'orgnr': org, 'name': reg.get('navn'), 'host': a.get('domain') or host(a.get('url')), 'url': a.get('url'), 'recorded_reason': reason,
                                'historical_class': 'NXDOMAIN/name-not-found' if reason == 'no_such_domain' else 'timeout' if reason == 'dns_timeout' else 'unknown (resolver error or DNS nomination budget)'})
            if row['run']['sections'].get('website') == 'ambiguous':
                categories.add('ambiguous')
            if sites or not categories:
                continue
            counts.update(categories)
            for attempt in attempts:
                request = next((e['url'] for e in events[org] if registrable(e['url']) == attempt.get('domain') and not urlsplit(e['url']).path.endswith('robots.txt')), None)
                attempt['candidate_url'] = attempt.get('url') or request
                attempt['candidate_url_basis'] = ('saved attempt URL' if attempt.get('url') else
                                                  'earliest saved non-robots request to candidate domain (nomination URL may differ)' if request else
                                                  'URL not retained; domain only, no URL invented')
            pages = []
            for event in events[org]:
                sha = event.get('content_sha256')
                path = work / 'state/blobs' / str(sha)
                if not sha or not path.exists() or urlsplit(event['url']).path.endswith(('robots.txt', '.xml')):
                    continue
                body = path.read_bytes()
                if hashlib.sha256(body).hexdigest() != sha:
                    raise ValueError('saved response hash mismatch')
                if b'<' not in body[:2048]:
                    continue
                page = Page(body, event['url'])
                signals = contexts(page, reg, org)
                matching = [a for a in attempts if a.get('domain') == registrable(event['url']) and a.get('reason')]
                pages.append({'url': event['url'], 'content_sha256': sha, 'status': event.get('status'), 'title': page.title,
                              'recorded_rules': sorted({a['reason'] for a in matching}), 'signals': signals})
            rejections.append({'seed': seed, 'orgnr': org, 'name': reg.get('navn'), 'section_state': row['run']['sections'].get('website'),
                               'categories': sorted(categories), 'attempts': attempts, 'pages': pages,
                               'limitation': 'Rules are recorded candidate outcomes, not reconstructed per-page decisions; HTTP receipts establish fetched-page association.'})
        summaries.append({'seed': seed, **dict(counts)})
        provenance.append({'seed': seed, 'work': str(work), 'envelopes_sha256': hashlib.sha256((work / 'envelopes.jsonl').read_bytes()).hexdigest(),
                           'report_sha256': hashlib.sha256((work / 'report.json').read_bytes()).hexdigest()})
    # Only exact-parent proofs already saved in these runs are used. No guessed mapping.
    parent_employers = {proven_parents[e] for e in employers if e in proven_parents}
    represented = (employers | parent_employers) & universe
    jobs = {'index_built_at': nav['built_at'], 'ads': nav['ads_count'], 'index_employers': len(employers),
            'universe_size': len(universe), 'direct_employers_in_universe': len(employers & universe),
            'proven_parent_employers_in_universe': len(parent_employers & universe), 'unique_represented_companies': len(represented),
            'expected_per_1000_lower_bound': len(represented) / len(universe) * 1000,
            'measured_job_companies': sum(s.get('job_companies', 0) for s in summaries), 'measured_inputs': 600,
            'measured_per_1000': sum(s.get('job_companies', 0) for s in summaries) / 600 * 1000,
            'limitation': 'No full underenheter snapshot is available locally. Parent coverage is a lower bound from saved exact-parent proofs; index entries are discovery metadata, not current posting proof. Not a complete expected-rate estimate.'}
    unique_dns = {(r['seed'], r['orgnr'], r['host']): r for r in dns}
    result = {'method': 'W0 saved-response audit; no publication or scoring changes', 'samples': summaries, 'provenance': provenance,
              'category_counts': dict(Counter(c for r in rejections for c in r['categories'])), 'companies': rejections,
              'dns_records': dns, 'dns_historical_counts': dict(Counter(r['historical_class'] for r in dns)),
              'dns_unique_candidate_counts': dict(Counter(r['historical_class'] for r in unique_dns.values())),
              'dns_unique_hosts': len({r['host'] for r in dns}), 'jobs': jobs}
    (DEST / 'rejections.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
    lines = ['# W0 rejection audit', '', 'Saved receipts only. Categories overlap. All fetched pages and identity locations are retained in rejections.json. A candidate-level rule cannot be attributed to one particular fetched page when the old output did not save that association.', '', '| Seed | Companies | Published sites | Declared homepage | Declared with a published site | Declared domain published | Veto | Ambiguous | Fetched without proof |', '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for s in summaries:
        lines.append('| ' + ' | '.join(str(s.get(k, 0)) for k in ('seed', 'companies', 'websites', 'declared_homepage', 'declared_homepage_published', 'declared_domain_published', 'veto', 'ambiguous', 'fetched-without-proof')) + ' |')
    lines += ['', '## DNS history', '', json.dumps(result['dns_historical_counts']), '', 'Generic dns_unavailable cannot retrospectively distinguish SERVFAIL, timeout or another resolver error. no_such_domain is the OS name-not-found category; it is not a saved authoritative DNS RCODE. Fresh public-resolver checks are separately recorded.', '', '## NAV/universe overlap', '', '```json', json.dumps(jobs, indent=2), '```', '']
    for r in rejections:
        lines += [f"## {r['seed']} / {r['orgnr']} / {r['name']}", '', f"Categories: {', '.join(r['categories'])}; terminal website state: {r['section_state']}.", '']
        for a in r['attempts']:
            lines.append('- Candidate: ' + str(a.get('candidate_url') or ('URL not retained; host ' + str(a.get('domain')))) + '; URL basis: ' + a['candidate_url_basis'] + '; recorded rule: `' + str(a.get('reason')) + '`; level: ' + str(a.get('level', 'not saved')) + '.')
        for p in r['pages']:
            signals = dict(p['signals']); signals.pop('regions')
            lines += ['', f"Page: {p['url']} — title: {p['title']}", '', f"SHA-256: `{p['content_sha256']}`; candidate rules: {', '.join(p['recorded_rules'])}", '', '```json', json.dumps(signals, ensure_ascii=False, indent=2), '```']
        if not r['pages']:
            lines += ['', 'No HTML body associated with this company survives in the saved request ledger. No identity signals inferred.']
    (DEST / 'rejections.md').write_text('\n'.join(lines) + '\n', encoding='utf8', newline='\n')
    print(json.dumps({'samples': summaries, 'categories': result['category_counts'], 'dns': result['dns_historical_counts'], 'jobs': jobs}, indent=2))


if __name__ == '__main__':
    audit()
