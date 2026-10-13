import base64
import json
from dataclasses import dataclass, field
from ..models.claim import Claim
from ..models.evidence import Evidence, canonical, digest, utc_now
from ..models.envelope import Error
from .excerpt import excerpt


@dataclass
class Section:
    state: str = "available"
    claims: list = field(default_factory=list)
    evidence: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    retries: int = 0


@dataclass
class Source:
    url: str
    body: bytes
    sha: str
    retrieved_at: str
    identifier: str | None = None


def add(section, source, org, family, field_name, value, locator, reporting=None, availability=None, effective=None, span=None, source_class="official_registry", method="signalpost.registry.v1",id_reporting=None):
    if value == "" or value == [] or value == {}:
        value = None
    state = availability or ("available" if value is not None else "not_available")
    evid = Evidence(id=digest([source.url, source.sha, locator, method]), source_url=source.url,
                    source_class=source_class, retrieved_at=source.retrieved_at, content_sha256=source.sha,
                    claim_span=span if span is not None else excerpt(source.body, value, locator), locator=locator, source_identifier=source.identifier,
                    extraction_method=method,
                    effective_at=effective, reporting_period=reporting)
    value = value if state == "available" else None
    claim = Claim(field=field_name, value=value, availability=state, evidence_ids=[evid.id],
                  id=digest([org, field_name, canonical(value), state, id_reporting if id_reporting is not None else reporting]), family=family,
                  reporting_period=reporting, first_observed_at=source.retrieved_at, last_observed_at=source.retrieved_at)
    section.evidence.append(evid)
    section.claims.append(claim)


def finish(section):
    if section.claims and not any(c.availability == "available" for c in section.claims):
        section.state = "not_available"
    return section


def missing(family, code, message=None, state="failed"):
    return Section(state=state, errors=[Error(section=family, code=code, message=message or code)])


def get(data, path):
    for key in path:
        if not isinstance(data, dict):
            return None
        data = data.get(key)
    return data


def response_source(response):
    return Source(response.url, response.body, response.sha, response.retrieved_at)


def decode(response, family):
    if response.status in (404, 410):
        return None, missing(family, "not_in_registry" if family == "identity" else "not_available", state="not_available")
    if response.status in (401, 403, 429):
        return None, missing(family, "http_blocked", f"HTTP {response.status}", "blocked")
    if response.status != 200:
        return None, missing(family, "source_error", f"HTTP {response.status}")
    return json.loads(response.body), None
