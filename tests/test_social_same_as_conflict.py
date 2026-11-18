import copy
import hashlib
import json
from pathlib import Path

import httpx
import pytest

from scripts.verify_output import verify
from scripts.verify_owner_social import verify as verify_social
from signalpost.sources.text import decode_body
from signalpost.web.html import Page
from signalpost.web.owner_social import declared_profiles, same_as_veto, visible_profiles
from tests import test_websites as web

FIXTURES = Path(__file__).parent / 'fixtures/social_hc1'
ARENA = 'https://www.facebook.com/arenaskog'
WOODWORKS = 'https://www.facebook.com/woodworkscluster'


@pytest.mark.parametrize('separate_page', [False, True])
def test_woodworks_saved_same_as_conflicts_with_visible_profile(separate_page):
    # Verbatim slices at offsets 5686 and 173284 of P3g's saved homepage.
    # Original SHA-256 8e2c2eed3e3549b40dde5c22acd82eaedef946c7e8310918f415d092e369af44.
    script = (FIXTURES / 'woodworks-sameas.body').read_bytes()
    anchor = (FIXTURES / 'woodworks-visible-link.body').read_bytes()
    assert hashlib.sha256(script).hexdigest() == 'a39599aaec473e8ba0373c0a48f844d1503e2ac78cf0a1803218e7fa13dd910d'
    assert hashlib.sha256(anchor).hexdigest() == '5796db3ea06948ad2111f6490eb9b16d7f61a194dd9d2c596d8504e7a939b1f2'
    root = 'https://woodworkscluster.no/'
    home = Page(script if separate_page else script + b'<footer>' + anchor + b'</footer>', root)
    pages = [home, Page(anchor, root + 'kontakt/')] if separate_page else [home]
    assert ARENA in declared_profiles(home, 'WOODWORKS! CLUSTER', '927525399')
    assert same_as_veto(ARENA, visible_profiles(pages), 'WOODWORKS! CLUSTER') == 'same_as_visible_profile_conflict'
    assert same_as_veto(WOODWORKS, visible_profiles(pages), 'WOODWORKS! CLUSTER') is None


def test_equivalent_visible_url_and_hidden_different_link():
    page = Page(b'<main><a href="http://no.linkedin.com/company/PetroOnline-AS/">LinkedIn</a>'
                b'<a hidden href="https://www.linkedin.com/company/elsewhere">Hidden</a></main>', 'https://accella.no/')
    assert same_as_veto('https://www.linkedin.com/company/petroonline-as',
                        visible_profiles([page]), 'ACCELLA SOLUTIONS AS') is None


def test_jsonld_only_uses_distinctive_current_or_proven_former_name():
    url = 'https://www.linkedin.com/company/petroonline-as'
    assert same_as_veto(url, {}, 'ACCELLA SOLUTIONS AS') == 'same_as_no_distinctive_name'
    assert same_as_veto(url, {}, 'ACCELLA SOLUTIONS AS', ['PETRO ONLINE AS']) is None
    assert same_as_veto('https://facebook.com/accella', {}, 'ACCELLA SOLUTIONS AS') is None
    assert same_as_veto('https://facebook.com/group', {}, 'NORDVIK GROUP AS') == 'same_as_no_distinctive_name'


def test_collector_checks_fetched_contact_page_and_verifier_replays_it(tmp_path, monkeypatch):
    target = 'https://facebook.com/example'
    node = {'@type': 'Organization', 'vatID': 'NO' + web.OUR + 'MVA', 'sameAs': [target]}
    home = web.html(extra='<nav><a href="/kontakt">Kontakt</a></nav>'
                          '<script type="application/ld+json">' + json.dumps(node) + '</script>')

    def run(folder, link):
        def respond(request):
            if request.url.path == '/robots.txt':
                return httpx.Response(200, text='User-agent: *\nAllow: /')
            if request.url.path == '/kontakt':
                return httpx.Response(200, text=f'<main><a href="{link}">Facebook</a></main>')
            return httpx.Response(200, text=home)
        _, row, requests, cfg = web.execute_web(folder, monkeypatch, response=respond)
        assert sum(url == 'https://example.no/kontakt' for url in requests) == 1
        assert any(c['field'] == 'official_website' for c in row['claims'])
        return row, cfg

    clean, cfg = run(tmp_path / 'clean', target)
    claim = next(c for c in clean['claims'] if c['field'].startswith('social_profile.'))
    assert claim['value']['url'] == target
    assert verify(cfg.output, cfg.state_dir, 1)['briefing_unverified_values'] == 0

    conflict, conflict_cfg = run(tmp_path / 'conflict', 'https://facebook.com/elsewhere')
    assert not any(c['field'].startswith('social_profile.') for c in conflict['claims'])
    forged = copy.deepcopy(clean)
    forged['run']['refresh']['website'] = conflict['run']['refresh']['website']
    evidence = {e['id']: e for e in forged['evidence']}
    read = lambda sha: (conflict_cfg.state_dir / 'blobs' / sha).read_bytes()
    with pytest.raises(AssertionError, match='JSON-LD social veto'):
        verify_social(web.OUR, forged, evidence, lambda sha: decode_body(read(sha)), read)
