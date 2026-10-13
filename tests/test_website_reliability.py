import asyncio
import socket
import httpx
import pytest
from signalpost.web.proof import score
from signalpost.web.html import Page
from signalpost.web.collector import followup_links
from signalpost.web import policy
from signalpost.budget import SourceFailure
from tests.test_websites import execute_web, html, OUR, OTHER


def test_registry_declared_is_not_available_to_guesses():
    body=html('Distinctive street 12',title='Distinctive Services')
    context={'name':'Distinctive Enterprise AS','street':['Distinctive street 12']}
    proof=score(Page(body.encode(),'https://example.no/'),OUR,context,'registry_website',[])
    assert proof.level=='REGISTRY_DECLARED' and proof.proof_type=='registry_declared_live'
    assert score(Page(body.encode(),'https://example.no/'),OUR,context,'registry_email',[]).level!='REGISTRY_DECLARED'
    assert score(Page(html('Org.nr '+OTHER,title='Distinctive').encode(),'https://example.no/'),OUR,context,'registry_website',[]).level=='REJECT'
    assert score(Page(html('',title='Holding').encode(),'https://example.no/'),OUR,{'name':'Holding AS'},'registry_website',[]).level!='REGISTRY_DECLARED'
    assert score(Page(html('',title='Distinctive Services').encode(),'https://example.no/'),OUR,context,'registry_website',[]).level!='REGISTRY_DECLARED'


def test_postcode_city_cannot_prove_a_different_group_company():
    body=html('5353 Straume',title='Sartor Holding')
    context={'name':'Sartor Utvikling AS','street':['Different road 11'],'postcode':'5353','city':'STRAUME'}
    assert score(Page(body.encode(),'https://group.no/'),OUR,context,'registry_website',[]).level!='REGISTRY_DECLARED'


def test_unicode_line_separator_does_not_mislocalize_orgnr():
    body='<script>const text="line\u2028separator";</script>' + html('Org.nr 923609016')
    page=Page(body.encode(),'https://example.no/')
    span=page.proof_span(OUR)
    assert span in page.raw and OUR in span


def test_followup_priority_and_no_captcha_form_false_block():
    page=Page(html('',extra='<a href="/privacy">Privacy</a><a href="/about">About</a><a href="/contact">Contact</a>').encode(),'https://example.no/')
    assert followup_links(page)==['https://example.no/contact','https://example.no/about','https://example.no/privacy']
    page=Page(html('',extra='<script src="recaptcha.js"></script>'+('Services and company facts. '*70)).encode(),'https://example.no/')
    assert score(page,OUR,{'name':'Example AS'},'registry_website',[]).level!='BLOCKED'


def test_www_connect_fallback_and_http_only_after_connection_failure(tmp_path,monkeypatch):
    def response(request):
        if request.url.host not in {'example.no','www.example.no'}: return httpx.Response(404,text='missing')
        if request.url.scheme=='https' and request.url.host=='example.no':
            raise httpx.ConnectError('TLS failed',request=request)
        return httpx.Response(200,text='User-agent: *\nAllow: /' if request.url.path=='/robots.txt' else html())
    report,row,requests,_=execute_web(tmp_path,monkeypatch,response=response)
    assert next(c for c in row['claims'] if c['field']=='official_website')['value']['final_url']=='https://www.example.no'
    assert not any(url.startswith('http://') for url in requests)
    assert report['max_requests_per_company']<=9


def test_plaintext_fallback_and_registry_timeout_retry(tmp_path,monkeypatch):
    def response(request):
        if request.url.host not in {'example.no','www.example.no'}: return httpx.Response(404,text='missing')
        if request.url.scheme=='https':raise httpx.ConnectError('TLS failed',request=request)
        return httpx.Response(200,text='User-agent: *\nAllow: /' if request.url.path=='/robots.txt' else html())
    _,row,requests,_=execute_web(tmp_path/'http',monkeypatch,response=response)
    assert next(c for c in row['claims'] if c['field']=='official_website')['value']['final_url']=='http://example.no'
    counts=0
    def once(request):
        nonlocal counts
        if request.url.host!='example.no': return httpx.Response(404,text='missing')
        if request.url.path=='/robots.txt':
            counts+=1
            if counts==1:raise httpx.ReadTimeout('timeout',request=request)
            return httpx.Response(200,text='User-agent: *\nAllow: /')
        return httpx.Response(200,text=html())
    _,row,_,_=execute_web(tmp_path/'retry',monkeypatch,response=once)
    assert counts==2 and any(c['field']=='official_website' for c in row['claims'])


def test_dns_nxdomain_is_distinct(monkeypatch):
    async def execute():
        loop=asyncio.get_running_loop()
        async def absent(*args,**kwargs):raise socket.gaierror(socket.EAI_NONAME,'absent')
        monkeypatch.setattr(loop,'getaddrinfo',absent)
        with pytest.raises(SourceFailure) as error:await policy.resolve_public('absent.no')
        assert error.value.code=='no_such_domain'
    asyncio.run(execute())


def test_optional_block_page_is_not_contact_evidence(tmp_path,monkeypatch):
    def response(request):
        if request.url.path=='/robots.txt':return httpx.Response(200,text='User-agent: *\nAllow: /')
        if request.url.path=='/contact':return httpx.Response(200,text=html('',extra='verify you are human <footer><a href="mailto:fake@example.no">Fake</a></footer>'))
        return httpx.Response(200,text=html('',extra='<a href="/contact">Contact</a><footer>Example gate 1</footer>'))
    _,row,_,_=execute_web(tmp_path,monkeypatch,response=response)
    assert not any(c['value']=='fake@example.no' for c in row['claims'])
