import json
import os
from pathlib import Path
from ..models.envelope import Envelope
from ..models.shapes import serialize, validate
from ..sources.blobstore import BlobStore
from collections import Counter
from ..models.envelope import Error, CompactProfile
from ..models.claim import Claim
from ..models.evidence import digest


def constrain(envelopes, shape, max_output_mb):
    def encode(e):
        return json.dumps(serialize(e, shape), ensure_ascii=False, separators=(",", ":"), allow_nan=False) + "\n"
    unique = {id(e): e for e in envelopes}
    copies = Counter(id(e) for e in envelopes)
    lines = {key: encode(e) for key, e in unique.items()}
    sizes = {key: len(line.encode("utf8")) for key, line in lines.items()}
    total = sum(sizes[key] * copies[key] for key in unique)
    ceiling = int(max_output_mb * 1024 * 1024)
    limited = []
    for key in sorted(unique, key=lambda k: sizes[k], reverse=True):
        if total <= ceiling:
            break
        e = unique[key]
        e.claims = [Claim(field=f + ".section", value=None, availability="failed", confidence=0,
                         evidence_ids=[], id=digest([e.organisation_number, f + ".section", None, "failed", None]),
                         family=f, first_observed_at=e.started_at, last_observed_at=e.completed_at)
                    for f in e.run.sections]
        e.evidence, e.changes = [], []
        e.errors.append(Error(section="output", code="budget_exhausted", message="Envelope reduced to terminal placeholders by max-output-mb"))
        e.run.sections = {f: "failed" for f in e.run.sections}
        e.run.legal_identity = {}
        e.run.terminal_status = "failed"
        e.state = "budget_exhausted"
        for module in e.modules.values():
            module.state = "budget_exhausted"
        e.profile = CompactProfile(organisation_number=e.organisation_number, values={c.field: None for c in e.claims}, evidence_ids=[])
        from ..synthesis.template import generate
        e.run.synthesis=generate(e)
        e.profile.synthesis=e.run.synthesis
        new_line = encode(e)
        new_size = len(new_line.encode("utf8"))
        total += (new_size - sizes[key]) * copies[key]
        lines[key], sizes[key] = new_line, new_size
        limited.append(e.organisation_number)
    return lines, limited, total > ceiling


def write(path: Path, envelopes, shape, blobs, max_output_mb=64):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    bodies = {}
    for envelope in envelopes:
        if envelope.run.synthesis is not None:
            from ..synthesis.validate import validate_synthesis
            envelope.run.synthesis=validate_synthesis(envelope.run.synthesis,envelope)
            envelope.profile.synthesis=envelope.run.synthesis
        for evidence in envelope.evidence:
            target = blobs.directory / evidence.content_sha256
            if target.exists():
                if evidence.content_sha256 not in bodies:
                    bodies[evidence.content_sha256] = target.read_bytes().decode("utf8", errors="replace")
                if evidence.claim_span not in bodies[evidence.content_sha256]:
                    raise ValueError("Evidence excerpt is not verbatim source text")
    lines, limited, minimum_exceeded = constrain(envelopes, shape, max_output_mb)
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        for envelope in envelopes:
            Envelope.model_validate(envelope.model_dump())
            handle.write(lines[id(envelope)])
        handle.flush()
        os.fsync(handle.fileno())
    expected = [e.organisation_number for e in envelopes]
    actual = []
    with temporary.open(encoding="utf-8") as handle:
        for line in handle:
            body = json.loads(line)
            validate(body, shape)
            actual.append(body["organisation_number"])
    if actual != expected:
        raise ValueError("Output membership/order differs from input")
    os.replace(temporary, path)
    return path.stat().st_size, limited, minimum_exceeded


def previous(path):
    if path is None:
        return {}, []
    rows, warnings = {}, []
    try:
        with path.open(encoding="utf-8-sig") as handle:
            for n, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                    shape = "union" if "profile" in row and "claims" in row else "reference" if "profile" in row else "contract"
                    validate(row, shape)
                    rows[row["organisation_number"]] = row
                except Exception as exc:
                    warnings.append(f"previous line {n} rejected: {type(exc).__name__}")
    except Exception as exc:
        warnings.append(f"previous file unreadable: {type(exc).__name__}")
    return rows, warnings
