"""Offline, deterministic profile presentation. Never modifies source envelopes."""
import html
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

from .models.shapes import validate
from .synthesis.nace import english_title

CSP = "default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; base-uri 'none'; form-action 'none'"
ASSETS = Path(__file__).with_name('site_assets')
GROUPS = [('what-it-does', 'What it does', 'identity'), ('financials', 'Financials', 'accounts'),
          ('people', 'People', 'roles'), ('locations', 'Locations', 'subunits'),
          ('online', 'Online presence', 'website'), ('hiring', 'Hiring', 'hiring'),
          ('activity', 'Public activity', 'activity')]
UNKNOWN = {'not_available': 'Checked; no information found within the source scope.',
           'failed': 'Check incomplete because a source or request budget was unavailable.',
           'blocked': 'Source access was refused by policy or robots.txt.',
           'not_applicable': 'This source is not applicable or was not enabled.',
           'ambiguous': 'Information could not be safely attributed to this company.'}


def esc(value):
    return html.escape(str(value), quote=True)


def safe_url(value):
    try:
        value = str(value)
        p = urlsplit(value)
        if p.scheme.lower() in {'http', 'https'} and p.hostname and not p.username and not p.password and not any(ord(c) < 32 for c in value):
            return value
    except ValueError:
        pass
    return None


def link(value, label=None):
    url = safe_url(value)
    return f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer nofollow">{esc(label if label is not None else value)}</a>' if url else esc(label if label is not None else value)


def chip(state):
    return f'<span class="chip {esc(state)}">{esc(state.replace("_", " "))}</span>'


def anchor(claim):
    # IDs come from validated claims, but prefix/hash conversion also prevents attribute injection.
    return 'fact-' + claim['id'][:16]


def normalize(raw):
    shape = 'union' if 'profile' in raw and 'claims' in raw else 'reference' if 'profile' in raw else 'contract'
    validate(raw, shape)
    if shape == 'reference':
        p = raw['profile']
        return {'organisation_number': raw['organisation_number'], 'claims': p['claims'], 'evidence': p['evidence'],
                'changes': p['changes'], 'run': {'sections': p['sections'], 'refresh': p['refresh'],
                'synthesis': p.get('synthesis'), 'completed_at': raw['completed_at']}}
    return raw


def registry_events(row):
    from types import SimpleNamespace
    from .registry_activity import recent
    from .models.claim import Claim
    from .models.evidence import Evidence
    obj = SimpleNamespace(run=SimpleNamespace(completed_at=row['run']['completed_at']),
                          claims=[Claim.model_validate(c) for c in row['claims']],
                          evidence=[Evidence.model_validate(e) for e in row['evidence']])
    return recent(obj)


def value_text(value):
    if value is None:
        return 'Unknown'
    if isinstance(value, bool):
        return 'Yes' if value else 'No'
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def display_time(value):
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M UTC')
    except (ValueError, AttributeError):
        return str(value)


def value_html(value):
    if isinstance(value, dict):
        return '<dl class="values">' + ''.join(f'<dt>{esc(k.replace("_", " "))}</dt><dd>{value_html(v)}</dd>' for k, v in sorted(value.items()) if k != 'birth_date') + '</dl>'
    if isinstance(value, list):
        return '<ul>' + ''.join('<li>' + value_html(v) + '</li>' for v in value) + '</ul>'
    return link(value) if isinstance(value, str) and safe_url(value) else esc(value_text(value))


def excerpt_html(span, value):
    # Highlight an exact leaf only, never markup from a source.
    leaves = []
    def walk(v):
        if isinstance(v, dict):
            for item in v.values(): walk(item)
        elif isinstance(v, list):
            for item in v: walk(item)
        elif v is not None: leaves.append(str(v))
    walk(value)
    match = next((v for v in sorted(leaves, key=len, reverse=True) if v and v in span), None)
    if not match:
        return esc(span)
    before, _, after = span.partition(match)
    return esc(before) + '<mark>' + esc(match) + '</mark>' + esc(after)


