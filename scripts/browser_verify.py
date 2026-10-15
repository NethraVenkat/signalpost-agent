"""Localhost-only installed Chrome verification with an ephemeral profile.

uv run --with playwright python scripts/browser_verify.py --root out/remediation
Requires browser-site/ generated from the recorded 100-company output.
"""
import argparse
import csv
import io
import json
import threading
from datetime import datetime,timezone,timedelta
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from playwright.sync_api import sync_playwright,expect


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,required=True)
    args=parser.parse_args();root=args.root.resolve();out=root/'browser-results';out.mkdir(exist_ok=True)
    class Handler(SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
        def do_GET(self):
            if self.path=='/favicon.ico':self.send_response(204);self.end_headers();return
            super().do_GET()
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(root)))
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    origin=f'http://127.0.0.1:{server.server_port}';results=[];errors=[];console=[]
    def check(name,fn):
        try:fn();results.append({'check':name,'status':'PASS'})
        except Exception as e:results.append({'check':name,'status':'FAIL','error':str(e)[:700]})
        print(json.dumps(results[-1]),flush=True)
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True,
                args=['--disable-background-networking','--disable-extensions','--no-first-run'])
            context=browser.new_context(accept_downloads=True,viewport={'width':1280,'height':900})
            context.set_default_timeout(5000)
            context.route('**/*',lambda route:route.continue_() if route.request.url.startswith(origin+'/') else route.abort())
            page=context.new_page();page.on('pageerror',lambda error:errors.append(str(error)))
            page.on('console',lambda message:console.append({'message':message.text,'location':message.location}) if message.type=='error' else None)
            base=origin+'/browser-site/'
            page.goto(base+'index.html')
            check('dashboard_total',lambda:expect(page.locator('#dash-total-companies')).to_have_text('100'))
            page.screenshot(path=str(out/'desktop-dashboard.png'),full_page=True)
            page.locator('#tab-directory').click()
            check('pagination',lambda:(page.locator('#next').click(),expect(page.locator('#page-label')).to_contain_text('2')))
            def search():
                page.locator('#search').fill('812573942')
                expect(page.locator('#search-autocomplete')).to_be_visible()
                page.locator('#search').press('ArrowDown');page.locator('#search').press('Escape')
                expect(page.locator('#result-count')).to_contain_text('1 companies')
                expect(page.locator('#results')).to_contain_text('RØRLEGGER 1 MOLDE AS')
            check('search_autocomplete_correct_unicode',search)
            page.locator('#search').fill('')
            def filtered_scope():
                page.locator('#filter-website').check()
                expect(page.locator('#result-count')).to_contain_text('7 companies')
                page.locator('#tab-dashboard').click()
                expect(page.locator('#filter-scope-warning')).to_be_visible()
                expect(page.locator('#dash-total-companies')).to_have_text('7')
                page.locator('#tab-directory').click()
            check('website_filter_and_scope',filtered_scope)
            page.locator('#filter-website').uncheck()
            def exports():
                for selector,ext in [('#export-directory-json','json'),('#export-directory-csv','csv')]:
                    with page.expect_download() as info:page.locator(selector).click()
                    path=out/('directory.'+ext);info.value.save_as(path)
                    text=path.read_text(encoding='utf-8-sig')
                    if ext=='csv':
                        rows=list(csv.DictReader(io.StringIO(text)));assert len(rows)==100
                        assert 'Currency' in rows[0]
                        expected={r['orgnr']:r.get('currency') or '' for r in json.loads((out/'directory.json').read_text(encoding='utf8'))}
                        assert all(r['Currency']==expected[r['Organisation number']] for r in rows)
                    else:assert len(json.loads(text))==100
            check('csv_json_downloads_and_currency_column',exports)
            def watchlist():
                page.locator('[data-watchlist]').filter(visible=True).first.click()
                assert len(json.loads(page.evaluate("localStorage.getItem('signalpost_watchlist_v1')")))==1
                page.locator('#filter-watchlist').check();expect(page.locator('#result-count')).to_contain_text('1 companies')
                page.locator('#filter-watchlist').uncheck()
            check('watchlist',watchlist)
            def views():
                page.once('dialog',lambda dialog:dialog.accept('QA view'))
                page.locator('#save-current-view').click();expect(page.locator('.saved-view-load')).to_have_text('QA view')
                page.locator('.saved-view-load').click()
            check('saved_views',views)
            for label,width,height in [('tablet',768,1024),('mobile',375,812)]:
                page.set_viewport_size({'width':width,'height':height})
                check(label+'_directory_overflow',lambda:assert_no_overflow(page))
                page.screenshot(path=str(out/(label+'-directory.png')),full_page=True)
            page.set_viewport_size({'width':1280,'height':900});page.goto(base+'compare.html')
            check('comparison_and_autocomplete',lambda:(page.locator('#company-1').fill('812573942'),page.locator('#company-2').fill('964624046'),expect(page.locator('.compare-card')).to_have_count(2),expect(page.locator('#company-options option').first).to_be_attached()))
            page.goto(base+'c/964624046.html')
            def evidence():
                button=page.locator('[data-toggle^="source-"]').first;button.click()
                expect(button).to_have_attribute('aria-expanded','true')
                target=button.get_attribute('data-toggle');expect(page.locator('#'+target+' blockquote').first).to_be_visible()
                assert page.locator('#'+target+' a').first.get_attribute('href').startswith('https://')
                expect(page.locator('#evidence-explorer')).to_be_visible()
            check('profile_evidence_links',evidence)
            check('correct_description_text',lambda:expect(page.locator('body')).to_contain_text('På Stell'))
            check('themes_and_keyboard_focus',lambda:(page.locator('#theme-toggle').click(),page.keyboard.press('Tab'),assert_focus(page)))
            page.set_viewport_size({'width':375,'height':812})
            check('mobile_profile_overflow',lambda:assert_no_overflow(page))
            page.screenshot(path=str(out/'mobile-profile.png'))
            # Reload each state so terminal polling cannot mask a new scenario.
            for state in ['running','partial','failed','completed','stale','static','disconnected']:
                context.unroute('**/progress.json')
                now=datetime.now(timezone.utc)
                data={'schema_version':1,'run_id':'synthetic-browser-status','status':'running' if state in ['running','partial','stale','disconnected'] else state,
                    'heartbeat':(now-timedelta(seconds=60) if state=='stale' else now).isoformat(),'elapsed_seconds':20,
                    'companies':{'total':100,'successful':20,'failed':1 if state=='partial' else 0,'in_flight':79,'queued':0},'requests':{'measured':50,'limit':2000},'stages':[]}
                calls=[0]
                def status_route(route):
                    calls[0]+=1
                    if state=='static':route.fulfill(status=404,body='missing')
                    elif state=='disconnected' and calls[0]>1:route.abort()
                    else:route.fulfill(content_type='application/json',body=json.dumps(data))
                context.route('**/progress.json',status_route)
                page.goto(base+'index.html');page.locator('#status-toggle').click()
                def status_check():
                    badge='completed' if state=='static' else 'running' if state in ['partial','disconnected'] else state
                    expect(page.locator('#status-badge')).to_have_text(badge)
                    if state=='disconnected':expect(page.locator('#status-badge')).to_have_text('stale',timeout=7000)
                    if state=='partial':expect(page.locator('#status-counters')).to_contain_text('1Failed')
                check('progress_'+state,status_check)
                if state in {'running','stale','failed'}:page.screenshot(path=str(out/('progress-'+state+'.png')))
            denied=browser.new_context(viewport={'width':375,'height':812})
            denied.route('**/*',lambda route:route.continue_() if route.request.url.startswith(origin+'/') else route.abort())
            denied.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Denied','SecurityError')}})")
            dp=denied.new_page();dp.on('pageerror',lambda error:errors.append(str(error)))
            dp.goto(base+'index.html');dp.locator('#tab-directory').click()
            def denied_check():
                dp.locator('#search').fill('812573942');expect(dp.locator('#result-count')).to_contain_text('1 companies')
                dp.locator('[data-watchlist]').filter(visible=True).first.click()
                dp.once('dialog',lambda dialog:dialog.accept('Denied storage'));dp.locator('#save-current-view').click()
                dp.locator('#theme-toggle').click()
            check('denied_storage_keeps_ui_operational',denied_check)
            dp.screenshot(path=str(out/'denied-storage.png'),full_page=True)
            page.goto(origin+'/integration-site/c/923609016.html')
            def group():
                body=page.locator('body').inner_text()
                assert 'group' in body.lower()
                assert 'hello@zephyrsynthetic.no' in body
                assert 'sibling@zephyrsynthetic.no' not in body
            check('synthetic_group_subject_contact_scope',group)
            page.screenshot(path=str(out/'synthetic-group-profile.png'),full_page=True)
            browser.close()
    finally:server.shutdown();server.server_close()
    unexpected=[e for e in console if not e['location'].get('url','').endswith('progress.json')]
    report={'scope':'Installed Chrome headless; isolated ephemeral contexts; localhost only; historical100 site regenerated with current source; synthetic progress states',
        'checks':results,'page_errors':errors,'console_errors':console,'screenshots':[p.name for p in out.glob('*.png')]}
    report['unexpected_console_errors']=unexpected
    (out/'results.json').write_text(json.dumps(report,ensure_ascii=True,indent=2),encoding='utf8')
    print(json.dumps({'passed':sum(r['status']=='PASS' for r in results),'failed':[r for r in results if r['status']!='PASS'],'page_errors':errors}))
    if errors or unexpected or any(r['status']=='FAIL' for r in results):raise SystemExit(1)


def assert_no_overflow(page):
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')


def assert_focus(page):
    assert page.evaluate('document.activeElement !== document.body')


if __name__=='__main__':main()
