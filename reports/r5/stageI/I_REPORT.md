# Stage I - accounts history

Implementation commit: this commit; the exact hash is recorded in the final combined D/I summary. No push or publication.

The current official Brreg OpenAPI explicitly documents the available-copy years endpoint. The development access probe returned HTTP 200 without authentication; source_review/ preserves the schema, response and hashes, and links the official catalogue/NLOD terms. A failed robots lookup is recorded, not treated as permission for website crawling. This is direct use of the documented official machine API under the existing registry allowlist. No PDFs, subscriptions, models or paid APIs are used.

Every returned earlier SELSKAP statement now retains its own entity, period, currency, raw amount and source-declared unit. Duplicate period ends are suppressed; wrong-owner/malformed records are withheld. Figures require no additional requests. One extra official lookup publishes the available-copy year list and individually cited year facts, with explicit scope that this is not exhaustive lifetime filing history. The maximum supported filing year feeds the existing newer-filing flag alongside the identity registry year. Comparable-period YoY and labelled derived ratios still require supported compatible units and cite both figure inputs.

No unit/scale inference is used, including for current NOK figures. The earlier empirical whole-NOK annotation is removed. Refresh carry-forward also strips that known legacy inference during outages. All live financial units were undeclared, so derived ratios and YoY are withheld honestly; source-declared-unit positive cases still pass tests. Year-lookup errors preserve supported figures and publish explicit unavailable coverage. Unsupported history/recovery is a refresh observation, not an invented filing deletion. A removed copy-year fact cites the complete current list as its negative receipt.

## Measured defaults

Exactly the seven evaluator flags, both original hash-checked samples, new run IDs and fresh isolated state. The final source manifests match the final implementation. All enrichment defaults and 8/13 caps are unchanged.

| Metric | D frozen | I frozen | D daily | I daily |
|---|---:|---:|---:|---:|
| verified_websites | 6 | 6 | 3 | 4 |
| social_profile_companies | 3 | 3 | 0 | 1 |
| contacts | 12 | 12 | 6 | 8 |
| job_ad_companies | 0 | 0 | 1 | 1 |
| activity_companies | 100 | 100 | 100 | 100 |
| activity_claims | 1226 | 1226 | 1147 | 1147 |
| total_facts | 10517 | 13354 | 10722 | 13760 |
| http_requests | 583 | 685 | 633 | 770 |
| runtime_seconds | 107.594 | 332.360 | 157.406 | 374.109 |
| process_wall_seconds | 115.011 | 344.325 | 163.190 | 386.778 |
| Accounts facts | 4208 | 7045 | 4361 | 7394 |
| Companies with >=2 figure periods | 92 | 92 | 92 | 92 |
| YoY sentences | 0 | 0 | 0 | 0 |
| Companies with >=2 filed years | 0 | 93 | 0 | 92 |
| Filed-year facts | 0 | 929 | 0 | 1040 |
| Newer-filing flags | 0 | 0 | 0 | 0 |

Both final runs: exit 0, 100 ordered terminal envelopes, 100-company site, 200/200 complete five-topic briefings, zero unsupported values, within 1,850 HTTP and 2,100 seconds, $0. Each sample has 100 successful filing-year lookups and zero 429 responses. The largest profiles are 248,114 bytes frozen / 222,972 daily, below the unchanged 250,000-byte gate. I adds 2,837 frozen / 3,033 daily accounts facts. The daily total also gains five website/social/contact facts when SUNNCOM fresh proof succeeds again. Source variation is not attributed entirely to this code.

## Corrections retained as evidence

- trials/burst/: the initial 100-company burst produced 30 successful frozen lookups and 70 blocked scopes (210 HTTP 429 attempts). Generic per-request retries were insufficient. The final shared gate spaces new lookups by >=2.1 seconds, returns 429 as blocked without an immediate retry, and delays all queued lookups for >=60 seconds or a longer Retry-After. Other transient failures retain bounded registry retries inside the gate. Waiting uses the original deadline and grants no budget. The rejected burst artifacts are retained for both samples.
- trials/paced_site_failure/: all 100 lookups succeeded, but a full-history profile reached 254,879 bytes and the site failed its existing gate. Individual copy-year rows now link to the common year-list evidence panel; every claim and receipt remains in local data and the Evidence Explorer. This reduces the largest profile to 248,114 bytes without changing the gate or dropping facts.
- trials/pre_legacy_unit/: a passing fresh run before the final legacy-unit refresh safeguard. Both final samples were then rerun with the exact final source. The old run is not substituted for the final measurement.
- Historical offline replay bundles explicitly declare synthetic 404 filing-year availability responses for newly introduced routes. They do not fabricate historical filing facts or weaken strict replay. The manifests label them SYNTHETIC; dedicated tests cover successful real-schema year responses.

## Validation and hand checks

Full pytest: 895 green, including own-link careers, exact NAV employer proof, all history periods, source-only units, malformed/foreign records, independent year/value tampering, comparable-only YoY, positive newer-filing flag, rate-limit cooldown, hard global stop, failure/recovery idempotence, negative list receipts and legacy-unit outage refresh. Offline test spacing uses a fixture override; a controlled-clock test checks the production 2.1/60-second policy. Production CLI defaults are unchanged by that test fixture.

Headless Chromium 156.0.8078.4 passes 20 desktop/mobile checks at 1280/360 px: search by name/org number, profile, retained registry events, source URL/excerpt/retrieval/hash, year-list source jumps, all evidence rows, largest history profile and comparison. All tap targets >=44 px, no horizontal overflow, no JavaScript errors, external browser requests blocked. browser-final/ contains 18 screenshots and browser_results.json. Local QA code was authored in this repository and uses an already installed MIT-licensed Playwright dependency; no other repository application code was copied. A transient approval-service Bad Request prevented the first browser launch; the authorized retry succeeded.

Hand-check DIGITALIQ 918266917 in jobs.md (same single live NAV job; no frozen or careers job). SPEDIFY's future-opportunity invitation is not promoted to an active vacancy. Review INNLANDET REVISJON IKS 987769386 for three figure periods and its linked year list; review BIEN SPAREBANK 991853995 where unavailable figures stay explicit despite available filing years. Check source-declared units in any future record before expecting ratios/YoY. No live newer-filing flag was observed; positive/source-tampering cases are tested. Daily SUNNCOM site and two social links return with current proof; exact URL deltas/receipts are in new_websites.md. No other URL changes relative to D.

Code: MIT. Brreg registry/accounts data: NLOD 2.0 with attribution. NAV: official feed/reuse terms, current live details, no published job descriptions or contact-person data. Bundled SSB data: CC BY 4.0. Company-site factual excerpts retain their own terms. Model calls=0, paid search=0, provider cost=$0; compute/storage/network are excluded as in prior reports.

The final combined report is ../stageD/SUMMARY.md. Stop after I and that summary; do not start C.
