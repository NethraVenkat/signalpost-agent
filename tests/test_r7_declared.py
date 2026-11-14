import pytest
from signalpost.web.html import Page
from signalpost.web.reach_identity import declared_live,DECLARED_LIVE
from signalpost.web.collector import candidate_proof
from signalpost.web.candidates import Candidate

ORG='923609016'
def page(markup,url='https://example.no/'):
    return Page(('<main>'+'Useful company services and contact information. '*20+'</main>'+markup).encode(),url)

def context(**changes):
    return {'name':'Unrelated AS','website':'example.no','candidate_url':'https://example.no/','phone':'22334455','email':'post@example.no','street':'Eksempelgata 12','postcode':'0123','city':'Oslo',**changes}

@pytest.mark.parametrize('markup',['<footer>Telefon: 22 33 44 55</footer>','<footer>post@example.no</footer>','<footer>Eksempelgata 12</footer>','<footer>0123 Oslo</footer>'])
def test_declared_live_one_exact_publisher_owner_signal(markup):
    p=page(markup);c=context()
    assert declared_live(p,ORG,c)['tier']==DECLARED_LIVE
    assert candidate_proof(p,ORG,c,Candidate(p.url,'example.no','registry_website'),[]).proof_type==DECLARED_LIVE

@pytest.mark.parametrize('markup',['<p>22 33 44 55 post@example.no Eksempelgata 12 0123 Oslo</p>','<footer hidden>post@example.no</footer>','<article><footer>post@example.no</footer></article>','<footer>Org.nr 993578843 post@example.no</footer>','<footer>Example Other AS post@example.no</footer>','<footer>Under construction post@example.no</footer>','<footer>Levert av <a>post@example.no</a></footer>'])
def test_no_body_hidden_article_foreign_other_publisher_placeholder_or_agency(markup):
    assert declared_live(page(markup),ORG,context()) is None

@pytest.mark.parametrize('changes',[{'candidate_url':'https://other.no/'},{'website':None},{'phone':'22334456','email':None,'street':None,'postcode':None}])
def test_declared_nomination_and_exact_signal_required(changes):
    assert declared_live(page('<footer>22 33 44 55</footer>'),ORG,context(**changes)) is None

def test_declared_cross_domain_and_short_shell_rejected():
    assert declared_live(page('<footer>post@example.no</footer>',url='https://other.no'),ORG,context()) is None
    assert declared_live(Page(b'<footer>post@example.no</footer>','https://example.no'),ORG,context()) is None

def test_shared_contacts_under_different_publisher_not_owner():
    assert declared_live(page('<footer>Example Broadband AS 22 33 44 55 Eksempelgata 12 0123 Oslo</footer>'),ORG,context(name='Example Holding AS')) is None

def test_unmarked_staff_contact_page_is_not_contact_owner_signal():
    p=page('<p>Our staff</p><div>Email: person@example.no</div>',url='https://example.no/contact')
    assert declared_live(p,ORG,context(email='person@example.no',phone=None,street=None,postcode=None)) is None

@pytest.mark.parametrize('declared',['https://example.no/company/us','https://example.no/firmaer/profile/'])
def test_declared_deep_profile_path_cannot_qualify(declared):
    assert declared_live(page('<footer>post@example.no</footer>'),ORG,context(website=declared,candidate_url=declared)) is None

@pytest.mark.parametrize('markup',['<meta property="og:site_name" content="Regional Portal"><footer>post@example.no</footer>','<div class="logo">Regional Portal</div><footer>post@example.no</footer>','<footer>Copyright Regional Portal post@example.no</footer>','<header>Find businesses</header><footer>post@example.no</footer>'])
def test_other_site_owner_or_portal_cannot_qualify(markup):
    assert declared_live(page(markup),ORG,context()) is None

@pytest.mark.parametrize('markup',['<footer>Daglig leder Person Test post@example.no 22 33 44 55</footer>','<address>John Smith Email: post@example.no</address>'])
def test_person_contacts_do_not_count_even_company_email(markup):
    assert declared_live(page(markup),ORG,context(street=None,postcode=None)) is None

def test_declared_live_publication_replays_registry_and_publisher(tmp_path,monkeypatch):
    import json
    from tests.test_websites import execute_web,FILL
    from scripts.verify_output import verify
    body='<html><header>Welcome</header><main>'+FILL+'</main><footer>Telefon: 12345678</footer></html>'
    _,row,_,cfg=execute_web(tmp_path,monkeypatch,body=body)
    claim=next(c for c in row['claims'] if c['field']=='official_website')
    assert claim['value']['proof_type']==DECLARED_LIVE
    verify(cfg.output,cfg.state_dir,1)
    claim['value']['publisher_identity']['owner_signal']['normalized_value']='87654321'
    cfg.output.write_text(json.dumps(row)+'\n',encoding='utf8')
    with pytest.raises(AssertionError):verify(cfg.output,cfg.state_dir,1)
