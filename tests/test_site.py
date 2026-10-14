import json
from html.parser import HTMLParser
from pathlib import Path
import pytest

from signalpost.models.shapes import serialize
from signalpost.site import generate_site, CSP
from tests.test_synthesis import envelope
from tests.test_synthesis_readability import available
from tests.test_registry import config, execute


class Markup(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.ids = set()
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if 'id' in attrs: self.ids.add(attrs['id'])
        if 'href' in attrs: self.links.append(attrs['href'])


def source(tmp, rows, shape='union'):
    p = tmp / 'source.jsonl'
    p.write_text('\n'.join(json.dumps(serialize(r, shape), ensure_ascii=False) for r in rows), encoding='utf8')
    return p


@pytest.mark.parametrize('shape', ['union', 'reference', 'contract'])
def test_site_membership_evidence_citations_and_determinism(tmp_path, shape):
    row, _ = envelope(tmp_path / 'run')
    out = tmp_path / 'site'
    inp = source(tmp_path, [row], shape)
    metrics = generate_site(inp, out)
    assert metrics['companies'] == 1 and metrics['pages'] == 3
    assert metrics['largest_profile_bytes'] < 250_000
    index = json.loads((out / 'data/index.json').read_text(encoding='utf8'))
    assert [r['orgnr'] for r in index] == [row.organisation_number]
    text = (out / f'c/{row.organisation_number}.html').read_text(encoding='utf8')
    markup = Markup(text)
    data_text = (out / f'c/{row.organisation_number}.data.js').read_text(encoding='utf8')
    payload = json.loads(data_text.removeprefix('window.SIGNALPOST_EVIDENCE = ').rstrip(';\n'))
    evidence = {}
    for record in payload['records']:
        e = dict(zip(payload['source_fields'], payload['sources'][record[0]]))
        e.update(zip(payload['evidence_fields'], record[1:]))
        evidence[e['id']] = e
    facts = {f['id']: f for f in payload['facts']}
    for href in markup.links:
        if href.startswith('#'): assert href[1:] in markup.ids
    for claim in row.claims:
        if claim.availability == 'available':
            assert 'fact-' + claim.id[:16] in markup.ids
            assert 'source-' + claim.id[:16] in markup.ids
            for eid in claim.evidence_ids:
                e = next(e for e in row.evidence if e.id == eid)
                assert evidence[eid]['content_sha256'] == e.content_sha256
                assert evidence[eid]['retrieved_at'] == e.retrieved_at
                assert evidence[eid]['claim_span'] == e.claim_span
                assert evidence[eid] == {key: getattr(e, key) for key in payload['source_fields'] + payload['evidence_fields']}
                assert eid in facts[claim.id[:16]]['evidence_ids']
    assert CSP in __import__('html').unescape(text)
    for tag, attrs in markup.tags:
        assert not any(k.startswith('on') for k in attrs)
        if tag in {'script', 'link', 'img'}:
            assert not (attrs.get('src') or attrs.get('href') or '').startswith(('http:', 'https:', '//'))
        if tag == 'a' and attrs.get('href', '').startswith(('http:', 'https:')):
            assert attrs['target'] == '_blank'
            assert set(attrs['rel'].split()) == {'noopener', 'noreferrer', 'nofollow'}
    before = {p.relative_to(out): p.read_bytes() for p in out.rglob('*') if p.is_file()}
    generate_site(inp, out)
    assert before == {p.relative_to(out): p.read_bytes() for p in out.rglob('*') if p.is_file()}


def test_xss_is_text_and_bad_urls_are_not_links(tmp_path):
    row, _ = envelope(tmp_path / 'run')
    evil = '<script>alert(1)</script> "><img src=x onerror=alert(2)>'
    available(row, 'identity.legal_name', evil)
    available(row, 'website_description.meta.x', {'text': evil, 'url': 'javascript:alert(1)'})
    available(row, 'hiring.job.x', {'title': evil, 'url': 'javascript:alert(1)'})
    available(row, 'official_website', {'final_url': 'javascript:alert(1)', 'identity_level': 'VERIFIED'})
    row.run.synthesis = None
    row.profile.synthesis = None
    out = tmp_path / 'site'
    generate_site(source(tmp_path, [row]), out, evil)
    for p in out.rglob('*.html'):
        text = p.read_text(encoding='utf8')
        markup = Markup(text)
        assert '<script>alert' not in text and '<img src=x' not in text
        assert not any(tag == 'img' for tag, _ in markup.tags)
        assert all(not url.lower().startswith('javascript:') for url in markup.links)
        assert all('src' in attrs for tag, attrs in markup.tags if tag == 'script')
    js = (out / 'data/index.js').read_text(encoding='utf8')
    assert '</script>' not in js and '<\\/script>' in js
    detail = (out / f'c/{row.organisation_number}.data.js').read_text(encoding='utf8')
    assert '</script>' not in detail and '<\\/script>' in detail
    assert 'innerHTML' not in (out / 'assets/site.js').read_text(encoding='utf8')


def test_site_error_is_isolated_and_reported(tmp_path, monkeypatch):
    cfg = config(tmp_path / 'run', ['923609016'])
    _, before = execute(cfg)
    cfg.site_dir = tmp_path / 'site'
    def fail(*args, **kwargs): raise RuntimeError('forced template error')
    monkeypatch.setattr('signalpost.site.profile', fail)
    report, after = execute(cfg)
    assert report['site']['state'] == 'failed' and report['site']['error'] == 'RuntimeError'
    assert report['site'] == json.loads(cfg.report.read_text(encoding='utf8'))['site']
    # Retrieval/run timestamps are allowed to change; site errors cannot change facts or synthesis.
    assert before[0]['claims'] == after[0]['claims'] or [(c['id'], c['value']) for c in before[0]['claims']] == [(c['id'], c['value']) for c in after[0]['claims']]
    assert before[0]['run']['synthesis'] == after[0]['run']['synthesis']
    assert not (cfg.site_dir / 'index.html').exists()


def test_cli_site_failure_keeps_exit_zero(tmp_path, monkeypatch):
    import respx
    from signalpost.cli import main
    from tests.test_registry import handler
    cfg = config(tmp_path / 'run', ['923609016'])
    monkeypatch.setattr('sys.argv', ['signalpost', 'run', '--organisations', str(cfg.organisations),
                         '--output', str(cfg.output), '--report', str(cfg.report), '--state-dir', str(cfg.state_dir),
                         '--site-dir', str(tmp_path / 'site')])
    def fail(*args, **kwargs): raise RuntimeError('forced template error')
    monkeypatch.setattr('signalpost.site.profile', fail)
    with respx.mock(assert_all_called=False) as router:
        router.get(url__regex=r'https://data\.brreg\.no/.*').mock(side_effect=handler())
        assert main() == 0
    assert json.loads(cfg.report.read_text(encoding='utf8'))['site']['state'] == 'failed'


def test_reject_path_traversal_and_source_overlap(tmp_path):
    row, _ = envelope(tmp_path / 'run')
    inp = source(tmp_path, [row])
    with pytest.raises(ValueError, match='contain'): generate_site(inp, tmp_path)
    raw = serialize(row, 'union'); raw['organisation_number'] = '../bad'
    inp.write_text(json.dumps(raw), encoding='utf8')
    with pytest.raises(ValueError, match='nine digit'): generate_site(inp, tmp_path / 'site')


def test_render_before_write_and_incomplete_evidence(tmp_path):
    row, _ = envelope(tmp_path / 'run')
    row.evidence[0].claim_span = ''
    out = tmp_path / 'site'
    with pytest.raises(ValueError, match='Incomplete evidence'):
        generate_site(source(tmp_path, [row]), out)
    assert not out.exists()


def test_registry_dates_count_in_activity_filter(tmp_path):
    row,_=envelope(tmp_path / 'run')
    row.run.completed_at='2026-10-13T00:00:00Z'
    available(row,'identity.founding_date','2026-01-01')
    row.run.synthesis=None;row.profile.synthesis=None
    out=tmp_path / 'site';generate_site(source(tmp_path,[row]),out)
    record=json.loads((out/'data/index.json').read_text(encoding='utf8'))[0]
    assert record['flags']['activity'] and record['activity']>=1
    assert record['sections']['activity']=='available'
    markup = Markup((out / f'c/{row.organisation_number}.html').read_text(encoding='utf8'))
    assert all(href[1:] in markup.ids for href in markup.links if href.startswith('#'))


def test_identical_duplicate_rows_share_a_profile(tmp_path):
    row, _ = envelope(tmp_path / 'run')
    result = generate_site(source(tmp_path, [row, row]), tmp_path / 'site')
    assert result['input_records'] == 2
    assert result['companies'] == 1 and result['pages'] == 3


def test_scalar_role_metadata_is_not_a_role_record(tmp_path):
    row,_=envelope(tmp_path/'run')
    available(row,'roles.detail.example.0.order',1)
    row.run.synthesis=None;row.profile.synthesis=None
    result=generate_site(source(tmp_path,[row]),tmp_path/'site')
    assert result['companies']==1


def test_dashboard_filters_comparison_and_timeline(tmp_path):
    row, _ = envelope(tmp_path / 'run')
    available(row, 'identity.employees', 5)
    available(row, 'identity.founding_date', '2020-05-15')
    row.run.synthesis = None
    row.profile.synthesis = None
    out = tmp_path / 'site'
    generate_site(source(tmp_path, [row]), out)

    index_html = (out / 'index.html').read_text(encoding='utf8')
    assert 'id="tab-dashboard"' in index_html
    assert 'id="tab-directory"' in index_html
    assert 'id="view-dashboard"' in index_html
    assert 'id="view-directory"' in index_html
    assert 'id="dashboard-scope-banner"' in index_html
    assert 'id="provenance-breakdown"' in index_html
    assert 'id="hiring-timeline"' in index_html
    assert 'id="recent-activity-list"' in index_html
    assert 'id="size-band"' in index_html
    assert 'id="active-filters-bar"' in index_html
    assert 'id="search-autocomplete"' in index_html

    index_json = json.loads((out / 'data/index.json').read_text(encoding='utf8'))[0]
    assert index_json['size_band'] == 'micro'
    assert index_json['founding_date'] == '2020-05-15'

    profile_html = (out / f'c/{row.organisation_number}.html').read_text(encoding='utf8')
    assert 'id="timeline"' in profile_html
    assert 'class="timeline-item"' in profile_html
    profile_markup = Markup(profile_html)
    for href in profile_markup.links:
        if href.startswith('#'):
            assert href[1:] in profile_markup.ids

    compare_html = (out / 'compare.html').read_text(encoding='utf8')
    assert 'id="comparison"' in compare_html
    assert 'id="clear-compare"' in compare_html
    assert 'id="company-options"' in compare_html


def test_update_status_panel_markup_and_accessibility(tmp_path):
    row, _ = envelope(tmp_path / 'run')
    out = tmp_path / 'site'
    generate_site(source(tmp_path, [row]), out)

    index_html = (out / 'index.html').read_text(encoding='utf8')
    assert 'id="status-toggle"' in index_html
    assert 'id="status-panel"' in index_html
    assert 'id="status-dot"' in index_html
    assert 'id="status-badge"' in index_html
    assert 'id="status-progress"' in index_html
    assert 'id="status-counters"' in index_html
    assert 'id="status-stages"' in index_html
    assert 'id="status-timing"' in index_html
    assert 'id="status-events"' in index_html
    assert 'role="dialog"' in index_html
    assert 'aria-modal="true"' in index_html
    assert 'aria-controls="status-panel"' in index_html

    # Check CSP and XSS safety
    markup = Markup(index_html)
    for tag, attrs in markup.tags:
        assert not any(k.startswith('on') for k in attrs)
    assert CSP in __import__('html').unescape(index_html)


