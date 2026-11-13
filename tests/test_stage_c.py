import asyncio
from types import SimpleNamespace
import httpx,pytest
from signalpost.web.proof_sitemaps import parse,discover
from signalpost.web.html import Page
from signalpost.web.proof import score
from signalpost.web.activity import parse as activity_parse
from tests.test_websites import execute_web,html,OUR


def test_maps_only_nominate_two_own_proof_pages():
    urls=['https://example.no/news/contact','https://evil.no/contact','https://example.no/privacy.pdf',
          'https://example.no/legal/personvern','https://example.no/contact-us','https://example.no/about','https://example.no/products/contact?x=1']
    xml='<urlset>'+''.join('<url><loc>'+u+'</loc></url>' for u in urls)+'</urlset>'
    assert parse(xml.encode(),'https://example.no/sitemap.xml','https://example.no/')[0]==urls[3:5]
    assert activity_parse(xml.encode(),'https://example.no/sitemap.xml',None)==([],[])
    with pytest.raises(ValueError):parse(b'<!DOCTYPE x><urlset/>','https://example.no/sitemap.xml','https://example.no/')


@pytest.mark.parametrize('title,extra',[('Just a moment','<script src="/cdn-cgi/challenge-platform/x"></script>'),
    ('Access Denied','<p>Request unsuccessful - Imperva</p>'),('Security verification','<script src="https://captcha-delivery.com/x"></script>')])
def test_challenges_are_blocked_even_with_identifier(title,extra):
    page=Page(html('Org nr '+OUR,extra=extra,title=title).encode(),'https://example.no/')
    assert score(page,OUR,{'name':'Example AS'},'registry_website',[]).level=='BLOCKED'


def test_recaptcha_contact_form_is_not_a_challenge():
    page=Page(html(extra='<form>Contact us <div class="g-recaptcha"></div></form>').encode(),'https://example.no/')
    assert score(page,OUR,{'name':'Example AS'},'registry_website',[]).level=='VERIFIED'


def test_passive_cloudflare_jsd_is_not_an_interactive_gate(tmp_path,monkeypatch):
    body=html(extra='<script src="/cdn-cgi/challenge-platform/scripts/jsd/main.js?ray=test"></script><script src="https://static.cloudflareinsights.com/beacon.min.js"></script>')
    assert score(Page(body.encode(),'https://example.no/'),OUR,{'name':'Example AS'},'registry_website',[]).level=='VERIFIED'
    _,row,_,_=execute_web(tmp_path,monkeypatch,body=body)
    assert any(c['field']=='official_website' and c['availability']=='available' for c in row['claims'])


def test_jsd_does_not_hide_a_visible_cloudflare_access_gate():
    body=html(extra='<script src="/cdn-cgi/challenge-platform/scripts/jsd/main.js"></script><p>Cloudflare - Enable JavaScript and cookies</p>',title='Just a moment')
    assert score(Page(body.encode(),'https://example.no/'),OUR,{'name':'Example AS'},'registry_website',[]).level=='BLOCKED'


@pytest.mark.parametrize('status',[200,403,503])
def test_transport_detects_challenges_before_http_retry_or_fallback(tmp_path,monkeypatch,status):
    def response(request):
        if request.url.path=='/robots.txt':return httpx.Response(200,text='User-agent: *\nAllow: /')
        return httpx.Response(status,text=html(extra='<script src="/cdn-cgi/challenge-platform/x"></script>',title='Just a moment'))
    report,row,urls,_=execute_web(tmp_path,monkeypatch,response=response)
    assert row['run']['sections']['website']=='blocked'
    assert any(e['code']=='block_page' for e in row['errors'])
    assert len([u for u in urls if u.startswith('https://example.no/')])==2
    assert all(sum(u==url for u in urls)==1 for url in urls if 'data.brreg.no' not in url)
    assert not any('/sitemap' in u or 'www.example' in u for u in urls)


def test_hidden_sitemap_privacy_proves_exact_number_within_existing_cap(tmp_path,monkeypatch):
    def response(request):
        if request.url.path=='/robots.txt':return httpx.Response(200,text='User-agent: *\nAllow: /\nSitemap: https://example.no/pages.xml')
        if request.url.path=='/pages.xml':return httpx.Response(200,text='<urlset><url><loc>https://example.no/legal/privacy</loc></url><url><loc>https://example.no/news/update</loc></url></urlset>',headers={'content-type':'application/xml'})
        if request.url.path=='/legal/privacy':return httpx.Response(200,text=html('Org nr '+OUR))
        return httpx.Response(200,text=html('',title='Unrelated'))
    report,row,urls,_=execute_web(tmp_path,monkeypatch,response=response)
    claim=next(c for c in row['claims'] if c['field']=='official_website' and c['availability']=='available')
    assert claim['value']['identity_level']=='VERIFIED' and claim['value']['proof_page_url'].endswith('/legal/privacy')
    assert not any('/news/' in u or u.endswith('/kontakt') for u in urls)
    assert len([u for u in urls if 'data.brreg.no' not in u])==4
    assert report['max_requests_per_company']<=13


def test_challenged_followup_stops_guesses_and_reports_blocked(tmp_path,monkeypatch):
    def response(request):
        if request.url.path=='/robots.txt':return httpx.Response(200,text='User-agent: *\nAllow: /')
        if request.url.path=='/contact':return httpx.Response(200,text=html(extra='Cloudflare checking your browser',title='Just a moment'))
        return httpx.Response(200,text=html('',extra='<footer><a href="/contact">Contact</a></footer>',title='Unrelated'))
    _,row,urls,_=execute_web(tmp_path,monkeypatch,response=response)
    assert row['run']['sections']['website']=='blocked'
    assert any(e['code']=='block_page' for e in row['errors'])
    assert not any('/sitemap' in u or '/personvern' in u for u in urls)


def test_sitemap_robots_and_budget_never_bypassed(tmp_path,monkeypatch):
    def response(request):
        if request.url.path=='/robots.txt':return httpx.Response(200,text='User-agent: *\nDisallow: /sitemap.xml')
        return httpx.Response(200,text=html('',title='Unrelated'))
    _,row,urls,_=execute_web(tmp_path/'robots',monkeypatch,response=response)
    assert not any('/sitemap.xml' in u for u in urls)
    assert row['run']['sections']['website']=='blocked'
    _,row,urls,_=execute_web(tmp_path/'budget',monkeypatch,body=html('',title='Unrelated'),website_request_cap=2)
    assert len([u for u in urls if 'data.brreg.no' not in u])==2


def test_sitemap_index_depth_and_two_page_quota_across_candidates():
    class Http:
        robots={};calls=[]
        async def get(self,url,*args,**kw):
            self.calls.append(url)
            body=b'<sitemapindex><sitemap><loc>https://example.no/pages.xml</loc></sitemap><sitemap><loc>https://example.no/news.xml</loc></sitemap></sitemapindex>' if url.endswith('sitemap.xml') else b'<urlset><url><loc>https://example.no/contact</loc></url><url><loc>https://example.no/privacy</loc></url></urlset>'
            return SimpleNamespace(body=body,url=url,status=200)
    http=Http();targets=asyncio.run(discover(OUR,http,'https://example.no/',set()))
    assert len(targets)==2 and len(http.calls)==2
    assert asyncio.run(discover(OUR,http,'https://example.no/',set()))==[] and len(http.calls)==2
