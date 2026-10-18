# Signalpost UI/UX and synthesis audit — Phase 1

**Audit branch:** `ux/audit` from submitted `c28b580` (`v1.1.1`). **Decision:** STOP after this audit; application code is unchanged. This is an offline `file://` audit of a fresh 50-input run, not a release claim. Evidence and the fixed dataset remain in this worktree. No push, tag, or Phase 2 work was performed.

## 1. Summary scorecard

| Check | Result | Evidence and finding |
|---|---|---|
| UX-1 Find | **PASS** | Name and organisation-number search worked on every audited page, `/` and Ctrl+K opened search, and directory A–Z / all-five-areas controls changed results from 49 to 14. [Directory at 375](screenshots/before/directory_375.png), [interaction output](dom-audit.json). |
| UX-2 Compare | **FAIL** | Two companies survive a URL reload and show five area rows, but a four-company URL is silently rewritten to three; there are only three selectors. Mobile cards stack without page overflow. [Four-company attempt at 375](screenshots/before/compare_4_375.png), [DOM output](dom-audit.json). |
| UX-3 Verify | **PARTIAL** | One-click panels worked for nine sampled fact types and expose source link/class, retrieved UTC, period, hash, method, locator and quote. Website proof type is visible. The required **exact** string `registry publication time (not effective date)` exists in the raw value but the site instead renders `Registry publication time: … (not effective date)`. Source class is generic, and compare missing cells omit the recorded reason. [Registry panel](screenshots/before/registry_evidence.png), [website panel](screenshots/before/website_evidence.png), [claim checks](deep-checks.json). |
| UX-4 Desktop | **PASS** | All nine page cases loaded at 1440 with zero console/page errors, including Equinor and the invalid-ID notice. A large profile is long but functional. [Equinor](screenshots/before/equinor_1440.png), [invalid notice](screenshots/before/invalid_input_1440.png), [DOM output](dom-audit.json). |
| UX-5 Mobile | **PARTIAL** | No document-level overflow at 375 or 320; search is at the top, tables remained within the viewport, and sampled text contrast found no value below 4.5. At 375, profile `<summary>` controls measure only 24 px high. [Near-empty first viewport](screenshots/before/near_empty_viewport_375.png), [full mobile screenshots](screenshots/before/), [DOM/tap output](dom-audit.json). |
| SYN-1 What it does | **PASS** | Registry purpose and NACE/industry prose appear in plain language with citations. [Equinor](screenshots/before/equinor_1440.png), [sentence audit](synthesis-checks.json). |
| SYN-2 What changed | **PARTIAL** | Registry and website updates are dated and cited, but zero of 50 synthesis outputs use the requested “no changes found in sources checked” wording. The dashboard activity list is empty while its KPI says 15 companies have activity. [Registry profile](screenshots/before/registry_activity_1440.png), [dashboard](screenshots/before/directory_1440.png), [checks](deep-checks.json), [synthesis audit](synthesis-checks.json). |
| SYN-3 What is unknown | **PARTIAL** | 257 unknown statements exist, and section badges show availability, but the cited summary appends muted sentences without a labelled unknowns block or the underlying reason. Compare shows a state chip plus “Unknown” but no reason. [Near-empty profile](screenshots/before/near_empty_375.png), [missing-state DOM](a11y-checks.json), [synthesis audit](synthesis-checks.json). |
| SYN-4 Every sentence cited | **PARTIAL** | All 420 sentences in the four factual synthesis sections have at least one resolvable claim citation. The 257 unknown statements have no claim IDs or direct state links. [Equinor citations](screenshots/before/equinor_viewport_375.png), [citation audit](synthesis-checks.json). |
| SYN-5 No unsupported claims | **FAIL** | Sampled financial text uses the reported period and avoids growth claims; NAV absence is scoped to ads. But the dashboard asserts “No recent verified registry filings within 2-year window” despite available recent registry events in this same sample. [Dashboard](screenshots/before/directory_375.png), [registry evidence](screenshots/before/registry_evidence.png), [contradiction check](deep-checks.json). |

**Count:** 3 PASS, 5 PARTIAL, 2 FAIL. The site works directly from disk with the network blocked and no console errors. The 250 KB initial-load hard rule fails on every company profile, so release readiness is blocked independent of the scorecard.

