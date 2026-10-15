# Revision improvements — 15 October 2026

**READY FOR REVISION**, within the verification scope below. Candidate source: **`2b0f633a92ffcfc164f80954457888d33375a35c`**. Started clean on `main` at `aeddf4d`; submitted `0d28df1` remains an ancestor. No push, deployment, email, history rewrite, paid service or unidentified-process termination occurred.

The revision fixes redundant NAV detail work, CSV formula-prefix gaps and missing visible last-successful-check timestamps. It closes the final ownership verification gap through production collection, verifies refresh transitions and a genuinely empty-package-cache installation, and measures the actual pipeline process. It does **not** establish a general website recall gain or an official score. [Machine evidence](revision-improvements.json) and [local submission checklist](revision-submission-checklist.md) accompany this report.

## Limitation register and outcomes

| Limitation / classification | Evidence and evaluation effect | Verification / success criterion | Effort / outcome |
|---|---|---|---|
| Final ownership/source alignment — verification gap | Last benchmark preceded spacing correction; potential missed company | Actual registry name + destination bytes through collector/dependent extraction; final 100 at candidate | Medium; passed, no historical counts rewritten |
| Website omissions — conservative abstention/external/budget | Measured 1000 had 46 sites; unknown-company recall unavailable | Inspect declarations/email/subunits/followups/redirects/XML; require independent exact-entity proof for any recovery | Medium; no further safe discovery mechanism established |
| NAV detail cap — confirmed redundant work | 35 successful attempts/20 URLs; historical incomplete scopes 820918312,912273938,935495369 | Coalesce checked versions without increasing cap; same saved fixture/ad output, fewer attempts; newer versions still checked | Medium; controlled 2→1; historical aggregate completeness remains unproven |
| Refresh — verification gap | Existing helper tests insufficient for full transition matrix | Actual-runner changes, failures/recovery, closure, idempotency, ordering and restart | Medium; passed controlled cases |
| Installation — verification gap | Prior clone used warm offline cache | New clone/venv/empty package cache, ordinary downloads and tracked-fixture production execution | Medium; passed; installed Python reused |
| Memory — measurement defect | Old RSS described launcher only | Root plus recursive descendants sampled every 1 s; observed peaks/limitations explicit | Small; actual pipeline 166.62 MB, tree 171.03 MB observed |
| Timing variability — remaining environment/performance limit | One unchanged timing assertion failed during coverage | Preserve logs; inspect CPU/queue/GC/writer; isolated and full repeat unchanged; one final live run | Medium; final checks pass, finite jitter remains |

## Confirmed changes and production-path evidence

**Ownership:** `scripts/verify_stored_website.py` replays original destination SHA `075cace4fba076890a5046d8dc7e77010236ffe15da89317a4f0cb44afef13d1`, exact org 932761483 and actual registry name **TUBING TEC AS**. Production collection returns an available verified website, description, email, phone and brand. The candidate is nominated by a legal-name slug; the registry row has no declared website/email. Nomination is not ownership evidence. The existing final proof correction suffices; no new proof relaxation was needed. Destination transport/redirect metadata is not reconstructed, and an unrecorded `/kontakt` followup fails explicitly. There are zero network requests in this check. Partner/customer mentions without independent ownership, foreign/script-only footers, similar names and sibling group contacts remain rejected in targeted/full tests.

**Permitted discovery:** offline review finds 111 registry website declarations, all parseable,236 email declarations,112 permitted email-domain nominations and 3,361 bounded slug nominations in the 998-row historical subset. Those are candidates, not verified companies. The failure funnel contains repeated diagnostic observations and must not be summed as unique companies. Cross-domain redirects, blocked sources and insufficient corroboration do not authorize ownership. Existing verified-subunit relationship evidence, email candidates, bounded contact/about followups and sitemap/feed paths are retained. No speculative connector or additional nomination strategy was added. Additional discovery candidates from this stage:0; no measured coverage/request/latency gain is claimed. TubingTec's stored recovery is separate from a fresh aggregate 1000 result.

