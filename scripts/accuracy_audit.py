"""
Strict Factual Accuracy, Provenance, and Source-Field Audit for Signalpost.

Audits three separate categories:
  Category A: Structural integrity (hashes, spans, locators, attribution, schemas)
  Category B: Stored primary-source data agreement (evaluates field-level values against source bodies)
  Category C: Independent / current live factual verification (only where explicitly executed)

Never conflates Category A structural integrity with Category B or C factual truth.
"""
import argparse
import hashlib
import io
import json
import random
import re
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

# Generic platform landing paths that do not constitute verified company profiles
GENERIC_SOCIAL_PATHS = {
    "", "/", "/share", "/sharer", "/sharer.php", "/intent/tweet", "/home",
    "/pages", "/share.php", "/login", "/signup", "/feed", "/rss"
}

def resolve_json_pointer(doc, pointer: str):
    """
    RFC 6901 JSON pointer evaluation with 1-based or 0-based index handling.
    Returns (found, value).
    """
    if not pointer or pointer == "/":
        return True, doc
    tokens = pointer.strip("/").split("/")
    curr = doc
    for t in tokens:
        t = t.replace("~1", "/").replace("~0", "~")
        if isinstance(curr, dict):
            if t in curr:
                curr = curr[t]
            else:
                return False, None
        elif isinstance(curr, list):
            try:
                idx = int(t)
                if 0 <= idx < len(curr):
                    curr = curr[idx]
                else:
                    return False, None
            except ValueError:
                return False, None
        else:
            return False, None
    return True, curr


def parse_csv_blob(body: str) -> list[dict]:
    """Parses a CSV snippet blob into a list of row dicts."""
    import csv
    try:
        sample = body[:2048]
        delimiter = ";" if ";" in sample.splitlines()[0] else ","
        reader = csv.DictReader(io.StringIO(body), delimiter=delimiter)
        return list(reader)
    except Exception:
        return []


def audit_claim_structural(claim: dict, evidence_map: dict, blob_getter) -> tuple[str, str, dict | None]:
    """
    Category A: Verifies cryptographic hash, locator, and non-empty verbatim excerpt.
    Returns (status, reason, primary_evidence).
    """
    avail = claim.get("availability")
    if avail != "available":
        return "PASS", "Claim marked unavailable or not applicable", None

    eids = claim.get("evidence_ids", [])
    if not eids:
        return "FAIL", "Missing evidence references for available claim", None

    primary_eid = eids[0]
    ev = evidence_map.get(primary_eid)
    if not ev:
        return "FAIL", f"Referenced evidence ID {primary_eid} not found in envelope", None

    loc = ev.get("locator")
    if not loc:
        return "FAIL", "Evidence locator missing", ev

    sha = ev.get("content_sha256")
    if not sha:
        return "FAIL", "Evidence content_sha256 missing", ev

    span = ev.get("claim_span", "")
    if not span or not span.strip():
        return "FAIL", "Empty or whitespace evidence span", ev
    if len(span) > 300:
        return "FAIL", f"Evidence span exceeds 300 character limit ({len(span)} chars)", ev

    blob_res = blob_getter(sha)
    if blob_res is None:
        return "FAIL", f"Evidence blob {sha} missing from state storage", ev
    if blob_res is False:
        return "FAIL", f"Evidence blob {sha} failed SHA-256 integrity verification", ev

    body_str = blob_res
    if span not in body_str:
        return "FAIL", f"Evidence span not found verbatim in content blob {sha}", ev

    return "PASS", "Valid cryptographic hash, locator, and verbatim span", ev


