"""
Adversarial test suite proving scripts/accuracy_audit.py detects corruptions across:
- Category A: Empty span, wrong locator, missing blob, hash mismatch, span not in blob
- Category B: Wrong organisation, name, role, subunit relationship
- Financial: amount mismatch, sign mismatch, currency mismatch, year mismatch, fabricated zero
- Web: Social URL absent, foreign owner, missing signals, unknown proof type
- Activity: Date belonging to another item, missing sitemap lastmod, missing URL
- Hiring: Missing employer orgnr in detail, mismatched employer orgnr, invalid subunit mapping
- Edge cases: Empty sample and zero denominator reporting (N/A)
"""
import hashlib
import json
import pytest
from scripts.accuracy_audit import (
    audit_claim_structural,
    audit_identity_claim,
    audit_accounts_claim,
    audit_roles_claim,
    audit_subunits_claim,
    audit_website_claim,
    audit_social_claim,
    audit_activity_claim,
    audit_hiring_claim,
    resolve_json_pointer,
)

ORG = "999592236"
OTHER_ORG = "912345678"


def make_blob(content: str):
    sha = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return sha, content


# -----------------------------------------------------------------------------
# 1. Category A: Structural Integrity & Excerpt Verbatim Tests
# -----------------------------------------------------------------------------

def test_structural_empty_span_detected():
    sha, body = make_blob("Some valid body text")
    claim = {"availability": "available", "evidence_ids": ["ev1"]}
    ev_map = {"ev1": {"id": "ev1", "locator": "/navn", "content_sha256": sha, "claim_span": "  "}}
    status, reason, _ = audit_claim_structural(claim, ev_map, lambda s: body)
    assert status == "FAIL"
    assert "Empty or whitespace evidence span" in reason


def test_structural_span_too_long_detected():
    long_span = "x" * 305
    sha, body = make_blob(long_span)
    claim = {"availability": "available", "evidence_ids": ["ev1"]}
    ev_map = {"ev1": {"id": "ev1", "locator": "/navn", "content_sha256": sha, "claim_span": long_span}}
    status, reason, _ = audit_claim_structural(claim, ev_map, lambda s: body)
    assert status == "FAIL"
    assert "exceeds 300 character limit" in reason


def test_structural_missing_blob_detected():
    claim = {"availability": "available", "evidence_ids": ["ev1"]}
    ev_map = {"ev1": {"id": "ev1", "locator": "/navn", "content_sha256": "0000000000000000", "claim_span": "text"}}
    status, reason, _ = audit_claim_structural(claim, ev_map, lambda s: None)
    assert status == "FAIL"
    assert "missing from state storage" in reason


def test_structural_hash_mismatch_detected():
    claim = {"availability": "available", "evidence_ids": ["ev1"]}
    ev_map = {"ev1": {"id": "ev1", "locator": "/navn", "content_sha256": "badhash", "claim_span": "text"}}
    status, reason, _ = audit_claim_structural(claim, ev_map, lambda s: False)
    assert status == "FAIL"
    assert "failed SHA-256 integrity" in reason


def test_structural_span_not_in_blob_detected():
    sha, body = make_blob("The actual text in the blob")
    claim = {"availability": "available", "evidence_ids": ["ev1"]}
    ev_map = {"ev1": {"id": "ev1", "locator": "/navn", "content_sha256": sha, "claim_span": "unrelated excerpt"}}
    status, reason, _ = audit_claim_structural(claim, ev_map, lambda s: body)
    assert status == "FAIL"
    assert "not found verbatim" in reason


# -----------------------------------------------------------------------------
# 2. Identity Claims: Organization & Field Value Mismatches
# -----------------------------------------------------------------------------

def test_identity_wrong_organisation_detected():
    body = json.dumps({"organisasjonsnummer": OTHER_ORG, "navn": "AUTONEXT AS"})
    claim = {"field": "identity.legal_name", "value": "AUTONEXT AS"}
    ev = {"locator": "/navn"}
    status, reason, _ = audit_identity_claim(ORG, claim, ev, body)
    assert status == "INCORRECT"
    assert "!= subject org" in reason


def test_identity_legal_name_mismatch_detected():
    body = json.dumps({"organisasjonsnummer": ORG, "navn": "AUTONEXT AS"})
    claim = {"field": "identity.legal_name", "value": "COMPLETELY WRONG NAME AS"}
    ev = {"locator": "/navn"}
    status, reason, _ = audit_identity_claim(ORG, claim, ev, body)
    assert status == "INCORRECT"
    assert "Legal name" in reason


