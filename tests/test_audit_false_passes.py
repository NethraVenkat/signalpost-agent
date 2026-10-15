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


# -----------------------------------------------------------------------------
# 13. Description: First 5 words match but remaining claim contains fabricated facts
# -----------------------------------------------------------------------------
def test_description_partial_word_match_rejected():
    """
    Proves that a description claim whose first five words appear in the source
    but which contains invented statements (e.g. lunar mining fleet) is strictly rejected.
    """
    body = "<html><body>Norwegian software company builds tools for developer automation.</body></html>"
    claim = {
        "field": "website_description.about_paragraph.1234",
        "value": "Norwegian software company builds tools. It also owns a lunar mining fleet."
    }
    ev = {"locator": "visible:p:first"}
    from scripts.accuracy_audit import audit_website_metadata_claim
    status, reason, _ = audit_website_metadata_claim(ORG, claim, ev, body)
    assert status == "INCORRECT", f"Auditor falsely passed description with invented lunar fleet: {reason}"
    assert "not found" in reason.lower()


# -----------------------------------------------------------------------------
# 14. Description: Summary description without sentence-level citations
# -----------------------------------------------------------------------------
def test_summary_description_without_sentence_citations_unverifiable():
    body = "<html><body>Norwegian software company builds tools.</body></html>"
    claim = {
        "field": "website_description.summary",
        "value": {
            "kind": "summary",
            "text": "Norwegian software company builds tools."
        }
    }
    ev = {"locator": "/"}
    from scripts.accuracy_audit import audit_website_metadata_claim
    status, reason, _ = audit_website_metadata_claim(ORG, claim, ev, body)
    assert status == "UNVERIFIABLE", f"Auditor should mark summary without sentence citations UNVERIFIABLE: {reason}"


# -----------------------------------------------------------------------------
# 15. Website ownership: Directory/aggregator domain (proff.no) rejected
# -----------------------------------------------------------------------------
def test_website_directory_page_rejected():
    body = "<html><body><h1>AUTONEXT AS</h1><p>Org.nr: 999 592 236</p></body></html>"
    claim = {
        "field": "official_website",
        "value": {
            "final_url": "https://proff.no/selskap/autonext-as/mosj%C3%B8en/biler-og-kj%C3%B8ret%C3%B8y/IF5Z7IO016D",
            "proof_type": "orgnr_on_page"
        }
    }
    ev = {"locator": "/"}
    status, reason, _ = audit_website_claim(ORG, claim, ev, body)
    assert status == "INCORRECT", f"Auditor falsely accepted directory page on proff.no: {reason}"
    assert "directory" in reason.lower() or "aggregator" in reason.lower()


# -----------------------------------------------------------------------------
# 16. Website ownership: Orgnr only present in script markup rejected
# -----------------------------------------------------------------------------
def test_website_script_only_orgnr_rejected():
    body = """<html>
      <head>
        <script type="text/javascript">
          var trackingConfig = { accountId: "999592236", event: "pageview" };
        </script>
      </head>
      <body>
        <h1>Welcome to Acme Portal</h1>
      </body>
    </html>"""
    claim = {
        "field": "official_website",
        "value": {
            "final_url": "https://example.no",
            "proof_type": "orgnr_on_page"
        }
    }
    ev = {"locator": "/"}
    status, reason, _ = audit_website_claim(ORG, claim, ev, body)
    assert status == "INCORRECT", f"Auditor falsely accepted orgnr only in script tags: {reason}"
    assert "script" in reason.lower() or "invisible" in reason.lower()


# -----------------------------------------------------------------------------
# 17. Website ownership: Orgnr only in customer/partner references rejected
# -----------------------------------------------------------------------------
def test_website_partner_customer_mention_rejected():
    body = """<html>
      <head><title>Software Agency AS</title></head>
      <body>
        <h1>Our Web Development Agency</h1>
        <h2>Våre fornøyde kunder</h2>
        <p>Vi har levert systemer til AUTONEXT AS (org.nr 999592236) siden 2020.</p>
        <footer>
          <p>© 2026 Agency AS - Org.nr 910000004</p>
        </footer>
      </body>
    </html>"""
    claim = {
        "field": "official_website",
        "value": {
            "final_url": "https://agency.example.no",
            "proof_type": "orgnr_on_page"
        }
    }
    ev = {"locator": "/"}
    status, reason, _ = audit_website_claim(ORG, claim, ev, body)
    assert status == "INCORRECT", f"Auditor falsely accepted partner/customer reference: {reason}"
    assert "foreign" in reason.lower() or "partner" in reason.lower() or "customer" in reason.lower()


