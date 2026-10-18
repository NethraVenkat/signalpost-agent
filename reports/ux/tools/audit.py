"""Offline file:// screenshot and DOM audit. No application code is modified."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

UX = Path(__file__).resolve().parents[1]
SITE = Path(os.environ.get('SIGNALPOST_AUDIT_SITE', str(UX / 'sample/site')))
OUT = Path(os.environ.get('SIGNALPOST_SCREENSHOT_DIR', str(UX / 'screenshots/before')))
OUT.mkdir(parents=True, exist_ok=True)
selection = json.loads((UX / 'sample/selection.json').read_text(encoding='utf8'))['special_cases']
cases = {
    'directory': 'index.html',
    'equinor': 'c/923609016.html',
    'filmtek': 'c/988330752.html',
    'small': 'c/925181536.html',
    'near_empty': 'c/820042182.html',
    'registry_activity': 'c/932525070.html',
    'compare_2': 'compare.html?companies=923609016,988330752',
    'compare_4': 'compare.html?companies=923609016,988330752,932525070,929583027',
    'invalid_input': 'index.html#invalid-inputs',
}
widths = (1440, 375, 320)


def dom_metrics(page):
    return page.evaluate("""() => {
      const root=document.documentElement;
      const visible=e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&r.width>0&&r.height>0};
      const controls=[...document.querySelectorAll('a[href],button,input,select,summary')].filter(visible);
      const small=controls.map(e=>{const r=e.getBoundingClientRect();return {tag:e.tagName,text:(e.innerText||e.getAttribute('aria-label')||'').slice(0,50),width:Math.round(r.width),height:Math.round(r.height)}}).filter(x=>x.width<40||x.height<40);
      const labelled=[...document.querySelectorAll('input,select')].filter(visible).filter(e=>!e.closest('label')&&!e.getAttribute('aria-label')&&!e.getAttribute('aria-labelledby'));
      const parse=v=>{const m=v.match(/rgba?\\(([^)]+)\\)/);return m?m[1].split(',').slice(0,3).map(Number):null};
      const lumi=c=>{let a=c.map(v=>v/255).map(v=>v<=.04045?v/12.92:Math.pow((v+.055)/1.055,2.4));return .2126*a[0]+.7152*a[1]+.0722*a[2]};
      const contrast=[];
      for(const e of [...document.querySelectorAll('h1,h2,h3,p,a,button,label,td,th,span')].filter(visible).slice(0,300)){
        if(!(e.innerText||'').trim())continue;
        let fg=parse(getComputedStyle(e).color), node=e, bg=null;
        while(node&&!bg){const v=getComputedStyle(node).backgroundColor;if(v!=='transparent'&&!v.endsWith(', 0)')&&!v.endsWith(',0)'))bg=parse(v);node=node.parentElement}
        if(!fg||!bg)continue;
        let l1=lumi(fg),l2=lumi(bg),ratio=(Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05);
        if(ratio<4.5)contrast.push({tag:e.tagName,text:(e.innerText||'').trim().slice(0,50),ratio:+ratio.toFixed(2),color:getComputedStyle(e).color,background:getComputedStyle(e).backgroundColor});
      }
      return {client_width:root.clientWidth,scroll_width:root.scrollWidth,overflow:root.scrollWidth>root.clientWidth,
        tap_target_count:controls.length,small_tap_count:small.length,small_tap_examples:small.slice(0,25),
        contrast_sample_count:Math.min(300,[...document.querySelectorAll('h1,h2,h3,p,a,button,label,td,th,span')].filter(visible).length),
        low_contrast_count:contrast.length,low_contrast_examples:contrast.slice(0,25),
        header_count:document.querySelectorAll('header').length,nav_count:document.querySelectorAll('nav').length,main_count:document.querySelectorAll('main').length,
        unlabelled_inputs:labelled.map(e=>e.outerHTML.slice(0,160)),images_without_alt:[...document.images].filter(e=>!e.hasAttribute('alt')).length,
        fact_count:document.querySelectorAll('.fact').length,evidence_button_count:document.querySelectorAll('button[data-toggle]').length,
        state_badge_count:document.querySelectorAll('.chip.available,.chip.not_available,.chip.not_applicable,.chip.failed,.chip.blocked,.chip.ambiguous').length,
        registry_label_exact:document.body.innerText.includes('registry publication time (not effective date)'),
        registry_label_casefold:document.body.innerText.toLowerCase().includes('registry publication time'),
        unknown_block:document.body.innerText.includes("What we don't know"),
        body_excerpt:document.body.innerText.slice(0,500)};
    }""")


def search_checks(page):
    result = {}
    try:
        page.locator('#global-search-open').click(timeout=3000)
        inp = page.locator('#global-search-input')
        for key, query in [('name', 'Equinor'), ('org', '923609016')]:
            inp.fill(query)
            result[key] = page.locator('#global-search-results a').all_inner_texts()
        page.keyboard.press('Escape')
        page.keyboard.press('/')
        result['slash_opens'] = page.locator('#global-search-dialog').evaluate('(e)=>e.open')
        page.keyboard.press('Escape')
        page.keyboard.press('Control+k')
        result['ctrl_k_opens'] = page.locator('#global-search-dialog').evaluate('(e)=>e.open')
        page.keyboard.press('Escape')
    except Exception as exc:
        result['error'] = str(exc)[:300]
    return result


def evidence_check(page):
    try:
        button = page.locator('button[data-toggle^="source-"]:visible').first
        if not button.count():return {'available': False}
        target = button.get_attribute('data-toggle')
        button.click(timeout=3000)
        panel = page.locator('[id="'+target+'"]')
        body = panel.inner_text(timeout=3000)
        return {'available': True, 'opened': not panel.get_attribute('hidden'), 'source': 'Source link' in body,
                'retrieval': 'Retrieved at (UTC)' in body, 'method': 'Extraction method / version' in body,
                'hash': 'SHA-256' in body, 'quote': bool(panel.locator('blockquote').count()),
                'excerpt': body[:350]}
    except Exception as exc:
        return {'available': True, 'error': str(exc)[:300]}


results = {'site': str(SITE), 'browser': 'Playwright Chrome, file://, all non-file requests aborted',
           'selection': selection, 'pages': {}, 'interactions': {}}
with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome', headless=True, args=['--allow-file-access-from-files'])
    for key, relative in cases.items():
        results['pages'][key] = {}
        for width in widths:
            context = browser.new_context(viewport={'width': width, 'height': 900}, device_scale_factor=1)
            page = context.new_page()
            errors = {'console': [], 'pageerror': [], 'requestfailed': [], 'blocked_external': []}
            page.on('console', lambda m: errors['console'].append(m.text) if m.type == 'error' else None)
            page.on('pageerror', lambda e: errors['pageerror'].append(str(e)))
            page.on('requestfailed', lambda r: errors['requestfailed'].append({'url': r.url, 'failure': r.failure}))

            def route_request(route):
                if route.request.url.startswith('file://'):
                    route.continue_()
                else:
                    errors['blocked_external'].append(route.request.url)
                    route.abort()
            page.route('**/*', route_request)
            path, *suffix = relative.split('?', 1)
            if '#' in path:
                path, fragment = path.split('#', 1)
                url = (SITE / path).resolve().as_uri() + '#' + fragment
            else:
                url = (SITE / path).resolve().as_uri()
            if suffix: url += '?' + suffix[0]
            entry = {'url': url, 'screenshot': str((OUT / f'{key}_{width}.png').relative_to(UX)), 'load_error': None}
            try:
                page.goto(url, wait_until='load', timeout=15000)
                page.wait_for_timeout(250)
                page.screenshot(path=str(OUT / f'{key}_{width}.png'), full_page=True, timeout=20000)
                entry['dom'] = dom_metrics(page)
                if width == 1440:
                    results['interactions'][key] = {'search': search_checks(page), 'evidence': evidence_check(page)}
                    if key == 'directory':
                        page.locator('#tab-directory').click()
                        page.locator('#sort').select_option('name')
                        before = page.locator('#result-count').inner_text()
                        page.locator('#area-filter').select_option('all')
                        results['interactions'][key]['directory'] = {
                            'sort_name_selected': page.locator('#sort').input_value(),
                            'all_five_selected': page.locator('#area-filter').input_value(),
                            'result_before': before, 'result_after': page.locator('#result-count').inner_text()}
                    if key.startswith('compare_'):
                        first = page.locator('.compare-card').count()
                        page.reload(wait_until='load')
                        results['interactions'][key]['compare'] = {'cards': first,
                            'cards_after_reload': page.locator('.compare-card').count(),
                            'input_count': page.locator('input[id^="company-"]').count(),
                            'url': page.url}
            except Exception as exc:
                entry['load_error'] = str(exc)[:500]
            entry['errors'] = errors
            results['pages'][key][str(width)] = entry
            context.close()
    browser.close()
Path(os.environ.get('SIGNALPOST_DOM_OUTPUT', str(UX / 'dom-audit.json'))).write_text(
    json.dumps(results, indent=2, ensure_ascii=False), encoding='utf8')
print(json.dumps({'screenshots': sum(len(v) for v in results['pages'].values()),
                  'load_failures': [(k,w) for k,v in results['pages'].items() for w,e in v.items() if e['load_error']],
                  'console_errors': sum(len(e['errors']['console']) for v in results['pages'].values() for e in v.values()),
                  'mobile_overflow': [(k,w) for k,v in results['pages'].items() for w,e in v.items()
                                      if e.get('dom',{}).get('overflow') and w!='1440']}))
