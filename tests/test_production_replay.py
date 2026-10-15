"""
Tests proving the production offline replay transport and runner execution.
"""
import asyncio
import json
import pytest
from pathlib import Path
import httpx

from scripts.production_replay import RecordedResponseTransport, build_fixture_map_from_envelopes
from signalpost.config import Config
from signalpost.runner import run as runner_run


def test_recorded_response_transport_serves_blobs(tmp_path):
    blobs_dir = tmp_path / "blobs"
    blobs_dir.mkdir(parents=True)
    blob_sha = "abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234"
    (blobs_dir / blob_sha).write_text(json.dumps({"organisasjonsnummer": "999592236", "navn": "TEST AS"}), encoding="utf-8")

    robots_sha = "bbbb1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234"
    (blobs_dir / robots_sha).write_text("User-agent: *\nDisallow: /admin\n", encoding="utf-8")

    fixture_map = {
        "https://data.brreg.no/enhetsregisteret/api/enheter/999592236": blob_sha,
        "https://example.no/robots.txt": robots_sha,
    }
    transport = RecordedResponseTransport(blobs_dir, fixture_map)

    async def check():
        async with httpx.AsyncClient(transport=transport) as client:
            # 1. Recorded Robots.txt served faithfully
            r_robots = await client.get("https://example.no/robots.txt")
            assert r_robots.status_code == 200
            assert "Disallow: /admin" in r_robots.text

            # 2. Known fixture
            r_fixture = await client.get("https://data.brreg.no/enhetsregisteret/api/enheter/999592236")
            assert r_fixture.status_code == 200
            data = r_fixture.json()
            assert data["navn"] == "TEST AS"

            # 3. Unknown URL / unrecorded robots.txt fails closed
            r_unknown = await client.get("https://evil.test/unrecorded")
            assert r_unknown.status_code == 404
            assert "https://evil.test/unrecorded" in transport.unexpected_requests

    asyncio.run(check())


def test_production_runner_with_offline_transport(tmp_path):
    blobs_dir = tmp_path / "blobs"
    blobs_dir.mkdir(parents=True)
    blob_sha = "1111222233334444555566667777888899990000aaaabbbbccccddddeeeeffff"
    entity_data = {
        "organisasjonsnummer": "999592236",
        "navn": "AUTONEXT AS",
        "organisasjonsform": {"kode": "AS", "beskrivelse": "Aksjeselskap"},
        "forretningsadresse": {"kommune": "VEFSN", "kommunenummer": "1824"},
        "antallAnsatte": 5,
        "konkurs": False
    }
    (blobs_dir / blob_sha).write_text(json.dumps(entity_data), encoding="utf-8")

    input_file = tmp_path / "input.txt"
    input_file.write_text("999592236\n", encoding="utf-8")

    fixture_map = {
        "https://data.brreg.no/enhetsregisteret/api/enheter/999592236": blob_sha
    }
    transport = RecordedResponseTransport(blobs_dir, fixture_map)

    out_env = tmp_path / "envelopes.jsonl"
    out_rep = tmp_path / "report.json"

    cfg = Config(
        organisations=input_file,
        output=out_env,
        report=out_rep,
        state_dir=tmp_path,
        workers=1,
        time_budget_seconds=30,
        websites=False,
        hiring=False
    )

    async def execute():
        async with httpx.AsyncClient(transport=transport, trust_env=False) as client:
            return await runner_run(cfg, client=client)

    rep = asyncio.run(execute())
    assert out_env.exists()
    rows = [json.loads(line) for line in out_env.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 1
    assert rows[0]["organisation_number"] == "999592236"
    assert rows[0]["run"]["sections"]["identity"] == "available"
