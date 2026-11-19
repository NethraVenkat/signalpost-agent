import json
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
