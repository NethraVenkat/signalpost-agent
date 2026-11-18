"""Pin the supplied website hand-checks and replay HC1c on the saved P2/P3g runs."""

import hashlib
import json
import re
from collections import Counter, defaultdict
from functools import lru_cache
from urllib.parse import urlsplit

from record_human_reviews import DATE, DEST, METHOD, REVIEWER, read, samples, save, sha256, value_sha256
from replay_social import reconstruct_pages
from scripts.verify_owner_social import verified_former_names
from scripts.verify_publisher_identity import registry_context
from signalpost.portable_paths import portable_text
from signalpost.sources.text import decode_body
from signalpost.web.challenge import detected as access_gate
from signalpost.web.html import Page
from signalpost.web.owner_social import group_site_receipt, website_scope
from signalpost.web.policy import domain


CORRECT = {
    ('816235502', 'industristal.no'), ('818003072', 'molliesafe.no'), ('911719266', 'restaurantdrift.no'),
    ('916094051', 'bjornsbil.no'), ('918811370', 'totenforsikring.no'), ('922569738', 'snuom.no'),
    ('925193313', 'undervisningsmateriell.no'), ('929455606', 'industriplast.no'), ('989952625', 'varmepumpeservice.no'),
    ('991380523', 'kvernodden.no'), ('992912952', 'dovrehandverk.no'), ('996441083', 'seaservices.no'),
    ('833242482', 'soliauto.no'), ('926765655', 'listerlaserklinikk.no'), ('966261218', 'bomlo.fhs.no'),
    ('970991786', 'agrando.no'), ('986902651', 'tinnheiabil.no'), ('988911879', 'elvegata16.no'),
    ('990825076', 'peculium.no'), ('998407257', 'gravitonia.com'),
}
SHARED = {
    ('930595764', 'westnesholding.no'): 'The footer contains the organisation’s own number. The site also presents subsidiaries.',
    ('991323848', 'trollheim.no'): 'The privacy PDF states “Vårt org. nr. er 991 323 848”. The site also presents subsidiary 924191627.',
    ('954583996', 'whalesafari.no'): 'The footer names “Whale2Sea AS / Hvalsafari AS”. Both companies are joint data controllers.',
}
UNSURE = {('825179062', 'ftfconsulting.no'), ('956510651', 'kirkengeiendom.no')}
NOTES = {
    '818003072': 'Molliesafe AS is a registered operating unit of Innosafe AS. The registry lists the domain.',
    '916094051': 'The organisation number is on the contact page.',
    '966261218': 'The school has a dedicated subdomain on fhs.no, which is reserved for folk high schools.',
    '996441083': 'The site shows “©2022 by Kvitsøy Sjøtjenester AS”.',
}


def archived_pages(row, events, site, evidence, load):
    pages, _ = reconstruct_pages(row, events, site, evidence, load)
    root = domain(site['final_url'])
    for event in events:
        url, sha = event['url'], event.get('content_sha256')
        if (event.get('section') != 'website' or event['status'] != 200 or event.get('error')
                or event.get('truncated') or not sha or (url, sha) in pages or domain(url) != root
                or urlsplit(url).path == '/robots.txt'):
            continue
        raw = load(sha)
        header = raw[:2048].lstrip(b'\xef\xbb\xbf \t\r\n').lower()
        if (header.startswith(b'%pdf-') or header.startswith(b'<?xml') and b'<html' not in header
                or re.match(rb'<(?:urlset|sitemapindex|rss|feed)\b', header)):
            continue  # HTML and plaintext are scope material. PDF proof and XML nominations have separate rules.
        page = Page(raw, url)
        if not access_gate(page):
            pages[url, sha] = page
    return pages


def write_report(items, counts):
    lines = [
        '# HC1c saved website replay', '',
        'The replay rechecks already-published websites against their saved own-page bytes and recorded registry identity. '
        'A group label records another registered entity on a fetched page. The published website URL, availability and proof tier are preserved.', '',
        '| Sample | Published websites | Retained | Newly labelled `group_site` |',
        '|---|---:|---:|---:|',
    ]
    for sample, report in counts.items():
        lines.append(f"| {sample} | {report['published']} | {report['retained']} | {report['relabelled']} |")
    lines += ['', '| Sample | Organisation | Saved website | Matched name or number | Saved page |',
              '|---|---|---|---|---|']
    for item in sorted((i for i in items if i['relabelled']), key=lambda i: (i['sample'], i['organisation_number'])):
        proof = item['group_receipt']
        lines.append(f"| {item['sample']} | {item['organisation_number']} · {item['company']} | `{item['url']}` | "
                     f"{proof['matched_text']} | [Saved page](<{proof['source_url']}>) |")
    lines += ['', 'Westnes Holding, Trollheim and Whale Safari all received the requested label. The Trollheim contact '
              'page prints the subsidiary name without a legal-form suffix. The frozen registry corroborates that full '
              'name stem at the shared registered domain. The phrase “endra organisasjonsform til AS” on Bjørns Bil '
              'describes a change of legal form and leaves its website label empty.', '',
              '[Pinned website verdicts](website_human_reviews.json) · [Every replay decision and receipt](website_replay.json)', '']
    (DEST / 'WEBSITE_REPLAY.md').write_text(portable_text('\n'.join(lines)), encoding='utf8', newline='\n')


