import pytest
from signalpost.web.collector import candidate_proof
from signalpost.web.candidates import Candidate
from signalpost.web.html import Page
from tests.test_websites import html,OUR,OTHER

@pytest.mark.parametrize('origin',['legal_name_slug','registry_email','registry_website'])
def test_proven_branch_publisher_number_proves_parent_candidate(origin):
    p=Page(html('Org.nr '+OTHER).encode(),'https://example.no/')
    proof=candidate_proof(p,OUR,{'name':'Example AS','subunits':[{'orgnr':OTHER}]},Candidate(p.url,'example.no',origin),[])
    assert proof.level=='VERIFIED' and proof.token==OTHER
    assert 'proven_subunit_publisher_number' in proof.signals

@pytest.mark.parametrize('markup,units',[
    ('<footer>Org.nr '+OTHER+'</footer>',[]),
    ('<article>Org.nr '+OTHER+'</article>',[{'orgnr':OTHER}]),
    ('<footer hidden>Org.nr '+OTHER+'</footer>',[{'orgnr':OTHER}]),
    ('<footer>Org.nr 988258229</footer>',[{'orgnr':OTHER}]),
    ('<footer>Levert av <a>Org.nr '+OTHER+'</a></footer>',[{'orgnr':OTHER}]),
    ('<footer>Org.nr '+OTHER+' Org.nr 988258229</footer>',[{'orgnr':OTHER}])])
def test_unproven_body_hidden_agency_or_foreign_branch_rejected(markup,units):
    p=Page(('<main>'+'Company information. '*30+'</main>'+markup).encode(),'https://example.no/')
    proof=candidate_proof(p,OUR,{'name':'Example AS','subunits':units},Candidate(p.url,'example.no','legal_name_slug'),[])
    assert proof.level!='VERIFIED'

def test_group_branch_number_rechecked_as_branch_without_overriding_other_vetoes():
    p=Page(html('Our companies Org.nr '+OTHER).encode(),'https://example.no/')
    proof=candidate_proof(p,OUR,{'name':'Example AS','subunits':[{'orgnr':OTHER}]},Candidate(p.url,'example.no','legal_name_slug'),[])
    assert proof.level=='VERIFIED' and proof.token==OTHER
