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
    assert sum(url.startswith('https://example.no/') for url in urls) == 4  # robots, home, map, vetoing proof page
    assert not any('/personvern' in url or '/om-oss' in url for url in urls)


def test_cached_dns_does_not_charge_another_company_at_its_nomination_limit(tmp_path):
    cfg = config(tmp_path, [OUR, OTHER])
    calls = []
    async def resolve(host, port):
        calls.append(host)
        return ['93.184.216.34']
    async def go():
        async with httpx.AsyncClient() as client:
            fetcher = WebsiteHttp(client, cfg, Budget(cfg), BlobStore(tmp_path), resolver=resolve)
            candidate = Candidate('https://cached.no/', 'cached.no', 'legal_name_slug')
            await fetcher.precheck(candidate, OUR)
            fetcher.dns_counts[OTHER] = 8
            await fetcher.precheck(candidate, OTHER)
            assert fetcher.dns_counts == {OUR: 1, OTHER: 8}
            with pytest.raises(SourceFailure):
                await fetcher.precheck(Candidate('https://new.no/', 'new.no', 'legal_name_slug'), OTHER)
            assert not fetcher.budget.events
    asyncio.run(go())
    assert calls == ['cached.no']


def test_activity_allowance_cannot_exceed_absolute_eight_request_ceiling(tmp_path):
    cfg = config(tmp_path, [OUR], website_request_cap=8, website_total_request_cap=13)
    async def resolve(host, port): return ['93.184.216.34']
    async def go():
        async with httpx.AsyncClient() as client:
            fetcher = WebsiteHttp(client, cfg, Budget(cfg), BlobStore(tmp_path), resolver=resolve)
            fetcher.counts[OUR] = 8
            fetcher.activity_extra.add(OUR)
            with pytest.raises(SourceFailure) as error:
                await fetcher.raw('https://example.no/', OUR, {'example.no'})
            assert error.value.code == 'website_budget_exhausted'
            assert not fetcher.budget.events
    asyncio.run(go())


def test_hostname_pair_reuses_candidate_without_reusing_entity_verdict(tmp_path):
    from types import SimpleNamespace
    from signalpost.web.html import Page
    from signalpost.web.proof import score
    cfg = config(tmp_path, [OUR, OTHER])
    calls = []
    async def resolve(host, port): return ['93.184.216.34']
    async def go():
        async with httpx.AsyncClient() as client:
            fetcher = WebsiteHttp(client, cfg, Budget(cfg), BlobStore(tmp_path), resolver=resolve)
            async def get(url, *args, **kwargs):
                calls.append(url)
                return SimpleNamespace(status=200, url=url, body=html('Org nr '+OUR).encode())
            fetcher.get = get
            first, second = await asyncio.gather(
                fetcher.candidate(Candidate('https://example.no/', 'example.no', 'registry_email'), OUR),
                fetcher.candidate(Candidate('https://www.example.no/', 'example.no', 'registry_website'), OTHER))
            assert first is second
            page = Page(second.body, second.url)
            assert score(page, OUR, {}, 'registry_email', []).level == 'VERIFIED'
            assert score(page, OTHER, {}, 'registry_website', []).level == 'REJECT'
            assert fetcher.dns_counts == {OUR: 1}
            assert fetcher.attempts[OTHER][-1]['reused_candidate']
    asyncio.run(go())
    assert calls == ['https://example.no/']


def test_source_veto_reused_across_hostname_pair_without_another_request(tmp_path):
    cfg = config(tmp_path, [OUR, OTHER])
    calls = []
    async def resolve(host, port): return ['93.184.216.34']
    async def go():
        async with httpx.AsyncClient() as client:
            fetcher = WebsiteHttp(client, cfg, Budget(cfg), BlobStore(tmp_path), resolver=resolve)
            async def get(url, *args, **kwargs):
                calls.append(url)
                raise SourceFailure('url_refused')
            fetcher.get = get
            for org, host in [(OUR, 'example.no'), (OTHER, 'www.example.no')]:
                with pytest.raises(SourceFailure) as error:
                    await fetcher.candidate(Candidate('https://'+host+'/', 'example.no', 'registry_email'), org)
                assert error.value.code == 'url_refused'
    asyncio.run(go())
    assert calls == ['https://example.no/']
