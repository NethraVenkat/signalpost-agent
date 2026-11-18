"""Record the supplied L/X2 hand-check and update the cumulative human ledger."""

from collections import Counter
from pathlib import Path

from record_human_reviews import DATE, DEST, METHOD, REVIEWER, ROOT, read, save, sha256, value_sha256
from signalpost.portable_paths import expand, portable_text

REPORTS = DEST.parent
STAGES = {'L': 'stageL/L', 'X2': 'stageX/X2'}
ORKDAL_PROFILE = 'https://www.facebook.com/pages/Orkdal-Blomster/119910848049561'
ORKDAL_REVIEW_URL = 'https://www.facebook.com/orkdalblomster'
SUPPLIED = (
    ('L', 20261117, '934608143', 'website', 'https://www.maritim.no',
     'Purchase terms name Norway Marine Supply AS as seller and list organisation number 934 608 143 and '
     'Åsbieveien 11, 4848 Arendal. The register lists www.maritim.no.'),
    ('X2', 20261017, '926818317', 'social', 'https://www.facebook.com/spedify.no',
     'The company footer lists Spedify AS, Sagveien 25, 1814 Askim and organisation number 926 818 317 '
     'next to the “Følg oss” link. The reviewer observed that the profile links back to spedify.no.'),
    ('X2', 20261115, '982326125', 'website', 'https://www.orkdalblomster.no',
     'The footer lists organisation number 982 326 125, phone 72 48 10 20 and Orkdalsveien 42, Orkanger.'),
    ('X2', 20261115, '982326125', 'social', ORKDAL_PROFILE,
     'The reviewer confirmed the short Facebook URL and reported that the profile links back to the company site. '
     'The archived footer links the numeric Facebook page.'),
    ('X2', 20261117, '926148931', 'website', 'https://atlo.no',
     'The site lists Atlo AS, organisation number 926 148 931 and Strandgaten 6, 5013 Bergen.'),
)

HISTORICAL = ('precision/ledger.json', 'stageH/precision/ledger.json')
REVIEW_LEDGERS = ('stageR3/human_reviews.json', 'stageR7/human_reviews.json',
                  'stageHC1/human_reviews.json', 'stageHC1/website_human_reviews.json')


def archived_reviews():
    inputs, reviews = {}, []
    for stage, seed, org, kind, url, note in SUPPLIED:
        folder = REPORTS / STAGES[stage]
        inventory = folder / 'identity_items.json'
        sample = f'{stage}/seed{seed}'
        settings_path = folder / f'seed{seed}/settings.json'
        counts_path = settings_path.with_name('counts.json')
        settings, counts = read(settings_path), read(counts_path)
        assert (settings['stage'], settings['seed']) == (stage, seed)
        args = settings['command_argv']
        organisations = Path(expand(args[args.index('--organisations') + 1]))
        assert sha256(organisations) == settings['input_sha256']
        pins = {
            'seed': seed, 'input_sha256': settings['input_sha256'],
            'envelopes_sha256': counts['envelopes_sha256'],
            'identity_inventory': inventory.relative_to(ROOT).as_posix(), 'identity_inventory_sha256': sha256(inventory),
            'settings': settings_path.relative_to(ROOT).as_posix(), 'settings_sha256': sha256(settings_path),
            'counts': counts_path.relative_to(ROOT).as_posix(), 'counts_sha256': sha256(counts_path),
        }
        inputs[sample] = pins
        item, = (i for i in read(inventory)['items'] if (i['seed'], i['orgnr'], i['kind'], i['identity'], i['change'])
                 == (seed, org, kind, url, 'added'))
        value = item['value']
        assert (value['final_url'] if kind == 'website' else value['url']) == url
        own = [e for e in item['evidence'] if e['source_class'] == 'company_owned']
        registry = [e for e in item['evidence'] if e['source_class'] == 'official_registry']
        locator = f'identity-proof:{org}' if kind == 'website' else f'company-link:{url}'
        assert any(e['locator'] == locator and 0 < len(e['claim_span']) <= 300 for e in own)
        pin = {
            'url': url, 'sample': sample, 'seed': seed, 'sample_sha256': pins['input_sha256'],
            'envelopes_sha256': pins['envelopes_sha256'], 'field': item['field'],
            'value_sha256': value_sha256(value), 'proof_tier': value.get('proof_type') or value['proof_tier'],
            'automated_verdict': item['review']['verdict'], 'receipts': own, 'registry_receipts': registry,
        }
        review = {
            'organisation_number': org, 'company': item['legal_name'], 'kind': kind,
            'verdict': 'correct', 'reviewer': REVIEWER, 'review_date': DATE, 'method': METHOD, 'note': note,
        }
        if url == ORKDAL_PROFILE:
            review.update(url=ORKDAL_REVIEW_URL, exact_saved_claim=False, related_saved_claim=pin,
                          attribution_source='https://www.orkdalblomster.no/',
                          url_match_note='The company homepage links the numeric page. Equivalence to the short URL is unresolved.')
        else:
            review.update(pin, exact_saved_claim=True)
        reviews.append(review)
    return inputs, reviews


