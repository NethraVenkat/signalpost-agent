import pytest
from signalpost.web.html import Page
from signalpost.web.proof import score
from signalpost.web.collector import candidate_proof
from signalpost.web.candidates import Candidate

OUR = '923609016'
OTHER = '993578843'
FILL = 'Ordinary local business information and services. ' * 10


def proof(footer, title='Example AS', body='', context=None):
    p = Page(f'<title>{title}</title><header>{title}</header><main>{FILL}{body}</main><footer>{footer}</footer>'.encode(), 'https://example.no/')
    return score(p, OUR, context or {'name': 'Example AS'}, 'registry_website', [])


def test_foreign_publisher_rejects_even_when_our_exact_orgnr_is_present():
    p = proof(f'Example AS {OUR}; Parent AS {OTHER}')
    assert p.level == 'REJECT' and p.reason == 'publisher_foreign_orgnr'


def test_proven_subunit_is_not_foreign_and_unproven_one_is():
    assert proof(f'{OUR}; {OTHER}', context={'name': 'Example AS', 'subunits': [{'orgnr': OTHER}]}).level == 'VERIFIED'
    assert proof(f'{OUR} {OTHER}').level == 'REJECT'


@pytest.mark.parametrize('form', ['IKS', 'SA', 'DA', 'ANS'])
def test_different_legal_form_veto_precedes_exact_number(form):
    assert proof(f'Example {form} {OUR}').reason == 'publisher_conflicting_legal_form'


def test_as_asa_exception():
    assert proof(f'Example ASA {OUR}').level == 'VERIFIED'


def test_group_without_own_publisher_number_rejects_even_body_mentions():
    assert proof('Part of Example Group', body=f'<p>{OUR}</p>').reason == 'publisher_group_without_exact_orgnr'
    assert proof(f'Part of Example Group {OUR}').level == 'VERIFIED'


@pytest.mark.parametrize('label', ['Welcome to nginx!', 'Apache2 Ubuntu Default Page', 'Under construction'])
def test_default_placeholder_precedes_own_number(label):
    assert proof(OUR, title=label).reason == 'publisher_placeholder'


def test_third_party_service_publisher_and_own_accountant():
    assert proof('', title='Foreign Accounting', body=f'Example AS {OUR}').reason == 'publisher_service_provider'
    assert proof(OUR, title='Example AS Accounting').level == 'VERIFIED'


def test_third_party_credit_client_list_article_does_not_create_new_veto():
    p = proof(f'© Example AS {OUR}<span>Utviklet av Agency AS {OTHER}</span>',
              body=f'<article>Other AS {OTHER}</article><section class="partners">Other AS {OTHER}</section>')
    # Existing owner-text rules remain intact; R4 adds no veto for excluded credits.
    assert not p.reason.startswith('publisher_')


def test_subunit_fallback_cannot_override_publisher_conflict():
    page = Page(f'<title>Example AS</title><p>{FILL}</p><footer>Foreign AS {OTHER}</footer>'.encode(), 'https://example.no/')
    p = candidate_proof(page, OUR, {'name': 'Example AS'}, Candidate('https://example.no/', 'example.no', 'subunit_website', OTHER), [])
    assert p.reason == 'publisher_foreign_orgnr'


def test_part_of_selection_process_is_not_group_branding():
    assert not proof('Som en del av utvelgelsen vurderer vi selskaper.', body=OUR).reason.startswith('publisher_')


def test_biography_group_name_outside_real_header_does_not_veto():
    page = Page(('<html><head><title>Example AS</title></head><body><div class="header-over-content dmPageBody"><div class="d-header-wrapper">Example AS</div>'
                 '<main>Employee formerly at Foreign Financial Group. ' + FILL + '</main>'
                 '<footer>© Example AS. Example gate 1, 0001 OSLO <a href="tel:12345678">Phone</a></footer></div></body></html>').encode(), 'https://example.no/om-oss')
    context = {'name': 'Example AS', 'street': ['Example gate 1'], 'postcode': '0001', 'city': 'OSLO', 'phone': '12345678'}
    # Like SISSENER, this is the existing corroborated HIGH path, without an
    # exact publisher number that would hide the false group-veto regression.
    assert score(page, OUR, context, 'registry_website', []).level == 'HIGH'