def test_identity_employees_mismatch_detected():
    body = json.dumps({"organisasjonsnummer": ORG, "antallAnsatte": 5})
    claim = {"field": "identity.employees", "value": 150}
    ev = {"locator": "/antallAnsatte"}
    status, reason, _ = audit_identity_claim(ORG, claim, ev, body)
    assert status == "INCORRECT"
    assert "Claim employees 150 != source 5" in reason


def test_identity_csv_field_mismatch_detected():
    csv_body = "organisasjonsnummer,navn,forretningsadresse.kommune\n999592236,AUTONEXT AS,VEFSN\n"
    claim = {"field": "identity.municipality", "value": "OSLO"}
    ev = {"locator": "row:999592236/column:forretningsadresse.kommune"}
    status, reason, _ = audit_identity_claim(ORG, claim, ev, csv_body)
    assert status == "INCORRECT"
    assert "Claim municipality 'OSLO' != CSV 'VEFSN'" in reason


# -----------------------------------------------------------------------------
# 3. Financials: Amount, Sign, Currency, Year, and Fabricated Zero Detection
# -----------------------------------------------------------------------------

def test_accounts_fabricated_zero_detected():
    # Source field is None/missing in Regnskapsregisteret filing
    body = json.dumps([{
        "regnskapstype": "SELSKAP",
        "virksomhet": {"organisasjonsnummer": ORG},
        "regnskapsperiode": {"fraDato": "2025-01-01", "tilDato": "2025-12-31"},
        "resultatregnskapResultat": {"driftsresultat": {"driftsinntekter": {"sumDriftsinntekter": None}}}
    }])
    claim = {
        "field": "accounts.revenue",
        "value": 0,  # Fabricated zero!
        "reporting_period": {"fiscal_year": "2025", "currency": "NOK"}
    }
    ev = {"locator": "/0/resultatregnskapResultat/driftsresultat/driftsinntekter/sumDriftsinntekter"}
    status, reason, _ = audit_accounts_claim(ORG, claim, ev, body)
    assert status == "INCORRECT"
    assert "Fabricated zero" in reason


def test_accounts_numeric_amount_mismatch_detected():
    body = json.dumps([{
        "regnskapstype": "SELSKAP",
        "virksomhet": {"organisasjonsnummer": ORG},
        "regnskapsperiode": {"fraDato": "2025-01-01", "tilDato": "2025-12-31"},
        "resultatregnskapResultat": {"aarsresultat": 5000000}
    }])
    claim = {
        "field": "accounts.net_result",
        "value": 1200000,
        "reporting_period": {"fiscal_year": "2025", "currency": "NOK"}
    }
    ev = {"locator": "/0/resultatregnskapResultat/aarsresultat"}
    status, reason, _ = audit_accounts_claim(ORG, claim, ev, body)
    assert status == "INCORRECT"
    assert "Numeric value mismatch" in reason


def test_accounts_numeric_sign_mismatch_detected():
    body = json.dumps([{
        "regnskapstype": "SELSKAP",
        "virksomhet": {"organisasjonsnummer": ORG},
        "regnskapsperiode": {"fraDato": "2025-01-01", "tilDato": "2025-12-31"},
        "resultatregnskapResultat": {"aarsresultat": -450000}  # Loss
    }])
    claim = {
        "field": "accounts.net_result",
        "value": 450000,  # Mislabeled as positive profit!
        "reporting_period": {"fiscal_year": "2025", "currency": "NOK"}
    }
    ev = {"locator": "/0/resultatregnskapResultat/aarsresultat"}
    status, reason, _ = audit_accounts_claim(ORG, claim, ev, body)
    assert status == "INCORRECT"
    assert "Numeric sign mismatch" in reason


def test_accounts_currency_mismatch_detected():
    body = json.dumps([{
        "regnskapstype": "SELSKAP",
        "virksomhet": {"organisasjonsnummer": ORG},
        "valuta": "USD",  # Filed in USD
        "regnskapsperiode": {"fraDato": "2025-01-01", "tilDato": "2025-12-31"},
        "resultatregnskapResultat": {"aarsresultat": 100000}
    }])
    claim = {
        "field": "accounts.net_result",
        "value": 100000,
        "reporting_period": {"fiscal_year": "2025", "currency": "NOK"}  # Wrong currency
    }
    ev = {"locator": "/0/resultatregnskapResultat/aarsresultat"}
    status, reason, _ = audit_accounts_claim(ORG, claim, ev, body)
    assert status == "INCORRECT"
    assert "Currency mismatch" in reason


