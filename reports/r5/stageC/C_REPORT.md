# Stage C - bounded proof-page discovery

Implementation commit: this commit; the exact hash is recorded in SUMMARY.md after the stage commit. No push or publication.

## Diagnosis and action

diagnosis.md/diagnosis.json use the actual F1 final runs. Every missing company is listed with state, exclusive primary cause, overlapping signals and saved attempt/request receipts. Primary buckets prioritize ambiguity/cutoff so the separate signal counts expose DNS/no-proof work hidden by a later cutoff. Robots includes access challenges; timeout includes connect/5xx. No candidate means no recorded nomination attempts; it does not assert no website exists.

| Cause | F1 frozen primary | F1 daily primary | C frozen primary | C daily primary |
|---|---:|---:|---:|---:|
| no candidate | 4 | 3 | 4 | 3 |
| DNS fail | 54 | 39 | 54 | 39 |
| timeout | 1 | 1 | 1 | 2 |
| robots | 3 | 4 | 1 | 5 |
| fetched-no-proof | 5 | 3 | 0 | 2 |
| veto | 6 | 13 | 11 | 14 |
| budget | 15 | 24 | 18 | 23 |
| ambiguous | 6 | 9 | 6 | 8 |

The largest cause is external DNS failure, followed by budget outcomes. No NXDOMAIN, timeout, robots refusal, foreign/group veto or ambiguous proof is bypassed. The two actionable issues addressed are budget ordering and fetched-no-proof discovery: own linked proof pages precede sitemap nominations, then blind fixed paths; known privacy aliases precede redundant bare /om guesses. A map request uses one existing slot, so a late blind alias can remain unchecked; tests require explicit cutoff instead of raising the cap. Existing strong registry/email/subunit/NAV candidate ranking is retained.

Own sitemaps only nominate contact/about/privacy/impressum pages. Per candidate, one map and at most one non-news page-map child are inspected; at most two sitemap-nominated HTML pages per company across both passes. Discovered proof-page URLs reject cross-domain/query-dependent/news targets and binary file suffixes. XML supplies no website proof: the fetched HTML must pass the unchanged identity scorer, exact number/corroboration, group/foreign veto and localized receipt rules. No HTTP/DNS/time allowance is added. Sitemap attempts/targets/cutoffs appear in run.refresh.proof_sitemaps.

Cloudflare active challenge markers, branded access-security gates and challenge titles are detected before identity scoring and before HTTP status retry/fallback, including text/plain challenge bodies and HTTP 403/503 gates. Blocked exceptions on own proof pages stop the candidate instead of continuing blind guesses. Ordinary recaptcha contact forms and passive Cloudflare scripts/jsd/main.js on a usable page are not access gates; a visible gate still blocks when JSD is present. Robots, public-IP pinning/TLS, terms, politeness, cumulative company/global budgets and once-only candidate veto/cache rules remain intact.

The instruction never to use sitemaps for news is applied to public activity as well as the new discovery path. Public updates now use explicitly linked RSS/Atom and bounded dated own-site HTML. Sitemaps cannot nominate news or supply lastmod claims. The corresponding activity/fact reduction is intentional; registry activity is retained and the measured difference is shown below.

## Accepted seven-flag measurements

Exactly --organisations, --bulk, --output, --profiles-output, --report, --run-id, --expected-count; original hash-checked seed 20261017/20261113 inputs; fresh state and new IDs. Both final C runs are sequential and use final source manifests. No enrichment/cap flags or paid services.

| Metric | I frozen | F1 frozen | C frozen | I daily | F1 daily | C daily |
|---|---:|---:|---:|---:|---:|---:|
| verified_websites | 6 | 6 | 5 | 4 | 4 | 4 |
| social_profile_companies | 3 | 3 | 3 | 1 | 1 | 1 |
| contacts | 12 | 12 | 11 | 8 | 8 | 8 |
| job_ad_companies | 0 | 0 | 0 | 1 | 1 | 1 |
| activity_companies | 100 | 100 | 100 | 100 | 100 | 100 |
| activity_claims | 1226 | 1225 | 1202 | 1147 | 1147 | 1137 |
| total_facts | 13354 | 13353 | 13325 | 13760 | 13760 | 13751 |
| http_requests | 685 | 692 | 689 | 770 | 775 | 773 |
| runtime_seconds | 332.360 | 593.000 | 347.984 | 374.109 | 383.782 | 369.500 |
| process_wall_seconds | 344.325 | 606.647 | 359.686 | 386.778 | 405.137 | 379.164 |
| Derived ratios | 0 | 153 | 153 | 0 | 169 | 169 |
| Comparable revenue YoY metrics | 0 | 50 | 50 | 0 | 63 | 63 |
| Distinct cited YoY sentence instances within profiles | 0 | 100 | 100 | 0 | 125 | 125 |

F1 restores dimensionless arithmetic without assigning absolute scale: matching exact-company statement, period, declared currency and unit field for ratios; matching unit fields (or both absent from the same approved entity schema), consecutive comparable annual periods and positive prior revenue for YoY. Every metric cites both inputs. Raw absolute amounts remain labelled unscaled where appropriate, and whole-currency sentence frames require declared matching units. Independent verification rechecks raw amounts/periods/currency/unit and statement/schema scope.