# -----------------------------------------------------------------------------
# 18. Website ownership: Multi-entity group list / directory table rejected
# -----------------------------------------------------------------------------
def test_website_multi_entity_group_list_rejected():
    body = """<html>
      <body>
        <h1>Group Subsidiary Directory</h1>
        <table>
          <tr><td>Subsidiary A</td><td>999592236</td></tr>
          <tr><td>Subsidiary B</td><td>910000004</td></tr>
          <tr><td>Subsidiary C</td><td>910000012</td></tr>
          <tr><td>Subsidiary D</td><td>910000020</td></tr>
        </table>
      </body>
    </html>"""
    claim = {
        "field": "official_website",
        "value": {
            "final_url": "https://conglomerate-holding.no/subsidiaries",
            "proof_type": "orgnr_on_page"
        }
    }
    ev = {"locator": "/"}
    status, reason, _ = audit_website_claim(ORG, claim, ev, body)
    assert status == "INCORRECT", f"Auditor falsely accepted multi-entity list: {reason}"
    assert "multi-entity" in reason.lower() or "directory" in reason.lower()


# -----------------------------------------------------------------------------
# 19. Website ownership: Verified footer context accepted
# -----------------------------------------------------------------------------
def test_website_verified_footer_accepted():
    body = """<html>
      <head><title>AUTONEXT AS - Bilforhandler</title></head>
      <body>
        <h1>Velkommen til Autonext</h1>
        <footer>
          <p>© 2026 AUTONEXT AS. Organisasjonsnummer 999 592 236 MVA. Lensegata 18, 8656 Mosjøen.</p>
        </footer>
      </body>
    </html>"""
    claim = {
        "field": "official_website",
        "value": {
            "final_url": "https://autonext.no",
            "proof_type": "orgnr_on_page"
        }
    }
    ev = {"locator": "visible:p:first"}
    status, reason, val = audit_website_claim(ORG, claim, ev, body)
    assert status == "CORRECT", f"Auditor rejected genuine footer ownership proof: {reason}"
    assert val == "https://autonext.no"


# -----------------------------------------------------------------------------
# 20. Website ownership: Registry declaration verified against Brønnøysund record
# -----------------------------------------------------------------------------
def test_website_registry_declaration_accepted():
    csv_body = "organisasjonsnummer,navn,hjemmeside\n999592236,AUTONEXT AS,autonext.no\n"
    claim = {
        "field": "official_website",
        "value": {
            "final_url": "https://autonext.no",
            "proof_type": "registry_declared"
        }
    }
    ev = {"locator": "row:999592236/column:hjemmeside"}
    context = {"website": "autonext.no"}
    status, reason, val = audit_website_claim(
        ORG, claim, ev, "<html><body>Hello</body></html>", registry_body=csv_body, context=context
    )
    assert status == "CORRECT", f"Auditor rejected valid registry declaration: {reason}"
    assert val == "https://autonext.no"


# -----------------------------------------------------------------------------
# 21. Multi-entity group site: Legitimate multi-entity contact page accepted
# -----------------------------------------------------------------------------
def test_website_legitimate_multi_entity_group_contact_page_accepted():
    from signalpost.web.proof import score
    from signalpost.web.html import Page

    simployer_org = "921407025"
    body = """<html>
      <head><title>Contact Us - Simployer</title></head>
      <body>
        <main>
          <h2>Incoming invoices to Simployer</h2>
          <div class="card-content">
            <div class="card-body">
              <h3>Simployer Group AS</h3>
              <span>Organisation number: 937 475 918<br>Invoice e-mail: invoicegroup@simployer.com</span>
            </div>
          </div>
          <div class="card-content">
            <div class="card-body">
              <h3>Simployer Solutions</h3>
              <span>Organisation number: 921 407 025<br>Invoice e-mail: invoicesolutions@simployer.com<br>Invoice address: Kalnesveien 5, 1712 Grålum</span>
            </div>
          </div>
          <div class="card-content">
            <div class="card-body">
              <h3>Simployer AS</h3>
              <span>Organisation number: 986 419 454<br>Invoice e-mail: invoiceNO@simployer.com</span>
            </div>
          </div>
        </main>
      </body>
    </html>"""

    # 1. Test production score()
    page = Page(body.encode("utf-8"), "https://www.simployer.com/contact-us")
    context = {"name": "SIMPLOYER SOLUTIONS AS", "website": "www.simployer.com"}
    proof = score(page, simployer_org, context, "registry_website", [])
    assert proof.level == "VERIFIED"
    assert proof.other_orgnrs == ["937475918", "986419454"]

    # 2. Test accuracy auditor
    claim = {
        "field": "official_website",
        "value": {
            "final_url": "https://www.simployer.com",
            "proof_type": "orgnr_on_page",
            "candidate_origin": "registry_website",
            "relationship_note": "group_site",
            "other_orgnrs": ["937475918", "986419454"]
        }
    }
    ev = {"locator": "identity-proof:921407025"}
    status, reason, val = audit_website_claim(
        simployer_org, claim, ev, body, context=context
    )
    assert status == "CORRECT", f"Auditor rejected legitimate group contact page: {reason}"
    assert val == "https://www.simployer.com"


