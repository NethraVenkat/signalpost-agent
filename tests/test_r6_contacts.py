import pytest
from signalpost.web import rarity
from signalpost.web.html import Page
from signalpost.web.publisher_identity import TWO_CONTACTS,two_contacts_receipt
from signalpost.web.collector import candidate_proof
from signalpost.web.candidates import Candidate

@pytest.fixture
def table(monkeypatch):
    data=rarity.load();counts={**data['counts'],'phone':{'22334455':2}}
    monkeypatch.setattr(rarity,'load',lambda:{**data,'counts':counts})
    return counts

def result(markup,**changes):
    context={'name':'Unrelated AS','phone':'22334455','street':'Eksempelgata 12','postcode':'0123',**changes}
    page=Page(('<main>'+'Company information. '*40+'</main>'+markup).encode(),'https://example.no/')
    return candidate_proof(page,'923609016',context,Candidate(page.url,'example.no','legal_name_slug'),[])

GOOD='<footer>Telefon: 22 33 44 55. Adresse: Eksempelgata 12, 0123 Oslo</footer>'

def test_two_contacts_without_name(table):
    proof=result(GOOD)
    assert proof.proof_type==TWO_CONTACTS
    assert proof.publisher_receipt['address']['postcode']=='0123'

@pytest.mark.parametrize('markup',[GOOD.replace('0123','0124'),GOOD.replace('12,','13,'),GOOD.replace('22 33 44 55','22 33 44 56'),GOOD.replace('footer','article'),GOOD.replace('<footer>','<footer hidden>'),GOOD.replace('Telefon:','Org.nr 993578843 Telefon:'),GOOD.replace('Telefon:','Regnskapskontor Telefon:'),GOOD.replace('Telefon:','Web agency Telefon:')])
def test_reject_missing_mismatched_body_hidden_conflict_service(table,markup):assert result(markup).proof_type!=TWO_CONTACTS

@pytest.mark.parametrize('count',[0,3])
def test_rarity_required(table,count):
    table['phone']['22334455']=count
    assert result(GOOD).proof_type!=TWO_CONTACTS

def test_whole_street_and_postcode_required(table):
    assert result(GOOD,street='Eksempelgata 1').proof_type!=TWO_CONTACTS
    assert result(GOOD,postcode=None).proof_type!=TWO_CONTACTS
