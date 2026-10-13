from .evidence import Model, Evidence
from .claim import Claim
from .envelope import Run, Change, Error, Operations, Module, Envelope, Profile
from .states import TerminalState

CONTRACT_KEYS = {"organisation_number", "run", "claims", "evidence", "changes", "errors", "operations"}
REFERENCE_KEYS = {"run_id", "organisation_number", "state", "started_at", "completed_at", "modules", "profile"}


class Contract(Model):
    organisation_number: str
    run: Run
    claims: list[Claim]
    evidence: list[Evidence]
    changes: list[Change]
    errors: list[Error]
    operations: Operations


class Reference(Model):
    run_id: str
    organisation_number: str
    state: TerminalState
    started_at: str
    completed_at: str
    modules: dict[str, Module]
    profile: Profile


def serialize(envelope: Envelope, shape: str):
    data = envelope.model_dump(mode="json")
    if shape == "contract":
        data = {k: v for k, v in data.items() if k in CONTRACT_KEYS}
    elif shape == "reference":
        data["profile"] = Profile(organisation_number=envelope.organisation_number,
                                  legal_identity=envelope.run.legal_identity, claims=envelope.claims,
                                  evidence=envelope.evidence, changes=envelope.changes, errors=envelope.errors,
                                  refresh=envelope.run.refresh, sections=envelope.run.sections,
                                  operations=envelope.operations,synthesis=envelope.run.synthesis).model_dump(mode="json")
        data = {k: v for k, v in data.items() if k in REFERENCE_KEYS}
    validate(data, shape)
    return data


def validate(data, shape):
    if shape == "union":
        return Envelope.model_validate(data)
    if shape == "contract":
        parsed = Contract.model_validate(data)
        claims, evidence, changes = parsed.claims, parsed.evidence, parsed.changes
    else:
        parsed = Reference.model_validate(data)
        claims = parsed.profile.claims
        evidence = parsed.profile.evidence
        changes = parsed.profile.changes
    ids = {e.id for e in evidence}
    if any(set(c.evidence_ids) - ids for c in claims) or any(set(c.old_evidence_ids + c.new_evidence_ids) - ids for c in changes):
        raise ValueError("Dangling evidence reference")
    return parsed
