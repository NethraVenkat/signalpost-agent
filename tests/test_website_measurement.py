import asyncio

import pytest

from signalpost.budget import SourceFailure
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
            await metrics.collect('first', 'pass1', stuck)
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
