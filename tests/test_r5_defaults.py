import sys

import pytest
from pydantic import ValidationError
from signalpost import cli
from signalpost.config import Config


def test_seven_flag_evaluator_command_uses_tested_caps(tmp_path, monkeypatch):
    seen = []

    async def capture(config):
        seen.append(config)
        return dict(emitted_envelopes=100, invalid_inputs=[], requests=0,
                    runtime_ms=0, changes=0, observation_changes=0,
                    deadline_hits=0, warnings=[])

    monkeypatch.setattr(cli, 'run', capture)
    monkeypatch.setattr(sys, 'argv', ['signalpost', 'run',
        '--organisations', str(tmp_path/'companies.jsonl'),
        '--bulk', str(tmp_path/'registry.csv'),
        '--output', str(tmp_path/'out/envelopes.jsonl'),
        '--profiles-output', str(tmp_path/'out/profiles.jsonl'),
        '--report', str(tmp_path/'out/report.json'),
        '--run-id', 'evaluator-seven-flags', '--expected-count', '100'])
    assert cli.main() == 0
    assert len(seen) == 1
    config = seen[0]
    assert (config.website_request_cap, config.website_total_request_cap) == (8, 13)
    assert config.site_dir == tmp_path/'out/site'
    assert config.websites and config.hiring and config.public_activity


@pytest.mark.parametrize('overrides', [
    {'website_request_cap': 9}, {'website_total_request_cap': 14},
    {'website_request_cap': -1}, {'website_total_request_cap': -1},
])
def test_library_rejects_caps_outside_tested_bounds(overrides):
    with pytest.raises(ValidationError):
        Config(organisations='input', output='out', report='report', **overrides)


def test_lower_caps_remain_available():
    config = Config(organisations='input', output='out', report='report',
                    website_request_cap=6, website_total_request_cap=9)
    assert (config.website_request_cap, config.website_total_request_cap) == (6, 9)
