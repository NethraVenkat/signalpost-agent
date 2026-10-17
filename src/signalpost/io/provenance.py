"""Registry attribution outside envelopes, preserving the existing claim contract.

Only a successful current-run request for the exact evidence URL and hash can
authorize live_verified. Injected clients (including offline replay) are never
described as live verification. Historical evidence retains its own attribution.
"""
from collections import Counter
from urllib.parse import urlsplit


def registry_provenance(envelopes, events, *, injected_client=False):
    successful = {(e['url'], e.get('content_sha256')) for e in events if e.get('status') == 200}
    claims = []
    counts = Counter()
    for envelope in {e.organisation_number: e for e in envelopes}.values():
        evidence = {e.id: e for e in envelope.evidence}
        for claim in envelope.claims:
            if claim.family not in {'identity', 'roles', 'subunits', 'accounts'}:
                continue
            sources = []
            for evidence_id in claim.evidence_ids:
                item = evidence.get(evidence_id)
                if item is None:
                    sources.append('unknown')
                elif urlsplit(item.source_url).path.endswith('/lastned/csv'):
                    sources.append('csv_cache')
                elif claim.carried_forward:
                    sources.append('historical_api')
                elif (item.source_url, item.content_sha256) in successful:
                    sources.append('api_checked' if injected_client else 'live_verified')
                else:
                    sources.append('unverified')
            source_types = sorted(set(sources)) or ['not_available']
            counts.update(source_types)
            claims.append({'organisation_number': envelope.organisation_number,
                           'claim_id': claim.id, 'field': claim.field,
                           'availability': claim.availability,
                           'source_types': source_types,
                           'evidence_ids': claim.evidence_ids})
    requests = Counter()
    for event in events:
        parsed = urlsplit(event['url'])
        if parsed.hostname != 'data.brreg.no':
            continue
        path = parsed.path
        if path.endswith('/roller'):
            requests['roles'] += 1
        elif path == '/enhetsregisteret/api/underenheter':
            requests['subunits'] += 1
        elif path.startswith('/enhetsregisteret/api/enheter/'):
            requests['identity'] += 1
        elif path.startswith('/regnskapsregisteret/'):
            requests['accounts'] += 1
    return {'scope': 'registry_claims_only',
            'transport': 'injected_client' if injected_client else 'live',
            'counts_by_source_type': dict(counts), 'requests_by_family': dict(requests),
            'claims': claims}
