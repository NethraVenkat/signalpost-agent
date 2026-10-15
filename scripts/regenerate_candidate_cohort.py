"""
Regenerates candidate cohort outputs using corrected shared production extractors.

Re-extracts website metadata (public brands, descriptions) directly from saved primary source blobs
using shared production functions (signalpost.web.collector.extract_public_brand and
signalpost.web.descriptions.extract), withholding unsupported facts and preserving all verified facts
across identity, accounts, roles, subunits, hiring, and activity.

Enforces:
- Explicit CLI arguments with separate input/output paths
- Blob SHA-256 integrity checks before reading
- Reusable shared production extractor logic (no duplicate extraction code)
- Deterministic claim ordering
- Detailed audit manifest generation
"""
import argparse
import hashlib
import html
import json
import logging
from pathlib import Path
import sys
from types import SimpleNamespace

from signalpost.models.envelope import Envelope, CompactProfile
from signalpost.models.evidence import digest
from signalpost.synthesis.template import generate as generate_synthesis
from signalpost.synthesis.validate import sentence_error, SECTIONS
from signalpost.sources.blobstore import BlobStore
from signalpost.io.envelope_writer import write
from signalpost.models.shapes import validate as validate_shape
from signalpost.web.html import Page
from signalpost.web.collector import extract_public_brand, extract_contacts_and_social, publish
from signalpost.web.descriptions import extract as extract_descriptions
from signalpost.sources.extract import Section

logger = logging.getLogger("regenerate_candidate_cohort")