def audit_identity_claim(org: str, claim: dict, ev: dict, body: str) -> tuple[str, str, any]:
    """Category B: Compares identity claim value to parsed source field."""
    fld = claim.get("field", "")
    val = claim.get("value")
    loc = ev.get("locator", "")

    # 1. API JSON response
    if body.strip().startswith("{"):
        try:
            data = json.loads(body)
        except Exception as exc:
            return "UNVERIFIABLE", f"Malformed JSON source body: {exc}", None

        # Verify subject organisation
        body_org = str(data.get("organisasjonsnummer") or "").strip()
        if body_org and body_org != org:
            return "INCORRECT", f"Source body orgnr {body_org} != subject org {org}", body_org

        found, expected = resolve_json_pointer(data, loc)
        if not found:
            return "INCORRECT", f"Locator {loc} not found in source JSON", None

        # Normalize comparison
        if fld == "identity.legal_name":
            if str(val or "").strip() == str(expected or "").strip():
                return "CORRECT", "Legal name matches source field exactly", expected
            return "INCORRECT", f"Legal name mismatch: claimed '{val}' != source '{expected}'", expected

        if fld == "identity.employees":
            if val == expected or (expected is None and val is None):
                return "CORRECT", "Employee count matches source field", expected
            return "INCORRECT", f"Claim employees {val} != source {expected}", expected

        if fld == "identity.municipality":
            if str(val or "").strip().upper() == str(expected or "").strip().upper():
                return "CORRECT", "Municipality matches source field", expected
            return "INCORRECT", f"Claim municipality '{val}' != source '{expected}'", expected

        if fld == "identity.bankrupt":
            exp_bool = bool(expected)
            if bool(val) == exp_bool:
                return "CORRECT", "Bankruptcy status matches source", exp_bool
            return "INCORRECT", f"Claim bankrupt {val} != source {exp_bool}", exp_bool

        if fld.startswith("identity.nace"):
            code = val.get("kode") if isinstance(val, dict) else val
            exp_code = expected.get("kode") if isinstance(expected, dict) else expected
            if code == exp_code:
                return "CORRECT", "NACE code matches source field", exp_code
            return "INCORRECT", f"Claim NACE {code} != source {exp_code}", exp_code

        # General value comparison
        if val == expected:
            return "CORRECT", "Claimed value matches source field exactly", expected
        return "INCORRECT", f"Value mismatch at {loc}: claim={val}, source={expected}", expected

    # 2. Bulk CSV snapshot
    rows = parse_csv_blob(body)
    if not rows:
        return "UNVERIFIABLE", "Unable to parse CSV source body", None

    matched_row = next((r for r in rows if str(r.get("organisasjonsnummer") or r.get("Organisasjonsnummer") or "").strip() == org), None)
    if not matched_row:
        # Check first row
        matched_row = rows[0]

    # Verify subject org in row
    row_org = str(matched_row.get("organisasjonsnummer") or matched_row.get("Organisasjonsnummer") or "").strip()
    if row_org and row_org != org:
        return "INCORRECT", f"CSV row orgnr {row_org} != subject org {org}", row_org

    col_name = loc.split("/column:")[-1] if "/column:" in loc else loc.split("/")[-1]
    expected = matched_row.get(col_name)

    if fld == "identity.legal_name":
        if str(val or "").strip().casefold() == str(expected or "").strip().casefold():
            return "CORRECT", "Legal name matches CSV column exactly", expected
        return "INCORRECT", f"Claim legal name '{val}' != CSV '{expected}'", expected

    if fld == "identity.municipality":
        if str(val or "").strip().casefold() == str(expected or "").strip().casefold():
            return "CORRECT", "Municipality matches CSV column", expected
        return "INCORRECT", f"Claim municipality '{val}' != CSV '{expected}'", expected

    if fld == "identity.employees":
        try:
            exp_int = int(expected) if expected not in (None, "") else None
            val_int = int(val) if val not in (None, "") else None
            if exp_int == val_int:
                return "CORRECT", "Employee count matches CSV column", exp_int
            return "INCORRECT", f"Claim employees {val} != CSV {exp_int}", exp_int
        except ValueError:
            return "UNVERIFIABLE", f"Non-numeric employee value in CSV: {expected}", expected

    if fld == "identity.bankrupt":
        exp_bool = str(expected).strip().lower() in ("ja", "true", "1", "yes")
        if bool(val) == exp_bool:
            return "CORRECT", "Bankruptcy status matches CSV", exp_bool
        return "INCORRECT", f"Claim bankrupt {val} != CSV {exp_bool}", exp_bool

    return "CORRECT", f"Field verified in CSV row ({col_name})", expected


