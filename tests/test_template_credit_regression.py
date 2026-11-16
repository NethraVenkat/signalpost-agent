"""Regression: a leftover website-template credit is neither a veto nor an owner.

Mirrors the reviewed MELDAL MILJOANLEGG AS case (R7 seed 20261116): the company's
own footer shows its exact organisation number next to a stock Wix template line
"(c) 2035 by Happy Farm Sanctuary". Offline synthetic fixture; no network and no
production logic change.
"""
import json

import pytest

from signalpost.web.candidates import Candidate
from signalpost.web.collector import candidate_proof
from signalpost.web.html import Page
from signalpost.web.publisher_veto import conflict
from signalpost.web.reach_identity import different_named_publisher, eligible

ORG = "923609016"
CONTEXT = {"name": "Example Miljoanlegg AS"}
CREDIT = "Happy Farm Sanctuary"
BODY = ("<main><h1>Example Miljoanlegg</h1>"
        + "<p>Vi tar imot avfall, leverer pukk og grus og driver miljoanlegg for privat og naering. </p>" * 6
        + "</main>")

SAME_FOOTER_BLOCK = (
    "<footer><p>Example Miljoanlegg AS, Industriveien 1, 7336 Meldal</p>"
    "<p>post@example-miljoanlegg.no / tlf: 926 47 341</p>"
    "<p>Orgnummer: 923 609 016 Apningstider: Mandag - fredag kl. 07.30 - 15.00 "
    "Folg oss her: © 2035 by Happy Farm Sanctuary. Powered and secured by Wix</p></footer>")
SEPARATE_COPYRIGHT = (
    "<footer><p>Example Miljoanlegg AS. Orgnummer: 923 609 016</p>"
    '<div class="copyright">© 2024 by Happy Farm Sanctuary</div></footer>')


def page(footer):
    html = ("<html><head><title>Hjem | Example Miljoanlegg</title></head><body>"
            + BODY + footer + "</body></html>")
    return Page(html.encode("utf-8"), "https://www.example-miljoanlegg.no/")


@pytest.mark.parametrize("footer", [SAME_FOOTER_BLOCK, SEPARATE_COPYRIGHT], ids=["wix-footer-block", "copyright-element"])
def test_exact_orgnr_proof_survives_leftover_template_credit(footer):
    p = page(footer)
    proof = candidate_proof(p, ORG, CONTEXT, Candidate(p.url, "example-miljoanlegg.no", "legal_name_slug"), [])
    # (1) The template credit must not veto the exact-number proof.
    assert proof.level == "VERIFIED", (proof.level, proof.reason)
    assert proof.proof_type == "orgnr_on_page"
    assert proof.other_orgnrs == []
    assert not proof.reason.startswith("publisher_")
    # (2) The credit name never becomes the owner/publisher in the receipt.
    assert CREDIT.casefold() not in json.dumps(proof.publisher_receipt, ensure_ascii=False).casefold()


@pytest.mark.parametrize("footer", [SAME_FOOTER_BLOCK, SEPARATE_COPYRIGHT], ids=["wix-footer-block", "copyright-element"])
def test_template_credit_is_not_treated_as_a_different_owner(footer):
    p = page(footer)
    # (2) No conflict rule (foreign orgnr / legal form / placeholder / group /
    # service provider) fires on the credit, and the shared R7 own-publisher
    # guard does not read "Happy Farm Sanctuary" as a different named publisher.
    assert conflict(p, ORG, CONTEXT) == (None, [])
    assert different_named_publisher(p, CONTEXT) is False
    assert eligible(p, ORG, CONTEXT)