## 2. Sample and reproduction

The root checkout contained unrelated untracked report files; no user file was removed. After `git fetch --tags origin`, a clean worktree/branch was created at `out/ux-audit-worktree` from `c28b580`. This is the documented workaround for the requested clean starting status. `uv sync --frozen` completed without a lockfile change. Existing Chrome was used through Playwright (`channel='chrome'`), avoiding a Chromium download. The audit-only Playwright package was cached under `reports/ux/tools/uv-cache/`, outside shipped dependencies. When network access later refused a PyPI connection, `uv run --offline --with playwright` reused that cache; no source request or application code was changed.

[`sample/batch.jsonl`](sample/batch.jsonl) contains exactly 50 inputs. [`sample/selection.json`](sample/selection.json) records the source SHA-256, bulk SHA-256 and special-case rationale. Controls: Equinor `923609016` (large), FILMTEK `988330752` (known site ambiguity), `932525070` (11 registry event claims), `929583027` (NAV ad), `991853995` (exact-proof website), `820042182` (sparse external coverage), and invalid `12345678`. The other 43 are distinct valid companies in input order from the frozen 1,000-company bulk cohort. The invalid ID has a terminal envelope and an index-page notice, **not** a separate invalid-input HTML route.

From this worktree, with the original frozen bulk CSV at `C:\Users\Manish\Downloads\Signalpost-v5\out\capacity-inputs\bulk1000.csv`:

```powershell
$env:UV_CACHE_DIR = Join-Path (Get-Location) 'reports/ux/tools/uv-cache'
uv run --frozen signalpost run --organisations reports/ux/sample/batch.jsonl --bulk 'C:\Users\Manish\Downloads\Signalpost-v5\out\capacity-inputs\bulk1000.csv' --output reports/ux/sample/out/envelopes.jsonl --profiles-output reports/ux/sample/out/profiles.jsonl --report reports/ux/sample/out/report.json --site-dir reports/ux/sample/site --state-dir reports/ux/sample/out/state --websites --hiring --public-activity --run-id ux-audit-50 --expected-count 50
.\.venv\Scripts\python.exe scripts/verify_output.py --first reports/ux/sample/out/envelopes.jsonl --state-dir reports/ux/sample/out/state --count 50 --organisations reports/ux/sample/batch.jsonl --report reports/ux/sample/out/report.json
uv run --offline --frozen --with playwright python reports/ux/tools/audit.py
uv run --offline --frozen --with playwright python reports/ux/tools/deep_checks.py
uv run --offline --frozen --with playwright python reports/ux/tools/a11y_checks.py
```

The run emitted 50 ordered envelopes (49 complete, one invalid submission error), used 284 HTTP requests and took 41.187 s. The verifier passed: 50 schema-valid lines, 3,716 published claims, 190 saved source blobs verified, 420 synthesis sentences, zero unverified values. The generated `out/` files, site and screenshots are deliberately ignored but retained locally as the **fixed dataset** for any approved before/after UI comparison: envelopes 7,704,022 bytes, profiles 5,162,584, report 2,006,525, site 8,240,897. The 41 full-page, evidence and viewport screenshots total 40,325,686 bytes; see [`dom-audit.json`](dom-audit.json) for all 27 full-page paths and [`deep-checks.json`](deep-checks.json) for evidence paths. Site-only regeneration is available as `signalpost site --input reports/ux/sample/out/envelopes.jsonl --out <site-dir>` (or `site.generate_site`); it requires no new extraction.

## 3. Generated-file inventory and page weight

[`inventory.json`](inventory.json) lists **all 105 generated paths**, byte sizes, purpose, every page dependency and initial-load total. The route/asset pattern is:

