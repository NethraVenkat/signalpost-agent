import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts.verify_owner_social import verify_website_scope
from signalpost.sources.extract import Section
from signalpost.web.candidates import Candidate
from signalpost.web.collector import publish_result
from signalpost.web.html import Page
from signalpost.web.owner_social import website_scope
from signalpost.web.policy import domain
from signalpost.web.proof import Proof


FIXTURES = Path(__file__).parent / 'fixtures/website_hc1'
SOURCES = json.loads((FIXTURES / 'sources.json').read_text(encoding='utf8'))


def fixture_bytes(name):
    body = (FIXTURES / name).read_bytes()
    assert hashlib.sha256(body).hexdigest() == SOURCES[name]['fixture_sha256']
    return body


def response_and_page(url, body):
    response = SimpleNamespace(url=url, body=body, retrieved_at='2026-11-17T10:00:00Z',
                               sha=hashlib.sha256(body).hexdigest())
    return response, Page(body, url)


@pytest.mark.parametrize('parts, legal_name, level, proof_type, token, contact, match', [
    (('westnes-subsidiary.body', 'westnes-orgnr.body'), 'WESTNES HOLDING AS', 'VERIFIED', 'orgnr_on_page',
     '930595764', None, 'Westnes Invest AS'),
    (('whalesafari-footer.body',), 'HVALSAFARI AS', 'HIGH', 'registry_declared_publisher_name',
     'Hvalsafari AS', None, 'Whale2Sea AS'),
    (('trollheim-title.body', '../social_hc1/trollheim-facebook.body'), 'TROLLHEIM AS', 'HIGH', 'signals',
     'Trollheim', '../social_hc1/trollheim-kontakt.body', 'trollheim kurs og kompetanse'),
])
def test_saved_group_website_keeps_original_identity_proof(parts, legal_name, level, proof_type, token, contact, match):
    source = SOURCES[parts[0]]
    org, url = source['organisation_number'], source['url']
    body = b'<html><head></head><body><footer>' + b'\n'.join(fixture_bytes(part) for part in parts) + b'</footer></body></html>'
    response, page = response_and_page(url, body)
    pages = [(response, page)]
    if contact:
        pages.append(response_and_page(SOURCES[contact]['url'], fixture_bytes(contact)))
    proof = Proof(level, proof_type, token=token)
    candidate = Candidate(url, domain(url), 'registry_website')
    http = SimpleNamespace(accepted_pages={}, attempts={})
    envelope = SimpleNamespace(claims=[], evidence=[], run=SimpleNamespace(refresh={}))

    section = publish_result(org, envelope, http, Section(), [(candidate, proof, response, page, pages)], [],
                             {'name': legal_name})

    site = next(claim for claim in section.claims if claim.field == 'official_website')
    assert section.state == 'available' and site.availability == 'available'
    assert site.value['relationship_note'] == 'group_site'
    assert site.value['identity_level'] == level and site.value['proof_type'] == proof_type
    assert site.value['final_url'] == url.rstrip('/') and site.value['other_orgnrs'] == []
    assert not any(claim.field.startswith('social_profile.') for claim in section.claims)
    evidence = {e.id: e.model_dump() for e in section.evidence}
    group_proof = next(evidence[ref] for ref in site.evidence_ids if evidence[ref]['locator'].startswith('group-site:'))
    source_response = pages[-1][0]
    assert group_proof['locator'].endswith(':' + match)
    assert group_proof['source_url'] == source_response.url and group_proof['content_sha256'] == source_response.sha
    assert match.casefold() in group_proof['claim_span'].casefold()

    parsed = {(r.url, r.sha): p for r, p in pages}
    stored_body = {r.sha: p.raw for r, p in pages}.__getitem__
    check = site.model_dump()
    assert verify_website_scope(org, check, parsed, legal_name, (), evidence, stored_body) == envelope.run.refresh['website']['social_scope']
    check['value']['relationship_note'] = None
    with pytest.raises(AssertionError, match='website relationship note'):
        verify_website_scope(org, check, parsed, legal_name, (), evidence, stored_body)


def test_saved_legal_form_in_prose_does_not_label_a_group():
    source = SOURCES['bjorns-form.body']
    page = Page(fixture_bytes('bjorns-form.body'), source['url'])
    site = {'final_url': source['url']}
    assert website_scope(site, [page], source['organisation_number'], 'BJØRNS BIL AS') == (None, None, None)
    company = Page(b'<p>Til AS</p>', source['url'])
    assert website_scope(site, [company], source['organisation_number'], 'BJØRNS BIL AS')[2] == 'Til AS'