def evidence_panel(claim, records, shared=False):
    parts = []
    ids = claim.get('evidence_ids', [])
    for i, eid in enumerate(ids):
        e = records[eid]
        if not (e.get('source_url') or e.get('source_identifier')) or not e.get('retrieved_at') or not e.get('claim_span') or len(e['claim_span']) > 300 or not e.get('content_sha256') or not e.get('extraction_method'):
            raise ValueError('Incomplete evidence for displayed claim')
        if shared and i > 0:
            parts.append(f'<p><a href="#evidence-{esc(eid)}">Additional supporting source {i + 1}</a></p>')
            continue
        sha = e['content_sha256']
        parts.append('<div class="evidence-record"><dl class="values">'
                     f'<dt>Source / class</dt><dd>{esc(e["source_class"])}</dd>'
                     f'<dt>Source link</dt><dd>{link(e["source_url"])}</dd>'
                     f'<dt>Registry identifier</dt><dd>{esc(e.get("source_identifier") or "Not supplied")}</dd>'
                     f'<dt>Retrieved at (UTC)</dt><dd>{esc(e["retrieved_at"])}</dd>'
                     f'<dt>Effective / reporting date</dt><dd>{esc(value_text(e.get("effective_at") or e.get("reporting_period") or claim.get("reporting_period")))}</dd>'
                     f'<dt>SHA-256</dt><dd><code title="{esc(sha)}">{esc(sha[:16])}…</code> '
                     f'<button type="button" data-copy="{esc(sha)}">Copy full hash</button></dd>'
                     f'<dt>Extraction method / version</dt><dd>{esc(e["extraction_method"])}</dd>'
                     f'<dt>Locator</dt><dd>{esc(e["locator"])}</dd></dl>'
                     f'<blockquote class="excerpt">{excerpt_html(e["claim_span"], claim["value"])}</blockquote></div>')
    if claim['availability'] == 'available' and not parts:
        raise ValueError('Available fact has no evidence')
    v = claim.get('value')
    identity = v.get('identity_level') if isinstance(v, dict) else None
    if identity:
        parts.append('<p>Website identity level: ' + esc(identity) + '</p>')
    return ''.join(parts)


def fact(claim, records):
    local_id = claim['id'][:16]
    available = claim['availability'] == 'available'
    label = claim['field'].replace('identity.', '').replace('accounts.', '').replace('_', ' ')
    if claim['family'] in {'roles', 'subunits', 'hiring'} and isinstance(claim['value'], dict):
        v = claim['value']
        label = v.get('title') or v.get('name') or {'roles': 'Registered role', 'subunits': 'Registered workplace', 'hiring': 'Job advertisement'}[claim['family']]
    if claim['field'].startswith('website_description.'):
        label = "Company's own description"
    v = claim.get('value')
    title = english_title(v) if claim['field'].startswith('identity.nace') and isinstance(v, dict) else None
    content = value_html(v) if available else '<p>' + esc(UNKNOWN.get(claim['availability'], 'Unknown.')) + '</p>'
    if title:
        content = '<p>English industry title: ' + esc(title) + '</p>' + content
    if claim.get('carried_forward'):
        content = '<p class="stale">Previously supported; not freshly checked.</p>' + content
    period = claim.get('reporting_period')
    if period:
        content += '<p>Reporting period / currency / unit: ' + esc(value_text(period)) + '</p>'
    panel = bool(claim.get('evidence_ids') or available)
    if panel:
        content += f'<button type="button" aria-expanded="false" aria-controls="source-{esc(local_id)}" data-toggle="source-{esc(local_id)}">Source</button><div id="source-{esc(local_id)}" data-source="{esc(local_id)}" class="evidence" hidden></div>'
    if claim['family'] == 'accounts':
        return f'<tr id="{esc(anchor(claim))}"><th scope="row">{esc(label)} {chip(claim["availability"])}</th><td>{content}</td></tr>'
    return f'<article class="fact" id="{esc(anchor(claim))}"><h3>{esc(label)} {chip(claim["availability"])}</h3>{content}</article>'


def sentence_html(sentence, claim_map, change_ids):
    cites = []
    for n, cid in enumerate(sentence.get('claim_ids', []), 1):
        target = anchor(claim_map[cid]) if cid in claim_map else 'change-' + cid if cid in change_ids else None
        if target is None:
            raise ValueError('Unresolved synthesis citation')
        cites.append(f'<a href="#{esc(target)}" aria-label="Source fact {n}">[{n}]</a>')
    return '<p>' + esc(sentence['text']) + ' ' + ' '.join(cites) + '</p>'


