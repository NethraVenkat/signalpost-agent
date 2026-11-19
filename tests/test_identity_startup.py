import asyncio
import json

import httpx
import pytest

from signalpost.runner import run
from signalpost.sources import identity_startup
from tests.test_registry import config, entity, numbers


@pytest.mark.parametrize('recovery', ['outage', 'recovers', 'scattered'])
def test_confirmed_outage_only_aborts_after_recovery_pause(tmp_path, monkeypatch, recovery):
    orgs = numbers(30)
    cfg = config(tmp_path, orgs, official_source_health=True)
    calls = []
    pauses = []

    async def wait(seconds):
        pauses.append(seconds)

    monkeypatch.setattr(identity_startup, '_wait', wait)

    def respond(request):
        if request.method == 'HEAD':
            return httpx.Response(200)
        org = request.url.path.rsplit('/', 1)[-1]
        # Keep ordinary follow-up sources out of this startup-policy test.
        if len(org) != 9:
            return httpx.Response(200, json=[])
        calls.append(org)
        index = len(calls)
        failing = recovery == 'outage' or (recovery == 'recovers' and index <= 25) or (recovery == 'scattered' and index in {1, 7, 15})
        if failing:
            raise httpx.ConnectError('temporary DNS/connect outage', request=request)
        return httpx.Response(200, json=entity(org))

    async def execute():
        async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
            return await run(cfg, client=client)

    metrics = asyncio.run(execute())
    rows = [json.loads(line) for line in cfg.output.read_text(encoding='utf8').splitlines()]
    assert len(rows) == len(orgs)
    check = metrics['startup_identity_check']
    if recovery == 'outage':
        assert len(calls) == 28 and pauses == [15]
        assert check['state'] == metrics['run_status'] == 'aborted'
        assert metrics['counts_by_state'] == {'source_error': 30}
        assert all(row['run']['terminal_status'] == 'failed' for row in rows)
        assert metrics['available_claims'] == metrics['successful_http_responses'] == 0
        assert any('data.brreg.no' in warning for warning in metrics['warnings'])
    else:
        assert metrics['run_status'] != 'aborted'
        assert any(row['run']['sections']['identity'] == 'available' for row in rows)
        assert pauses == ([15] if recovery == 'recovers' else [])


def test_all_failed_sections_are_never_counted_complete(tmp_path):
    cfg = config(tmp_path, ['923609016'])

    async def execute():
        async with httpx.AsyncClient(transport=httpx.MockTransport(lambda request: httpx.Response(403))) as client:
            return await run(cfg, client=client)

    metrics = asyncio.run(execute())
    assert metrics['counts_by_state'].get('complete', 0) == 0
    assert metrics['run_status'] == 'failed'
    assert metrics['warnings']