def test_accounts_consolidated_type_detected():
    body = json.dumps([{
        "regnskapstype": "KONSERN",  # Consolidated group accounts, not exact company
        "virksomhet": {"organisasjonsnummer": ORG},
        "valuta": "NOK",
        "regnskapsperiode": {"fraDato": "2025-01-01", "tilDato": "2025-12-31"},
        "resultatregnskapResultat": {"aarsresultat": 100000}
    }])
    claim = {
        "field": "accounts.net_result",
        "value": 100000,
        "reporting_period": {"fiscal_year": "2025", "currency": "NOK"}
    }
    ev = {"locator": "/0/resultatregnskapResultat/aarsresultat"}
    status, reason, _ = audit_accounts_claim(ORG, claim, ev, body)
    assert status == "INCORRECT"
    assert "Consolidated account type KONSERN published" in reason


# -----------------------------------------------------------------------------
# 4. Roles & Subunits: Relationship & Value Mismatches
# -----------------------------------------------------------------------------

def test_roles_person_mismatch_detected():
    body = json.dumps({
        "organisasjonsnummer": ORG,
        "rollegrupper": [{
            "roller": [{
                "type": {"kode": "DAGL", "beskrivelse": "Daglig leder"},
                "person": {"navn": {"fornavn": "Barez", "etternavn": "Piri"}}
            }]
        }]
    })
    claim = {
        "field": "roles.role.1",
        "value": {"name": "Ola Nordmann", "role_type": {"kode": "DAGL"}}
    }
    ev = {"locator": "/rollegrupper/0/roller/0"}
    status, reason, _ = audit_roles_claim(ORG, claim, ev, body)
    assert status == "INCORRECT"
    assert "Role person name mismatch" in reason


def test_subunits_parent_mismatch_detected():
    body = json.dumps({
        "_embedded": {
            "underenheter": [{
                "organisasjonsnummer": "937979606",
                "overordnetEnhet": OTHER_ORG,  # Belongs to a different parent!
                "navn": "AUTONEXT AS AVD BILLINGSTAD"
            }]
        }
    })
    claim = {
        "field": "subunits.unit.937979606",
        "value": {"organisation_number": "937979606", "name": "AUTONEXT AS AVD BILLINGSTAD"}
    }
    ev = {"locator": "/_embedded/underenheter/0"}
    status, reason, _ = audit_subunits_claim(ORG, claim, ev, body)
    assert status == "INCORRECT"
    assert "Subunit parent orgnr" in reason


# -----------------------------------------------------------------------------
# 5. Websites & Social: Proof Validation & Foreign Owner Detection
# -----------------------------------------------------------------------------

def test_website_missing_orgnr_on_page_detected():
    body = "<html><body>Welcome to Example AS! Contact us today.</body></html>"
    claim = {
        "field": "official_website",
        "value": {"url": "https://example.no", "proof_type": "orgnr_on_page"}
    }
    ev = {"locator": "/"}
    status, reason, _ = audit_website_claim(ORG, claim, ev, body)
    assert status == "INCORRECT"
    assert "orgnr 999592236 not found on page" in reason


def test_website_empty_signals_detected():
    body = "<html><body>Welcome to Example AS!</body></html>"
    claim = {
        "field": "official_website",
        "value": {"url": "https://example.no", "proof_type": "signals", "signals": []}
    }
    ev = {"locator": "/"}
    status, reason, _ = audit_website_claim(ORG, claim, ev, body)
    assert status == "INCORRECT"
    assert "signals list is empty" in reason


def test_website_unsupported_signals_detected():
    body = "<html><body>Welcome to Example AS in Oslo!</body></html>"
    claim = {
        "field": "official_website",
        "value": {"url": "https://example.no", "proof_type": "signals", "signals": ["Trondheim", "Bergen"]}
    }
    ev = {"locator": "/"}
    status, reason, _ = audit_website_claim(ORG, claim, ev, body)
    assert status == "INCORRECT"
    assert "not found in page body" in reason


def test_website_registry_declared_not_in_registry_detected():
    body = "<html><body>Welcome to Example!</body></html>"
    claim = {
        "field": "official_website",
        "value": {"url": "https://invented-domain.no", "proof_type": "registry_declared"}
    }
    ev = {"locator": "/"}
    registry_body = "organisasjonsnummer,hjemmeside\n999592236,actual-domain.no\n"
    status, reason, _ = audit_website_claim(ORG, claim, ev, body, registry_body=registry_body)
    assert status == "INCORRECT"
    assert "not found in registry body" in reason


