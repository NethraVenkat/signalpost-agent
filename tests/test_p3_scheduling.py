"""P3b/P3c: exact-ID sources on different hosts run side by side; one host stays serial."""
import asyncio
from types import SimpleNamespace

from signalpost.sources import exact_official as eo
from signalpost.sources import exact_public as ep
from signalpost.sources.extract import Section


def envelopes(n=3):
    return {f'92360901{i}': SimpleNamespace(run=SimpleNamespace(sections={'identity': 'available'}), claims=[]) for i in range(n)}


def test_live_official_families_overlap_but_each_stays_serial(monkeypatch):
    active = {}; peak = {'all': 0}; per = {}
    def fetcher(family):
        async def fetch(org, http, now):
            active[family] = active.get(family, 0) + 1
            per[family] = max(per.get(family, 0), active[family])
            peak['all'] = max(peak['all'], sum(active.values()))
            await asyncio.sleep(0.01)
            active[family] -= 1
            return Section(state='not_available')
        return fetch
    monkeypatch.setattr(eo, 'FETCHERS', {'state_aid': fetcher('state_aid'), 'licences': fetcher('licences')})
    monkeypatch.setattr(eo, 'LOCAL', {})
    cfg = SimpleNamespace(state_aid=True, licences=True, research=False, inspections=False, request_timeout=1, website_user_agent='t')
    seen = []
    asyncio.run(eo.enrich(envelopes(), None, cfg, None, None, lambda e, f, s: seen.append(f)))
    assert peak['all'] == 2 and per == {'state_aid': 1, 'licences': 1}
    assert seen.count('state_aid') == 3 and seen.count('licences') == 3


def test_gleif_ted_and_official_start_together(monkeypatch):
    started = []
    async def batch(name):
        started.append(name); await asyncio.sleep(0.02); return {}
    monkeypatch.setattr(ep, 'gleif_batch', lambda orgs, http: batch('gleif'))
    monkeypatch.setattr(ep, 'ted_batch', lambda orgs, http, now: batch('ted'))
    async def official(*a): started.append('official'); await asyncio.sleep(0.02)
    monkeypatch.setattr(eo, 'enrich', official)
    cfg = SimpleNamespace(gleif=True, procurement=True)
    async def main():
        task = asyncio.create_task(ep.enrich(envelopes(), None, cfg, None, None, lambda *a: None))
        await asyncio.sleep(0.005)
        assert sorted(started) == ['gleif', 'official', 'ted']  # all in flight before any finishes
        await task
    monkeypatch.setattr(ep, 'PublicHttp', lambda *a, **k: None)
    asyncio.run(main())
