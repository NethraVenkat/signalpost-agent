import pytest
from signalpost.web.html import Page
from signalpost.web.social import discover_strict
from tests.test_websites import OUR, OTHER, execute_web, html

URL = 'https://www.linkedin.com/company/123301'


@pytest.mark.parametrize('tag', ['header', 'footer', 'div role="contentinfo"'])
def test_numeric_linkedin_requires_own_semantic_header_or_footer(tag):
    close = tag.split()[0]
    page = Page(html('', extra=f'<{tag}><a href="{URL}">LinkedIn</a></{close}>').encode(), 'https://example.no/')
    assert list(discover_strict(page, 'Example AS')) == [URL]


@pytest.mark.parametrize('extra', [
    f'<nav><a href="{URL}">LinkedIn</a></nav>',
    f'<script type="application/ld+json">{{"sameAs":"{URL}"}}</script>',
    f'<article><footer><a href="{URL}">LinkedIn</a></footer></article>',
    f'<footer hidden><a href="{URL}">LinkedIn</a></footer>',
    f'<footer><div class="agency-credit"><a href="{URL}">LinkedIn</a></div></footer>',
    f'<footer><a href="{URL}">Founder</a></footer>',
    f'<footer>Utviklet av <a href="{URL}">LinkedIn</a></footer>',
    f'<footer>Our founder: <a href="{URL}">LinkedIn</a></footer>',
    '<footer><a href="https://facebook.com/123301">Facebook</a></footer>',
    '<footer><a href="https://linkedin.com/company/123abc">LinkedIn</a></footer>',
    '<footer><a href="https://linkedin.com/in/123301">LinkedIn</a></footer>',
])
def test_numeric_exception_does_not_bypass_context_or_platform_rules(extra):
    page = Page(html('', extra=extra).encode(), 'https://example.no/')
    assert not discover_strict(page, 'Example AS')


@pytest.mark.parametrize('footer,title', [
    ('Org nr '+OUR+' Parent '+OTHER, 'Example AS'),
    ('Org nr '+OUR, 'Example Holding'),
    ('Org nr '+OUR+' Our companies', 'Example AS'),
])
def test_numeric_linkedin_from_shared_group_site_is_withheld(tmp_path, monkeypatch, footer, title):
    _, row, _, _ = execute_web(tmp_path, monkeypatch, body=html(footer, title=title,
                        extra=f'<footer><a href="{URL}">LinkedIn</a></footer>'))
    assert any(c['field'] == 'official_website' for c in row['claims']) == (OTHER not in footer)
    assert not any(c['field'].startswith('social_profile.') for c in row['claims'])


def test_numeric_profile_retains_name_identity_and_verbatim_link_proof(tmp_path, monkeypatch):
    _, row, requests, _ = execute_web(tmp_path, monkeypatch, body=html('Org nr '+OUR,
                        extra=f'<footer><a href="{URL}">LinkedIn</a></footer>'))
    claim = next(c for c in row['claims'] if c['field'].startswith('social_profile.'))
    assert claim['value']['proof_tier'] == 'own_header_footer_numeric_linkedin_v1'
    evidence = {e['id']: e for e in row['evidence']}
    linked = [evidence[eid] for eid in claim['evidence_ids']]
    assert any(URL in e['claim_span'] for e in linked)
    assert any(OUR in e['claim_span'] for e in linked)
    assert any(e['source_class'] == 'official_registry' for e in linked)
    assert not any('linkedin.com' in request for request in requests)


def test_numeric_profile_is_not_carried_through_failed_refresh(tmp_path, monkeypatch):
    from signalpost.models.envelope import Envelope
    from signalpost.refresh.diff import apply
    from signalpost.sources.blobstore import BlobStore
    _, old, _, cfg = execute_web(tmp_path, monkeypatch, body=html('Org nr '+OUR,
                         extra=f'<footer><a href="{URL}">LinkedIn</a></footer>'))
    current = Envelope.model_validate(old)
    current.claims = [c for c in current.claims if not c.field.startswith('social_profile.')]
    current.run.sections['website'] = 'failed'
    apply(current, old, BlobStore(cfg.state_dir))
    assert not any(c.field.startswith('social_profile.') for c in current.claims)
