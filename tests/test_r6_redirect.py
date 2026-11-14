import pytest
from signalpost.web.html import Page
from signalpost.web.candidates import Candidate
from signalpost.web.collector import candidate_proof
from signalpost.web.publisher_identity import REDIRECT,redirect_receipt

ORG='923609016'


def proof(markup,**ctx):
    p=Page(('<main>'+'Ordinary business information. '*20+'</main>'+markup).encode(),'https://newdomain.no/')
    context={'name':'Example AS','website':'old.no','candidate_url':'https://www.old.no/',**ctx}
    return candidate_proof(p,ORG,context,Candidate(context['candidate_url'],'old.no','registry_website'),[])


def test_exact_full_publisher_name_on_registered_redirect():
    p=proof('<footer>Example AS</footer>')
    assert p.level=='HIGH' and p.proof_type==REDIRECT
    assert p.publisher_receipt['registry_homepage']=='old.no'


@pytest.mark.parametrize('markup',[
    '<p>Example AS</p>','<footer>Example</footer>','<footer>Example ASA</footer>',
    '<footer>Levert av <a>Example AS</a></footer>',
    '<footer>Example AS, Org.nr 993578843</footer>',
    '<footer>Example AS Part of Example Group</footer>',
    '<footer>Example AS under construction</footer>',
    '<footer hidden>Example AS</footer>',
])
def test_wrong_context_suffix_hidden_or_veto_rejects(markup):
    assert proof(markup).proof_type!=REDIRECT


def test_no_registry_candidate_and_same_domain_do_not_use_redirect_tier():
    assert proof('<footer>Example AS</footer>',candidate_url='https://unregistered.no/').proof_type!=REDIRECT
    assert proof('<footer>Example AS</footer>',website=None).proof_type!=REDIRECT
    p=Page(b'<footer>Example AS</footer>','https://old.no/')
    assert not redirect_receipt(p,ORG,{'name':'Example AS','website':'old.no','candidate_url':'https://old.no/'})