# -----------------------------------------------------------------------------
# 22. Multi-entity group site: Incorrectly attributed group site rejected
# -----------------------------------------------------------------------------
def test_website_incorrectly_attributed_group_site_rejected():
    from signalpost.web.proof import score
    from signalpost.web.html import Page

    body = """<html>
      <head><title>Holding Group - Directory</title></head>
      <body>
        <header><h1>Holding Group Enterprise Directory</h1></header>
        <main>
          <p>Holding Group operates diversified businesses across technology, consulting, logistics and retail across the Nordic region. We provide corporate governance and support functions.</p>
          <p>Holding Group Enterprise Directory provides information on group entities and administrative corporate listings across all divisions.</p>
          <h1>Group Structure</h1>
          <p>The following entities are part of the conglomerate:</p>
          <table>
            <tr><td>Subsidiary A</td><td>999592236</td></tr>
            <tr><td>Subsidiary B</td><td>937475918</td></tr>
            <tr><td>Subsidiary C</td><td>986419454</td></tr>
          </table>
        </main>
        <footer><p>© Holding Group 2026. All rights reserved.</p></footer>
      </body>
    </html>"""

    # 1. Production score() on guessed slug candidate must reject multi-entity directory table
    page = Page(body.encode("utf-8"), "https://www.conglomerate-holding.no/structure")
    context = {"name": "AUTONEXT AS", "website": "autonext.no"}
    proof = score(page, ORG, context, "legal_name_slug", [])
    assert proof.level == "REJECT", f"Production verifier accepted unverified multi-entity page: {proof.level}"
    assert proof.reason == "unverified_multi_entity_site"

    # 2. Auditor must reject claim missing relationship_note
    claim_no_note = {
        "field": "official_website",
        "value": {
            "final_url": "https://www.conglomerate-holding.no",
            "proof_type": "orgnr_on_page",
            "candidate_origin": "registry_website",
            "other_orgnrs": ["937475918", "986419454"]
        }
    }
    ev = {"locator": "/"}
    status, reason, _ = audit_website_claim(ORG, claim_no_note, ev, body, context=context)
    assert status == "INCORRECT", f"Auditor accepted group site missing relationship_note: {reason}"

    # 3. Auditor must reject claim on uncorroborated domain
    claim_uncorroborated = {
        "field": "official_website",
        "value": {
            "final_url": "https://www.conglomerate-holding.no",
            "proof_type": "orgnr_on_page",
            "candidate_origin": "legal_name_slug",
            "relationship_note": "group_site",
            "other_orgnrs": ["937475918", "986419454"]
        }
    }
    status, reason, _ = audit_website_claim(ORG, claim_uncorroborated, ev, body, context=context)
    assert status == "INCORRECT", f"Auditor accepted uncorroborated domain as group site: {reason}"


# -----------------------------------------------------------------------------
# 23. Group-site claim attribution: Two company cards with different invoice emails
# -----------------------------------------------------------------------------
def test_group_site_two_company_cards_different_invoice_emails():
    """
    On a multi-entity group site, contacts located inside a sibling entity card
    must NOT be attributed to the subject company.
    """
    from scripts.accuracy_audit import audit_website_metadata_claim

    body = """<html>
      <body>
        <div class="card entity-card">
          <h3>Simployer Solutions</h3>
          <p>Organisation number: 921 407 025</p>
          <p>Invoice e-mail: invoicesolutions@simployer.com</p>
        </div>
        <div class="card entity-card">
          <h3>Simployer AS</h3>
          <p>Organisation number: 986 419 454</p>
          <p>Invoice e-mail: invoiceNO@simployer.com</p>
        </div>
      </body>
    </html>"""

    subject_org = "921407025"

    # 1. Subject entity contact: invoicesolutions@simployer.com -> CORRECT
    claim_correct = {
        "field": "contact.email.1",
        "value": "invoicesolutions@simployer.com"
    }
    status, reason, _ = audit_website_metadata_claim(
        subject_org, claim_correct, {"locator": "contact:invoicesolutions@simployer.com"}, body,
        website_claim={"value": {"relationship_note": "group_site", "other_orgnrs": ["986419454"]}}
    )
    assert status == "CORRECT", f"Auditor rejected legitimate entity contact: {reason}"

    # 2. Sibling entity contact: invoiceNO@simployer.com -> INCORRECT for subject 921407025
    claim_sibling = {
        "field": "contact.email.2",
        "value": "invoiceNO@simployer.com"
    }
    status, reason, _ = audit_website_metadata_claim(
        subject_org, claim_sibling, {"locator": "contact:invoiceNO@simployer.com"}, body,
        website_claim={"value": {"relationship_note": "group_site", "other_orgnrs": ["986419454"]}}
    )
    assert status == "INCORRECT", f"Auditor accepted sibling entity contact: {reason}"
    assert "sibling" in reason.lower() or "other entity" in reason.lower() or "card" in reason.lower()


