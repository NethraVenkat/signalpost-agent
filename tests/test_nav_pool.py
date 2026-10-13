from signalpost.sources.nav import time_cap
from tests.test_registry import config


def test_nav_time_cap_follows_budget_and_can_be_overridden(tmp_path):
    assert time_cap(config(tmp_path / 'small', [], time_budget_seconds=900)) == 315
    assert time_cap(config(tmp_path / 'default', [])) == 600
    assert time_cap(config(tmp_path / 'override', [], nav_time_cap_seconds=240)) == 240


def test_live_runner_has_two_pools_and_nav_starts_first(tmp_path, monkeypatch):
    import asyncio, json, httpx
    from signalpost.runner import run
    from tests.test_nav import TOKEN
    from tests.test_registry import handler
    calls=[];pools=[]
    def transport(limit, metrics=None):
        pool=len(pools);pools.append(limit)
        def response(request):
            calls.append((pool,request.url.host,request.url.path))
            if request.url.host=='pam-stilling-feed.nav.no':
                if request.url.path=='/api/publicToken':return httpx.Response(200,text=TOKEN)
                return httpx.Response(200,json={'items':[],'next_url':None})
            return handler()(request)
        return httpx.MockTransport(response)
    monkeypatch.delenv('NAV_API_TOKEN',raising=False)
    monkeypatch.setattr('signalpost.runner.safe_transport',transport)
    cfg=config(tmp_path,['923609016'],hiring=True)
    report=asyncio.run(run(cfg))
    assert len(pools)==2 and pools[1]==cfg.nav_concurrency
    assert calls[0][1]=='pam-stilling-feed.nav.no'
    assert all(pool==1 for pool,host,_ in calls if host=='pam-stilling-feed.nav.no')
    assert all(pool==0 for pool,host,_ in calls if host=='data.brreg.no')
    assert report['hiring_prefetch']['feed_complete'] is True
