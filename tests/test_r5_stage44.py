import json
import pytest
import httpx
from signalpost.web.html import Page
from signalpost.web.proof import score, orgnrs
from signalpost.web.collector import proof_page_targets
from tests.test_websites import OUR, html, execute_web


@pytest.mark.parametrize('value',['NO923609016MVA','923.609.016 MVA','923 609 016','no 923609016 mva'])
def test_explicit_org_formats(value):
    assert orgnrs(value)=={OUR}
    page=Page(html('Org.nr '+value).encode(),'https://example.no/')
    assert score(page,OUR,{},'legal_name_slug',[]).level=='VERIFIED'
    assert page.proof_span(OUR) in page.raw


@pytest.mark.parametrize('key',['orgnr','organisation_number','vatID'])
def test_explicit_meta_identifier_can_prove_entity(key):
    page=Page(html('',extra=f'<meta name="{key}" content="NO{OUR}MVA">').encode(),'https://example.no/')
    assert score(page,OUR,{},'legal_name_slug',[]).level=='VERIFIED'


@pytest.mark.parametrize('body',[
    {'@type':['Person','Organization'],'vatID':OUR},
    {'@type':'WebPage','about':{'@type':'Organization','vatID':OUR}},
    {'@type':'Organization','customer':{'@type':'Organization','vatID':OUR}},
    {'@type':'Organization','identifier':{'propertyID':'ISBN','value':OUR}},
])
def test_unrelated_jsonld_never_establishes_owner(body):
    page=Page(html('',extra='<script type="application/ld+json">'+json.dumps(body)+'</script>').encode(),'https://example.no/')
    assert score(page,OUR,{},'legal_name_slug',[]).level!='VERIFIED'


def test_generic_seo_metadata_is_not_company_proof():
    page=Page(html('',extra=f'<meta name="description" content="Customer {OUR}">').encode(),'https://example.no/')
    assert score(page,OUR,{},'legal_name_slug',[]).level!='VERIFIED'


@pytest.mark.parametrize('value',['1 923609016','1.923609016','923609016.0','NO1923609016MVA'])
def test_long_numeric_run_never_yields_a_company_suffix(value):
    assert not orgnrs(value)


def test_contact_about_privacy_priority_fits_original_cap(tmp_path,monkeypatch):
    def response(request):
        if request.url.path=='/robots.txt':return httpx.Response(200,text='User-agent: *\nAllow: /')
        if request.url.path=='/personvern':return httpx.Response(200,text=html('Org.nr '+OUR))
        if request.url.path=='/':return httpx.Response(200,text=html('',title='Unrelated'))
        return httpx.Response(404,text='missing')
    report,row,urls,_=execute_web(tmp_path,monkeypatch,response=response)
    claim=next(c for c in row['claims'] if c['field']=='official_website')
    assert claim['value']['proof_page_url'].endswith('/personvern')
    # One additional metered filing-year lookup; proof HTTP cap is unchanged.
    assert report['max_requests_per_company']<=10
    assert not any('sitemap' in u for u in urls)
