import gzip
import json

import pytest

from scripts.verify_publisher_identity import verify
from signalpost.web import seed_index
from signalpost.web.candidates import Candidate, generate
from signalpost.web.collector import candidate_proof
from signalpost.web.html import Page


def test_bundle_nominates_after_registry_contacts_with_existing_limit(tmp_path, monkeypatch):
    monkeypatch.setattr(seed_index, "DIRECTORY", tmp_path)
    seed_index.load.cache_clear()
    try:
        payload = {"version": 1, "source": "commoncrawl", "entries": {
            "991853995": [["seed.no"], ["declared.no"], ["proff.no"]],
        }}
        (tmp_path / "commoncrawl.json.gz").write_bytes(gzip.compress(json.dumps(payload).encode()))
        seeds = seed_index.load()["991853995"]
        nominees = generate({
            "name": "Testing Company AS",
            "website": "declared.no",
            "subunits": [{"orgnr": "912766349", "website": "unit.no"}],
            "website_seeds": seeds,
        }, limit=3)
        assert [(candidate.domain, candidate.origin) for candidate in nominees] == [
            ("declared.no", "registry_website"),
            ("unit.no", "subunit_registry_website"),
            ("seed.no", "seed_commoncrawl"),
        ]
    finally:
        seed_index.load.cache_clear()


def test_seed_promotion_requires_live_own_number_and_respects_conflicts():
    org = "991853995"
    url = "https://seed.no/"
    seed = Candidate(url, "seed.no", "seed_openstreetmap")
    description = "Testing Company provides scheduling services throughout the region. " * 6

    def evaluate(content, publisher):
        body = f"<title>Testing Company AS</title><main>{description}{content}</main><footer>{publisher}</footer>"
        return candidate_proof(Page(body.encode(), url), org, {"name": "Testing Company AS"}, seed, [])

    assert evaluate("", "Org.nr 991 853 995").level == "VERIFIED"
    assert evaluate("Client Org.nr 991 853 995", "Testing Company AS").level == "LOW"
    assert evaluate("Org.nr 991 853 995", "Org.nr 912 766 349").level == "REJECT"
    assert evaluate("", "Under construction. Org.nr 991 853 995").level == "REJECT"


def test_seed_website_receipt_replays_exact_publisher_proof():
    org = "991853995"
    url = "https://seed.no/kontakt"
    claim = {
        "field": "official_website", "availability": "available", "evidence_ids": ["proof"],
        "value": {
            "proof_type": "orgnr_on_page", "candidate_origin": "seed_commoncrawl",
            "identity_level": "VERIFIED", "proof_page_url": url, "final_url": "https://seed.no",
        },
    }
    evidence = {"proof": {
        "source_class": "company_owned", "source_url": url,
        "locator": f"identity-proof:{org}", "content_sha256": "body",
    }}
    description = "Testing Company provides scheduling services throughout the region. " * 6
    body = f"<main>{description}</main><footer>Org.nr {org}</footer>"
    assert verify(org, {"claims": [claim]}, evidence, lambda _: body) == 1
    third_party = f"<main>{description}</main><article>Client Org.nr {org}</article>"
    with pytest.raises(AssertionError, match="lacks live exact publisher evidence"):
        verify(org, {"claims": [claim]}, evidence, lambda _: third_party)
