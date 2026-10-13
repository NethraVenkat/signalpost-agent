'use strict';
(() => {
  const records = window.SIGNALPOST_INDEX || [];
  const byId = new Map(records.map(r => [r.orgnr, r]));
  const fold = text => String(text ?? '').toLowerCase().replace(/ø/g,'o').replace(/æ/g,'ae').replace(/å/g,'a').normalize('NFD').replace(/[\u0300-\u036f]/g,'');
  const element = (tag, text, cls) => { const e = document.createElement(tag); if(text != null) e.textContent = text; if(cls) e.className = cls; return e; };
  const stateChip = state => element('span', String(state).replace(/_/g,' '), 'chip '+state);
  const format = value => value == null ? 'Unknown' : typeof value === 'number' ? value.toLocaleString('en-US',{maximumFractionDigits:20}) : String(value);
  document.addEventListener('click', async event => {
    const button = event.target.closest('button'); if(!button) return;
    if(button.dataset.toggle){const target=document.getElementById(button.dataset.toggle);if(target){target.hidden=!target.hidden;button.setAttribute('aria-expanded',String(!target.hidden));}}
    if(button.dataset.copy){
      try { await navigator.clipboard.writeText(button.dataset.copy); button.textContent='Copied'; }
      catch { const input=element('textarea');input.value=button.dataset.copy;input.setAttribute('aria-label','Select and copy this value');button.after(input);input.focus();input.select();try{document.execCommand('copy');}catch{} }
    }
  });
  if(document.body.dataset.page === 'index') {
    let pageNumber=0; const pageSize=30;
    const controls=['search','municipality','division','sort','filter-website','filter-jobs','filter-social','filter-activity','filter-incomplete'];
    function draw(){
      const query=fold(document.getElementById('search').value);
      const selected=records.filter(r => {
        if(!fold(r.name+' '+r.orgnr+' '+(r.municipality||'')).includes(query)) return false;
        const town=document.getElementById('municipality').value, division=document.getElementById('division').value;
        if(town && r.municipality!==town || division && !(r.nace||'').startsWith(division)) return false;
        for(const key of ['website','jobs','social','activity']) if(document.getElementById('filter-'+key).checked && !r.flags[key]) return false;
        return !document.getElementById('filter-incomplete').checked || Object.values(r.sections).some(s => s==='failed'||s==='blocked');
      });
      const sort=document.getElementById('sort').value;
      selected.sort((a,b) => sort==='name' ? a.name.localeCompare(b.name,'nb')||a.orgnr.localeCompare(b.orgnr) : (b[sort] ?? -Infinity)-(a[sort] ?? -Infinity)||a.orgnr.localeCompare(b.orgnr));
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
    for(const id of controls) document.getElementById(id).addEventListener(id==='search'?'input':'change',()=>{pageNumber=0;draw();});
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
