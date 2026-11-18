"""Reapply the social rules to every saved P2 and P3g social claim offline."""

import hashlib
import json
import sys
from collections import Counter, defaultdict

from record_human_reviews import DEST, ROOT, read, samples, save, value_sha256

sys.path.insert(0, str(ROOT))
from scripts.verify_owner_social import verified_former_names
from scripts.verify_publisher_identity import registry_context
from signalpost.portable_paths import portable_text
from signalpost.sources.text import decode_body
from signalpost.web.html import Page
from signalpost.web.owner_social import SAME_AS, page_profiles, profile_key, profile_url, same_as_veto, site_scope, visible_profiles
from signalpost.web.policy import domain, normalize_url


def reconstruct_pages(row, events, site, evidence, load):
    root = domain(site['final_url'])
    refresh = row['run']['refresh']
    initial_urls = set(refresh['website']['checked_urls'])
    contact = refresh.get('owner_social', {})
    contact_urls = {normalize_url(url) for url in contact.get('checked_urls', [])}
    accepted_contact = contact.get('state') == 'available'
    expected = initial_urls | contact_urls
    pages = {}
    eligible = set()
    for e in evidence.values():
        if (e['source_class'] == 'company_owned' and e['locator'].startswith('company-link:')
                and domain(e['source_url']) == root):
            key = e['source_url'], e['content_sha256']
            pages[key] = Page(load(key[1]), key[0])
            eligible.add(key)
    covered = {url for url, _ in pages}
    # The request log pins the HTML that contributed no published receipt.
    redirects = {normalize_url(e['url']): normalize_url(e['redirect_target'])
                 for e in events if 'redirect_target' in e}
    routes = {}
    for requested in expected:
        target = requested
        for _ in range(4):
            if target not in redirects or redirects[target] == target:
                break
            target = redirects[target]
        if target and domain(target) == root:
            routes.setdefault(target, set()).add(requested)
    for e in events:
        url = e['url']
        if e['status'] != 200 or e['error'] or not e.get('content_sha256') or url not in routes:
            continue
        key = url, e['content_sha256']
        if key not in pages:
            pages[key] = Page(load(key[1]), url)
        checked = routes[url]
        if checked & initial_urls or accepted_contact and checked & contact_urls:
            eligible.add(key)
        covered.update(checked)
    # Older output cannot prove a negative when a checked page is absent.
    assert expected <= covered, (row['organisation_number'], sorted(expected - covered))
    return pages, eligible


def competing_link(url, pages):
    platform, claimed = profile_key(url)
    for page in pages:
        for link in page.links:
            if not link.rendered or not (visible_url := profile_url(link.href)):
                continue
            linked_platform, linked = profile_key(visible_url)
            if linked_platform == platform and linked != claimed:
                return {
                    'source_url': page.url,
                    'content_sha256': hashlib.sha256(page.body).hexdigest(),
                    'matched_text': visible_url,
                    'claim_span': link.span,
                }
    raise ValueError('Missing visible conflict receipt')


def write_summary(totals, results):
    reason = {
        'same_as_visible_profile_conflict': 'Different visible profile on the same platform',
        'same_as_no_distinctive_name': 'JSON-LD-only handle lacks a distinctive registry-name token',
        'other_registered_name_on_page': 'Another full registered legal name appears on the site',
        'other_registered_entity_on_shared_domain': 'Visible registered name at the same registered domain',
        'other_orgnr_on_page': 'Another valid organisation number appears on the site',
        'website_group_proof': 'The website proof identifies a group site',
    }
    lines = [
        '# HC1 saved social replay', '',
        'The replay uses the recorded website proof pages and contact-page receipts from P2 and P3g. '
        'It verifies their hashes locally and reapplies the current social publication rules to the saved URLs.',
        '',
        '| Sample | Original URLs | Retained | Withheld | Human-correct retained | Human-correct withheld |',
        '|---|---:|---:|---:|---:|---:|',
    ]
    for label, counts in totals.items():
        lines.append('| ' + label + ' | ' + ' | '.join(str(counts.get(key, 0)) for key in (
            'original', 'retained', 'withheld', 'human_correct_retained', 'human_correct_withheld')) + ' |')
    lines += ['', 'Both human-confirmed wrong links were withheld. Three human-confirmed correct links were also '
              'withheld under the same shared-site rule. The table lists every withheld URL.', '',
              '| Sample | Organisation | Saved URL | Human verdict | Original automated verdict | Reason |',
              '|---|---|---|---|---|---|']
    for item in sorted((r for r in results if not r['retained']),
                       key=lambda r: (r['human_verdict'] != 'wrong', r['sample'], r['organisation_number'], r['url'])):
        detail = reason.get(item['reason'], item['reason'])
        witness = item['veto_receipt']
        if witness and witness['matched_text']:
            detail += f" · [{witness['matched_text']}](<{witness['source_url']}>)"
        lines.append(f"| {item['sample']} | {item['organisation_number']} · {item['company']} | "
                     f"`{item['url']}` | {item['human_verdict'] or 'unreviewed'} | "
                     f"{item['original_automated_verdict']} | {detail} |")
    lines += ['', 'The three human-confirmed losses are Accella’s LinkedIn (another registered firm in the '
              'site credit), OfficeAid’s Facebook (another registered firm named in a product category), and '
              'Trollheim’s Twitter (the same site names a second entity registered at that domain). The '
              'saved pages do not supply the exact-organisation profile tie required on a shared site.', '',
              '[Pinned human verdicts](human_reviews.json) · [Every replay decision and proof excerpt](replay.json)', '']
    (DEST / 'REPLAY.md').write_text(portable_text('\n'.join(lines)), encoding='utf8', newline='\n')