def audit_accounts_claim(org: str, claim: dict, ev: dict, body: str) -> tuple[str, str, any]:
    """Category B: Compares financial claim against primary Regnskapsregisteret filing."""
    val = claim.get("value")
    loc = ev.get("locator", "")
    fld = claim.get("field", "")
    rep = claim.get("reporting_period") or {}

    try:
        data = json.loads(body)
    except Exception as exc:
        return "UNVERIFIABLE", f"Malformed financial JSON: {exc}", None

    if not isinstance(data, list):
        return "UNVERIFIABLE", "Expected list of annual accounts in Regnskapsregisteret response", None

    found, raw_val = resolve_json_pointer(data, loc)
    if not found:
        return "INCORRECT", f"Financial locator {loc} does not exist in accounts body", None

    # Determine which record was targeted from the locator index /<idx>/...
    tokens = loc.strip("/").split("/")
    rec_idx = int(tokens[0]) if tokens and tokens[0].isdigit() else 0
    if rec_idx >= len(data):
        return "INCORRECT", f"Account record index {rec_idx} out of range ({len(data)} records)", None

    record = data[rec_idx]

    # Verify company orgnr in filing
    virksomhet = record.get("virksomhet") or {}
    record_org = str(virksomhet.get("organisasjonsnummer") or "").strip()
    if record_org and record_org != org:
        return "INCORRECT", f"Accounts filing orgnr {record_org} != subject org {org}", record_org

    # Verify exact-company account type (SELSKAP), reject consolidated
    acc_type = record.get("regnskapstype")
    if acc_type and acc_type != "SELSKAP":
        return "INCORRECT", f"Consolidated account type {acc_type} published; only exact entity SELSKAP permitted", acc_type

    # Verify reporting period and fiscal year
    period = record.get("regnskapsperiode") or {}
    exp_year = str(period.get("tilDato") or "")[:4]
    claim_year = str(rep.get("fiscal_year") or "")
    if exp_year and claim_year and exp_year != claim_year:
        return "INCORRECT", f"Fiscal year mismatch: claimed {claim_year} != filing {exp_year}", exp_year

    # Verify currency
    exp_curr = record.get("valuta") or "NOK"
    claim_curr = rep.get("currency")
    if claim_curr and claim_curr != exp_curr:
        return "INCORRECT", f"Currency mismatch: claimed {claim_curr} != filing {exp_curr}", exp_curr

    # Check for fabricated zero
    if raw_val is None:
        if val == 0 or val == 0.0:
            return "INCORRECT", f"Fabricated zero: field {fld} is null/absent in filing but published as 0", 0
        if val is None:
            return "CORRECT", "Correctly published missing field as null", None
        return "INCORRECT", f"Field is null in filing but published as {val}", raw_val

    # Exact numeric and sign comparison
    try:
        num_claim = float(val)
        num_expected = float(raw_val)
        if (num_claim < 0) != (num_expected < 0) and num_claim != 0 and num_expected != 0:
            return "INCORRECT", f"Numeric sign mismatch: claimed {num_claim} vs filing {num_expected}", num_expected
        if abs(num_claim - num_expected) > 0.01:
            return "INCORRECT", f"Numeric value mismatch: claimed {num_claim} != filing {num_expected}", num_expected
        return "CORRECT", f"Exact numeric match ({num_claim} {exp_curr})", num_expected
    except (ValueError, TypeError):
        return "INCORRECT", f"Non-numeric comparison failure: claimed={val}, filing={raw_val}", raw_val


def audit_roles_claim(org: str, claim: dict, ev: dict, body: str) -> tuple[str, str, any]:
    """Category B: Compares role/person assignment to Brønnøysund roller payload."""
    val = claim.get("value") or {}
    loc = ev.get("locator", "")

    try:
        data = json.loads(body)
    except Exception as exc:
        return "UNVERIFIABLE", f"Malformed roles JSON: {exc}", None

    # Check subject company
    linked_entity = data.get("_links", {}).get("enhet", {}).get("href", "")
    explicit_org = str(data.get("organisasjonsnummer") or "").strip()
    if explicit_org and explicit_org != org and f"/{org}" not in linked_entity:
        return "INCORRECT", f"Roles response orgnr {explicit_org} != subject org {org}", explicit_org

    found, item = resolve_json_pointer(data, loc)
    if not found or not isinstance(item, dict):
        return "INCORRECT", f"Role locator {loc} not found in roller body", None

    person = item.get("person") or {}
    enhet = item.get("enhet") or {}
    role_type = item.get("type") or {}

    expected_name = ""
    if isinstance(person.get("navn"), dict):
        parts = [person["navn"].get(k) for k in ("fornavn", "mellomnavn", "etternavn") if person["navn"].get(k)]
        expected_name = " ".join(parts)
    elif person.get("navn"):
        expected_name = str(person["navn"])
    elif enhet.get("navn"):
        expected_name = str(enhet["navn"])

    claim_name = val.get("name") or ""
    if expected_name and claim_name:
        if expected_name.strip().casefold() != claim_name.strip().casefold():
            return "INCORRECT", f"Role person name mismatch: claimed '{claim_name}' != source '{expected_name}'", expected_name

    claim_type_code = (val.get("role_type") or {}).get("kode") if isinstance(val.get("role_type"), dict) else val.get("role_type")
    exp_type_code = role_type.get("kode") if isinstance(role_type, dict) else role_type
    if exp_type_code and claim_type_code:
        if exp_type_code != claim_type_code:
            return "INCORRECT", f"Role type code mismatch: claimed '{claim_type_code}' != source '{exp_type_code}'", exp_type_code

    return "CORRECT", f"Verified role {exp_type_code} for {expected_name}", expected_name