def page(title, body, prefix='', kind='profile', company_data=None):
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<meta http-equiv="Content-Security-Policy" content="{esc(CSP)}">'
            f'<title>{esc(title)}</title><link rel="stylesheet" href="{prefix}assets/site.css">'
            f'<script src="{prefix}data/index.js" defer></script>'
            + (f'<script src="{esc(company_data)}" defer></script>' if company_data else '') +
            f'<script src="{prefix}assets/site.js" defer></script>'
            f'</head><body data-page="{kind}"><a class="skip" href="#main">Skip to content</a>'
            f'<nav aria-label="Main"><a class="brand" href="{prefix}index.html">Signalpost</a>'
            f'<a href="{prefix}index.html">Search companies</a><a href="{prefix}compare.html">Compare</a></nav>'
            f'<main id="main">{body}</main><footer>Evidence first. Unknown values remain unknown.</footer></body></html>\n')


def profile(row, title):
    claims = row['claims']
    claim_map = {c['id']: c for c in claims}
    records = {e['id']: e for e in row['evidence']}
    by_field = {c['field']: c['value'] for c in claims if c['availability'] == 'available'}
    org = row['organisation_number']
    synthesis = row['run'].get('synthesis') or {}
    support = synthesis.get('change_claims') or []
    change_ids = {c['id'] for c in support}
    name = by_field.get('identity.legal_name', org)
    body = f'<header><p class="eyebrow">Company profile</p><h1>{esc(name)}</h1><p>Organisation number: <code>{esc(org)}</code> <button type="button" data-copy="{esc(org)}">Copy organisation number</button></p>'
    for field in ('identity.organisation_form', 'identity.legal_form', 'identity.municipality'):
        if field in by_field:
            v = by_field[field]
            display = (str(v.get('beskrivelse') or '') + ' (' + str(v.get('kode') or '') + ')') if isinstance(v, dict) else value_text(v)
            body += '<p>' + esc(display) + '</p>'
    body += ''.join('<p><span class="chip">' + esc(c['field'].replace('identity.', '').replace('_', ' ')) + ': ' + esc(value_text(c['value'])) + '</span></p>' for c in claims if c['availability'] == 'available' and any(x in c['field'] for x in ('bankrupt', 'liquidation', 'deleted')))
    body += '<p>Last checked: <time>' + esc(display_time(row['run']['completed_at'])) + '</time></p></header>'
    sentences = [s for key in ('what_it_does', 'scale', 'leadership', 'changes') for s in synthesis.get('sections', {}).get(key, [])]
    body += '<section class="summary"><h2>Cited summary</h2>'
    body += ''.join(sentence_html(s, claim_map, change_ids) for s in sentences[:4])
    if len(sentences) > 4:
        body += '<button type="button" aria-expanded="false" aria-controls="full-summary" data-toggle="full-summary">Show full cited summary</button><div id="full-summary" hidden>'
        body += ''.join(sentence_html(s, claim_map, change_ids) for s in sentences[4:]) + '</div>'
    body += ''.join('<p class="muted">' + esc(u.get('text') or u['reason']) + '</p>' for u in synthesis.get('sections', {}).get('unknowns', [])) + '</section>'
    buckets = {key: [] for key, _, _ in GROUPS}
    for c in claims:
        f = c['field']; family = c['family']
        key = ('what-it-does' if f.startswith('website_description.') else
               'locations' if family == 'subunits' or 'address' in f else
               'online' if family == 'website' or f == 'identity.registered_website' else
               'financials' if family == 'accounts' else 'people' if family == 'roles' else
               'hiring' if family == 'hiring' else 'activity' if family == 'activity' else 'what-it-does')
        buckets[key].append(c)
    for key, label, family in GROUPS:
        items = buckets[key]
        details=[c for c in items if c['field'].startswith(('roles.detail.','subunits.detail.'))]
        items=[c for c in items if not c['field'].startswith(('roles.detail.','subunits.detail.'))]
        if key == 'activity': items.sort(key=lambda c: str((c['value'] or {}).get('date', '')) if isinstance(c['value'], dict) else '', reverse=True)
        state = row['run']['sections'].get(family, 'not_applicable')
        dated_registry = registry_events(row) if key == 'activity' else []
        public_state = 'available' if dated_registry and state in {'not_applicable','not_available'} else state
        body += f'<section id="{key}"><h2>{label} {chip(public_state)}</h2>'
        if key == 'activity':
            if dated_registry: body += '<h3>Recent registry dates</h3>'
            for day, label, c in dated_registry:
                body += '<p>' + esc(label + ': ' + day) + f' <a href="#fact-{esc(c.id[:16])}">Registry source</a></p>'
            body += '<h3>Website updates ' + chip(state) + '</h3>'
        if key == 'financials': body += '<p>Reported values from Regnskapsregisteret; no figures are calculated.</p>'
        if key == 'online': body += '<p>Website proof types: orgnr = exact registered number; registry_declared = registered site with corroboration; signals = accepted identity signals.</p>'
        if not items or state != 'available': body += '<p>' + esc(UNKNOWN.get(state, 'No facts published in this section.')) + '</p>'
        if key == 'financials' and items:
            body += '<table class="financial-table"><caption>Reported financial facts</caption><thead><tr><th scope="col">Metric</th><th scope="col">Value and evidence</th></tr></thead><tbody>'
        for i, c in enumerate(items):
            if key == 'locations' and i == 10:
                body += '<button type="button" aria-expanded="false" aria-controls="more-locations" data-toggle="more-locations">Show remaining workplaces</button><div id="more-locations" hidden>'
            body += fact(c, records)
        if key == 'locations' and len(items) > 10: body += '</div>'
        if key == 'financials' and items: body += '</tbody></table>'
        if details:
            body += '<details><summary>Additional official attributes ('+str(len(details))+')</summary><div data-registry-details="'+esc(key)+'"></div></details>'
        body += '</section>'
    body += '<section id="changes"><h2>Changes timeline</h2>'
    changes = sorted(row['changes'], key=lambda c: c['last_observed_at'], reverse=True)
    for event in changes: body += '<article class="fact"><p>' + esc(value_text(event)) + '</p></article>'
    if not changes: body += '<p>' + ('First observation' if row['run'].get('refresh', {}).get('mode') == 'baseline' else 'No changes since the previous run') + '</p>'
    for c in support:
        body += f'<div id="change-{esc(c["id"])}">{esc(value_text(c))}</div>'
    observations = row['run'].get('refresh', {}).get('observation_changes', [])
    body += '<button type="button" aria-expanded="false" aria-controls="observations" data-toggle="observations">Check status changes</button><div id="observations" hidden>' + value_html(observations) + '</div></section>'
    body += f'<p><a href="../index.html">Back to search</a> · <a href="../compare.html#{esc(org)}">Compare with…</a></p>'
    return page(str(name) + ' · ' + title, body, '../', company_data=org+'.data.js')


