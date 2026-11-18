"""Replay owner social declarations against original pages and official identity."""
import csv
import hashlib
import io
import json
import re

from signalpost.sources.bulk_registry import column
from signalpost.sources.registry_fields import reported
from signalpost.web.html import Page
from signalpost.web.owner_social import (
    FOLLOW_US, GROUP_RECEIPT_METHOD, SAME_AS, SAME_AS_POLICY, SHARED_SITE_POLICY, SOCIAL_POLICY,
    declared_profiles, former_names, group_site_receipt, page_profiles, same_as_veto, site_scope,
    visible_profiles, website_scope,
)
from signalpost.web.policy import domain
from scripts.verify_publisher_identity import registry_context

TIERS = {SAME_AS, FOLLOW_US}


def reviewed_pages(site, review, stored_body, raw_body):
    manifest = review.get('social_pages')
    assert isinstance(manifest, list) and manifest, 'Missing social page receipts'
    pages = {}
    for entry in manifest:
        url, sha = entry['url'], entry['content_sha256']
        assert domain(url) == domain(site['value']['final_url']), 'Foreign social page receipt'
        assert re.fullmatch(r'[0-9a-f]{64}', sha), 'Invalid social page hash'
        if raw_body is not None:
            assert hashlib.sha256(raw_body(sha)).hexdigest() == sha, 'Invalid social page body'
        text = stored_body(sha)
        pages[url, sha] = Page(text.encode('utf8'), url, text=text)
    assert set(review.get('checked_urls', [])) <= {url for url, _ in pages}, 'Incomplete social page receipts'
    return pages


def verified_former_names(org, data, evidence, stored_body, refs):
    names = []
    for claim in data['claims']:
        if (claim['field'] != 'identity.historical_names' or claim['availability'] != 'available'
                or claim.get('carried_forward')):
            continue
        for ref in set(claim['evidence_ids']) & set(refs):
            e = evidence[ref]
            if e['source_class'] != 'official_registry':
                continue
            body = stored_body(e['content_sha256'])
            if e['locator'].casefold() == '/historiskenavn':
                row = json.loads(body)
                value = column(row, 'historiskeNavn')[0]
            elif e['locator'].casefold() == f'row:{org}/column:historiskenavn':
                row = next((r for r in csv.DictReader(io.StringIO(body))
                            if column(r, 'organisasjonsnummer')[0] == org), {})
                value = reported(column(row, 'historiskeNavn')[0], 'records', csv=True)
            else:
                continue
            if column(row, 'organisasjonsnummer')[0] == org and value == claim['value']:
                names.extend(former_names(value))
    return tuple(dict.fromkeys(names))


def verify_website_scope(org, site, pages, name, history, evidence, stored_body):
    value = site['value']
    receipts = [evidence[ref] for ref in site['evidence_ids']]
    proof_page = None
    if value.get('matched_via_subunit'):
        proof = next((e for e in receipts if e['source_url'] == value['proof_page_url']
                      and 'identity-proof:' in e['locator']), None)
        assert proof, 'Missing subunit website proof'
        text = stored_body(proof['content_sha256'])
        proof_page = Page(text.encode('utf8'), proof['source_url'], text=text)
    scope, page, match = website_scope(value, list(pages.values()), org, name, history, proof_page=proof_page)
    expected_label = 'group_site' if scope == 'website_group_proof' or page is not None else None
    assert value.get('relationship_note') == expected_label, 'Unsupported social site scope: website relationship note'

    expected_receipts = []
    if page is not None:
        locator, span = group_site_receipt(page, scope, match)
        if span:
            url, sha = next(key for key, parsed in pages.items() if parsed is page)
            expected_receipts.append((url, sha, locator, span, 'company_owned', GROUP_RECEIPT_METHOD))
    actual_receipts = [(e['source_url'], e['content_sha256'], e['locator'], e['claim_span'],
                        e['source_class'], e['extraction_method']) for e in receipts
                       if e['locator'].startswith('group-site:') or e['extraction_method'] == GROUP_RECEIPT_METHOD]
    assert expected_receipts == actual_receipts, 'Unsupported group-site evidence'
    return scope


