import json
from html.parser import HTMLParser
from pathlib import Path
import pytest

from signalpost.models.shapes import serialize
from signalpost.site import (
    generate_site, CSP, sanitize_csv_cell, format_csv_orgnr,
    export_directory_csv, export_directory_json,
    export_profile_claims_json, export_profile_summary_csv
)
from tests.test_synthesis import envelope
from tests.test_synthesis_readability import available
from tests.test_registry import config, execute


def test_unknown_reporting_currency_is_not_exported_as_nok():
    import csv,io
    row=next(csv.DictReader(io.StringIO(export_directory_csv([{'orgnr':'923609016','revenue':123}]))))
    assert row['Revenue']=='123' and row['Currency']==''


def test_csv_control_prefixes_cannot_hide_formulas():
    import csv,io
    for prefix in ['\x00','\x0b','\x1f','\x7f','\x85','\u200b','\ufeff','\u00a0',' \n\t']:
        for trigger in ['=SUM(1,2)','+cmd','-2+3','@SUM(A1)']:
            raw=prefix+trigger
            decoded=next(csv.reader(io.StringIO(sanitize_csv_cell(raw))))[0]
            assert decoded=="'"+raw
    for text in ['æøå “quoted”','line1\nline2','a,"b"',None,'-12.34']:
        cell=sanitize_csv_cell(text)
        assert cell=='' if text is None else next(csv.reader(io.StringIO(cell)))[0]==text


def test_carried_fact_shows_last_successful_check():
    from signalpost.site import fact
    claim={'id':'a'*64,'field':'identity.legal_name','family':'identity','value':'Example AS',
           'availability':'available','carried_forward':True,'last_observed_at':'2026-10-01T12:00:00Z','evidence_ids':[]}
    markup=fact(claim,{})
    assert 'Previously supported; not freshly checked' in markup
    assert 'Last successfully checked:' in markup and '2026-10-01' in markup


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


def test_large_company_page_stays_under_gate_with_every_claim_reachable(tmp_path):
    from signalpost.models.claim import Claim
    row, _ = envelope(tmp_path / 'run')
    template = row.claims[0]
    for n in range(400):
        row.claims.append(Claim(**{**template.model_dump(), 'id': ('%016x' % (n + 1)) + '0' * 48, 'field': f'subunits.detail.{n}'}))
    out = tmp_path / 'site'
    metrics = generate_site(source(tmp_path, [row]), out)
    html = (out / f'c/{row.organisation_number}.html').read_text(encoding='utf8')
    assert metrics['largest_profile_bytes'] < 250_000
    assert 'id="explorer-show-all"' in html
    data = (out / f'c/{row.organisation_number}.data.js').read_text(encoding='utf8')
    payload = json.loads(data[len('window.SIGNALPOST_EVIDENCE = '):-2])
    shown = html.count('<th scope="row">')
    assert shown + len(payload['explorer_rows']) >= len(row.claims)


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


def test_formula_sanitization_and_orgnr_formatting():
    # Dangerous formula characters are prefixed with single quote '
    assert sanitize_csv_cell("=1+1") == "'=1+1"
    assert sanitize_csv_cell("+cmd|' /C calc'!A0") == "'+cmd|' /C calc'!A0"
    assert sanitize_csv_cell("-MIN(A1:A5)") == "'-MIN(A1:A5)"
    assert sanitize_csv_cell("-2+3") == "'-2+3"
    assert sanitize_csv_cell("@SUM(B1:B2)") == "'@SUM(B1:B2)"
    assert sanitize_csv_cell("\ttab_attack") == "'\ttab_attack"
    assert sanitize_csv_cell(" =1+1") == "' =1+1"
    assert sanitize_csv_cell("\rcarriage_return") == '"\'\rcarriage_return"'

    # Commas, quotes, and newlines are safely quoted and escaped per RFC 4180
    assert sanitize_csv_cell('Hello, "World"') == '"Hello, ""World"""'
    assert sanitize_csv_cell("Line 1\nLine 2") == '"Line 1\nLine 2"'

    # Legitimate numbers (including negative amounts and string negative numbers) remain clean
    assert sanitize_csv_cell(12345) == "12345"
    assert sanitize_csv_cell(-450000) == "-450000"
    assert sanitize_csv_cell("-450000") == "-450000"
    assert sanitize_csv_cell("-12.34") == "-12.34"
    assert sanitize_csv_cell(0) == "0"
    assert sanitize_csv_cell(None) == ""
    assert sanitize_csv_cell(True) == "Yes"
    assert sanitize_csv_cell(False) == "No"

    # Organisation numbers formatted as plain literal digit strings (no ="..." formula bypass)
    assert format_csv_orgnr("012345678") == "012345678"
    assert format_csv_orgnr(987654321) == "987654321"