def replay():
    ledger = read(DEST / 'human_reviews.json')
    hand_checks = {(r['sample'], r['organisation_number'], r['field'], r['value_sha256']): r['verdict']
                   for r in ledger['reviews']}
    results, totals = [], {}
    for label, folder, work, pins, inventory, rows in samples():
        assert pins == ledger['inputs'][label]
        events = defaultdict(list)
        for event in read(folder / 'report.json')['request_log']:
            if event.get('section') == 'website':
                events[event['organisation_number']].append(event)
        automated = {i['claim_id']: i['automated_verdict'] for i in inventory['records'] if i['kind'] == 'social'}
        counters = Counter()
        for org, (row, claims) in rows.items():
            def load(digest):
                saved = (work / 'state/blobs' / digest).read_bytes()
                assert hashlib.sha256(saved).hexdigest() == digest
                return saved

            evidence = {e['id']: e for e in row['evidence']}
            stored = lambda digest: decode_body(load(digest))
            site = next(c['value'] for c in row['claims'] if c['field'] == 'official_website'
                        and c['availability'] == 'available')
            context, _ = registry_context(org, row, evidence, stored)
            context['former_names'] = verified_former_names(org, row, evidence, stored, evidence)
            pages, eligible = reconstruct_pages(row, events[org], site, evidence, load)
            visible = visible_profiles(pages.values())
            scope, scope_page, detail = site_scope(site, list(pages.values()), org, context['name'], context['former_names'])
            kept = {url for key, page in pages.items() if key in eligible
                    for url in page_profiles(page, site, org, context, visible, bool(scope))}
            scope_receipt = None
            if scope_page:
                scope_receipt = {
                    'source_url': scope_page.url,
                    'content_sha256': hashlib.sha256(scope_page.body).hexdigest(),
                    'matched_text': detail,
                    'claim_span': scope_page.span_for(detail)[:300] if detail else None,
                }
            for claim in claims.values():
                value = claim['value']
                url = value['url']
                digest = value_sha256(value)
                verdict = hand_checks.get((label, org, claim['field'], digest))
                allowed = url in kept
                reason = None
                if not allowed:
                    if scope:
                        reason = scope
                    elif value['proof_tier'] == SAME_AS:
                        reason = same_as_veto(url, visible, context['name'], context['former_names'])
                    assert reason, (label, org, url, 'Missing reproduction of the original publication proof')
                receipts = [evidence[ref] for ref in claim['evidence_ids']
                            if evidence[ref]['locator'] == 'company-link:' + url]
                assert receipts and all(e['claim_span'] in stored(e['content_sha256']) for e in receipts)
                counters['original'] += 1
                counters['retained' if allowed else 'withheld'] += 1
                if verdict == 'correct':
                    counters['human_correct_retained' if allowed else 'human_correct_withheld'] += 1
                veto_receipt = scope_receipt if reason == scope else None
                if reason == 'same_as_visible_profile_conflict':
                    veto_receipt = competing_link(url, pages.values())
                results.append({
                    'sample': label, 'organisation_number': org, 'company': context['name'],
                    'field': claim['field'], 'claim_id': claim['id'], 'url': url, 'value_sha256': digest,
                    'retained': allowed, 'reason': reason, 'human_verdict': verdict,
                    'original_automated_verdict': automated[claim['id']],
                    'proof_receipts': receipts,
                    'veto_receipt': veto_receipt,
                })
        assert len(automated) == counters['original']
        totals[label] = dict(counters)
    wrong = [item for item in results if item['human_verdict'] == 'wrong']
    assert len(wrong) == 2 and all(not item['retained'] for item in wrong)
    assert sum(item['human_verdict'] == 'correct' for item in results) == ledger['counts']['correct']
    save(DEST / 'replay.json', {'inputs': ledger['inputs'], 'samples': totals, 'items': results})
    write_summary(totals, results)
    print(json.dumps(totals))
    for item in results:
        if not item['retained']:
            print(item['sample'], item['organisation_number'], item['url'], item['reason'],
                  item['human_verdict'] or item['original_automated_verdict'])


if __name__ == '__main__':
    replay()
