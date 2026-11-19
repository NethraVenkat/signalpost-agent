"""S2 Støtteregisteret: exact-beneficiary state-aid awards only."""
import asyncio
import copy
import json
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from signalpost.sources import exact_official as eo
from signalpost.sources.http import Response

ORG = '923609016'
OTHER = '974760673'
NOW = datetime(2026, 11, 16, tzinfo=timezone.utc)
AWARD = {
    'stoettetiltaksnummer': '1000374345', 'status': 'stoettetiltaksstatus.registrert',
    'type': 'stoettetiltakstype.stoettetildelingMedStatsstoette', 'mottattDato': '2026-10-28',
    'stoetteinstrument': 'stoetteinstrumenttype.tilskudd', 'tildeltBeloep': {'beloep': 1500000.0, 'valuta': 'NOK'},
    'tilknyttetStoetteordning': '1000026412', 'tildelingsdato': '2026-09-08',
    'rolle': [{'type': 'rolletype.stoettegiver', 'rolleinnehavertype': 'virksomhet',
               'rolleinnehaverVirksomhet': {'organisasjonsnummer': '970141669', 'navn': 'NORGES FORSKNINGSRÅD'}},
              {'type': 'rolletype.stoettemottaker', 'rolleinnehavertype': 'virksomhet',
               'rolleinnehaverVirksomhet': {'organisasjonsnummer': ORG, 'navn': 'EXAMPLE AS'}}]}


def variant(**changes):
    item = copy.deepcopy(AWARD)
    item.update(changes)
    return item


def test_exact_single_beneficiary_award_is_published_with_source_values():
    value, paths = eo.state_aid_award(AWARD, ORG, NOW)
    assert value == {'company_orgnr': ORG, 'award_id': '1000374345', 'date': '2026-09-08',
                     'date_source': 'award date (tildelingsdato) as registered in Støtteregisteret',
                     'granting_authority': 'NORGES FORSKNINGSRÅD', 'granting_authority_orgnr': '970141669',
                     'label': 'State aid award', 'amount': 1500000.0, 'currency': 'NOK',
                     'scheme_id': '1000026412', 'instrument': 'stoetteinstrumenttype.tilskudd'}
    assert '/rolle/1/rolleinnehaverVirksomhet/organisasjonsnummer' in paths and '/tildeltBeloep/beloep' in paths


@pytest.mark.parametrize('item', [
    variant(rolle=[AWARD['rolle'][0], {**AWARD['rolle'][1], 'rolleinnehaverVirksomhet': {'organisasjonsnummer': OTHER, 'navn': 'X'}}]),
    variant(rolle=AWARD['rolle'] + [{**AWARD['rolle'][1], 'rolleinnehaverVirksomhet': {'organisasjonsnummer': OTHER, 'navn': 'X'}}]),
    variant(rolle=[AWARD['rolle'][1]]),                                   # no granting authority
    variant(rolle=[AWARD['rolle'][0], {**AWARD['rolle'][1], 'type': 'rolletype.spesifisertStoettemottaker'}]),
    variant(status='stoettetiltaksstatus.slettet'),
    variant(type='stoettetiltakstype.stoetteordning'),                    # a scheme, not an award
    variant(tildelingsdato='2027-01-01'),                                 # future
    variant(tildelingsdato='2023-11-15'),                                 # outside 36 months
    variant(tildelingsdato='08.09.2026'),                                 # unparsed format
    variant(stoettetiltaksnummer=None),
])
def test_unattributable_or_undated_awards_abstain(item):
    assert eo.state_aid_award(item, ORG, NOW) is None


