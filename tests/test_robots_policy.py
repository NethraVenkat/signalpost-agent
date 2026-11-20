import asyncio
import hashlib
from pathlib import Path

import httpx
import pytest

from signalpost.budget import Budget, SourceFailure
from signalpost.sources.blobstore import BlobStore
from signalpost.web.fetcher import WebsiteHttp
from signalpost.web.robots import RobotsPolicy
from tests.test_registry import config


def test_combines_wildcard_groups_and_chooses_most_specific_rule():
    policy = RobotsPolicy([
        'User-agent: *', 'Disallow: /one', 'Disallow: /two',
        'Sitemap: https://example.no/publisher-map.xml',
        'User-agent: *', 'Allow: /one/public', 'Disallow: /three',
        'Allow: /two', 'Disallow: /download/*.csv$',
    ])
    can_fetch = lambda path: policy.can_fetch('SignalpostAgent/1.0', 'https://example.no' + path)
    assert not can_fetch('/one/private')
    assert can_fetch('/one/public')
    assert can_fetch('/two')  # Allow wins an equally specific tie.
    assert not can_fetch('/three')
    assert not can_fetch('/download/month/report.csv')
    assert can_fetch('/download/month/report.csv?format=preview')
    assert policy.site_maps() == ['https://example.no/publisher-map.xml']


@pytest.mark.parametrize('directive', ['Allow:', 'Disallow:'])
def test_empty_directives_end_agent_list_without_restricting_paths(directive):
    policy = RobotsPolicy([
        'User-agent: *', directive, 'User-agent: UnrelatedBot',
        'Disallow: /', 'User-agent: SignalpostAgent', 'Disallow: /mine',
        'User-agent: SignalpostAgent', 'Disallow: /other',
    ])
    assert policy.can_fetch('AnotherBot/1.0', 'https://example.no/mine')
    assert not policy.can_fetch('UnrelatedBot/1.0', 'https://example.no/')
    assert policy.can_fetch('SignalpostAgent/1.0', 'https://example.no/')
    assert not policy.can_fetch('SignalpostAgent/1.0', 'https://example.no/mine')
    assert not policy.can_fetch('SignalpostAgent/1.0', 'https://example.no/other')


def test_saved_clime_policy_denies_all_nine_historical_paths(tmp_path):
    org = '923609016'
    cfg = config(tmp_path, [org], dns_precheck=False)
    raw = Path(__file__).with_name('fixtures').joinpath('robots_clime.txt').read_bytes()
    raw = raw.replace(b'\r\n', b'\n')
    assert hashlib.sha256(raw).hexdigest() == (
        'f746e6bb107cdcef4d19a5903b1491098eedfcedd21f68bcdbc12311206c8195'
    )
    paths = ('/', '/sitemap.xml', '/personvern', '/personvernerklaering', '/kontakt',
             '/om-oss', '/kontakt-oss', '/salgsbetingelser', '/kjopsbetingelser')
    requests = []

    def respond(request):
        requests.append(request.url.path)
        assert request.url.path == '/robots.txt'
        return httpx.Response(200, content=raw, headers={'Content-Type': 'text/plain'})

    async def replay():
        async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
            fetcher = WebsiteHttp(client, cfg, Budget(cfg), BlobStore(cfg.state_dir))
            for path in paths:
                with pytest.raises(SourceFailure) as failure:
                    await fetcher.get('https://clime.com' + path, org, 'clime.com')
                assert failure.value.code == 'robots'

    asyncio.run(replay())
    assert requests == ['/robots.txt']