def test_directory_exports_csv_and_json():
    records = [
        {
            "orgnr": "012345678",
            "name": "Nordic Solutions AS",
            "municipality": "Oslo",
            "nace": "62.010",
            "industry_en": "Computer programming activities",
            "employees": 15,
            "size_band": "small",
            "revenue": 25000000,
            "annual_result": 3200000,
            "currency": "NOK",
            "unit": "NOK",
            "fiscal_year": 2024,
            "website": "https://example.no",
            "website_origin": "registry_website",
            "jobs": 2,
            "social": 1,
            "activity": 3,
            "claim_count": 28,
            "last_checked": "2026-10-14T10:00:00Z"
        }
    ]

    csv_data = export_directory_csv(records)
    lines = csv_data.strip().split("\r\n")
    assert len(lines) == 2
    assert "Organisation number,Name,Municipality" in lines[0]
    assert "Revenue,Annual result,Currency,Financial unit,Fiscal year" in lines[0]
    assert "012345678,Nordic Solutions AS,Oslo" in lines[1]
    assert "25000000,3200000,NOK,NOK,2024" in lines[1]

    json_data = export_directory_json(records)
    parsed = json.loads(json_data)
    assert len(parsed) == 1
    assert parsed[0]["orgnr"] == "012345678"
    assert parsed[0]["name"] == "Nordic Solutions AS"


def test_profile_claims_provenance_exports(tmp_path):
    row, _ = envelope(tmp_path / 'run')
    # Row dictionary as used in site generation
    row_dict = json.loads(json.dumps(serialize(row, 'union')))

    json_exp = export_profile_claims_json(row_dict)
    data = json.loads(json_exp)
    assert data["organisation_number"] == row.organisation_number
    assert data["claims_count"] == len(row.claims)
    assert len(data["claims"]) == len(row.claims)

    # Check complete supporting provenance on available claims
    available_claim = next(c for c in data["claims"] if c["availability"] == "available" and c["evidence"])
    ev = available_claim["evidence"][0]
    for key in ("source_class", "source_url", "locator", "claim_span", "content_sha256", "retrieved_at"):
        assert key in ev
        assert ev[key] is not None
        assert len(ev["claim_span"]) <= 300

    csv_exp = export_profile_summary_csv(row_dict)
    csv_lines = csv_exp.strip().split("\r\n")
    assert len(csv_lines) == len(row.claims) + 1
    assert "Organisation number,Field,Family,Availability,Value" in csv_lines[0]
    assert f'{row.organisation_number}' in csv_lines[1]


def test_evidence_explorer_markup_and_export_controls(tmp_path):
    row, _ = envelope(tmp_path / 'run')
    out = tmp_path / 'site'
    generate_site(source(tmp_path, [row]), out)

    profile_html = (out / f'c/{row.organisation_number}.html').read_text(encoding='utf8')
    assert 'id="evidence-explorer"' in profile_html
    assert 'class="evidence-explorer-table"' in profile_html
    assert 'id="export-profile-json"' in profile_html
    assert 'id="export-profile-csv"' in profile_html

    # Check gate: profile HTML must be under 250 KB
    assert len(profile_html.encode('utf8')) < 250_000

    # Check dashboard and directory export buttons on index.html
    index_html = (out / 'index.html').read_text(encoding='utf8')
    assert 'id="export-dashboard-csv"' in index_html
    assert 'id="export-dashboard-json"' in index_html
    assert 'id="export-directory-csv"' in index_html
    assert 'id="export-directory-json"' in index_html

    # Ensure CSP is intact
    assert CSP in __import__('html').unescape(profile_html)
    assert CSP in __import__('html').unescape(index_html)


