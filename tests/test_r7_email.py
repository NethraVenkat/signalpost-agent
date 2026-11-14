import pytest
from signalpost.web import rarity
from signalpost.web.reach_identity import unique_email
from tests.test_r7_declared import page,context,ORG

@pytest.fixture
def counts(monkeypatch):
    d=rarity.load();counts={**d['counts'],'email':{'post@gmail.com':1,'post@example.no':1}}
    monkeypatch.setattr(rarity,'load',lambda:{**d,'counts':counts})
    return counts

@pytest.mark.parametrize('email',['post@gmail.com','post@example.no'])
def test_unique_email_may_be_freemail_in_publisher(counts,email):
    assert unique_email(page('<footer>'+email+'</footer>'),ORG,context(email=email,website=None))['tier']=='unique_registry_email'

@pytest.mark.parametrize('count',[0,2,3])
def test_full_email_must_be_unique(counts,count):
    counts['email']['post@gmail.com']=count
    assert unique_email(page('<footer>post@gmail.com</footer>'),ORG,context(email='post@gmail.com')) is None

@pytest.mark.parametrize('markup',['<p>post@gmail.com</p>','<footer hidden>post@gmail.com</footer>','<footer>Other Publisher AS post@gmail.com</footer>','<footer>Levert av <a>post@gmail.com</a></footer>'])
def test_hidden_body_agency_and_foreign_publisher_excluded(counts,markup):
    assert unique_email(page(markup),ORG,context(email='post@gmail.com')) is None

def test_staff_contact_does_not_establish_owner(counts):
    p=page('<p>Our staff</p><div>Email: post@gmail.com</div>',url='https://example.no/contact')
    assert unique_email(p,ORG,context(email='post@gmail.com')) is None
