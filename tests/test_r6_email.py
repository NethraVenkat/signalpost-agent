import pytest
from signalpost.web import rarity
from signalpost.web.html import Page
from signalpost.web.collector import candidate_proof
from signalpost.web.candidates import Candidate
from signalpost.web.publisher_identity import OWN_EMAIL

@pytest.fixture
def table(monkeypatch):
    data=rarity.load();counts={**data['counts'],'email':{'post@example.no':2,'post@gmail.com':1}}
    monkeypatch.setattr(rarity,'load',lambda:{**data,'counts':counts})
    return counts

def proof(markup,email='post@example.no'):
    p=Page(('<main>'+'Information and services. '*30+'</main>'+markup).encode(),'https://example.no/')
    return candidate_proof(p,'923609016',{'name':'Unrelated AS','email':email},Candidate(p.url,'example.no','registry_email'),[])

def test_exact_rare_own_email_without_name(table):
    assert proof('<footer>post@example.no</footer>').proof_type==OWN_EMAIL

@pytest.mark.parametrize('markup',['<p>post@example.no</p>','<article><footer>post@example.no</footer></article>',
    '<footer>Levert av <a>post@example.no</a></footer>','<footer>post@other.no</footer>',
    '<footer>post@example.no Org.nr 993578843</footer>','<footer hidden>post@example.no</footer>'])
def test_body_foreign_hidden_credit_and_id_veto(table,markup):assert proof(markup).proof_type!=OWN_EMAIL

@pytest.mark.parametrize('count',[0,3,5])
def test_absent_or_common_email(table,count):
    table['email']['post@example.no']=count
    assert proof('<footer>post@example.no</footer>').proof_type!=OWN_EMAIL

def test_freemail_and_different_domain(table):
    assert proof('<footer>post@gmail.com</footer>',email='post@gmail.com').proof_type!=OWN_EMAIL
    assert proof('<footer>post@example.no</footer>',email='post@different.no').proof_type!=OWN_EMAIL
