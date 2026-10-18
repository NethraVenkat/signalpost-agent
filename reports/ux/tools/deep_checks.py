"""Targeted source and synthesis checks against the generated offline site."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

UX = Path(__file__).resolve().parents[1]
SITE = UX / 'sample/site'
rows = {r['organisation_number']: r for r in (json.loads(line) for line in (UX / 'sample/out/envelopes.jsonl').open(encoding='utf8'))}
cases = {
    'identity': ('923609016', next(c for c in rows['923609016']['claims'] if c['field'] == 'identity.legal_name')),
    'roles': ('923609016', next(c for c in rows['923609016']['claims'] if c['field'].startswith('roles.role.'))),
    'subunits': ('923609016', next(c for c in rows['923609016']['claims'] if c['field'].startswith('subunits.unit.'))),
    'registry': ('932525070', next(c for c in rows['932525070']['claims'] if c['field'].startswith('registry_change.'))),
    'website': ('991853995', next(c for c in rows['991853995']['claims'] if c['field'] == 'official_website')),
    'social': ('991853995', next(c for c in rows['991853995']['claims'] if c['field'].startswith('social_profile.'))),
    'website_activity': ('991853995', next(c for c in rows['991853995']['claims'] if c['field'].startswith('dated_item.'))),
    'nav': ('929583027', next(c for c in rows['929583027']['claims'] if c['family'] == 'hiring' and c['availability'] == 'available')),
    'accounts': ('923609016', next(c for c in rows['923609016']['claims'] if c['field'] == 'accounts.revenue' and c['availability'] == 'available')),
}
result = {'claim_checks': {}, 'status_file': {}, 'dashboard': {}}
with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome', headless=True, args=['--allow-file-access-from-files'])
    for label, (org, claim) in cases.items():
        page = browser.new_page()
        page.goto((SITE / 'c' / f'{org}.html').resolve().as_uri())
        target = page.locator(f'#fact-{claim["id"][:16]}')
        if not target.count():
            target = page.locator(f'#field-{claim["id"][:16]}')
        buttons = target.locator('button[data-toggle^="source-"]')
        entry = {'org': org, 'field': claim['field'], 'fact_found': bool(target.count()), 'button_found': bool(buttons.count())}
        if buttons.count():
            button = buttons.first
            panel_id = button.get_attribute('data-toggle')
            button.click()
            panel = page.locator('#' + panel_id)
            body = panel.inner_text()
            entry.update({'opened': panel.is_visible(), 'source_link': 'Source link' in body,
                          'retrieval_utc': 'Retrieved at (UTC)' in body,
                          'method': 'Extraction method / version' in body,
                          'sha256': 'SHA-256' in body,
                          'source_quote': bool(panel.locator('blockquote').count()),
                          'source_href': panel.locator('a[href^="http"]').first.get_attribute('href') if panel.locator('a[href^="http"]').count() else None})
            shot = UX / 'screenshots/before' / f'{label}_evidence.png'
            target.screenshot(path=str(shot))
            entry['screenshot'] = str(shot.relative_to(UX))
        if label == 'registry':
            entry['visible_registry_label'] = 'Registry publication time:' in target.inner_text()
            entry['raw_registry_label'] = claim['value'].get('date_source')
            entry['visible_publication_timestamp'] = claim['value']['date'] in target.inner_text()
        if label == 'website':
            value = claim['value']
            entry['proof_type'] = value.get('proof_type')
            entry['identity_level'] = value.get('identity_level')
            entry['proof_url_in_source_panel'] = value.get('proof_page_url') in (body if buttons.count() else '')
            entry['proof_reason_visible'] = value.get('proof_type') in target.inner_text()
        if label == 'nav':
            entry['source_class'] = [e['source_class'] for e in rows[org]['evidence'] if e['id'] in claim['evidence_ids']]
            entry['job_title_visible'] = claim['value']['title'] in target.inner_text()
        result['claim_checks'][label] = entry
        page.close()

    page = browser.new_page()
    requests = []
    page.on('request', lambda r: requests.append(r.url))
    page.goto((SITE / 'index.html').resolve().as_uri())
    result['dashboard'] = {'reported_activity_companies': page.locator('#dash-total-activity').inner_text(),
                           'recent_list_text': page.locator('#recent-activity-list').inner_text(),
                           'index_records_with_recent_events': sum(bool(r.get('recent_events')) for r in json.loads((SITE / 'data/index.json').read_text(encoding='utf8')) if isinstance(r, dict))}
    page.locator('#status-toggle').click()
    page.locator('#status-panel').screenshot(path=str(UX / 'screenshots/before/status_file.png'))
    result['status_file'] = {'panel_visible': page.locator('#status-panel').is_visible(),
                             'snapshot_note': page.locator('#status-snapshot-note').inner_text(),
                             'non_file_requests': [x for x in requests if not x.startswith('file:')],
                             'progress_requests': [x for x in requests if 'progress.json' in x]}
    page.close()
    browser.close()
(UX / 'deep-checks.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf8')
print(json.dumps(result, indent=2, ensure_ascii=False))