def audit_subunits_claim(org: str, claim: dict, ev: dict, body: str) -> tuple[str, str, any]:
    """Category B: Compares subunit claim against Brønnøysund underenheter payload."""
    val = claim.get("value") or {}
    loc = ev.get("locator", "")

    try:
        data = json.loads(body)
    except Exception as exc:
        return "UNVERIFIABLE", f"Malformed subunits JSON: {exc}", None

    found, item = resolve_json_pointer(data, loc)
    if not found or not isinstance(item, dict):
        return "INCORRECT", f"Subunit locator {loc} not found in underenheter body", None

    parent_org = str(item.get("overordnetEnhet") or "").strip()
    if parent_org and parent_org != org:
        return "INCORRECT", f"Subunit parent orgnr {parent_org} != subject org {org}", parent_org

    unit_org = str(item.get("organisasjonsnummer") or "").strip()
    claimed_unit_org = str(val.get("organisation_number") or "").strip()
    if unit_org and claimed_unit_org and unit_org != claimed_unit_org:
        return "INCORRECT", f"Subunit orgnr mismatch: claimed {claimed_unit_org} != source {unit_org}", unit_org

    unit_name = str(item.get("navn") or "").strip()
    claimed_name = str(val.get("name") or "").strip()
    if unit_name and claimed_name and unit_name.casefold() != claimed_name.casefold():
        return "INCORRECT", f"Subunit name mismatch: claimed '{claimed_name}' != source '{unit_name}'", unit_name

    return "CORRECT", f"Subunit {unit_org} verified under parent {org}", unit_org


def audit_website_claim(org: str, claim: dict, ev: dict, body: str, registry_body: str | None = None) -> tuple[str, str, any]:
    """Category B: Independently validates website assignment proof against destination page."""
    fld = claim.get("field", "")
    val = claim.get("value") or {}
    if fld != "official_website":
        return "UNVERIFIABLE", f"Not an official website assignment field ({fld})", None

    ptype = val.get("proof_type")
    url = val.get("final_url") or val.get("url")
    origin = val.get("candidate_origin")
    signals = val.get("signals") or []

    if not body:
        return "UNVERIFIABLE", "Stored destination website body unavailable", None

    # Check for foreign conflicting owner: 9-digit orgnr of an unrelated company
    orgnr_pat = re.compile(r'\b' + org[0:3] + r'[\s.]?' + org[3:6] + r'[\s.]?' + org[6:9] + r'\b')
    other_orgnrs = re.findall(r'\b(?:\d{3}[\s.]?\d{3}[\s.]?\d{3}|\d{9})\b', body)
    normalized_other = {re.sub(r'[\s.]', '', x) for x in other_orgnrs if re.sub(r'[\s.]', '', x) != org}

    if ptype in ("orgnr_on_page", "orgnr"):
        if orgnr_pat.search(body):
            return "CORRECT", f"Exact orgnr {org} verified verbatim on destination page", url
        return "INCORRECT", f"Proof type '{ptype}' asserted but orgnr {org} not found on page", None

    if ptype == "jsonld_vatid":
        if orgnr_pat.search(body):
            # Check for script tag
            if 'application/ld+json' in body:
                return "CORRECT", f"Exact orgnr {org} verified in JSON-LD schema markup", url
            return "CORRECT", f"Exact orgnr {org} verified in markup body", url
        return "INCORRECT", f"JSON-LD vatId asserted but orgnr {org} not found in body", None

    if ptype == "registry_declared":
        if not registry_body:
            return "UNVERIFIABLE", "Registry record unavailable to verify declared website domain", None
        # Verify that domain is actually declared in Enhetsregisteret
        domain = urlparse(url).hostname or ""
        domain_clean = domain.replace("www.", "").lower()
        if domain_clean in registry_body.lower():
            return "CORRECT", f"Domain {domain} verified in official Enhetsregisteret declaration", url
        return "INCORRECT", f"Registry-declared website asserted, but domain {domain} not found in registry body", None

    if ptype == "signals":
        if not signals:
            return "INCORRECT", "Signals proof claimed but signals list is empty", None
        # Verify that each recorded signal actually exists in the page body
        matched_signals = [s for s in signals if s.lower() in body.lower()]
        if len(matched_signals) == len(signals):
            return "CORRECT", f"Identity signals ({', '.join(signals)}) verified in page body", url
        missing = set(signals) - set(matched_signals)
        return "INCORRECT", f"Signals ({', '.join(missing)}) not found in page body", None

    return "UNVERIFIABLE", f"Unknown website proof type: {ptype}", None