# -----------------------------------------------------------------------------
# 24. Group-site claim attribution: One shared group contact requires explicit scope
# -----------------------------------------------------------------------------
def test_group_site_shared_group_contact_unlabelled_rejected_as_entity_contact():
    """
    On a group site, a shared group contact (e.g. info@simployer.com in footer)
    without entity-specific link must NOT be published as an entity-specific contact.
    """
    from scripts.accuracy_audit import audit_website_metadata_claim

    body = """<html>
      <body>
        <div class="card entity-card">
          <h3>Simployer Solutions</h3>
          <p>Organisation number: 921 407 025</p>
        </div>
        <footer>
          <p>Group Head Office: info@simployer.com</p>
        </footer>
      </body>
    </html>"""

    subject_org = "921407025"
    claim = {
        "field": "contact.email.group",
        "value": "info@simployer.com"
    }
    status, reason, _ = audit_website_metadata_claim(
        subject_org, claim, {"locator": "contact:info@simployer.com"}, body,
        website_claim={"value": {"relationship_note": "group_site", "other_orgnrs": ["986419454"]}}
    )
    assert status == "INCORRECT", f"Auditor accepted unlabelled shared contact as entity contact: {reason}"


# -----------------------------------------------------------------------------
# 25. Group-site claim attribution: Sibling-company social account rejected
# -----------------------------------------------------------------------------
def test_group_site_sibling_company_social_account_rejected():
    """
    A social account belonging to a sibling or parent entity must NOT be published
    as the subsidiary subject's social profile.
    """
    from scripts.accuracy_audit import audit_social_claim

    body = """<html>
      <body>
        <div class="card entity-card">
          <h3>Simployer Solutions</h3>
          <p>Organisation number: 921 407 025</p>
        </div>
        <div class="card entity-card">
          <h3>Simployer Group AS</h3>
          <p>Organisation number: 937 475 918</p>
          <a href="https://www.linkedin.com/company/simployergroup">Group LinkedIn</a>
        </div>
      </body>
    </html>"""

    subject_org = "921407025"
    claim = {
        "field": "social_profile.simployergroup",
        "value": {
            "url": "https://www.linkedin.com/company/simployergroup",
            "platform": "linkedin.com"
        }
    }
    status, reason, _ = audit_social_claim(
        subject_org, claim, {"locator": "company-link:https://www.linkedin.com/company/simployergroup"}, body,
        website_claim={"value": {"relationship_note": "group_site", "other_orgnrs": ["937475918"]}}
    )
    assert status == "INCORRECT", f"Auditor accepted sibling social account: {reason}"


# -----------------------------------------------------------------------------
# 26. Group-site claim attribution: Group customer count must not become subsidiary metric
# -----------------------------------------------------------------------------
def test_group_site_customer_count_not_subsidiary_statistics():
    """
    Group-wide metrics (e.g. '12,000+ companies in the Nordics') must NOT be published
    as the subsidiary's own employee count or scale claim.
    """
    from scripts.accuracy_audit import audit_website_metadata_claim

    body = """<html>
      <body>
        <p>Simployer One is trusted by 12,000+ companies across the Nordics.</p>
      </body>
    </html>"""

    subject_org = "921407025"
    # An extractor claiming 12000 as subsidiary scale/customer count must be rejected
    claim = {
        "field": "company_scale.customer_count",
        "value": 12000
    }
    status, reason, _ = audit_website_metadata_claim(
        subject_org, claim, {"locator": "text"}, body,
        website_claim={"value": {"relationship_note": "group_site", "other_orgnrs": ["937475918"]}}
    )
    assert status in ("INCORRECT", "UNVERIFIABLE")


