"""Recent official dates, derived only from evidence-backed identity claims."""
from datetime import date

LABELS = {'identity.registration_date': 'Registered in Enhetsregisteret',
          'identity.founding_date': 'Founded', 'identity.vat_registration_date': 'Registered for VAT',
          'identity.deleted': 'Deletion recorded'}


def recent(envelope):
    try:
        checked = date.fromisoformat(envelope.run.completed_at[:10])
        try: cutoff = checked.replace(year=checked.year-2)
        except ValueError: cutoff = checked.replace(year=checked.year-2, day=28)
    except (ValueError, AttributeError):
        return []
    evidence = {e.id: e for e in envelope.evidence}
    events = []
    for claim in envelope.claims:
        if claim.field not in LABELS or claim.availability != 'available' or not claim.evidence_ids or claim.carried_forward: continue
        value = claim.value if isinstance(claim.value, str) else next((evidence[eid].effective_at for eid in claim.evidence_ids if evidence[eid].effective_at), None)
        try: day = date.fromisoformat(str(value)[:10])
        except ValueError: continue
        if cutoff <= day <= checked:
            events.append((day.isoformat(), LABELS[claim.field], claim))
    return sorted(events, key=lambda item: (item[0], item[1]), reverse=True)
