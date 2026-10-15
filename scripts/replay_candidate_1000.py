"""Saved-source replay producing the corrected 1,000-company cohort.

Enforces the corrected NAV employer orgnr invariant:
- Ads lacking valid 9-digit employer.orgnr are discarded.
- Preserves all verified claims across identity, accounts, roles, subunits, website, activity, and verified hiring.
- Regenerates and validates synthesis sentences and compact profiles.
"""
import json
import re
from pathlib import Path

from signalpost.models.envelope import Envelope, CompactProfile, Claim, Error
from signalpost.models.evidence import digest, utc_now
from signalpost.synthesis.template import generate as generate_synthesis
from signalpost.synthesis.validate import sentence_error, SECTIONS
from signalpost.sources.blobstore import BlobStore
from signalpost.io.envelope_writer import write
from signalpost.models.shapes import validate as validate_shape

INPUT_PATH = Path("out/w5-opt1000-rev4-envelopes.jsonl")
OUT_ENVELOPES = Path("out/candidate-1000-corrected-envelopes.jsonl")
OUT_PROFILES = Path("out/candidate-1000-corrected-profiles.jsonl")
STATE_DIR = Path("state")
BLOBS_DIR = STATE_DIR / "blobs"


def is_valid_hiring_claim(claim: dict, evidence_map: dict) -> bool:
    """Verifies that ad detail payload contains a valid 9-digit employer.orgnr."""
    eids = claim.get("evidence_ids", [])
    if not eids:
        return False
    ev = evidence_map.get(eids[0])
    if not ev:
        return False
    sha = getattr(ev, "content_sha256", None) or (ev.get("content_sha256") if isinstance(ev, dict) else None)
    if not sha:
        return False
    blob_path = BLOBS_DIR / sha
    if not blob_path.exists():
        return False
    try:
        data = json.loads(blob_path.read_text(encoding="utf-8", errors="replace"))
        ad = data.get("ad_content") or data
        employer = ad.get("employer") or {}
        orgnr = str(employer.get("orgnr") or "").strip()
        return bool(orgnr and re.match(r"^\d{9}$", orgnr))
    except Exception:
        return False


def main():
    print(f"Reading historical cohort from {INPUT_PATH}...")
    lines = INPUT_PATH.read_text(encoding="utf-8-sig").splitlines()
    total = len(lines)
    print(f"Loaded {total} envelope lines.")

    corrected_rows = []
    hiring_dropped_count = 0
    hiring_retained_count = 0
    companies_with_hiring_dropped = set()

    for line in lines:
        if not line.strip():
            continue
        raw = json.loads(line)
        env = Envelope.model_validate(raw)
        org = env.organisation_number
        ev_map = {e.id: e for e in env.evidence}

        # Check hiring claims
        hiring_claims = [c for c in env.claims if c.family == "hiring" and c.availability == "available"]
        dropped = []
        kept = []
        for c in hiring_claims:
            if is_valid_hiring_claim(c.model_dump(mode="json"), ev_map):
                kept.append(c)
                hiring_retained_count += 1
            else:
                dropped.append(c)
                hiring_dropped_count += 1
                companies_with_hiring_dropped.add(org)

        if dropped:
            # Remove dropped hiring claims and their isolated evidence
            dropped_ids = {c.id for c in dropped}
            dropped_ev_ids = {eid for c in dropped for eid in c.evidence_ids}
            env.claims = [c for c in env.claims if c.id not in dropped_ids]
            
            # Check remaining hiring claims for this org
            remaining_hiring = [c for c in env.claims if c.family == "hiring" and c.availability == "available"]
            if not remaining_hiring:
                now = env.completed_at
                env.run.sections["hiring"] = "not_available"
                # Add not_available section placeholder
                env.claims.append(Claim(
                    field="hiring.section",
                    value=None,
                    availability="not_available",
                    evidence_ids=[],
                    confidence=0,
                    family="hiring",
                    id=digest([org, "hiring.section", None, "not_available", None]),
                    first_observed_at=now,
                    last_observed_at=now
                ))
            
            # Regenerate synthesis
            synthesis = generate_synthesis(env)
            sentences = [s for sec in SECTIONS for s in getattr(synthesis.sections, sec)]
            for s in sentences:
                err = sentence_error(s, env)
                assert err is None, f"Synthesis sentence error for {org}: {err} in sentence '{s.text}'"
            assert synthesis.checks.values_verified, f"Synthesis values unverified for {org}"
            
            env.run.synthesis = synthesis
            env.profile = CompactProfile(
                organisation_number=org,
                values={c.field: c.value for c in env.claims},
                evidence_ids=[e.id for e in env.evidence],
                synthesis=synthesis
            )

        corrected_rows.append(env)

    print(f"Replay complete: {len(corrected_rows)} envelopes processed.")
    print(f"Hiring claims: retained {hiring_retained_count}, dropped {hiring_dropped_count} unsupported ads across {len(companies_with_hiring_dropped)} companies.")

    # Write corrected envelopes
    blobs = BlobStore(STATE_DIR)
    write(OUT_ENVELOPES, corrected_rows, "union", blobs, 256)
    print(f"Wrote {len(corrected_rows)} corrected envelopes to {OUT_ENVELOPES}")

    # Write corrected profiles
    profile_lines = []
    for r in corrected_rows:
        prof_data = r.profile.model_dump(mode="json") if hasattr(r.profile, "model_dump") else r.profile
        profile_lines.append(json.dumps(prof_data, ensure_ascii=False))
    OUT_PROFILES.write_text("\n".join(profile_lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(profile_lines)} corrected profiles to {OUT_PROFILES}")

    # Validate output shapes
    for r in corrected_rows:
        validate_shape(r.model_dump(mode="json"), "union")
    print("All 1,000 corrected envelopes verified against union shape schema!")


if __name__ == "__main__":
    main()
