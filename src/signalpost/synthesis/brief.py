"""Select a small, cited overview from already validated template sentences."""


def select(synthesis, claims, limit=8):
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
