# Remediation release — 15 October 2026

**READY FOR REVISION.** The confirmed shared decoding, auditor, event-loop blocking, progress-state, currency and ownership defects are fixed. All 391 tests pass; separate statement coverage is 91.58%; strict replay, fresh-clone integration and actual Chrome interactions pass. This is local operational readiness, not organiser acceptance, a score, factual accuracy or recall.

Fixed source: `a11d4ec68445c332ad10f22b063eca061a646a0a`. Live measurements below are at **`45ebf1e`**, before the final footer-name spacing correction. That last change passes the complete suite, actual saved-page/context regression, strict replay and fresh clone; it has **not** been live benchmarked. Measured live coverage has not been increased to predict its effect. No further live crawl was made after this bounded investigation.

Started clean on `main` at `d4abfc2`; submitted `0d28df1` is preserved. No push, deployment, email, paid search or process termination. Unidentified preexisting Python processes and personal browser profiles were preserved. The [machine report](remediation-release.json) records exact commands, hashes, timestamps, audits, load summaries and every historical failure classification. Large raw evidence remains under `out/remediation/` and is intentionally untracked.

## Root causes and corrections

* **812573942:** the original gzip registry download (despite its `.csv` filename), prepared CSV, extracted identity and serialized claim already contain correct UTF-8 `RØRLEGGER 1 MOLDE AS`. The previous investigation read UTF-8 through the Windows cp1252 default and reported false mojibake. No business-name change or source replacement is justified. The original is preserved; the subset was reproducibly regenerated with the existing `scripts/extract_bulk.py` and matches the previously prepared subset hash.
* **964624046:** recorded source `7bef154551fb044a42008392449c126fb18c9c95eb696e879fada0bc96ad4e44` contains the correct UTF-8 full paragraph. An inline link interrupts raw HTML text, so raw substring auditing falsely rejected the claim. The independent auditor now parses complete paragraph/meta text, within the production 300-character limit, rather than accepting a short matching word or trusting proof labels. The historical 100-company audit becomes 6,977/6,977 without changing its claims or evidence.
* **Actual encoding bug:** Page extraction understood declared legacy HTML, but evidence writing/verification decoded it as UTF-8. The shared bounded decoder now handles UTF-8/BOM and supported declared Windows-1252/Latin-1 encodings consistently. It ignores fake script/meta declarations, retains literal mojibake supplied by a source, and preserves raw bytes and SHA-256. Regression fixtures cover Norwegian letters, punctuation, bulk write/read, extraction/serialization and both reported cases. There is no company-specific production repair.
* **Blocking work:** report construction, serialization and file writing ran synchronously on the event loop. They now use the existing bounded worker mechanism. Per-worker queue/wall/thread-CPU, process-CPU and GC thread-CPU diagnostics separate CPU work from waiting. Deadlines, cancellation, accounting and identity isolation remain enforced; timing assertions are unchanged.
* **Browser defects:** a disconnected progress endpoint fabricated a completed static run; it now preserves the last data and reports stale while polling. A 15-second heartbeat policy detects stale active runs. Unknown currencies remain blank/Unknown instead of becoming NOK in display/export.
* **Ownership false negative:** an unrelated “Våre kunder” heading rejected an independently identified owner. Complete own-brand title plus a real copyright footer with the single exact organisation number can now establish ownership; foreign and script-only footers still fail. The final correction compares full names across word spacing (`TUBING TEC AS` versus `TubingTec AS`) without rewriting published identity. Saved page `075cace4fba076890a5046d8dc7e77010236ffe15da89317a4f0cb44afef13d1` passes using the **actual registry context**. Earlier manual validation used the wrong spacing; that check alone was insufficient. `footer-actual-context.json` records the corrected check.

The earlier [final evaluation](final-feature-evaluation.md) is preserved as historical evidence. Its two corruption findings, inability to exercise a browser, requirement for universal source success, and combined-activity count are superseded here.

## Verification at the fixed tree

