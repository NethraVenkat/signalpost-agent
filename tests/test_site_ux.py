"""Site-only regression checks for the approved UX gaps."""
from copy import deepcopy
from pathlib import Path
import re

from signalpost.models.shapes import serialize
from signalpost.site import compare_page, index_record, profile
from tests.test_synthesis import envelope


def test_g1_index_uses_newest_dated_claim_with_receipt_anchor(tmp_path):
    row, _ = envelope(tmp_path)
    data = serialize(row, 'union')
    source = next(c for c in data['claims'] if c['availability'] == 'available')
    for ident, date, title in [('e' * 64, '2026-10-01', 'Older update'),
                               ('f' * 64, '2026-10-17', 'Newer update')]:
        event = deepcopy(source)
        event.update(id=ident, family='activity', field='dated_item.' + ident[:8],
                     value={'date': date, 'title': title, 'url': 'https://example.test/news'})
        data['claims'].append(event)
    record = index_record(data)
    assert record['recent_events'] == [
        {'date': '2026-10-17', 'label': 'Newer update', 'anchor': 'fact-' + 'f' * 16}]
    assert record['latest_activity_label'] == 'Newer update'
    assert record['activity'] >= 2


def test_g1_no_changes_wording_requires_checked_not_available_state(tmp_path):
    row, _ = envelope(tmp_path)
    data = serialize(row, 'union')
    data['run']['sections']['activity'] = 'not_available'
    assert 'No dated changes found in sources checked.' in profile(data, 'Signalpost')
    data['run']['sections']['activity'] = 'failed'
    assert 'No dated changes found in sources checked.' not in profile(data, 'Signalpost')


def test_g6_disclosure_controls_have_at_least_40px_target_rule():
    css = (Path(__file__).resolve().parents[1] / 'src/signalpost/site_assets/site.css').read_text(encoding='utf8')
    rule = re.search(r'details\s*>\s*summary\s*\{([^}]+)\}', css)
    assert rule is not None
    height = re.search(r'min-height:\s*(\d+)px', rule.group(1))
    assert height is not None and int(height.group(1)) >= 40


def test_g2_comparison_has_four_selectors_and_preserves_four_url_ids():
    html = compare_page('Signalpost')
    assert all(f'id="company-{i}"' in html for i in range(4))
    assert 'id="company-4"' not in html
    assert 'up to four companies' in html
    js = (Path(__file__).resolve().parents[1] / 'src/signalpost/site_assets/site.js').read_text(encoding='utf8')
    assert '.slice(0, 4)' in js
    assert 'Select up to 4 companies' in js
