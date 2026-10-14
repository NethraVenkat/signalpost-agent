"""Pipeline progress data model. Used only for status reporting, never alters evaluator output."""
from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any


class StageStatus(BaseModel):
    name: str
    state: str = "queued"  # queued | running | completed | failed


class CompanyCounts(BaseModel):
    total: int = 0
    queued: int = 0
    in_flight: int = 0
    successful: int = 0
    failed: int = 0

    @property
    def terminal(self) -> int:
        return self.successful + self.failed


class RequestMetrics(BaseModel):
    measured: int = 0
    limit: int | None = None
    estimated_cost_usd: float = 0.0


class ActivityEvent(BaseModel):
    timestamp: float
    message: str


class ProgressState(BaseModel):
    """Atomic pipeline progress snapshot.

    Written periodically by the runner. Never contains secrets,
    source bodies, or values that would alter evaluator output.
    """
    schema_version: int = 1
    run_id: str = ""
    status: str = "running"  # running | completed | failed | interrupted
    start_time: str = ""
    heartbeat: str = ""
    elapsed_seconds: float = 0.0

    companies: CompanyCounts = Field(default_factory=CompanyCounts)
    stages: list[StageStatus] = Field(default_factory=list)
    requests: RequestMetrics = Field(default_factory=RequestMetrics)
    activity_log: list[ActivityEvent] = Field(default_factory=list)

    input_rows: int = 0
    duplicate_inputs: int = 0