def company_payload(row):
    evidence={e['id']:e for e in row['evidence']}
    referenced=set()
    facts=[]
    def leaves(value):
        if isinstance(value,dict):
            for key,item in value.items():
                if key!='birth_date':yield from leaves(item)
        elif isinstance(value,list):
            for item in value:yield from leaves(item)
        elif value is not None:yield str(value)
    for claim in row['claims']:
        if not claim.get('evidence_ids') and claim['availability']!='available':continue
        # Validate the entire evidence set before writing any file.
        evidence_panel(claim,evidence)
        referenced.update(claim['evidence_ids'])
        v=claim.get('value')
        facts.append({'id':claim['id'][:16],'evidence_ids':claim['evidence_ids'],
                      'values':list(leaves(v)), 'reporting_period':claim.get('reporting_period'),
                      'identity_level':v.get('identity_level') if isinstance(v,dict) else None})
    if len({c['id'][:16] for c in row['claims']}) != len(row['claims']):
        raise ValueError('Conflicting local fact anchors')
    # Records from one response share source metadata. Store it once without losing fields.
    source_fields=['source_url','source_class','retrieved_at','content_sha256',
                   'extraction_method','source_identifier','reporting_period']
    evidence_fields=['id','claim_span','locator','effective_at']
    sources=[]; source_lookup={}; records=[]
    for eid in sorted(referenced):
        e=evidence[eid]
        shared=[e.get(k) for k in source_fields]
        key=json.dumps(shared,sort_keys=True,ensure_ascii=False)
        if key not in source_lookup:
            source_lookup[key]=len(sources);sources.append(shared)
        records.append([source_lookup[key]]+[e.get(k) for k in evidence_fields])
    details=[{'id':c['id'][:16],'field':c['field'],'value':c['value'],'availability':c['availability'],
              'group':'people' if c['family']=='roles' else 'locations'} for c in row['claims']
             if c['field'].startswith(('roles.detail.','subunits.detail.'))]
    return {'source_fields':source_fields,'sources':sources,'evidence_fields':evidence_fields,
            'records':records,'facts':facts,'registry_details':details}