| Check | Result and scope |
|---|---|
| Targeted ownership/adversarial regressions | 30 passed; actual saved page/context independently passes |
| Full suite | **391 passed in 53.32s**; `closed-tests.log`, JUnit `closed-tests.xml` |
| Separate coverage | **391 passed in 58.19s**; **5,416/5,914 statements = 91.5793%**, 498 missing, 4 excluded; branch coverage not enabled |
| Strict production replay twice | 31 declared HTTP fixtures; fixed observation `2026-10-15T10:00:00Z`; 5 input envelopes including duplicate/invalid; 40 published claims, 9 blobs, 22 synthesis sentences; identical complete claims, evidence, modules, synthesis and states; zero changes/observation changes; strict unexpected interaction failure enabled |
| Positive feature behavior | Parent + verified-subunit hiring produces 2 jobs; missing employer excluded; group contacts exclude sibling; nonempty descriptions/social/feed activity; deliberate accounts 503 remains failed |
| Fresh clone | `state/remediation-closed`, new venv, `uv sync --frozen --offline`; import confirmed clone source; actual strict production pipeline using only tracked manifest/blobs; complete semantic equality with both replays |
| Chrome | **23 interaction checks pass**, 0 page JS errors, 0 unexpected console errors; 3 intentionally induced progress endpoint errors retained |
| Static checks | `git diff --check` passes; credential pattern scan 0 matches; no configured lint/type checker in `pyproject.toml` |

Browser checks use installed Chrome headless, ephemeral contexts and localhost-only routing: dashboard total/filter scope, search/autocomplete and keyboard, pagination, comparison, evidence links/expansion, CSV/JSON downloads/currency, watchlist/saved views, denied storage, group labels/no sibling leakage, corrected Norwegian text, running/partial/failed/completed/stale/static/disconnected progress, themes/focus, desktop/tablet/mobile overflow. Executable harness: `scripts/browser_verify.py`. Results/downloads and nine screenshots: `out/remediation/browser-results/`, including `desktop-dashboard.png`, `mobile-profile.png`, `tablet-directory.png`, `denied-storage.png`, `progress-stale.png`. Desktop/mobile images were visually inspected. Browser assets are unchanged by the later backend ownership fixes; browser data is regenerated archived100 plus synthetic state/group fixtures, not an independent truth set.

Earlier failed tests, harness attempts and logs remain available. Earlier 390-test runs emitted a harmless pytest-cache permission warning; the final runs disable the optional cache provider and pass. No assertion was relaxed. Coverage is run separately from all performance measurements.

## Live measurements and comparison

Both cohorts retain exact historical membership/order, fresh runtime state, websites/hiring/public-activity enabled, 64 workers, host concurrency 10, NAV detail concurrency 4, 10s request timeout and deadline fraction 0.85. Search queries and provider cap are zero. Budgets: 100 = 600s/2,000 requests/NAV 240s; 1,000 = 2,400s/20,000 requests/NAV 900s. HTTP counts include attempts/retries; DNS is separate. Bulk identity is used with live fallback; the 1,000 subset has 998 rows, with fallback for 936758932 and 993617512.

* 100 input SHA-256: `54de285dd71e69515c532febc37cfec16a467d7bc0880c96931fc6c83ecc807a`; bulk `a2d13b6b88ed7cf66a581bb99342c09cd7d55638e15ea6601d2fc6f680715e29`.
* 1,000 input SHA-256: `ae47e66f7a2cc14a85e0bc207c99d9029a32d826ae064eb9530389f23dd5f5a2`; exact historical `de2f6fa` cohort order; bulk `3f2de0601515a14db74936ee0958ad680535c45f57c8cbbd9c310c2fd96d8c83`.
* Final observations: 100 `13:26:46–13:27:45 UTC`; 1,000 `13:28:55–13:33:38 UTC`, 15 October. Declared index `nav-20261014T042640.758720Z-v1`, 9,015 ads, 403,768 compressed bytes, age 1.375/1.377 days.

