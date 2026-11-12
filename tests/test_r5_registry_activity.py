import asyncio
from datetime import datetime, timezone

import httpx
import pytest

from signalpost.budget import SourceFailure
from signalpost.sources import registry_changes as rc
from tests.test_registry_changes import ORG, NOW, event, response, envelope, extract


@pytest.mark.parametrize('now,expected', [('2026-11-12', '2023-11-12'), ('2024-02-29', '2021-02-28')])
def test_36_calendar_month_cutoff(now, expected):
    assert rc.cutoff(datetime.fromisoformat(now).replace(tzinfo=timezone.utc)).date().isoformat() == expected


@pytest.mark.parametrize('date', [None, '', 'invalid', '2026-01-01T00:00:00'])
def test_missing_or_naive_event_date_never_publishes(date):
    with pytest.raises(SourceFailure, match='registry_change_missing_or_invalid_date'):
        extract(event(dato=date))


def test_missing_date_key_never_publishes():
    item = event(); del item['dato']
    with pytest.raises(SourceFailure): extract(item)


def test_unproven_historical_subunit_abstains():
    item = event(endringstype='Sletting')
    result = rc.extract(item, response(item), '/event', ORG, 'underenheter', {})
    assert result.state == 'not_available' and not result.claims
    assert result.errors[0].code == 'registry_change_parent_not_proven'


def test_window_and_registry_coverage_independent_of_website():
    class Http:
        async def get(self, url, org):
            assert httpx.URL(url).params['dato'] == '2023-10-18T07:00:00.000Z'
            return response({'page': {'number': 0, 'size': 1000, 'totalElements': 0, 'totalPages': 0}})
    env = envelope()
    env.run.sections['activity'] = 'failed'
    result = asyncio.run(rc.fetch_batch({ORG: env}, Http(), None, NOW))
    info = env.run.refresh['registry_activity']
    assert info['state'] == result[ORG].state == 'not_available'
    assert info['lookback_months'] == 36
    assert info['unavailable_types']['formal_announcements']['state'] == 'not_available'
    assert rc.merge(env, result[ORG], True).state == 'failed'


@pytest.mark.parametrize('mode', ['duplicate', 'missing_date', 'outside', 'short_page'])
def test_bad_second_page_retains_verified_first_page(monkeypatch, mode):
    monkeypatch.setattr(rc, 'PAGE_SIZE', 1)
    class Http:
        async def get(self, url, org):
            page = int(httpx.URL(url).params['page'])
            item = event(oppdateringsid=10 + page)
            if page:
                if mode == 'duplicate': item['oppdateringsid'] = 10
                if mode == 'missing_date': item.pop('dato')
                if mode == 'outside': item['dato'] = '2023-01-01T00:00:00Z'
            return response({'page': {'number': page, 'size': 1, 'totalElements': 2, 'totalPages': 2},
                             '_embedded': {'oppdaterteEnheter': [] if page and mode == 'short_page' else [item]}})
    result = asyncio.run(rc.fetch_batch({ORG: envelope()}, Http(), None, NOW))[ORG]
    assert result.state == 'failed' and len(result.claims) == 1
    assert result.claims[0].value['event_id'] == 10
    assert result.evidence[0].effective_at is None