def index_record(row):
    available = [c for c in row['claims'] if c['availability'] == 'available']
    fields = {c['field']: c for c in available}
    def get(field): return fields.get(field, {}).get('value')
    industry = next((c for c in available if c['field'].startswith('identity.nace')), None)
    iv = industry['value'] if industry else {}
    website = get('official_website')
    roles = [c for c in available if c['field'].startswith('roles.role.') and isinstance(c['value'],dict)]
    def role(code):
        return next((c for c in roles if (c['value'].get('role_type') or {}).get('kode') == code and not c['value'].get('inactive')), None)
    ceo, chair, auditor = role('DAGL'), role('LEDE'), role('REVI')
    result = {'orgnr': row['organisation_number'], 'name': get('identity.legal_name') or row['organisation_number'],
              'municipality': get('identity.municipality'), 'nace': iv.get('kode'), 'industry_en': english_title(iv) if iv else None,
              'industry_no': iv.get('beskrivelse'), 'employees': get('identity.employees'), 'revenue': get('accounts.revenue'),
              'annual_result': get('accounts.net_result'), 'fiscal_year': next(((c.get('reporting_period') or {}).get('fiscal_year') for c in available if c['family'] == 'accounts' and (c.get('reporting_period') or {}).get('fiscal_year')), None),
              'ceo': ceo['value'].get('name') if ceo else None, 'chair': chair['value'].get('name') if chair else None,
              'auditor': auditor['value'].get('name') if auditor else None,
              'workplaces': sum(c['field'].startswith('subunits.unit.') for c in available) if row['run']['sections'].get('subunits') == 'available' else None,
              'website': website.get('final_url') if isinstance(website, dict) else None,
              'social': sum(c['family'] == 'website' and 'social' in c['field'] for c in available),
              'jobs': sum(c['family'] == 'hiring' and not c.get('carried_forward') for c in available),
              'activity': sum(c['family'] == 'activity' for c in available) + len(registry_events(row)), 'sections': dict(row['run']['sections']),
              'claim_count': len(available), 'last_checked': row['run']['completed_at'], 'anchors': {}}
    mapping = {'name': 'identity.legal_name', 'municipality': 'identity.municipality', 'employees': 'identity.employees',
               'revenue': 'accounts.revenue', 'annual_result': 'accounts.net_result', 'website': 'official_website'}
    for key, field in mapping.items():
        if field in fields: result['anchors'][key] = anchor(fields[field])
    if industry: result['anchors']['industry'] = anchor(industry)
    for key, c in [('ceo', ceo), ('chair', chair), ('auditor', auditor)]:
        if c: result['anchors'][key] = anchor(c)
    result['flags'] = {key: bool(result[key]) for key in ('website', 'jobs', 'social', 'activity')}
    if result['activity'] and result['sections'].get('activity','not_applicable') in {'not_available','not_applicable'}:
        result['sections']['activity']='available'
    return result