| Metric | Previous measured | Current measured (`45ebf1e`) | Conditions / change / verdict |
|---|---:|---:|---|
| 100 wall / runner seconds | 90.653 / 86.109 | **58.604 / 56.609** | Same cohort/bulk, later live sources and different load; NOT DIRECTLY COMPARABLE as causal speedup; no controlled % claim |
| 100 HTTP / DNS | 574 / 761 | **577 / 764** | +3/+3 observed attempts; source behavior varies |
| 100 NAV total / feed seconds | 20.234 / 5.954 | **15.938 / 7.921** | Completed 6-page forward feed, no cohort candidate jobs; not a broken-hiring finding |
| 100 loop lag p95 / max ms | 25 / 104 | **25 / 41** | Responsive isolated observation, no unexplained systemic stall |
| Degraded no-bulk100 wall / NAV / lag p95,max | 500.216 / 242.719 / 2,900,10,931 | Bulk100 above | Different identity source and incomplete header processing; NOT DIRECTLY COMPARABLE |
| 1,000 runner seconds | 268.875 (historically labeled wall; timing scope uncertain) | **267.593**; external wall **283.141** | Same cohort/bulk; later feed/load, old external wall unavailable; NOT DIRECTLY COMPARABLE |
| 1,000 HTTP / DNS | 5,074 / 6,809 | **5,572 / 7,290** | +498/+481 observed; different forward feed and live responses |
| 1,000 NAV total / feed seconds | 141.312 / 2.547, 2 pages | **132.125 / 8.578**, 6 pages | 35 detail attempts; 9 ads/6 companies; feed/header complete, details incomplete for 3 explicitly reported scopes |
| 1,000 loop lag p95 / max ms | Historical comparable measurement unavailable | **72 / 572** | GC/CPU and resource constraints measured; no global deadline/output failure |
| Full tests | 375 passed in prior fresh clone | **391 passed** | +16 tests (+4.27%); suite changed |
| Statement coverage | 5,345/5,858 = 91.2427%, run had 3 timing failures | **5,416/5,914 = 91.5793%** | +0.3366 percentage points; changed denominator, previous run failed |
| Provider fees | $0 previous100 | **$0 both cohorts** | Paid search disabled; no model adapter |

The first isolated remediation measurements at `ec3702f` are retained: 100 wall/runner 64.968/61.422s, 577 HTTP; 1,000 wall/runner 368.597/346.547s, 5,577 HTTP. Diagnostic repeats followed a confirmed ownership false negative and a changed source tree, not selection of a faster/easier cohort. All runs are disclosed; no repeated crawl follows the final spacing correction. The old 57.77s NAV result is not a current measurement.

### Coverage and output safety

Counts below are companies with published facts, except jobs. Current means **measured** output, not predicted post-fix recall.

| Family | Previous100 → measured100 | Previous1,000 → measured1,000 | Interpretation |
|---|---:|---:|---|
| Identity | 100 → 100 | 1,000 → 1,000 | Stable |
| Accounts / roles | 99/100 → 99/100 | 998/997 → 998/997 | Stable |
| Subunits | 75 → 75 | 767 → 766 | 952814036 now returns checked-empty source data; no error |
| Official websites | 7 → 7 | 47 → 46 | TubingTec conservative false negative remains in measured artifact; final actual-context stored regression passes; count not retroactively changed |
| Social links | 5 → 5 | 29 → 29 | Stable company coverage |
| Jobs / hiring companies | 0/0 → 0/0 | 9/6 → 9/6 | Positive hiring separately proven in fixtures |
| Web activity | 1 → 1 | 4 → 4 | Source-derived dated web items |
| Registry activity | 13 → 13 | 114 → 114 | Derived from published registry dates, separately counted |
| Combined activity | **14 → 14** | **118 → 118** | Corrects earlier100 report's erroneous combined count of 1 |

Published claim-family counts (previous → measured1,000): identity 28,876→28,876; accounts 22,085→22,085; roles 11,323→11,323; subunits 6,332→6,325; website 342→329; hiring 9→9; activity 40→40. The machine report includes both cohort denominators. Removing unsupported claims is a quality correction, not automatically a coverage regression.

100: **100 valid terminal envelopes**, 93 complete/7 submission_error; 37 failed, 14 ambiguous, 2 blocked sections. Integrity verifies **6,977 claims, 390 blobs, 820 synthesis sentences**; stored-source audit all100 **6,977/6,977 correct**, zero incorrect/unverifiable/wrong-company/unsupported findings.

1,000: **1,000 valid terminal envelopes**, 924 complete/76 submission_error; 299 failed, 152 ambiguous, 10 blocked sections. Integrity verifies **68,987 claims, 3,849 blobs, 8,021 synthesis sentences**. Reproducible stored-source sample110 (including web/hiring/activity publishers) reviews **8,483/8,483 correct**, zero incorrect/unverifiable findings. These are conditional published-fact checks, not recall or independent live truth. Both runs: schema/membership pass, zero handled/unhandled exceptions, zero global deadline hits/output reductions and valid cited synthesis.

NAV detail discovery remains explicitly incomplete for 820918312, 912273938 and 935495369 (35-detail cap; 5 cap events). Failed discovery never becomes verified job absence. Forward-name fallback cannot cover unknown trading names.

## Stall diagnosis and source failures