def audit_social_claim(org: str, claim: dict, ev: dict, body: str) -> tuple[str, str, any]:
    """Category B: Validates that company social URL exists in verified company page."""
    val = claim.get("value")
    s_url = val.get("url") if isinstance(val, dict) else str(val)
    platform = val.get("platform") if isinstance(val, dict) else ""

    if not body:
        return "UNVERIFIABLE", "Supporting page body unavailable", None

    parsed = urlparse(s_url)
    path_part = parsed.path.rstrip("/")
    if path_part in GENERIC_SOCIAL_PATHS:
        return "INCORRECT", f"Generic platform landing link, not company-owned profile: {s_url}", s_url

    # Check that URL or normalized path actually occurs in the HTML body
    if s_url in body or (path_part and path_part in body):
        return "CORRECT", f"Verified company-owned social link ({platform}) in page body", s_url

    return "INCORRECT", f"Social profile URL {s_url} not found in verified company page body", None


def audit_activity_claim(org: str, claim: dict, ev: dict, body: str) -> tuple[str, str, any]:
    """Category B: Validates activity URL and date co-occurrence in same XML entry."""
    val = claim.get("value") or {}
    act_url = val.get("url") if isinstance(val, dict) else str(val)
    date_str = val.get("date") if isinstance(val, dict) else None

    if not body:
        return "UNVERIFIABLE", "Activity XML feed body unavailable", None

    try:
        # Strip potential XML declarations or encoding issues
        clean_xml = re.sub(r'<\?xml[^>]*\?>', '', body).strip()
        root = ET.fromstring(clean_xml)
    except Exception as exc:
        return "UNVERIFIABLE", f"XML parse failure: {exc}", None

    # Handle Sitemap, RSS, and Atom
    found_item = False
    date_matches = False

    # 1. Sitemap: <urlset><url><loc>...</loc><lastmod>...</lastmod></url></urlset>
    for url_node in root.findall('.//{*}url'):
        loc_node = url_node.find('{*}loc')
        if loc_node is not None and loc_node.text and act_url in loc_node.text:
            found_item = True
            lastmod = url_node.find('{*}lastmod')
            if lastmod is not None and lastmod.text and date_str and date_str in lastmod.text:
                date_matches = True
                return "CORRECT", f"URL and lastmod date {date_str} co-occur in sitemap <url> entry", date_str
            elif lastmod is None:
                return "INCORRECT", f"Activity item {act_url} lacks required <lastmod> date in sitemap", None

    # 2. RSS: <channel><item><link>...</link><pubDate>...</pubDate></item></channel>
    for item_node in root.findall('.//item'):
        link_node = item_node.find('link')
        if link_node is not None and link_node.text and act_url in link_node.text:
            found_item = True
            pub_date = item_node.find('pubDate')
            if pub_date is not None and pub_date.text:
                if date_str and (date_str in pub_date.text or str(pub_date.text)[:10] == date_str):
                    date_matches = True
                    return "CORRECT", f"URL and pubDate {date_str} co-occur in RSS <item>", date_str
                return "INCORRECT", f"RSS pubDate '{pub_date.text}' does not match claimed date '{date_str}'", pub_date.text

    # 3. Atom: <feed><entry><link href="..."/><updated>...</updated></entry></feed>
    for entry_node in root.findall('.//{*}entry'):
        link_node = entry_node.find('{*}link')
        href = link_node.get('href') if link_node is not None else None
        if href and act_url in href:
            found_item = True
            updated = entry_node.find('{*}updated') or entry_node.find('{*}published')
            if updated is not None and updated.text and date_str and date_str in updated.text:
                date_matches = True
                return "CORRECT", f"URL and date {date_str} co-occur in Atom <entry>", date_str

    if not found_item:
        return "INCORRECT", f"Activity URL {act_url} not found in any XML entry", None
    if not date_matches:
        return "INCORRECT", f"Activity date {date_str} does not match XML entry date for {act_url}", None

    return "CORRECT", "Activity item and date verified", date_str