def index_page(records, title):
    n = len(records)
    summary = f'{n} companies'
    for key in ('website', 'jobs', 'activity'):
        summary += f' · {sum(r["flags"][key] for r in records) / n * 100 if n else 0:.1f}% with {key}'
    summary += ' · Run date: ' + max((r['last_checked'] for r in records), default='Unknown')
    body = f'<header><p class="eyebrow">Company research, with receipts</p><h1>{esc(title)}</h1><p>{esc(summary)}</p></header>'
    body += '<section class="filters" aria-label="Company filters"><label>Search name or organisation number<input id="search" type="search" autocomplete="off"></label>'
    for key, label in [('municipality', 'Municipality'), ('division', 'NACE division')]:
        values = sorted({str(r['municipality']) for r in records if r['municipality']}) if key == 'municipality' else sorted({r['nace'][:2] for r in records if r['nace']})
        body += f'<label>{label}<select id="{key}"><option value="">All</option>' + ''.join(f'<option value="{esc(v)}">{esc(v)}</option>' for v in values) + '</select></label>'
    body += '<label>Sort<select id="sort"><option value="claim_count">Most data found</option><option value="name">Name</option><option value="revenue">Revenue</option><option value="employees">Employees</option></select></label>'
    for key, label in [('website', 'Verified website'), ('jobs', 'Job ads'), ('social', 'Social profiles'), ('activity', 'Public activity'), ('incomplete', 'Failed or blocked sections')]:
        body += f'<label class="check"><input id="filter-{key}" type="checkbox">{label}</label>'
    body += '</section><p id="result-count" role="status" aria-live="polite"></p><div id="results" class="results">'
    # Complete static fallback is useful when JavaScript is disabled and for indexing.
    for r in records:
        body += f'<article class="company"><h2><a href="c/{esc(r["orgnr"])}.html">{esc(r["name"])}</a></h2><p>{esc(r["orgnr"])} · {esc(r["municipality"] or "Unknown municipality")}</p></article>'
    body += '</div><div class="pagination"><button id="previous" type="button">Previous</button><span id="page-label"></span><button id="next" type="button">Next</button></div>'
    return page(title, body, kind='index')


def compare_page(title):
    body = '<header><p class="eyebrow">Side by side</p><h1>Compare companies</h1><p>Select two or three companies. Every value links to its profile evidence.</p></header><section class="filters">'
    for i in range(3): body += f'<label>Company {i + 1}<input type="search" id="company-{i}" list="company-options" autocomplete="off"></label>'
    body += '</section><datalist id="company-options"></datalist><p id="compare-status" role="status"></p><div id="comparison" class="comparison"></div>'
    return page('Compare · ' + title, body, kind='compare')


def generate_site(input_path, out, title='Signalpost'):
    input_path, out = Path(input_path), Path(out)
    if input_path.resolve().is_relative_to(out.resolve()):
        raise ValueError('Site directory must not contain its source envelopes')
    input_rows = [normalize(json.loads(line)) for line in input_path.read_text(encoding='utf-8-sig').splitlines() if line.strip()]
    unique={}
    for row in input_rows:
        org=row['organisation_number']
        if org in unique and unique[org]!=row:raise ValueError('Conflicting duplicate company envelopes')
        unique[org]=row
    rows=list(unique.values())
    if any(not re.fullmatch(r'\d{9}', r['organisation_number']) for r in rows):
        raise ValueError('Site filenames require nine digit identifiers')
    records = [index_record(r) for r in rows]
    payload = json.dumps(records, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)
    js_payload = payload.replace('</', '<\\/').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    files = {'index.html': index_page(records, title), 'compare.html': compare_page(title),
             'data/index.json': payload + '\n', 'data/index.js': 'window.SIGNALPOST_INDEX = ' + js_payload + ';\n'}
    for row in rows:
        org=row['organisation_number']
        files['c/' + org + '.html'] = profile(row, title)
        data=json.dumps(company_payload(row),ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
        data=data.replace('</','<\\/').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
        files['c/'+org+'.data.js']='window.SIGNALPOST_EVIDENCE = '+data+';\n'
    for filename in ('site.css', 'site.js'): files['assets/' + filename] = (ASSETS / filename).read_text(encoding='utf8')
    # Render everything before writes: template errors cannot leave half a new site.
    if any(len(content.encode('utf8')) >= 250_000 for path, content in files.items() if path.startswith('c/') and path.endswith('.html')):
        raise ValueError('Profile page exceeds 250 KB gate')
    for filename, content in files.items():
        target = out / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding='utf8', newline='\n')
    sizes = {filename: len(content.encode('utf8')) for filename, content in files.items()}
    return {'companies': len(rows), 'input_records':len(input_rows), 'pages': len(rows) + 2, 'total_bytes': sum(sizes.values()),
            'largest_profile_data_bytes':max((size for path,size in sizes.items() if path.endswith('.data.js')),default=0),
            'largest_profile_bytes': max((size for path, size in sizes.items() if path.startswith('c/') and path.endswith('.html')), default=0)}
