"""Focused keyboard, missing-value and focus checks for the offline audit."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

UX = Path(__file__).resolve().parents[1]
SITE = Path(os.environ.get('SIGNALPOST_AUDIT_SITE', str(UX / 'sample/site')))
cases = {'directory': 'index.html', 'profile': 'c/820042182.html', 'compare': 'compare.html?companies=923609016,820042182'}
result = {}
with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome', headless=True, args=['--allow-file-access-from-files'])
    for label, rel in cases.items():
        context = browser.new_context(viewport={'width': 375, 'height': 900})
        page = context.new_page()
        path, *query = rel.split('?', 1)
        url = (SITE / path).resolve().as_uri() + ('?' + query[0] if query else '')
        page.goto(url)
        focus = []
        for _ in range(10):
            page.keyboard.press('Tab')
            focus.append(page.evaluate('''() => {const e=document.activeElement,s=getComputedStyle(e);return {
                tag:e.tagName,text:(e.innerText||e.getAttribute('aria-label')||'').slice(0,60),
                outline_style:s.outlineStyle,outline_width:s.outlineWidth,box_shadow:s.boxShadow,
                visible:!!(e.getClientRects().length)}}'''))
        missing = page.evaluate('''() => [...document.querySelectorAll('.fact')].filter(e=>
            e.querySelector('.chip.not_available,.chip.failed,.chip.blocked,.chip.ambiguous,.chip.not_applicable'))
            .map(e=>({heading:e.querySelector('h3')?.innerText||'',text:e.innerText.slice(0,250)})).slice(0,15)''')
        compare_missing = page.evaluate('''() => [...document.querySelectorAll('.compare-cell')].filter(e=>
            e.querySelector('.chip.not_available,.chip.failed,.chip.blocked,.chip.ambiguous,.chip.not_applicable'))
            .map(e=>e.innerText.slice(0,140)).slice(0,15)''')
        small_targets = page.evaluate('''() => [...document.querySelectorAll('a[href],button,input,select,summary')]
            .filter(e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return r.width>0&&r.height>0&&s.visibility!=='hidden'})
            .map(e=>{const r=e.getBoundingClientRect();return {text:(e.innerText||e.getAttribute('aria-label')||'').slice(0,60),
                       width:Math.round(r.width),height:Math.round(r.height)}})
            .filter(e=>e.width<40||e.height<40).slice(0,25)''')
        result[label] = {'focus_sequence': focus, 'missing_examples': missing,
                         'compare_missing_examples': compare_missing,
                         'small_tap_targets': small_targets,
                         'unlabelled_visible_inputs': page.evaluate('''() => [...document.querySelectorAll('input,select')]
                             .filter(e=>e.getClientRects().length && !e.closest('label') &&
                               !e.getAttribute('aria-label') && !e.getAttribute('aria-labelledby')).map(e=>e.outerHTML.slice(0,150))''')}
        context.close()
    browser.close()
Path(os.environ.get('SIGNALPOST_A11Y_OUTPUT', str(UX / 'a11y-checks.json'))).write_text(
    json.dumps(result, indent=2, ensure_ascii=False), encoding='utf8')
print(json.dumps({k:{'focus':len(v['focus_sequence']), 'missing':len(v['missing_examples']),
                     'compare_missing':len(v['compare_missing_examples']),
                     'unlabelled':len(v['unlabelled_visible_inputs']),
                     'small_tap_targets':v['small_tap_targets']} for k,v in result.items()}))
