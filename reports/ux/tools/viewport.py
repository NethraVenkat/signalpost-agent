"""Capture readable first-viewport supplements to the full-page audit shots."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ux = Path(__file__).resolve().parents[1]
site = ux / 'sample/site'
with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome', headless=True, args=['--allow-file-access-from-files'])
    for name, rel in [('equinor', 'c/923609016.html'), ('near_empty', 'c/820042182.html'),
                      ('registry_activity', 'c/932525070.html'), ('compare_4', 'compare.html?companies=923609016,988330752,932525070,929583027')]:
        context = browser.new_context(viewport={'width': 375, 'height': 900})
        page = context.new_page()
        path, *query = rel.split('?', 1)
        page.goto((site / path).resolve().as_uri() + ('?' + query[0] if query else ''))
        page.screenshot(path=str(ux / 'screenshots/before' / f'{name}_viewport_375.png'))
        context.close()
    browser.close()
