"""Offline field-coverage replay from saved envelopes and their content blobs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
from pathlib import Path
from statistics import median
from urllib.parse import parse_qs, urlsplit

from signalpost.models.envelope import Envelope
from signalpost.site import generate_site
from signalpost.sources import brreg_enhet, bulk_registry
from signalpost.sources.brreg_underenheter import extract_page
from signalpost.sources.extract import Section, Source
from signalpost.sources.http import Response


def deny_network(event, args):
    if event in {"socket.connect", "socket.getaddrinfo", "socket.sendto", "socket.gethostbyname"}:
        raise RuntimeError("Offline field audit attempted network access")


def top_five(site: Path):
    items = [
        {"orgnr": page.stem, "bytes": page.stat().st_size}
        for page in (site / "c").glob("*.html")
    ]
    return sorted(items, key=lambda item: (-item["bytes"], item["orgnr"]))[:5]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--envelopes", type=Path, required=True)
    parser.add_argument("--blobs", type=Path, required=True)
    parser.add_argument("--before-site", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sys.addaudithook(deny_network)

    rows = [json.loads(line) for line in args.envelopes.read_text(encoding="utf-8").splitlines() if line.strip()]
    added_by_company = {}
    identity_claims_by_company = {}
    parent_claims_by_company = {}
    raw_hashes = set()
    for row in rows:
        org = row["organisation_number"]
        existing_fields = {claim["field"] for claim in row["claims"]}
        added_claims = []
        added_evidence = []
        if "identity.organisation_number" not in existing_fields:
            evidence_by_id = {item["id"]: item for item in row["evidence"]}
            identity_claim = next((claim for claim in row["claims"] if claim["field"] == "identity.legal_name"), None)
            if identity_claim is None or not identity_claim.get("evidence_ids"):
                raise ValueError("Saved company name claim lacks source evidence")
            identity_evidence = evidence_by_id[identity_claim["evidence_ids"][0]]
            identity_body = (args.blobs / identity_evidence["content_sha256"]).read_bytes()
            if hashlib.sha256(identity_body).hexdigest() != identity_evidence["content_sha256"]:
                raise ValueError("A saved identity response blob did not match its content hash")
            raw_hashes.add(identity_evidence["content_sha256"])
            identity_source = Source(
                identity_evidence["source_url"], identity_body,
                identity_evidence["content_sha256"], identity_evidence["retrieved_at"],
                identity_evidence.get("source_identifier"),
            )
            if identity_evidence["source_url"].endswith("/lastned/csv"):
                record = next(csv.DictReader(io.StringIO(identity_body.decode("utf-8-sig"))))
                identity_section = bulk_registry.extract(org, record, identity_source)
            else:
                identity_section = brreg_enhet.extract_response(
                    org, Response(identity_body, 200, identity_source.url, identity_source.retrieved_at, identity_source.sha)
                )
            number_claim = next(c for c in identity_section.claims if c.field == "identity.organisation_number")
            number_evidence = next(e for e in identity_section.evidence if e.id in number_claim.evidence_ids)
            added_claims.append(number_claim.model_dump(mode="json"))
            added_evidence.append(number_evidence.model_dump(mode="json"))
            existing_fields.add(number_claim.field)

        evidence_rows = [e for e in row["evidence"] if urlsplit(e["source_url"]).path == "/enhetsregisteret/api/underenheter"]
        sources = {}
        for evidence in evidence_rows:
            key = (evidence["source_url"], evidence["content_sha256"], evidence["retrieved_at"])
            sources[key] = evidence
        for (url, sha, retrieved_at) in sorted(sources):
            blob = args.blobs / sha
            body = blob.read_bytes()
            if hashlib.sha256(body).hexdigest() != sha:
                raise ValueError("A saved response blob did not match its content hash")
            raw_hashes.add(sha)
            query = parse_qs(urlsplit(url).query)
            page_number = int(query.get("page", ["0"])[0])
            response = Response(body, 200, url, retrieved_at, sha)
            section = Section()
            extract_page(org, response, section, page_number)
            for claim in section.claims:
                if not claim.field.endswith(".parent_organisation_number"):
                    continue
                if claim.field in existing_fields:
                    continue
                evidence = next(e for e in section.evidence if e.id in claim.evidence_ids)
                if evidence.locator.rsplit("/", 1)[-1] != "overordnetEnhet" or claim.value != org:
                    raise ValueError("Parent claim failed exact-field validation")
                added_claims.append(claim.model_dump(mode="json"))
                added_evidence.append(evidence.model_dump(mode="json"))
                existing_fields.add(claim.field)

        row["claims"].extend(added_claims)
        row["evidence"].extend(added_evidence)
        profile = row.get("profile", {})
        if "values" in profile:
            profile["values"].update({claim["field"]: claim["value"] for claim in added_claims})
            profile["evidence_ids"] = sorted(set(profile.get("evidence_ids", [])) | {
                evidence["id"] for evidence in added_evidence
            })
        Envelope.model_validate(row)
        added_by_company[org] = len(added_claims)
        identity_claims_by_company[org] = sum(
            claim['field'] == 'identity.organisation_number' for claim in added_claims
        )
        parent_claims_by_company[org] = sum(
            claim['field'].endswith('.parent_organisation_number') for claim in added_claims
        )

    args.output.mkdir(parents=True, exist_ok=False)
    envelope_path = args.output / "envelopes.jsonl"
    envelope_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows),
        encoding="utf-8",
        newline="\n",
    )
    site_result = generate_site(envelope_path, args.output / "site")
    after = top_five(args.output / "site")
    before = top_five(args.before_site)
    counts = list(added_by_company.values())
    report = {
        "scope": "Offline claims derived from saved exact-orgnr Enhetsregisteret subunit responses",
        "companies": len(rows),
        "companies_with_new_identity_claim": sum(count > 0 for count in identity_claims_by_company.values()),
        "companies_with_new_parent_claim": sum(count > 0 for count in parent_claims_by_company.values()),
        "new_identity_claims": sum(identity_claims_by_company.values()),
        "new_parent_claims": sum(parent_claims_by_company.values()),
        "new_claims": sum(counts),
        "median_new_claims_all_companies": median(counts) if counts else 0,
        "median_new_claims_affected_companies": median([count for count in counts if count]),
        "additional_http_requests": 0,
        "network_disabled": True,
        "saved_response_blobs_checked": len(raw_hashes),
        "before_top_five": before,
        "after_top_five": after,
        "largest_profile_bytes": site_result["largest_profile_bytes"],
        "site": site_result,
    }
    if len(rows) != 500 or report["largest_profile_bytes"] > 235_000:
        raise ValueError("500-company or effective profile-size gate failed")
    (args.output / "measurement.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