**NAV:** scope/header preparation could enqueue a detail version already in flight; dequeue did not notice that the version had since completed. It spent another request/cap slot on identical evidence. Dequeue now drops checked/failed versions. Failure bookkeeping is version-specific, allowing a genuinely newer feed version to be checked. Pending nominations merge affected subjects. Exact parent/subunit authorization, retries, request/cost accounting and all caps remain unchanged. A production-prefetch controlled fixture at baseline `a11d4ec` and candidate uses **2→1 detail attempts (−50%)**, identical published ad values and complete discovery in both. This is a controlled scheduling comparison, not measured live recall or overall runtime improvement. Newer versions still refetch; 304 responses reuse only conditionally revalidated bodies. No new fairness policy or unvalidated cached-detail publication was introduced.

**Refresh/exports:** controlled actual-runner tests cover unchanged facts, legal name/address changes, a financial period/value change with old/new evidence, changed website/contact,429/503/DNS/connect/timeout failures, partial failure/recovery, duplicate rows and cancellation/restart. Separate runner transitions cover changed job title/evidence, inactive/deleted closure,304 reuse, failed detail and partial feed without false closure/absence. Unchanged snapshots create no company events; failures retain eligible facts with original evidence and successful-check time. Hiring still requires current live detail proof and is not retained as freshly active after failure. Retrieval/observation timestamps remain distinct from source reporting dates. Carried facts now display their last successful check. Python and browser CSV exports guard formulas hidden behind C0/C1 controls, Unicode whitespace/BOM/zero-width prefixes, with proper quote/newline handling and no formula-based identifier formatting.

## Final validation, including the failed attempt

| Check | Result |
|---|---|
| Full suite at candidate tree | **401 passed,106.60 s**; no timing assertion changed |
| First separate coverage | **400 passed,1 failed,263.01 s**; `test_deadline_partial_progress` took 21.859 s against its 3 s assertion |
| Isolated coverage rerun | **1 passed**, original 3 s assertion; total pytest duration 67.01 s includes framework/import/reporting overhead |
| Full coverage repeat | **401 passed,169.18 s**; **5,428/5,920 statements=91.6892%**;492 missing,4 excluded; branch coverage not enabled |
| Targeted checks | Ownership/adversarial 60 pass; NAV 39 pass; runner refresh/site 31 pass; eight additional controlled NAV transition assertions pass |
| Strict replay twice + cold clone | 31 declared fixtures;5 envelopes including duplicate/invalid,40 published claims,9 supporting blobs,22 synthesis sentences;0 unexpected interactions |
| Complete determinism comparison | **Every envelope value equal** across both replays and cold clone, excluding only `/run_id`, `/run/run_id`, `/operations/runtime_ms` |
| Cold installation | New `state/revision-cold` clone/venv; initially absent `state/revision-cold-cache`; `uv sync --frozen` prepared 25 packages with network downloads; actual tracked-fixture pipeline passes |
| Browser | **25 Chrome interaction checks pass**,0 page JS errors,0 unexpected console errors;3 deliberately induced progress-endpoint errors retained |
| Lint/types/secrets | No configured lint/type checker; diff check passes; credential pattern scan 0 matches; generated data excluded from Git |

The first coverage failure is retained, not relabeled a pass. Its monitor recorded 1.0 s process CPU over 21.36 s wall, no recorded GC pause/worker queue delay, and writer 18.203 s wall/0.3125 s thread CPU. This identifies waiting/descheduling around output work, not CPU saturation, but does not uniquely establish an OS/filesystem cause. The complete unmodified repeat passes. Initial development harness runs also failed on fixture/setup and expected-field errors; their logs remain under `out/revision/`, followed by the passing targeted runs. No established production or timing assertion was relaxed. Final live loop jitter and low available system memory remain limitations, not evidence of a guaranteed responsiveness bound.

Cold installation reused the preinstalled Python 3.12.15 runtime on Windows 11 build 26300; it was a cold **package** install, not a new OS/Python installation. No ignored outputs/state/environment were copied to the clone. Its imported module path points into that clone. Search was unconfigured with 0 queries and$0 cost. PowerShell decorated uv's normal stderr startup message as `NativeCommandError`; uv returned 0, installed successfully and the resulting environment executed integration.

Chrome used isolated temporary contexts and localhost-only page routing, without personal profiles/accounts. Checks cover progress running/partial/failed/completed/stale/static/disconnected states; evidence and downloads; currencies; hiring filter; watchlists/saved views with normal/denied storage; keyboard/themes; tablet/mobile overflow and group labels. The added CSV cases exercise downloaded browser files. Nine screenshots and executable results are in `out/revision/browser-results/`; desktop/mobile were visually inspected. UI data is the archived 100 regenerated at candidate plus declared synthetic integration/state cases.