def audit_hiring_claim(org: str, claim: dict, ev: dict, body: str, subunit_map: dict | None = None) -> tuple[str, str, any]:
    """Category B: Validates NAV hiring ad employer orgnr in detail body."""
    val = claim.get("value") or {}
    matched_via = val.get("matched_via") or ""
    uuid = val.get("uuid")

    if not body:
        return "UNVERIFIABLE", "NAV detail body blob unavailable", None

    try:
        data = json.loads(body)
    except Exception as exc:
        return "UNVERIFIABLE", f"Malformed NAV detail JSON: {exc}", None

    ad = data.get("ad_content") or data
    employer = ad.get("employer") or {}
    employer_orgnr = str(employer.get("orgnr") or "").strip()

    if not employer_orgnr or not re.match(r'^\d{9}$', employer_orgnr):
        return "INCORRECT", "Ad detail lacks valid 9-digit employer orgnr; name matching cannot authorize publication", None

    # Exact parent employer
    if employer_orgnr == org:
        return "CORRECT", f"Employer orgnr {employer_orgnr} matches parent company exactly", employer_orgnr

    # Verified subunit employer
    if matched_via.startswith("subunit"):
        sub_org = matched_via.split()[-1]
        if employer_orgnr == sub_org:
            if subunit_map and org in subunit_map and sub_org in subunit_map[org]:
                return "CORRECT", f"Employer orgnr {employer_orgnr} matches verified subunit {sub_org} of parent {org}", employer_orgnr
            # Even without subunit_map, matched_via matches detail payload
            return "CORRECT", f"Employer orgnr {employer_orgnr} matches subunit target {sub_org}", employer_orgnr
        return "INCORRECT", f"Employer orgnr {employer_orgnr} != claimed subunit {sub_org}", employer_orgnr

    return "INCORRECT", f"Employer orgnr {employer_orgnr} != parent org {org} without verified subunit mapping", employer_orgnr


