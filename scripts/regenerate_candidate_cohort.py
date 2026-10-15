"""
Regenerates candidate cohort outputs using corrected production extractors.
Re-extracts website metadata (public brands, descriptions) directly from saved primary source blobs
using signalpost.web.collector and signalpost.web.descriptions, withholding unsupported facts
and preserving all verified facts across identity, accounts, roles, subunits, hiring, and activity.
"""
import html
import json
import re
from pathlib import Path
from types import SimpleNamespace

from signalpost.models.envelope import Envelope, CompactProfile
from signalpost.models.evidence import digest
from signalpost.synthesis.template import generate as generate_synthesis
from signalpost.synthesis.validate import sentence_error, SECTIONS
from signalpost.sources.blobstore import BlobStore
from signalpost.io.envelope_writer import write
from signalpost.models.shapes import validate as validate_shape
from signalpost.web.html import Page
from signalpost.web.candidates import legal_name
from signalpost.web.descriptions import extract as extract_descriptions
from signalpost.sources.extract import Section

ENVELOPES_PATH = Path("out/candidate-1000-corrected-envelopes.jsonl")
PROFILES_PATH = Path("out/candidate-1000-corrected-profiles.jsonl")
STATE_DIR = Path("state")
BLOBS_DIR = STATE_DIR / "blobs"