| Path / count | Bytes and purpose | Loaded on navigation |
|---|---|---|
| `index.html` | 21,006; dashboard, directory, hiring explorer, invalid-ID notice `#invalid-inputs` | CSS 33,797 + index JS 65,188 + UI JS 67,153; **187,144 total** |
| `compare.html?companies=a,b` | 3,789; selectors and side-by-side cards; `#a,b` also parsed | same shared assets; **169,927 total** |
| `c/<orgnr>.html` ×49 | 49 company profiles; largest 128,305 (Equinor) | shared assets plus `c/<orgnr>.data.js`; **267,262–814,033 total**, all over limit |
| `c/<orgnr>.data.js` ×49 | fact/evidence payload used by evidence panels and details; Equinor 519,590 | initially loaded on its profile, despite `defer`; no lazy data chunks |
| `data/index.js` | 65,188; search/directory/compare record index | every page, including profiles |
| `data/index.json` | 65,161; optional data export | not loaded on navigation |
| `assets/site.js`, `assets/site.css` | 67,153 / 33,797; interactions/style | every page |
| `progress.json` | 1,423; run status | not fetched on `file://`; status panel uses a static snapshot |

No HTML file exceeds 250 KB; **all 49 company initial loads exceed 250 KB**. Equinor is 814,033 bytes, and its individual data script is 519,590 bytes. There are no lazy chunks to measure. `defer` does not exempt a script from the initial-load budget. The browser test confirms the status panel makes zero `progress.json` requests from disk and shows a static UTC snapshot ([status screenshot](screenshots/before/status_file.png), [check](deep-checks.json)). Non-file requests were aborted throughout the main audit; none were attempted.

## 4. UI data contract

The site consumes the canonical envelope's `organisation_number`, `claims`, `evidence`, `changes`, `run.sections`, `run.refresh`, `run.synthesis`, and `run.completed_at`. `site.normalize` also accepts profile-shaped input and maps it into this view. Profile labels and area buckets are built from `claims[*].family`, `field`, `value`, `availability`, `reporting_period`, `carried_forward`, `last_observed_at`, and `evidence_ids`.

| UI area | Fields read or derived |
|---|---|
| Header / company brief | `identity.legal_name`, `organisation_form`, `legal_form`, `municipality`, founding/registration dates, NACE descriptions/codes, activity/purpose, employee count, state flags; `organisation_number`, `run.completed_at`. |
| Latest financials | `accounts.*` claim values and `reporting_period.fiscal_year`, `period_start`, `period_end`, `currency`, `unit`; published values only, no calculated growth ratio. |
| Who runs it? | `roles.role.*` and `roles.detail.*` names/titles/order; additional official attributes render on details expansion. |
| Working here / locations | `identity.employees`, `subunits.unit.*`, `subunits.detail.*`, `hiring.job.*`; NAV title, publication date, matched employer and source. |
| Online presence | `official_website` URL, `identity_level`, `proof_type`, `proof_page_url`, matched subunit; `website_description.*`, `social_profile.*`, contacts and registered website. |
| Recent activity | `activity`/`dated_item.*`, `registry_change.*` title/date/source URL, plus registry dates derived from identity/account facts; section `run.sections.activity`. |
| Cited summary / unknowns | `run.synthesis.sections.what_it_does`, `scale`, `leadership`, `changes`, `unknowns`, each factual sentence's `claim_ids`, and `change_claims` for change citations. Unknown `reason` is present in data but only its shorter `text` is rendered. |
| Availability / receipts | `run.sections`, per-claim `availability`; evidence `source_url`, `source_identifier`, `source_class`, `retrieved_at` UTC, `effective_at`/`reporting_period`, `content_sha256`, `extraction_method`, `locator`, `claim_span`, and claim `confidence`. |
| Directory / compare | A derived index record from available claims: name/orgnr, municipality, NACE, employees, website/proof, financial values/period, role leaders, workplaces, jobs, activity, section states, claim counts, anchor links. |

The raw top-level `errors`, `operations`, `modules`, `state`, `run_id`, `started_at` and `profile` object are **not separately displayed**; `run.completed_at` is displayed as last checked, and `run.refresh`/`changes` are displayed in the freshness section. Raw source-error codes and full unknown `reason` strings are not shown, though section states and short explanatory text are. This makes a distinction between availability being represented and its precise reason being visible.

## 5. Evidence links and disclosure

Counts below are evidence records in this sample, not distinct URLs. Every sampled fact type's “Check the evidence” panel showed source class, URL, retrieval UTC, effective/reporting period or “Unknown,” hash, method/version, locator and excerpt ([targeted checks](deep-checks.json)). The external URL itself opens outside the offline site; the site's receipts remain usable without network.

