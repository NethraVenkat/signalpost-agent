import asyncio
import httpx
import pytest
from signalpost.budget import Budget, SourceFailure
from signalpost.sources.blobstore import BlobStore
from signalpost.web.fetcher import WebsiteHttp
from signalpost.web.candidates import Candidate, generate
from tests.test_registry import config
from tests.test_websites import OUR, OTHER, execute_web, html


@pytest.mark.parametrize('status', [404, 410, 500])
def test_http_response_does_not_authorize_second_hostname(tmp_path, monkeypatch, status):
    def response(request):
        return httpx.Response(status, text='missing')
    _, _, urls, _ = execute_web(tmp_path, monkeypatch, response=response)
    assert not any('www.example.no' in url for url in urls)


def test_exact_proof_stops_candidate_and_proof_page_work(tmp_path, monkeypatch):
    _, row, urls, _ = execute_web(tmp_path, monkeypatch, body=html(extra='<a href="/contact">Contact</a>'))
    assert any(c['field'] == 'official_website' for c in row['claims'])
    assert not any('/contact' in url for url in urls)


def test_shared_page_reused_but_domain_veto_precedes_all_work(tmp_path):
    cfg = config(tmp_path, [OUR, OTHER])
    calls = []
    async def go():
        async with httpx.AsyncClient() as client:
            fetcher = WebsiteHttp(client, cfg, Budget(cfg), BlobStore(tmp_path))
            async def raw(url, *args, **kwargs):
                calls.append(url)
                return object()
            fetcher.raw = raw
            first, second = await asyncio.gather(
                fetcher.get('https://example.no/', OUR, 'example.no'),
                fetcher.get('https://example.no/', OTHER, 'example.no'))
            assert first is second
            with pytest.raises(SourceFailure):
                await fetcher.candidate(Candidate('https://proff.no/', 'proff.no', 'legal_name_slug'), OUR)
            assert not fetcher.dns_counts
    asyncio.run(go())
    assert calls == ['https://example.no/']


def test_registry_fields_precede_variants():
    candidates = generate({'name': 'Example AS', 'website': 'registered.no', 'email': 'a@email.no'})
    assert [c.origin for c in candidates[:2]] == ['registry_website', 'registry_email']


def test_full_name_precedes_subunit_provider_contact():
    candidates = generate({'name': 'Spedify AS', 'subunits': [
        {'orgnr': OTHER, 'name': 'Spedify Workshop', 'email': 'a@provider.no'}]})
    domains = [c.domain for c in candidates]
    assert domains.index('spedify.no') < domains.index('provider.no')


def test_proof_page_veto_stops_remaining_requests(tmp_path, monkeypatch):
    def response(request):
        if request.url.path == '/robots.txt': return httpx.Response(200, text='User-agent: *\nAllow: /')
        if request.url.path == '/': return httpx.Response(200, text=html('', title='Unrelated'))
        return httpx.Response(200, text=html('Org nr '+OTHER, title='Unrelated'))
    _, row, urls, _ = execute_web(tmp_path, monkeypatch, response=response)
    assert not any(c['field'] == 'official_website' for c in row['claims'])
    assert sum(url.startswith('https://example.no/') for url in urls) == 3
