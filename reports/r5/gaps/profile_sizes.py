"""Reconstruct HTML sizes from saved envelopes without publishing a site or HTTP."""
import argparse
from collections import Counter
import json
from pathlib import Path

from signalpost import site


def saved_rows(path):
    with path.open(encoding='utf8') as stream:
        for line in stream:
            if line.strip():
                yield site.normalize(json.loads(line))


def measure(path):
    sizes = {}
    oversized = []
    for row in saved_rows(path):
        visible, inline = site.EXPLORER_VISIBLE_ROWS, site.OFFICIAL_INLINE
        rendered = site.profile(row, 'Signalpost', visible)
        while len(rendered.encode('utf8')) >= site.PROFILE_HTML_LIMIT and visible:
            visible //= 2
            rendered = site.profile(row, 'Signalpost', visible)
        while len(rendered.encode('utf8')) >= site.PROFILE_HTML_LIMIT and inline:
            inline //= 2
            rendered = site.profile(row, 'Signalpost', visible, official_inline=inline)
        if len(rendered.encode('utf8')) >= site.PROFILE_HTML_LIMIT:
            rendered = site.profile(row, 'Signalpost', visible, official_inline=inline, source_shortcuts=False)
        size = len(rendered.encode('utf8'))
        org = row['organisation_number']
        sizes[org] = size
        if size >= site.PROFILE_HTML_LIMIT:
            available = [c for c in row['claims'] if c['availability'] == 'available']
            oversized.append({'organisation_number': org, 'bytes': size,
                'available_by_family': dict(Counter(c['family'] for c in available)),
                'registered_workplace_claims': sum(c['field'].startswith('subunits.unit.') for c in available),
                'consolidated_claims': sum(c['field'].startswith('accounts.consolidated.') for c in available),
                'state_aid_claims': sum(c['field'].startswith('state_aid.award.') for c in available),
                'visible_explorer_rows': visible, 'inline_official_facts': inline})
    return {'kind': 'Offline reconstruction using the measured checkout renderer; no pages published and no live run',
            'profile_limit_bytes': site.PROFILE_HTML_LIMIT, 'largest_rendered_profile_bytes': max(sizes.values()),
            'companies': len(sizes), 'oversized': oversized, 'profile_bytes': sizes}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--envelopes', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    def no_network(event, values):
        if event in {'socket.connect', 'socket.getaddrinfo', 'socket.gethostbyname', 'socket.sendto'}:
            raise RuntimeError('Saved-profile size diagnosis must not access network')
    import sys
    sys.addaudithook(no_network)
    result = measure(args.envelopes)
    args.out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'profile_bytes'}))
