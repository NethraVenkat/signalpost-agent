from signalpost.config import Config
from signalpost import cli


def _invoke(monkeypatch, override):
    observed = {}

    async def fake_run(config):
        observed["config"] = config
        return {"emitted_envelopes": 0, "invalid_inputs": 0, "requests": 0,
                "runtime_ms": 0, "changes": 0, "observation_changes": 0,
                "deadline_hits": 0, "warnings": []}

    monkeypatch.setattr(cli, "run", fake_run)
    monkeypatch.setattr("sys.argv", ["signalpost", "run", "--organisations", "in.jsonl",
                                     "--output", "out.jsonl", "--report", "report.json"])
    if override is None:
        monkeypatch.delenv("SIGNALPOST_WEBSITE_SEEDS", raising=False)
    else:
        monkeypatch.setenv("SIGNALPOST_WEBSITE_SEEDS", override)
    assert cli.main() == 0
    return observed["config"]


def test_website_seeds_default_on_and_can_be_disabled_without_cli_flag(monkeypatch):
    assert Config(organisations="in", output="out", report="report").website_seed_index is True
    assert _invoke(monkeypatch, None).website_seed_index is True
    assert _invoke(monkeypatch, "0").website_seed_index is False
    assert _invoke(monkeypatch, "1").website_seed_index is True
