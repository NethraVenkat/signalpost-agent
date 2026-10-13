from typing import Any
from pydantic import Field, model_validator
from .evidence import Model, Evidence
from .claim import Claim
from .states import Availability, TerminalState


class Error(Model):
    section: str
    code: str
    message: str


class Module(Model):
    state: TerminalState
    retry_count: int = 0
    final_timestamp: str


class Operations(Model):
    requests: int = 0
    runtime_ms: int = 0
    third_party_cost_usd: float = 0


class Run(Model):
    run_id: str
    started_at: str
    completed_at: str
    terminal_status: str = "completed"
    legal_identity: dict = Field(default_factory=dict)
    refresh: dict = Field(default_factory=dict)
    sections: dict[str, Availability] = Field(default_factory=dict)


class Change(Model):
    organisation_number: str
    type: str
    field: str
    old_value: Any
    new_value: Any
    old_evidence_ids: list[str]
    new_evidence_ids: list[str]
    materiality: str
    first_observed_at: str
    last_observed_at: str
    source_url: str | None = None
    retrieved_at: str | None = None
    effective_at: str | None = None
    source_class: str | None = None
    old_content_sha256: str | None = None
    new_content_sha256: str | None = None
    status: Availability


class Profile(Model):
    organisation_number: str = ""
    legal_identity: dict = Field(default_factory=dict)
    claims: list[Claim] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)
    changes: list[Change] = Field(default_factory=list)
    errors: list[Error] = Field(default_factory=list)
    refresh: dict = Field(default_factory=dict)
    sections: dict[str, Availability] = Field(default_factory=dict)
    operations: Operations = Field(default_factory=Operations)


class CompactProfile(Model):
    organisation_number: str
    values: dict
    evidence_ids: list[str]


class Envelope(Model):
    organisation_number: str
    run: Run
    claims: list[Claim]
    evidence: list[Evidence]
    changes: list[Change]
    errors: list[Error]
    operations: Operations
    run_id: str
    state: TerminalState
    started_at: str
    completed_at: str
    modules: dict[str, Module]
    profile: CompactProfile | Profile

    @model_validator(mode="after")
    def evidence_links(self):
        ids = {e.id for e in self.evidence}
        if len(ids) != len(self.evidence):
            raise ValueError("Duplicate evidence IDs")
        if len({c.field for c in self.claims}) != len(self.claims):
            raise ValueError("Duplicate claim fields")
        for claim in self.claims:
            if set(claim.evidence_ids) - ids:
                raise ValueError("Dangling claim evidence")
        for event in self.changes:
            if set(event.old_evidence_ids + event.new_evidence_ids) - ids:
                raise ValueError("Dangling change evidence")
        return self