## One final 100 live observation

The [current primary evaluation contract](https://builderr.ai/docs/signalpost-evaluation-harness.md) specifies a supplied per-run batch/resource budget. It does not publish the supplied listing's numeric 45 min/2,000/$10 limits. The [current challenge page](https://builderr.ai/challenges/signalpost) requests a 100-company smoke report and says precomputed profiles are not scored. Downloaded contract/brief/source-policy copies and hashes are retained. This task uses conservative explicit **600 s,2,000 HTTP attempts,$0 provider cost**, without claiming those settle future organiser budgets or DNS accounting.

Input SHA-256: `54de285dd71e69515c532febc37cfec16a467d7bc0880c96931fc6c83ecc807a`; unchanged membership/order. Bulk SHA-256: `a2d13b6b88ed7cf66a581bb99342c09cd7d55638e15ea6601d2fc6f680715e29`. Fresh state; websites/hiring/public activity on;64 workers, host 10, NAV 4;10 s registry timeout,0.85 source deadline fraction; website/domain protections unchanged. Declared NAV index `nav-20261014T042640.758720Z-v1`,9,015 entries,403,768 compressed bytes, age 1.43994 days. No tests, browser, installation or bulk preparation ran concurrently. **Only one live attempt in this revision.**

Windows 11/Python 3.12.15,16 logical CPUs,16.77 GB RAM. Observation **15:00:09–15:01:19 UTC,15 October**. Sampled system CPU mean 41.86%, minimum available RAM 845,615,104 bytes. Unrelated processes were preserved.

| Metric | Previous observation (`45ebf1e`) | Candidate measured (`2b0f633`) | Change / interpretation |
|---|---:|---:|---|
| Wall / runner seconds | 58.604 /56.609 | **69.560 /65.156** | Wall+10.956 s,+18.70%; slower later observation, not a controlled regression attribution |
| HTTP / DNS | 577 /764 | **572 /755** | −5 HTTP/−9 DNS; later source behavior |
| Repeated-URL accounting | Not reclassified here | 17 additional same-subject/URL attempts;10 follow prior failure/transient status | Raw attempts retained; repeated checks and transport retries are not interchangeable |
| Provider cost / search calls | $0 /0 | **$0 /0** | Stable |
| NAV total / feed seconds | 15.938 /7.921 | **28.015 /8.390** |6 pages,0 candidates/details; non-feed residual 19.625 s includes dependency readiness/scoring/scheduling, not an extra 19.625 s of feed transport |
| NAV completeness | Complete | **Feed/header/detail scope complete** | No sample jobs; positive hiring independently tested |
| Loop lag p 95 / max ms | 25 /41 | **71 /1,244** | Worse observed jitter; current load/memory differ; no global deadline/output failure |
| Pipeline memory | Unmeasured; launcher-only RSS | **166,621,184 bytes pipeline peak;171,028,480 bytes root+descendant peak** |1 s sampling; brief peaks may be missed, summed RSS can double-count shared pages |
| Valid terminal outputs | 100 | **100**,93 complete/7 submission_error | All inputs retained |
| Failed / ambiguous / blocked sections | 37 /14 /2 | **41 /14 /2** | Source availability differs; publication counts below stable |
| Websites / social companies | 7 /5 | **7 /5** | Stable |
| Jobs / hiring companies | 0 /0 | **0 /0** | Stable sample; no name-only publication |
| Web / registry / combined activity companies | 1 /13 /14 | **1 /13 /14** | Stable; separately counted |
| Stored-source agreement | 6,977/6,977 | **6,977/6,977**,all 100 |0 incorrect/unverifiable/wrong-company findings; not independent truth/recall |
| Tests / statement coverage | 391 /91.5793% | **401 /91.6892%** |+10 meaningful tests,+0.1099 percentage points; denominator changed |
| Browser checks / install | 23 /warm-cache clone | **25 /empty-package-cache network install** | Broader verification |

Identity/accounts/roles/subunit claim counts remain 2,888/2,192/1,192/636; website 65 and web activity 4 claims remain unchanged. Integrity verifies 6,977 available claims,390 supporting blobs and 820 cited synthesis sentences. No global deadline hits, handled/unhandled exceptions, output reductions or schema/membership failures. All published families are checked; zero jobs has a zero publication denominator, not a 100% precision result.

HTTP counts include attempts/retries, robots and NAV token/feed calls. DNS is separately 755; HTTP+reported DNS is 1,327, still below 2,000 arithmetically, but connection attempts/TLS and the organiser's definition are not independently settled. The earlier 20,000-request development allowance is not evidence of daily 2,000-request compliance.

Process CPU 29.98 s over 67.81 s monitored wall; writer 21.078 s wall/2.141 s thread CPU; max recorded source queue 0.171 s; site 2.250 s/2.000 s. GC max 94 ms (worker thread). These measurements separate finite CPU/GC/queue cost from larger waiting/descheduling residuals; they do not uniquely explain every 1,244 ms pause. No additional live repeat was made to select a better result.

## Full 1000 review package and remaining limits

**No new 1000 live run.** The concrete scheduling question is answered with controlled production replay; another crawl is unnecessary. The historical source snapshot remains at `45ebf1e`:46 websites,29 social companies,9 jobs/6 companies,4 web-activity and 114 registry-activity companies;118 combined. Its last measured wall 283.141 s/5,572 HTTP is historical, not candidate performance. The three historical NAV incomplete scopes are not declared repaired in aggregate: exact archived forward-feed bodies were not retained, and deduplication tests do not prove exhaustive live discovery.

The entire stored 1000 cohort is revalidated for schema, order/membership, all evidence references and synthesis:68,987 published claims,3,849 supporting blobs,8,021 sentences. Presentation is regenerated with the candidate. There are **1,000 company pages,1,002 total HTML pages**,156,917,439 total site bytes. Maximum actual profile HTML 133,317 bytes; per-profile data JS 133,843 bytes; raw profile JSONL line 173,384 bytes. This is a full-cohort artifact check; the earlier 110-company stored-source sample 8,483/8,483 remains a historical sampled check.

Local delivery: `out/revision/revision-profiles1000.zip`, external `profiles1000-manifest.json`, `package-summary.json`. The ZIP supplies raw profiles, envelopes, batch, registry subset, generated site and **all 4,083 referenced evidence blobs**, including records beyond the 3,849 supporting current available claims. Every packaged file has a SHA-256; archive contents are read back and verified. Package SHA/size are in the machine report. `out/revision/evidence-manifest.json` separately hashes final100 outputs/state/site, browser captures/downloads and retained logs. Keep ZIP and manifest together through revision review, along with the original source directory; extract to a new folder and open `site/index.html` offline. Large evidence remains outside Git and has not been uploaded or emailed.

Remaining limits: no independently measured recall or official score; sparse permitted website coverage and legitimate/external/budget abstentions; unknown trading-name discovery; unproven aggregate closure of the three old NAV scopes; timing jitter and one historical coverage failure before successful repeats; sampled rather than continuous memory, with 1000 pipeline peak still unmeasured. No known material wrong-company or unsupported publication remains in the reviewed scope. These limits preclude a qualification or score guarantee.

## Reproduction and commits

Use Python 3.12+ and `uv sync --frozen`. Full suite: `uv run pytest -q -p no:cacheprovider`. Coverage: `uv run --with pytest-cov pytest -q -p no:cacheprovider --cov=signalpost --cov-report=json:out/coverage.json`. Strict replay uses `python -m scripts.production_replay` with tracked `tests/fixtures/external_integration/{batch.txt,manifest.json,blobs}`, fixed observation `2026-10-15T10:00:00Z`, strict mode, all three external feature flags and distinct output/state directories. Exact executed live command, parameters, timestamps and artifact hashes are in the machine report and `out/revision/live100/measurement.json`. The stored ownership command is documented by `scripts/verify_stored_website.py --help`; browser command is `uv run --with playwright --with psutil python scripts/browser_verify.py --root out/revision` after generating its two documented sites. Do not rerun a live crawl merely to inspect these results.

Implementation/verification commits: **`29186d4`** collector ownership replay; **`e93c937`** NAV coalescing; **`7006067`** runner refresh verification, successful-check display and CSV protection; **`2b0f633`** actual-process memory and browser cases. Release documentation is committed separately. Final HEAD/status and report hashes are recorded after that commit in `out/revision/closeout.json`.
