"""Select a small, cited overview from already validated template sentences."""

LIMITATION = 'Only one reported fiscal period is supported here; financial direction is not established.'
EMPLOYEE_GAP = 'The registry does not report an employee count.'
DEPTH_LABELS = {
    'identity.institutional_sector': 'Registered institutional sector',
    'identity.registered_in_vat': 'VAT registration flag as reported',
    'identity.foreign_register_name': 'Foreign registration authority as reported',
    'identity.home_country_registration_number': 'Home-country registration number as reported',
    'identity.legislation_country': 'Country of applicable legislation as reported',
}


def depth_text(claim):
    """Exact, field-bound frames; never interpret these as ownership proof."""
    if claim.field == 'identity.employees_reported' and claim.value is False and not claim.carried_forward:
        return EMPLOYEE_GAP
    label = DEPTH_LABELS.get(claim.field)
    if label is None or claim.carried_forward: return None
    value = claim.value
    if claim.field == 'identity.institutional_sector':
        if not isinstance(value, dict) or not value.get('kode') or not value.get('beskrivelse'): return None
        value = str(value['kode']) + ': ' + str(value['beskrivelse'])
    elif claim.field == 'identity.registered_in_vat':
        if type(value) is not bool: return None
        value = 'true' if value else 'false'
    elif not isinstance(value, str) or not value: return None
    return label + ': ' + value + '.'


def period_claims(envelope):
    claims = [c for c in envelope.claims if c.family == 'accounts' and c.availability == 'available']
    if not claims or any(c.carried_forward or not c.reporting_period or not c.reporting_period.get('period_end') for c in claims): return []
    periods = {(c.reporting_period.get('period_start'), c.reporting_period['period_end']) for c in claims}
    return sorted(claims, key=lambda c: c.id) if len(periods) == 1 else []


def build(synthesis, claims, limit=6):
    """Cover activity, scale, leadership, dated events and evidenced limitations.

    Four to six sentences when supported. Sparse companies are never padded.
    This operates on the validated full sentence catalog, not source text.
    """
    sections = synthesis.get('sections', {})
    available = {c['id']: c for c in claims if c['availability'] == 'available'}
    candidates = [s for key in ('what_it_does','scale','leadership','changes') for s in sections.get(key, [])
                  if s.get('claim_ids') and all(cid in available for cid in s['claim_ids'])]
    def fields(sentence): return [available[cid]['field'] for cid in sentence['claim_ids']]
    def matches(sentence, prefixes): return any(f.startswith(prefixes) for f in fields(sentence))
    choices = []
    predicates = [
        lambda s: matches(s, ('identity.registered_activity','identity.statutory_purpose','website_description.')),
        lambda s: (any(f in {'accounts.revenue','identity.employees'} or f.startswith('subunits.unit.') for f in fields(s))
                   and s['text'] != LIMITATION),
        lambda s: s in sections.get('leadership', []),
        lambda s: matches(s, ('registry_change.','dated_item.')),
        lambda s: s['text'] in {LIMITATION, EMPLOYEE_GAP},
        lambda s: matches(s, tuple(DEPTH_LABELS)),
    ]
    for predicate in predicates:
        item = next((s for s in candidates if s not in choices and predicate(s)), None)
        if item: choices.append(item)
    # Companies lacking descriptions/financials still receive supported registry
    # context; do not claim a missing category was checked or infer a value.
    choices.extend(s for s in candidates if s not in choices)
    unique = []
    for item in choices:
        if not any(s['text'] == item['text'] for s in unique): unique.append(item)
    return unique[:min(limit, 6)]


def select(synthesis, claims, limit=8):
    if synthesis.get('briefing'):
        allowed = {c['id'] for c in claims if c['availability'] == 'available'}
        return [s for s in synthesis['briefing'] if s.get('claim_ids') and all(cid in allowed for cid in s['claim_ids'])][:min(limit, 6)]
    sections = synthesis.get('sections', {})
    sentences = [s for key in ('what_it_does', 'scale', 'leadership', 'changes')
                 for s in sections.get(key, [])]
    permitted = {c['id']: c for c in claims if c['availability'] == 'available'}
    permitted.update({c['id']: c for c in synthesis.get('change_claims', [])})
    supported = [s for s in sentences if s.get('claim_ids') and all(cid in permitted for cid in s['claim_ids'])]

    def matches(sentence, prefixes):
        return any(permitted[cid]['field'].startswith(prefixes) for cid in sentence['claim_ids'])

    choices = []
    predicates = [
        lambda s: s in sections.get('what_it_does', []),
        lambda s: s in sections.get('leadership', []),
        lambda s: matches(s, ('identity.municipality', 'identity.registered_address', 'subunits.unit.')),
        lambda s: matches(s, ('accounts.',)),
        lambda s: matches(s, ('hiring.job.',)),
        lambda s: matches(s, ('registry_change.', 'dated_item.')),
        lambda s: s in sections.get('changes', []) and not matches(s, ('registry_change.', 'dated_item.')),
        lambda s: matches(s, ('website_description.',)),
    ]
    for predicate in predicates:
        sentence = next((s for s in supported if s not in choices and predicate(s)), None)
        if sentence:
            choices.append(sentence)
    choices.extend(s for s in supported if s not in choices)
    return choices[:limit]