## Sitemap and access audit

- frozen: map attempt states `{"failed": 3, "nominated": 3, "not_available": 16}`; companies by nominated-page count `{"0": 97, "1": 3}`; new exact sites proved via map targets: 0; challenge companies: none.
- daily: map attempt states `{"failed": 4, "nominated": 2, "not_available": 19}`; companies by nominated-page count `{"0": 98, "1": 2}`; new exact sites proved via map targets: 0; challenge companies: none.

No recall gain is claimed when the strict proof does not support one. Source variation and access/cap failures are not proof of website closure. new_websites.md lists every added/removed site/social URL with organisation number, company, proof tier, exact excerpt, retrieval time, source URL and hash; unchanged URLs remain in url_inventory.json.

- stageF1/frozen to stageC/frozen: 0 added, 1 removed website/social URLs.
- stageF1/daily to stageC/daily: 0 added, 0 removed website/social URLs.

## Gates, trials and hand checks

Full F1 pytest: 899 green. Final C pytest: 912 green (pytest-release.txt); final focused suite: 96 green. Tests include positive hidden-map exact proof, two-page quota across candidates, one-child depth, cross-domain/news/binary/query rejection, malformed/DTD refusal, hard budgets/robots, veto stops, ordinary contact forms, passive JSD versus real gates, 200/403/503 challenges, own-link careers, financial scope/scale and all existing contracts. Earlier tests are retained; stale legacy assertions were updated to the new explicit sitemap policy, never by raising a resource/proof gate.

Each final run exits 0 with 100 ordered terminal envelopes, an available 100-company site, all five cited briefing topics, zero unsupported values, HTTP <=1850, completion within 2100 seconds and $0. audit.json rechecks the seven flags, final source hashes, <=13 cumulative website HTTP, two nominated-page quota, no sitemap news, and the unchanged <250000-byte profile gate. Review exact section states rather than treating exit 0 as source success. Financial metrics are dimensionless; no future performance or commercial suitability is inferred.

Headless Chromium 156.0.8078.4 passes 20 checks at 1280/360 px on the final recovered frozen site: search by name/org number, profiles, complete retained registry timeline/source receipts, restored financial briefings, filed-year source jumps, largest history profile, all evidence and comparison. Eighteen screenshots are in browser-release/, including mobile-financial-row showing unknown absolute unit. Targets >=44px, no horizontal scroll/JavaScript errors; external browser requests blocked. All QA/application code is authored within this repository; only an installed Playwright dependency is used, with no application code copied from another repository.

Retained trials: pre_transport/ includes initial proof-scoring-only runs and browser evidence; html_only_transport/ preserves the later incomplete implementation run, its complete output reverified independently, and the report-postprocessor collision failure. passive_jsd_false_block/ retains both audited trial samples and the historical URL receipt for a false DIGITALIQ removal: a broad challenge-platform matcher mistook passive JSD for an interactive gate. The final rule excludes passive JSD on usable pages and still blocks active/visible gates; both samples were remeasured. A host no-progress interval inflated trial runtimes. One superseded wrapper read the newer run's fixed report directory; its own report/counts were reconstructed and independently reverified in the trial folder, not accepted as final metrics. Final measurements are sequential, have their own fresh state, and pass the final audit. Further tests caught text/plain gates and swallowed blocked exceptions; final source handles both. An automatic approval-review timeout delayed the final test launch; the authorized single retry succeeded. No trial output is substituted for an accepted run.

The unchanged-code dns_outage/ pair is retained separately: the frozen run had 15 role, 16 figure and 19 filing-year checks reporting OS name-not-found failures; the daily run had seven incomplete subunit/hiring scopes. These were not converted to success or replaced with historical proofs. One fresh recovery run per sample followed; accepted comparison rows use those later runs and the source-failure pair remains inspectable. The daily reporting wrapper also exposed a counting bug when a state was absent from the baseline: the helper now includes newly observed states and regenerated its table from saved output without a crawl. All retained outputs independently verify zero unsupported values. Passive JSD behavior was checked against the vendor's official documentation; passive_jsd_review.json replays DIGITALIQ's saved body and exact number without a live fetch or publication carry-forward.

Hand checks: compare F1 and C proof URL inventories; inspect any removed URL's current failure plus historical proof, never promote the historical receipt. Check the map-nominated candidate pages in audit.json/diagnosis_after.json: a nomination is not identity proof. Inspect challenge receipts for the org numbers in audit.json and the complete request ledgers, and verify no follow-up guess or alternate host bypassed a blocked candidate. For F1, inspect a matching-missing-unit ratio and a comparable YoY example alongside the raw amount's unknown-unit label; both input citations are retained. SPEDIFY and INNLANDET REVISJON IKS profiles exercise the restored arithmetic and source panels. Registry-only activity remains available even where public website checks fail.

Cost/models/licences: $0 provider fees; model calls=0, paid search=0. Code and Playwright retain MIT, Brreg NLOD 2.0 attribution, NAV official reuse terms and SSB CC BY 4.0; company content retains its own terms. Compute/storage/network excluded as in prior reports. No push, publication or next stage. Commit C, commit the combined SUMMARY.md, then stop.
