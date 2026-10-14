# Signalpost UI Verification and Architecture Documentation

This document describes the design, implementation, and reproducible verification procedures for the Signalpost user interface.

## 1. Feature Architecture

The Signalpost UI provides an offline, zero-external-dependency static site generator that compiles evaluated company envelopes into a fast, accessible research interface with receipts.

### 1.1 Visual Redesign
- **Design Tokens**: Standardized slate and navy color system with teal accents (`--navy-900: #0a1120`, `--navy-800: #0f172a`, `--teal-400: #14b8a6`, `--teal-500: #0d9488`).
- **Typography & Hierarchy**: System font stack (`system-ui, -apple-system, sans-serif`) with readable scales and accessible WCAG AA contrast.
- **Responsive Layout**: Fluid breakpoints supporting desktop (`1280px`), tablet (`768px`), and mobile (`375px`) viewports with zero horizontal overflow (`scrollWidth <= innerWidth`).
- **Dark/Light Theme**: Client-side theme switch persisting preference in `localStorage`.

### 1.2 Cohort Dashboard
- **Cohort Scope**: Banner indicating evaluated entity count (e.g., `1,000 companies`) with reactive filter warnings.
- **Summary KPI Cards**: Metric tiles displaying total companies, verified website count and percentage, active hiring counts, and recent activity percentage.
- **Provenance Breakdown**: Segmented bars showing distribution of verified website origins (`registry_website`, `legal_name_slug`, `search_brave`, `registry_email`).
- **Hiring Timeline**: Monthly aggregation chart of active job advertisements from the NAV stream.
- **Recent Public Activity**: Feed of verified official registry changes and filings within a 2-year window, complete with links to anchor receipts.

### 1.3 Advanced Combinable Filters
- **Facet Dimensions**: Municipality dropdown, NACE 2-digit industry division dropdown, and Company Size bands:
  - `micro`: 1–9 employees
  - `small`: 10–49 employees
  - `medium`: 50–249 employees
  - `large`: 250+ employees
  - `zero`: 0 employees
  - `unknown`: No employee data reported
- **Active Filter Chips**: Dismissible filter chips with `[✕]` buttons and a global "Clear all" action.
- **Faceted Counts & URL Sync**: Real-time result counts and deep-linkable URL parameters (`?q=...&municipality=...&division=...&size=...`).

### 1.4 Side-by-Side Company Comparison
- **Entity Selection**: Multi-company input matching up to 3 companies simultaneously with autocomplete datalist options.
- **Aligned Matrix**: Uniform rows comparing legal name, orgnr, municipality, founding date, industry, scale, financials (revenue, result, period), governance (CEO, chair, auditor), hiring, and website.
- **Receipt Deep-links**: Every attribute cell links directly to its source proof on the respective profile page.
- **Interactive Controls**: Per-company `[✕ Remove]` button and "Clear all" action with URL hash persistence (`#org1,org2,org3`).

### 1.5 Company Timeline
- **Business Event Chronology**: Reverse-chronological timeline on company profile pages (`c/<orgnr>.html`) showing founding, VAT registration, financial filings, and job postings.
- **Evidence Integrity**: Distinguishes verified real-world business event dates from system scrape and observation timestamps. Every dated node links directly to its `#fact-...` citation.

### 1.6 Search Refinements
- **Debounced Search**: 150ms client-side search across legal names and organisation numbers with Norwegian diacritic normalization.
- **Keyboard-Navigable Autocomplete**: Dropdown popup navigable via `ArrowDown`, `ArrowUp`, `Enter`, and `Escape`.
- **Empty States**: Helpful no-result fallbacks with a 1-click filter reset.

---

## 2. Invariants & Safety Constraints

1. **Zero `innerHTML` Usage**:
   Client-side scripts in `src/signalpost/site_assets/site.js` use safe DOM construction APIs (`document.createElement`, `textContent`, `append`, `replaceChildren`) to eliminate XSS vectors. Enforced by unit test assertion `assert 'innerHTML' not in (out / 'assets/site.js').read_text()`.
2. **Strict CSP & Local Assets**:
   No external CDNs, fonts, or tracking scripts (`default-src 'self'`).
3. **No `<img>` Tags**:
   All icons and status indicators use CSS or text/Unicode.
4. **Profile Budget Gate**:
   Largest company profile page must remain under 250,000 bytes. In the 1,000-company cohort, the largest profile is 71,718 bytes.
5. **Deterministic Page Count**:
   Total output pages generated must equal `len(records) + 2` (`index.html`, `compare.html`, and `c/<orgnr>.html`). The dashboard is hosted inside `index.html` via accessible tabs to preserve this invariant.

---

## 3. Reproducible Verification Commands

### Site Generation
```powershell
uv run signalpost site --input out/w5-opt1000-rev4-envelopes.jsonl --out dev-notes/site-w5-opt1000-rev4 --title "Signalpost"
```

### Automated Unit and Integration Tests
```powershell
# Site-specific tests (including dashboard, timeline, comparison, size bands, security)
uv run pytest tests/test_site.py

# Full regression suite across entire project (278 tests)
uv run pytest
```

### Browser Automated QA (Headless Chrome via CDP)
```powershell
node dev-notes/scripts/ui_verification.mjs
```
The script validates:
- Desktop (1280px) and mobile (375px) layouts without horizontal overflow.
- Dashboard metric counts, provenance bars, hiring timeline, and recent activity.
- Directory pagination, search autocomplete, keyboard navigation, and active filter chips.
- Company comparison side-by-side display, individual removal, and mobile stacking.
- Company profile timeline nodes and receipt anchor links.
- Takes screenshots in `dev-notes/screens/`.

### Interactive Inspection
```powershell
uv run python -m http.server -d dev-notes/site-w5-opt1000-rev4 8080
```
Visit `http://localhost:8080` in any browser.
