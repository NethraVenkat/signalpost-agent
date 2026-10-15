# Final feature evaluation — 15 October 2026

**NOT READY.** The measured live smoke contains incomplete sections, one confirmed description mismatch and an encoding-corrupted supplied bulk identity. Browser workflows could not be exercised because the automation inventory exposed no browser or app surfaces. Do not infer a competition score, rank, overall factual accuracy or recall.

Measured source: `cc21602` (production fixes `2cebfbf`; exact-byte fixture attributes `cc21602`), descendant of expected `f672439` and submitted `0d28df1`. Repository was clean on `main` at entry; origin is `https://github.com/NethraVenkat/signalpost-agent.git`. No push, deployment or email was performed. No AGENTS.md was found at the repository or checked ancestor locations. Existing Python processes were present; CIM command-line inspection was denied, so their purposes are UNVERIFIED and they were preserved.

Environment: Windows 11 build 26300, AMD64, Python 3.12.15, Intel64 Family 6 Model 154 Stepping 3, 16 logical CPUs. Hardware model, memory and exclusive-machine conditions are UNVERIFIED. Exact environment and organiser-file hashes: `out/final-evaluation/environment.json`.

## Requirements and source authority

Read README, docs/EVAL.md, docs/SOURCES.md, docs/RULES_COMPLIANCE.md and the original extracted starter kit at `C:/Users/Manish/AppData/Local/Temp/signalpost-stage0-bbf43b36cefb441aadfbeceaa7bc3626/extracted/signalpost-starter-kit`. Its README, OUTPUT_CONTRACT.md, external-connectors.md, competition-control-loop.md and norway-sources.md were inspected; file hashes are recorded. This local archive's correspondence with the organiser's latest version remains UNVERIFIED. The kit encourages a 100-company smoke and larger local tests. The contract requires evidence lists while proxy scorers read evidence dictionaries; the separate profiles output remains the documented resolution, not proof of hidden evaluator acceptance. No scoring weights were invented.

The original organiser brief and independently authenticated staff cache guidance remain unresolved. Repository compliance notes are secondary interpretations. README/docs contain stale test counts, conflicting output-cap wording and NAV concurrency claims; the measured configuration and code take precedence in this report.

