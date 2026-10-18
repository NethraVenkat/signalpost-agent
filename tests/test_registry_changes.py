import asyncio
import hashlib
import json
import re
from dataclasses import replace
from types import SimpleNamespace

import httpx
import pytest

from signalpost.budget import SourceFailure
from signalpost.models.shapes import validate
from signalpost.runner import placeholder, update, run
from signalpost.sources import registry_changes as rc
from signalpost.sources.extract import Section
from signalpost.sources.http import Response
from signalpost.synthesis.template import generate
from signalpost.synthesis.validate import sentence_error
from signalpost.site import fact
from tests.test_registry import config, numbers, handler

ORG = '923609016'
OTHER = '988330752'
NOW = '2026-10-18T07:00:00Z'


def event(**kwargs):
    return dict({'organisasjonsnummer': ORG, 'oppdateringsid': 10,
                 'dato': '2026-09-01T12:30:00Z', 'endringstype': 'Endring',
                 'endringer': [{'op': 'replace', 'path': '/navn', 'value': 'New name AS'}]}, **kwargs)


def response(data, endpoint='enheter'):
    body = json.dumps(data).encode()
    return Response(body, 200, rc.BASE + 'oppdateringer/' + endpoint + '?size=1000', NOW,
                    hashlib.sha256(body).hexdigest())


def envelope(org=ORG):
    env = placeholder(org, 'test', NOW, ('identity', 'subunits', 'activity'))
    env.run.sections.update(identity='available', subunits='not_available')
    return env


def extract(e):
    return rc.extract(e, response({'event': e}), '/event', ORG, 'enheter')


@pytest.mark.parametrize('path', ['/navn', '/kapital/belop', '/forretningsadresse/adresse/0', '/postadresse', '/postadresse/postnummer'])
def test_named_fields_have_exact_values_and_publication_evidence(path):
    e = event(endringer=[{'op': 'replace', 'path': path, 'value': 0}])
    section = extract(e)
    c = section.claims[0]
    assert c.value['new_value'] == 0
    assert c.value['date'] == e['dato'] and c.value['date_source'] == rc.DATE_LABEL
    assert 'old_value' not in c.value
    assert section.evidence[0].effective_at is None
    assert section.evidence[0].content_sha256 == response({'event': e}).sha
    assert section.evidence[0].retrieved_at == NOW
    assert section.evidence[0].extraction_method == rc.METHOD


@pytest.mark.parametrize('changes', [[], [{'op': 'replace', 'path': '/sisteInnsendteAarsregnskap', 'value': '2025'}],
    [{'op': 'replace', 'path': '/antallAnsatte', 'value': 40}], [{'op': 'replace', 'path': '/naeringskode1', 'value': {}}],
    [{'op': 'replace', 'path': '/kapital/innfortDato', 'value': '2026-01-01'}]])
def test_bare_or_excluded_update_never_publishes(changes):
    assert not extract(event(endringer=changes)).claims


def test_removal_does_not_invent_new_or_old_value():
    c = extract(event(endringer=[{'op': 'remove', 'path': '/postadresse'}])).claims[0]
    assert 'new_value' not in c.value and 'old_value' not in c.value
    assert 'field removed' in rc.sentence(c.value)


def test_wrong_entity_rejected():
    with pytest.raises(SourceFailure): extract(event(organisasjonsnummer=OTHER))


@pytest.mark.parametrize('kind', ['Ny', 'Sletting'])
def test_subunit_exact_parent_and_start_date(kind):
    proof = extract(event()).evidence[0]
    scope = {OTHER: ({'overordnetEnhet': ORG, 'oppstartsdato': '2025-04-01'}, proof)}
    e = event(organisasjonsnummer=OTHER, endringstype=kind)
    s = rc.extract(e, response(e, 'underenheter'), '/event', ORG, 'underenheter', scope)
    assert len(s.claims) == 1 and s.claims[0].value['subunit_orgnr'] == OTHER
    assert ('start_date' in s.claims[0].value) == (kind == 'Ny')
    scope[OTHER][0]['overordnetEnhet'] = OTHER
    with pytest.raises(SourceFailure): rc.extract(e, response(e), '/event', ORG, 'underenheter', scope)


def test_pagination_complete_and_duplicate_page_fails(monkeypatch):
    monkeypatch.setattr(rc, 'PAGE_SIZE', 1)
    class Http:
        duplicate = False
        async def get(self, url, org):
            page = int(httpx.URL(url).params['page'])
            return response({'page': {'number': page, 'size': 1, 'totalElements': 2, 'totalPages': 2},
                             '_embedded': {'oppdaterteEnheter': [event(oppdateringsid=10 if self.duplicate else 10+page)]}})
    async def collect(http):
        return [e async for e in rc.pages(http, 'enheter', [ORG], '2024-10-18T00:00:00Z', NOW)]
    http = Http()
    assert len(asyncio.run(collect(http))) == 2
    http.duplicate = True
    with pytest.raises(SourceFailure): asyncio.run(collect(http))


