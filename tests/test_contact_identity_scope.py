"""Keep contact attribution tied to the website identity after descriptions."""
from types import SimpleNamespace
from signalpost.web import collector, descriptions
from signalpost.web.html import Page
from signalpost.web.proof import Proof
from signalpost.web.candidates import Candidate
from signalpost.sources.extract import Section


def test_description_append_preserves_identity_for_contacts(monkeypatch):
    org = '923609016'
    raw = ('<html><h1>Example</h1><p>Org.nr. 923609016</p>'+'<p>Example content.</p>'*30+'</html>').encode()
    page = Page(raw, 'https://example.no/')
    response = SimpleNamespace(url='https://example.no/', body=raw, retrieved_at='2026-10-15T10:00:00Z', sha='a'*64)
    # Capture the exact website claim passed to descriptions, then append a
    # different claim as the real description extractor does.
    captured = []
    def describe(section, org, claim, pages):
        captured.append(claim)
        section.claims.append(SimpleNamespace(value={'text':'Description'}))
    def contacts(section, org, claim, pages, **kwargs):
        assert claim is captured[0]
        assert claim.value['relationship_note']=='group_site'
    monkeypatch.setattr(descriptions, 'extract', describe)
    monkeypatch.setattr(collector, 'extract_contacts_and_social', contacts)
    monkeypatch.setattr(collector, 'extract_public_brand', lambda *args: None)
    proof = Proof('VERIFIED', 'orgnr_on_page', other_orgnrs=['988258229'], token=org)
    candidate = Candidate('https://example.no/', 'example.no', 'registry_website')
    http = SimpleNamespace(accepted_pages={}, attempts={})
    envelope = SimpleNamespace(claims=[], evidence=[], run=SimpleNamespace(refresh={}))
    collector.publish_result(org, envelope, http, Section(state='available'),
        [(candidate, proof, response, page, [(response,page)])], [], {'name':'Example AS'})
