import pytest
from signalpost.web import rarity
from signalpost.web.reach_identity import unique_phone
from tests.test_r7_declared import page,context,ORG

@pytest.fixture
def counts(monkeypatch):
    d=rarity.load();counts={**d['counts'],'phone':{'22334455':1}}
    monkeypatch.setattr(rarity,'load',lambda:{**d,'counts':counts})
    return counts

def test_unique_phone_footer_without_name(counts):
    r=unique_phone(page('<footer>Telefon: 22 33 44 55</footer>'),ORG,context(website=None))
    assert r['tier']=='unique_registry_phone' and r['owner_signal']['rarity_count']==1

@pytest.mark.parametrize('count',[0,2,3])
def test_phone_must_be_exactly_unique(counts,count):
    counts['phone']['22334455']=count
    assert unique_phone(page('<footer>22 33 44 55</footer>'),ORG,context()) is None

@pytest.mark.parametrize('markup',['<header>22 33 44 55</header>','<p>22 33 44 55</p>','<footer>Other Business AS 22 33 44 55</footer>','<footer>22 33 44 56</footer>','<footer>Regnskapskontor 22 33 44 55</footer>','<footer>Property management 22 33 44 55</footer>','<footer>Web agency 22 33 44 55</footer>'])
def test_wrong_context_different_publisher_and_service_excluded(counts,markup):
    assert unique_phone(page(markup),ORG,context()) is None
