"""
Strict Factual Accuracy, Provenance, and Source-Field Audit for Signalpost.

Audits three separate categories:
  Category A: Structural integrity (hashes, spans, locators, attribution, schemas)
  Category B: Stored primary-source data agreement (evaluates field-level values against source bodies)
  Category C: Independent / current live factual verification (only where explicitly executed)

Never conflates Category A structural integrity with Category B or C factual truth.
"""
import argparse
from decimal import Decimal, InvalidOperation
import hashlib
import html
import io
import json
import random
import re
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path
from html.parser import HTMLParser
from signalpost.sources.text import decode_body
from urllib.parse import urlparse

from signalpost.web.html import Page, json_values
from signalpost.web.candidates import legal_name
from signalpost.web.proof import phone, orgnrs, is_dedicated_entity_card, extract_entity_cards, find_containing_card

# Known directory and aggregator domains that cannot serve as company official websites
DIRECTORY_DOMAINS = {
    "proff.no", "180.no", "gulesider.no", "purehelp.no", "allabolag.se",
    "enhetsregisteret.no", "brreg.no", "facebook.com", "linkedin.com",
    "instagram.com", "twitter.com", "x.com", "wikipedia.org", "youtube.com"
}

# Generic platform landing paths that do not constitute verified company profiles
GENERIC_SOCIAL_PATHS = {
    "", "/", "/share", "/sharer", "/sharer.php", "/intent/tweet", "/home",
    "/pages", "/share.php", "/login", "/signup", "/feed", "/rss"
}

IDENTITY_CSV_FIELD_COLUMNS = {
    "identity.legal_name": ["navn"],
    "identity.registered_website": ["hjemmeside"],
    "identity.municipality": ["forretningsadresse.kommune", "kommune", "postadresse.kommune"],
    "identity.employees": ["antallAnsatte"],
    "identity.bankrupt": ["konkurs"],
    "identity.organisation_type": ["organisasjonsform.kode", "organisasjonsform"],
    "identity.registration_date": ["registreringsdatoEnhetsregisteret"],
    "identity.nace": ["naeringskode1.kode", "naeringskode1"],
    "identity.institution_sector_code": ["institusjonellSektorkode.kode", "institusjonellSektorkode"],
    "identity.mva_registered": ["registrertIMvaregisteret"],
}

IDENTITY_JSON_FIELD_POINTER_ENDS = {
    "identity.legal_name": ["/navn"],
    "identity.registered_website": ["/hjemmeside"],
    "identity.municipality": ["/kommune"],
    "identity.employees": ["/antallAnsatte"],
    "identity.bankrupt": ["/konkurs"],
    "identity.organisation_type": ["/kode", "/organisasjonsform"],
    "identity.registration_date": ["/registreringsdatoEnhetsregisteret"],
    "identity.nace": ["/kode", "/naeringskode1"],
    "identity.institution_sector_code": ["/kode", "/institusjonellSektorkode"],
    "identity.mva_registered": ["/registrertIMvaregisteret"],
}