def test_verified_changes_and_freshness_presentation(tmp_path):
    row, _ = envelope(tmp_path / 'run')
    from signalpost.models.envelope import Change
    row.changes = [
        Change(
            organisation_number=row.organisation_number,
            type="changed",
            field="identity.legal_name",
            old_value="Old Corp AS",
            new_value="New Corp AS",
            old_evidence_ids=[],
            new_evidence_ids=[],
            materiality="material",
            first_observed_at="2025-01-01T00:00:00Z",
            last_observed_at="2026-10-14T10:00:00Z",
            old_locator="row:old/col:navn",
            new_locator="row:new/col:navn",
            old_content_sha256="1111222233334444555566667777888899990000aaaabbbbccccddddeeeeffff",
            new_content_sha256="aaaabbbbccccddddeeeeffff1111222233334444555566667777888899990000",
            status="available"
        )
    ]
    row.run.refresh["observation_changes"] = [
        {
            "section": "roles",
            "previous_state": "failed",
            "current_state": "not_available",
            "reason": "http_timeout"
        }
    ]
    out = tmp_path / 'site'
    generate_site(source(tmp_path, [row]), out)

    profile_html = (out / f'c/{row.organisation_number}.html').read_text(encoding='utf8')
    assert 'class="freshness-banner"' in profile_html
    assert 'Last verified:' in profile_html
    assert 'Verified business changes' in profile_html
    assert 'Old Corp AS' in profile_html
    assert 'New Corp AS' in profile_html
    assert 'row:old/col:navn' in profile_html
    assert 'row:new/col:navn' in profile_html
    assert '111122223333' in profile_html
    assert 'aaaabbbbcccc' in profile_html

    # Check separation of source availability / observation changes
    assert 'Source availability &amp; observation changes' in profile_html
    assert 'roles' in profile_html
    assert 'http_timeout' in profile_html


def test_hiring_explorer_watchlist_and_financial_trend(tmp_path):
    row, _ = envelope(tmp_path / 'run')
    available(row, 'hiring.job.one', {
        'title': 'Senior Cloud Engineer',
        'published': '2026-10-01T08:00:00Z',
        'expires': '2026-11-01T08:00:00Z',
        'matched_via': 'exact_orgnr',
        'uuid': 'nav-uuid-1234'
    })
    available(row, 'accounts.revenue', 18000000, reporting_period={'fiscal_year': 2024, 'period_start': '2024-01-01', 'period_end': '2024-12-31'})
    available(row, 'accounts.operating_profit', 3000000, reporting_period={'fiscal_year': 2023, 'period_start': '2023-01-01', 'period_end': '2023-12-31'})
    out = tmp_path / 'site'
    generate_site(source(tmp_path, [row]), out)

    index_html = (out / 'index.html').read_text(encoding='utf8')
    assert 'id="tab-hiring"' in index_html
    assert 'id="view-hiring"' in index_html
    assert 'id="filter-watchlist"' in index_html
    assert 'class="saved-views-bar"' in index_html

    index_data = json.loads((out / 'data/index.json').read_text(encoding='utf8'))
    assert len(index_data) == 1
    postings = index_data[0].get('job_postings', [])
    assert len(postings) >= 1
    assert any(j['title'] == 'Senior Cloud Engineer' for j in postings)

    profile_html = (out / f'c/{row.organisation_number}.html').read_text(encoding='utf8')
    assert 'btn-watchlist' in profile_html
    assert 'class="financial-trend-banner"' in profile_html
    assert 'Multi-year filing trend' in profile_html




