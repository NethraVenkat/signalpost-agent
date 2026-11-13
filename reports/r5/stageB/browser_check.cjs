/* Authored local QA; uses the installed Playwright package, no external app code. */
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const assert = require('node:assert/strict');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const root = path.resolve(process.argv[2] || 'docs/demo');
const out = path.resolve(process.argv[3] || 'reports/r5/stageU');
fs.mkdirSync(out, {recursive:true});
const server = http.createServer((req, res) => {
  const pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
  if(!pathname.startsWith('/signalpost-agent/')) {res.writeHead(404).end(); return;}
  const file = path.resolve(root, pathname.slice('/signalpost-agent/'.length) || 'index.html');
  if(!file.startsWith(root+path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {res.writeHead(404).end(); return;}
  res.setHeader('content-type', ({'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json'})[path.extname(file)] || 'application/octet-stream');
  fs.createReadStream(file).pipe(res);
});

async function inspect(page, label) {
  const result = await page.evaluate(() => {
    const badTargets = [...document.querySelectorAll('button,input,select,a[href],summary')].filter(e => {
      const r=e.getBoundingClientRect();
      return r.width && r.height && !e.closest('[hidden]') && !e.matches('.skip') && getComputedStyle(e).visibility!=='hidden' && (r.width<43.9 || r.height<43.9);
    }).map(e => ({tag:e.tagName,id:e.id,text:e.textContent.slice(0,60),width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height}));
    return {width:innerWidth, scrollWidth:document.documentElement.scrollWidth, badTargets};
  });
  assert.ok(result.scrollWidth <= result.width+1, label+': horizontal page overflow '+JSON.stringify(result));
  assert.deepEqual(result.badTargets, [], label+': targets below 44px');
  return {label,...result};
}

async function main() {
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const base='http://127.0.0.1:'+server.address().port+'/signalpost-agent/';
  const browser=await chromium.launch({headless:true});
  const results=[];
  try {
    for(const width of [1280,360]) {
      const label=width===1280?'desktop':'mobile';
      const context=await browser.newContext({viewport:{width,height:900},colorScheme:'light',reducedMotion:'reduce'});
      await context.route('**/*',route=>route.request().url().startsWith(base)?route.continue():route.abort());
      const page=await context.newPage(); const errors=[];
      page.on('pageerror',error=>errors.push(error.message));
      await page.goto(base,{waitUntil:'load'});
      results.push(await inspect(page,label+' dashboard'));
      await page.locator('#tab-directory').click();
      await page.locator('#search').fill('SPEDIFY');
      await page.waitForFunction(()=>document.querySelectorAll('#results .company').length===1);
      assert.match(await page.locator('#results').innerText(),/SPEDIFY/);
      await page.locator('#search').fill('926818317');
      await page.waitForFunction(()=>document.querySelectorAll('#results .company').length===1);
      results.push(await inspect(page,label+' search by name and number'));
      await page.screenshot({path:path.join(out,label+'-directory.png')});
      await page.locator('#results .company h2 a').click();
      await page.waitForSelector('.verification-hint');
      results.push(await inspect(page,label+' profile'));
      const expectedEvents=await page.evaluate(()=>window.SIGNALPOST_EVIDENCE.facts.filter(f=>f.field.startsWith('registry_change.')).length);
      const eventEntries=page.locator('#timeline .timeline-item').filter({has:page.locator('.timeline-meta .chip').filter({hasText:'Registry update'})});
      assert.ok(expectedEvents>0 && expectedEvents<=50);
      assert.equal(await eventEntries.count(),expectedEvents);
      const sourceJump=eventEntries.first().locator('a');
      const eventTarget=await sourceJump.getAttribute('href');
      await sourceJump.click();
      const eventCard=page.locator(eventTarget);
      const eventButton=eventCard.locator('button[data-toggle]').first();
      await eventButton.click();
      const eventPanel=page.locator('#'+await eventButton.getAttribute('aria-controls'));
      await eventPanel.waitFor({state:'visible'});
      const eventText=await eventPanel.innerText();
      assert.match(eventText,/[a-f0-9]{64}/);
      assert.ok(eventText.includes('Retrieved at (UTC)') && eventText.includes('Source link'));
      results.push(await inspect(page,label+' all retained registry events and source receipt'));
      await eventCard.screenshot({path:path.join(out,label+'-registry-event.png')});
      await eventButton.click();

      await page.locator('.verification-hint summary').click();
      assert.ok(await page.locator('.verification-hint p').isVisible());
      await page.locator('.verification-hint summary').click();
      await page.screenshot({path:path.join(out,label+'-profile.png')});
      const brief=await page.locator('.summary').innerText();
      for(const term of ['First run','What is unknown','Partner-screening takeaway','Derived']) assert.ok(brief.includes(term),term+' missing from visible briefing');
      const statusLink=page.locator('.summary a[aria-label^="Run-status citation"]').first();
      await statusLink.click();
      const statusTarget=page.locator(await statusLink.getAttribute('href'));
      await statusTarget.waitFor({state:'visible'});
      assert.ok((await statusTarget.innerText()).includes('Recorded by this run'));
      results.push(await inspect(page,label+' cited run observation'));
      await statusTarget.screenshot({path:path.join(out,label+'-run-observation.png')});
      await page.locator('.run-observations summary').click();

      const button=page.locator('button[data-toggle^="source-"]').first();
      const panelId=await button.getAttribute('aria-controls');
      await button.click();
      const panel=page.locator('#'+panelId);
      await panel.waitFor({state:'visible'});
      const text=await panel.innerText();
      for(const needed of ['Source link','Retrieved at (UTC)','SHA-256']) assert.ok(text.includes(needed),needed);
      assert.match(text,/[a-f0-9]{64}/);
      assert.ok((await panel.locator('.excerpt').innerText()).length>0);
      assert.match(await panel.locator('a').first().getAttribute('href'),/^https?:\/\//);
      results.push(await inspect(page,label+' source panel'));
      await panel.screenshot({path:path.join(out,label+'-source.png')});
      assert.ok(await page.locator('.fact-source').count()>0);
      if(await page.locator('#explorer-show-all').count()) {
        await page.locator('#explorer-show-all').click();
        results.push(await inspect(page,label+' all evidence rows'));
      }
      if(width===360) {
        await page.locator('.financial-table tbody tr').first().screenshot({path:path.join(out,'mobile-financial-row.png')});
        await page.locator('.evidence-explorer-table tbody tr').first().screenshot({path:path.join(out,'mobile-evidence-row.png')});
      }
      await page.goto(base+'compare.html');
      await page.locator('#company-0').fill('926818317');
      await page.locator('#company-1').fill('991853995');
      await page.waitForFunction(()=>document.querySelectorAll('.compare-card').length===2);
      results.push(await inspect(page,label+' two-company comparison'));
      await page.locator('#comparison').screenshot({path:path.join(out,label+'-compare.png')});
      assert.deepEqual(errors,[],label+' JavaScript errors');
      await context.close();
    }
    fs.writeFileSync(path.join(out,'browser_results.json'),JSON.stringify({browser:browser.version(),basePath:'/signalpost-agent/',results,externalRequestsAllowed:false},null,2)+'\n');
    console.log(JSON.stringify({checks:results.length,screenshots:14,browser:browser.version()}));
  } finally {await browser.close(); server.close();}
}
main().catch(error=>{console.error(error);server.close();process.exitCode=1;});
