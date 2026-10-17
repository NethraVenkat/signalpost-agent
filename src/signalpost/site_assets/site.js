'use strict';
(() => {
  const records = window.SIGNALPOST_INDEX || [];
  const byId = new Map(records.map(r => [r.orgnr, r]));
  const fold = text => String(text ?? '').toLowerCase().replace(/ø/g,'o').replace(/æ/g,'ae').replace(/å/g,'a').normalize('NFD').replace(/[\u0300-\u036f]/g,'');
  const element = (tag, text, cls) => { const e = document.createElement(tag); if(text != null) e.textContent = text; if(cls) e.className = cls; return e; };
  const stateChip = state => element('span', String(state).replace(/_/g,' '), 'chip '+state);
  const format = value => value == null ? 'Unknown' : typeof value === 'number' ? value.toLocaleString('en-US',{maximumFractionDigits:20}) : String(value);

  const sanitizeCsvCell = value => {
    if (value == null) return '';
    if (typeof value === 'boolean') return value ? 'Yes' : 'No';
    if (typeof value === 'number') return String(value);
    let s = typeof value === 'object' ? JSON.stringify(value) : String(value);
    if (/^-?\d+(?:\.\d+)?$/.test(s.trim())) return s.trim();
    const stripped = s.replace(/^[\s\x00-\x1f\x7f-\x9f\u200b-\u200d\u2060\ufeff]+/, '');
    if (stripped && ['=', '+', '-', '@'].includes(stripped[0])) s = "'" + s;
    else if (s && (s.charCodeAt(0) < 32 || (s.charCodeAt(0) >= 127 && s.charCodeAt(0) <= 159))) s = "'" + s;
    if (/[,"\n\r]/.test(s)) s = '"' + s.replace(/"/g, '""') + '"';
    return s;
  };

  const formatCsvOrgnr = orgnr => String(orgnr ?? '').trim();

  function downloadFile(filename, content, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  // Watchlist & Saved Views Storage
  const WATCHLIST_KEY = 'signalpost_watchlist_v1';
  const SAVED_VIEWS_KEY = 'signalpost_saved_views_v1';

  function getWatchlist() {
    try {
      const data = localStorage.getItem(WATCHLIST_KEY);
      return new Set(data ? JSON.parse(data) : []);
    } catch {
      return new Set();
    }
  }

  function saveWatchlist(set) {
    try {
      localStorage.setItem(WATCHLIST_KEY, JSON.stringify([...set]));
    } catch {}
  }

  function toggleWatchlist(orgnr) {
    const list = getWatchlist();
    if (list.has(orgnr)) list.delete(orgnr);
    else list.add(orgnr);
    saveWatchlist(list);
    updateWatchlistUI();
    return list.has(orgnr);
  }

  function updateWatchlistUI() {
    const list = getWatchlist();
    const countEl = document.getElementById('watchlist-count');
    if (countEl) countEl.textContent = String(list.size);
    document.querySelectorAll('[data-watchlist]').forEach(btn => {
      const org = btn.dataset.watchlist;
      const active = list.has(org);
      btn.classList.toggle('active', active);
      if (btn.classList.contains('btn-watchlist')) {
        btn.textContent = active ? '★ In Watchlist' : '⭐ Add to Watchlist';
      }
      if (btn.classList.contains('btn-watchlist-card')) {
        btn.textContent = active ? '★' : '☆';
        btn.setAttribute('aria-label', (active ? 'Remove ' : 'Add ') + 'watchlist');
      }
    });
  }

  document.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-watchlist]');
    if (btn) {
      const org = btn.dataset.watchlist;
      if (org) {
        toggleWatchlist(org);
        if (typeof window._triggerDraw === 'function') {
          window._triggerDraw();
        }
      }
    }
  });

  // Evidence panel support
  const localData = window.SIGNALPOST_EVIDENCE || {sources:[],records:[],facts:[]};
  const evidence = new Map(localData.records.map(row => {
    const e = Object.fromEntries(localData.source_fields.map((key,i) => [key, localData.sources[row[0]][i]]));
    localData.evidence_fields.forEach((key,i) => { e[key] = row[i+1]; });
    return [e.id, e];
  }));
  const facts = new Map(localData.facts.map(f => [f.id, f]));

  function sourceLink(raw) {
    const a = element('a', raw);
    try {
      const url = new URL(raw);
      if(!/^https?:\/\//i.test(raw) || !['http:','https:'].includes(url.protocol) || url.username || url.password || /[\x00-\x1f]/.test(raw)) {
        return element('span', raw);
      }
      a.href = url.href;
      a.target = '_blank';
      a.rel = 'noopener noreferrer nofollow';
      return a;
    } catch {
      return element('span', raw);
    }
  }

  function showEvidence(panel) {
    if(panel.dataset.loaded) return;
    const fact = facts.get(panel.dataset.source);
    if(!fact) {
      panel.replaceChildren(element('p', 'Local source data could not be loaded.'));
      return;
    }
    panel.replaceChildren();
    for(const id of fact.evidence_ids) {
      const e = evidence.get(id);
      if(!e) continue;
      const record = element('div', null, 'evidence-record');
      const dl = element('dl', null, 'values');
      const pair = (label, value) => {
        dl.append(element('dt', label));
        const dd = element('dd');
        dd.append(value?.nodeType ? value : element('span', value ?? 'Not supplied'));
        dl.append(dd);
      };
      pair('Source / class', e.source_class);
      pair('Source link', sourceLink(e.source_url));
      pair('Registry identifier', e.source_identifier);
      pair('Retrieved at (UTC)', e.retrieved_at);
      const period = e.reporting_period || fact.reporting_period;
      pair('Effective / reporting date', e.effective_at || (period ? JSON.stringify(period) : 'Unknown'));
      const hash = element('div');
      const code = element('code', e.content_sha256.slice(0, 16) + '…');
      code.title = e.content_sha256;
      const copy = element('button', 'Copy full hash');
      copy.type = 'button';
      copy.dataset.copy = e.content_sha256;
      hash.append(code, copy);
      pair('SHA-256', hash);
      pair('Extraction method / version', e.extraction_method);
      pair('Locator', e.locator);
      if(fact.identity_level) pair('Website identity level', fact.identity_level);
      const quote = element('blockquote', null, 'excerpt');
      const match = [...fact.values].sort((a,b) => b.length - a.length).find(v => v && e.claim_span.includes(v));
      if(match) {
        const at = e.claim_span.indexOf(match);
        quote.append(document.createTextNode(e.claim_span.slice(0, at)), element('mark', match), document.createTextNode(e.claim_span.slice(at + match.length)));
      } else {
        quote.textContent = e.claim_span;
      }
      record.append(dl, quote);
      panel.append(record);
    }
    panel.dataset.loaded = 'true';
  }

  document.addEventListener('click', async event => {
    const button = event.target.closest('button');
    if(!button) return;
    if(button.dataset.toggle) {
      const target = document.getElementById(button.dataset.toggle);
      if(target) {
        if(target.dataset.source) showEvidence(target);
        target.hidden = !target.hidden;
        button.setAttribute('aria-expanded', String(!target.hidden));
      }
    }
    if(button.dataset.copy) {
      try {
        await navigator.clipboard.writeText(button.dataset.copy);
        button.textContent = 'Copied';
      } catch {
        const input = element('textarea');
        input.value = button.dataset.copy;
        input.setAttribute('aria-label', 'Select and copy this value');
        button.after(input);
        input.focus();
        input.select();
        try { document.execCommand('copy'); } catch {}
      }
    }
  });

  // Additional official metadata
  for(const fact of localData.registry_details || []) {
    const root = document.querySelector('[data-registry-details="'+fact.group+'"]');
    if(!root) continue;
    const article = element('article', null, 'fact');
    article.id = 'fact-' + fact.id;
    article.append(element('h3', fact.field), stateChip(fact.availability));
    article.append(element('pre', fact.value == null ? 'Unknown' : JSON.stringify(fact.value, null, 2)));
    const button = element('button', 'Source');
    button.type = 'button';
    button.dataset.toggle = 'source-' + fact.id;
    button.setAttribute('aria-expanded', 'false');
    button.setAttribute('aria-controls', 'source-' + fact.id);
    const panel = element('div', null, 'evidence');
    panel.id = 'source-' + fact.id;
    panel.dataset.source = fact.id;
    panel.hidden = true;
    article.append(button, panel);
    root.append(article);
  }

  function revealFact() {
    const target = document.getElementById(location.hash.slice(1));
    if(!target) return;
    for(let parent = target.parentElement; parent; parent = parent.parentElement) {
      if(parent.tagName === 'DETAILS') parent.open = true;
    }
    if(target.scrollIntoView) target.scrollIntoView();
  }
  window.addEventListener('hashchange', revealFact);
  revealFact();

  // Theme toggle
  const themeToggle = document.getElementById('theme-toggle');
  if(themeToggle) {
    let savedTheme = null;
    try { savedTheme = localStorage.getItem('signalpost_theme'); } catch {}
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const currentTheme = savedTheme || (prefersDark ? 'dark' : 'light');
    document.documentElement.dataset.theme = currentTheme;
    themeToggle.textContent = currentTheme === 'dark' ? '☀️ Light' : '🌙 Dark';
    themeToggle.addEventListener('click', () => {
      const nextTheme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      document.documentElement.dataset.theme = nextTheme;
      try { localStorage.setItem('signalpost_theme', nextTheme); } catch {}
      themeToggle.textContent = nextTheme === 'dark' ? '☀️ Light' : '🌙 Dark';
    });
  }

  // Pre-process indexed records
  for(const r of records) {
    r._search = fold(r.name + ' ' + r.orgnr + ' ' + (r.municipality || '') + ' ' + (r.website || ''));
    r.score = (r.claim_count || 0) * 10 + (r.website ? 20 : 0) + (r.jobs ? 20 : 0) + (r.social ? 10 : 0) + (r.activity ? 10 : 0);
  }

  // ==========================================
  // PAGE: INDEX (Dashboard & Directory)
  // ==========================================
  if(document.body.dataset.page === 'index') {
    let pageNumber = 0;
    const pageSize = 30;
    let searchSequence = 0;
    let currentSelectedRecords = records;

    // View tab elements
    const tabDash = document.getElementById('tab-dashboard');
    const tabDir = document.getElementById('tab-directory');
    const tabHiring = document.getElementById('tab-hiring');
    const viewDash = document.getElementById('view-dashboard');
    const viewDir = document.getElementById('view-directory');
    const viewHiring = document.getElementById('view-hiring');

    function switchView(viewName) {
      const isDash = viewName === 'dashboard';
      const isDir = viewName === 'directory';
      const isHiring = viewName === 'hiring';
      if(tabDash && tabDir && viewDash && viewDir) {
        tabDash.classList.toggle('active', isDash);
        tabDash.setAttribute('aria-selected', String(isDash));
        tabDir.classList.toggle('active', isDir);
        tabDir.setAttribute('aria-selected', String(isDir));
        if (tabHiring) {
          tabHiring.classList.toggle('active', isHiring);
          tabHiring.setAttribute('aria-selected', String(isHiring));
        }
        viewDash.hidden = !isDash;
        viewDir.hidden = !isDir;
        if (viewHiring) viewHiring.hidden = !isHiring;
      }
      if (isHiring && typeof renderHiringExplorer === 'function') {
        renderHiringExplorer();
      }
    }

    if(tabDash && tabDir) {
      tabDash.addEventListener('click', () => {
        switchView('dashboard');
        updateQueryParams({ view: 'dashboard' });
      });
      tabDir.addEventListener('click', () => {
        switchView('directory');
        updateQueryParams({ view: 'directory' });
      });
    }
    if(tabHiring) {
      tabHiring.addEventListener('click', () => {
        switchView('hiring');
        updateQueryParams({ view: 'hiring' });
      });
    }

    // Filter controls
    const searchInput = document.getElementById('search');
    const autocompleteBox = document.getElementById('search-autocomplete');
    const muniSelect = document.getElementById('municipality');
    const divSelect = document.getElementById('division');
    const sizeSelect = document.getElementById('size-band');
    const sortSelect = document.getElementById('sort');
    const filterWeb = document.getElementById('filter-website');
    const filterJobs = document.getElementById('filter-jobs');
    const filterSocial = document.getElementById('filter-social');
    const filterAct = document.getElementById('filter-activity');
    const filterInc = document.getElementById('filter-incomplete');
    const filterWatchlist = document.getElementById('filter-watchlist');
    const activeFiltersBar = document.getElementById('active-filters-bar');
    const activeFiltersContainer = document.getElementById('active-filter-chips');
    const clearFiltersBtn = document.getElementById('clear-filters');
    const resetEmptyBtn = document.getElementById('reset-empty-filters');
    const resetDashBtn = document.getElementById('reset-dashboard-filters');
    const emptyResultsBox = document.getElementById('empty-results');

    // Dashboard widgets
    const scopeCountEl = document.getElementById('filter-scope-count');
    const scopeWarningEl = document.getElementById('filter-scope-warning');
    const dashTotalComp = document.getElementById('dash-total-companies');
    const dashTotalWeb = document.getElementById('dash-total-websites');
    const dashWebPct = document.getElementById('dash-websites-pct');
    const dashTotalJobs = document.getElementById('dash-total-jobs');
    const dashHiringComp = document.getElementById('dash-hiring-companies');
    const dashTotalAct = document.getElementById('dash-total-activity');
    const dashActPct = document.getElementById('dash-activity-pct');
    const provBox = document.getElementById('provenance-breakdown');
    const hiringBox = document.getElementById('hiring-timeline');
    const actBox = document.getElementById('recent-activity-list');

    // Read URL params
    const initialParams = new URLSearchParams(window.location.search);
    if(initialParams.get('q') && searchInput) searchInput.value = initialParams.get('q');
    if(initialParams.get('municipality') && muniSelect) muniSelect.value = initialParams.get('municipality');
    if(initialParams.get('division') && divSelect) divSelect.value = initialParams.get('division');
    if(initialParams.get('size') && sizeSelect) sizeSelect.value = initialParams.get('size');
    if(initialParams.get('sort') && sortSelect) sortSelect.value = initialParams.get('sort');
    if(initialParams.get('web') === '1' && filterWeb) filterWeb.checked = true;
    if(initialParams.get('jobs') === '1' && filterJobs) filterJobs.checked = true;
    if(initialParams.get('social') === '1' && filterSocial) filterSocial.checked = true;
    if(initialParams.get('activity') === '1' && filterAct) filterAct.checked = true;
    if(initialParams.get('incomplete') === '1' && filterInc) filterInc.checked = true;

    // View initialization
    const reqView = initialParams.get('view') || (window.location.hash === '#directory' ? 'directory' : 'dashboard');
    switchView(reqView);

    function updateQueryParams(overrides = {}) {
      const params = new URLSearchParams(window.location.search);
      if(searchInput?.value.trim()) params.set('q', searchInput.value.trim()); else params.delete('q');
      if(muniSelect?.value) params.set('municipality', muniSelect.value); else params.delete('municipality');
      if(divSelect?.value) params.set('division', divSelect.value); else params.delete('division');
      if(sizeSelect?.value) params.set('size', sizeSelect.value); else params.delete('size');
      if(sortSelect?.value && sortSelect.value !== 'claim_count') params.set('sort', sortSelect.value); else params.delete('sort');
      if(filterWeb?.checked) params.set('web', '1'); else params.delete('web');
      if(filterJobs?.checked) params.set('jobs', '1'); else params.delete('jobs');
      if(filterSocial?.checked) params.set('social', '1'); else params.delete('social');
      if(filterAct?.checked) params.set('activity', '1'); else params.delete('activity');
      if(filterInc?.checked) params.set('incomplete', '1'); else params.delete('incomplete');
      for(const [k, v] of Object.entries(overrides)) {
        if(v == null) params.delete(k); else params.set(k, v);
      }
      const newQuery = params.toString();
      const newUrl = window.location.pathname + (newQuery ? '?' + newQuery : '') + window.location.hash;
      window.history.replaceState(null, '', newUrl);
    }

    function clearAllFilters() {
      if(searchInput) searchInput.value = '';
      if(muniSelect) muniSelect.value = '';
      if(divSelect) divSelect.value = '';
      if(sizeSelect) sizeSelect.value = '';
      if(filterWeb) filterWeb.checked = false;
      if(filterJobs) filterJobs.checked = false;
      if(filterSocial) filterSocial.checked = false;
      if(filterAct) filterAct.checked = false;
      if(filterInc) filterInc.checked = false;
      if(filterWatchlist) filterWatchlist.checked = false;
      pageNumber = 0;
      updateQueryParams();
      draw();
    }

    if(clearFiltersBtn) clearFiltersBtn.addEventListener('click', clearAllFilters);
    if(resetEmptyBtn) resetEmptyBtn.addEventListener('click', clearAllFilters);
    if(resetDashBtn) resetDashBtn.addEventListener('click', clearAllFilters);

    function renderDashboard(selected, isFiltered) {
      const total = selected.length;
      const fullCount = records.length;
      if(scopeWarningEl && scopeCountEl) {
        scopeWarningEl.hidden = !isFiltered;
        scopeCountEl.textContent = total.toLocaleString('en-US');
      }

      // Summary KPI card values
      if(dashTotalComp) dashTotalComp.textContent = total.toLocaleString('en-US');
      const webCount = selected.filter(r => r.flags.website).length;
      if(dashTotalWeb) dashTotalWeb.textContent = webCount.toLocaleString('en-US');
      if(dashWebPct) dashWebPct.textContent = (total ? (webCount / total * 100).toFixed(1) : '0.0') + '%';

      const jobCount = selected.reduce((acc, r) => acc + (r.jobs || 0), 0);
      const hiringCompCount = selected.filter(r => r.flags.jobs).length;
      if(dashTotalJobs) dashTotalJobs.textContent = jobCount.toLocaleString('en-US');
      if(dashHiringComp) dashHiringComp.textContent = hiringCompCount + (hiringCompCount === 1 ? ' company' : ' companies');

      const actCount = selected.filter(r => r.flags.activity).length;
      if(dashTotalAct) dashTotalAct.textContent = actCount.toLocaleString('en-US');
      if(dashActPct) dashActPct.textContent = (total ? (actCount / total * 100).toFixed(1) : '0.0') + '%';

      // Provenance categories breakdown
      if(provBox) {
        provBox.replaceChildren();
        const provCounts = { registry_website: 0, legal_name_slug: 0, search_brave: 0, registry_email: 0, other: 0 };
        for(const r of selected) {
          if(r.website) {
            const org = r.website_origin;
            if(org in provCounts) provCounts[org]++;
            else if(org) provCounts.other++;
            else provCounts.registry_website++;
          }
        }
        const provLabels = {
          registry_website: 'Official Registry Declared (Enhetsregisteret)',
          legal_name_slug: 'Derived Domain from Legal Name',
          search_brave: 'Corroborated External Search (Brave API/Mock)',
          registry_email: 'Registry Contact Email Domain',
          other: 'Other Corroborated Source'
        };
        const activeProv = Object.entries(provCounts).filter(([_, count]) => count > 0);
        if(!activeProv.length) {
          provBox.append(element('p', 'No verified websites in current filter scope.', 'muted'));
        } else {
          for(const [key, count] of activeProv) {
            const row = element('div', null, 'provenance-row');
            const labels = element('div', null, 'provenance-labels');
            labels.append(element('span', provLabels[key] || key));
            const pct = webCount ? ((count / webCount) * 100).toFixed(1) : '0.0';
            labels.append(element('span', count + ' (' + pct + '%)', 'provenance-meta'));
            const barBg = element('div', null, 'provenance-bar-bg');
            const barFill = element('div', null, 'provenance-bar-fill');
            barFill.style.width = pct + '%';
            barBg.append(barFill);
            row.append(labels, barBg);
            provBox.append(row);
          }
        }
      }

      // Hiring timeline chart
      if(hiringBox) {
        hiringBox.replaceChildren();
        const monthCounts = {};
        for(const r of selected) {
          if(r.job_dates && r.job_dates.length) {
            for(const d of r.job_dates) {
              const month = String(d).slice(0, 7);
              monthCounts[month] = (monthCounts[month] || 0) + 1;
            }
          }
        }
        const months = Object.keys(monthCounts).sort();
        if(!months.length) {
          hiringBox.append(element('p', 'No active job postings recalled in current scope.', 'muted'));
        } else {
          const maxVal = Math.max(...Object.values(monthCounts), 1);
          for(const m of months) {
            const count = monthCounts[m];
            const row = element('div', null, 'timeline-chart-row');
            row.append(element('span', m, 'timeline-bar-label'));
            const barBg = element('div', null, 'timeline-bar-bg');
            const barFill = element('div', null, 'timeline-bar-fill');
            barFill.style.width = ((count / maxVal) * 100).toFixed(1) + '%';
            barBg.append(barFill);
            row.append(barBg, element('span', count + (count === 1 ? ' job' : ' jobs'), 'timeline-bar-val'));
            hiringBox.append(row);
          }
        }
      }

      // Recent verified activity list
      if(actBox) {
        actBox.replaceChildren();
        const recentEvents = [];
        for(const r of selected) {
          if(r.recent_events && r.recent_events.length) {
            for(const ev of r.recent_events) {
              recentEvents.push({ orgnr: r.orgnr, name: r.name, date: ev.date, label: ev.label, anchor: ev.anchor });
            }
          }
        }
        recentEvents.sort((a,b) => (b.date || '').localeCompare(a.date || ''));
        const slice = recentEvents.slice(0, 8);
        if(!slice.length) {
          actBox.append(element('p', 'No recent verified registry filings within 2-year window for current selection.', 'muted'));
        } else {
          for(const ev of slice) {
            const row = element('div', null, 'activity-row');
            const main = element('div', null, 'activity-row-main');
            main.append(element('time', ev.date, 'activity-row-date'));
            const a = element('a', ev.name, 'activity-row-company');
            a.href = 'c/' + ev.orgnr + '.html' + (ev.anchor ? '#' + ev.anchor : '');
            main.append(a);
            main.append(element('span', ev.label, 'activity-row-label'));
            row.append(main);
            const viewLink = element('a', 'View receipts');
            viewLink.href = 'c/' + ev.orgnr + '.html' + (ev.anchor ? '#' + ev.anchor : '');
            row.append(viewLink);
            actBox.append(row);
          }
        }
      }
    }

    function renderActiveFilterChips(filters) {
      if(!activeFiltersContainer || !activeFiltersBar) return;
      activeFiltersContainer.replaceChildren();
      const chips = [];
      if(filters.query) {
        chips.push({ label: 'Search: "' + filters.query + '"', clear: () => { searchInput.value = ''; } });
      }
      if(filters.town) {
        chips.push({ label: 'Municipality: ' + filters.town, clear: () => { muniSelect.value = ''; } });
      }
      if(filters.division) {
        chips.push({ label: 'Division: ' + filters.division, clear: () => { divSelect.value = ''; } });
      }
      if(filters.size) {
        const sizeLabels = { micro: 'Micro (1–9)', small: 'Small (10–49)', medium: 'Medium (50–249)', large: 'Large (250+)', zero: 'Zero (0)', unknown: 'Unknown Size' };
        chips.push({ label: 'Size: ' + (sizeLabels[filters.size] || filters.size), clear: () => { sizeSelect.value = ''; } });
      }
      if(filters.web) chips.push({ label: 'Verified Website', clear: () => { filterWeb.checked = false; } });
      if(filters.jobs) chips.push({ label: 'Job Ads', clear: () => { filterJobs.checked = false; } });
      if(filters.social) chips.push({ label: 'Social Profiles', clear: () => { filterSocial.checked = false; } });
      if(filters.act) chips.push({ label: 'Public Activity', clear: () => { filterAct.checked = false; } });
      if(filters.inc) chips.push({ label: 'Incomplete Sections', clear: () => { filterInc.checked = false; } });
      if(filters.wlOnly) chips.push({ label: 'Watchlist (' + getWatchlist().size + ')', clear: () => { filterWatchlist.checked = false; } });

      activeFiltersBar.hidden = chips.length === 0;
      for(const chip of chips) {
        const item = element('span', chip.label, 'filter-chip');
        const btn = element('button', '✕', 'filter-chip-remove');
        btn.type = 'button';
        btn.setAttribute('aria-label', 'Remove ' + chip.label + ' filter');
        btn.addEventListener('click', () => { chip.clear(); draw(); });
        item.append(btn);
        activeFiltersContainer.append(item);
      }
    }

    function draw() {
      const currentSeq = ++searchSequence;
      const query = fold(searchInput?.value.trim());
      const town = muniSelect?.value || '';
      const division = divSelect?.value || '';
      const size = sizeSelect?.value || '';
      const web = filterWeb?.checked || false;
      const jobs = filterJobs?.checked || false;
      const social = filterSocial?.checked || false;
      const act = filterAct?.checked || false;
      const inc = filterInc?.checked || false;
      const wlOnly = filterWatchlist?.checked || false;
      const wlSet = getWatchlist();

      const isFiltered = Boolean(query || town || division || size || web || jobs || social || act || inc || wlOnly);

      const selected = records.filter(r => {
        if(query && !r._search.includes(query)) return false;
        if(town) {
          if(town === 'Unknown') { if(r.municipality) return false; }
          else if(r.municipality !== town) return false;
        }
        if(division) {
          if(division === 'Unknown') { if(r.nace) return false; }
          else if(!(r.nace || '').startsWith(division)) return false;
        }
        if(size && r.size_band !== size) return false;
        if(web && !r.flags.website) return false;
        if(jobs && !r.flags.jobs) return false;
        if(social && !r.flags.social) return false;
        if(act && !r.flags.activity) return false;
        if(inc && !Object.values(r.sections).some(s => s === 'failed' || s === 'blocked')) return false;
        if(wlOnly && !wlSet.has(r.orgnr)) return false;
        return true;
      });

      if(currentSeq !== searchSequence) return;

      const sort = sortSelect?.value || 'claim_count';
      selected.sort((a,b) => {
        if(sort === 'name') return a.name.localeCompare(b.name, 'nb') || a.orgnr.localeCompare(b.orgnr);
        if(sort === 'score') return (b.score ?? -Infinity) - (a.score ?? -Infinity) || a.orgnr.localeCompare(b.orgnr);
        return (b[sort] ?? -Infinity) - (a[sort] ?? -Infinity) || a.orgnr.localeCompare(b.orgnr);
      });

      const pages = Math.max(1, Math.ceil(selected.length / pageSize));
      pageNumber = Math.min(pageNumber, pages - 1);

      // Render Dashboard
      renderDashboard(selected, isFiltered);

      // Render Active Filter Chips
      renderActiveFilterChips({ query, town, division, size, web, jobs, social, act, inc, wlOnly });

      // Render Directory Results
      const results = document.getElementById('results');
      if(results) {
        results.replaceChildren();
        if(emptyResultsBox) emptyResultsBox.hidden = selected.length > 0;
        if(selected.length === 0) {
          document.getElementById('result-count').textContent = '0 companies match active filters';
        } else {
          for(const r of selected.slice(pageNumber * pageSize, (pageNumber + 1) * pageSize)) {
            const card = element('article', null, 'company');
            const heading = element('h2');
            const a = element('a', r.name);
            a.href = 'c/' + r.orgnr + '.html';
            heading.append(a);
            const isSaved = wlSet.has(r.orgnr);
            const starBtn = element('button', isSaved ? '★' : '☆', 'btn-watchlist-card' + (isSaved ? ' active' : ''));
            starBtn.type = 'button';
            starBtn.dataset.watchlist = r.orgnr;
            starBtn.setAttribute('aria-label', (isSaved ? 'Remove from' : 'Add to') + ' watchlist');
            heading.append(' ', starBtn);
            card.append(heading);
            card.append(element('p', r.orgnr + ' · ' + (r.municipality || 'Unknown municipality')));
            card.append(element('p', r.industry_en || r.industry_no || 'Industry unknown'));
            const badges = element('div', null, 'badges');
            for(const [label, family] of [['identity','identity'],['accounts','accounts'],['people','roles'],['web','website'],['hiring','hiring'],['activity','activity']]) {
              const state = r.sections[family] || 'not_applicable';
              badges.append(element('span', label + ': ' + state.replace(/_/g,' '), 'chip ' + state));
            }
            card.append(badges);
            card.append(element('p', 'Revenue: ' + format(r.revenue) + ' · Employees: ' + format(r.employees)));
            results.append(card);
          }
          const pct = ((selected.length / records.length) * 100).toFixed(1);
          document.getElementById('result-count').textContent = 'Showing ' + selected.length.toLocaleString('en-US') + ' companies (' + pct + '% of dataset)';
        }
      }

      const prevBtn = document.getElementById('previous');
      const nextBtn = document.getElementById('next');
      const pageLbl = document.getElementById('page-label');
      if(pageLbl) pageLbl.textContent = 'Page ' + (pageNumber + 1) + ' of ' + pages;
      if(prevBtn) prevBtn.disabled = pageNumber === 0;
      if(nextBtn) nextBtn.disabled = pageNumber === pages - 1;

      updateWatchlistUI();

      currentSelectedRecords = selected;
      updateQueryParams();
    }

    // Search autocomplete logic
    let highlightedIndex = -1;
    function renderAutocomplete() {
      if(!autocompleteBox || !searchInput) return;
      const q = fold(searchInput.value.trim());
      if(q.length < 2) {
        autocompleteBox.hidden = true;
        autocompleteBox.replaceChildren();
        highlightedIndex = -1;
        return;
      }
      const matches = records.filter(r => r._search.includes(q)).slice(0, 6);
      if(!matches.length) {
        autocompleteBox.hidden = true;
        autocompleteBox.replaceChildren();
        highlightedIndex = -1;
        return;
      }
      autocompleteBox.replaceChildren();
      highlightedIndex = -1;
      matches.forEach((r, idx) => {
        const item = element('div', null, 'autocomplete-item');
        item.setAttribute('role', 'option');
        item.dataset.index = String(idx);
        item.dataset.orgnr = r.orgnr;
        item.append(element('span', r.name, 'autocomplete-name'));
        item.append(element('span', r.orgnr + ' · ' + (r.municipality || 'Unknown location') + (r.website ? ' · ' + r.website : ''), 'autocomplete-meta'));
        item.addEventListener('mousedown', e => {
          e.preventDefault();
          window.location.href = 'c/' + r.orgnr + '.html';
        });
        autocompleteBox.append(item);
      });
      autocompleteBox.hidden = false;
    }

    if(searchInput) {
      let debounceTimer = null;
      searchInput.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
          pageNumber = 0;
          renderAutocomplete();
          draw();
        }, 150);
      });
      searchInput.addEventListener('keydown', e => {
        if(autocompleteBox && !autocompleteBox.hidden) {
          const items = autocompleteBox.querySelectorAll('.autocomplete-item');
          if(e.key === 'ArrowDown') {
            e.preventDefault();
            highlightedIndex = Math.min(highlightedIndex + 1, items.length - 1);
            items.forEach((it, i) => it.classList.toggle('is-highlighted', i === highlightedIndex));
          } else if(e.key === 'ArrowUp') {
            e.preventDefault();
            highlightedIndex = Math.max(highlightedIndex - 1, -1);
            items.forEach((it, i) => it.classList.toggle('is-highlighted', i === highlightedIndex));
          } else if(e.key === 'Enter') {
            if(highlightedIndex >= 0 && items[highlightedIndex]) {
              e.preventDefault();
              const orgnr = items[highlightedIndex].dataset.orgnr;
              if(orgnr) window.location.href = 'c/' + orgnr + '.html';
            } else {
              autocompleteBox.hidden = true;
            }
          } else if(e.key === 'Escape') {
            autocompleteBox.hidden = true;
            highlightedIndex = -1;
          }
        }
      });
      searchInput.addEventListener('blur', () => {
        setTimeout(() => { if(autocompleteBox) autocompleteBox.hidden = true; }, 200);
      });
    }

    // Attach listeners to select & check controls
    const controls = ['municipality', 'division', 'size-band', 'sort', 'filter-website', 'filter-jobs', 'filter-social', 'filter-activity', 'filter-incomplete', 'filter-watchlist'];
    for(const id of controls) {
      const el = document.getElementById(id);
      if(el) {
        el.addEventListener('change', () => {
          pageNumber = 0;
          draw();
        });
      }
    }

    const prevBtn = document.getElementById('previous');
    const nextBtn = document.getElementById('next');
    if(prevBtn) prevBtn.addEventListener('click', () => { pageNumber--; draw(); });
    if(nextBtn) nextBtn.addEventListener('click', () => { pageNumber++; draw(); });

    function exportRecordsCsv(dataToExport, filename) {
      const headers = [
        "Organisation number", "Name", "Municipality", "Industry code", "Industry title",
        "Employees", "Size band", "Revenue", "Annual result", "Currency", "Financial unit", "Fiscal year",
        "Verified website", "Website provenance", "Job postings", "Social profiles",
        "Public activity", "Claim count", "Last checked"
      ];
      const lines = [headers.join(',')];
      for (const r of dataToExport) {
        const row = [
          formatCsvOrgnr(r.orgnr),
          sanitizeCsvCell(r.name),
          sanitizeCsvCell(r.municipality),
          sanitizeCsvCell(r.nace),
          sanitizeCsvCell(r.industry_en || r.industry_no),
          sanitizeCsvCell(r.employees),
          sanitizeCsvCell(r.size_band),
          sanitizeCsvCell(r.revenue),
          sanitizeCsvCell(r.annual_result),
          sanitizeCsvCell(r.currency || ''),
          sanitizeCsvCell(r.unit || ''),
          sanitizeCsvCell(r.fiscal_year),
          sanitizeCsvCell(r.website),
          sanitizeCsvCell(r.website_origin),
          sanitizeCsvCell(r.jobs),
          sanitizeCsvCell(r.social),
          sanitizeCsvCell(r.activity),
          sanitizeCsvCell(r.claim_count),
          sanitizeCsvCell(r.last_checked)
        ];
        lines.push(row.join(','));
      }
      downloadFile(filename, lines.join('\r\n') + '\r\n', 'text/csv;charset=utf-8');
    }

    function exportRecordsJson(dataToExport, filename) {
      downloadFile(filename, JSON.stringify(dataToExport, null, 2), 'application/json;charset=utf-8');
    }

    const expDashCsv = document.getElementById('export-dashboard-csv');
    const expDashJson = document.getElementById('export-dashboard-json');
    const expDirCsv = document.getElementById('export-directory-csv');
    const expDirJson = document.getElementById('export-directory-json');

    if (expDashCsv) expDashCsv.addEventListener('click', () => exportRecordsCsv(currentSelectedRecords, 'signalpost-cohort.csv'));
    if (expDashJson) expDashJson.addEventListener('click', () => exportRecordsJson(currentSelectedRecords, 'signalpost-cohort.json'));
    if (expDirCsv) expDirCsv.addEventListener('click', () => exportRecordsCsv(currentSelectedRecords, 'signalpost-directory.csv'));
    if (expDirJson) expDirJson.addEventListener('click', () => exportRecordsJson(currentSelectedRecords, 'signalpost-directory.json'));

    // Saved Views
    function getSavedViews() {
      try {
        const data = localStorage.getItem(SAVED_VIEWS_KEY);
        return data ? JSON.parse(data) : [];
      } catch {
        return [];
      }
    }

    function saveSavedViews(views) {
      try {
        localStorage.setItem(SAVED_VIEWS_KEY, JSON.stringify(views));
      } catch {}
    }

    function renderSavedViews() {
      const container = document.getElementById('saved-views-list');
      if (!container) return;
      container.replaceChildren();
      const views = getSavedViews();
      if (!views.length) {
        container.append(element('span', 'No saved views yet', 'muted'));
        return;
      }
      for (let idx = 0; idx < views.length; idx++) {
        const v = views[idx];
        const pill = element('div', null, 'saved-view-pill');
        const loadBtn = element('button', v.name, 'saved-view-load');
        loadBtn.type = 'button';
        loadBtn.title = 'Apply saved view: ' + v.name;
        loadBtn.addEventListener('click', () => {
          const params = new URLSearchParams(v.query || '');
          if (searchInput) searchInput.value = params.get('q') || '';
          if (muniSelect) muniSelect.value = params.get('municipality') || '';
          if (divSelect) divSelect.value = params.get('division') || '';
          if (sizeSelect) sizeSelect.value = params.get('size') || '';
          if (sortSelect) sortSelect.value = params.get('sort') || 'claim_count';
          if (filterWeb) filterWeb.checked = params.get('web') === '1';
          if (filterJobs) filterJobs.checked = params.get('jobs') === '1';
          if (filterSocial) filterSocial.checked = params.get('social') === '1';
          if (filterAct) filterAct.checked = params.get('activity') === '1';
          if (filterInc) filterInc.checked = params.get('incomplete') === '1';
          if (filterWatchlist) filterWatchlist.checked = params.get('wl') === '1';
          pageNumber = 0;
          updateQueryParams();
          draw();
        });
        const delBtn = element('button', '✕', 'saved-view-delete');
        delBtn.type = 'button';
        delBtn.setAttribute('aria-label', 'Delete saved view ' + v.name);
        delBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          const updated = getSavedViews().filter((_, i) => i !== idx);
          saveSavedViews(updated);
          renderSavedViews();
        });
        pill.append(loadBtn, delBtn);
        container.append(pill);
      }
    }

    const saveViewBtn = document.getElementById('save-current-view');
    if (saveViewBtn) {
      saveViewBtn.addEventListener('click', () => {
        const views = getSavedViews();
        const defaultName = 'View ' + (views.length + 1);
        const name = (typeof window.prompt === 'function' ? window.prompt('Name for this view:', defaultName) : defaultName) || defaultName;
        const params = new URLSearchParams(window.location.search);
        if (filterWatchlist?.checked) params.set('wl', '1'); else params.delete('wl');
        views.push({ name, query: params.toString() });
        saveSavedViews(views);
        renderSavedViews();
      });
    }

    const clearWlBtn = document.getElementById('clear-watchlist');
    if (clearWlBtn) {
      clearWlBtn.addEventListener('click', () => {
        saveWatchlist(new Set());
        updateWatchlistUI();
        draw();
      });
    }

    // Hiring Explorer
    function renderHiringExplorer() {
      const titleInput = document.getElementById('hiring-search-title');
      const compInput = document.getElementById('hiring-search-company');
      const dateSelect = document.getElementById('hiring-filter-date');
      const container = document.getElementById('hiring-results');
      const countEl = document.getElementById('hiring-count');
      const emptyEl = document.getElementById('hiring-empty');
      if (!container) return;

      const titleQuery = fold(titleInput?.value.trim());
      const compQuery = fold(compInput?.value.trim());
      const dateCutoffDays = dateSelect?.value || 'all';

      const matchedJobs = [];
      for (const r of records) {
        if (compQuery && !fold(r.name + ' ' + r.orgnr).includes(compQuery)) continue;
        if (r.job_postings && r.job_postings.length) {
          for (const j of r.job_postings) {
            if (titleQuery && !fold(j.title).includes(titleQuery)) continue;
            if (dateCutoffDays !== 'all' && j.published) {
              const pubDate = new Date(j.published);
              const now = new Date();
              const diffDays = (now - pubDate) / (1000 * 60 * 60 * 24);
              if (!isNaN(diffDays) && diffDays > parseInt(dateCutoffDays, 10)) continue;
            }
            matchedJobs.push({
              companyName: r.name,
              orgnr: r.orgnr,
              municipality: r.municipality,
              title: j.title,
              published: j.published,
              expires: j.expires,
              matched_via: j.matched_via,
              anchor: j.anchor
            });
          }
        }
      }

      matchedJobs.sort((a, b) => (b.published || '').localeCompare(a.published || ''));

      container.replaceChildren();
      if (emptyEl) emptyEl.hidden = matchedJobs.length > 0;
      if (countEl) {
        countEl.textContent = matchedJobs.length === 1 
          ? '1 active job posting recalled' 
          : matchedJobs.length.toLocaleString('en-US') + ' active job postings recalled';
      }

      for (const job of matchedJobs) {
        const card = element('article', null, 'hiring-card');
        const header = element('div', null, 'hiring-card-header');
        header.append(element('h3', job.title, 'hiring-card-title'));
        if (job.published) {
          header.append(element('time', 'Published: ' + job.published, 'hiring-card-date'));
        }
        card.append(header);

        const meta = element('div', null, 'hiring-card-meta');
        const compLink = element('a', job.companyName, 'hiring-card-company');
        compLink.href = 'c/' + job.orgnr + '.html' + (job.anchor ? '#' + job.anchor : '');
        meta.append(compLink);
        meta.append(element('span', ' · ' + job.orgnr + (job.municipality ? ' · ' + job.municipality : '')));
        card.append(meta);

        const footer = element('div', null, 'hiring-card-footer');
        if (job.matched_via) {
          footer.append(element('span', 'Matched via: ' + job.matched_via, 'chip match-source'));
        }
        const viewProof = element('a', 'View proof & receipt', 'btn-sm');
        viewProof.href = 'c/' + job.orgnr + '.html' + (job.anchor ? '#' + job.anchor : '');
        footer.append(viewProof);
        card.append(footer);

        container.append(card);
      }
    }

    const hTitle = document.getElementById('hiring-search-title');
    const hComp = document.getElementById('hiring-search-company');
    const hDate = document.getElementById('hiring-filter-date');
    if (hTitle) hTitle.addEventListener('input', () => renderHiringExplorer());
    if (hComp) hComp.addEventListener('input', () => renderHiringExplorer());
    if (hDate) hDate.addEventListener('change', () => renderHiringExplorer());

    window._triggerDraw = draw;
    renderSavedViews();
    renderHiringExplorer();
    updateWatchlistUI();

    draw();
  }

  // ==========================================
  // PAGE: PROFILE (Evidence Explorer & Safe Exports)
  // ==========================================
  if(document.body.dataset.page === 'profile') {
    const showAllBtn = document.getElementById('explorer-show-all');
    if (showAllBtn) {
      showAllBtn.addEventListener('click', () => {
        const body = document.querySelector('.evidence-explorer-table tbody');
        const fragment = document.createDocumentFragment();
        for (const [label, availability, value, sourceClass, locator, sha, span] of (localData.explorer_rows || [])) {
          const tr = element('tr');
          const th = element('th', label); th.scope = 'row';
          const state = element('td'); state.append(stateChip(availability));
          const loc = element('td'); loc.append(element('code', locator));
          const hash = element('td');
          if (sha) { const code = element('code', sha.slice(0, 12) + '…'); code.title = sha; hash.append(code); } else { hash.textContent = '—'; }
          const excerpt = element('td'); excerpt.append(element('blockquote', span, 'table-excerpt'));
          tr.append(th, state, element('td', value), element('td', sourceClass), loc, hash, excerpt);
          fragment.append(tr);
        }
        body.append(fragment);
        const note = document.getElementById('explorer-more-note');
        if (note) note.textContent = 'Showing all claims.';
        showAllBtn.remove();
      });
    }
    const exportJsonBtn = document.getElementById('export-profile-json');
    const exportCsvBtn = document.getElementById('export-profile-csv');

    if (exportJsonBtn) {
      exportJsonBtn.addEventListener('click', () => {
        const orgnr = localData.orgnr || 'company';
        const items = (localData.facts || []).map(f => ({
          id: f.id,
          field: f.field,
          family: f.family,
          availability: f.availability,
          value: f.value,
          reporting_period: f.reporting_period,
          evidence: (f.evidence_ids || []).map(eid => {
            const e = evidence.get(eid);
            return e ? {
              id: e.id,
              source_class: e.source_class,
              source_url: e.source_url,
              source_identifier: e.source_identifier,
              locator: e.locator,
              claim_span: e.claim_span,
              content_sha256: e.content_sha256,
              retrieved_at: e.retrieved_at,
              effective_at: e.effective_at,
              extraction_method: e.extraction_method
            } : null;
          }).filter(Boolean)
        }));
        const exportObj = {
          organisation_number: orgnr,
          company_name: localData.name || orgnr,
          exported_at: new Date().toISOString(),
          claims_count: items.length,
          claims: items
        };
        downloadFile(orgnr + '-provenance.json', JSON.stringify(exportObj, null, 2), 'application/json;charset=utf-8');
      });
    }

    if (exportCsvBtn) {
      exportCsvBtn.addEventListener('click', () => {
        const orgnr = localData.orgnr || 'company';
        const headers = [
          "Organisation number", "Field", "Family", "Availability",
          "Value", "Reporting period", "Evidence count", "Primary source class",
          "Primary source URL", "Primary locator", "Primary SHA-256", "Primary excerpt"
        ];
        const lines = [headers.join(',')];
        for (const f of (localData.facts || [])) {
          const primaryId = (f.evidence_ids || [])[0];
          const primary = primaryId ? evidence.get(primaryId) : null;
          const rowCells = [
            formatCsvOrgnr(orgnr),
            sanitizeCsvCell(f.field),
            sanitizeCsvCell(f.family),
            sanitizeCsvCell(f.availability),
            sanitizeCsvCell(typeof f.value === 'object' ? JSON.stringify(f.value) : f.value),
            sanitizeCsvCell(f.reporting_period ? JSON.stringify(f.reporting_period) : ''),
            sanitizeCsvCell((f.evidence_ids || []).length),
            sanitizeCsvCell(primary ? primary.source_class : ''),
            sanitizeCsvCell(primary ? primary.source_url : ''),
            sanitizeCsvCell(primary ? primary.locator : ''),
            sanitizeCsvCell(primary ? primary.content_sha256 : ''),
            sanitizeCsvCell(primary ? primary.claim_span : '')
          ];
          lines.push(rowCells.join(','));
        }
        downloadFile(orgnr + '-summary.csv', lines.join('\r\n') + '\r\n', 'text/csv;charset=utf-8');
      });
    }
    updateWatchlistUI();
  }

  // ==========================================
  // PAGE: COMPARE (Side-by-side Comparison)
  // ==========================================
  if(document.body.dataset.page === 'compare') {
    const options = document.getElementById('company-options');
    if(options) {
      for(const r of records) {
        const option = element('option');
        option.value = r.orgnr;
        option.label = r.name + ' (' + r.orgnr + ')';
        options.append(option);
      }
    }

    const inputs = [0, 1, 2].map(i => document.getElementById('company-' + i));
    const clearBtn = document.getElementById('clear-compare');

    const fields = [
      ['name', 'Legal Name', 'identity'],
      ['orgnr', 'Organisation Number', 'identity'],
      ['municipality', 'Municipality', 'identity'],
      ['founding_date', 'Founding Date', 'identity'],
      ['industry', 'Industry (NACE)', 'identity'],
      ['employees', 'Employee Count', 'identity'],
      ['size_band', 'Size Category', 'identity'],
      ['workplaces', 'Workplaces Count', 'subunits'],
      ['website', 'Verified Website', 'website'],
      ['website_origin', 'Website Provenance', 'website'],
      ['website_proof', 'Proof Type', 'website'],
      ['revenue', 'Revenue', 'accounts'],
      ['annual_result', 'Annual Result', 'accounts'],
      ['currency', 'Reporting Currency', 'accounts'],
      ['fiscal_year', 'Reporting Period', 'accounts'],
      ['ceo', 'CEO / Daglig Leder', 'roles'],
      ['chair', 'Board Chair / Styreleder', 'roles'],
      ['auditor', 'Auditor / Revisor', 'roles'],
      ['jobs', 'Active Job Postings', 'hiring'],
      ['activity', 'Public Activity Items', 'activity'],
      ['last_checked', 'Last Verification Run', 'identity']
    ];

    function draw() {
      const selected = [];
      for(const input of inputs) {
        if(!input) continue;
        const val = input.value.trim();
        const r = byId.get(val) || records.find(r => fold(r.name) === fold(val) || r.orgnr === val);
        if(r && !selected.includes(r)) selected.push(r);
      }

      const root = document.getElementById('comparison');
      const status = document.getElementById('compare-status');
      if(status) {
        status.textContent = selected.length === 0 ? 'Select up to 3 companies above to compare.' :
                             selected.length === 1 ? '1 company selected. Select another to compare.' :
                             selected.length + ' companies compared side-by-side.';
      }
      if(!root) return;
      root.replaceChildren();

      selected.forEach((r, idx) => {
        const card = element('article', null, 'compare-card');
        const header = element('div', null, 'compare-card-header');
        const h2 = element('h2');
        const aName = element('a', r.name);
        aName.href = 'c/' + r.orgnr + '.html';
        h2.append(aName);
        const removeBtn = element('button', '✕ Remove', 'compare-remove-btn');
        removeBtn.type = 'button';
        removeBtn.setAttribute('aria-label', 'Remove ' + r.name + ' from comparison');
        removeBtn.addEventListener('click', () => {
          inputs[idx].value = '';
          draw();
        });
        header.append(h2, removeBtn);
        card.append(header);

        for(const [key, label, family] of fields) {
          const cell = element('div', null, 'compare-cell');
          cell.append(element('strong', label));
          const state = r.sections[family] || 'not_applicable';

          let val = key === 'industry' ? (r.industry_en || r.industry_no) : r[key];
          if(key === 'size_band') {
            const sizeMap = { micro: 'Micro (1–9)', small: 'Small (10–49)', medium: 'Medium (50–249)', large: 'Large (250+)', zero: 'Zero (0)', unknown: 'Unknown' };
            val = sizeMap[val] || val;
          }
          if((key === 'revenue' || key === 'annual_result') && val != null) {
            val = format(val) + ' ' + (r.currency || 'Unknown currency');
          }
          if(['social', 'jobs', 'activity'].includes(key) && state !== 'available') {
            val = null;
          }

          const hasVal = val != null && val !== '';
          const chipState = hasVal ? 'available' : (state === 'available' ? 'not_available' : state);
          cell.append(stateChip(chipState));

          const aVal = element('a', format(val), 'compare-val');
          const fallback = {
            industry: 'what-it-does',
            fiscal_year: 'financials',
            workplaces: 'locations',
            social: 'online',
            jobs: 'hiring',
            activity: 'activity',
            ceo: 'people',
            chair: 'people',
            auditor: 'people',
            website: 'online',
            website_origin: 'online',
            website_proof: 'online'
          };
          aVal.href = 'c/' + r.orgnr + '.html#' + (r.anchors[key] || fallback[key] || 'main');
          cell.append(aVal);
          card.append(cell);
        }
        root.append(card);
      });

      const hash = selected.map(r => r.orgnr).join(',');
      if(location.hash.slice(1) !== hash) {
        history.replaceState(null, '', hash ? '#' + hash : window.location.pathname);
      }
    }

    if(clearBtn) {
      clearBtn.addEventListener('click', () => {
        inputs.forEach(i => { if(i) i.value = ''; });
        draw();
      });
    }

    function fromHash() {
      const ids = location.hash.slice(1).split(',').filter(Boolean).slice(0, 3);
      inputs.forEach((input, i) => {
        if(input) input.value = byId.has(ids[i]) ? ids[i] : '';
      });
      draw();
    }

    for(const input of inputs) {
      if(input) input.addEventListener('input', draw);
    }
    window.addEventListener('hashchange', fromHash);
    fromHash();
  }

  // ==========================================
  // UPDATE STATUS PANEL
  // ==========================================
  const statusToggle = document.getElementById('status-toggle');
  const statusPanel = document.getElementById('status-panel');
  const statusClose = document.getElementById('status-close');
  const statusDot = document.getElementById('status-dot');
  const statusBadge = document.getElementById('status-badge');
  const statusProgress = document.getElementById('status-progress');
  const statusProgressText = document.getElementById('status-progress-text');
  const statusCounters = document.getElementById('status-counters');
  const statusStages = document.getElementById('status-stages');
  const statusTiming = document.getElementById('status-timing');
  const statusEvents = document.getElementById('status-events');
  const statusSnapshotNote = document.getElementById('status-snapshot-note');

  let statusPollTimer = null;
  let statusTerminal = false;
  let statusLastRunId = null;
  let statusLastData = null;

  function formatElapsed(seconds) {
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return m > 0 ? m + 'm ' + s + 's' : s + 's';
  }

  function renderStatusData(data) {
    if (!data) return;

    // Detect replaced run: different run_id means a new run replaced the old one
    if (statusLastRunId && data.run_id && data.run_id !== statusLastRunId) {
      statusTerminal = false; // Reset for new run
    }
    statusLastRunId = data.run_id || null;

    statusLastData = data;
    let status = data.status || 'unknown';
    if (status === 'running' && data.heartbeat && Date.now() - Date.parse(data.heartbeat) > 15000) status = 'stale';
    const isTerminal = status === 'completed' || status === 'failed' || status === 'interrupted';
    if (statusSnapshotNote && status !== 'stale') statusSnapshotNote.hidden = true;

    // Status dot
    if (statusDot) {
      statusDot.className = 'status-dot ' + (status === 'stale' ? 'stale' : isTerminal ? status : 'running');
    }

    // Badge
    if (statusBadge) {
      statusBadge.textContent = status.replace(/_/g, ' ');
      statusBadge.className = 'chip ' + (status === 'completed' ? 'available' : status === 'failed' ? 'failed' : 'not_applicable');
    }

    // Progress bar: real completion percentage from company counts
    const co = data.companies || {};
    const total = co.total || 0;
    const terminal = (co.successful || 0) + (co.failed || 0);
    const pct = total > 0 ? Math.round((terminal / total) * 100) : 0;
    if (statusProgress) statusProgress.value = pct;
    if (statusProgressText) {
      statusProgressText.textContent = total > 0
        ? terminal + ' of ' + total + ' companies completed (' + pct + '%)'
        : 'Waiting for pipeline data...';
    }

    // Company counters
    if (statusCounters) {
      statusCounters.replaceChildren();
      const counters = [
        { label: 'Queued', value: co.queued || 0 },
        { label: 'In flight', value: co.in_flight || 0 },
        { label: 'Successful', value: co.successful || 0 },
        { label: 'Failed', value: co.failed || 0 }
      ];
      for (const c of counters) {
        const div = element('div', null, 'status-counter');
        div.append(element('span', String(c.value), 'status-counter-value'));
        div.append(element('span', c.label, 'status-counter-label'));
        statusCounters.append(div);
      }
    }

    // Pipeline stages
    if (statusStages) {
      statusStages.replaceChildren();
      for (const stage of (data.stages || [])) {
        const row = element('div', null, 'status-stage');
        const icons = { completed: '✅', running: '⏳', queued: '⬜', failed: '❌' };
        row.append(element('span', icons[stage.state] || '⬜', 'status-stage-icon'));
        row.append(element('span', stage.name));
        row.append(stateChip(stage.state));
        statusStages.append(row);
      }
    }

    // Timing and resources
    if (statusTiming) {
      statusTiming.replaceChildren();
      const pairs = [
        ['Elapsed time', formatElapsed(data.elapsed_seconds || 0)],
        ['Last update', data.heartbeat ? data.heartbeat.replace('T', ' ').replace(/\.\d+Z?$/, ' UTC') : 'Unknown'],
        ['Requests', (data.requests?.measured || 0) + (data.requests?.limit != null ? ' / ' + data.requests.limit : '')],
        ['Estimated cost', '$' + (data.requests?.estimated_cost_usd || 0).toFixed(4)]
      ];
      if (data.input_rows) pairs.push(['Input rows', String(data.input_rows) + (data.duplicate_inputs ? ' (' + data.duplicate_inputs + ' duplicates)' : '')]);
      for (const [label, value] of pairs) {
        statusTiming.append(element('dt', label));
        statusTiming.append(element('dd', value));
      }
    }

    // Recent events (last 6)
    if (statusEvents) {
      statusEvents.replaceChildren();
      const events = (data.activity_log || []).slice(-6).reverse();
      if (events.length === 0) {
        statusEvents.append(element('p', 'No events recorded yet.', 'muted'));
      } else {
        for (const ev of events) {
          const row = element('div', null, 'status-event');
          row.append(element('span', formatElapsed(ev.timestamp || 0), 'status-event-time'));
          row.append(element('span', ev.message || '', 'status-event-msg'));
          statusEvents.append(row);
        }
      }
    }

    if (isTerminal) {
      statusTerminal = true;
    }
  }

  function showStaticSnapshot() {
    // In static/offline mode, show recorded run info from the index data
    if (!records.length) return;
    const lastChecked = records.reduce((latest, r) => r.last_checked > latest ? r.last_checked : latest, '');
    const totalCompanies = records.length;
    const websiteCount = records.filter(r => r.flags?.website).length;
    const hiringCount = records.filter(r => r.flags?.jobs).length;

    renderStatusData({
      schema_version: 1,
      status: 'completed',
      start_time: lastChecked,
      heartbeat: lastChecked,
      elapsed_seconds: 0,
      companies: {
        total: totalCompanies,
        queued: 0,
        in_flight: 0,
        successful: totalCompanies,
        failed: 0
      },
      stages: [
        { name: 'Registry & Subunits', state: 'completed' },
        { name: 'Website Verification', state: websiteCount > 0 ? 'completed' : 'completed' },
        { name: 'Output & Site Publishing', state: 'completed' }
      ],
      requests: { measured: 0, limit: null, estimated_cost_usd: 0 },
      activity_log: [],
      input_rows: totalCompanies,
      duplicate_inputs: 0
    });

    if (statusSnapshotNote) {
      statusSnapshotNote.textContent = 'Snapshot from completed run at ' + (lastChecked ? lastChecked.replace('T', ' ').replace(/\.\d+Z?$/, ' UTC') : 'unknown time') + '. No live updates available.';
      statusSnapshotNote.hidden = false;
    }
    statusTerminal = true;
  }

  async function pollProgress() {
    if (statusTerminal) return;
    if (document.hidden) return; // Pause while hidden

    try {
      let resp = await fetch('progress.json', { cache: 'no-store' });
      if (!resp.ok) {
        resp = await fetch('state/progress.json', { cache: 'no-store' });
      }
      if (!resp.ok) {
        showUnavailableProgress();
        return;
      }
      const data = await resp.json();
      if (!data || typeof data !== 'object' || !data.schema_version) {
        showUnavailableProgress();
        return;
      }
      renderStatusData(data);
    } catch {
      showUnavailableProgress();
    }
  }

  function showUnavailableProgress() {
      if (statusLastData && !statusTerminal) {
        renderStatusData({...statusLastData, status: 'stale'});
        if (statusSnapshotNote) {
          statusSnapshotNote.textContent = 'Live progress unavailable. Showing the last received update.';
          statusSnapshotNote.hidden = false;
        }
      } else showStaticSnapshot();
  }

  function startPolling() {
    if (statusTerminal || statusPollTimer) return;
    // Only poll for same-origin HTTP(S) served pages
    if (location.protocol === 'file:') {
      showStaticSnapshot();
      return;
    }
    pollProgress();
    statusPollTimer = setInterval(() => {
      if (statusTerminal) {
        clearInterval(statusPollTimer);
        statusPollTimer = null;
        return;
      }
      pollProgress();
    }, 3000); // 3 second poll interval
  }

  function stopPolling() {
    if (statusPollTimer) {
      clearInterval(statusPollTimer);
      statusPollTimer = null;
    }
  }

  // Pause polling while tab is hidden
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      stopPolling();
    } else if (statusPanel && !statusPanel.hidden && !statusTerminal) {
      startPolling();
    }
  });

  if (statusToggle && statusPanel) {
    statusToggle.addEventListener('click', () => {
      const opening = statusPanel.hidden;
      statusPanel.hidden = !opening;
      statusToggle.setAttribute('aria-expanded', String(opening));
      if (opening) {
        startPolling();
      } else {
        stopPolling();
      }
    });
  }

  if (statusClose && statusPanel && statusToggle) {
    statusClose.addEventListener('click', () => {
      statusPanel.hidden = true;
      statusToggle.setAttribute('aria-expanded', 'false');
      stopPolling();
      statusToggle.focus();
    });
  }

  // Escape key closes status panel
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && statusPanel && !statusPanel.hidden) {
      statusPanel.hidden = true;
      if (statusToggle) {
        statusToggle.setAttribute('aria-expanded', 'false');
        statusToggle.focus();
      }
      stopPolling();
    }
  });

  // Initialize dot with static data
  if (statusDot && records.length) {
    statusDot.className = 'status-dot completed';
  }
})();