def verify(org,data,evidence,stored_body,raw_body=None):
    review = (data.get('run') or data).get('refresh', {}).get('website', {})
    policy = review.get('social_policy')
    group_labels = policy == SOCIAL_POLICY
    current = policy in {SHARED_SITE_POLICY, SOCIAL_POLICY}
    check_site = current or policy == SAME_AS_POLICY
    claims = [c for c in data['claims'] if c['field'].startswith('social_profile.')
              and c['availability'] == 'available' and (current or c['value'].get('proof_tier') in TIERS)]
    if not claims and not group_labels:
        return 0
    site = next((c for c in data['claims'] if c['field'] == 'official_website'
                 and c['availability'] == 'available'), None)
    if not claims and (not site or site.get('carried_forward')):
        return 0
    assert site, 'Owner social requires a verified/HIGH website'
    context, _ = registry_context(org, data, evidence, stored_body)
    name_refs = {r for c in data['claims'] if c['field'] == 'identity.legal_name'
                 and c['availability'] == 'available' for r in c['evidence_ids']}
    if check_site:
        pages = reviewed_pages(site, review, stored_body, raw_body)
        visible = visible_profiles(pages.values())
    if current:
        eligible = {(p['url'], p['content_sha256']) for p in review['social_pages'] if p['eligible'] is True}
        scope_names = verified_former_names(org, data, evidence, stored_body, evidence)
        name = context.get('name') or ''
        if group_labels:
            scope = verify_website_scope(org, site, pages, name, scope_names, evidence, stored_body)
        else:
            scope, _, _ = site_scope(site['value'], list(pages.values()), org, name, scope_names)
        assert scope == review.get('social_scope'), 'Unsupported social site scope'
    for claim in claims:
        value = claim['value']
        tier = value['proof_tier']
        if tier in TIERS:
            assert site['value']['identity_level'] in {'HIGH', 'VERIFIED'}, 'Owner social requires a verified/HIGH website'
        if not current:
            assert not site['value'].get('other_orgnrs') and site['value'].get('relationship_note') != 'group_site', (
                'Group social declaration')
        assert name_refs and name_refs<=set(claim['evidence_ids']),'Missing legal-name dependencies'
        assert set(site['evidence_ids'])<=set(claim['evidence_ids']),'Missing verified-site dependencies'
        assert value['company_name']==context['name'],'Unsupported social legal name'
        history = ()
        if check_site and tier == SAME_AS and same_as_veto(value['url'], visible, context['name']):
            history = verified_former_names(org, data, evidence, stored_body, claim['evidence_ids'])
            assert not same_as_veto(value['url'], visible, context['name'], history), 'JSON-LD social veto'
        receipt = value.get('owner_declaration')
        matched = False
        for ref in claim['evidence_ids']:
            e=evidence[ref]
            if e['source_class']!='company_owned' or e['locator']!='company-link:'+value['url']:continue
            assert domain(e['source_url'])==domain(site['value']['final_url']),'Foreign social publisher'
            if check_site:
                key = e['source_url'], e['content_sha256']
                assert key in pages and (not current or key in eligible), 'Missing eligible social page'
                page = pages[key]
            else:
                text=stored_body(e['content_sha256'])
                page=Page(text.encode('utf8'),e['source_url'],text=text)
            if current:
                profiles = page_profiles(page, site['value'], org, {**context, 'former_names': history}, visible, bool(scope))
            else:
                profiles = declared_profiles(page, context['name'], org, context)
            expected = profiles.get(value['url'])
            if expected and expected['tier'] == tier and expected['span'] == e['claim_span']:
                matched |= expected == receipt if tier in TIERS else receipt is None
        assert matched,'Unsupported owner social declaration'
    return len(claims)
