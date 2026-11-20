import asyncio
import time
from types import SimpleNamespace

import pytest

from signalpost.budget import SourceFailure
from signalpost.models.envelope import Error
from signalpost.runner import placeholder
from signalpost.web import adaptive
from signalpost.web.measurement import CAP, WebsiteMeasurement, count_request, phase


def test_company_cap_is_cumulative_and_leaves_other_company_budget_intact():
    async def execute():
        metrics = WebsiteMeasurement(.12)

        async def first_pass():
            count_request()
            await asyncio.sleep(.05)

        async def stuck():
            count_request()
            async with phase('dns'):
                await asyncio.Event().wait()

        await metrics.collect('first', 'pass1', first_pass)
        with pytest.raises(SourceFailure, match=CAP):
            await metrics.collect('first', 'pass2', stuck)
        await metrics.collect('second', 'pass1', first_pass)
        return metrics.report(['first', 'second'])

    report = asyncio.run(execute())
    assert report['companies_hitting_cap'] == 1
    first, second = (report['per_company'][org] for org in ('first', 'second'))
    assert first['requests'] == 2 and first['company_cap_hit']
    assert first['attempts'][-1]['waiting_on'] == 'dns'
    assert first['attempts'][-1]['state'] == CAP
    assert first['attempts'][-1]['active_seconds'] < .12
    assert second['requests'] == 1 and not second['company_cap_hit']


def test_reports_batch_interruptions_separately_from_company_cap():
    async def execute():
        metrics = WebsiteMeasurement(10)

        async def blocked():
            async with phase('host_slot'):
                await asyncio.Event().wait()

        with pytest.raises(TimeoutError):
            async with asyncio.timeout(.02):
                await metrics.collect('first', 'pass1', blocked)
        with pytest.raises(TimeoutError):
            async with asyncio.timeout(.02):
                async with metrics.company_slot('queued', asyncio.Semaphore(0)):
                    raise AssertionError('The slot was never acquired')
        return metrics.report(['first', 'queued'])

    report = asyncio.run(execute())
    first = report['per_company']['first']['attempts'][0]
    queued = report['per_company']['queued']
    assert first['state'] == 'batch_deadline' and first['waiting_on'] == 'host_slot'
    assert queued['queue_interrupted'] and queued['attempts'] == []
    assert report['companies_hitting_cap'] == 0


def test_pass2_cutoff_attaches_one_website_error_to_each_affected_company():
    first, second = '923609016', '988330752'
    envelopes = {
        org: placeholder(org, 'website-cutoff', '2026-11-20T00:00:00Z', ('website',))
        for org in (first, second)
    }
    envelopes[second].errors.append(Error(section='website', code='deadline', message='Already recorded'))
    now = time.monotonic()
    http = SimpleNamespace(
        budget=SimpleNamespace(
            start=now - 100, deadline=now + 100, pass2_cutoff=now, phase='pass1', events=[],
        ),
        discovery_sessions={org: {'context': {}} for org in envelopes},
    )

    report = asyncio.run(adaptive.run(envelopes, http, None, {}, {}, None, None))

    assert report['pass2']['states'] == {'deadline': 2}
    for envelope in envelopes.values():
        assert sum(error.section == 'website' and error.code == 'deadline' for error in envelope.errors) == 1