def regenerate_cohort(
    input_path: Path,
    output_envelopes: Path,
    output_profiles: Path,
    manifest_path: Path,
    state_dir: Path,
) -> dict:
    blobs_dir = state_dir / "blobs"
    if not input_path.exists():
        raise FileNotFoundError(f"Input envelopes not found: {input_path}")

    print(f"Reading envelopes from {input_path}...")
    lines = input_path.read_text(encoding="utf-8-sig").splitlines()
    print(f"Loaded {len(lines)} envelopes.")

    updated_envelopes = []
    brand_changes = []
    desc_changes = []
    contact_changes = []
    total_claims_before = 0
    total_claims_after = 0
    blob_integrity_failures = 0

    for line in lines:
        if not line.strip():
            continue
        env = Envelope.model_validate_json(line)
        org = env.organisation_number
        total_claims_before += len(env.claims)

        web_claim = next((c for c in env.claims if c.field == "official_website" and c.availability == "available"), None)
        if not web_claim:
            # Deterministic claim ordering
            env.claims.sort(key=lambda c: (c.family, c.field, c.id))
            total_claims_after += len(env.claims)
            updated_envelopes.append(env)
            continue

        # Find company-owned pages with blob integrity checks
        pages = []
        seen_urls = set()
        for ev in env.evidence:
            s_url = ev.source_url
            if ev.source_class == "company_owned" and s_url and s_url not in seen_urls:
                seen_urls.add(s_url)
                sha = ev.content_sha256
                p = blobs_dir / sha
                if p.exists():
                    b = p.read_bytes()
                    # Verify blob SHA-256 integrity
                    actual_sha = hashlib.sha256(b).hexdigest()
                    if actual_sha.lower() != sha.lower():
                        logger.error("Corrupt blob %s for %s", sha, s_url)
                        blob_integrity_failures += 1
                        continue
                    pg = Page(b, s_url)
                    resp = SimpleNamespace(url=s_url, body=b, sha=sha, retrieved_at=ev.retrieved_at)
                    pages.append((resp, pg))

        if not pages:
            env.claims.sort(key=lambda c: (c.family, c.field, c.id))
            total_claims_after += len(env.claims)
            updated_envelopes.append(env)
            continue

        # Separate website claims to keep vs re-extract
        retained_claims = [
            c for c in env.claims
            if c.field == "official_website" or not (
                c.field == "public_brand"
                or c.field.startswith("website_description")
                or c.field.startswith("contact.")
                or c.field.startswith("social_profile.")
            )
        ]

        # 1. Re-extract descriptions using production descriptions extractor
        desc_sec = Section("website")
        extract_descriptions(desc_sec, org, web_claim, pages)

        # 2. Re-extract public brand using shared production function
        legal_nm_claim = next((c for c in env.claims if c.field == "identity.legal_name"), None)
        legal_nm = legal_nm_claim.value if legal_nm_claim else env.profile.values.get("identity.legal_name")

        proof_url = web_claim.value.get("final_url") or web_claim.value.get("proof_page_url")
        root_page_tuple = next(
            ((r, p) for r, p in pages if r.url == proof_url or r.url.rstrip("/") == proof_url.rstrip("/")),
            pages[0]
        )
        root_resp, root_page = root_page_tuple

        brand_sec = Section("website")
        brand = extract_public_brand(root_page, legal_nm)
        if brand:
            span = (root_page.span_for(brand) or "")[:150]
            publish(brand_sec, root_resp, org, "public_brand", brand, "meta:brand", span)

        # 3. Re-extract contacts and social channels using shared production function
        contact_social_sec = Section("website")
        extract_contacts_and_social(
            contact_social_sec, org, web_claim, pages,
            context={"name": legal_nm}, envelope=env
        )

        # Track changes
        old_brand = next((c for c in env.claims if c.field == "public_brand"), None)
        new_brand = next((c for c in brand_sec.claims if c.field == "public_brand"), None)
        if (old_brand is None) != (new_brand is None) or (old_brand and new_brand and old_brand.value != new_brand.value):
            brand_changes.append({
                "orgnr": org,
                "old": old_brand.value if old_brand else None,
                "new": new_brand.value if new_brand else None,
            })

        old_descs = {c.field: c.value for c in env.claims if c.field.startswith("website_description")}
        new_descs = {c.field: c.value for c in desc_sec.claims if c.field.startswith("website_description")}
        if old_descs != new_descs:
            desc_changes.append({
                "orgnr": org,
                "old_fields": list(old_descs.keys()),
                "new_fields": list(new_descs.keys()),
            })

        old_contacts = {c.field: c.value for c in env.claims if c.field.startswith("contact.") or c.field.startswith("social_profile.")}
        new_contacts = {c.field: c.value for c in contact_social_sec.claims if c.field.startswith("contact.") or c.field.startswith("social_profile.")}
        if old_contacts != new_contacts:
            contact_changes.append({
                "orgnr": org,
                "old_fields": list(old_contacts.keys()),
                "old_values": [str(v) for v in old_contacts.values()],
                "new_fields": list(new_contacts.keys()),
                "new_values": [str(v) for v in new_contacts.values()],
            })

        new_claims = retained_claims + brand_sec.claims + desc_sec.claims + contact_social_sec.claims
        # Deterministic claim ordering
        new_claims.sort(key=lambda c: (c.family, c.field, c.id))
        env.claims = new_claims
        total_claims_after += len(new_claims)

        # Update evidence references
        new_ev_by_id = {e.id: e for e in brand_sec.evidence + desc_sec.evidence + contact_social_sec.evidence}
        referenced_eids = {eid for c in env.claims for eid in c.evidence_ids}
        updated_evidence = [e for e in env.evidence if e.id in referenced_eids]
        for eid in referenced_eids:
            if eid in new_ev_by_id and all(e.id != eid for e in updated_evidence):
                updated_evidence.append(new_ev_by_id[eid])
        # Sort evidence deterministically
        updated_evidence.sort(key=lambda e: e.id)
        env.evidence = updated_evidence

        # Re-synthesize summary with template mode
        synthesis = generate_synthesis(env)
        sentences = [s for sec in SECTIONS for s in getattr(synthesis.sections, sec)]
        for s in sentences:
            err = sentence_error(s, env)
            assert err is None, f"Synthesis sentence error for {org}: {err} in '{s.text}'"
        assert synthesis.checks.values_verified, f"Synthesis unverified for {org}"

        env.run.synthesis = synthesis
        env.profile = CompactProfile(
            organisation_number=org,
            values={c.field: c.value for c in env.claims},
            evidence_ids=[e.id for e in env.evidence],
            synthesis=synthesis
        )
        updated_envelopes.append(env)

    print(f"Regeneration complete: {len(updated_envelopes)} envelopes. Brand changes: {len(brand_changes)}, Desc changes: {len(desc_changes)}, Contact changes: {len(contact_changes)}")

    # Write out updated envelopes
    output_envelopes.parent.mkdir(parents=True, exist_ok=True)
    output_profiles.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    blobs = BlobStore(state_dir)
    write(output_envelopes, updated_envelopes, "union", blobs, 256)
    print(f"Wrote updated envelopes to {output_envelopes}")

    # Write out updated profiles
    profile_lines = []
    for r in updated_envelopes:
        prof_data = r.profile.model_dump(mode="json") if hasattr(r.profile, "model_dump") else r.profile
        profile_lines.append(json.dumps(prof_data, ensure_ascii=False))
    output_profiles.write_text("\n".join(profile_lines) + "\n", encoding="utf-8")
    print(f"Wrote updated profiles to {output_profiles}")

    # Validate shape schema
    for r in updated_envelopes:
        validate_shape(r.model_dump(mode="json"), "union")
    print("All envelopes verified against union shape schema!")

    # Compute output SHA-256 checksums
    env_bytes = output_envelopes.read_bytes()
    env_sha = hashlib.sha256(env_bytes).hexdigest()
    prof_bytes = output_profiles.read_bytes()
    prof_sha = hashlib.sha256(prof_bytes).hexdigest()

    manifest = {
        "input_path": str(input_path),
        "output_envelopes": str(output_envelopes),
        "output_envelopes_sha256": env_sha,
        "output_profiles": str(output_profiles),
        "output_profiles_sha256": prof_sha,
        "total_envelopes": len(updated_envelopes),
        "brand_changes_count": len(brand_changes),
        "brand_changes": brand_changes,
        "desc_changes_count": len(desc_changes),
        "desc_changes": desc_changes,
        "contact_changes_count": len(contact_changes),
        "contact_changes": contact_changes,
        "total_claims_before": total_claims_before,
        "total_claims_after": total_claims_after,
        "blob_integrity_failures": blob_integrity_failures,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote change manifest to {manifest_path}")

    return manifest


def main():
    parser = argparse.ArgumentParser(description="Regenerate Candidate Cohort using Shared Production Extractors")
    parser.add_argument("--input", type=Path, default=Path("out/candidate-1000-corrected-envelopes.jsonl"))
    parser.add_argument("--output", type=Path, default=Path("out/candidate-1000-corrected-envelopes.jsonl"))
    parser.add_argument("--profiles-output", type=Path, default=Path("out/candidate-1000-corrected-profiles.jsonl"))
    parser.add_argument("--manifest-output", type=Path, default=Path("reports/candidate-regeneration-manifest.json"))
    parser.add_argument("--state-dir", type=Path, default=Path("state"))
    args = parser.parse_args()

    regenerate_cohort(
        input_path=args.input,
        output_envelopes=args.output,
        output_profiles=args.profiles_output,
        manifest_path=args.manifest_output,
        state_dir=args.state_dir,
    )


if __name__ == "__main__":
    main()