| Link type / sample count | Example route or value | Source name, retrieval date, method in the UI |
|---|---|---|
| BRREG entities/bulk — 1,652 | `data.brreg.no/enhetsregisteret/api/enheter/<org>` or `/lastned/csv` | Generic `official_registry` class; UTC and method in panel. |
| BRREG roles — 637 | `/enheter/<org>/roller` | Same generic class; UTC and method in panel. |
| BRREG subunits — 610 | `/underenheter?overordnetEnhet=<org>` | Same generic class; UTC and method in panel. |
| BRREG updates — 36 | `/oppdateringer/enheter?...includeChanges=true` | Same generic class; UTC/method/locator in panel; raw URL is very long due 50-ID query. |
| BRREG accounts — 1,060 | `data.brreg.no/regnskapsregisteret/regnskap/<org>` | Generic `official_registry` class; UTC and method in panel, fiscal period in claim. |
| NAV ads — 1 | `pam-stilling-feed.nav.no/api/v1/feedentry/<uuid>` | `official_nav` class; UTC and method in panel. |
| Company-owned/report pages — 116 | `www.bien.no`, `www.filmtek.no`, annual-report PDFs | `company_owned`/`company_report` class; UTC and method in panel. |
| Social profile values — 4 | LinkedIn/Facebook/Instagram/X URLs in BIEN claim values | Profile link visible in fact; the supporting receipt is the company page where it was observed, with `company_owned`, UTC and method. The social platform itself is not a separate fetched evidence source. |

The panels identify a **source class**, not a human-friendly provider name; the URL reveals BRREG/NAV/domain. Website proof type (`orgnr_on_page`) and `VERIFIED` identity level are visible for BIEN, and the proof page URL appears in its receipt. Registry evidence correctly leaves “Effective / reporting date” unknown, while its publication timestamp appears in the fact sentence; only the exact required label fails.

## 6. Detailed browser and synthesis findings

The audit opened directory, Equinor, FILMTEK, small company `925181536`, near-empty company, registry activity company, compare with two and attempted four companies, and invalid-input notice, each at 1440/375/320. [`dom-audit.json`](dom-audit.json) records the 27 full-page screenshot paths and all console, page, request, overflow, tap and sampled contrast results. There were **zero** load failures, console/page errors, failed requests, attempted external requests, or mobile horizontal overflows. Sampled visible text had zero measured contrast ratios under 4.5:1; this is a sample of the first 300 visible text elements per page, not a full WCAG certification. Header/nav/main landmarks, labelled visible inputs, alt attributes and visible 3 px keyboard focus outlines passed the sampled DOM checks ([keyboard/missing-value output](a11y-checks.json)). The first ten Tab stops begin at “Skip to content,” traverse top navigation and reach search. The 375 px profile `summary` disclosures are 24 px high; at 320 the responsive treatment yielded no measured controls below 40 px in the sampled cases.

Missing profile facts show a state chip and a scoped explanation rather than an unexplained zero or dash. The near-empty company’s `NOK 0` annual result is an **available sourced claim**, not a missing-value placeholder. Compare missing cells show “Unknown” plus a state chip, but do not expose the recorded reason until the user follows the profile link. The invalid ID appears in the index notice and its JSON terminal envelope; it does not get a company page. [Near-empty screenshot](screenshots/before/near_empty_viewport_375.png), [invalid notice](screenshots/before/invalid_input_375.png), [state output](a11y-checks.json).

The dashboard contradiction is deterministic. `index_record` computes `activity` and `latest_activity_*`, but does not emit `recent_events`; `site.js` populates the recent list **only** from `recent_events`. All 49 index records lack that key, so the list always says no recent filings, even when the KPI says 15 and registry event facts are present. [Source check](deep-checks.json). The four-company comparison is also deterministic: `compare_page` renders three inputs; `site.js` creates three input handles and slices URL IDs to three.

All 420 factual synthesis sentences in this sample resolve their citations and the verifier found zero unsupported values. The 257 unknown statements derive from states but have no citation links; the report does **not** treat those as fabricated facts. No sampled financial sentence asserts growth from one year, and absence of NAV ads is scoped to ads rather than employment. The false dashboard “no recent” claim is nevertheless unsupported by its own index facts. [Sentence audit](synthesis-checks.json).

