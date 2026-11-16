"""P3d: every evidence record repeats its exact request URL, so update-feed batches
must keep that URL short. Same request shape, fewer numbers per request."""
import asyncio
import json
from urllib.parse import urlsplit, parse_qs

from signalpost.sources import registry_changes as rc


class Recorder:
    def __init__(self):
        self.urls = []
        self.blobs = None

    async def get(self, url, org):
        self.urls.append(url)
        raise Stop


class Stop(Exception):
    pass


def test_update_feed_urls_stay_short():
    assert rc.CHUNK == 20
    http = Recorder()
    numbers = [str(923609016 + i) for i in range(rc.CHUNK)]
    async def drain():
        async for _ in rc.pages(http, 'enheter', numbers, '2026-01-01T00:00:00Z', '2026-11-16T00:00:00Z'):
            pass
    try:
        asyncio.run(drain())
    except Stop:
        pass  # only the request URL shape matters here
    assert http.urls, 'no request built'
    url = http.urls[0]
    assert parse_qs(urlsplit(url).query)['organisasjonsnummer'][0].split(',') == numbers
    assert len(url) < 500  # 20 numbers: 450 characters (200 numbers: ~2,600)