def test_timeout_fails_even_with_no_website():
    class Http:
        async def get(self, *args): raise SourceFailure('timeout')
    result = asyncio.run(rc.fetch_batch({ORG: envelope()}, Http(), None, NOW))
    assert result[ORG].state == 'failed' and result[ORG].errors[0].code == 'timeout'


@pytest.mark.parametrize('endpoint', ['enheter', 'underenheter'])
@pytest.mark.parametrize('until,expected', [
    ('2026-10-18T07:04:40.345521Z', '2026-10-18T07:04:40.345Z'),
    ('2026-10-18T12:34:40.345521+05:30', '2026-10-18T07:04:40.345Z'),
    ('2026-10-18T07:04:40Z', '2026-10-18T07:04:40.000Z'),
])
def test_brreg_query_timestamp_contract(endpoint, until, expected):
    class Http:
        async def get(self, url, org):
            params = httpx.URL(url).params
            assert params['dato'] == '2024-10-18T07:04:40.000Z'
            assert params['updatedBefore'] == expected
            for name in ('dato', 'updatedBefore'):
                assert re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z', params[name])
            return response({'page': {'number': 0, 'size': 1000, 'totalElements': 0, 'totalPages': 0}})
    async def collect():
        return [item async for item in rc.pages(Http(), endpoint, [ORG], '2024-10-18T07:04:40Z', until)]
    assert asyncio.run(collect()) == []


def test_brreg_http400_marks_activity_failed(tmp_path):
    original = handler()
    def respond(request):
        if '/oppdateringer/' in request.url.path:
            return httpx.Response(400, json={'status': 400, 'valideringsfeil': []})
        return original(request)
    async def go():
        cfg = config(tmp_path, [ORG], registry_changes=True)
        async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
            await run(cfg, client=client)
        return json.loads(cfg.output.read_text(encoding='utf8').split('\n')[0])
    row = asyncio.run(go())
    assert row['run']['sections']['identity'] == 'available'
    assert row['run']['sections']['activity'] == 'failed'
    assert any(e['section'] == 'activity' and e['code'] == 'registry_change_http_400' for e in row['errors'])
    assert not any(c['field'].startswith('registry_change.') for c in row['claims'])


def test_latest_summary_citation_and_site_publication_label():
    env = envelope()
    a = extract(event())
    b = extract(event(oppdateringsid=11, dato='2026-10-01T00:00:00Z'))
    a.claims.extend(b.claims); a.evidence.extend(b.evidence)
    update(env, 'activity', a)
    synthesis = generate(env)
    sentence = synthesis.sections.changes[0]
    assert sentence.claim_ids == [b.claims[0].id]
    assert sentence_error(sentence, env) is None
    rendered = fact(b.claims[0].model_dump(), {e.id: e.model_dump() for e in b.evidence})
    assert 'registry publication time (not effective date):' in rendered
    assert 'New name AS' in rendered


def test_disabled_flag_makes_no_feed_requests_and_preserves_ids(tmp_path):
    async def go():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler())) as client:
            cfg = config(tmp_path, [ORG], registry_changes=False)
            await run(cfg, client=client)
            return json.loads(cfg.output.read_text().splitlines()[0])
    row = asyncio.run(go())
    assert 'activity' not in row['run']['sections']


@pytest.mark.parametrize('flags,enabled', [([], True), (['--registry-changes'], True), (['--no-registry-changes'], False)])
def test_release_default_and_cli_off_switch(tmp_path, monkeypatch, flags, enabled):
    from signalpost import cli
    from signalpost.config import Config
    paths = dict(organisations=tmp_path/'input', output=tmp_path/'output', report=tmp_path/'report')
    assert Config(**paths).registry_changes is True
    seen = []
    async def capture(cfg):
        seen.append(cfg.registry_changes)
        return dict(emitted_envelopes=0, invalid_inputs=[], requests=0, runtime_ms=0,
                    changes=0, observation_changes=0, deadline_hits=0, warnings=[])
    monkeypatch.setattr(cli, 'run', capture)
    monkeypatch.setattr('sys.argv', ['signalpost', 'run', *[arg for key, value in paths.items()
                                                         for arg in ('--'+key, str(value))], *flags])
    assert cli.main() == 0 and seen == [enabled]


def test_forced_feed_failure_100_terminal_envelopes(tmp_path):
    orgs = numbers(100)
    baseline = handler()
    def respond(request):
        if '/oppdateringer/' in request.url.path: return httpx.Response(503)
        return baseline(request)
    async def go():
        cfg = config(tmp_path, orgs, registry_changes=True)
        async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
            report = await run(cfg, client=client)
        return report, [json.loads(line) for line in cfg.output.read_text().splitlines()]
    report, rows = asyncio.run(go())
    assert report['emitted_envelopes'] == 100
    assert [r['organisation_number'] for r in rows] == orgs
    for row in rows:
        validate(row, 'union')
        assert row['run']['sections']['identity'] == 'available'
        assert row['run']['sections']['activity'] == 'failed'
