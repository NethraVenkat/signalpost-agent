import copy
import hashlib
import json
from pathlib import Path

import httpx
import pytest

from scripts.verify_output import verify
from scripts.verify_owner_social import verify as verify_social
from signalpost.sources.text import decode_body
from signalpost.web import social_registry
from signalpost.web.html import Page
from signalpost.web.owner_social import SAME_AS, page_profiles, site_scope, visible_profiles
from signalpost.web.social import discover_strict
from tests import test_websites as web

FIXTURES = Path(__file__).parent / 'fixtures/social_hc1'
TROLLHEIM_FB = 'https://facebook.com/TrollheimAS'


def test_trollheim_saved_link_and_contact_share_a_registered_site():
    # Exact byte slices from P3g: homepage SHA 15f2a742f2d0baf7a6ba588677bd54709bdf264771c719f4519a33d081d92e4a
    # (offset 78325) and contact-page SHA 0c08bfb18994f5475cf65a36a9ef4883ac87d7e84385690c938d2bceaa9beaac (offset 65392).
    link = (FIXTURES / 'trollheim-facebook.body').read_bytes()
    contact = (FIXTURES / 'trollheim-kontakt.body').read_bytes()
    assert hashlib.sha256(link).hexdigest() == '0e2e308fbbe053a5e0fa7cceb0720bd4b6a36eabe773c1877300c9db453c0194'
    assert hashlib.sha256(contact).hexdigest() == '219cd43d89a3e72d1dc35ca9da8a719fb2de7c2ef20828c26d84c3e32d0810c9'
    org = '991323848'
    site = {'final_url': 'https://trollheim.no', 'identity_level': 'HIGH'}
    home = Page(b'<footer>' + link + b'</footer>', site['final_url'] + '/')
    contact_page = Page(contact, site['final_url'] + '/kontakt/')
    pages = [home, contact_page]
    assert TROLLHEIM_FB in discover_strict(home, 'TROLLHEIM AS')
    scope, source, _ = site_scope(site, pages, org, 'TROLLHEIM AS')
    assert scope == 'other_registered_entity_on_shared_domain' and source is contact_page
    assert not page_profiles(home, site, org, {'name': 'TROLLHEIM AS'}, visible_profiles(pages), True)


def test_registered_foreign_name_with_legal_form_in_rendered_page():
    site = {'final_url': 'https://example.no'}
    html = b'<p><strong>Trollheim Kurs og Kompetanse</strong> AS</p>'
    page = Page(html, site['final_url'])
    assert site_scope(site, [page], web.OUR, 'EXAMPLE AS')[0] == 'other_registered_name_on_page'
    assert site_scope(site, [page], '924191627', 'TROLLHEIM KURS OG KOMPETANSE AS')[0] is None
    assert site_scope(site, [Page(b'<p hidden>' + html + b'</p>', site['final_url'])],
                      web.OUR, 'EXAMPLE AS')[0] is None


@pytest.mark.parametrize('exact_link', [False, True])
def test_second_own_page_vetoes_social_without_changing_the_website(tmp_path, monkeypatch, exact_link):
    url = 'https://www.facebook.com/example'
    schema = ''
    if exact_link:
        schema = '<script type="application/ld+json">' + json.dumps({
            '@type': 'Organization', 'vatID': 'NO' + web.OUR + 'MVA', 'sameAs': url,
        }) + '</script>'
    homepage = web.html(
        'Org.nr ' + web.OUR + f' <a href="{url}">Facebook</a>',
        '<nav><a href="/kontakt">Kontakt</a></nav>' + schema,
    )

    def respond(request):
        if request.url.path == '/robots.txt':
            return httpx.Response(200, text='User-agent: *\nAllow: /')
        if request.url.path == '/kontakt':
            # Contact publisher is itself foreign. Its HTML supplies veto evidence.
            return httpx.Response(200, text='<footer>Subsidiary AS Org.nr ' + web.OTHER + '</footer>')
        return httpx.Response(200, text=homepage)

    _, row, requests, cfg = web.execute_web(tmp_path, monkeypatch, response=respond)
    website = next(c for c in row['claims'] if c['field'] == 'official_website')
    assert website['value']['identity_level'] == 'VERIFIED'
    assert website['value']['relationship_note'] is None
    assert requests.count('https://example.no/kontakt') == 1
    refresh = row['run']['refresh']['website']
    assert refresh['social_scope'] == 'other_orgnr_on_page'
    contact = next(p for p in refresh['social_pages'] if p['url'].endswith('/kontakt'))
    assert not contact['eligible']
    socials = [c for c in row['claims'] if c['field'].startswith('social_profile.')]
    if not exact_link:
        assert not socials
        return
    assert len(socials) == 1
    assert socials[0]['value']['proof_tier'] == SAME_AS
    assert socials[0]['value']['owner_declaration']['owner_match'] == 'exact_orgnr'
    assert verify(cfg.output, cfg.state_dir, 1)['briefing_unverified_values'] == 0

    forged = copy.deepcopy(row)
    value = next(c['value'] for c in forged['claims'] if c['field'].startswith('social_profile.'))
    value['proof_tier'] = 'own_header_footer_exact_name_v1'
    value.pop('owner_declaration')
    evidence = {e['id']: e for e in forged['evidence']}
    read = lambda sha: (cfg.state_dir / 'blobs' / sha).read_bytes()
    with pytest.raises(AssertionError, match='Unsupported owner social declaration'):
        verify_social(web.OUR, forged, evidence, lambda sha: decode_body(read(sha)), read)


def test_missing_registry_index_does_not_open_a_shared_site_bypass(monkeypatch):
    def unavailable():
        raise OSError('Bundle missing')

    monkeypatch.setattr(social_registry, 'load', unavailable)
    page = Page(b'<footer><a href="https://facebook.com/example">Facebook</a></footer>', 'https://example.no')
    site = {'final_url': page.url, 'identity_level': 'VERIFIED'}
    scope, _, _ = site_scope(site, [page], web.OUR, 'EXAMPLE AS')
    assert scope == 'registry_name_index_unavailable'
    assert not page_profiles(page, site, web.OUR, {'name': 'EXAMPLE AS'}, visible_profiles([page]), bool(scope))


def test_refresh_records_policy_abstention_without_claiming_account_removal(tmp_path, monkeypatch):
    url = 'https://facebook.com/example'
    anchor = f'<a href="{url}">Facebook</a>'
    footer = 'Org.nr ' + web.OUR + ' ' + anchor
    _, before, _, first = web.execute_web(tmp_path / 'old', monkeypatch, body=web.html(footer))
    field = next(c['field'] for c in before['claims'] if c['field'].startswith('social_profile.'))
    _, after, _, _ = web.execute_web(
        tmp_path / 'new', monkeypatch,
        body=web.html(footer, '<main>Trollheim Kurs og Kompetanse AS</main>'), previous=first.output,
    )
    assert any(c['field'] == 'official_website' for c in after['claims'])
    assert not any(c['field'] == field for c in after['claims'])
    assert not any(change['field'] == field for change in after['changes'])
    observations = after['run']['refresh']['observation_changes']
    assert any(o.get('field') == field and o['reason'] == 'social_site_scope_unresolved' for o in observations)
