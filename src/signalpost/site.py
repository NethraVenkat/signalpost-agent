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


def sanitize_csv_cell(value):
    if value is None:
        return ""
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, (dict, list)):
        s = json.dumps(value, ensure_ascii=False, sort_keys=True)
    else:
        s = str(value)
    # Preserve legitimate numeric literals including negative numbers (e.g. -50000, -12.34)
    if re.match(r'^-?\d+(?:\.\d+)?$', s.strip()):
        return s.strip()
    # Sanitize formula injection triggers (including leading whitespace/control characters)
    stripped = re.sub(r'^[\s\x00-\x1f\x7f-\x9f\u200b-\u200d\u2060\ufeff]+', '', s)
    if stripped and stripped[0] in ('=', '+', '-', '@'):
        s = "'" + s
    elif s and (ord(s[0]) < 32 or 127 <= ord(s[0]) <= 159):
        s = "'" + s
    if any(c in s for c in (',', '"', '\n', '\r')):
        s = '"' + s.replace('"', '""') + '"'
    return s


def format_csv_orgnr(orgnr):
    return str(orgnr).strip()


def export_directory_csv(records):
    headers = [
        "Organisation number", "Name", "Municipality", "Industry code", "Industry title",
        "Employees", "Size band", "Revenue", "Annual result", "Currency", "Financial unit", "Fiscal year",
        "Verified website", "Website provenance", "Job postings", "Social profiles",
        "Public activity", "Claim count", "Last checked"
    ]
    lines = [",".join(headers)]
    for r in records:
        row = [
            format_csv_orgnr(r.get("orgnr", "")),
            sanitize_csv_cell(r.get("name")),
            sanitize_csv_cell(r.get("municipality")),
            sanitize_csv_cell(r.get("nace")),
            sanitize_csv_cell(r.get("industry_en") or r.get("industry_no")),
            sanitize_csv_cell(r.get("employees")),
            sanitize_csv_cell(r.get("size_band")),
            sanitize_csv_cell(r.get("revenue")),
            sanitize_csv_cell(r.get("annual_result")),
            sanitize_csv_cell(r.get("currency") or ""),
            sanitize_csv_cell(r.get("unit") or ""),
            sanitize_csv_cell(r.get("fiscal_year")),
            sanitize_csv_cell(r.get("website")),
            sanitize_csv_cell(r.get("website_origin")),
            sanitize_csv_cell(r.get("jobs")),
            sanitize_csv_cell(r.get("social")),
            sanitize_csv_cell(r.get("activity")),
            sanitize_csv_cell(r.get("claim_count")),
            sanitize_csv_cell(r.get("last_checked")),
        ]
        lines.append(",".join(row))
    return "\r\n".join(lines) + "\r\n"


def export_directory_json(records):
    return json.dumps(records, indent=2, ensure_ascii=False)