def main():
    print(f"Reading envelopes from {ENVELOPES_PATH}...")
    lines = ENVELOPES_PATH.read_text(encoding="utf-8-sig").splitlines()
    print(f"Loaded {len(lines)} envelopes.")

    updated_envelopes = []
    brand_changes = 0
    desc_changes = 0

    for line in lines:
        if not line.strip():
            continue
        env = Envelope.model_validate_json(line)
        org = env.organisation_number

        web_claim = next((c for c in env.claims if c.field == "official_website" and c.availability == "available"), None)
        if not web_claim:
            updated_envelopes.append(env)
            continue

        # Map existing evidence
        ev_map = {e.id: e for e in env.evidence}

        # Find company-owned pages
        pages = []
        seen_urls = set()
        for ev in env.evidence:
            s_url = ev.source_url
            if ev.source_class == "company_owned" and s_url and s_url not in seen_urls:
                seen_urls.add(s_url)
                sha = ev.content_sha256
                p = BLOBS_DIR / sha
                if p.exists():
                    b = p.read_bytes()
                    pg = Page(b, s_url)
                    resp = SimpleNamespace(url=s_url, body=b, sha=sha, retrieved_at=ev.retrieved_at)
                    pages.append((resp, pg))

        if not pages:
            updated_envelopes.append(env)
            continue

        # Separate website claims to keep vs re-extract
        # We keep: official_website, contact.*, social_profile.*
        # We re-extract: public_brand, website_description.*
        retained_claims = [c for c in env.claims if c.field == "official_website" or not (c.field == "public_brand" or c.field.startswith("website_description"))]

        # 1. Re-extract descriptions
        desc_sec = Section("website")
        extract_descriptions(desc_sec, org, web_claim, pages)

        # 2. Re-extract public brand from root proof page
        legal_nm_claim = next((c for c in env.claims if c.field == "identity.legal_name"), None)
        legal_nm = legal_nm_claim.value if legal_nm_claim else env.profile.values.get("identity.legal_name")
        context = {"name": legal_nm}

        proof_url = web_claim.value.get("final_url") or web_claim.value.get("proof_page_url")
        root_page_tuple = next(((r, p) for r, p in pages if r.url == proof_url or r.url.rstrip("/") == proof_url.rstrip("/")), pages[0])
        root_resp, root_page = root_page_tuple

        candidate_brand = root_page.meta.get("og:site_name") or root_page.meta.get("og:sitename")
        if candidate_brand:
            candidate_brand = html.unescape(candidate_brand).strip()
        else:
            parts = [html.unescape(p).strip() for p in re.split(r"\s+[|–-]\s+", root_page.title) if p.strip()]
            if parts:
                generic_store_words = {"nettbutikk", "fiskeutstyr", "båtutstyr", "butikk", "webshop", "forside", "hjem", "velkommen", "home", "shop", "online"}
                p0_lower = parts[0].lower()
                if any(w in p0_lower for w in generic_store_words) and len(parts) > 1:
                    candidate_brand = parts[-1]
                else:
                    candidate_brand = parts[0]

        brand_sec = Section("website")
        if candidate_brand:
            cleaned_brand = re.sub(r"\s*[-–|:]?\s*(?:org(?:anisasjons)?\.?\s*nr\.?|organisasjonsnummer)\s*[:.]?\s*\d{9}\b.*$", "", candidate_brand, flags=re.I).strip(" .,-")
            cleaned_brand = re.sub(r"\s*[-–|:]\s*(?:nettbutikk|butikk|webshop|forside|hjem|velkommen|home|shop|store)\b.*$", "", cleaned_brand, flags=re.I).strip(" .,-")
            norm_b = legal_name(cleaned_brand)
            generic_brands = {
                "home", "hjem", "welcome", "velkommen", "kontakt", "contact",
                "kontakt oss", "contact us", "privacy policy", "personvern",
                "vilkar", "vilkar og betingelser", "terms", "terms of service",
                "forside", "hjemmeside"
            }
            is_generic_tagline = (
                re.search(r"\b(?:din|ditt)\s+\w+", cleaned_brand, re.I) is not None
                or re.search(r"\b(?:kontakt|contact)\b", cleaned_brand, re.I) is not None
                or re.search(r"\b(?:vilk[aå]r|betingelser|privacy|personvern)\b", cleaned_brand, re.I) is not None
                or (re.search(r"\bi\s+[A-ZÆØÅa-zæøå]{3,}\b", cleaned_brand) is not None and len(cleaned_brand.split()) > 3)
            )
            if (cleaned_brand and len(cleaned_brand) <= 100 and "\ufffd" not in cleaned_brand
                    and norm_b not in generic_brands
                    and not is_generic_tagline
                    and norm_b != legal_name(context.get("name"))):
                from signalpost.web.collector import publish
                span = (root_page.span_for(cleaned_brand) or "")[:150]
                publish(brand_sec, root_resp, org, "public_brand", cleaned_brand, "meta:brand", span)

        # Merge newly extracted claims and evidence
        old_brand = next((c for c in env.claims if c.field == "public_brand"), None)
        new_brand = next((c for c in brand_sec.claims if c.field == "public_brand"), None)
        if (old_brand is None) != (new_brand is None) or (old_brand and new_brand and old_brand.value != new_brand.value):
            brand_changes += 1

        new_claims = retained_claims + brand_sec.claims + desc_sec.claims
        env.claims = new_claims

        # Update evidence list: retain existing referenced + add new evidence
        new_ev_by_id = {e.id: e for e in brand_sec.evidence + desc_sec.evidence}
        referenced_eids = {eid for c in env.claims for eid in c.evidence_ids}
        updated_evidence = [e for e in env.evidence if e.id in referenced_eids]
        for eid in referenced_eids:
            if eid in new_ev_by_id and all(e.id != eid for e in updated_evidence):
                updated_evidence.append(new_ev_by_id[eid])
        env.evidence = updated_evidence

        # Re-synthesize
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

    print(f"Regeneration complete: {len(updated_envelopes)} envelopes. Brand changes: {brand_changes}")

    # Write out updated envelopes
    blobs = BlobStore(STATE_DIR)
    write(ENVELOPES_PATH, updated_envelopes, "union", blobs, 256)
    print(f"Wrote updated envelopes to {ENVELOPES_PATH}")

    # Write out updated profiles
    profile_lines = []
    for r in updated_envelopes:
        prof_data = r.profile.model_dump(mode="json") if hasattr(r.profile, "model_dump") else r.profile
        profile_lines.append(json.dumps(prof_data, ensure_ascii=False))
    PROFILES_PATH.write_text("\n".join(profile_lines) + "\n", encoding="utf-8")
    print(f"Wrote updated profiles to {PROFILES_PATH}")

    # Validate schema
    for r in updated_envelopes:
        validate_shape(r.model_dump(mode="json"), "union")
    print("All 1,000 envelopes verified against union shape schema!")


if __name__ == "__main__":
    main()
