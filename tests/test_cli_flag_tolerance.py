import json
from collections import Counter
import sys

import httpx
import pytest

from signalpost import cli
from signalpost.runner import run
from tests.test_registry import handler


@pytest.mark.parametrize('extra', [[], ['--invented-one', '--invented-two', '--invented-three']])
def test_minimum_flags_and_unknown_flags_produce_real_envelopes(tmp_path, monkeypatch, capsys, extra):
    batch = tmp_path / 'batch.txt'
    batch.write_text('923609016\nbad\n', encoding='utf8')
    output, report = tmp_path / 'envelopes.jsonl', tmp_path / 'report.json'

    async def isolated_run(config):
        # Exercise the real CLI, runner, serializer and report without live sources.
        for name in ('websites', 'hiring', 'public_activity', 'registry_changes', 'gleif',
                     'procurement', 'state_aid', 'research', 'licences', 'inspections',
                     'official_source_health'):
            setattr(config, name, False)
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler())) as client:
            return await run(config, client=client)

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(cli, 'run', isolated_run)
    monkeypatch.setattr(sys, 'argv', ['signalpost', 'run', '--organisations', str(batch),
                                   '--output', str(output), '--report', str(report), *extra])
    assert cli.main() == 0
    rows = [json.loads(line) for line in output.read_text(encoding='utf8').splitlines()]
    assert [row['organisation_number'] for row in rows] == ['923609016', 'bad']
    assert rows[0]['run']['sections']['identity'] == 'available'
    metrics = json.loads(report.read_text(encoding='utf8'))
    assert metrics['unrecognized_arguments'] == extra
    assert bool(metrics['warnings']) == bool(extra)
    assert bool('ignoring unrecognised arguments' in capsys.readouterr().err) == bool(extra)


@pytest.mark.parametrize('scenario,exit_code', [('total', 1), ('accounts', 0), ('recovers', 0)])
def test_live_connectivity_exit_handles_bulk_anchored_runs(tmp_path, monkeypatch, capsys, scenario, exit_code):
    org = '923609016'
    batch = tmp_path / 'batch.txt'
    bulk = tmp_path / 'registry.csv'
    output, report = tmp_path / 'envelopes.jsonl', tmp_path / 'report.json'
    batch.write_text(org + '\n', encoding='utf8')
    bulk.write_text(f'organisasjonsnummer,navn\n{org},EXAMPLE AS\n', encoding='utf8')
    calls = Counter()
    normal = handler()

    def respond(request):
        path = request.url.path
        calls[path] += 1
        if scenario == 'total' or (path == '/regnskapsregisteret/regnskap/' + org
                and (scenario == 'accounts' or calls[path] == 1)):
            raise httpx.ConnectError('fixture outage', request=request)
        return normal(request)

    async def no_delay(budget, event, attempt, **kwargs):
        return None

    async def isolated_run(config):
        for name in ('websites', 'hiring', 'public_activity', 'registry_changes', 'gleif',
                     'procurement', 'state_aid', 'research', 'licences', 'inspections',
                     'official_source_health', 'corporate_registry'):
            setattr(config, name, False)
        async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
            return await run(config, client=client)

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr('signalpost.sources.http.pause', no_delay)
    monkeypatch.setattr(cli, 'run', isolated_run)
    monkeypatch.setattr(sys, 'argv', ['signalpost', 'run', '--organisations', str(batch),
                                     '--bulk', str(bulk), '--output', str(output),
                                     '--profiles-output', 'profiles.jsonl', '--report', str(report),
                                     '--run-id', 'connectivity-test', '--expected-count', '1'])
    assert cli.main() == exit_code
    info = json.loads(report.read_text(encoding='utf8'))
    assert info['emitted_envelopes'] == 1
    assert (info['successful_http_responses'] == 0) == (scenario == 'total')
    row = json.loads(output.read_text(encoding='utf8'))
    assert row['run']['sections']['identity'] == 'available'
    if scenario in {'total', 'accounts'}:
        assert info['run_status'] == 'partial'
        assert row['run']['sections']['accounts'] == 'failed'
    else:
        assert calls['/regnskapsregisteret/regnskap/' + org] == 2
        assert row['run']['sections']['accounts'] == 'not_available'
    assert ('zero successful HTTP responses' in capsys.readouterr().err) == (scenario == 'total')
