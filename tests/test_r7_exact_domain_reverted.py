from signalpost.web.html import Page
from signalpost.web.candidates import Candidate
from signalpost.web.collector import candidate_proof
from signalpost.web import rarity

def test_full_name_exact_domain_and_norwegian_lang_do_not_prove_template(monkeypatch):
    d=rarity.load();monkeypatch.setattr(rarity,'load',lambda:{**d,'counts':{**d['counts'],'name':{'example invest':1}}})
    p=Page(('<html lang="nb"><head><title>Example Invest AS</title></head><main>FREE PSD TEMPLATE POWERFUL ONE PAGE THEME '+('Lorem ipsum dolor sit amet. '*30)+'OUR TEAM KEVIN PERRY Tel: 123456789 admin@domain.com</main><footer>Designed by MageeWP Themes</footer></html>').encode(),'https://example-invest.no/')
    proof=candidate_proof(p,'923609016',{'name':'Example Invest AS'},Candidate(p.url,'example-invest.no','legal_name_slug'),[])
    assert proof.level not in {'HIGH','VERIFIED'}

def test_stock_theme_is_vetoed_before_any_existing_declared_name_tier():
    p=Page(('<html><head><title>Example Invest AS</title></head><main>'+('Lorem ipsum dolor sit amet. '*5)+'FREE PSD TEMPLATE admin@domain.com KEVIN PERRY</main></html>').encode(),'https://example-invest.no/')
    proof=candidate_proof(p,'923609016',{'name':'Example Invest AS','website':p.url},Candidate(p.url,'example-invest.no','registry_website'),[])
    assert proof.level=='REJECT' and proof.reason=='publisher_placeholder'

def test_isolated_template_text_does_not_veto_real_company_content():
    from signalpost.web.publisher_veto import conflict
    p=Page(('<header>Example AS</header><main>'+('Real company services. '*30)+'<section>Testimonials Lorem ipsum dolor sit amet.</section></main><footer>Example AS Org.nr 923609016</footer>').encode(),'https://example.no/')
    assert conflict(p,'923609016',{'name':'Example AS'})[0] is None