def test_amount_is_never_invented():
    value, paths = eo.state_aid_award(variant(tildeltBeloep=None), ORG, NOW)
    assert 'amount' not in value and 'currency' not in value and 'amount_range' not in value
    value, _ = eo.state_aid_award(variant(tildeltBeloep={'beloep': float('nan'), 'valuta': 'NOK'}), ORG, NOW)
    assert 'amount' not in value
    value, paths = eo.state_aid_award(variant(tildeltBeloep=None, beloepsintervall={'fraBeloep': 500000, 'tilBeloep': 1000000}), ORG, NOW)
    assert value['amount_range'] == {'from': 500000, 'to': 1000000} and '/beloepsintervall/tilBeloep' in paths


class FakeHttp:
    def __init__(self, pages):
        self.pages, self.calls = pages, []

    async def request(self, url, org, payload=None, headers=None):
        self.calls.append((url, payload, headers))
        body = json.dumps({'pageSize': eo.STOTTE_PAGE_SIZE, 'page': len(self.calls),
                           'stoettetildeling': self.pages[len(self.calls) - 1]}, ensure_ascii=False).encode()
        return Response(body, 200, url, '2026-11-16T09:00:00Z', 'a' * 64)


def test_section_receipts_point_at_exact_source_scalars_and_none_found_is_explicit():
    http = FakeHttp([[AWARD]])
    section = asyncio.run(eo.state_aid(ORG, http, NOW))
    assert http.calls[0][1] == [{'field': 'STOETTEMOTTAKER_ORGNR', 'value': ORG, 'matchType': 'EXACT_MATCH'}]
    assert http.calls[0][2] == {'Accept': 'application/json'}
    [claim] = section.claims
    assert claim.field == 'state_aid.award.1000374345' and claim.family == 'state_aid'
    spans = {e.locator: e.claim_span for e in section.evidence}
    assert '"organisasjonsnummer": "' + ORG + '"' in spans['/stoettetildeling/0/rolle/1/rolleinnehaverVirksomhet/organisasjonsnummer']
    assert '2026-09-08' in spans['/stoettetildeling/0/tildelingsdato']
    empty = asyncio.run(eo.state_aid(ORG, FakeHttp([[variant(tildelingsdato='2020-01-01')]]), NOW))
    assert empty.state == 'not_available' and empty.claims[0].field == 'state_aid.awards' and empty.claims[0].value is None


def verify_section(section, body, org=ORG, mutate=None):
    from scripts.verify_output import verify_exact_official
    claims = [c.model_dump(mode='json') for c in section.claims]
    if mutate:
        mutate(claims[0])
    evidence = {e.id: e.model_dump(mode='json') for e in section.evidence}
    return verify_exact_official({'organisation_number': org}, {'claims': claims}, evidence, lambda sha: body.decode())


def test_independent_verifier_replays_value_and_rejects_forgery():
    http = FakeHttp([[AWARD]])
    section = asyncio.run(eo.state_aid(ORG, http, NOW))
    body = json.dumps({'pageSize': eo.STOTTE_PAGE_SIZE, 'page': 1, 'stoettetildeling': [AWARD]}, ensure_ascii=False).encode()
    assert verify_section(section, body) == 1
    with pytest.raises(AssertionError):
        verify_section(section, body, mutate=lambda c: c['value'].update(amount=2500000.0))
    with pytest.raises(AssertionError):
        verify_section(section, body, mutate=lambda c: c['value'].update(granting_authority='SOMEONE ELSE'))
    with pytest.raises(AssertionError):  # the record names a different beneficiary than this envelope
        verify_section(section, body, org=OTHER)


def test_pagination_limit_is_explicit():
    full = [variant(stoettetiltaksnummer=str(1000 + i)) for i in range(eo.STOTTE_PAGE_SIZE)]
    http = FakeHttp([full] * eo.STOTTE_MAX_PAGES)
    section = asyncio.run(eo.state_aid(ORG, http, NOW))
    assert len(http.calls) == eo.STOTTE_MAX_PAGES
    assert any(e.code == 'state_aid_pagination_limit' for e in section.errors)


