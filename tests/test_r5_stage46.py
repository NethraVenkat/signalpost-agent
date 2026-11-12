import json
import pytest
from signalpost.web.html import Page
from signalpost.web.social import discover_strict
from tests.test_websites import html, OUR, OTHER, execute_web


@pytest.mark.parametrize('tag',['header','footer'])
def test_exact_company_profile_in_own_header_footer(tag):
    page=Page(html('',extra=f'<{tag}><a href="https://facebook.com/example">Facebook</a></{tag}>').encode(),'https://example.no/')
    assert list(discover_strict(page,'Example AS'))==['https://facebook.com/example']


@pytest.mark.parametrize('extra',[
    '<nav><a href="https://facebook.com/example">Example</a></nav>',
    '<script type="application/ld+json">{"sameAs":"https://facebook.com/example"}</script>',
    '<footer><a href="https://facebook.com/founder-person">Founder</a></footer>',
    '<footer><div class="agency-credit"><a href="https://facebook.com/example">Example</a></div></footer>',
    '<footer><a href="https://facebook.com/example-group">Example Group</a></footer>',
    '<article><footer><a href="https://facebook.com/example">Example</a></footer></article>',
    '<footer hidden><a href="https://facebook.com/example">Example</a></footer>',
])
def test_non_own_or_wrong_name_profile_abstains(extra):
    page=Page(html('',extra=extra).encode(),'https://example.no/')
    assert not discover_strict(page,'Example AS')


@pytest.mark.parametrize('name,handle',[('Εταιρεία AS','as'),('Éxample AS','xample'),('AS','as')])
def test_unicode_letters_and_suffix_only_names_cannot_create_false_agreement(name,handle):
    page=Page(html('',extra=f'<footer><a href="https://facebook.com/{handle}">Company</a></footer>').encode(),'https://example.no/')
    assert not discover_strict(page,name)


def test_full_literal_unicode_company_handle_can_match():
    page=Page(html('',extra='<footer><a href="https://facebook.com/εταιρεία">Company</a></footer>').encode(),'https://example.no/')
    assert discover_strict(page,'Εταιρεία AS')


def test_group_footer_does_not_publish_even_matching_handle(tmp_path,monkeypatch):
    _,row,_,_=execute_web(tmp_path,monkeypatch,body=html('Org.nr '+OUR+' Parent '+OTHER,
                        extra='<footer><a href="https://facebook.com/example">Example</a></footer>'))
    assert any(c['field']=='official_website' for c in row['claims'])
    assert not any(c['field'].startswith('social_profile.') for c in row['claims'])


def test_social_proof_links_registry_name_site_identity_and_exact_span(tmp_path,monkeypatch):
    _,row,_,_=execute_web(tmp_path,monkeypatch,body=html('Org.nr '+OUR,
                        extra='<footer><a href="https://facebook.com/example">Example</a></footer>'))
    claim=next(c for c in row['claims'] if c['field'].startswith('social_profile.'))
    assert claim['value']['proof_tier']=='own_header_footer_exact_name_v1'
    records={e['id']:e for e in row['evidence']}
    assert {'company_owned','official_registry'} <= {records[eid]['source_class'] for eid in claim['evidence_ids']}


def test_legacy_social_cannot_return_through_failed_refresh(tmp_path,monkeypatch):
    from signalpost.models.envelope import Envelope
    from signalpost.refresh.diff import apply
    from signalpost.sources.blobstore import BlobStore
    _,old,_,cfg=execute_web(tmp_path,monkeypatch,body=html('Org.nr '+OUR,
                         extra='<footer><a href="https://facebook.com/example">Example</a></footer>'))
    for c in old['claims']:
        if c['field'].startswith('social_profile.'):c['value'].pop('proof_tier')
    current=Envelope.model_validate(old)
    current.claims=[c for c in current.claims if not c.field.startswith('social_profile.')]
    current.run.sections['website']='failed'
    apply(current,old,BlobStore(cfg.state_dir))
    assert not any(c.field.startswith('social_profile.') for c in current.claims)


@pytest.mark.parametrize('enabled',[True,False])
def test_policy_tightening_is_observation_only_in_checked_scope(tmp_path,monkeypatch,enabled):
    from signalpost.models.envelope import Envelope
    from signalpost.refresh.diff import apply
    from signalpost.sources.blobstore import BlobStore
    _,old,_,cfg=execute_web(tmp_path,monkeypatch,body=html('Org.nr '+OUR,
                         extra='<footer><a href="https://facebook.com/example">Example</a></footer>'))
    for c in old['claims']:
        if c['field'].startswith('social_profile.'):c['value'].pop('proof_tier')
    current=Envelope.model_validate(old)
    current.claims=[c for c in current.claims if not c.field.startswith('social_profile.')]
    if not enabled:current.run.sections.pop('website')
    apply(current,old,BlobStore(cfg.state_dir))
    assert not any(c.field.startswith('social_profile.') for c in current.changes)
    observations=[o for o in current.run.refresh['observation_changes'] if o.get('reason')=='social_proof_policy_changed']
    assert bool(observations) is enabled
