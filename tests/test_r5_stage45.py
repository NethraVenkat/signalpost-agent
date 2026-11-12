import pytest
from signalpost.web.proof import registry_contacts
from signalpost.web.html import Page
from signalpost.web.collector import candidate_proof
from signalpost.web.candidates import Candidate
from tests.test_websites import html, OUR, OTHER, execute_web


@pytest.mark.parametrize('actual',['+47 12 34 56 78','0047 12345678','12 34 56 78'])
def test_exact_registry_phone_normalization(actual):
    page=Page(html('',extra=f'<a href="tel:{actual}">Phone</a>').encode(),'https://example.no/')
    matches=registry_contacts(page,{'phone':'12345678'})
    assert matches['phone'][0]=='+4712345678'
    assert matches['phone'][1] in page.raw


@pytest.mark.parametrize('actual,expected',[('person@example.no',True),('person@sub.example.no',False),
                                         ('person@other.no',False),('person@example.no.evil.no',False)])
def test_exact_email_domain_not_substring(actual,expected):
    page=Page(html('',extra=f'<a href="mailto:{actual}">Email</a>').encode(),'https://example.no/')
    assert bool(registry_contacts(page,{'email':'registered@example.no'})) is expected


def test_free_mail_and_wrong_phone_cannot_prove_company():
    page=Page(html('',extra='<a href="mailto:anyone@gmail.com">Email</a><a href="tel:12345679">Phone</a>').encode(),'https://example.no/')
    assert not registry_contacts(page,{'email':'registered@gmail.com','phone':'12345678'})


@pytest.mark.parametrize('domain',['sub.gmail.com','department.outlook.com','invalid..no'])
def test_shared_provider_subdomains_do_not_count_as_corporate_proof(domain):
    page=Page(html('',extra=f'<a href="mailto:anyone@{domain}">Email</a>').encode(),'https://example.no/')
    assert not registry_contacts(page,{'email':'registered@'+domain})


@pytest.mark.parametrize('footer,extra',[('Org.nr '+OTHER,''),('', 'Our companies'),('Org.nr '+OUR,'This domain is for sale')])
def test_contact_agreement_never_overrides_veto(footer,extra):
    page=Page(html(footer,extra=extra+'<a href="tel:12345678">Phone</a>').encode(),'https://example.no/')
    proof=candidate_proof(page,OUR,{'name':'Example AS','phone':'12345678'},Candidate(page.url,'example.no','registry_website'),[])
    assert proof.level=='REJECT'


def test_phone_alone_on_guessed_domain_is_not_identity_proof():
    page=Page(html('',extra='<a href="tel:12345678">Phone</a>').encode(),'https://example.no/')
    assert candidate_proof(page,OUR,{'name':'Example AS','phone':'12345678'},Candidate(page.url,'example.no','legal_name_slug'),[]).level not in {'VERIFIED','HIGH'}


def test_corroboration_retains_both_registry_and_page_evidence(tmp_path,monkeypatch):
    _,row,_,_=execute_web(tmp_path,monkeypatch,body=html('Org.nr '+OUR,extra='<footer><a href="tel:12345678">Phone</a></footer>'))
    claim=next(c for c in row['claims'] if c['field']=='official_website')
    assert claim['value']['registry_contact_matches']['phone']=='+4712345678'
    evidence={e['id']:e for e in row['evidence']}
    assert {'official_registry','company_owned'} <= {evidence[eid]['source_class'] for eid in claim['evidence_ids']}
    assert any(evidence[eid]['extraction_method']=='signalpost.registry_contact.v1' for eid in claim['evidence_ids'])
