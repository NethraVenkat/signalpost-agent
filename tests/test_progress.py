import asyncio
import json
import pytest
from pathlib import Path
from signalpost.models.progress import ProgressState, StageStatus, CompanyCounts
from signalpost.progress import ProgressWriter


def test_progress_state_schema_and_serialization(tmp_path):
    writer = ProgressWriter(
        state_dir=tmp_path,
        run_id="run-12345",
        total_companies=10,
        input_rows=12,
        duplicate_inputs=2,
        request_limit=200,
        stages=["Stage 1", "Stage 2"],
    )
    writer.company_started("123456789")
    writer.company_completed("123456789", success=True)
    writer.company_started("987654321")
    writer.company_completed("987654321", success=False)
    writer.stage_update("Stage 1", "completed")
    writer.log_event("Event A happened")
    writer.set_cost(0.025)

    snap = writer._snapshot(budget_events_count=5)
    assert snap.run_id == "run-12345"
    assert snap.companies.total == 10
    assert snap.companies.successful == 1
    assert snap.companies.failed == 1
    assert snap.companies.in_flight == 0
    assert snap.companies.queued == 8
    assert snap.companies.terminal == 2
    assert snap.requests.measured == 5
    assert snap.requests.limit == 200
    assert snap.requests.estimated_cost_usd == 0.025
    assert len(snap.activity_log) == 1
    assert snap.activity_log[0].message == "Event A happened"
    assert snap.input_rows == 12
    assert snap.duplicate_inputs == 2

    # Verify atomic write
    writer._write_atomic(snap.model_dump_json(indent=2))
    assert (tmp_path / "progress.json").exists()
    loaded = json.loads((tmp_path / "progress.json").read_text(encoding="utf-8"))
    assert loaded["schema_version"] == 1
    assert loaded["run_id"] == "run-12345"


@pytest.mark.anyio
async def test_progress_writer_lifecycle(tmp_path):
    class FakeBudget:
        events = [{"url": "http://test"}]

    writer = ProgressWriter(
        state_dir=tmp_path,
        run_id="run-life",
        total_companies=5,
        input_rows=5,
        duplicate_inputs=0,
        request_limit=100,
    )
    writer.start(FakeBudget())
    writer.company_started("111222333")
    writer.stage_update("Registry & Subunits", "running")
    writer.log_event("Processing started")
    await asyncio.sleep(0.1)
    await writer.stop(FakeBudget())

    assert (tmp_path / "progress.json").exists()
    data = json.loads((tmp_path / "progress.json").read_text(encoding="utf-8"))
    assert data["status"] in ("completed", "failed")
    assert data["run_id"] == "run-life"
