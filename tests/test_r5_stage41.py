import asyncio
import httpx
import pytest
from signalpost.budget import SourceFailure
from signalpost.web import policy
from signalpost.web.candidates import Candidate
from signalpost.web.fetcher import WebsiteHttp
from signalpost.web.html import Page
from signalpost.web.proof import score
from signalpost.web.collector import proof_page_targets
from tests.test_websites import html, OUR, execute_web


def test_dns_fallback_checks_other_hostname_without_raising_caps(tmp_path, monkeypatch):
    calls=[]
    async def resolve(host, port=443):
        calls.append(host)
        if host=='example.no': raise SourceFailure('no_such_domain')
        return ['93.184.216.34']
    monkeypatch.setattr(policy,'resolve_public',resolve)
    # Test the candidate layer directly; registry-origin candidates intentionally
    # skip nomination prechecks but still undergo request-time DNS checks.
    from tests.test_registry import config
    from signalpost.budget import Budget
    from signalpost.sources.blobstore import BlobStore
    cfg=config(tmp_path,[OUR])
    async def go():
        async with httpx.AsyncClient() as client:
            fetcher=WebsiteHttp(client,cfg,Budget(cfg),BlobStore(tmp_path))
            async def get(url,*args):
                assert url.startswith('https://www.example.no/')
                return type('Response',(),{'status':200})()
            fetcher.get=get
            await fetcher.candidate(Candidate('http://example.no/','example.no','registry_email'),OUR)
            assert fetcher.dns_counts[OUR]==2
    asyncio.run(go())
    assert calls==['example.no','www.example.no']


@pytest.mark.parametrize('host',['amazon.com','etsy.com','proff.no','finn.no'])
def test_directory_marketplace_veto_even_with_number(host):
    with pytest.raises(SourceFailure): policy.validate_url('https://'+host+'/',{host})


def test_group_requires_exact_number_and_parked_veto_wins():
    page=Page(html('Example gate 1',extra='Our companies',title='Example AS').encode(),'https://example.no/')
    assert score(page,OUR,{'name':'Example AS','street':['Example gate 1']},'registry_website',[]).reason=='group_without_exact_orgnr'
    page=Page(html('Org nr '+OUR,extra='This domain is for sale').encode(),'https://example.no/')
    assert score(page,OUR,{},'registry_website',[]).reason=='parked'


def test_proof_pages_do_not_spend_html_budget_on_pdf():
    page=Page(html('',extra='<a href="/privacy.pdf">Privacy</a><a href="/kontakt">Contact</a>').encode(),'https://example.no/')
    assert not any('.pdf' in u for u in proof_page_targets(page,page.url))


def test_collector_does_not_fetch_sitemap_or_rss_candidates(tmp_path,monkeypatch):
    _,_,urls,_=execute_web(tmp_path,monkeypatch,body=html('No identifier here',title='Unrelated'))
    assert not any(p in url for url in urls for p in ('sitemap.xml','feed.xml','rss.xml','/feed/'))
