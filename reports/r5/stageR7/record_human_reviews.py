"""Record the reviewer's supplied R7 human verdicts, preserving automated verdicts.

Verdicts and basis text are the reviewer's own independent web hand-check,
supplied in conversation; this script does not fetch anything.  Each review is
pinned to the exact R7 sample, organisation, field and value SHA-256 of the
saved claim in R7/identity_items.json.
"""
from signalpost.portable_paths import portable  # saved paths stay repo-relative
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEST = Path(__file__).resolve().parent
REVIEWER = 'Nethra Venkat'
DATE = '2026-11-15'
METHOD = 'Human hand-check with independent web verification, supplied explicitly in conversation.'
# Exact reviewer table (URL as written by the reviewer; basis verbatim).
SUPPLIED = [
    ('997995414', 'PEAK LANDSCAPES AS', 'website', 'https://www.peaklandscapes.no/',
     'Exact legal name "Peak Landscapes AS" + exact register address "Alunsjøveien 65, 0957 Oslo" in footer; '
     'site links instagram.com/peak_landscapes_as/. No org nr on site. "© 2025 by SGNXT" is the web designer '
     'credit, not the owner.'),
    ('995135086', 'CRAFTING HOUSE AS', 'website', 'https://craftinghouse.no/',
     '"Orgnr 995 135 086 MVA" on contact page; matches registry-declared homepage. Site address omits "A" '
     '(register: Biskop Gunnerus\' gate 14A) — minor, not a conflict.'),
    ('983089887', 'MELDAL MILJØANLEGG AS', 'website', 'https://www.meldalmiljoanlegg.no/',
     '"Orgnummer: 983 089 887" on site. Footer "© 2035 by Happy Farm Sanctuary" is leftover template text, '
     'not a different owner. Contact john.horg@meldalmiljoanlegg.no / 92647341 independently tied to '
     '983089887 in a Doffin procurement notice.'),
    ('997995414', 'PEAK LANDSCAPES AS', 'social', 'instagram.com/peak_landscapes_as/',
     'Instagram peak_landscapes_as confirmed human-CORRECT: linked from the company\'s own site.'),
]
REGISTRY_FIELDS = ('column:navn', 'column:hjemmeside', 'columns:forretningsadresse.*', 'columns:postadresse.*')


def value_sha256(value):
    # Same canonical form as scripts/precision_ledger.py.
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def norm(url):
    url = url.lower().rstrip('/')
    for prefix in ('https://', 'http://', 'www.'):
        url = url.removeprefix(prefix)
    return url


def saved_url(item):
    v = item['value']
    return v.get('final_url') or v.get('url')


def main():
    data = json.loads((DEST / 'R7/identity_items.json').read_text(encoding='utf8'))
    reviews = []
    for org, company, kind, url, basis in SUPPLIED:
        matches = [i for i in data['items'] if i['orgnr'] == org and i['kind'] == kind and norm(saved_url(i)) == norm(url)]
        assert len(matches) == 1, (org, kind, url, len(matches))
        item = matches[0]
        own = [e for e in item['evidence'] if e['source_class'] == 'company_owned'
               and (e['locator'].startswith(('identity-proof:', 'company-link:', 'publisher')) or kind == 'website')]
        registry = [e for e in item['evidence'] if e['source_class'] == 'official_registry'
                    and e['locator'].endswith(REGISTRY_FIELDS)]
        assert own, (org, kind)
        reviews.append({
            'organisation_number': org, 'company': company, 'kind': kind, 'url': url,
            'saved_value_url': saved_url(item), 'field': item['field'],
            'sample': f"seed{item['seed']}", 'stage': 'R7', 'change': item['change'],
            'value_sha256': value_sha256(item['value']),
            'verdict': 'correct', 'reviewer': REVIEWER, 'review_date': DATE, 'method': METHOD, 'basis': basis,
            'automated_verdict': item['review']['verdict'],
            'automated_checks': item['review']['checks'],
            'proof_tier': item['value'].get('proof_type') or item['value'].get('proof_tier'),
            'identity_level': item['value'].get('identity_level'),
            'receipts': own, 'registry_receipts': registry})
    assert sum(r['kind'] == 'website' for r in reviews) == 3 and sum(r['kind'] == 'social' for r in reviews) == 1
    result = {
        'reviewer': REVIEWER, 'review_date': DATE, 'stage': 'R7', 'reviews': reviews,
        'counts': {'website': {'human_verified_correct': 3, 'wrong': 0}, 'social': {'human_verified_correct': 1, 'wrong': 0}},
        'totals': {'human_verified_correct': 4, 'wrong': 0,
                   'previous_recorded_human_verified_correct': 24, 'cumulative_human_verified_correct': 28},
        'counting_method': 'Distinct organisation/type/URL. None of these four items appears in earlier human reviews '
                           '(stageR3/human_reviews.json, precision/human_reviews.json), so the recorded cumulative '
                           'human-verified count rises 24 -> 28. The earlier items-checked union is not recomputed here.',
        'input': 'reports/r5/stageR7/R7/identity_items.json',
        'limits': 'Human verification is the reviewer\'s supplied independent web hand-check, not an assistant '
                  're-fetch or a population precision estimate. Automated verdicts, proof tiers and published '
                  'outputs are unchanged. CRAFTING HOUSE was published under registry_declared_live (R7a); the '
                  'reviewer\'s contact-page orgnr basis is recorded as human context, not as a change of tier. '
                  'Verdicts are scoped to these exact sample/value hashes and transfer to no other domain or profile.'}
    (DEST / 'human_reviews.json').write_text(json.dumps(portable(result), ensure_ascii=False, indent=2) + '\n',
                                            encoding='utf8', newline='\n')
    print(json.dumps({'reviews': len(reviews), 'receipts': [len(r['receipts']) for r in reviews],
                      'registry_receipts': [len(r['registry_receipts']) for r in reviews],
                      'value_sha256': [r['value_sha256'][:12] for r in reviews]}))


if __name__ == '__main__':
    main()
