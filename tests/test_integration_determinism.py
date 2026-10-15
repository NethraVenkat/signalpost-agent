"""
Integration determinism verification:
Runs production replay twice with isolated directories and validates
that all output envelopes, claims, values, availability states, and
syntheses are 100% semantically identical.
"""
import asyncio
import json
from pathlib import Path
import pytest

from scripts.production_replay import run_production_replay


def test_production_replay_determinism_across_runs(tmp_path):
    input_csv = Path("tests/fixtures/integration_declared_batch.csv")
    manifest_path = Path("tests/fixtures/integration_bundle/manifest.json")
    fixtures_dir = Path("tests/fixtures/integration_bundle/blobs")

    # Isolated paths for Run 1
    dir1 = tmp_path / "run1"
    dir1.mkdir(parents=True)
    out1 = dir1 / "envelopes.jsonl"
    rep1 = dir1 / "report.json"

    # Isolated paths for Run 2
    dir2 = tmp_path / "run2"
    dir2.mkdir(parents=True)
    out2 = dir2 / "envelopes.jsonl"
    rep2 = dir2 / "report.json"

    async def execute_runs():
        r1 = await run_production_replay(
            input_path=input_csv,
            output_envelopes=out1,
            output_report=rep1,
            state_dir=dir1 / "state",
            manifest_path=manifest_path,
            fixtures_dir=fixtures_dir,
            bulk=input_csv,
            websites=False,
            hiring=False,
            workers=1,
        )
        r2 = await run_production_replay(
            input_path=input_csv,
            output_envelopes=out2,
            output_report=rep2,
            state_dir=dir2 / "state",
            manifest_path=manifest_path,
            fixtures_dir=fixtures_dir,
            bulk=input_csv,
            websites=False,
            hiring=False,
            workers=1,
        )
        return r1, r2

    asyncio.run(execute_runs())

    assert out1.exists()
    assert out2.exists()

    lines1 = [json.loads(l) for l in out1.read_text(encoding="utf-8-sig").splitlines() if l.strip()]
    lines2 = [json.loads(l) for l in out2.read_text(encoding="utf-8-sig").splitlines() if l.strip()]

    # Multiplicity & order check: 4 input rows (excluding header) -> 4 envelopes
    assert len(lines1) == len(lines2) == 4
    for env1, env2 in zip(lines1, lines2):
        assert env1["organisation_number"] == env2["organisation_number"]

        claims1 = sorted([(c["field"], json.dumps(c.get("value"), sort_keys=True), c.get("availability")) for c in env1.get("claims", [])])
        claims2 = sorted([(c["field"], json.dumps(c.get("value"), sort_keys=True), c.get("availability")) for c in env2.get("claims", [])])
        assert claims1 == claims2, f"Claims mismatch for org {env1['organisation_number']}"

        # Synthesis check
        syn1 = env1.get("run", {}).get("synthesis", {}).get("summary")
        syn2 = env2.get("run", {}).get("synthesis", {}).get("summary")
        assert syn1 == syn2, f"Synthesis mismatch for org {env1['organisation_number']}"