ACCOUNTS_FIELD_LOCATOR_RULES = {
    "accounts.revenue": ["driftsinntekter", "sumDriftsinntekter", "salgsinntekt", "inntekter"],
    "accounts.operating_profit": ["driftsresultat", "sumDriftsresultat"],
    "accounts.annual_result": ["aarsresultat", "ordinaertResultatFoerSkattekostnad", "totalresultat"],
    "accounts.net_result": ["aarsresultat", "aarsresultatEtterSkattekostnad", "totalresultat"],
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
    Category A: Verifies cryptographic hash, locator, and non-empty verbatim excerpt
    for EVERY evidence reference in claim.evidence_ids.
    Returns (status, reason, primary_evidence).
    """
    avail = claim.get("availability")
    if avail != "available":
        return "PASS", "Claim marked unavailable or not applicable", None

    eids = claim.get("evidence_ids", [])
    if not eids:
        return "FAIL", "[ERR_NO_EVIDENCE] Missing evidence references for available claim", None

    first_ev = None
    for idx, eid in enumerate(eids):
        ev = evidence_map.get(eid)
        if not ev:
            return "FAIL", f"[ERR_MISSING_EVIDENCE_ID] Referenced evidence ID {eid} not found in envelope", None

        if first_ev is None:
            first_ev = ev

        loc = ev.get("locator")
        if not loc:
            return "FAIL", f"[ERR_MISSING_LOCATOR] Evidence locator missing for {eid}", ev

        sha = ev.get("content_sha256")
        if not sha:
            return "FAIL", f"[ERR_MISSING_HASH] Evidence content_sha256 missing for {eid}", ev

        span = ev.get("claim_span", "")
        if not span or not span.strip():
            return "FAIL", f"[ERR_EMPTY_SPAN] Empty or whitespace evidence span for {eid}", ev
        if len(span) > 300:
            return "FAIL", f"[ERR_SPAN_TOO_LONG] Evidence span exceeds 300 character limit ({len(span)} chars) for {eid}", ev

        blob_res = blob_getter(sha)
        if blob_res is None:
            return "FAIL", f"[ERR_MISSING_BLOB] Evidence blob {sha} missing from state storage for {eid}", ev
        if blob_res is False:
            return "FAIL", f"[ERR_CORRUPTED_BLOB] Evidence blob {sha} failed SHA-256 integrity verification for {eid}", ev

        body_str = blob_res
        if span not in body_str:
            return "FAIL", f"[ERR_SPAN_NOT_VERBATIM] Evidence span not found verbatim in content blob {sha} for {eid}", ev

    return "PASS", f"Valid cryptographic hash, locator, and verbatim span across {len(eids)} evidence references", first_ev


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
        if not body_org:
            return "UNVERIFIABLE", "Missing organisation number in source JSON", None
        if body_org != org:
            return "INCORRECT", f"Source body orgnr {body_org} != subject org {org}", body_org

        # Verify locator targets expected path for field
        for key, allowed_ends in IDENTITY_JSON_FIELD_POINTER_ENDS.items():
            if fld == key or fld.startswith(key + "."):
                if not any(loc.endswith(end) or end in loc for end in allowed_ends):
                    return "INCORRECT", f"Locator {loc} does not target expected path for {fld}", None

        found, expected = resolve_json_pointer(data, loc)
        if not found:
            return "INCORRECT", f"Locator {loc} not found in source JSON", None

        # Typed comparisons
        if fld == "identity.legal_name":
            if str(val or "").strip() == str(expected or "").strip():
                return "CORRECT", "Legal name matches source field exactly", expected
            return "INCORRECT", f"Legal name mismatch: claimed '{val}' != source '{expected}'", expected

        if fld == "identity.registered_website":
            exp_w = str(expected or "").strip().lower()
            claim_w = str(val or "").strip().lower()
            if claim_w == exp_w and exp_w != "":
                return "CORRECT", "Registered website matches source field exactly", expected
            return "INCORRECT", f"Claim registered website '{val}' != source '{expected}'", expected

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
            if str(code or "").strip() == str(exp_code or "").strip():
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
        return "UNVERIFIABLE", f"Subject organisation {org} not found in CSV snapshot", None

    # Verify subject org in row
    row_org = str(matched_row.get("organisasjonsnummer") or matched_row.get("Organisasjonsnummer") or "").strip()
    if not row_org:
        return "UNVERIFIABLE", "CSV row lacks organisation number", None
    if row_org != org:
        return "INCORRECT", f"CSV row orgnr {row_org} != subject org {org}", row_org

    if "/columns:" in loc:
        prefix = loc.split("/columns:")[-1].rstrip(".*")
        expected_dict = {}
        for k, v in matched_row.items():
            if k and k.lower().startswith(prefix.lower() + ".") and v not in (None, ""):
                expected_dict[k.split(".", 1)[-1]] = v
        if isinstance(val, dict) and val and all(expected_dict.get(k) == v for k, v in val.items()):
            return "CORRECT", f"Composite fields match CSV columns for {prefix}", expected_dict
        if val == expected_dict:
            return "CORRECT", f"Composite fields match CSV columns for {prefix}", expected_dict
        return "INCORRECT", f"Composite mismatch for {fld}: claimed {val} != CSV {expected_dict}", expected_dict

    col_name = loc.split("/column:")[-1] if "/column:" in loc else loc.split("/")[-1]
    actual_col = next((k for k in matched_row.keys() if k and k.lower() == col_name.lower()), None)
    if not actual_col:
        return "INCORRECT", f"Column '{col_name}' not found in CSV row", None

    # Verify locator column belongs to claimed field
    for key, cols in IDENTITY_CSV_FIELD_COLUMNS.items():
        if fld == key or fld.startswith(key + "."):
            if not any(col.lower() == col_name.lower() for col in cols):
                return "INCORRECT", f"Column '{col_name}' does not match expected columns {cols} for {fld}", col_name

    expected = matched_row.get(actual_col)

    if fld == "identity.legal_name":
        if str(val or "").strip().casefold() == str(expected or "").strip().casefold():
            return "CORRECT", "Legal name matches CSV column exactly", expected
        return "INCORRECT", f"Claim legal name '{val}' != CSV '{expected}'", expected

    if fld == "identity.registered_website":
        exp_web = str(expected or "").strip().lower()
        claim_web = str(val or "").strip().lower()
        if claim_web == exp_web and exp_web != "":
            return "CORRECT", f"Registered website '{claim_web}' matches CSV", expected
        return "INCORRECT", f"Claim registered website '{val}' != CSV '{expected}'", expected

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

    if isinstance(val, bool) or fld == "identity.bankrupt" or (expected and str(expected).lower() in ("true", "false", "ja", "nei")):
        exp_bool = str(expected).strip().lower() in ("ja", "true", "1", "yes")
        if bool(val) == exp_bool:
            return "CORRECT", f"Boolean field {fld} matches CSV", exp_bool
        return "INCORRECT", f"Claim {fld} {val} != CSV {exp_bool}", exp_bool

    if str(val or "").strip() == str(expected or "").strip():
        return "CORRECT", f"Field verified in CSV row ({actual_col})", expected
    return "INCORRECT", f"Field {fld} value mismatch: claim '{val}' != CSV '{expected}'", expected


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

    # Check locator path compatibility against field
    if fld in ACCOUNTS_FIELD_LOCATOR_RULES:
        allowed_parts = ACCOUNTS_FIELD_LOCATOR_RULES[fld]
        if not any(part.lower() in loc.lower() for part in allowed_parts):
            return "INCORRECT", f"Locator '{loc}' does not target expected path for financial field {fld}", None
    if fld == "accounts.revenue" and ("driftskostnad" in loc or "kostnad" in loc.lower()):
        return "INCORRECT", f"Revenue claim locator '{loc}' points to expenses rather than revenue", None

    found, raw_val = resolve_json_pointer(data, loc)
    if not found:
        return "INCORRECT", f"Financial locator {loc} does not exist in accounts body", None

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

    # Verify reporting period and boundaries
    period = record.get("regnskapsperiode") or {}
    exp_year = str(period.get("tilDato") or "")[:4]
    claim_year = str(rep.get("fiscal_year") or "")
    if exp_year and claim_year and exp_year != claim_year:
        return "INCORRECT", f"Fiscal year mismatch: claimed {claim_year} != filing {exp_year}", exp_year

    exp_start = str(period.get("fraDato") or "")
    claim_start = str(rep.get("start_date") or "")
    if exp_start and claim_start and exp_start != claim_start:
        return "INCORRECT", f"Reporting period start_date mismatch: claimed {claim_start} != filing {exp_start}", exp_start

    exp_end = str(period.get("tilDato") or "")
    claim_end = str(rep.get("end_date") or "")
    if exp_end and claim_end and exp_end != claim_end:
        return "INCORRECT", f"Reporting period end_date mismatch: claimed {claim_end} != filing {exp_end}", exp_end

    # Verify currency
    exp_curr = record.get("valuta") or "NOK"
    claim_curr = rep.get("currency")
    if claim_curr and claim_curr != exp_curr:
        return "INCORRECT", f"Currency mismatch: claimed {claim_curr} != filing {exp_curr}", exp_curr

    # Verify units
    claim_unit = rep.get("unit")
    if claim_unit and str(claim_unit).lower() not in ("whole", "nok", "1", "units", "standard"):
        return "INCORRECT", f"Unit mismatch: claimed unit '{claim_unit}' but Regnskapsregisteret filings are in whole units", "whole"

    # Check for fabricated zero
    if raw_val is None:
        if val == 0 or val == 0.0 or val == "0":
            return "INCORRECT", f"Fabricated zero: field {fld} is null/absent in filing but published as 0", 0
        if val is None:
            return "CORRECT", "Correctly published missing field as null", None
        return "INCORRECT", f"Field is null in filing but published as {val}", raw_val

    # Exact Decimal numeric and sign comparison
    try:
        dec_claim = Decimal(str(val))
        dec_expected = Decimal(str(raw_val))
        num_ret = float(dec_expected) if "." in str(dec_expected) else int(dec_expected)
        if (dec_claim < 0) != (dec_expected < 0) and dec_claim != 0 and dec_expected != 0:
            return "INCORRECT", f"Numeric sign mismatch: claimed {dec_claim} vs filing {dec_expected}", num_ret
        if dec_claim != dec_expected:
            return "INCORRECT", f"Numeric value mismatch: claimed {dec_claim} != filing {dec_expected}", num_ret
        return "CORRECT", f"Exact numeric match ({dec_claim} {exp_curr})", num_ret
    except (InvalidOperation, ValueError, TypeError):
        return "INCORRECT", f"Non-numeric comparison failure: claimed={val}, filing={raw_val}", raw_val


def audit_roles_claim(org: str, claim: dict, ev: dict, body: str) -> tuple[str, str, any]:
    """Category B: Compares role/person assignment to Brønnøysund roller payload."""
    fld = claim.get("field", "")
    val = claim.get("value")
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
    if not found:
        return "INCORRECT", f"Role locator {loc} not found in roller body", None

    item_clean = {k: v for k, v in item.items() if k != '_links'} if isinstance(item, dict) else item
    if fld.startswith("roles.detail."):
        if val == item_clean:
            return "CORRECT", f"Role detail matches source field ({fld})", item_clean
        return "INCORRECT", f"Role detail mismatch: claimed {val} != source {item_clean}", item_clean

    if not val or not isinstance(val, dict):
        return "INCORRECT", "Role claim value is empty or invalid", None

    if not isinstance(item, dict):
        return "INCORRECT", f"Role locator {loc} expected dict, got {type(item).__name__}", None

    val_dict = val
    person = item.get("person") or {}
    enhet = item.get("enhet") or {}
    role_type = item.get("type") or {}

    expected_name = ""
    if isinstance(person.get("navn"), dict):
        parts = [str(person["navn"].get(k)) for k in ("fornavn", "mellomnavn", "etternavn") if person["navn"].get(k)]
        expected_name = " ".join(parts)
    elif person.get("navn"):
        expected_name = " ".join(person["navn"]) if isinstance(person["navn"], list) else str(person["navn"])
    elif enhet.get("navn"):
        expected_name = " ".join(enhet["navn"]) if isinstance(enhet["navn"], list) else str(enhet["navn"])

    raw_claim_name = val_dict.get("name")
    claim_name = " ".join(raw_claim_name) if isinstance(raw_claim_name, list) else str(raw_claim_name or "")
    claim_type_code = (val_dict.get("role_type") or {}).get("kode") if isinstance(val_dict.get("role_type"), dict) else val_dict.get("role_type")
    exp_type_code = role_type.get("kode") if isinstance(role_type, dict) else role_type

    # Require non-empty claim value containing expected name and role code
    if not claim_name.strip() and expected_name.strip():
        return "INCORRECT", f"Role claim value missing person/entity name (source has '{expected_name}')", None
    if not claim_type_code and exp_type_code:
        return "INCORRECT", f"Role claim value missing role type code (source has '{exp_type_code}')", None

    if expected_name and claim_name:
        if expected_name.strip().casefold() != claim_name.strip().casefold():
            return "INCORRECT", f"Role person name mismatch: claimed '{claim_name}' != source '{expected_name}'", expected_name

    if exp_type_code and claim_type_code:
        if exp_type_code != claim_type_code:
            return "INCORRECT", f"Role type code mismatch: claimed '{claim_type_code}' != source '{exp_type_code}'", exp_type_code

    return "CORRECT", f"Verified role {exp_type_code} for {expected_name}", expected_name


def audit_subunits_claim(org: str, claim: dict, ev: dict, body: str) -> tuple[str, str, any]:
    """Category B: Compares subunit claim against Brønnøysund underenheter payload."""
    fld = claim.get("field", "")
    val = claim.get("value")
    loc = ev.get("locator", "")

    try:
        data = json.loads(body)
    except Exception as exc:
        return "UNVERIFIABLE", f"Malformed subunits JSON: {exc}", None

    found, item = resolve_json_pointer(data, loc)
    if not found:
        return "INCORRECT", f"Subunit locator {loc} not found in underenheter body", None

    item_clean = {k: v for k, v in item.items() if k != '_links'} if isinstance(item, dict) else item
    if fld.startswith("subunits.detail."):
        if val == item_clean:
            return "CORRECT", f"Subunit detail matches source field ({fld})", item_clean
        return "INCORRECT", f"Subunit detail mismatch: claimed {val} != source {item_clean}", item_clean

    if not val or not isinstance(val, dict):
        return "INCORRECT", "Subunit claim value is empty or invalid", None

    if not isinstance(item, dict):
        return "INCORRECT", f"Subunit locator {loc} expected dict, got {type(item).__name__}", None

    val_dict = val
    parent_org = str(item.get("overordnetEnhet") or "").strip()
    if not parent_org:
        return "INCORRECT", "Source subunit record lacks overordnetEnhet", None
    if parent_org != org:
        return "INCORRECT", f"Subunit parent orgnr {parent_org} != subject org {org}", parent_org

    unit_org = str(item.get("organisasjonsnummer") or "").strip()
    claimed_unit_org = str(val_dict.get("organisation_number") or "").strip()
    if not claimed_unit_org or unit_org != claimed_unit_org:
        return "INCORRECT", f"Subunit orgnr mismatch: claimed '{claimed_unit_org}' != source '{unit_org}'", unit_org

    unit_name = str(item.get("navn") or "").strip()
    claimed_name = str(val_dict.get("name") or "").strip()
    if not claimed_name or unit_name.casefold() != claimed_name.casefold():
        return "INCORRECT", f"Subunit name mismatch: claimed '{claimed_name}' != source '{unit_name}'", unit_name

    return "CORRECT", f"Subunit {unit_org} verified under parent {org}", unit_org


def extract_org_context_and_leaders(claims: list[dict]) -> tuple[dict, list[str]]:
    """Extracts identity context and leadership names from envelope claims for website evaluation."""
    name = next((c.get("value") for c in claims if c.get("field") == "identity.legal_name"), None)
    muni = next((c.get("value") for c in claims if c.get("field") == "identity.municipality"), None)
    reg_web = next((c.get("value") for c in claims if c.get("field") == "identity.registered_website"), None)
    addr_claim = next((c.get("value") for c in claims if c.get("field") == "identity.registered_address"), None) or {}
    street = addr_claim.get("adresse") if isinstance(addr_claim, dict) else None
    postcode = addr_claim.get("postnummer") if isinstance(addr_claim, dict) else None
    city = addr_claim.get("poststed") if isinstance(addr_claim, dict) else None
    phone_val = next((c.get("value") for c in claims if "phone" in c.get("field", "") or "telefon" in c.get("field", "")), None)
    context = {
        "name": name,
        "website": reg_web,
        "phone": phone_val,
        "municipality": muni,
        "street": street,
        "postcode": postcode,
        "city": city,
    }
    leaders = []
    for c in claims:
        if c.get("field", "").startswith("roles.role."):
            val_r = c.get("value")
            if isinstance(val_r, dict):
                type_code = (val_r.get("role_type") or {}).get("kode") if isinstance(val_r.get("role_type"), dict) else val_r.get("role_type")
                if type_code in ("LEDE", "LEDI", "STYR", "DAGL"):
                    raw_nm = val_r.get("name")
                    if isinstance(raw_nm, list):
                        leaders.extend(raw_nm)
                    elif isinstance(raw_nm, str):
                        leaders.append(raw_nm)
    return context, leaders


def audit_website_claim(
    org: str,
    claim: dict,
    ev: dict,
    body: str,
    registry_body: str | None = None,
    context: dict | None = None,
    leaders: list[str] | None = None,
) -> tuple[str, str, any]:
    """Category B: Independently validates website assignment proof against destination page."""
    fld = claim.get("field", "")
    val = claim.get("value") or {}
    if fld != "official_website":
        return "UNVERIFIABLE", f"Not an official website assignment field ({fld})", None

    ptype = val.get("proof_type")
    url = val.get("final_url") or val.get("url")
    origin = val.get("candidate_origin")
    signals = val.get("signals") or []
    identity_level = val.get("identity_level")

    if not body:
        return "UNVERIFIABLE", "Stored destination website body unavailable", None

    # 1. Reject known directory and social aggregator domains
    if url:
        cand_host = urlparse(url).netloc.lower().replace("www.", "")
        if cand_host in DIRECTORY_DOMAINS or any(cand_host.endswith("." + d) or cand_host == d for d in DIRECTORY_DOMAINS):
            return "INCORRECT", f"Directory/aggregator domain '{cand_host}' cannot serve as company official website", None

    page = Page(body.encode("utf-8", errors="replace"), val.get("proof_page_url") or url or "")
    orgnr_pat = re.compile(r'\b' + org[0:3] + r'[\s.]?' + org[3:6] + r'[\s.]?' + org[6:9] + r'\b')

    # Extract all organization numbers from page
    visible_orgnrs = orgnrs(page.visible)
    owner_orgnrs = orgnrs(page.owner_text)
    brand_orgnrs = orgnrs(" ".join(page.brand_parts))
    meta_orgnrs = orgnrs(" ".join(page.meta.values()))

    json_ids = set()
    for block in page.jsonld:
        for key in ("vatID", "taxID", "identifier"):
            for v in json_values(block, key, exclude_person=True):
                if isinstance(v, str):
                    normalized = re.sub(r"^\s*NO\s*|\s*MVA\s*$", " ", v, flags=re.I).strip()
                    json_ids |= orgnrs(normalized)
                elif isinstance(v, dict):
                    json_ids |= orgnrs(v.get("value", ""))

    all_structural_orgnrs = visible_orgnrs | owner_orgnrs | meta_orgnrs | json_ids

    # 2. Check for script-only occurrence
    if orgnr_pat.search(body) and org not in all_structural_orgnrs:
        return "INCORRECT", f"Orgnr {org} found only in script tags or invisible markup, not in company-identifying page context", None

    # 3. If another distinct company owns the footer/header brand context
    if brand_orgnrs and org not in brand_orgnrs and org not in json_ids:
        return "INCORRECT", f"Site footer/header brand ownership identifies foreign organisation {sorted(brand_orgnrs)}, not claimed {org}", None

    # 4. Check for customer/partner/client references
    if org in visible_orgnrs and org not in brand_orgnrs and org not in json_ids:
        visible_text = page.visible
        is_partner_mention = False
        for m in orgnr_pat.finditer(visible_text):
            start = max(0, m.start() - 250)
            context_window = visible_text[start:m.end() + 50].lower()
            if re.search(r"\b(?:kunder|våre\s+kunder|kundene|partnere|våre\s+partnere|partners|our\s+partners|referanser|kundereferanser|clients|our\s+clients|leverandører|portfolio)\b", context_window):
                is_partner_mention = True
                break
        if is_partner_mention:
            return "INCORRECT", f"Orgnr {org} appears only as partner/customer reference, not ownership proof", None

    # 5. Check for multi-entity group lists or directory tables
    if len(all_structural_orgnrs) >= 3 and (org not in brand_orgnrs and org not in json_ids):
        # A group page listing the company is valid only if labeled group_site
        # and corroborated by registry declaration and dedicated entity card.
        is_legitimate_group = False
        if val.get("relationship_note") == "group_site":
            domain = (urlparse(url).hostname or "").replace("www.", "").lower()
            reg_domain = ""
            if context and context.get("website"):
                reg_domain = (urlparse(context["website"] if "://" in str(context["website"]) else "https://" + str(context["website"])).hostname or "").replace("www.", "").lower()
            domain_corroborated = (origin == "registry_website") or (reg_domain and domain == reg_domain)
            if domain_corroborated:
                legal_nm = (context or {}).get("name", "")
                if is_dedicated_entity_card(page.raw, org, legal_nm):
                    is_legitimate_group = True
        if not is_legitimate_group:
            return "INCORRECT", f"Multi-entity list or directory table containing multiple organisation numbers ({len(all_structural_orgnrs)} found)", None

    if ptype in ("orgnr_on_page", "orgnr"):
        if org in all_structural_orgnrs:
            return "CORRECT", f"Exact orgnr {org} verified in company ownership context", url
        if orgnr_pat.search(body):
            return "INCORRECT", f"Proof type '{ptype}' asserted but orgnr {org} not found in structural ownership context", None
        return "INCORRECT", f"Proof type '{ptype}' asserted but orgnr {org} not found on page", None

    if ptype == "jsonld_vatid":
        if org in json_ids:
            return "CORRECT", f"Exact orgnr {org} verified in JSON-LD schema markup", url
        if org in all_structural_orgnrs:
            return "INCORRECT", f"JSON-LD vatId asserted but orgnr {org} only found in general page text, not JSON-LD schema", None
        return "INCORRECT", f"JSON-LD vatId asserted but orgnr {org} not found in body", None

    if ptype in ("registry_declared", "registry_declared_live"):
        if not registry_body and not (context and context.get("website")):
            return "UNVERIFIABLE", "Registry record unavailable to verify declared website domain", None
        domain = urlparse(url).hostname or ""
        domain_clean = domain.replace("www.", "").lower()
        reg_domain = ""
        if context and context.get("website"):
            reg_domain = (urlparse(context["website"] if "://" in str(context["website"]) else "https://" + str(context["website"])).hostname or "").replace("www.", "").lower()
        if (domain_clean and reg_domain and domain_clean == reg_domain) or (registry_body and domain_clean and domain_clean in registry_body.lower()):
            if ptype == "registry_declared_live":
                # Verify live corroborated signals
                branded = legal_name(page.title + " " + page.meta.get("og:site_name", "") + " " + " ".join(page.brand_parts))
                name = legal_name(context.get("name") if context else "")
                tokens = [t for t in name.split() if len(t) >= 4 and t.isalpha()] if name else []
                token_match = any(re.search(r"(?<!\w)" + re.escape(t) + r"(?!\w)", branded) for t in tokens)
                if not token_match and not (org in all_structural_orgnrs):
                    return "INCORRECT", "Registry declared live proof missing live name corroboration on page", None
            return "CORRECT", f"Domain {domain} verified in official Enhetsregisteret declaration", url
        return "INCORRECT", f"Registry-declared website asserted, but domain {domain} not found in registry body", None

    if ptype == "signals":
        if not signals:
            return "INCORRECT", "Signals proof claimed but signals list is empty", None

        # Check documented acceptance threshold
        if identity_level and identity_level in ("LOW", "MEDIUM"):
            return "INCORRECT", f"Signals identity level '{identity_level}' is below documented acceptance threshold (HIGH/REGISTRY_DECLARED)", None

        valid_signal_types = {"legal_name", "address", "phone", "leader", "municipality", "registry_website", "distinctive_legal_name"}
        unsupported_types = [s for s in signals if s not in valid_signal_types]
        if unsupported_types:
            return "INCORRECT", f"Signals ({', '.join(unsupported_types)}) not found in page body or unsupported signal types", None

        ctx = context or {}
        cand_domain = (urlparse(url).hostname or "").replace("www.", "").lower()
        text = legal_name(page.title + " " + page.meta.get("og:site_name", "") + " " + page.owner_text)
        norm_name = legal_name(ctx.get("name"))
        verified_signals = []
        pts = 0

        for s in signals:
            if s == "legal_name":
                if norm_name and re.search(r"(?<!\w)" + re.escape(norm_name) + r"(?!\w)", text):
                    verified_signals.append(s)
                    pts += 2
            elif s == "address":
                st = ctx.get("street")
                sts = st if isinstance(st, list) else [st]
                addr = any(x and len(str(x)) > 4 and legal_name(x) in text for x in sts)
                if not addr and ctx.get("postcode") and ctx.get("city"):
                    addr = str(ctx["postcode"]) in page.visible and legal_name(ctx["city"]) in text
                if addr:
                    verified_signals.append(s)
                    pts += 2
            elif s == "phone":
                exp_p = phone(ctx.get("phone"))
                page_p = {phone(l.href[4:]) for l in page.links if l.href.startswith("tel:")}
                for m in re.finditer(r"(?:\+47|0047)[ .()0-9-]{8,20}", page.visible):
                    page_p.add(phone(m.group()))
                if exp_p and exp_p in page_p:
                    verified_signals.append(s)
                    pts += 2
            elif s == "leader":
                if leaders and any(legal_name(l) and legal_name(l) in text for l in leaders):
                    verified_signals.append(s)
                    pts += 2
            elif s == "municipality":
                muni = legal_name(ctx.get("municipality"))
                if muni and muni in text:
                    verified_signals.append(s)
                    pts += 1
            elif s == "registry_website":
                reg_w = ctx.get("website") or ""
                reg_domain = (urlparse(reg_w if "://" in str(reg_w) else "https://" + str(reg_w)).hostname or "").replace("www.", "").lower() if reg_w else ""
                if cand_domain and reg_domain and cand_domain == reg_domain:
                    verified_signals.append(s)
                    pts += 2
                elif registry_body and cand_domain and cand_domain in registry_body.lower():
                    verified_signals.append(s)
                    pts += 2

        if len(verified_signals) != len(signals):
            missing = set(signals) - set(verified_signals)
            return "INCORRECT", f"Signals ({', '.join(missing)}) not verified against primary source facts", None

        # Recomputed points from verified primary source facts - strictly require pts >= 5
        if pts < 5:
            return "INCORRECT", f"Signals proof below acceptance threshold: recomputed points={pts} (< 5)", None
        if "legal_name" not in verified_signals:
            return "INCORRECT", "Signals proof missing required legal_name signal", None
        if not (set(verified_signals) & {"address", "phone", "leader", "registry_website"}):
            return "INCORRECT", "Signals proof missing required anchor signal (address/phone/leader/registry_website)", None
        if len(verified_signals) < 2:
            return "INCORRECT", "Signals proof requires at least 2 distinct verified signals", None

        return "CORRECT", f"Identity signals ({', '.join(signals)}) verified against primary source facts and destination page (recomputed points={pts})", url

    return "UNVERIFIABLE", f"Unknown website proof type: {ptype}", None


class DescriptionParser(HTMLParser):
    """Independent full paragraph/meta extraction; no proof-label trust."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.paragraph = None
        self.texts = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {'script', 'style', 'template'}:
            self.hidden += 1
        if tag == 'p' and not self.hidden:
            self.paragraph = []
        if tag == 'meta' and attrs.get('name', attrs.get('property')) in {'description', 'og:description'}:
            self.texts.append(attrs.get('content', ''))

    def handle_endtag(self, tag):
        if tag == 'p' and self.paragraph is not None:
            self.texts.append(''.join(self.paragraph))
            self.paragraph = None
        if tag in {'script', 'style', 'template'}:
            self.hidden = max(0, self.hidden - 1)

    def handle_data(self, data):
        if self.paragraph is not None and not self.hidden:
            self.paragraph.append(data)


def audit_website_metadata_claim(
    org: str, claim: dict, ev: dict, body: str, website_claim: dict = None, context: dict = None
) -> tuple[str, str, any]:
    """Category B: Validates contact/metadata claim value against verified company page body."""
    if not body:
        return "UNVERIFIABLE", "Stored page body unavailable", None

    fld = claim.get("field", "")
    val = claim.get("value")
    if val is None or val == "":
        return "INCORRECT", f"Empty metadata claim value for {fld}", None

    val_text = val.get("text", val) if isinstance(val, dict) else val
    val_str = str(val_text).strip()
    norm_val = html.unescape(html.unescape(val_str)).lower()
    norm_body = html.unescape(html.unescape(body)).lower()

    web_val = website_claim.get("value", {}) if isinstance(website_claim, dict) else {}
    is_group = (web_val.get("relationship_note") == "group_site") or bool(web_val.get("other_orgnrs"))
    other_orgnrs = set(web_val.get("other_orgnrs", []))

    if fld.startswith("contact.email"):
        if norm_val not in norm_body and val_str.lower() not in body.lower():
            return "INCORRECT", f"Contact '{val_str}' not found in page body", None

        if is_group:
            cards = extract_entity_cards(body)
            m = re.search(re.escape(val_str), body, re.IGNORECASE)
            if not m:
                return "INCORRECT", f"Contact '{val_str}' not found in page body", None
            pos = m.start()
            c = find_containing_card(cards, pos)
            if c:
                if c.is_sibling(org, other_orgnrs):
                    return "INCORRECT", f"Contact '{val_str}' belongs to sibling entity in dedicated card, not subject {org}", None
                if c.matches_org(org, context):
                    return "CORRECT", f"Contact '{val_str}' verified in entity card for {org}", val_str
                return "INCORRECT", f"Contact '{val_str}' belongs to sibling entity in dedicated card, not subject {org}", None
            else:
                return "INCORRECT", f"Contact '{val_str}' on group site lacks entity-specific attribution linking to subject {org}", None

        return "CORRECT", f"Contact email '{val_str}' verified in page body", val_str

    if fld.startswith("contact.phone"):
        norm_phone = phone(val_str)
        phone_matches = []
        for m in re.finditer(r"(?:\+47|0047|\b)[ .()0-9-]{8,20}\b", body):
            p = phone(m.group())
            if p:
                phone_matches.append((p, m.start()))
        for m in re.finditer(r'href=[\'"]tel:([^\'"]+)[\'"]', body, re.I):
            p = phone(m.group(1))
            if p:
                phone_matches.append((p, m.start()))
        page_phones = {p for p, _ in phone_matches}

        matched_pos = None
        if norm_phone and norm_phone in page_phones:
            matched_pos = next((pos for p, pos in phone_matches if p == norm_phone), None)
        elif norm_val in norm_body or val_str in body:
            matched_pos = body.find(val_str) if val_str in body else None
        else:
            return "INCORRECT", f"Contact phone '{val_str}' not found in page body", None

        if is_group:
            cards = extract_entity_cards(body)
            if matched_pos is not None:
                c = find_containing_card(cards, matched_pos)
                if c:
                    if c.is_sibling(org, other_orgnrs):
                        return "INCORRECT", f"Contact phone '{val_str}' belongs to sibling entity in dedicated card, not subject {org}", None
                    if c.matches_org(org, context):
                        return "CORRECT", f"Contact phone '{val_str}' verified in entity card for {org}", val_str
                    return "INCORRECT", f"Contact phone '{val_str}' belongs to sibling entity in dedicated card, not subject {org}", None
                else:
                    return "INCORRECT", f"Contact phone '{val_str}' on group site lacks entity-specific attribution linking to subject {org}", None

        return "CORRECT", f"Contact phone '{val_str}' verified in page body", val_str

    if fld.startswith("company_scale.") or "customer_count" in fld:
        if is_group:
            return "INCORRECT", f"Group-wide metrics cannot be published as subsidiary statistics: {val_str}", None

    if fld == "public_brand":
        if norm_val in norm_body or val_str.lower() in body.lower():
            return "CORRECT", f"Public brand '{val_str}' verified in page body", val_str
        return "INCORRECT", f"Public brand '{val_str}' not found in page body", None

    if fld.startswith("website_description"):
        is_summary = (
            (isinstance(val, dict) and (val.get("kind") == "summary" or val.get("summary_kind") == "summary"))
            or fld.endswith(".summary")
        )
        if is_summary:
            citations = val.get("citations") if isinstance(val, dict) else None
            sentence_cites = val.get("sentences") if isinstance(val, dict) else None
            if not citations and not sentence_cites:
                return "UNVERIFIABLE", "Summary description lacks sentence-level citations", None

        norm_val_compact = re.sub(r"\s+", " ", norm_val).strip()
        norm_body_compact = re.sub(r"\s+", " ", norm_body).strip()

        parsed = DescriptionParser()
        parsed.feed(body)
        # Only markup/entity decoding and the production 300-character cap.
        # Matching a few words does not establish sentence support.
        if any(re.sub(r'\s+', ' ', text.strip()[:300]).lower() == norm_val_compact
               for text in parsed.texts):
            return "CORRECT", "Complete description verified in parsed source text", val_str

        if norm_val in norm_body or val_str.lower() in body.lower() or norm_val_compact in norm_body_compact:
            return "CORRECT", "Website description verified in page body", val_str
        return "INCORRECT", "Website description not found in page body", None

    return "UNVERIFIABLE", f"No semantic validator for website metadata field {fld}", None


def audit_social_claim(
    org: str, claim: dict, ev: dict, body: str, website_claim: dict = None, context: dict = None
) -> tuple[str, str, any]:
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

    claimed_host = parsed.netloc.lower().replace("www.", "")
    claimed_path = path_part.lower()

    web_val = website_claim.get("value", {}) if isinstance(website_claim, dict) else {}
    is_group = (web_val.get("relationship_note") == "group_site") or bool(web_val.get("other_orgnrs"))
    other_orgnrs = set(web_val.get("other_orgnrs", []))

    if is_group:
        legal_nm = (context or {}).get("name", "").lower()
        if any(term in claimed_path for term in ("group", "holding", "gruppe")) and not any(term in legal_nm for term in ("group", "holding", "gruppe")):
            return "INCORRECT", f"Social URL '{s_url}' belongs to parent/group entity, not subsidiary {org}", s_url
        cards = extract_entity_cards(body)
        m = re.search(re.escape(s_url), body, re.IGNORECASE)
        if m:
            pos = m.start()
            c = find_containing_card(cards, pos)
            if c and c.is_sibling(org, other_orgnrs):
                return "INCORRECT", f"Social URL '{s_url}' belongs to sibling entity in dedicated card, not subject {org}", s_url

    hrefs = re.findall(r'href=[\'"]([^\'"]+)[\'"]', body, re.IGNORECASE)
    plain_urls = re.findall(r'https?://[^\s<>"\']+', body)
    all_links = set(hrefs + plain_urls)

    for link in all_links:
        try:
            cand = urlparse(link)
            cand_host = cand.netloc.lower().replace("www.", "")
            cand_path = cand.path.rstrip("/").lower()
            if cand_host and cand_host == claimed_host and cand_path == claimed_path:
                return "CORRECT", f"Verified company-owned social link ({platform}) in page body", s_url
        except Exception:
            continue

    if s_url in body:
        return "CORRECT", f"Verified company-owned social link ({platform}) in page body", s_url

    return "INCORRECT", f"Social profile URL {s_url} not found in verified company page body", None


def audit_activity_claim(org: str, claim: dict, ev: dict, body: str) -> tuple[str, str, any]:
    """Category B: Validates activity URL and date co-occurrence in same XML entry."""
    val = claim.get("value") or {}
    act_url = val.get("url") if isinstance(val, dict) else str(val)
    date_str = val.get("date") if isinstance(val, dict) else None
    date_kind = val.get("date_kind") if isinstance(val, dict) else None

    if not body:
        return "UNVERIFIABLE", "Activity XML feed body unavailable", None

    try:
        clean_xml = re.sub(r'<\?xml[^>]*\?>', '', body).strip()
        root = ET.fromstring(clean_xml)
    except Exception as exc:
        return "UNVERIFIABLE", f"XML parse failure: {exc}", None

    def norm_url(u: str) -> str:
        if not u:
            return ""
        u = u.strip().rstrip("/")
        parsed = urlparse(u)
        scheme = parsed.scheme.lower()
        netloc = parsed.netloc.lower().replace("www.", "")
        path = parsed.path.rstrip("/")
        return f"{scheme}://{netloc}{path}"

    target_norm = norm_url(act_url)

    # 1. Sitemap: <urlset><url><loc>...</loc><lastmod>...</lastmod></url></urlset>
    for url_node in root.findall('.//{*}url'):
        loc_node = url_node.find('{*}loc')
        if loc_node is not None and loc_node.text:
            if norm_url(loc_node.text) == target_norm:
                if date_kind in ("published", "publication"):
                    return "INCORRECT", f"Sitemap <lastmod> date cannot be claimed as publication date for {act_url}", None
                lastmod = url_node.find('{*}lastmod')
                if lastmod is not None and lastmod.text and date_str:
                    clean_lastmod = lastmod.text.strip()
                    if date_str == clean_lastmod or clean_lastmod.startswith(date_str) or date_str.startswith(clean_lastmod[:10]):
                        return "CORRECT", f"URL and lastmod date {date_str} co-occur in sitemap <url> entry", date_str
                    return "INCORRECT", f"Activity date {date_str} does not match XML entry date '{clean_lastmod}' for {act_url}", clean_lastmod
                elif lastmod is None:
                    return "INCORRECT", f"Activity item {act_url} lacks required <lastmod> date in sitemap", None

    # 2. RSS: <channel><item><link>...</link><pubDate>...</pubDate></item></channel>
    for item_node in root.findall('.//item'):
        link_node = item_node.find('link')
        if link_node is not None and link_node.text:
            if norm_url(link_node.text) == target_norm:
                pub_date = item_node.find('pubDate')
                if pub_date is not None and pub_date.text:
                    if date_str and (date_str in pub_date.text or str(pub_date.text)[:10] == date_str):
                        return "CORRECT", f"URL and pubDate {date_str} co-occur in RSS <item>", date_str
                    return "INCORRECT", f"RSS pubDate '{pub_date.text}' does not match claimed date '{date_str}'", pub_date.text
                return "INCORRECT", f"RSS item {act_url} lacks pubDate", None

    # 3. Atom: <feed><entry><link href="..."/><updated>...</updated></entry></feed>
    for entry_node in root.findall('.//{*}entry'):
        link_node = entry_node.find('{*}link')
        href = link_node.get('href') if link_node is not None else (link_node.text if link_node is not None else None)
        if href and norm_url(href) == target_norm:
            updated = entry_node.find('{*}updated') or entry_node.find('{*}published')
            if updated is not None and updated.text and date_str:
                clean_upd = updated.text.strip()
                if date_str in clean_upd or clean_upd.startswith(date_str) or date_str.startswith(clean_upd[:10]):
                    return "CORRECT", f"URL and date {date_str} co-occur in Atom <entry>", date_str
                return "INCORRECT", f"Atom date '{clean_upd}' does not match claimed date '{date_str}'", clean_upd

    return "INCORRECT", f"Activity URL {act_url} not found in any XML entry", None


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

    # Check ad UUID
    body_uuid = data.get("uuid") or ad.get("uuid")
    if uuid and body_uuid and str(uuid).lower() != str(body_uuid).lower():
        return "INCORRECT", f"Ad UUID mismatch: claimed {uuid} != payload {body_uuid}", body_uuid

    # Check title if provided
    claim_title = val.get("title")
    body_title = ad.get("title")
    if claim_title and body_title and str(claim_title).strip() != str(body_title).strip():
        return "INCORRECT", f"Ad title mismatch: claimed '{claim_title}' != payload '{body_title}'", body_title

    # Check status if provided
    claim_status = val.get("status")
    body_status = data.get("status") or ad.get("status")
    if claim_status and body_status and str(claim_status).upper() != str(body_status).upper():
        return "INCORRECT", f"Ad status mismatch: claimed '{claim_status}' != payload '{body_status}'", body_status

    # Exact parent employer
    if employer_orgnr == org:
        return "CORRECT", f"Employer orgnr {employer_orgnr} matches parent company exactly", employer_orgnr

    # Verified subunit employer
    if matched_via.startswith("subunit"):
        sub_org = matched_via.split()[-1]
        if employer_orgnr == sub_org:
            if subunit_map and org in subunit_map and sub_org in subunit_map[org]:
                return "CORRECT", f"Employer orgnr {employer_orgnr} matches verified subunit {sub_org} of parent {org}", employer_orgnr
            return "INCORRECT", f"Employer orgnr {employer_orgnr} claims subunit of {org}, but subunit is not verified under parent", employer_orgnr
        return "INCORRECT", f"Employer orgnr {employer_orgnr} != claimed subunit {sub_org}", employer_orgnr

    return "INCORRECT", f"Employer orgnr {employer_orgnr} != parent org {org} without verified subunit mapping", employer_orgnr


def run_comprehensive_audit(envelopes_path: Path, state_dir: Path, sample_seed: int = 20261015, min_sample: int = 110, output_path: Path | None = None):
    blobs_dir = state_dir / "blobs"
    if not blobs_dir.exists():
        raise FileNotFoundError(f"State blobs directory not found: {blobs_dir}")

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
            blob_cache[sha] = decode_body(b)
        return blob_cache[sha]

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
        "missing_attribution": 0,
        "by_family": Counter()
    }

    company_by_org = {}
    companies_with_web = []
    companies_with_jobs = []
    companies_with_act = []
    companies_with_loss = []
    companies_with_subunits = []
    companies_with_non_nok = []
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

            if fam == "website":
                has_web = True
                fld = c.get("field", "")
                if fld == "official_website":
                    cat_a["by_family"]["official_website"] += 1
                elif "social" in fld:
                    cat_a["by_family"]["social_profiles"] += 1
                else:
                    cat_a["by_family"]["other_website_claims"] += 1

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
            num_eids = len(c.get("evidence_ids", []))
            if status == "PASS":
                cat_a["hash_checks"] += num_eids
                cat_a["hash_passes"] += num_eids
                cat_a["span_checks"] += num_eids
                cat_a["span_passes"] += num_eids
                cat_a["locator_passes"] += num_eids
            else:
                if "ERR_MISSING_HASH" in reason or "ERR_CORRUPTED_BLOB" in reason:
                    cat_a["hash_checks"] += 1
                    cat_a["hash_failures"] += 1
                elif "ERR_MISSING_BLOB" in reason:
                    cat_a["missing_blobs"] += 1
                elif "SPAN" in reason:
                    cat_a["span_checks"] += 1
                    cat_a["span_failures"] += 1
                elif "LOCATOR" in reason:
                    cat_a["locator_failures"] += 1

        if has_web: companies_with_web.append(org)
        if has_jobs: companies_with_jobs.append(org)
        if has_act: companies_with_act.append(org)
        if has_sub: companies_with_subunits.append(org)

    cat_a["by_family"]["aggregate_all_families"] = cat_a["available_claims"]

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

    item_findings = []
    family_stats = defaultdict(lambda: {
        "reviewed": 0, "correct": 0, "incorrect": 0, "unverifiable": 0,
        "wrong_company": 0, "missing_attribution": 0, "unsupported": 0, "fabricated_zeroes": 0
    })

    for org in sampled_orgs:
        r = company_by_org[org]
        ev_map = {e["id"]: e for e in r.get("evidence", [])}
        org_context, org_leaders = extract_org_context_and_leaders(r.get("claims", []))
        org_website_claim = next((c for c in r.get("claims", []) if c.get("field") == "official_website"), None)

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
            fld = c.get("field", "")
            avail = c.get("availability")
            if avail != "available":
                continue

            if fam not in {"identity", "accounts", "roles", "subunits", "website", "hiring", "activity"}:
                continue

            target_fams = [fam]
            if fam == "website":
                if fld == "official_website":
                    target_fams.append("official_website")
                elif "social" in fld:
                    target_fams.append("social_profiles")
                else:
                    target_fams.append("other_website_claims")

            eids = c.get("evidence_ids", [])
            if not eids:
                for tf in target_fams + ["aggregate_all_families"]:
                    family_stats[tf]["reviewed"] += 1
                    family_stats[tf]["unsupported"] += 1
                    family_stats[tf]["incorrect"] += 1
                item_findings.append({
                    "orgnr": org, "family": fam, "field": fld, "status": "INCORRECT",
                    "reason": "Missing evidence references", "claim_value": c.get("value")
                })
                continue

            ev = ev_map.get(eids[0])
            if not ev:
                for tf in target_fams + ["aggregate_all_families"]:
                    family_stats[tf]["reviewed"] += 1
                    family_stats[tf]["unsupported"] += 1
                    family_stats[tf]["incorrect"] += 1
                item_findings.append({
                    "orgnr": org, "family": fam, "field": fld, "status": "INCORRECT",
                    "reason": f"Evidence {eids[0]} not found in envelope", "claim_value": c.get("value")
                })
                continue

            sha = ev.get("content_sha256")
            body = get_blob(sha)
            if not body:
                for tf in target_fams + ["aggregate_all_families"]:
                    family_stats[tf]["reviewed"] += 1
                    family_stats[tf]["unverifiable"] += 1
                item_findings.append({
                    "orgnr": org, "family": fam, "field": fld, "status": "UNVERIFIABLE",
                    "reason": f"Blob {sha} not found or corrupted", "claim_value": c.get("value")
                })
                continue

            if fam == "identity":
                status, reason, exp = audit_identity_claim(org, c, ev, body)
            elif fam == "accounts":
                status, reason, exp = audit_accounts_claim(org, c, ev, body)
                if "fabricated zero" in reason.lower():
                    for tf in target_fams + ["aggregate_all_families"]:
                        family_stats[tf]["fabricated_zeroes"] += 1
            elif fam == "roles":
                status, reason, exp = audit_roles_claim(org, c, ev, body)
            elif fam == "subunits":
                status, reason, exp = audit_subunits_claim(org, c, ev, body)
            elif fam == "website":
                if fld == "official_website":
                    status, reason, exp = audit_website_claim(
                        org, c, ev, body, reg_body, context=org_context, leaders=org_leaders
                    )
                elif "social" in fld:
                    status, reason, exp = audit_social_claim(
                        org, c, ev, body, website_claim=org_website_claim, context=org_context
                    )
                else:
                    status, reason, exp = audit_website_metadata_claim(
                        org, c, ev, body, website_claim=org_website_claim, context=org_context
                    )
            elif fam == "hiring":
                status, reason, exp = audit_hiring_claim(org, c, ev, body, subunit_parent_map)
            elif fam == "activity":
                status, reason, exp = audit_activity_claim(org, c, ev, body)
            else:
                status, reason, exp = "UNVERIFIABLE", f"No semantic checker for family {fam}", None

            for tf in target_fams + ["aggregate_all_families"]:
                st = family_stats[tf]
                st["reviewed"] += 1
                if status == "CORRECT":
                    st["correct"] += 1
                elif status == "INCORRECT":
                    st["incorrect"] += 1
                else:
                    st["unverifiable"] += 1
                if "wrong" in reason.lower() and "org" in reason.lower():
                    st["wrong_company"] += 1
                elif "lacks" in reason.lower() and "org" in reason.lower():
                    st["missing_attribution"] += 1

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
            "publication_denominator": total_published,
            "reviewed": rev,
            "correct": corr,
            "incorrect": inc,
            "unverifiable": unv,
            "wrong_company": stat["wrong_company"],
            "missing_attribution": stat["missing_attribution"],
            "unsupported": stat["unsupported"],
            "fabricated_zeroes": stat["fabricated_zeroes"],
            "precision": precision,
            "precision_denominator": verifiable,
            "verification_rate": vrate,
            "verification_rate_denominator": rev,
        }

    report = {
        "audit_metadata": {
            "auditor_version": "2.2-parsed-description-explicit-decoding",
            "envelopes_file": envelopes_path.name,
            "total_companies": total_companies,
            "sample_seed": sample_seed,
            "sample_size": len(sampled_orgs),
            "sampled_organisations": sampled_orgs
        },
        "category_a_structural_integrity": cat_a,
        "category_b_stored_source_agreement": {
            fam: compute_family_metrics(family_stats[fam], cat_a["by_family"][fam])
            for fam in [
                "identity",
                "accounts",
                "roles",
                "subunits",
                "official_website",
                "social_profiles",
                "other_website_claims",
                "website",
                "hiring",
                "activity",
                "aggregate_all_families",
            ]
        },
        "category_c_live_verification": {
            "status": "NOT EVALUATED (STORED REPLAY VERIFICATION ONLY)",
            "limitations": "Category B proves exact agreement with stored Brønnøysund, NAV, and web blobs. Independent current-live web verification was not re-executed during this static offline audit."
        },
        "item_findings": item_findings
    }

    out_file = output_path or Path("reports/accuracy-audit-report.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    print(f"Wrote strict accuracy audit report to {out_file}")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    default_env = Path("out/candidate-1000-corrected-envelopes.jsonl")
    if not default_env.exists():
        default_env = Path("out/w5-opt1000-rev4-envelopes.jsonl")
    parser.add_argument("--envelopes", type=Path, default=default_env)
    parser.add_argument("--state-dir", type=Path, default=Path("state"))
    parser.add_argument("--seed", type=int, default=20261015)
    parser.add_argument("--sample-size", type=int, default=110)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = run_comprehensive_audit(args.envelopes, args.state_dir, args.seed, args.sample_size, args.output)
    print("\n=== CATEGORY B AUDIT SUMMARY ===")
    for fam, stats in report["category_b_stored_source_agreement"].items():
        prec_str = f"{stats['precision']*100:.2f}%" if stats['precision'] is not None else "N/A"
        vrate_str = f"{stats['verification_rate']*100:.2f}%" if stats['verification_rate'] is not None else "N/A"
        pub = stats['total_published_claims']
        print(f"{fam:24}: Pub={pub:5} | Rev={stats['reviewed']:4} | Corr={stats['correct']:4} | Inc={stats['incorrect']:2} | Unv={stats['unverifiable']:2} | Prec={prec_str:>7} | VRate={vrate_str:>7} | WrongOrg={stats['wrong_company']}")
