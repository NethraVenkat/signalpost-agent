import pytest
from signalpost.web import rarity
from signalpost.web.html import Page
from signalpost.web.reach_identity import unique_name_domain
from tests.test_r7_declared import context,ORG

@pytest.fixture
def counts(monkeypatch):
    d=rarity.load();counts={**d['counts'],'name':{'example workshop':1}}
    monkeypatch.setattr(rarity,'load',lambda:{**d,'counts':counts})
    return counts

def build(url='https://exampleworkshop.no/',name='Example Workshop AS',tie='lang="nb"',extra=''):
    return Page((f'<html {tie}><header>{name}</header><main>'+('Company information. '*30)+f'</main>{extra}</html>').encode(),url)

def ctx(url='https://exampleworkshop.no/'):
    return context(name='Example Workshop AS',website=None,candidate_url=url,phone=None,email=None,street=None,postcode=None)

@pytest.mark.parametrize('url',['https://exampleworkshop.no/','https://example-workshop.com/'])
def test_unique_exact_name_and_domain_with_norway_tie(counts,url):
    assert unique_name_domain(build(url),ORG,ctx(url))['tier']=='exact_name_unique_domain'

@pytest.mark.parametrize('count',[0,2])
def test_unique_name_key_required(counts,count):
    counts['name']['example workshop']=count
    assert unique_name_domain(build(),ORG,ctx()) is None

@pytest.mark.parametrize('url',['https://example.no/','https://exampleworkshopother.no/'])
def test_full_domain_label_required(counts,url):assert unique_name_domain(build(url),ORG,ctx(url)) is None

def test_suffix_norway_tie_and_non_group_required(counts):
    assert unique_name_domain(build(name='Example Workshop'),ORG,ctx()) is None
    assert unique_name_domain(build(tie='lang="en"'),ORG,ctx()) is None
    assert unique_name_domain(build(extra='<footer>Franchise</footer>'),ORG,ctx()) is None
    assert unique_name_domain(build(extra='<footer>Org.nr 993578843</footer>'),ORG,ctx()) is None
    assert unique_name_domain(build(extra='<footer>Our companies</footer>'),ORG,ctx()) is None

@pytest.mark.parametrize('label',['aeoeaaworkshop','aoaworkshop','aeoeaa-workshop','aoa-workshop'])
def test_both_norwegian_folding_schemes_require_same_full_publisher_name(counts,label):
    from signalpost.web.rarity import name_key
    name=chr(198)+chr(216)+chr(197)+' Workshop AS'
    counts['name'][name_key(name)]=1
    url='https://'+label+'.no/'
    p=build(url,name=name)
    c={**ctx(url),'name':name}
    assert unique_name_domain(p,ORG,c)['domain_label']==label
