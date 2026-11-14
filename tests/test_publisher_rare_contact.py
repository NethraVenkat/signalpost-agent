import copy
import pytest
from signalpost.web.html import Page
from signalpost.web.collector import candidate_proof
from signalpost.web.candidates import Candidate
from signalpost.web.publisher_identity import RARE,rare_receipt
from signalpost.web import rarity

ORG='923609016'
FILL='Information about business activities and services. '*12


@pytest.fixture
def counts(monkeypatch):
    original=rarity.load()
    table={**original,'counts':{'phone':{'12345678':1,'87654321':2},'email':{'post@example.no':1,'post@gmail.com':2},'domain':{'example.no':2},'name':{}}}
    monkeypatch.setattr(rarity,'load',lambda:table)
    return table['counts']


def prove(markup,**ctx):
    p=Page(f'<title>Example AS</title><main>{FILL}</main>{markup}'.encode(),'https://example.no/')
    context={'name':'Example AS','phone':'12345678','email':'post@example.no','candidate_url':'https://example.no/',**ctx}
    return candidate_proof(p,ORG,context,Candidate('https://example.no/','example.no','registry_email'),[])


@pytest.mark.parametrize('markup,context,kind',[
    ('<footer>Telefon +47 12 34 56 78</footer>',{},'phone'),
    ('<footer>Telefon 87654321</footer>',{'phone':None,'mobile':'+47 87654321'},'phone'),
    ('<footer>post@example.no</footer>',{},'email'),
    ('<footer>Contact: post@example.no.</footer>',{},'email'),
    ('<address>Adresse Oslo; post@example.no</address>',{},'email'),
    ('<footer>other@example.no</footer>',{},'domain'),
    ('<footer>example.no</footer>',{},'domain'),
    ('<footer>post@gmail.com</footer>',{'email':'post@gmail.com'},'email'),
])
def test_exact_rare_registry_contact_in_own_publisher_block(counts,markup,context,kind):
    proof=prove(markup,**context)
    assert proof.level=='HIGH' and proof.proof_type==RARE
    assert proof.publisher_receipt['contact']['kind']==kind
    assert 1<=proof.publisher_receipt['contact']['rarity_count']<=2


@pytest.mark.parametrize('markup',[
    '<p>Telefon 12345678; post@example.no</p>',
    '<header>Telefon 12345678; post@example.no</header>',
    '<footer><section class="staff">Telefon 12345678; post@example.no</section></footer>',
    '<footer><div><h2>Våre ansatte</h2>Telefon 12345678; post@example.no</div></footer>',
    '<footer><div class="partners">Telefon 12345678; post@example.no</div></footer>',
    '<footer><article>Telefon 12345678; post@example.no</article></footer>',
    '<footer>Levert av <a>Telefon 12345678; post@example.no</a></footer>',
    '<footer hidden>Telefon 12345678; post@example.no</footer>',
    '<footer>0123456789; post@other-example.no</footer>',
])
def test_contact_in_staff_body_header_article_partner_or_agency_context_cannot_count(counts,markup):
    assert prove(markup).proof_type!=RARE


@pytest.mark.parametrize('frequency',[0,3,4,5])
def test_absent_or_shared_contact_abstains(counts,frequency):
    counts['phone']['12345678']=frequency
    assert prove('<footer>Telefon 12345678</footer>',email=None).proof_type!=RARE


def test_name_repetition_is_one_group_and_suffix_required(counts):
    assert prove('<footer>Example AS Example AS Example AS</footer>').proof_type!=RARE
    p=Page(f'<title>Example</title><main>{FILL}</main><footer>Example; Telefon 12345678</footer>'.encode(),'https://example.no/')
    assert not rare_receipt(p,ORG,{'name':'Example AS','phone':'12345678'})


def test_domain_only_requires_exact_own_registrable_domain(counts):
    assert prove('<footer>other@example.no.evil.no</footer>').proof_type!=RARE
    assert prove('<footer>other@notexample.no</footer>').proof_type!=RARE
    counts['domain']['other.no']=1
    assert prove('<footer>new@other.no</footer>',email='post@other.no').proof_type!=RARE
    counts['domain']['mail.example.no']=1
    assert prove('<footer>new@mail.example.no</footer>',email='post@mail.example.no').proof_type!=RARE


def test_foreign_number_and_group_override_name_and_rare_contact(counts):
    assert prove('<footer>Example AS Telefon 12345678; Org.nr 993578843</footer>').level=='REJECT'
    assert prove('<footer>Example AS Telefon 12345678; Part of Example Group</footer>').level=='REJECT'


def test_missing_or_broken_table_never_causes_network_or_publication(monkeypatch):
    def broken():raise OSError('local table unavailable')
    monkeypatch.setattr(rarity,'load',broken)
    assert prove('<footer>Telefon 12345678</footer>').proof_type!=RARE


def test_production_publication_and_verifier_real_bundled_counts(tmp_path,monkeypatch):
    import json
    from tests.test_websites import execute_web,html
    from tests.test_registry import entity
    from scripts.verify_output import verify
    # Use an actual unique table key while keeping exact registry fields in our
    # authored fixture. This is an offline fixture, not a claimed real company.
    phone=next(k for k,v in rarity.load()['counts']['phone'].items() if v==1)
    import tests.test_websites as web
    original=web.entity
    def record(org):
        value=original(org);value['telefon']=phone;value['hjemmeside']=None
        return value
    monkeypatch.setattr(web,'entity',record)
    # execute_web overwrites the phone; set its registered mobile as the exact
    # rare source input instead, and discover through the registry email.
    def mobile_record(org):
        value=record(org);value['mobil']=phone;value['epostadresse']='post@example.no';return value
    monkeypatch.setattr(web,'entity',mobile_record)
    _,row,_,cfg=execute_web(tmp_path,monkeypatch,body=html('Example AS; Telefon '+phone),website=None)
    site=next(c for c in row['claims'] if c['field']=='official_website')
    assert site['value']['proof_type']==RARE and site['value']['publisher_identity']['contact']['registry_field']=='mobile'
    verify(cfg.output,cfg.state_dir,1)
    site['value']['publisher_identity']['contact']['rarity_count']=2
    cfg.output.write_text(json.dumps(row)+'\n',encoding='utf8')
    with pytest.raises(AssertionError):verify(cfg.output,cfg.state_dir,1)