def export_profile_claims_json(row):
    claims = row.get("claims", [])
    evidence_map = {e["id"]: e for e in row.get("evidence", [])}
    items = []
    for c in claims:
        item = {
            "id": c.get("id"),
            "field": c.get("field"),
            "family": c.get("family"),
            "availability": c.get("availability"),
            "value": c.get("value"),
            "reporting_period": c.get("reporting_period"),
            "carried_forward": c.get("carried_forward", False),
            "evidence": []
        }
        for eid in c.get("evidence_ids", []):
            if eid in evidence_map:
                e = evidence_map[eid]
                item["evidence"].append({
                    "id": e.get("id"),
                    "source_class": e.get("source_class"),
                    "source_url": e.get("source_url"),
                    "source_identifier": e.get("source_identifier"),
                    "locator": e.get("locator"),
                    "claim_span": e.get("claim_span"),
                    "content_sha256": e.get("content_sha256"),
                    "retrieved_at": e.get("retrieved_at"),
                    "effective_at": e.get("effective_at"),
                    "extraction_method": e.get("extraction_method"),
                })
        items.append(item)
    payload = {
        "organisation_number": row.get("organisation_number"),
        "claims_count": len(items),
        "exported_at": datetime.now().isoformat() + "Z",
        "claims": items
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def export_profile_summary_csv(row):
    headers = [
        "Organisation number", "Field", "Family", "Availability",
        "Value", "Reporting period", "Evidence count", "Primary source class",
        "Primary source URL", "Primary locator", "Primary SHA-256", "Primary excerpt"
    ]
    org = row.get("organisation_number", "")
    evidence_map = {e["id"]: e for e in row.get("evidence", [])}
    lines = [",".join(headers)]
    for c in row.get("claims", []):
        eids = c.get("evidence_ids", [])
        primary = evidence_map.get(eids[0]) if eids else None
        val_str = value_text(c.get("value"))
        row_cells = [
            format_csv_orgnr(org),
            sanitize_csv_cell(c.get("field")),
            sanitize_csv_cell(c.get("family")),
            sanitize_csv_cell(c.get("availability")),
            sanitize_csv_cell(val_str),
            sanitize_csv_cell(value_text(c.get("reporting_period")) if c.get("reporting_period") else ""),
            sanitize_csv_cell(len(eids)),
            sanitize_csv_cell(primary.get("source_class") if primary else ""),
            sanitize_csv_cell(primary.get("source_url") if primary else ""),
            sanitize_csv_cell(primary.get("locator") if primary else ""),
            sanitize_csv_cell(primary.get("content_sha256") if primary else ""),
            sanitize_csv_cell(primary.get("claim_span") if primary else ""),
        ]
        lines.append(",".join(row_cells))
    return "\r\n".join(lines) + "\r\n"


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
        content = '<p class="stale">Previously supported; not freshly checked. Last successfully checked: ' + esc(display_time(claim.get('last_observed_at'))) + '.</p>' + content
    period = claim.get('reporting_period')
    if period:
        parts = []
        if period.get('fiscal_year'): parts.append(f"Fiscal year: {period['fiscal_year']}")
        if period.get('period_start') and period.get('period_end'): parts.append(f"Accounting period: {period['period_start']} to {period['period_end']}")
        parts.append(f"Currency: {period.get('currency') or 'Unknown'}")
        if period.get('unit'): parts.append(f"Unit: {period['unit']}")
        content += '<p class="financial-meta muted">' + esc(' · '.join(parts)) + '</p>'
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
            f'<a href="{prefix}index.html">Dashboard</a>'
            f'<a href="{prefix}index.html#directory">Directory</a>'
            f'<a href="{prefix}compare.html">Compare</a>'
            f'<button type="button" id="status-toggle" class="status-toggle" aria-label="Toggle update status panel" aria-expanded="false" aria-controls="status-panel">'
            '<span id="status-dot" class="status-dot"></span> Update status</button>'
            f'<button type="button" id="theme-toggle" class="theme-toggle" aria-label="Toggle dark mode">Theme</button></nav>'
            '<div id="status-panel" class="status-panel" role="dialog" aria-modal="true" aria-label="Update status" hidden>'
            '<div class="status-panel-inner">'
            '<div class="status-panel-header">'
            '<h2>Update status <span id="status-badge" class="chip"></span></h2>'
            '<button type="button" id="status-close" class="status-close" aria-label="Close update status panel">&times;</button>'
            '</div>'
            '<div class="status-progress-section">'
            '<div class="status-progress-bar-wrap"><progress id="status-progress" max="100" value="0"></progress></div>'
            '<p id="status-progress-text" class="status-progress-text"></p>'
            '</div>'
            '<div class="status-section">'
            '<h3>Companies</h3>'
            '<div id="status-counters" class="status-counters"></div>'
            '</div>'
            '<div class="status-section">'
            '<h3>Pipeline stages</h3>'
            '<div id="status-stages" class="status-stages"></div>'
            '</div>'
            '<div class="status-section">'
            '<h3>Timing &amp; resources</h3>'
            '<dl id="status-timing" class="values status-timing"></dl>'
            '</div>'
            '<div class="status-section">'
            '<h3>Recent events</h3>'
            '<div id="status-events" class="status-events"></div>'
            '</div>'
            '<p id="status-snapshot-note" class="status-snapshot-note muted" hidden></p>'
            '</div></div>'
            f'<main id="main">{body}</main><footer>Evidence first. Unknown values remain unknown.</footer></body></html>\n')


EXPLORER_VISIBLE_ROWS = 50


def explorer_cells(c, records):
    """Plain-text cells for one Evidence Explorer row (page and data file share this)."""
    f = c.get('field', '')
    v_str = value_text(c.get('value'))
    if len(v_str) > 80: v_str = v_str[:77] + '…'
    eids = c.get('evidence_ids', [])
    e = records.get(eids[0]) if eids else None
    span = e.get('claim_span', '—') if e else '—'
    if len(span) > 100: span = span[:97] + '…'
    return [f.replace('identity.', '').replace('accounts.', '').replace('_', ' '), c.get('availability', 'unknown'), v_str,
            e.get('source_class', '—') if e else '—', e.get('locator', '—') if e else '—',
            e.get('content_sha256', '') if e else '', span]


