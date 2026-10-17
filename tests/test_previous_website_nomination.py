import httpx
from signalpost.web import collector
from signalpost.web.candidates import Candidate
from tests.test_websites import execute_web, html, FILL, OTHER


def test_refresh_revalidates_known_proof_before_rediscovery_without_changing_ids(tmp_path, monkeypatch):
    monkeypatch.setattr(collector, 'generate', lambda context: [Candidate('https://brand.no', 'brand.no', 'legal_name_slug')])
    def source(request):
        if request.url.path == '/robots.txt':
            return httpx.Response(200, text='User-agent: *\nAllow: /')
        if request.url.path == '/kontakt':
            return httpx.Response(200, text=html())
        return httpx.Response(200, text='<main>' + FILL + '<a href="/kontakt">Kontakt</a></main>')
    _, first, _, cfg = execute_web(tmp_path / 'first', monkeypatch, website=None, response=source)
    old = next(c for c in first['claims'] if c['field'] == 'official_website')
    assert old['value']['proof_page_url'].endswith('/kontakt')
    monkeypatch.setattr(collector, 'generate', lambda context: [])
    def updated_home(request):
        if request.url.path == '/robots.txt':
            return httpx.Response(200, text='User-agent: *\nAllow: /')
        return httpx.Response(200, text=html())
    _, second, requests, _ = execute_web(tmp_path / 'second', monkeypatch, website=None,
                                         response=updated_home, previous=cfg.output)
    new = next(c for c in second['claims'] if c['field'] == 'official_website')
    assert new['id'] == old['id'] and new['value'] == old['value'] and not new['carried_forward']
    assert 'https://brand.no/kontakt' in requests
    def foreign(request):
        return httpx.Response(200, text='User-agent: *\nAllow: /' if request.url.path == '/robots.txt' else html('Org nr ' + OTHER))
    _, rejected, rejected_requests, _ = execute_web(tmp_path / 'foreign', monkeypatch, website=None,
                                     response=foreign, previous=cfg.output)
    assert not any(c['field'] == 'official_website' and not c['carried_forward'] for c in rejected['claims'])
    assert 'https://brand.no/kontakt' not in rejected_requests


def test_registry_change_or_removed_subunit_cannot_reuse_historical_scope():
    old = {'claims': [{'field': 'identity.registered_website', 'availability': 'available', 'value': 'https://old.no'},
                      {'field': 'official_website', 'availability': 'available', 'value': {
                          'final_url': 'https://branch.no', 'proof_page_url': 'https://branch.no/kontakt',
                          'identity_level': 'VERIFIED', 'candidate_origin': 'subunit_registry_email',
                          'matched_via_subunit': '933248380'}}]}
    assert collector.previous_nomination(old, {'website': 'https://new.no'}, {'933248380': {}}) == (None, None)
    assert collector.previous_nomination(old, {'website': 'https://old.no'}, {}) == (None, None)
