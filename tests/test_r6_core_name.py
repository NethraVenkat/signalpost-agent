import pytest
from signalpost.web.html import Page
from signalpost.web.candidates import Candidate
from signalpost.web.collector import candidate_proof
from signalpost.web.publisher_identity import CORE,core_receipt
from signalpost.web import rarity

ORG='923609016'


@pytest.fixture
def table(monkeypatch):
    original=rarity.load()
    counts={**original['counts'],'name':{'distinctive':2,'service':1,'short':1}}
    monkeypatch.setattr(rarity,'load',lambda:{**original,'counts':counts})
    return counts


def proof(markup,**ctx):
    page=Page(('<main>'+'Ordinary business services and information. '*12+'</main>'+markup).encode(),'https://distinctive.no/')
    context={'name':'Distinctive AS','website':'distinctive.no','candidate_url':'https://www.distinctive.no/',**ctx}
    return candidate_proof(page,ORG,context,Candidate(context['candidate_url'],'distinctive.no','registry_website'),[])


def test_declared_rare_core_in_publisher_without_suffix(table):
    result=proof('<title>Distinctive</title><footer>© Distinctive</footer>')
    assert result.level=='HIGH' and result.proof_type==CORE
    assert result.publisher_receipt['name_rarity_count']==2
    assert result.publisher_receipt['core_name']=='distinctive'


@pytest.mark.parametrize('markup',[
    '<p>Distinctive</p>','<article><header>Distinctive</header></article>',
    '<footer><div class="clients">Distinctive</div></footer>',
    '<footer>Developed by <a>Distinctive</a></footer>',
    '<header hidden>Distinctive</header>',
    '<footer>Distinctive Org.nr 993578843</footer>',
    '<footer>Distinctive Group</footer>',
    '<footer>Distinctive domain is parked</footer>',
])
def test_excluded_name_or_conflict_never_qualifies(table,markup):
    assert proof(markup).proof_type!=CORE


@pytest.mark.parametrize('frequency',[0,3,5])
def test_positive_name_rarity_bound(table,frequency):
    table['name']['distinctive']=frequency
    assert proof('<title>Distinctive</title>').proof_type!=CORE


def test_generic_and_unregistered_domain_abstain(table):
    assert proof('<title>Service</title>',name='Service AS').proof_type!=CORE
    assert proof('<title>Distinctive</title>',website=None).proof_type!=CORE
    assert proof('<title>Distinctive</title>',website='other.no').proof_type!=CORE
    assert proof('<title>Distinctive</title>',candidate_url='https://unregistered.no/').proof_type!=CORE


def test_cross_domain_target_never_qualifies_as_r6a(table):
    page=Page(b'<title>Distinctive</title>','https://elsewhere.no/')
    assert not core_receipt(page,ORG,{'name':'Distinctive AS','website':'distinctive.no','candidate_url':'https://distinctive.no/'})


def test_missing_rarity_table_abstains(monkeypatch):
    def missing():raise OSError('missing table')
    monkeypatch.setattr(rarity,'load',missing)
    assert proof('<title>Distinctive</title>').proof_type!=CORE