## 7. Ranked gaps

The estimated score gains are **upper bounds**, because a check only earns points when every part passes. Risk refers to data correctness, not development time. All proposals keep extraction, identities, envelopes and shipped dependencies unchanged. No `[SYNTH-ENVELOPE]` change is recommended.

| Rank / ID | Gap and checks; potential points | Effort / risk | Files and existing fields; tag |
|---|---|---|---|
| 1 / **G1** | Supply `recent_events` from existing dated registry/activity claims and remove the false empty message; use the newest event in the summary card, and say “no changes found in sources checked” only when supported by the checked scope. SYN-2, SYN-5, up to **4.8** combined if all wording checks pass. | **S, 25 min / low** | `site.py`, `site_assets/site.js`, site tests; `claims[*].field/value/date/evidence_ids`, index `latest_activity_*`, `run.sections`; **[SITE-ONLY]**. |
| 2 / **G6** | Raise 375 px profile disclosure hit areas from 24 to ≥40 px. UX-5, up to **1.6**. | **S, 15 min / none** | `site_assets/site.css`, site test; no new data; **[SITE-ONLY]**. |
| 3 / **G3** | Add a labelled “What remains unknown” block with each state and its recorded reason; link or clearly identify state-backed unknowns. SYN-3 and potentially SYN-4, up to **4.8**. | **M, 50 min / low** | `site.py`, CSS, tests; `run.synthesis.sections.unknowns[*].text/reason`, `run.sections`, unavailable claims; **[SITE-ONLY]**. |
| 4 / **G2** | Render/select four comparison companies and preserve all four IDs on URL reload; keep five area states. UX-2, up to **1.6**. | **S, 25 min / low** | `site.py`, `site_assets/site.js`, CSS if needed, tests; derived index records and `run.sections`; **[SITE-ONLY]**. |
| 5 / **G5** | Render the literal registry publication-time label and human-readable source names; expose reason on compare missing cells or direct source-state link. UX-3, up to **1.6**. | **S, 25 min / low** | `site.py`, `site_assets/site.js`, tests; `registry_change.value.date_source`, `evidence.source_class`, `run.sections`, unknown reasons; **[SITE-ONLY]**. |
| 6 / **G4** | Meet initial-load ≤250 KB on every profile and ≤250 KB per lazy chunk, using local script chunks, with no `fetch` and no loss of visible facts/receipts. Mandatory release rule; direct rubric points uncertain. | **L, 90–120 min / low only with exact fact/receipt regression checks** | `site.py`, `site_assets/site.js`, site tests; generated index and per-company claims/evidence payload. **[SITE-ONLY]**. |

G4 is a **veto for release until fixed**, regardless of point-per-minute ranking. It is ranked below shorter scoring fixes by estimated direct points/effort, but would have to be done first in any approved implementation. A safe, fully gated Phase 2 set does **not** fit confidently in three hours: G4 alone may need 90–120 minutes, while fixed-data browser checks, full tests, the 50-company output comparison, default 1,000 run and clean-clone smoke consume the remaining time. The narrowest provisional subset is **G4 + G1 + gates** at exactly 180 minutes on optimistic estimates, with no contingency; therefore **no set is marked as reliably fitting ≤3 hours**. G2/G3/G5/G6 should only be added if time remains after G4 proves feasible. No medium-risk proposal is recommended.

## 8. Proposed Phase 2 plan (requires explicit approval)

After a reply of `APPROVED: <gap IDs>`, branch `ux/r4` from `ux/audit`. First implement only the approved site-layer gaps, one logical commit per gap. Regenerate from the **fixed** envelopes and rerun the offline screenshots/DOM checks, including exact factual/evidence equivalence and all three byte limits. A provisional three-hour budget is G4 100 min, G1 25 min, then 55 min for tests, output comparison, default 1,000-company gate, local CI steps and a clean-clone smoke; this budget has little contingency and therefore does not guarantee completion. The user’s 17:00 IST stop-new-work and 17:30 IST hard stop still govern any later phase. If a gate cannot finish, report **NOT READY**. No push occurs without the separate `PUSH` instruction, and remote CI remains pending until then.

**Phase 1 ends here. Await explicit `APPROVED: …` before changing application code.**
