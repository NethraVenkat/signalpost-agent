import base64
import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Any
from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from pydantic import Field


def utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical(value: Any):
    if isinstance(value, str):
        return " ".join(value.split()).casefold()
    if isinstance(value, list):
        return sorted((canonical(x) for x in value), key=lambda x: json.dumps(x, sort_keys=True, ensure_ascii=False))
    if isinstance(value, dict):
        return {k: canonical(v) for k, v in sorted(value.items())}
    return value


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


class Model(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class Evidence(Model):
    id: str
    source_url: str
    source_class: str
    retrieved_at: str
    content_sha256: str
    claim_span: str
    locator: str
    extraction_method: str = "signalpost.registry.v1"
    source_identifier: str | None = None
    effective_at: str | None = None
    reporting_period: dict | None = None
    snapshot_body_base64: str | None = Field(default=None, exclude=True)

    @field_validator("retrieved_at")
    @classmethod
    def timestamp(cls, value):
        if not value.endswith("Z"):
            raise ValueError("retrieved_at must be UTC Z")
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return value

    @model_validator(mode="after")
    def body_hash(self):
        if not re.fullmatch("[0-9a-f]{64}", self.content_sha256):
            raise ValueError("Invalid source hash")
        if self.snapshot_body_base64 is not None:
            body = base64.b64decode(self.snapshot_body_base64, validate=True)
            if hashlib.sha256(body).hexdigest() != self.content_sha256:
                raise ValueError("Snapshot hash mismatch")
        if len(self.claim_span) > 300 and self.snapshot_body_base64 is None:
            raise ValueError("Excerpt exceeds 300 characters")
        expected = digest([self.source_url, self.content_sha256, self.locator, self.extraction_method])
        if expected != self.id:
            raise ValueError("Evidence ID mismatch")
        return self
