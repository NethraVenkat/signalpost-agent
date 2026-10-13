from typing import Any
from pydantic import Field, model_validator
from .evidence import Model
from .states import Availability


class Claim(Model):
    field: str
    value: Any
    availability: Availability
    confidence: float = Field(default=1.0, ge=0, le=1)
    evidence_ids: list[str] = Field(default_factory=list)
    id: str
    family: str
    reporting_period: dict | None = None
    carried_forward: bool = False
    first_observed_at: str
    last_observed_at: str
    reasons: dict[str, str] = Field(default_factory=dict)

    @model_validator(mode="after")
    def available_has_evidence(self):
        if self.availability == "available" and (self.value is None or not self.evidence_ids):
            raise ValueError("Available claims require a value and evidence")
        if self.availability != "available" and self.value is not None:
            raise ValueError("Unavailable claim values must be null")
        return self