def cumulative(additions):
    verdicts = {}

    def record(org, kind, value, verdict, exact=True):
        key = org, kind, value
        previous = verdicts.get(key)
        assert previous is None or previous[0] == verdict, key
        verdicts[key] = verdict, exact or (previous is not None and previous[1])

    for name in HISTORICAL:
        for item in read(REPORTS / name)['items']:
            if human := item.get('human_review'):
                value, kind = item['value'], item['kind']
                identifiers = {'website': 'final_url', 'social': 'url', 'LEI': 'lei', 'job': 'uuid'}
                assert value_sha256(value) == human['value_sha256']
                record(item['organisation_number'], kind, value[identifiers[kind]], human['verdict'])
    for reviews in [*(read(REPORTS / name)['reviews'] for name in REVIEW_LEDGERS), additions]:
        for review in reviews:
            record(review['organisation_number'], review['kind'], review.get('saved_value_url', review['url']),
                   review['verdict'], review.get('exact_saved_claim', True))

    types = ('website', 'social', 'job', 'LEI')
    outcomes = ('correct', 'wrong', 'unsure')
    counts = {}
    for kind in types:
        seen = Counter(outcome for (_, typ, _), (outcome, _) in verdicts.items() if typ == kind)
        counts[kind] = {key: seen[key] for key in outcomes}
    totals = {key: sum(row[key] for row in counts.values()) for key in outcomes}
    exact = Counter(outcome for outcome, scoped in verdicts.values() if scoped)
    return {'by_kind': counts, 'totals': totals, 'exact_saved_items': {key: exact[key] for key in outcomes}}


def replace_section(path, heading, following, content):
    text = path.read_text(encoding='utf8')
    earlier, marker, later = text.partition(heading)
    if marker:
        text = earlier
        if following:
            _, separator, rest = later.partition(following)
            assert separator
            text += separator + rest
    if following:
        assert following in text
        text = text.replace(following, content + '\n\n' + following, 1)
    else:
        text = text.rstrip() + '\n\n' + content + '\n'
    path.write_text(portable_text(text), encoding='utf8', newline='\n')


def main():
    inputs, reviews = archived_reviews()
    counts = cumulative(reviews)
    totals = counts['totals']
    exact = counts['exact_saved_items']
    save(DEST / 'l_x2_human_reviews.json', {
        'reviewer': REVIEWER, 'review_date': DATE, 'method': METHOD, 'inputs': inputs, 'reviews': reviews,
        'review_counts': {'correct': len(reviews), 'exact_saved_claims': sum(r['exact_saved_claim'] for r in reviews)},
        'cumulative': counts, 'prior_ledgers': [f'reports/r5/{name}' for name in (*HISTORICAL, *REVIEW_LEDGERS)],
    })

    heading = '## Cumulative human verdicts through HC1 L/X2'
    scope = ('The L/X2 hand-check was supplied by Nethra Venkat on 2026-11-18. The cumulative counts cover '
             'human-reviewed items from T, H, R5/R3, R7, P2/P3g and L/X2, deduplicated by organisation and '
             'exact URL, LEI or job UUID.')
    lines = [heading, '', scope, '', '| Type | Correct | Wrong | Unsure |', '|---|---:|---:|---:|']
    for kind, row in counts['by_kind'].items():
        lines.append(f"| {kind} | {row['correct']} | {row['wrong']} | {row['unsure']} |")
    lines += [f"| **Total** | **{totals['correct']}** | **{totals['wrong']}** | **{totals['unsure']}** |", '',
              f"Of the {sum(totals.values())} distinct human verdicts, {sum(exact.values())} match exact saved items, "
              f"including {exact['correct']} correct. Orkdal’s own footer links the archived numeric Facebook page. "
              'The reviewer’s short Facebook URL has its own verdict, with the numeric claim pinned as related evidence. '
              '[Orkdal Blomster homepage](https://www.orkdalblomster.no/)', '',
              '| Organisation | Type | Reviewed URL | Verdict |', '|---|---|---|---|']
    for review in reviews:
        lines.append(f"| {review['organisation_number']} {review['company']} | {review['kind']} | `{review['url']}` | Correct |")
    lines += ['', 'The L/X2 pins use the committed identity inventories, sample settings, and envelope hashes '
              'from the recorded counts. [L/X2 verdicts and receipts](../stageHC1/l_x2_human_reviews.json)']
    replace_section(REPORTS / 'stageR3/LEDGER.md', heading, '', '\n'.join(lines))

    heading = '### Cumulative human precision through L/X2'
    readme = (f"{heading}\n\nNethra Venkat’s 2026-11-18 L/X2 hand-check adds five correct verdicts. The cumulative "
              f"ledger contains **{sum(totals.values())} distinct human-reviewed items** with **{totals['correct']} correct**, "
              f"**{totals['wrong']} wrong**, and **{totals['unsure']} unsure**. "
              f"**{exact['correct']} correct** verdicts match exact saved items. Orkdal’s reviewed short Facebook URL "
              'is recorded with a reference to the separately pinned numeric claim. '
              '[Cumulative human ledger](reports/r5/stageR3/LEDGER.md#cumulative-human-verdicts-through-hc1-lx2) · '
              '[L/X2 verdicts and receipts](reports/r5/stageHC1/l_x2_human_reviews.json)')
    replace_section(ROOT / 'README.md', heading, '### Historical scale measurements', readme)


if __name__ == '__main__':
    main()