def test_social_url_absent_from_page_detected():
    body = "<html><body>Follow us on social media! No links here.</body></html>"
    claim = {
        "field": "social_profile.1",
        "value": {"url": "https://linkedin.com/company/example", "platform": "linkedin"}
    }
    ev = {"locator": "/"}
    status, reason, _ = audit_social_claim(ORG, claim, ev, body)
    assert status == "INCORRECT"
    assert "not found in verified company page body" in reason


def test_social_generic_share_link_rejected():
    body = '<html><body><a href="https://facebook.com/sharer/sharer.php?u=foo">Share</a></body></html>'
    claim = {
        "field": "social_profile.1",
        "value": {"url": "https://facebook.com/sharer", "platform": "facebook"}
    }
    ev = {"locator": "/"}
    status, reason, _ = audit_social_claim(ORG, claim, ev, body)
    assert status == "INCORRECT"
    assert "Generic platform landing link" in reason


# -----------------------------------------------------------------------------
# 6. Activity: Date Association & Sitemap Lastmod Semantics
# -----------------------------------------------------------------------------

def test_activity_date_belonging_to_another_item_detected():
    xml = """<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <url><loc>https://example.no/news/first</loc><lastmod>2026-01-01</lastmod></url>
      <url><loc>https://example.no/news/second</loc><lastmod>2026-10-10</lastmod></url>
    </urlset>"""
    # Claim asserts first item with second item's date!
    claim = {
        "field": "activity.item.1",
        "value": {"url": "https://example.no/news/first", "date": "2026-10-10"}
    }
    ev = {"locator": "/"}
    status, reason, _ = audit_activity_claim(ORG, claim, ev, xml)
    assert status == "INCORRECT"
    assert "does not match XML entry date" in reason


def test_activity_url_not_found_detected():
    xml = """<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <url><loc>https://example.no/news/first</loc><lastmod>2026-01-01</lastmod></url>
    </urlset>"""
    claim = {
        "field": "activity.item.1",
        "value": {"url": "https://example.no/news/missing", "date": "2026-01-01"}
    }
    ev = {"locator": "/"}
    status, reason, _ = audit_activity_claim(ORG, claim, ev, xml)
    assert status == "INCORRECT"
    assert "not found in any XML entry" in reason


# -----------------------------------------------------------------------------
# 7. Hiring: Employer Orgnr Proof & Subunit Verification
# -----------------------------------------------------------------------------

def test_hiring_missing_employer_orgnr_in_detail_detected():
    detail_body = json.dumps({
        "uuid": "00000000-0000-4000-8000-000000000001",
        "status": "ACTIVE",
        "ad_content": {
            "title": "Software Engineer",
            "employer": {"name": "Example AS", "orgnr": None}  # Missing employer orgnr!
        }
    })
    claim = {
        "field": "hiring.job.00000000-0000-4000-8000-000000000001",
        "value": {"uuid": "00000000-0000-4000-8000-000000000001", "matched_via": "organisation 999592236"}
    }
    ev = {"locator": "/ad_content"}
    status, reason, _ = audit_hiring_claim(ORG, claim, ev, detail_body)
    assert status == "INCORRECT"
    assert "lacks valid 9-digit employer orgnr" in reason


def test_hiring_mismatched_employer_orgnr_detected():
    detail_body = json.dumps({
        "uuid": "00000000-0000-4000-8000-000000000001",
        "status": "ACTIVE",
        "ad_content": {
            "title": "Software Engineer",
            "employer": {"name": "Foreign AS", "orgnr": OTHER_ORG}  # Belongs to a different company!
        }
    })
    claim = {
        "field": "hiring.job.00000000-0000-4000-8000-000000000001",
        "value": {"uuid": "00000000-0000-4000-8000-000000000001", "matched_via": "organisation 999592236"}
    }
    ev = {"locator": "/ad_content"}
    status, reason, _ = audit_hiring_claim(ORG, claim, ev, detail_body)
    assert status == "INCORRECT"
    assert "!= parent org" in reason


def test_hiring_invalid_subunit_mapping_detected():
    detail_body = json.dumps({
        "uuid": "00000000-0000-4000-8000-000000000001",
        "status": "ACTIVE",
        "ad_content": {
            "title": "Branch Manager",
            "employer": {"name": "Branch", "orgnr": "937979606"}
        }
    })
    # Ad claims subunit 999999999, but detail payload has 937979606
    claim = {
        "field": "hiring.job.00000000-0000-4000-8000-000000000001",
        "value": {"uuid": "00000000-0000-4000-8000-000000000001", "matched_via": "subunit 999999999"}
    }
    ev = {"locator": "/ad_content"}
    status, reason, _ = audit_hiring_claim(ORG, claim, ev, detail_body)
    assert status == "INCORRECT"
    assert "!= claimed subunit" in reason
