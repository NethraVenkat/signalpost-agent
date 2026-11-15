import pytest,httpx
from signalpost.web.html import Page
from signalpost.web.legal_pages import legal_links,is_legal
from signalpost.web.collector import followup_links,proof_page_targets
from signalpost.web.proof_sitemaps import parse
from tests.test_websites import execute_web,html,OUR,OTHER

@pytest.mark.parametrize('term',['salgsbetingelser','kjopsbetingelser','kjopsvilkar','handelsbetingelser','vilkar','betingelser','personvern','personvernerklaering','cookies','angrerett','impressum','juridisk','om-nettstedet','terms','privacy','conditions'])
def test_requested_legal_page_vocabulary(term):assert is_legal('/'+term)

def test_own_footer_legal_first_no_foreign_article_pdf_or_hidden():
    p=Page(html('',extra='<footer><a href="/contact">Contact</a><a href="/salgsbetingelser">Terms</a><a href="https://foreign.no/privacy">Privacy</a><a href="/vilkar.pdf">Terms PDF</a><a hidden href="/secret-terms">Terms</a></footer><article><a href="/article-terms">Terms</a></article>').encode(),'https://example.no/')
    assert legal_links(p)==['https://example.no/salgsbetingelser']
    assert followup_links(p)[0].endswith('/salgsbetingelser')
    assert legal_links(p,pdf=True)==['https://example.no/vilkar.pdf']
    assert not any('.pdf' in u for u in proof_page_targets(p,p.url))

def test_sitemap_legal_prioritisation_is_same_site_and_bounded():
    xml=b'<urlset><url><loc>https://example.no/about</loc></url><url><loc>https://example.no/salgsbetingelser</loc></url><url><loc>https://example.no/news/terms</loc></url><url><loc>https://other.no/terms</loc></url></urlset>'
    pages,_=parse(xml,'https://example.no/sitemap.xml','https://example.no/')
    assert pages==['https://example.no/salgsbetingelser','https://example.no/about']

@pytest.mark.parametrize('owner,accepted',[(OUR,True),(OTHER,False)])
def test_own_linked_legal_page_exact_number_and_conflict(tmp_path,monkeypatch,owner,accepted):
    def response(req):
        if req.url.path=='/robots.txt':return httpx.Response(200,text='User-agent: *\nAllow: /')
        if req.url.path=='/salgsbetingelser':return httpx.Response(200,text=html('Org.nr '+owner,title='Terms'))
        return httpx.Response(200,text=html('',extra='<footer><a href="/contact">Contact</a><a href="/salgsbetingelser">Terms</a></footer>',title='Services'))
    report,row,urls,_=execute_web(tmp_path,monkeypatch,response=response,website=None)
    sites=[c for c in row['claims'] if c['field']=='official_website' and c['availability']=='available']
    assert bool(sites)==accepted
    if accepted:
        assert sites[0]['value']['identity_level']=='VERIFIED'
        assert sites[0]['value']['proof_page_url'].endswith('/salgsbetingelser')
        assert sum(u.endswith('/contact') for u in urls)==1
        assert next(n for n,u in enumerate(urls) if u.endswith('/salgsbetingelser'))<next(n for n,u in enumerate(urls) if u.endswith('/contact'))
        assert row['run']['refresh']['owner_social']['checked_urls']==['https://example.no/contact']
    else:
        assert not any(u.endswith('/contact') for u in urls)
    assert report['max_requests_per_company']<=13

def test_new_legal_page_cannot_substitute_name_or_contact_for_exact_number(tmp_path,monkeypatch):
    from signalpost.web import rarity
    data=rarity.load();monkeypatch.setattr(rarity,'load',lambda:{**data,'counts':{**data['counts'],'phone':{'12345678':1}}})
    def response(req):
        if req.url.path=='/robots.txt':return httpx.Response(200,text='User-agent: *\nAllow: /')
        if req.url.path=='/salgsbetingelser':return httpx.Response(200,text=html('Example AS Telefon: 12345678',title='Example AS'))
        return httpx.Response(200,text=html('',extra='<footer><a href="/salgsbetingelser">Terms</a></footer>',title='Services'))
    _,row,_,_=execute_web(tmp_path,monkeypatch,response=response,website=None)
    assert not any(c['field']=='official_website' and c['availability']=='available' for c in row['claims'])