def profile(row, title):
    claims = row['claims']
    claim_map = {c['id']: c for c in claims}
    records = {e['id']: e for e in row['evidence']}
    by_field = {c['field']: c['value'] for c in claims if c['availability'] == 'available'}
    fields_map = {c['field']: c for c in claims if c['availability'] == 'available'}
    org = row['organisation_number']
    synthesis = row['run'].get('synthesis') or {}
    support = synthesis.get('change_claims') or []
    change_ids = {c['id'] for c in support}
    name = by_field.get('identity.legal_name', org)
    body = f'<header><p class="eyebrow">Company profile</p><h1>{esc(name)}</h1><p>Organisation number: <code>{esc(org)}</code> <button type="button" data-copy="{esc(org)}">Copy organisation number</button> <button type="button" class="btn-watchlist" data-watchlist="{esc(org)}">⭐ Watchlist</button></p>'
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
        if key == 'financials':
            body += '<p>Reported values from Regnskapsregisteret; no figures or growth ratios are calculated.</p>'
            years = sorted({(c.get('reporting_period') or {}).get('fiscal_year') for c in items if (c.get('reporting_period') or {}).get('fiscal_year')}, reverse=True)
            currencies = sorted({(c.get('reporting_period') or {}).get('currency') for c in items if (c.get('reporting_period') or {}).get('currency')})
            curr_str = ", ".join(currencies) if currencies else "NOK"
            if len(years) > 1:
                body += f'<div class="financial-trend-banner"><p><strong>Multi-year filing trend:</strong> Accounts filed across {len(years)} fiscal years ({", ".join(str(y) for y in years)}). Reporting currency: {esc(curr_str)}. No derived growth ratios are calculated.</p></div>'
            elif len(years) == 1:
                body += f'<div class="financial-trend-banner"><p><strong>Reporting period:</strong> Fiscal year {years[0]} filed in Regnskapsregisteret ({esc(curr_str)}). Single-year reported values.</p></div>'
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

    # 5. Verified Company Timeline (Dated business events)
    timeline_events = []
    founding_items = [
        ('identity.founding_date', 'Company founded', 'Founding'),
        ('identity.registration_date', 'Registered in Enhetsregisteret', 'Registry'),
        ('identity.vat_registration_date', 'Registered for VAT', 'Registry')
    ]
    for fld, lbl, tlabel in founding_items:
        if fld in fields_map:
            c = fields_map[fld]
            val = str(c.get('value', ''))
            if val:
                timeline_events.append({
                    'date': val[:10],
                    'label': lbl,
                    'detail': f'Official date in Brønnøysundregistrene: {val}',
                    'type_class': 'available',
                    'type_label': tlabel,
                    'anchor': anchor(c)
                })

    seen_fiscal_years = set()
    for c in claims:
        if c['family'] == 'accounts' and c['availability'] == 'available' and c.get('reporting_period'):
            period = c['reporting_period']
            f_year = period.get('fiscal_year')
            p_end = period.get('period_end') or (f'{f_year}-12-31' if f_year else None)
            if f_year and f_year not in seen_fiscal_years and p_end:
                seen_fiscal_years.add(f_year)
                rev = by_field.get('accounts.revenue')
                res = by_field.get('accounts.net_result')
                details_parts = []
                curr = period.get('currency') or 'Unknown currency'
                if rev is not None: details_parts.append(f'Revenue: {value_text(rev)} {esc(curr)}')
                if res is not None: details_parts.append(f'Net result: {value_text(res)} {esc(curr)}')
                detail_str = f'Fiscal year {f_year} filed in Regnskapsregisteret' + (f' ({", ".join(details_parts)})' if details_parts else '')
                timeline_events.append({
                    'date': str(p_end)[:10],
                    'label': f'Financial accounts ({f_year})',
                    'detail': detail_str,
                    'type_class': 'available',
                    'type_label': 'Financials',
                    'anchor': anchor(c)
                })

    for c in claims:
        if c['family'] == 'hiring' and c['availability'] == 'available' and isinstance(c.get('value'), dict):
            j = c['value']
            pub = j.get('published')
            if pub:
                title_ad = j.get('title') or 'Job advertisement'
                via = f" (matched via {j['matched_via']})" if j.get('matched_via') else ''
                timeline_events.append({
                    'date': str(pub)[:10],
                    'label': f'Job posted: {title_ad}',
                    'detail': f'Active job advertisement on Arbeidsplassen (NAV){via}',
                    'type_class': 'available',
                    'type_label': 'Hiring',
                    'anchor': anchor(c)
                })

    dated_reg = registry_events(row)
    for day, lbl, c in dated_reg:
        c_anchor = f'fact-{c.id[:16]}' if hasattr(c, 'id') else anchor(c)
        if not any(e['date'] == day and lbl in e['label'] for e in timeline_events):
            timeline_events.append({
                'date': day,
                'label': f'Registry event: {lbl}',
                'detail': 'Filing recorded in Norwegian business registry',
                'type_class': 'available',
                'type_label': 'Registry',
                'anchor': c_anchor
            })

    changes = sorted(row['changes'], key=lambda c: c['last_observed_at'], reverse=True)
    for event in changes:
        if event.get('last_observed_at'):
            timeline_events.append({
                'date': event['last_observed_at'][:10],
                'label': f"Verified change: {event.get('field', 'Attribute').replace('_', ' ')}",
                'detail': 'Previous verified value updated in registry refresh',
                'type_class': 'available',
                'type_label': 'Change',
                'anchor': None
            })

    timeline_events.sort(key=lambda e: (e['date'], e['label']), reverse=True)

    body += '<section id="timeline" class="company-timeline"><h2>Company timeline</h2>'
    body += '<p class="timeline-note muted">Verified dates from official registry filings, financial accounts, and job postings. Retrieval and observation timestamps are excluded. Timeline does not represent an exhaustive company history.</p>'
    if timeline_events:
        body += '<div class="timeline-container">'
        for ev in timeline_events:
            body += '<div class="timeline-item"><div class="timeline-node" aria-hidden="true"></div><div class="timeline-body">'
            body += f'<div class="timeline-meta"><time class="timeline-date">{esc(ev["date"])}</time><span class="chip {esc(ev["type_class"])}">{esc(ev["type_label"])}</span></div>'
            body += f'<h3 class="timeline-title">{esc(ev["label"])}</h3>'
            if ev.get('detail'):
                body += f'<p class="timeline-detail">{esc(ev["detail"])}</p>'
            if ev.get('anchor'):
                body += f'<p class="timeline-link"><a href="#{esc(ev["anchor"])}">View source evidence</a></p>'
            body += '</div></div>'
        body += '</div>'
    else:
        body += '<p class="timeline-empty">No dated business events verified for this entity.</p>'
    body += '</section>'

    body += '<section id="changes" class="changes-section"><h2>Verified changes &amp; freshness</h2>'
    body += f'<div class="freshness-banner"><p><strong>Last verified:</strong> <time class="verified-time">{esc(display_time(row["run"]["completed_at"]))}</time> <span class="chip available">{esc(row["run"].get("refresh", {}).get("mode", "baseline"))}</span></p></div>'

    # Business changes subsection
    body += '<h3>Verified business changes</h3>'
    if changes:
        body += '<div class="changes-list">'
        for event in changes:
            field_name = event.get('field', 'Attribute').replace('identity.', '').replace('accounts.', '').replace('_', ' ')
            ch_type = event.get('type', 'changed')
            mat = event.get('materiality', 'material')
            old_ids = event.get('old_evidence_ids', [])
            new_ids = event.get('new_evidence_ids', [])
            old_ev = records.get(old_ids[0]) if old_ids else None
            new_ev = records.get(new_ids[0]) if new_ids else None
            old_loc = event.get('old_locator') or (old_ev.get('locator') if old_ev else '—')
            new_loc = event.get('new_locator') or (new_ev.get('locator') if new_ev else '—')
            old_sha = event.get('old_content_sha256') or (old_ev.get('content_sha256') if old_ev else '')
            new_sha = event.get('new_content_sha256') or (new_ev.get('content_sha256') if new_ev else '')
            old_val_html = value_html(event.get('old_value')) if event.get('old_value') is not None else '<span class="muted">None (added)</span>'
            new_val_html = value_html(event.get('new_value')) if event.get('new_value') is not None else '<span class="muted">None (removed)</span>'
            old_sha_disp = f'<code title="{esc(old_sha)}">{esc(old_sha[:12])}…</code>' if old_sha else '—'
            new_sha_disp = f'<code title="{esc(new_sha)}">{esc(new_sha[:12])}…</code>' if new_sha else '—'

            body += f'<article class="change-card"><div class="change-card-header"><h4>Change in: {esc(field_name)}</h4><div><span class="chip available">{esc(ch_type)}</span> <span class="chip not_applicable">{esc(mat)}</span></div></div>'
            body += f'<p class="change-time muted">Observed: <time>{esc(display_time(event.get("last_observed_at")))}</time></p>'
            body += '<div class="change-comparison-grid">'
            body += f'<div class="change-col change-col-prev"><h5>Previous value</h5><div class="change-val">{old_val_html}</div><dl class="values values-compact"><dt>Locator</dt><dd><code>{esc(old_loc)}</code></dd><dt>SHA-256</dt><dd>{old_sha_disp}</dd></dl></div>'
            body += f'<div class="change-col change-col-curr"><h5>Current value</h5><div class="change-val">{new_val_html}</div><dl class="values values-compact"><dt>Locator</dt><dd><code>{esc(new_loc)}</code></dd><dt>SHA-256</dt><dd>{new_sha_disp}</dd></dl></div>'
            body += '</div></article>'
        body += '</div>'
    else:
        mode_note = 'First observation (baseline run).' if row['run'].get('refresh', {}).get('mode') == 'baseline' else 'No business changes detected since the previous verification run.'
        body += f'<p class="muted">{esc(mode_note)}</p>'

    for c in support:
        body += f'<div id="change-{esc(c["id"])}">{esc(value_text(c))}</div>'

    # Source availability & observation changes subsection
    observations = row['run'].get('refresh', {}).get('observation_changes', [])
    body += '<div class="observation-changes-section"><h3>Source availability &amp; observation changes</h3>'
    body += '<p class="muted">Operational shifts in source availability (e.g. rate limits, timeouts, schema updates) tracked separately from business modifications.</p>'
    if observations:
        body += '<div class="table-responsive"><table class="observation-table"><thead><tr><th scope="col">Section / Source</th><th scope="col">Previous State</th><th scope="col">Current State</th><th scope="col">Reason / Detail</th></tr></thead><tbody>'
        for ob in observations:
            sec = ob.get('section', 'general')
            prev_st = ob.get('previous_state', '—')
            curr_st = ob.get('current_state', '—')
            rsn = ob.get('reason', '—')
            fld = ob.get('field')
            sec_lbl = f'{sec}.{fld}' if fld else sec
            body += f'<tr><td><strong>{esc(sec_lbl)}</strong></td><td>{chip(prev_st)}</td><td>{chip(curr_st)}</td><td>{esc(rsn)}</td></tr>'
        body += '</tbody></table></div>'
    else:
        body += '<p class="muted">No source observation or availability transitions occurred during this verification run.</p>'
    body += '</div></section>'

    # Evidence Explorer Section
    body += '<section id="evidence-explorer" class="evidence-explorer">'
    body += '<div class="evidence-explorer-header">'
    body += '<h2>Evidence Explorer</h2>'
    body += '<div class="export-actions">'
    body += '<button type="button" id="export-profile-json" class="btn-export">Export Provenance (JSON)</button> '
    body += '<button type="button" id="export-profile-csv" class="btn-export">Export Summary (CSV)</button>'
    body += '</div></div>'
    body += '<p class="muted">Audit trail of verified company facts with complete supporting provenance, exact source locators, cryptographic SHA-256 receipts, and verbatim source excerpts.</p>'
    body += '<div class="table-responsive"><table class="evidence-explorer-table" aria-label="Evidence Explorer audit trail">'
    body += '<thead><tr><th scope="col">Fact / Claim</th><th scope="col">Status</th><th scope="col">Value</th><th scope="col">Source Class</th><th scope="col">Locator</th><th scope="col">SHA-256</th><th scope="col">Verbatim Excerpt</th></tr></thead><tbody>'
    for c in claims[:EXPLORER_VISIBLE_ROWS]:
        lbl, avail, v_str, s_class, loc, sha, span = explorer_cells(c, records)
        sha_disp = f'<code title="{esc(sha)}">{esc(sha[:12])}…</code>' if sha else '—'
        body += f'<tr><th scope="row">{esc(lbl)}</th><td>{chip(avail)}</td><td>{esc(v_str)}</td><td>{esc(s_class)}</td><td><code>{esc(loc)}</code></td><td>{sha_disp}</td><td><blockquote class="table-excerpt">{esc(span)}</blockquote></td></tr>'
    body += '</tbody></table></div>'
    hidden = len(claims) - EXPLORER_VISIBLE_ROWS
    if hidden > 0:
        body += (f'<p class="muted" id="explorer-more-note">Showing {EXPLORER_VISIBLE_ROWS} of {len(claims)} claims; every claim stays in the exports and the company data file.</p>'
                 f'<button type="button" id="explorer-show-all" data-hidden="{hidden}">Show the remaining {hidden} claims</button>')
    body += '</section>'

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
                      'field':claim.get('field'),'family':claim.get('family'),'availability':claim.get('availability'),
                      'values':list(leaves(v)), 'value':v, 'reporting_period':claim.get('reporting_period'),
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
    name = next((c['value'] for c in row['claims'] if c['field'] == 'identity.legal_name' and c['availability'] == 'available'), row['organisation_number'])
    all_records = {e['id']: e for e in row['evidence']}
    payload = {'orgnr': row['organisation_number'], 'name': name,
               'source_fields':source_fields,'sources':sources,'evidence_fields':evidence_fields,
               'records':records,'facts':facts,'registry_details':details}
    if len(row['claims']) > EXPLORER_VISIBLE_ROWS:
        payload['explorer_rows'] = [explorer_cells(c, all_records) for c in row['claims'][EXPLORER_VISIBLE_ROWS:]]
    return payload


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

    emp = get('identity.employees')
    if emp is None:
        size_band = 'unknown'
    else:
        try:
            n = int(emp)
            if n == 0: size_band = 'zero'
            elif 1 <= n <= 9: size_band = 'micro'
            elif 10 <= n <= 49: size_band = 'small'
            elif 50 <= n <= 249: size_band = 'medium'
            elif n >= 250: size_band = 'large'
            else: size_band = 'unknown'
        except (ValueError, TypeError):
            size_band = 'unknown'

    founding_date = get('identity.founding_date') or get('identity.registration_date')
    web_origin = website.get('candidate_origin') if isinstance(website, dict) else None
    web_proof = website.get('proof_type') if isinstance(website, dict) else None

    job_postings = []
    for c in available:
        if c['family'] == 'hiring' and isinstance(c.get('value'), dict):
            j = c['value']
            job_postings.append({
                'title': j.get('title') or 'Job advertisement',
                'published': str(j.get('published'))[:10] if j.get('published') else None,
                'expires': str(j.get('expires'))[:10] if j.get('expires') else None,
                'matched_via': j.get('matched_via'),
                'anchor': anchor(c),
                'uuid': j.get('uuid')
            })
    job_titles = [j['title'] for j in job_postings if j.get('title')]
    job_dates = [j['published'] for j in job_postings if j.get('published')]

    reg_events = registry_events(row)
    latest_event = reg_events[0] if reg_events else None

    result = {'orgnr': row['organisation_number'], 'name': get('identity.legal_name') or row['organisation_number'],
              'municipality': get('identity.municipality'), 'nace': iv.get('kode'), 'industry_en': english_title(iv) if iv else None,
              'industry_no': iv.get('beskrivelse'), 'employees': emp, 'size_band': size_band,
              'revenue': get('accounts.revenue'),
              'annual_result': get('accounts.net_result'), 'fiscal_year': next(((c.get('reporting_period') or {}).get('fiscal_year') for c in available if c['family'] == 'accounts' and (c.get('reporting_period') or {}).get('fiscal_year')), None),
              'currency': next(((c.get('reporting_period') or {}).get('currency') for c in available if c['family'] == 'accounts' and (c.get('reporting_period') or {}).get('currency')), None) if (get('accounts.revenue') is not None or get('accounts.net_result') is not None) else None,
              'unit': next(((c.get('reporting_period') or {}).get('unit') for c in available if c['family'] == 'accounts' and (c.get('reporting_period') or {}).get('unit')), None) if (get('accounts.revenue') is not None or get('accounts.net_result') is not None) else None,
              'founding_date': str(founding_date) if founding_date else None,
              'ceo': ceo['value'].get('name') if ceo else None, 'chair': chair['value'].get('name') if chair else None,
              'auditor': auditor['value'].get('name') if auditor else None,
              'workplaces': sum(c['field'].startswith('subunits.unit.') for c in available) if row['run']['sections'].get('subunits') == 'available' else None,
              'website': website.get('final_url') if isinstance(website, dict) else None,
              'website_origin': web_origin,
              'website_proof': web_proof,
              'social': sum(c['family'] == 'website' and 'social' in c['field'] for c in available),
              'jobs': sum(c['family'] == 'hiring' and not c.get('carried_forward') for c in available),
              'job_titles': job_titles[:3],
              'job_dates': job_dates,
              'job_postings': job_postings,
              'activity': sum(c['family'] == 'activity' for c in available) + len(reg_events),
              'latest_activity_date': latest_event[0] if latest_event else None,
              'latest_activity_label': latest_event[1] if latest_event else None,
              'sections': dict(row['run']['sections']),
              'claim_count': len(available), 'last_checked': row['run']['completed_at'], 'anchors': {}}
    mapping = {'name': 'identity.legal_name', 'municipality': 'identity.municipality', 'employees': 'identity.employees',
               'revenue': 'accounts.revenue', 'annual_result': 'accounts.net_result', 'website': 'official_website'}
    if founding_date and 'identity.founding_date' in fields: mapping['founding_date'] = anchor(fields['identity.founding_date'])
    elif founding_date and 'identity.registration_date' in fields: mapping['founding_date'] = anchor(fields['identity.registration_date'])
    for key, field in mapping.items():
        if field in fields and key not in result['anchors']: result['anchors'][key] = anchor(fields[field])
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
    body = f'<header><p class="eyebrow">Company research, with receipts</p><h1>{esc(title)}</h1><p id="cohort-summary">{esc(summary)}</p></header>'

    # View switcher tabs
    body += '<div class="view-switcher" role="tablist" aria-label="View selection">'
    body += '<button type="button" id="tab-dashboard" class="tab-btn active" role="tab" aria-selected="true" aria-controls="view-dashboard">📊 Dashboard</button>'
    body += '<button type="button" id="tab-directory" class="tab-btn" role="tab" aria-selected="false" aria-controls="view-directory">🏢 Company Directory</button>'
    body += '<button type="button" id="tab-hiring" class="tab-btn" role="tab" aria-selected="false" aria-controls="view-hiring">💼 Hiring Explorer</button>'
    body += '</div>'

    # 1. Dashboard View
    body += '<section id="view-dashboard" class="dashboard-view" role="tabpanel" aria-labelledby="tab-dashboard">'
    body += '<div class="scope-banner" id="dashboard-scope-banner">'
    body += f'<div class="scope-text-wrap"><span class="scope-tag">Cohort Scope</span> <span id="scope-text">Full evaluated cohort: {n} companies in Norwegian corporate dataset</span></div>'
    body += '<div class="export-bar" aria-label="Export cohort data"><span class="export-label">Export Cohort:</span> <button type="button" id="export-dashboard-csv" class="btn-export">Export CSV</button> <button type="button" id="export-dashboard-json" class="btn-export">Export JSON</button></div>'
    body += '<div id="filter-scope-warning" class="filter-warning" hidden>⚠️ Filters active: metrics reflect <strong id="filter-scope-count">0</strong> matching companies. <button type="button" class="btn-link" id="reset-dashboard-filters">Clear filters to view full dataset</button></div>'
    body += '</div>'

    # Summary KPI cards
    web_count = sum(r['flags']['website'] for r in records)
    job_count = sum(r['jobs'] for r in records)
    hiring_comp = sum(r['flags']['jobs'] for r in records)
    act_count = sum(r['flags']['activity'] for r in records)

    body += '<div class="dashboard-metrics-grid">'
    body += f'<div class="metric-card" id="dash-card-companies"><div class="metric-header"><span class="metric-title">Evaluated Companies</span><span class="chip available">100% Cohort</span></div><div class="metric-value" id="dash-total-companies">{n}</div><div class="metric-desc">Total corporate entities evaluated in dataset</div></div>'
    body += f'<div class="metric-card" id="dash-card-websites"><div class="metric-header"><span class="metric-title">Verified Websites</span><span class="chip available" id="dash-websites-pct">{web_count / n * 100 if n else 0:.1f}%</span></div><div class="metric-value" id="dash-total-websites">{web_count}</div><div class="metric-desc">Official company sites verified by identity rules</div></div>'
    body += f'<div class="metric-card" id="dash-card-hiring"><div class="metric-header"><span class="metric-title">Active Hiring</span><span class="chip available" id="dash-hiring-companies">{hiring_comp} companies</span></div><div class="metric-value" id="dash-total-jobs">{job_count}</div><div class="metric-desc">Active job postings recalled from NAV stream</div></div>'
    body += f'<div class="metric-card" id="dash-card-activity"><div class="metric-header"><span class="metric-title">Recent Public Activity</span><span class="chip available" id="dash-activity-pct">{act_count / n * 100 if n else 0:.1f}%</span></div><div class="metric-value" id="dash-total-activity">{act_count}</div><div class="metric-desc">Entities with official filings or activity within 2 years</div></div>'
    body += '</div>'

    # Analytics grid
    body += '<div class="dashboard-analytics-grid">'
    body += '<div class="analytics-card">'
    body += '<h3>Website Source Provenance</h3>'
    body += '<p class="card-subtitle">Verified domains broken down by corroboration provenance category</p>'
    body += '<div id="provenance-breakdown" class="provenance-breakdown"></div>'
    body += '<p class="card-footer-note">All websites corroborated under strict identity resolution (organisation number, registry declared, or identity signals).</p>'
    body += '</div>'

    body += '<div class="analytics-card">'
    body += '<h3>Hiring Activity Timeline</h3>'
    body += '<p class="card-subtitle">Active job advertisements by publication date from official NAV stream</p>'
    body += '<div id="hiring-timeline" class="hiring-timeline-chart"></div>'
    body += '<p class="card-footer-note">Based on active NAV postings. Unlisted entities have no active jobs in the evaluation scope, not zero employment.</p>'
    body += '</div>'
    body += '</div>'

    body += '<div class="analytics-card full-width">'
    body += '<h3>Recent Verified Company Activity</h3>'
    body += '<p class="card-subtitle">Official business filings, amendments, and verified events (most recent first)</p>'
    body += '<div id="recent-activity-list" class="recent-activity-list"></div>'
    body += '<p class="card-footer-note">Fetch failures and observation changes are excluded. Only verified registry events are shown.</p>'
    body += '</div>'
    body += '</section>'

    # 2. Company Directory View
    body += '<section id="view-directory" class="directory-view" role="tabpanel" aria-labelledby="tab-directory" hidden>'
    body += '<div id="directory"></div>'
    body += '<div class="export-bar" aria-label="Export directory data"><span class="export-label">Export Directory:</span> <button type="button" id="export-directory-csv" class="btn-export">Export CSV</button> <button type="button" id="export-directory-json" class="btn-export">Export JSON</button></div>'
    body += '<div class="saved-views-bar" aria-label="Saved views and watchlist"><span class="saved-views-label">Saved Views:</span><div id="saved-views-list" class="saved-views-list"></div><button type="button" id="save-current-view" class="btn-sm">💾 Save view</button><button type="button" id="clear-watchlist" class="btn-sm">Clear watchlist</button><span class="storage-notice muted">Stored locally in your browser.</span></div>'
    body += '<div class="search-box">'
    body += '<label for="search" class="visually-hidden">Search name, organisation number, or website</label>'
    body += '<div class="search-input-wrapper">'
    body += '<span class="search-icon" aria-hidden="true">🔍</span>'
    body += '<input id="search" type="search" autocomplete="off" placeholder="Search by company name, orgnr, website, municipality..." aria-autocomplete="list" aria-controls="search-autocomplete">'
    body += '<div id="search-autocomplete" class="autocomplete-dropdown" role="listbox" aria-label="Company suggestions" hidden></div>'
    body += '</div></div>'

    body += '<section class="filters" aria-label="Company filters">'
    values_muni = sorted({str(r['municipality']) for r in records if r['municipality']})
    body += '<label>Municipality<select id="municipality"><option value="">All municipalities</option>' + ''.join(f'<option value="{esc(v)}">{esc(v)}</option>' for v in values_muni) + '<option value="Unknown">Unknown municipality</option></select></label>'

    values_div = sorted({r['nace'][:2] for r in records if r['nace']})
    body += '<label>Industry (NACE)<select id="division"><option value="">All industries</option>' + ''.join(f'<option value="{esc(v)}">Division {esc(v)}</option>' for v in values_div) + '<option value="Unknown">Unknown industry</option></select></label>'

    body += '<label>Company size<select id="size-band"><option value="">All sizes</option>'
    body += '<option value="micro">Micro (1–9 employees)</option>'
    body += '<option value="small">Small (10–49 employees)</option>'
    body += '<option value="medium">Medium (50–249 employees)</option>'
    body += '<option value="large">Large (250+ employees)</option>'
    body += '<option value="zero">Zero (0 employees)</option>'
    body += '<option value="unknown">Unknown / Unreported</option>'
    body += '</select></label>'

    body += '<label>Sort<select id="sort"><option value="claim_count">By claims</option><option value="name">A–Z</option><option value="score">By score</option><option value="revenue">Revenue</option><option value="employees">Employees</option></select></label>'

    for key, label in [('website', 'Verified website'), ('jobs', 'Job ads'), ('social', 'Social profiles'), ('activity', 'Public activity'), ('incomplete', 'Failed or blocked sections')]:
        body += f'<label class="check"><input id="filter-{key}" type="checkbox">{label}</label>'
    body += '<label class="check"><input id="filter-watchlist" type="checkbox">⭐ Watchlist (<span id="watchlist-count">0</span>)</label>'
    body += '</section>'

    body += '<div id="active-filters-bar" class="active-filters-bar" hidden>'
    body += '<span class="filter-chips-label">Active filters:</span>'
    body += '<div id="active-filter-chips" class="active-filter-chips"></div>'
    body += '<button type="button" id="clear-filters" class="btn-clear-filters">Clear all filters</button>'
    body += '</div>'

    body += '<p id="result-count" role="status" aria-live="polite" class="result-count"></p>'

    body += '<div id="empty-results" class="empty-state" hidden>'
    body += '<h3>No companies match your search and filters</h3>'
    body += '<p>Try adjusting your search terms, searching for a 9-digit organisation number, or clearing active filters.</p>'
    body += '<button type="button" id="reset-empty-filters" class="btn-primary">Clear all filters</button>'
    body += '</div>'

    body += '<div id="results" class="results">'
    for r in records:
        body += f'<article class="company"><h2><a href="c/{esc(r["orgnr"])}.html">{esc(r["name"])}</a></h2><p>{esc(r["orgnr"])} · {esc(r["municipality"] or "Unknown municipality")}</p></article>'
    body += '</div><div class="pagination"><button id="previous" type="button">Previous</button><span id="page-label"></span><button id="next" type="button">Next</button></div>'
    body += '</section>'

    # 3. Hiring Explorer View
    body += '<section id="view-hiring" class="hiring-view" role="tabpanel" aria-labelledby="tab-hiring" hidden>'
    body += '<div class="hiring-header">'
    body += '<h2>Hiring Explorer</h2>'
    body += '<p class="muted">Active job postings recalled from Arbeidsplassen (NAV) public stream with verified company matching.</p>'
    body += '<div class="hiring-scope-box"><p><strong>Recalled job postings:</strong> Evaluated from NAV public stream. Unlisted companies have no active job postings recalled within this scope, which does not imply zero employment.</p></div>'
    body += '</div>'
    body += '<div class="hiring-filters-grid">'
    body += '<label>Job title keyword<input type="search" id="hiring-search-title" placeholder="Search job title (e.g. Utvikler, Konsulent)..." autocomplete="off"></label>'
    body += '<label>Company<input type="search" id="hiring-search-company" placeholder="Search company name or orgnr..." autocomplete="off"></label>'
    body += '<label>Published within<select id="hiring-filter-date"><option value="all">All publication dates</option><option value="7">Last 7 days</option><option value="30">Last 30 days</option><option value="90">Last 90 days</option></select></label>'
    body += '</div>'
    body += '<p id="hiring-count" class="result-count" role="status" aria-live="polite"></p>'
    body += '<div id="hiring-results" class="hiring-results"></div>'
    body += '<div id="hiring-empty" class="empty-state" hidden>'
    body += '<h3>No job postings match active filters</h3>'
    body += '<p>Zero results indicates no active job ads match your criteria in the evaluated cohort. This does not indicate zero employment.</p>'
    body += '</div>'
    body += '</section>'
    return page(title, body, kind='index')


def compare_page(title):
    body = '<header><p class="eyebrow">Side by side</p><h1>Compare companies</h1><p>Select up to three companies for side-by-side comparison across verified facts, scale, financials, and online presence.</p></header>'
    body += '<section class="filters compare-inputs-grid" aria-label="Company selectors">'
    for i in range(3):
        body += f'<label>Company {i + 1}<input type="search" id="company-{i}" list="company-options" autocomplete="off" placeholder="Enter company name or orgnr..."></label>'
    body += '<div class="compare-actions"><button type="button" id="clear-compare" class="btn-clear-filters">Clear all</button></div>'
    body += '</section><datalist id="company-options"></datalist>'
    body += '<p id="compare-status" role="status" class="compare-status"></p>'
    body += '<div id="comparison" class="comparison"></div>'
    return page('Compare · ' + title, body, kind='compare')


def generate_site(input_path, out, title='Signalpost'):
    input_path, out = Path(input_path), Path(out)
    if input_path.resolve().is_relative_to(out.resolve()):
        raise ValueError('Site directory must not contain its source envelopes')
    input_rows = [normalize(json.loads(line)) for line in input_path.read_text(encoding='utf-8-sig').split('\n') if line.strip()]
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
