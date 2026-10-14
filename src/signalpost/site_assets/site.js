'use strict';
(() => {
  const records = window.SIGNALPOST_INDEX || [];
  const byId = new Map(records.map(r => [r.orgnr, r]));
  const fold = text => String(text ?? '').toLowerCase().replace(/ø/g,'o').replace(/æ/g,'ae').replace(/å/g,'a').normalize('NFD').replace(/[\u0300-\u036f]/g,'');
  const element = (tag, text, cls) => { const e = document.createElement(tag); if(text != null) e.textContent = text; if(cls) e.className = cls; return e; };
  const stateChip = state => element('span', String(state).replace(/_/g,' '), 'chip '+state);
  const format = value => value == null ? 'Unknown' : typeof value === 'number' ? value.toLocaleString('en-US',{maximumFractionDigits:20}) : String(value);
  const localData=window.SIGNALPOST_EVIDENCE || {sources:[],records:[],facts:[]};
  const evidence=new Map(localData.records.map(row=>{
    const e=Object.fromEntries(localData.source_fields.map((key,i)=>[key,localData.sources[row[0]][i]]));
    localData.evidence_fields.forEach((key,i)=>{e[key]=row[i+1];});return [e.id,e];
  }));
  const facts=new Map(localData.facts.map(f=>[f.id,f]));
  function sourceLink(raw){const a=element('a',raw);try{const url=new URL(raw);if(!/^https?:\/\//i.test(raw)||!['http:','https:'].includes(url.protocol)||url.username||url.password||/[\x00-\x1f]/.test(raw))return element('span',raw);a.href=url.href;a.target='_blank';a.rel='noopener noreferrer nofollow';return a;}catch{return element('span',raw);}}
  function showEvidence(panel){
    if(panel.dataset.loaded)return;
    const fact=facts.get(panel.dataset.source);if(!fact){panel.replaceChildren(element('p','Local source data could not be loaded.'));return;}
    panel.replaceChildren();
    for(const id of fact.evidence_ids){const e=evidence.get(id);if(!e)continue;const record=element('div',null,'evidence-record'),dl=element('dl',null,'values');
      const pair=(label,value)=>{dl.append(element('dt',label));const dd=element('dd');dd.append(value?.nodeType?value:element('span',value??'Not supplied'));dl.append(dd);};
      pair('Source / class',e.source_class);pair('Source link',sourceLink(e.source_url));pair('Registry identifier',e.source_identifier);pair('Retrieved at (UTC)',e.retrieved_at);
      const period=e.reporting_period||fact.reporting_period;
      pair('Effective / reporting date',e.effective_at||(period?JSON.stringify(period):'Unknown'));
      const hash=element('div'),code=element('code',e.content_sha256.slice(0,16)+'…');code.title=e.content_sha256;const copy=element('button','Copy full hash');copy.type='button';copy.dataset.copy=e.content_sha256;hash.append(code,copy);pair('SHA-256',hash);
      pair('Extraction method / version',e.extraction_method);pair('Locator',e.locator);if(fact.identity_level)pair('Website identity level',fact.identity_level);
      const quote=element('blockquote',null,'excerpt');const match=[...fact.values].sort((a,b)=>b.length-a.length).find(v=>v&&e.claim_span.includes(v));
      if(match){const at=e.claim_span.indexOf(match);quote.append(document.createTextNode(e.claim_span.slice(0,at)),element('mark',match),document.createTextNode(e.claim_span.slice(at+match.length)));}else quote.textContent=e.claim_span;
      record.append(dl,quote);panel.append(record);
    }
    panel.dataset.loaded='true';
  }
  document.addEventListener('click', async event => {
    const button = event.target.closest('button'); if(!button) return;
    if(button.dataset.toggle){const target=document.getElementById(button.dataset.toggle);if(target){if(target.dataset.source)showEvidence(target);target.hidden=!target.hidden;button.setAttribute('aria-expanded',String(!target.hidden));}}
    if(button.dataset.copy){
      try { await navigator.clipboard.writeText(button.dataset.copy); button.textContent='Copied'; }
      catch { const input=element('textarea');input.value=button.dataset.copy;input.setAttribute('aria-label','Select and copy this value');button.after(input);input.focus();input.select();try{document.execCommand('copy');}catch{} }
    }
  });
  // Additional official metadata shares the offline evidence payload. Build with
  // text nodes only, so source strings never become executable markup.
  for(const fact of localData.registry_details||[]){
    const root=document.querySelector('[data-registry-details="'+fact.group+'"]');if(!root)continue;
    const article=element('article',null,'fact');article.id='fact-'+fact.id;
    article.append(element('h3',fact.field),stateChip(fact.availability));
    article.append(element('pre',fact.value==null?'Unknown':JSON.stringify(fact.value,null,2)));
    const button=element('button','Source');button.type='button';button.dataset.toggle='source-'+fact.id;
    button.setAttribute('aria-expanded','false');button.setAttribute('aria-controls','source-'+fact.id);
    const panel=element('div',null,'evidence');panel.id='source-'+fact.id;panel.dataset.source=fact.id;panel.hidden=true;
    article.append(button,panel);root.append(article);
  }
  function revealFact(){const target=document.getElementById(location.hash.slice(1));if(!target)return;
    for(let parent=target.parentElement;parent;parent=parent.parentElement)if(parent.tagName==='DETAILS')parent.open=true;
  }
  window.addEventListener('hashchange',revealFact);revealFact();
  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    const savedTheme = localStorage.getItem('signalpost_theme');
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const currentTheme = savedTheme || (prefersDark ? 'dark' : 'light');
    document.documentElement.dataset.theme = currentTheme;
    themeToggle.textContent = currentTheme === 'dark' ? '☀️ Light' : '🌙 Dark';
    themeToggle.addEventListener('click', () => {
      const nextTheme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      document.documentElement.dataset.theme = nextTheme;
      localStorage.setItem('signalpost_theme', nextTheme);
      themeToggle.textContent = nextTheme === 'dark' ? '☀️ Light' : '🌙 Dark';
    });
  }
  if(document.body.dataset.page === 'index') {
    let pageNumber=0; const pageSize=30;
    for(const r of records){
      r._search = fold(r.name+' '+r.orgnr+' '+(r.municipality||'')+' '+(r.website||''));
      r.score = (r.claim_count||0)*10 + (r.website?20:0) + (r.jobs?20:0) + (r.social?10:0) + (r.activity?10:0);
    }
    const sortEl = document.getElementById('sort');
    const savedSort = sessionStorage.getItem('signalpost_sort');
    if (savedSort && sortEl && Array.from(sortEl.options).some(o => o.value === savedSort)) {
      sortEl.value = savedSort;
    }
    const controls=['search','municipality','division','sort','filter-website','filter-jobs','filter-social','filter-activity','filter-incomplete'];
    function draw(){
      const query=fold(document.getElementById('search').value);
      const selected=records.filter(r => {
        if(!r._search.includes(query)) return false;
        const town=document.getElementById('municipality').value, division=document.getElementById('division').value;
        if(town && r.municipality!==town || division && !(r.nace||'').startsWith(division)) return false;
        for(const key of ['website','jobs','social','activity']) if(document.getElementById('filter-'+key).checked && !r.flags[key]) return false;
        return !document.getElementById('filter-incomplete').checked || Object.values(r.sections).some(s => s==='failed'||s==='blocked');
      });
      const sort=document.getElementById('sort').value;
      selected.sort((a,b) => sort==='name' ? a.name.localeCompare(b.name,'nb')||a.orgnr.localeCompare(b.orgnr) : sort==='score' ? (b.score ?? -Infinity)-(a.score ?? -Infinity)||a.orgnr.localeCompare(b.orgnr) : (b[sort] ?? -Infinity)-(a[sort] ?? -Infinity)||a.orgnr.localeCompare(b.orgnr));
      const pages=Math.max(1,Math.ceil(selected.length/pageSize));pageNumber=Math.min(pageNumber,pages-1);
      const results=document.getElementById('results');results.replaceChildren();
      for(const r of selected.slice(pageNumber*pageSize,(pageNumber+1)*pageSize)){
        const card=element('article',null,'company'), heading=element('h2'), a=element('a',r.name);a.href='c/'+r.orgnr+'.html';heading.append(a);card.append(heading);
        card.append(element('p',r.orgnr+' · '+(r.municipality||'Unknown municipality')));
        card.append(element('p',r.industry_en||r.industry_no||'Industry unknown'));
        const badges=element('div',null,'badges');for(const [label,family] of [['identity','identity'],['accounts','accounts'],['people','roles'],['web','website'],['hiring','hiring'],['activity','activity']]){const state=r.sections[family]||'not_applicable';badges.append(element('span',label+': '+state.replace(/_/g,' '),'chip '+state));}card.append(badges);
        card.append(element('p','Revenue: '+format(r.revenue)+' · Employees: '+format(r.employees)));results.append(card);
      }
      document.getElementById('result-count').textContent=selected.length+' companies match';document.getElementById('page-label').textContent='Page '+(pageNumber+1)+' of '+pages;
      document.getElementById('previous').disabled=pageNumber===0;document.getElementById('next').disabled=pageNumber===pages-1;
    }
    for(const id of controls) {
      const el = document.getElementById(id);
      if(el) {
        el.addEventListener(id==='search'?'input':'change',()=>{
          if(id==='sort') sessionStorage.setItem('signalpost_sort', el.value);
          pageNumber=0;draw();
        });
      }
    }
    document.getElementById('previous').addEventListener('click',()=>{pageNumber--;draw();});document.getElementById('next').addEventListener('click',()=>{pageNumber++;draw();});draw();
  }
  if(document.body.dataset.page === 'compare'){
    const options=document.getElementById('company-options');for(const r of records){const option=element('option');option.value=r.orgnr;option.label=r.name;options.append(option);}
    const inputs=[0,1,2].map(i=>document.getElementById('company-'+i));
    const fields=[['name','Name','identity'],['orgnr','Organisation number','identity'],['municipality','Municipality','identity'],['industry','Industry','identity'],['employees','Employees','identity'],['revenue','Revenue','accounts'],['annual_result','Annual result','accounts'],['fiscal_year','Fiscal year','accounts'],['ceo','CEO','roles'],['chair','Chair','roles'],['auditor','Auditor','roles'],['workplaces','Workplaces count','subunits'],['website','Website','website'],['social','Social count','website'],['jobs','Active ads','hiring'],['activity','Activity items','activity'],['last_checked','Last checked','identity']];
    function draw(){
      const selected=[];for(const input of inputs){const r=byId.get(input.value.trim())||records.find(r=>fold(r.name)===fold(input.value.trim()));if(r&&!selected.includes(r))selected.push(r);}
      const root=document.getElementById('comparison');root.replaceChildren();document.getElementById('compare-status').textContent=selected.length<2?'Select at least two companies.':selected.length+' companies selected';
      for(const r of selected){const card=element('article',null,'compare-card');card.append(element('h2',r.name));for(const [key,label,family] of fields){const cell=element('div',null,'compare-cell');cell.append(element('strong',label));const state=r.sections[family]||'not_applicable';let value=key==='industry'?(r.industry_en||r.industry_no):r[key];if(['social','jobs','activity'].includes(key)&&state!=='available')value=null;const available=value!=null;cell.append(stateChip(available?'available':state==='available'?'not_available':state));const a=element('a',format(value));const fallback={industry:'what-it-does',fiscal_year:'financials',workplaces:'locations',social:'online',jobs:'hiring',activity:'activity',ceo:'people',chair:'people',auditor:'people'};a.href='c/'+r.orgnr+'.html#'+(r.anchors[key]||fallback[key]||'main');cell.append(a);card.append(cell);}root.append(card);}
      const hash=selected.map(r=>r.orgnr).join(',');if(location.hash.slice(1)!==hash)history.replaceState(null,'','#'+hash);
    }
    function fromHash(){const ids=location.hash.slice(1).split(',').slice(0,3);inputs.forEach((input,i)=>input.value=byId.has(ids[i])?ids[i]:'');draw();}
    for(const input of inputs)input.addEventListener('input',draw);window.addEventListener('hashchange',fromHash);fromHash();
  }
})();