def robots_reset_client(search_body, failure='ConnectError'):
    import httpx
    calls = []

    def handler(request):
        calls.append((request.method, request.url.path, request.headers.get('accept')))
        if request.url.path == '/robots.txt':
            raise getattr(httpx, failure)('robots transport unavailable')
        return httpx.Response(200, content=search_body)
    return httpx.AsyncClient(transport=httpx.MockTransport(handler)), calls


@pytest.mark.parametrize('unserved', [True, False])
@pytest.mark.parametrize('failure', ['ConnectError', 'ReadTimeout'])
def test_robots_reset_always_blocks_and_caches_the_refusal(unserved, failure, monkeypatch):
    import hashlib
    from signalpost.budget import SourceFailure
    from signalpost.sources.exact_public import PublicHttp
    from tests.test_official_resilience import FakeBudget
    import signalpost.sources.official_resilience as retry

    async def no_sleep(_):
        return None
    monkeypatch.setattr(retry.asyncio, 'sleep', no_sleep)

    class Blobs:
        def put(self, raw):
            return hashlib.sha256(raw).hexdigest()

    async def run():
        client, calls = robots_reset_client(b'{}', failure)
        async with client:
            budget = FakeBudget()
            http = PublicHttp(client, SimpleNamespace(request_timeout=1, website_user_agent='SignalpostTest'), budget, Blobs(),
                              hosts=eo.HOSTS, sections=eo.SECTION_BY_HOST, robots_unserved=eo.HOSTS if unserved else (), politeness=0)
            for _ in range(2):
                with pytest.raises(SourceFailure) as error:
                    await http.request(eo.stotte_url(1), ORG, eo.stotte_payload(ORG))
                assert error.value.code == 'public_robots_unavailable'
            assert http.robots[eo.STOTTE_HOST] is False
            assert all(path == '/robots.txt' for _, path, _ in calls)
            assert len(calls) == 3
            assert budget.events[-1]['robots_decision'].startswith('blocked')
    asyncio.run(run())


@pytest.mark.parametrize('robots_status', [200, 204, 404, 403])
def test_robots_reset_then_success_or_4xx_allows_data(robots_status, monkeypatch):
    import hashlib
    import httpx
    from signalpost.sources.exact_public import PublicHttp
    from tests.test_official_resilience import FakeBudget
    import signalpost.sources.official_resilience as retry

    async def no_sleep(_):
        return None
    monkeypatch.setattr(retry.asyncio, 'sleep', no_sleep)
    calls = []

    def handler(request):
        calls.append(request.url.path)
        if request.url.path == '/robots.txt':
            if calls.count('/robots.txt') == 1 and robots_status == 200:
                raise httpx.ConnectError('connection reset')
            return httpx.Response(robots_status, content=b'User-agent: *\nAllow: /\n')
        return httpx.Response(200, content=b'{}')

    class Blobs:
        def put(self, raw):
            return hashlib.sha256(raw).hexdigest()

    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            budget = FakeBudget()
            http = PublicHttp(client, SimpleNamespace(request_timeout=1, website_user_agent='SignalpostTest'),
                              budget, Blobs(), hosts=eo.HOSTS, robots_unserved=eo.HOSTS, politeness=0)
            assert (await http.request(eo.stotte_url(1), ORG, eo.stotte_payload(ORG))).status == 200
            assert calls[-1] != '/robots.txt'
            assert calls.count('/robots.txt') == (2 if robots_status == 200 else 1)
            if robots_status == 200:
                assert budget.events[0]['official_retry_backoff_seconds'] == 5
    asyncio.run(run())


def test_briefing_sentence_states_exact_amount_without_scientific_notation():
    value, _ = eo.state_aid_award(AWARD, ORG, NOW)
    claim = SimpleNamespace(field='state_aid.award.1000374345', value=value, id='c1', availability='available', carried_forward=False)
    [sentence] = eo.briefing_sentences(SimpleNamespace(claims=[claim]))
    assert sentence.text == 'State aid award: 1500000 NOK from NORGES FORSKNINGSRÅD; 2026-09-08.'
