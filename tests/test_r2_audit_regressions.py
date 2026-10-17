import json
from signalpost.web.html import Page
from signalpost.web.social import discover
from scripts.accuracy_audit import audit_identity_claim, audit_social_claim, audit_website_claim

ORG = '826440082'

def test_escaped_jsonld_social_span_is_localized_verbatim():
    url = 'https://www.linkedin.com/company/sorarkitekter?originalSubdomain=no'
    literal = json.dumps(url).replace('/', r'\/')
    body = '<html>' + 'x' * 500 + '<script type="application/ld+json">{"@type":"Organization","sameAs":[' + literal + ']}</script></html>'
    page = Page(body.encode(), 'https://company.no/')
    links = discover(page)
    assert len(links) == 1
    claim_url, span = next(iter(links.items()))
    assert span in body and literal in span and not span.startswith('<html>')
    claim = {'value': {'url': claim_url, 'platform': 'linkedin'}}
    assert audit_social_claim(ORG, claim, {'source_url': page.url}, body)[0] == 'CORRECT'
    assert audit_social_claim(ORG, {'value': {'url': 'https://www.linkedin.com/company/other'}}, {}, body)[0] == 'INCORRECT'

def test_deletion_audit_requires_true_and_valid_date_and_subject():
    claim = {'field': 'identity.deleted', 'value': True}
    ev = {'locator': '/slettedato'}
    source = {'organisasjonsnummer': ORG, 'slettedato': '2026-08-25'}
    assert audit_identity_claim(ORG, claim, ev, json.dumps(source))[0] == 'CORRECT'
    for date in ('nonsense', '', None, False):
        assert audit_identity_claim(ORG, claim, ev, json.dumps({**source, 'slettedato': date}))[0] == 'INCORRECT'
    assert audit_identity_claim(ORG, {**claim, 'value': False}, ev, json.dumps(source))[0] == 'INCORRECT'
    assert audit_identity_claim('923609016', claim, ev, json.dumps(source))[0] == 'INCORRECT'

def test_invoice_references_are_not_customer_ownership():
    value = {'final_url': 'https://example.no/', 'identity_level': 'VERIFIED', 'proof_type': 'orgnr_on_page', 'candidate_origin': 'legal_name_slug'}
    claim = {'field': 'official_website', 'value': value}
    own = '<title>Example AS</title><p>Fakturaadresse Example AS</p><p>EHF: Org. nr. 826440082. Vedlegg og referanser.</p>'
    context = {'name': 'Example AS'}
    assert audit_website_claim(ORG, claim, {}, own, context=context)[0] == 'CORRECT'
    customer = own.replace('Vedlegg og referanser', 'Våre kunder og referanser')
    assert audit_website_claim(ORG, claim, {}, customer, context=context)[0] == 'INCORRECT'
