"""Atomic progress writer for the pipeline.

Writes state/progress.json periodically during pipeline execution.
Never alters evaluator output, stdout, evidence, or deterministic results.
Never exposes secrets or source bodies.
"""
from __future__ import annotations

import asyncio
import json
import os
import tempfile
import time
from pathlib import Path

from .models.evidence import utc_now
from .models.progress import (
    ActivityEvent,
    CompanyCounts,
    ProgressState,
    RequestMetrics,
    StageStatus,
)


# Bounded activity log
MAX_ACTIVITY_EVENTS = 20


class ProgressWriter:
    """Collects pipeline events and writes periodic atomic snapshots.

    The writer runs as an asyncio background task. All public methods
    are thread-safe only in the sense that they are called from the
    async event loop. Writes use atomic rename to avoid torn reads.
    """

    def __init__(
        self,
        state_dir: Path,
        run_id: str,
        total_companies: int,
        input_rows: int,
        duplicate_inputs: int,
        request_limit: int | None,
        stages: list[str] | None = None,
    ):
        self.path = state_dir / "progress.json"
        self._task: asyncio.Task | None = None
        self._lock = asyncio.Lock()

        # Immutable run metadata
        self._run_id = run_id
        self._start_time = utc_now()
        self._start_mono = time.monotonic()

        # Company tracking
        self._total = total_companies
        self._successful: set[str] = set()
        self._failed: set[str] = set()
        self._in_flight: set[str] = set()

        # Request tracking
        self._request_limit = request_limit

        # Stage tracking
        stage_names = stages or [
            "Registry & Subunits",
            "Website Verification",
            "NAV Hiring Matching",
            "Cited Synthesis",
            "Output & Site Publishing",
        ]
        self._stages = {name: "queued" for name in stage_names}
        self._stage_order = stage_names

        # Activity log (bounded circular buffer)
        self._activity: list[ActivityEvent] = []

        # Input metadata
        self._input_rows = input_rows
        self._duplicate_inputs = duplicate_inputs

        # Cost tracking
        self._estimated_cost_usd = 0.0

        # Terminal flag
        self._terminal = False

    def _snapshot(self, budget_events_count: int = 0) -> ProgressState:
        """Build a snapshot of current state. Must be called from event loop."""
        queued = self._total - len(self._successful) - len(self._failed) - len(self._in_flight)
        return ProgressState(
            schema_version=1,
            run_id=self._run_id,
            status="completed" if self._terminal and not self._failed
                   else "failed" if self._terminal and self._failed
                   else "running",
            start_time=self._start_time,
            heartbeat=utc_now(),
            elapsed_seconds=round(time.monotonic() - self._start_mono, 2),
            companies=CompanyCounts(
                total=self._total,
                queued=max(0, queued),
                in_flight=len(self._in_flight),
                successful=len(self._successful),
                failed=len(self._failed),
            ),
            stages=[
                StageStatus(name=name, state=self._stages[name])
                for name in self._stage_order
            ],
            requests=RequestMetrics(
                measured=budget_events_count,
                limit=self._request_limit,
                estimated_cost_usd=self._estimated_cost_usd,
            ),
            activity_log=list(self._activity[-6:]),  # Last 6 for the panel
            input_rows=self._input_rows,
            duplicate_inputs=self._duplicate_inputs,
        )

    def _write_atomic(self, data: str) -> None:
        """Write JSON to progress.json atomically using rename."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(
            dir=str(self.path.parent), suffix=".tmp", prefix=".progress-"
        )
        try:
            os.write(fd, data.encode("utf-8"))
            os.close(fd)
            fd = -1
            # On Windows, target must not exist for rename
            try:
                os.replace(tmp, str(self.path))
            except OSError:
                # Fallback: remove then rename
                try:
                    os.unlink(str(self.path))
                except OSError:
                    pass
                os.rename(tmp, str(self.path))
        except Exception:
            if fd >= 0:
                os.close(fd)
            try:
                os.unlink(tmp)
            except OSError:
                pass

    async def _periodic(self, budget) -> None:
        """Background task: write progress every 2 seconds."""
        try:
            while not self._terminal:
                await asyncio.sleep(2)
                async with self._lock:
                    count = len(budget.events) if budget else 0
                    snapshot = self._snapshot(count)
                try:
                    data = snapshot.model_dump_json(indent=2)
                    await asyncio.get_event_loop().run_in_executor(
                        None, self._write_atomic, data
                    )
                except Exception:
                    pass  # Progress reporting must not disrupt the pipeline
        except asyncio.CancelledError:
            pass

    def start(self, budget) -> None:
        """Start the periodic writer as a background task."""
        self._task = asyncio.create_task(self._periodic(budget))

    async def stop(self, budget=None) -> None:
        """Stop the writer and write a final snapshot."""
        self._terminal = True
        if self._task:
            self._task.cancel()
            await asyncio.gather(self._task, return_exceptions=True)
            self._task = None
        # Final snapshot
        try:
            count = len(budget.events) if budget else 0
            snapshot = self._snapshot(count)
            data = snapshot.model_dump_json(indent=2)
            await asyncio.get_event_loop().run_in_executor(
                None, self._write_atomic, data
            )
        except Exception:
            pass

    # ---- Event recording ----

    def company_started(self, org: str) -> None:
        self._in_flight.add(org)

    def company_completed(self, org: str, success: bool = True) -> None:
        self._in_flight.discard(org)
        if success:
            self._successful.add(org)
        else:
            self._failed.add(org)

    def stage_update(self, name: str, state: str) -> None:
        if name in self._stages:
            self._stages[name] = state

    def log_event(self, message: str) -> None:
        event = ActivityEvent(
            timestamp=round(time.monotonic() - self._start_mono, 2),
            message=message[:200],  # Bounded message length
        )
        self._activity.append(event)
        if len(self._activity) > MAX_ACTIVITY_EVENTS:
            self._activity = self._activity[-MAX_ACTIVITY_EVENTS:]

    def set_cost(self, cost_usd: float) -> None:
        self._estimated_cost_usd = cost_usd