def main():
    inputs, reviews, items, counts, matched = {}, [], [], {}, set()
    for sample, folder, work, pins, inventory, rows in samples('website'):
        inputs[sample] = {**pins, 'report_sha256': sha256(folder / 'report.json')}
        events = defaultdict(list)
        for event in read(folder / 'report.json')['request_log']:
            if event.get('organisation_number') in rows:
                events[event['organisation_number']].append(event)

        @lru_cache(maxsize=32)
        def load(sha):
            body = (work / 'state/blobs' / sha).read_bytes()
            assert hashlib.sha256(body).hexdigest() == sha
            return body

        def stored(sha):
            return decode_body(load(sha))

        statistics = Counter(published=0, retained=0, relabelled=0)
        for item in inventory['records']:
            if item['kind'] != 'website':
                continue
            org, url = item['organisation_number'], item['url']
            row, claims = rows[org]
            claim = claims[item['claim_id']]
            value = claim['value']
            assert value['final_url'] == url and claim['field'] == item['field']
            original_sha = value_sha256(value)
            evidence = {e['id']: e for e in row['evidence']}
            for receipt in item['receipts']:
                assert receipt['claim_span'] in stored(receipt['content_sha256'])

            key = org, urlsplit(url).hostname.removeprefix('www.')
            human_label = None
            if item['automated_verdict'] != 'correct':
                assert key not in matched and key in CORRECT | SHARED.keys() | UNSURE, (sample, key)
                matched.add(key)
                human_label = 'unsure' if key in UNSURE else 'correct'
                note = ('The site did not open for the reviewer. Keep the original automated label.' if key in UNSURE
                        else SHARED.get(key) or NOTES.get(org) or 'Confirmed by the reviewer.')
                reviews.append({
                    'sample': sample, 'seed': pins['seed'], 'sample_sha256': pins['input_sha256'],
                    'envelopes_sha256': pins['envelopes_sha256'], 'organisation_number': org,
                    'company': item['company'], 'kind': 'website', 'url': url, 'field': claim['field'],
                    'claim_id': claim['id'], 'value_sha256': original_sha, 'verdict': human_label,
                    'human_verified': key not in UNSURE, 'relationship_note': 'group_site' if key in SHARED else None,
                    'reviewer': REVIEWER, 'review_date': DATE, 'method': METHOD,
                    'automated_verdict': item['automated_verdict'], 'automated_reasons': item['reasons'],
                    'proof_tier': item['proof_tier'], 'note': note, 'receipts': item['receipts'],
                })

            pages = archived_pages(row, events[org], value, evidence, load)
            identity = next(evidence[r] for r in claim['evidence_ids'] if 'identity-proof:' in evidence[r]['locator'])
            proof_page = Page(load(identity['content_sha256']), identity['source_url'])
            context, _ = registry_context(org, row, evidence, stored)
            history = verified_former_names(org, row, evidence, stored, evidence)
            scope, page, witness = website_scope(value, list(pages.values()), org, context.get('name') or '', history,
                                                 proof_page=proof_page)
            old = value.get('relationship_note')
            new = 'group_site' if page is not None or scope == 'website_group_proof' else old
            witness_receipt = None
            if page is not None:
                source, sha = next(k for k, parsed in pages.items() if parsed is page)
                locator, span = group_site_receipt(page, scope, witness)
                assert not span or span in stored(sha)
                witness_receipt = {'source_url': source, 'content_sha256': sha, 'locator': locator,
                                   'claim_span': span, 'matched_text': witness}
            elif scope == 'website_group_proof':
                witness_receipt = {k: identity[k] for k in ('source_url', 'content_sha256', 'locator', 'claim_span')}
                witness_receipt['matched_text'] = ', '.join(value['other_orgnrs']) or 'Proven subunit on a group page'
            relabelled = new != old
            if key in SHARED:
                assert new == 'group_site' and witness_receipt, key
            statistics.update(published=1, retained=1, relabelled=int(relabelled))
            items.append({
                'sample': sample, 'organisation_number': org, 'company': item['company'], 'url': url,
                'claim_id': claim['id'], 'value_sha256': original_sha,
                'replayed_value_sha256': value_sha256({**value, 'relationship_note': new}),
                'before': old, 'after': new, 'relabelled': relabelled, 'retained': True,
                'scope': scope, 'group_receipt': witness_receipt, 'human_verdict': human_label,
                'original_automated_verdict': item['automated_verdict'],
            })
        assert len(rows) == statistics['published']
        counts[sample] = dict(statistics)

    assert matched == CORRECT | SHARED.keys() | UNSURE
    totals = {v: sum(r['verdict'] == v for r in reviews) for v in ('correct', 'wrong', 'unsure')}
    totals['correct_group_site'] = sum(r['relationship_note'] == 'group_site' for r in reviews)
    save(DEST / 'website_human_reviews.json', {'reviewer': REVIEWER, 'review_date': DATE, 'method': METHOD,
                                               'inputs': inputs, 'counts': totals, 'reviews': reviews})
    save(DEST / 'website_replay.json', {'inputs': inputs, 'samples': counts, 'items': items})
    write_report(items, counts)
    print(json.dumps({'reviews': totals, 'samples': counts}))


if __name__ == '__main__':
    main()