Public [NAV feed documentation](https://navikt.github.io/pam-stilling-feed/), [NAV reuse terms](https://arbeidsplassen.nav.no/vilkar-api) and [Brreg dataset documentation](https://www.brreg.no/en/use-of-data-from-the-bronnoysund-register-centre/datasets-and-api/) were opened during this evaluation. NAV provides free access and a public experimental token, requires updates/removal of inactive advertisements, and distinguishes modification events from publication dates. Company-site robots, public-IP checks and bounded requests remain enabled. No social platform was crawled. Paid search was explicitly disabled.

## Confirmed fixes

1. Verified website publication crashed for companies with subunits: a list of subunit dictionaries was inserted into a set. Extract identifiers instead. The synthetic production replay now exercises this path.
2. Website descriptions appended claims before contact extraction, causing the contact extractor to receive a description rather than the website identity claim. Preserve the identity claim, including group relationship metadata; a regression asserts object identity across the two extractors.
3. A partner-directory mention with an exact organisation number was accepted as website ownership. Reject that context without independent entity-card/structured ownership proof. Existing multi-entity rejection semantics are preserved.
4. Denied localStorage access during theme initialization stopped later dashboard initialization. Catch read/write failures; executable Node regression checks denied reads and writes and successful theme toggling.
5. Offline replay now uses declared synthetic DNS and an optional timezone-aware fixed observation clock, with an isolated missing NAV index to prevent accidental use of live discovery metadata. Fixture response bytes have `-text` Git attributes.

## Feature matrix

PASS means the stated local scope was exercised; it does not establish hidden competition acceptance. Synthetic fixtures establish implementation behavior only.

| Requirement | Implementation | Test/runtime evidence | Status | Finding |
|---|---|---|---|---|
| Input validation, order, duplicates, terminal outputs | input_adapter, runner, shapes | evaluator input suite; strict five-row replay; live 100 membership verifier | PASS | Duplicate shares research; invalid input retained without published facts |
| Registry identity, roles, subunits, exact accounts | sources/brreg*, regnskap, financial_units | full suite; live 100; stored auditor | PARTIAL | 99 companies publish accounts; source failures explicit |
| Website discovery, ownership, redirects, groups | candidates, fetcher, proof | website suites; synthetic accepted group/rejected partner; live seven sites | PARTIAL | Two attribution/extraction defects fixed; recall ground truth absent |
| Entity versus group contacts, socials, descriptions | collector, descriptions, social | group fixture excludes sibling email/social; identity regression | PARTIAL | One live description mismatch remains in measured artifact |
| NAV employer proof, subunit mapping, dates, completeness | nav, nav_stream, nav_cached | NAV suite; synthetic two accepted jobs and missing-proof rejection; live feed complete | PASS | Live sample has zero candidate ads; no hiring recall claim |
| Activity publication/modification semantics | web/activity | activity suite; fixture asserts pubDate; live four claims | PASS | Website versus registry activity must remain separate |
| Synthesis, citations, unknowns, absence | synthesis, verifier | live 820 sentences, zero unverified values; replay verifier | PASS | Source incompleteness is explicit |
| Refresh/history/failures/idempotency | refresh/diff | refresh suites; fixed source second output: zero changes/observations | PASS | Live refresh was not remeasured |
| Evidence explorer and source/snapshot links | site, site.js | generated markup/provenance tests; source-body verification | PARTIAL | Click workflows and snapshot navigation not browser verified |
| Dashboard counts and scope | site, index scripts | membership/activity-count tests; 100 profiles/102 pages | PARTIAL | Browser rendering unverified |
| Search/autocomplete/filters/pagination/comparison | site.js | static generation tests and inspection | PARTIAL | Real interactions unverified |
| CSV/JSON, units/currencies/periods/formulas | exports, regnskap | export/formula/unit suites | PARTIAL | Download and spreadsheet-open workflows unverified |
| Progress lifecycle, counters, failures, disconnection, fallback | progress, runner, site.js | progress suite; live progress reached Pipeline complete | PARTIAL | Browser disconnect and static-fallback behavior unverified |
| Watchlists, saved views, financial views, storage errors | site.js | site suite; executable denied-storage theme regression | PARTIAL | End-to-end saved-view/watchlist storage errors not browser exercised |
| Responsive layout, keyboard, focus, themes, console | site assets | markup/CSS inspection and theme execution | UNVERIFIED | No available browser surfaces at desktop/tablet/mobile |
| Install, one-command run, no-key fallback, budgets, compliance | CLI, config, sources | frozen fresh-clone install; 375 tests; production replay; $0 smoke | PARTIAL | Exact organiser budget/cache acceptance still unresolved |

## Executed checks and artifacts

All paths below are relative to the repository. Large source bodies and generated output remain local under ignored `out/` and `state/`; the report is tracked independently.

- Entry revision: 371 tests passed in 95.59 seconds; coverage run 371 passed in 106.79 seconds. `out/final-evaluation/tests-basic.log`, `coverage-tests.log`, `coverage.json`, `pytest.xml`. Coverage scope `--cov=src`: 5,306/5,855 statements, 90.6234% (rounded 91%). This is statement coverage, not branch or factual coverage.
- Candidate full suite after the first fixes: 374 passed in 78.45 seconds, `candidate-tests-pass.log`. The fresh clone at `cc21602` includes the theme test: **375 passed in 68.15 seconds**, `fresh-tests.log`; frozen dependency install `fresh-sync.log`. A subsequent local coverage run completed **372 passed, three timing failures in 1366.71 seconds**, `final-tests.log`. The three unchanged cases then passed in4.88seconds (`timing-rerun.log`). Preserve both outcomes; the deadline test took28.672seconds against a3-second bound during severe execution stalls. No test threshold was weakened. Coverage was5345/5858 statements (91.242744964%), four excluded lines, no branch measurement.
- No lint or type checker is configured in pyproject.toml. `git diff --check` passed before the source commits. Do not label unconfigured lint/type checks as passed.
- Credential scan: `python dev-notes/scripts/scan_credentials.py`, zero matches, `credentials.log`. Its regex/extension scope is limited; this is not proof against all secrets. No secret values were emitted. Generated artifacts remain ignored; the new synthetic response bodies are explicitly tracked.
- Strict production replay twice: `fixed1/`, `fixed2/`; verifier `fixed-verification.json`: five envelopes, 40 published synthetic claims, nine supporting blobs, 22 cited sentences, zero unverified synthesis values, identical claim IDs, zero company changes and zero observations. The test also compares complete claims/evidence/modules/synthesis/section states. Run IDs and timing diagnostics are treated as volatile. Declared but unused fixtures are permitted; missing/corrupt/mismatched/exhausted/incomplete consumed fixtures fail strict replay.
- Fresh clone `state/final-evaluation-clone`, new .venv, only tracked fixtures, same documented production command: `fresh-replay.log` completed successfully with 31 declared HTTP fixtures. No source/body copying into the clone was needed. Candidate and submitted-baseline clones are clean. Although the baseline has no bundled replay script, applying the candidate harness externally to its unchanged installed runner succeeded; see the same-source comparison below. No compatibility code was added to either checkout.
- Live verifier: `live100-verification.json`, 100 envelopes, 6,977 claims, 390 source blobs and 820 cited sentences, zero unverified synthesis values. Site: 102 pages, 15,902,495 total bytes, largest profile HTML 125,571 bytes and data file 118,205 bytes, below the documented 250 KB profile bound. Output reductions/deadlines and unhandled exceptions: zero.
- Browser inventory returned apps=[] and browsers=[]: browser workflows and console errors **NOT RUN**, not passed.

## Current live benchmark

Measured source `cc21602`, seed 20261015, input SHA-256 `54de285dd71e69515c532febc37cfec16a467d7bc0880c96931fc6c83ecc807a`; public universe archive/content hashes and sample size in `sample.json`. Bulk extraction found 100/100 records (`bulk.log`). Bulk hash is in the machine run report. Runtime state was newly created at `out/final-evaluation/live100/state`; no runtime cache was copied. The shipped declared NAV index is a separate development cache: version nav-20261014T042640.758720Z-v1, 403,768 compressed bytes, 9,015 ads, 1.267 days old. This is **cold runtime / declared-index / live sources**, not an index-free cold run. Observation begins 2026-10-15T10:51:21.375358Z. The batch ran alongside verification work, so machine exclusivity is not established.

Exact command (PowerShell environment also removed BRAVE_SEARCH_API_KEY and SIGNALPOST_SEARCH_PROVIDER without printing values):

```powershell
.venv/Scripts/python.exe -m signalpost.cli run --organisations out/final-evaluation/live100-input.jsonl --bulk out/final-evaluation/live100-bulk.csv --output out/final-evaluation/live100/envelopes.jsonl --profiles-output out/final-evaluation/live100/profiles.jsonl --report out/final-evaluation/live100/report.json --site-dir out/final-evaluation/live100/site --state-dir out/final-evaluation/live100/state --websites --hiring --public-activity --max-cost-usd 0 --search-max-queries 0 --time-budget-seconds 600 --expected-count 100
```

Wall time 90.6528699 seconds; reported runner time 86.109 seconds (different scopes). HTTP 574, DNS resolver invocations 761, search queries zero, estimated provider cost $0. NAV total 20.234 seconds including scope dependencies; feed 5.954 seconds, five pages, six requests including token, 1,801,628 bytes, zero candidate/details, feed and discovery complete. Registry/subunit completion markers 13.781/5.609 seconds. Event-loop heartbeat 100 ms: p95 lag 25 ms, maximum 104 ms, 825 samples. These timings are not extrapolated to 1,000 companies.

Registry/NAV retries measured as repeated exact URL/company dispatches within their single-fetch paths: first run2registry/0NAV; no-bulk repeat21registry/0NAV. HTTP totals include these attempts. Website fallback/retry count is UNVERIFIED as a separate metric; do not silently equate it with zero or with DNS resolver invocations. Machine summary records this measurement definition.

100 outputs: 92 complete and eight submission_error; 37 failed section states, 16 ambiguous and two blocked across all section/company combinations. Eight incomplete website checks also caused explicit failed activity sections; one website request cap and external unavailability remain visible. Exit zero is output completion, not clean-source success. **1,000-company live: NOT RUN because the required 100-company smoke gate did not pass.**

| Family | Published claims | Companies with claims /100 |
|---|---:|---:|
| Identity | 2,888 | 100 |
| Accounts | 2,192 | 99 |
| Roles | 1,192 | 100 |
| Subunits | 636 | 75 |
| Website (all website fields) | 65 | 7 |
| Hiring | 0 | 0 |
| Activity | 4 | 1 |

Official websites: seven. Social URLs: seven claims across five companies. Website dated-activity companies: one. Mock-domain discovery is not a live search measurement; optional production search was disabled. The local bulk contains mojibake for at least one identity: org812573942 is stored as `RÃ˜RLEGGER 1 MOLDE AS` while the current official record says `RØRLEGGER 1 MOLDE AS`. This is an input/source encoding defect, not a name-change observation. A same-input no-bulk repeat was initiated in a new state directory; retain its separate report and conditions.

### Same-input live identity repeat (no bulk)

`out/final-evaluation/live100-official/` uses the same input hash/seed and source commit, all features and $0/search-disabled configuration, with live official registry identity instead of the corrupted local bulk and another empty state directory. Exact command is the first command above with `--bulk ...` omitted and every output/state/site/report path changed from `live100/` to `live100-official/`. Observation began2026-10-15T11:21:27.509673Z. Wall500.2158051seconds; runner461.937seconds;610HTTP;829DNS;$0. All100 envelopes have terminal state complete, but213 section states are failed and two blocked. Terminal completion therefore does not establish source completeness. NAV242.719seconds total versus43.484seconds feed, six pages, seven requests, zero details; feed_complete=true but header_processing_complete=false and failure_cause=nav_time_cap. Maximum/p95 event-loop lag10931/2900ms shows materially degraded execution; do not describe this as a normal performance regression or compare its runtime directly with the earlier100-company run.

Coverage: identity2888claims/100companies, accounts2192/99, roles1192/100, subunits636/75, website5/1, social0, hiring0, activity0. The losses coincide with source failures and execution stalls; there is no ground truth to establish recall loss. Verifier:6913claims,377blobs,796sentences,zero unverified values. All6913claims were reviewed against stored sources: identity2888/2888, accounts2192/2192, roles1192/1192, subunits636/636, website5/5; hiring/activity have zero denominators. Incorrect/unverifiable counts zero, precision and verification rate100% for each nonempty family. These are stored-source results, not independent live precision. Generated site102pages/15,911,203bytes; largest HTML126,823bytes and data118,818bytes. The1000-company run remains NOT RUN because the clean-source gate failed again.

Final coverage retry logged two further failures before being stopped after reaching57% during the same degraded environment. The completed fresh-clone375-test pass, failed372/3 coverage run and unchanged3/3 timing rerun remain separate outcomes. Do not silently discard the failure logs.

## Accuracy populations and limitations

Structural integrity and semantic agreement are distinct. The verifier validates evidence hashes/spans, membership and synthesis, not all claim meanings. The corrected auditor re-parses source fields and ownership contexts rather than accepting proof labels alone; its existing false-pass regressions ran. It is still a software auditor, not independent ground truth. Its description substring check caught a current text mismatch.

New 100-company collection, all 100 reviewed against their stored source bodies (`live-audit/reports/accuracy-audit-report.json`):

| Family | Published | Reviewed | Correct | Incorrect | Unverifiable | Precision (correct/verifiable) | Verification rate (verifiable/reviewed) |
|---|---:|---:|---:|---:|---:|---|---|
| Identity | 2888 | 2888 | 2888 | 0 | 0 | 2888/2888 | 2888/2888 |
| Accounts | 2192 | 2192 | 2192 | 0 | 0 | 2192/2192 | 2192/2192 |
| Roles | 1192 | 1192 | 1192 | 0 | 0 | 1192/1192 | 1192/1192 |
| Subunits | 636 | 636 | 636 | 0 | 0 | 636/636 | 636/636 |
| Official website | 7 | 7 | 7 | 0 | 0 | 7/7 | 7/7 |
| Social profiles | 7 | 7 | 7 | 0 | 0 | 7/7 | 7/7 |
| Other website fields | 51 | 51 | 50 | 1 | 0 | 50/51 | 51/51 |
| Website total (includes preceding three rows) | 65 | 65 | 64 | 1 | 0 | 64/65 | 65/65 |
| Hiring | 0 | 0 | 0 | 0 | 0 | N/A (0 denominator) | N/A |
| Activity | 4 | 4 | 4 | 0 | 0 | 4/4 | 4/4 |

Do not sum website subcategories and total twice. Aggregate stored agreement is 6,976/6,977, not overall factual accuracy. The finding is org 964624046, website_description.about_paragraph.682bbcaeef404520, body 7bef154551fb044a42008392449c126fb18c9c95eb696e879fada0bc96ad4e44: published text contains mojibake while the stored page decodes to normal Norwegian. Current Page extraction of those same bytes produces the correct text; the origin of the measured artifact's mismatch remains unresolved. Do not erase or relabel it as correct.

Older saved 1,000-company cohort re-audit (`stored-audit.json`, `stored-audit.log`): 68,990 published claims; stratified 110 companies, 8,500 reviewed/correct, zero incorrect/unverifiable. Family reviewed counts: identity 3,309; accounts 2,508; roles 1,394; subunits 914; website 326 (47 official, 64 social, 215 other); hiring nine; activity 40. All precision/verification-rate denominators equal those reviewed counts. This reproduces the prior stored-source result, not fresh collection. Independent post-batch registry re-fetch (`independent-live-verification.json`) reviewed five identity pairs: four matched, one differed due to the bulk mojibake (`registry-freshness-finding.json`). Pair agreement4/5 is not overall accuracy. No independent current website/hiring precision is asserted.

## Historical versus current comparison

### A. Same recorded-source functional regression

`state/final-evaluation-baseline` remains at0d28df1, with a separate frozen environment. `baseline-import.txt` verifies imports from that checkout. Run the candidate's external harness using its baseline Python (`.venv/Scripts/python.exe ../../scripts/production_replay.py` from the baseline directory), identical flags to the documented strict command, and paths to `../../tests/fixtures/external_integration/`; use local `out/replay` output/report/state. Set PYTHONPATH to the baseline's `src`. The baseline's source files were not edited. Both runners used the same31tracked HTTP fixtures, fixed2026-10-15T10:00:00Z, four workers, missing live NAV index and synthetic declared DNS. Strict replay completed without fixture integrity/matching failures. Full artifacts: `baseline-external-replay.log`, baseline `out/replay/`, candidate `fixed1/`, `same-source-comparison.json`, and the tracked machine summary.

Deduplicated functional comparison (five input records/three valid companies plus duplicate and invalid):

| Metric | Submitted0d28df1 | Candidatecc21602 | Absolute/percentage change | Interpretation |
|---|---:|---:|---|---|
| Wrong partner-directory website publications | 1 | 0 | -1 /-100% | Attribution correction |
| Sibling email publications | 1 | 0 | -1 /-100% | Entity-scope correction |
| Total official website publications | 2 | 1 | -1 /-50% | The removed publication was unsupported |
| Valid subject group website | 1 | 1 | 0 /0% | Preserved |
| Exact-parent/listed-subunit jobs | 2 | 2 | 0 /0% | Preserved |
| Dated activity claims | 1 | 1 | 0 /0% | Preserved |
| Unique available claims, all families | 29 | 26 | -3 /-10.34% | Includes removed unsupported site/contact/social data |
| HTTP requests | 29 | 29 | 0 /0% | Same declared-source scope |

This is synthetic functional evidence, not factual-accuracy coverage. Recorded runner timings20.234/6.297seconds have different observed timeout/stall conditions and are NOT DIRECTLY COMPARABLE as performance. No speedup is claimed.

### B. Live operational comparison

Original report paths and SHA-256 values: `historical-reports.json`. Historical input hashes, exact machine/hardware, environment flags and observation metadata absent from those reports are **UNVERIFIED**, not reconstructed from names. Submitted-v3 metadata records seed 20261024, measured_at 2026-10-14T14:25:37.827601Z, fresh runtime state plus shipped index. Older de2f6fa metadata records seed 20261018, measured_at 2026-10-14T06:33:03.155607Z and the same broad cache description. Seeds differ. The submitted report's $3.015 must not be assumed paid production search: its search configuration/mock assistance requires further attribution. No comparable speed/cost percentage is justified across these live populations.

| Metric | Historical value + commit | Current measured value + commit | Conditions/comparability | Change | Verdict |
|---|---|---|---|---|---|
| Runtime | 1328.094 s, 0d28df1; 268.875 s, de2f6fa | Bulk100:90.653 s wall/86.109 runner; live-identity100:500.216/461.937 s, cc21602 | 100 versus1000; seeds/live time/config and stalls differ | N/A | NOT DIRECTLY COMPARABLE |
| HTTP requests | 7319, 0d28df1; 5074, de2f6fa | Bulk100:574;live-identity100:610, cc21602 | Different population and source conditions | N/A | NOT DIRECTLY COMPARABLE |
| DNS resolver calls | 12205, 0d28df1; 6809, de2f6fa | Bulk100:761;live-identity100:829, cc21602 | Separate from HTTP; different scope | N/A | NOT DIRECTLY COMPARABLE |
| Provider costs | $3.015, 0d28df1; $0, de2f6fa | $0; zero queries, cc21602 | Search/mock configuration differs | N/A | No paid services enabled |
| NAV total | 141.312 s, de2f6fa; 57.77 s claimed elsewhere | Bulk100:20.234s/feed5.954s;live-identity100:242.719s/feed43.484s, cc21602 | Different scopes; second run capped/incomplete | N/A | 57.77 s original machine provenance UNVERIFIED |
| Websites | 47/1000, both reports | 7/100, cc21602 | Different seeds and time | N/A | Coverage, not recall |
| Social-profile companies | 31/1000 submitted; 29/1000 older | 5/100 companies, seven URL claims, cc21602 | Different populations | N/A | NOT DIRECTLY COMPARABLE |
| Hiring | 16 ads/8 companies, 0d28df1;9/6,de2f6fa | 0 ads/0 companies, cc21602 | No candidates in new sample | N/A | No inferred regression/recall |
| Web/combined activity companies | 4/118 of1000,de2f6fa | One website/combined activity company of100, cc21602 | Different populations | N/A | No recall claim |
| Tests | 371, f672439 re-executed | 375, cc21602 fresh clone | Same suite plus four regressions | +4 (+1.08%) | PASS |
| Statement coverage | 94.2% prior claim, config UNKNOWN;90.6234%, f672439 | 5345/5858=91.2427%, cc21602 | Same src statement scope for entry/current; current run had three timing failures | +0.6193 percentage points from entry | Earlier94.2 not comparable; mixed test outcome disclosed |
| Stored-source agreement | 8500/8500 older cohort | 8500/8500 reproduced;6976/6977 new100, cc21602 | Different populations; stored evidence only | N/A | One current description defect |
| Structural evidence | Historical release verifier stored result | 6977 claims/390 bodies verified, cc21602 | Local integrity, not factual accuracy | N/A | PASS in stated scope |
| Attribution | Historical proof labels insufficient alone | Directory/subunit/group regressions fixed; measured new100 no wrong-company findings | Audit assumptions remain limited | N/A | Fixes tested; no overall accuracy claim |

## Reproduction and remaining gates

Use new output/state directories for independent reruns; the live command above must not be reused with an already populated state path and called cold. Offline reproducible integration:

```powershell
uv sync --frozen
uv run pytest -q -o cache_dir=out/pytest-cache
uv run python scripts/production_replay.py --input tests/fixtures/external_integration/batch.txt --manifest tests/fixtures/external_integration/manifest.json --fixtures-dir tests/fixtures/external_integration/blobs --output out/replay/envelopes.jsonl --report out/replay/report.json --state-dir out/replay/state --websites --hiring --public-activity --observation-time 2026-10-15T10:00:00Z
uv run python scripts/verify_output.py --first out/replay/envelopes.jsonl --organisations tests/fixtures/external_integration/batch.txt --count 5 --state-dir out/replay/state
uv run signalpost site --input out/replay/envelopes.jsonl --out out/replay/site
python -m http.server 8765 --directory out/replay/site
```

Preview `http://localhost:8765/`; stop the local server afterward. Browser testing, description encoding discrepancy, clean live-source smoke, consistent local timing-test execution and organiser contract/cache/resource acceptance remain open. No1,000-company live result or percentage speedup is fabricated. Source commits are separate from the documentation-only report commit. Severe execution stalls and a failed Node file-read fallback are recorded rather than hidden. Final git status: clean after the documentation commit; the verification command and HEAD are captured in `out/final-evaluation/closeout.log`. Local generated evidence remains ignored. No preview server was left running by this evaluation.
