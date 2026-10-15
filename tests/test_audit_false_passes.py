"""
Regression test suite proving the current auditor (HEAD fc0dfec) incorrectly accepts
12 specific invalid claims (false passes).

Requirement 1: Record the tests failing against the old implementation, then fix them.
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
)

ORG = "999592236"
OTHER_ORG = "912345678"


def make_blob(content: str):
    sha = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return sha, content


# -----------------------------------------------------------------------------
# 1. CSV identity: registered_website = evil.no when source column has real.no
# -----------------------------------------------------------------------------
def test_csv_identity_website_mismatch_rejected():
    csv_body = "organisasjonsnummer,navn,hjemmeside\n999592236,TEST AS,real.no\n"
    claim = {
        "field": "identity.registered_website",
        "value": "evil.no"
    }
    ev = {"locator": "row:999592236/column:hjemmeside"}
    status, reason, _ = audit_identity_claim(ORG, claim, ev, csv_body)
    assert status == "INCORRECT", f"Auditor falsely accepted mismatched CSV website: {reason}"
    assert "evil.no" in reason or "real.no" in reason or "mismatch" in reason.lower()


# -----------------------------------------------------------------------------
# 2. NAV employer matching claimed subunit when parent's subunit map is empty
# -----------------------------------------------------------------------------
def test_nav_employer_subunit_empty_map_rejected():
    detail_body = json.dumps({
        "uuid": "00000000-0000-4000-8000-000000000001",
        "status": "ACTIVE",
        "ad_content": {
            "title": "Branch Manager",
            "employer": {"name": "Branch", "orgnr": "937979606"}
        }
    })
    claim = {
        "field": "hiring.job.00000000-0000-4000-8000-000000000001",
        "value": {
            "uuid": "00000000-0000-4000-8000-000000000001",
            "matched_via": "subunit 937979606"
        }
    }
    ev = {"locator": "/ad_content"}
    # Subunit map is empty: parent 999592236 has NO verified subunit 937979606
    empty_subunit_map = {}
    status, reason, _ = audit_hiring_claim(ORG, claim, ev, detail_body, subunit_map=empty_subunit_map)
    assert status == "INCORRECT", f"Auditor falsely accepted subunit hiring without subunit proof: {reason}"


# -----------------------------------------------------------------------------
# 3. LinkedIn URL when only the same path on evil.test appears in HTML
# -----------------------------------------------------------------------------
def test_social_url_different_host_same_path_rejected():
    # Destination HTML contains a link to evil.test with path /company/acme
    body = '<html><body><a href="https://evil.test/company/acme">Our Evil Network</a></body></html>'
    claim = {
        "field": "social_profile.linkedin",
        "value": {
            "url": "https://linkedin.com/company/acme",
            "platform": "linkedin"
        }
    }
    ev = {"locator": "/"}
    status, reason, _ = audit_social_claim(ORG, claim, ev, body)
    assert status == "INCORRECT", f"Auditor falsely accepted path match on wrong domain: {reason}"


# -----------------------------------------------------------------------------
# 4. An empty role value against a populated person/role source
# -----------------------------------------------------------------------------
def test_empty_role_value_against_populated_source_rejected():
    body = json.dumps({
        "organisasjonsnummer": ORG,
        "rollegrupper": [{
            "type": {"kode": "STYR", "beskrivelse": "Styre"},
            "roller": [{
                "type": {"kode": "DAGL", "beskrivelse": "Daglig leder"},
                "person": {"navn": {"fornavn": "Ola", "etternavn": "Nordmann"}}
            }]
        }]
    })
    # Empty claim value: missing both name and role_type
    claim = {
        "field": "roles.role.1",
        "value": {}
    }
    ev = {"locator": "/rollegrupper/0/roller/0"}
    status, reason, _ = audit_roles_claim(ORG, claim, ev, body)
    assert status == "INCORRECT", f"Auditor falsely accepted empty role claim value: {reason}"


# -----------------------------------------------------------------------------
# 5. Activity URL /news/a when the source contains only /news/another
# -----------------------------------------------------------------------------
def test_activity_url_prefix_collision_rejected():
    atom = """<feed xmlns="http://www.w3.org/2005/Atom">
      <entry>
        <link href="https://example.no/news/another"/>
        <updated>2026-10-10T12:00:00Z</updated>
      </entry>
    </feed>"""
    # Claim points to /news/a, which is a substring of /news/another but NOT an exact match
    claim = {
        "field": "activity.item.1",
        "value": {
            "url": "https://example.no/news/a",
            "date": "2026-10-10"
        }
    }
    ev = {"locator": "/"}
    status, reason, _ = audit_activity_claim(ORG, claim, ev, atom)
    assert status == "INCORRECT", f"Auditor falsely accepted substring URL match: {reason}"
    assert "not found" in reason.lower() or "mismatch" in reason.lower()


# -----------------------------------------------------------------------------
# 6. Sitemap lastmod presented as publication date
# -----------------------------------------------------------------------------
def test_sitemap_lastmod_not_accepted_as_publication_date():
    sitemap = """<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <url>
        <loc>https://example.no/news/post1</loc>
        <lastmod>2026-10-10</lastmod>
      </url>
    </urlset>"""
    claim = {
        "field": "activity.item.1",
        "value": {
            "url": "https://example.no/news/post1",
            "date": "2026-10-10",
            "date_kind": "published"  # Claiming publication date from sitemap lastmod!
        }
    }
    ev = {"locator": "/"}
    status, reason, _ = audit_activity_claim(ORG, claim, ev, sitemap)
    assert status == "INCORRECT", f"Auditor falsely accepted sitemap lastmod as publication date: {reason}"


# -----------------------------------------------------------------------------
# 7. Arbitrary website metadata/contact value with valid but unrelated excerpt
# -----------------------------------------------------------------------------
def test_website_metadata_arbitrary_value_rejected():
    # If claim claims email hacker@evil.com with an unrelated span
    body = "<html><body>Contact us at support@example.no</body></html>"
    claim = {
        "field": "contact.email.1",
        "value": "hacker@evil.com"
    }
    ev = {"locator": "contact:hacker@evil.com"}
    # Under fixed auditor, contact claims must be checked against page body
    from scripts.accuracy_audit import audit_website_metadata_claim
    status, reason, _ = audit_website_metadata_claim(ORG, claim, ev, body)
    assert status == "INCORRECT", f"Auditor falsely accepted arbitrary metadata/contact claim: {reason}"


# -----------------------------------------------------------------------------
# 8. Website registry signal where registered domain differs from candidate domain
# -----------------------------------------------------------------------------
def test_website_registry_signal_domain_mismatch_rejected():
    html_body = "<html><head><title>Candidate Site</title></head><body>Welcome</body></html>"
    claim = {
        "field": "official_website",
        "value": {
            "final_url": "https://evil-candidate.no",
            "proof_type": "signals",
            "signals": ["registry_website"]
        }
    }
    ev = {"locator": "identity-proof:Candidate Site"}
    context = {
        "name": "TEST AS",
        "website": "real-company.no"  # Registered domain is real-company.no, NOT evil-candidate.no!
    }
    status, reason, _ = audit_website_claim(
        ORG, claim, ev, html_body, context=context, leaders=[]
    )
    assert status == "INCORRECT", f"Auditor falsely accepted registry_website signal for mismatched domain: {reason}"


# -----------------------------------------------------------------------------
# 9. Unsupported signals proof below documented acceptance threshold
# -----------------------------------------------------------------------------
def test_website_signals_below_acceptance_threshold_rejected():
    # Municipality alone gives only 1 point. Acceptance threshold requires:
    # points >= 5, legal_name, own_brand, len(signals)>=2, and one of address/phone/leader.
    html_body = "<html><head><title>Some Generic Site</title></head><body>Located in OSLO</body></html>"
    claim = {
        "field": "official_website",
        "value": {
            "final_url": "https://generic-site.no",
            "proof_type": "signals",
            "signals": ["municipality"],
            "points": 1,
            "identity_level": "LOW"
        }
    }
    ev = {"locator": "identity-proof:Generic Site"}
    context = {
        "name": "TEST AS",
        "municipality": "OSLO"
    }
    status, reason, _ = audit_website_claim(
        ORG, claim, ev, html_body, context=context, leaders=[]
    )
    assert status == "INCORRECT", f"Auditor falsely accepted website signals below threshold: {reason}"


# -----------------------------------------------------------------------------
# 10. Valid first evidence reference followed by missing or corrupt additional evidence
# -----------------------------------------------------------------------------
def test_structural_second_evidence_corrupt_rejected():
    sha1, body1 = make_blob("Valid first evidence body")
    claim = {
        "availability": "available",
        "evidence_ids": ["ev1", "ev2_corrupt"]
    }
    ev_map = {
        "ev1": {"id": "ev1", "locator": "/navn", "content_sha256": sha1, "claim_span": "Valid first"},
        "ev2_corrupt": {"id": "ev2_corrupt", "locator": "/addr", "content_sha256": "badsha", "claim_span": "Corrupt span"}
    }
    def blob_getter(s):
        if s == sha1: return body1
        return False  # Hash mismatch or missing
    status, reason, _ = audit_claim_structural(claim, ev_map, blob_getter)
    assert status == "FAIL", f"Auditor falsely passed claim with corrupt second evidence: {reason}"
    assert "ev2_corrupt" in reason or "integrity" in reason.lower() or "second" in reason.lower()


# -----------------------------------------------------------------------------
# 11. Financial claim with wrong units or reporting-period boundaries
# -----------------------------------------------------------------------------
def test_accounts_wrong_period_boundaries_or_units_rejected():
    # Regnskapsregisteret period: 2025-07-01 to 2025-12-31 (6 months)
    body = json.dumps([{
        "regnskapstype": "SELSKAP",
        "virksomhet": {"organisasjonsnummer": ORG},
        "regnskapsperiode": {"fraDato": "2025-07-01", "tilDato": "2025-12-31"},
        "valuta": "NOK",
        "resultatregnskapResultat": {
            "driftsresultat": {
                "driftsinntekter": {"sumDriftsinntekter": 500000}
            }
        }
    }])
    # Claim claims full year 2025-01-01 to 2025-12-31 with unit "thousands"
    claim = {
        "field": "accounts.revenue",
        "value": 500000,
        "reporting_period": {
            "fiscal_year": "2025",
            "start_date": "2025-01-01",  # Mismatch: filing has 2025-07-01
            "end_date": "2025-12-31",
            "currency": "NOK",
            "unit": "thousands"  # Mismatch: filing is in whole NOK
        }
    }
    ev = {"locator": "/0/resultatregnskapResultat/driftsresultat/driftsinntekter/sumDriftsinntekter"}
    status, reason, _ = audit_accounts_claim(ORG, claim, ev, body)
    assert status == "INCORRECT", f"Auditor falsely accepted wrong reporting boundaries/units: {reason}"


# -----------------------------------------------------------------------------
# 12. Claim whose locator selects a matching value belonging to a different field
# -----------------------------------------------------------------------------
def test_accounts_locator_pointing_to_wrong_field_rejected():
    # Filing where driftskostnad equals 1000000
    body = json.dumps([{
        "regnskapstype": "SELSKAP",
        "virksomhet": {"organisasjonsnummer": ORG},
        "regnskapsperiode": {"fraDato": "2025-01-01", "tilDato": "2025-12-31"},
        "valuta": "NOK",
        "resultatregnskapResultat": {
            "driftsresultat": {
                "driftsinntekter": {"sumDriftsinntekter": 2000000},
                "driftskostnad": {"sumDriftskostnad": 1000000}
            }
        }
    }])
    # Claim claims revenue = 1000000, but locator points to sumDriftskostnad!
    claim = {
        "field": "accounts.revenue",
        "value": 1000000,
        "reporting_period": {
            "fiscal_year": "2025",
            "start_date": "2025-01-01",
            "end_date": "2025-12-31",
            "currency": "NOK"
        }
    }
    ev = {"locator": "/0/resultatregnskapResultat/driftsresultat/driftskostnad/sumDriftskostnad"}
    status, reason, _ = audit_accounts_claim(ORG, claim, ev, body)
    assert status == "INCORRECT", f"Auditor falsely accepted revenue claim with expense locator: {reason}"