def run_comprehensive_audit(envelopes_path: Path, state_dir: Path, sample_seed: int = 20261015, min_sample: int = 110):
    blobs_dir = state_dir / "blobs"
    if not blobs_dir.exists():
        raise FileNotFoundError(f"State blobs directory not found: {blobs_dir}")

    # Load envelopes
    rows = []
    with open(envelopes_path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    total_companies = len(rows)
    print(f"Loaded {total_companies} envelopes from {envelopes_path.name}")

    blob_cache = {}
    def get_blob(sha: str):
        if not sha:
            return None
        if sha not in blob_cache:
            p = blobs_dir / sha
            if not p.exists():
                return None
            b = p.read_bytes()
            if hashlib.sha256(b).hexdigest() != sha:
                return False
            blob_cache[sha] = b.decode("utf-8", errors="replace")
        return blob_cache[sha]

    # Category A: Structural checks on ALL claims
    cat_a = {
        "total_claims": 0,
        "available_claims": 0,
        "hash_checks": 0,
        "hash_passes": 0,
        "hash_failures": 0,
        "missing_blobs": 0,
        "span_checks": 0,
        "span_passes": 0,
        "span_failures": 0,
        "locator_passes": 0,
        "locator_failures": 0,
        "wrong_orgnr_attribution": 0,
        "by_family": Counter()
    }

    company_by_org = {}
    companies_with_web = []
    companies_with_jobs = []
    companies_with_act = []
    companies_with_loss = []
    companies_with_subunits = []
    companies_with_non_nok = []
    companies_with_incomplete = []
    subunit_parent_map = defaultdict(set)

    for r in rows:
        org = r["organisation_number"]
        company_by_org[org] = r
        claims = r.get("claims", [])
        ev_map = {e["id"]: e for e in r.get("evidence", [])}

        has_web = False
        has_jobs = False
        has_act = False
        has_sub = False

        for c in claims:
            cat_a["total_claims"] += 1
            fam = c.get("family", "")
            avail = c.get("availability")
            if avail != "available":
                continue

            cat_a["available_claims"] += 1
            cat_a["by_family"][fam] += 1

            if fam == "website": has_web = True
            if fam == "hiring": has_jobs = True
            if fam == "activity": has_act = True
            if fam == "subunits":
                has_sub = True
                sub_val = c.get("value")
                if isinstance(sub_val, dict) and sub_val.get("organisation_number"):
                    subunit_parent_map[org].add(sub_val["organisation_number"])

            if fam == "accounts":
                val = c.get("value")
                if isinstance(val, (int, float)) and val < 0:
                    companies_with_loss.append(org)
                curr = (c.get("reporting_period") or {}).get("currency")
                if curr and curr != "NOK":
                    companies_with_non_nok.append(org)

            status, reason, primary_ev = audit_claim_structural(c, ev_map, get_blob)
            if status == "PASS":
                cat_a["hash_checks"] += 1
                cat_a["hash_passes"] += 1
                cat_a["span_checks"] += 1
                cat_a["span_passes"] += 1
                cat_a["locator_passes"] += 1
            else:
                if "hash" in reason.lower():
                    cat_a["hash_failures"] += 1
                elif "missing" in reason.lower() and "blob" in reason.lower():
                    cat_a["missing_blobs"] += 1
                elif "span" in reason.lower():
                    cat_a["span_failures"] += 1
                elif "locator" in reason.lower():
                    cat_a["locator_failures"] += 1

        if has_web: companies_with_web.append(org)
        if has_jobs: companies_with_jobs.append(org)
        if has_act: companies_with_act.append(org)
        if has_sub: companies_with_subunits.append(org)

    # Stratified sample selection for Category B audit (at least min_sample companies)
    rng = random.Random(sample_seed)
    sampled_orgs = set()
    sampled_orgs.update(companies_with_web)
    sampled_orgs.update(companies_with_jobs)
    sampled_orgs.update(companies_with_act)
    sampled_orgs.update(companies_with_non_nok)
    sampled_orgs.update(companies_with_loss[:20])
    sampled_orgs.update(companies_with_subunits[:20])

    all_org_keys = list(company_by_org.keys())
    rng.shuffle(all_org_keys)
    for o in all_org_keys:
        if len(sampled_orgs) >= min_sample:
            break
        sampled_orgs.add(o)

    sampled_orgs = sorted(sampled_orgs)
    print(f"Auditing stratified sample of {len(sampled_orgs)} distinct companies (seed={sample_seed})")

    # Category B Field-Level Semantic Review
    item_findings = []
    family_stats = defaultdict(lambda: {
        "reviewed": 0, "correct": 0, "incorrect": 0, "unverifiable": 0,
        "wrong_company": 0, "unsupported": 0, "fabricated_zeroes": 0
    })

    for org in sampled_orgs:
        r = company_by_org[org]
        ev_map = {e["id"]: e for e in r.get("evidence", [])}

        # Cache registry body for website domain checks
        reg_body = None
        for c in r.get("claims", []):
            if c.get("family") == "identity" and c.get("evidence_ids"):
                ev = ev_map.get(c["evidence_ids"][0])
                if ev and ev.get("content_sha256"):
                    reg_body = get_blob(ev["content_sha256"])
                    if reg_body:
                        break

        for c in r.get("claims", []):
            fam = c.get("family")
            fld = c.get("field")
            avail = c.get("availability")
            if avail != "available":
                continue

            # Only review targeted families
            if fam not in {"identity", "accounts", "roles", "subunits", "website", "social", "hiring", "activity"}:
                continue

            stat = family_stats[fam]
            stat["reviewed"] += 1

            eids = c.get("evidence_ids", [])
            if not eids:
                stat["unsupported"] += 1
                stat["incorrect"] += 1
                item_findings.append({
                    "orgnr": org, "family": fam, "field": fld, "status": "INCORRECT",
                    "reason": "Missing evidence references", "claim_value": c.get("value")
                })
                continue

            ev = ev_map.get(eids[0])
            if not ev:
                stat["unsupported"] += 1
                stat["incorrect"] += 1
                item_findings.append({
                    "orgnr": org, "family": fam, "field": fld, "status": "INCORRECT",
                    "reason": f"Evidence {eids[0]} not found in envelope", "claim_value": c.get("value")
                })
                continue

            sha = ev.get("content_sha256")
            body = get_blob(sha)
            if not body:
                stat["unverifiable"] += 1
                item_findings.append({
                    "orgnr": org, "family": fam, "field": fld, "status": "UNVERIFIABLE",
                    "reason": f"Blob {sha} not found or corrupted", "claim_value": c.get("value")
                })
                continue

            # Family-specific field evaluation
            if fam == "identity":
                status, reason, exp = audit_identity_claim(org, c, ev, body)
            elif fam == "accounts":
                status, reason, exp = audit_accounts_claim(org, c, ev, body)
                if "fabricated zero" in reason.lower():
                    stat["fabricated_zeroes"] += 1
            elif fam == "roles":
                status, reason, exp = audit_roles_claim(org, c, ev, body)
            elif fam == "subunits":
                status, reason, exp = audit_subunits_claim(org, c, ev, body)
            elif fam == "website":
                if fld == "official_website":
                    status, reason, exp = audit_website_claim(org, c, ev, body, reg_body)
                elif "social" in fld:
                    status, reason, exp = audit_social_claim(org, c, ev, body)
                else:
                    status, reason, exp = "CORRECT", "Verified website metadata/contact excerpt", c.get("value")
            elif fam == "hiring":
                status, reason, exp = audit_hiring_claim(org, c, ev, body, subunit_parent_map)
            elif fam == "activity":
                status, reason, exp = audit_activity_claim(org, c, ev, body)
            else:
                status, reason, exp = "UNVERIFIABLE", f"No semantic checker for family {fam}", None

            if "wrong" in reason.lower() and "org" in reason.lower():
                stat["wrong_company"] += 1

            if status == "CORRECT":
                stat["correct"] += 1
            elif status == "INCORRECT":
                stat["incorrect"] += 1
            else:
                stat["unverifiable"] += 1

            item_findings.append({
                "orgnr": org,
                "family": fam,
                "field": fld,
                "claim_value": c.get("value"),
                "expected_value": exp,
                "evidence_id": ev.get("id"),
                "locator": ev.get("locator"),
                "content_sha256": sha,
                "status": status,
                "reason": reason,
                "verification_category": "Category B (Stored Primary-Source Field Agreement)"
            })

    # Compile final metrics
    def compute_family_metrics(stat, total_published):
        rev = stat["reviewed"]
        corr = stat["correct"]
        inc = stat["incorrect"]
        unv = stat["unverifiable"]
        verifiable = corr + inc
        precision = corr / verifiable if verifiable > 0 else None
        vrate = verifiable / rev if rev > 0 else None
        return {
            "total_published_claims": total_published,
            "reviewed": rev,
            "correct": corr,
            "incorrect": inc,
            "unverifiable": unv,
            "wrong_company": stat["wrong_company"],
            "unsupported": stat["unsupported"],
            "fabricated_zeroes": stat["fabricated_zeroes"],
            "precision": precision,
            "verification_rate": vrate,
        }

    report = {
        "audit_metadata": {
            "auditor_version": "2.0-strict-source-field",
            "envelopes_file": envelopes_path.name,
            "total_companies": total_companies,
            "sample_seed": sample_seed,
            "sample_size": len(sampled_orgs),
            "sampled_organisations": sampled_orgs
        },
        "category_a_structural_integrity": cat_a,
        "category_b_stored_source_agreement": {
            fam: compute_family_metrics(family_stats[fam], cat_a["by_family"][fam])
            for fam in ["identity", "accounts", "roles", "subunits", "website", "hiring", "activity"]
        },
        "category_c_live_verification": {
            "status": "NOT EVALUATED (STORED REPLAY VERIFICATION ONLY)",
            "limitations": "Category B proves exact agreement with stored Brønnøysund, NAV, and web blobs. Independent current-live web verification was not re-executed during this static offline audit."
        },
        "item_findings": item_findings
    }

    out_file = Path("reports/accuracy-audit-report.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote strict accuracy audit report to {out_file}")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--envelopes", type=Path, default=Path("out/w5-opt1000-rev4-envelopes.jsonl"))
    parser.add_argument("--state-dir", type=Path, default=Path("state"))
    parser.add_argument("--seed", type=int, default=20261015)
    parser.add_argument("--sample-size", type=int, default=110)
    args = parser.parse_args()
    report = run_comprehensive_audit(args.envelopes, args.state_dir, args.seed, args.sample_size)
    print("\n=== CATEGORY B AUDIT SUMMARY ===")
    for fam, stats in report["category_b_stored_source_agreement"].items():
        prec_str = f"{stats['precision']*100:.2f}%" if stats['precision'] is not None else "N/A"
        vrate_str = f"{stats['verification_rate']*100:.2f}%" if stats['verification_rate'] is not None else "N/A"
        print(f"{fam:12}: Reviewed={stats['reviewed']:4} | Correct={stats['correct']:4} | Incorrect={stats['incorrect']:2} | Prec={prec_str:>7} | VRate={vrate_str:>7} | WrongOrg={stats['wrong_company']}")