Windows 11 build26300, Python3.12.15, Intel family6/model154, 16 logical CPUs, 16.77GB RAM. Benchmarks ran without pytest/coverage/browser/bulk processing. Unrelated system work continued. Final1,000 sampled system CPU mean19.84%/max57.2%, minimum available RAM2.004GB; earlier1,000 mean40.36% with only188MB available and 1,822ms max lag. This supports contention sensitivity, not a unique retrospective explanation or causal speedup.

Final100 uses 16.17s process CPU over57.89s monitor wall; final1,000 uses175.52s over282.28s. Final1,000 writer worker:93.109s wall/10.672s thread CPU; site13.297s/12.813s; blob-write max queue0.328s. The writer residual includes filesystem waits and OS descheduling, not pure CPU. GC maximum391ms includes390.625ms thread CPU; some GC runs on the main thread and can briefly pause responsiveness. There is no evidence of catastrophic executor saturation in the final runs. Pipeline peak RSS is **not measured**: the external driver's RSS is only the Windows launcher. Disk/load samples and complete worker metrics are retained, with that limitation explicit.

Historical timing failures subsequently pass unchanged, including full and coverage runs. Historical logs lack enough CPU/queue evidence to uniquely assign their severe stalls; they are neither proven code regressions nor dismissed as purely environmental. Demonstrated blocking report work is fixed; residual finite CPU/GC/I/O cost remains measured.

Every historical failed/blocked/ambiguous section is classified in machine evidence (270 rows): first100 33 legitimate abstentions, 11 external failures, 11 budget/deadline; no-bulk100 56 abstentions, 56 external failures, 103 budget/deadline. Activity withheld because website attribution/discovery failed is an abstention, not proof of no activity. No fixture/input or implementation defect is established by those error rows; publication/auditor/UI defects are investigated separately above. External DNS/outage/robots restrictions remain observable limitations. Universal source success is not an operational gate.

The conditional1,000 gate was met after the primary100: encoding resolved, no known material wrong-company/unsupported publication, bounded terminal outputs and no unexplained systemic stall. The later discovered conservative ownership omission was fixed and locally verified. Remaining source incompleteness is explicit; no known wrong-company publication is retained in the reviewed scope. Organiser brief authentication, hidden acceptance rules and official scoring remain unresolved external questions.

## Reproduction and commits

Run from repository root, setting `PYTHONUTF8=1`; this Windows environment uses `UV_CACHE_DIR=state/evaluation-uv-cache` for offline tool dependencies.

```powershell
.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider --junitxml=out/remediation/closed-tests.xml
uv run --offline --with pytest-cov pytest -q -p no:cacheprovider --cov=signalpost --cov-report=json:out/remediation/closed-coverage.json
.venv/Scripts/python.exe scripts/extract_bulk.py --bulk state/downloads/registry.csv --batch out/final-evaluation/live100-input.jsonl --output out/remediation/registry100.csv
.venv/Scripts/python.exe -m scripts.production_replay --input tests/fixtures/external_integration/batch.txt --manifest tests/fixtures/external_integration/manifest.json --fixtures-dir tests/fixtures/external_integration/blobs --output out/replay/envelopes.jsonl --report out/replay/report.json --state-dir out/replay/state --mode strict --websites --hiring --public-activity --workers 1 --observation-time 2026-10-15T10:00:00Z
uv run --offline --with playwright --with psutil python scripts/browser_verify.py --root out/remediation
```

For two replays use distinct output/state directories (`closed-replay1`, `closed-replay2`); compare with `scripts/verify_output.py --first ... --second ... --state-dir ... --count 5`. Fresh-clone logs are `closed-clone.log`, `closed-fresh-sync.log`, `closed-fresh-import.log`, `closed-fresh-replay.log`. Live reproduction uses `scripts/benchmark_run.py --input ... --bulk ... --output-dir <new-directory> --count 100 --input-sha256 <above> --time-budget 600` (1,000 uses count1000/time2400); exact executed commands are in the machine report and each `measurement.json`. Do not rerun these live commands just to inspect results.

Source commits: `4738385` shared decoding/auditor; `5eba5ad` bounded report offload/diagnostics; `ec3702f` progress/currency/browser harness; `d3a4337` independent footer ownership; `45ebf1e` complete-head test fixtures; `a11d4ec` complete-name spacing proof. The first footer fixture omitted a document head and initially failed; the fixture was corrected without relaxing its assertion. Documentation is committed separately from these measured/tested trees. Final branch/status and report hashes are recorded in `out/remediation/closeout.json` after the documentation commit.
