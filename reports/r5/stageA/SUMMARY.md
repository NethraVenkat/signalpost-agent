# Stage A0 and Stage A - final report

Completed A0 and A on revision/r5. All commits use Nethra Venkat <nethravenkat510@gmail.com>. No git push, publication, paid search/model call or Stage B. Proof tiers, exact company/subunit identity checks, vetoes, robots/terms, TLS/SSRF protection and politeness remain enforced.

## Commits and gates

| Stage | Commit | Full pytest |
|---|---|---|
| Stage S comparison | 74cd0ad | 805 passed |
| A0 default enrichment / hard limits | 7df7afd | 822 passed in 198.07s |
| A adaptive scheduler, evidence and this report | This commit, directly following 7df7afd | **838 passed in 213.11s** |

The final source tree matches source_manifest.json (including newly added files); release_audit.json checks that fingerprint, exactly seven CLI flags, request/pass totals, cumulative website/DNS maxima and completion. See tests.txt for the final green gate. Previous failed and green diagnostic gates are retained, with no timing-threshold or proof-assertion relaxation.

## A0 - enrichment by default

The seven evaluator flags now enable websites, hiring and public website activity in CLI and library defaults. --no-websites, --no-hiring and --no-public-activity disable them; positive flags remain compatible. Website caps stay 8/13 defaults and upper bounds. README's runnable example uses only the official seven flags and explains the actual defaults.

One shared meter limits all HTTP sources, shared NAV traffic, robots, redirects and retries to floor(1850 * unique inputs / 100). An explicit max-requests can only lower it. Default time is 2,100 seconds, clamped to 21 seconds per unique input with a crawl cutoff and output/site reserve. Duplicate input rows cannot inflate limits; slow preparation cannot extend the network deadline. Report.limits, enrichment and completion make effective controls/results explicit.

## Measured frozen 100

All accepted measurements use the same hash-checked seed-20261017 companies and frozen registry subset, fresh state and new run IDs. A0 and A use **exactly seven flags**, without cap, feature, adaptive or state-dir flags. A fresh working directory isolates the default state/. Metadata retains exact argv, environment, resolved defaults and output hashes. Stage S used explicit full-feature flags.

| Metric | Stage S full-feature | A0 seven flags | A seven flags |
|---|---:|---:|---:|
| verified_websites | 6 | 6 | 5 |
| social_profile_companies | 3 | 3 | 3 |
| activity_companies | 31 | 31 | 31 |
| activity_claims | 90 | 90 | 90 |
| total_facts | 9381 | 9381 | 9378 |
| locations | 73 | 73 | 73 |
| job_ad_companies | 0 | 0 | 0 |
| contacts | 12 | 12 | 10 |
| http_requests | 887 | 904 | 905 |
| runtime_seconds | 255.094 | 299.625 | 457.390 |
| process_wall_seconds | 262.766 | 325.795 | 504.951 |
| Social URLs | 8 | 8 | 8 |
| Jobs (available claims) | 0 | 0 | 0 |
| website / failed | 18 | 16 | 17 |
| activity / failed | 25 | 23 | 24 |
| hiring / failed | 11 | 11 | 11 |
| accounts / failed | 1 | 1 | 1 |
| Provider cost USD | 0 | 0 | 0 |
| Global HTTP cap | 2000 | 1850 | 1850 |
| Requested time ceiling (seconds) | 2400 | 2100 | 2100 |
| Site companies / HTML pages | 100 / 102 | 100 / 102 | 100 / 102 |

A0 restores six websites and all Stage S fact counts to the actual evaluator command. In the final A run SPEDIFY is retained, including its numeric LinkedIn URL. INNLANDET REVISJON IKS (987769386), https://irev.no, is withheld after fresh registry-host timeouts and exhaustion of its cumulative allowance. Its website and two contacts account for the three fewer facts. This is a live check failure, not a claim the old website was wrong. All social URLs are unchanged. BIEN accounts still returns HTTP 500; 11 hiring sections remain incomplete, so zero verified jobs is not a claim that none exist.

The final A process finishes in **504.951s wall time**; report.completion includes outputs/site at **501.609s**, within the requested/scaled 2,100s limit. The site is available for all 100 companies. Maximum observed website HTTP is eight per company and maximum DNS nominations is eight (a www/non-www pair is one nomination). Actual HTTP is 905/1850. Both A0 and A independently verify 100 complete cited briefing contracts, 4,208 financial values, 153 derived ratios and **zero unsupported synthesis/briefing values**. Report exceptions/warnings are zero for the accepted A run. HTTP/runtime differences include live source and machine-load variation; they are not attributed entirely to the code.

## A - adaptive two-pass scheduler

Pass 1 preserves the measured registry-homepage/email and two strongest full-name priorities; branch/provider contacts, current live NAV employer homepages and remaining name variants also nominate within the original ceilings. NAV nominations require a saved active detail with the exact employer number or a currently registered subunit. Feed-header/index names never authorize publication.

After pass 1 and shared source processing finish, pass 2 ranks untried candidates by source strength and .no preference within each tier. It uses the same cumulative HTTP/DNS counters, original deadline, veto set, robots gates, candidate/page caches and proof functions. Exact-number proof stops further work for that company. No budget is reset to force a gain.

| Pass | All HTTP | Website HTTP | Exact websites gained |
|---|---:|---:|---:|
| pass1 | 905 | 243 | 5 |
| pass2 | 0 | 0 | 0 |

Pass 2 runtime: 0.593s. Per-company outcomes:

| Outcome | Companies |
|---|---:|
| already_verified | 5 |
| checked_no_gain | 1 |
| dns_budget_exhausted | 14 |
| no_pending_candidates | 68 |
| website_budget_exhausted | 12 |

**No additional websites were gained by pass 2 on this cohort.** Global headroom is not permission to exceed cumulative company/DNS ceilings. Planning skips keep pass 1's completed checked scope while recording explicit pass-2 budget states and envelope errors. An attempted incomplete check retains its actual failed/budget source state. Full per-company states and every request's pass label are in report.json; all section/count comparisons are in counts.json and table.md.

The native integration test demonstrates a genuine positive case: a late, exact-employer NAV homepage gains a VERIFIED website and own-footer numeric LinkedIn profile with two extra HTTP requests, within the unchanged cumulative limits. Other tests enforce veto/robots non-retry, missing/foreign/expired NAV rejection, per-company/global/deadline/DNS cutoffs, no budget reset, optional-pass failure isolation and completed-scope preservation. Activity refresh keeps existing registry events without duplicates and drops public activity tied to a replaced website proof.

## Trials retained and corrections

- interrupted/ preserves the first attempt: the tool/host made no progress across a roughly four-hour gap. The process returned mandatory output but exceeded the time limit; the measurement guard rejected it. It is not counted as normal performance. No claim is made that software can preempt a suspended host or arbitrary stalled filesystem/input work.
- order_trial/ preserves the next measured regression: promoting branch/provider contacts ahead of strong full-name candidates caused SPEDIFY's own site to miss its allowance. That trial lost SPEDIFY and its social URL. The final code restores the existing measured priority, and the final fresh run restores both URLs. No proof rule was loosened and no quota was raised.
- A regression test caught duplicate registry activity when failed public-activity refresh preserved facts that were then merged again. The merge now adds only missing fields. A second guard removes dated public facts whose old website identity proof has been replaced.
- A0 diagnostics retain the outdated NAV-time expectation correction and an unchanged five-second HTML-localization timeout. Later full green gates retain the same timing assertions. Legacy single-pass/source fixtures explicitly opt out; separate real evaluator-command tests use the production defaults.

## URL evidence, site checks and hand check

[new_websites.md](new_websites.md) lists every added/removed website/social URL against A0 and Stage S, with organisation number, legal name, proof tier, exact excerpt, source URL, retrieval date and hash. url_inventory.json includes all final and comparison URLs and their receipts. Final delta: zero added URLs, one removed website URL, zero social changes. Removed proof is clearly labelled historical.

Authored headless Chromium passes 14 checks at 1280/360px for both A0 and final A, with external browser requests blocked: search/name/number, profile, compare, full source receipts, visible briefing/run-status citations, >=44px controls and no horizontal page overflow or JavaScript errors. The final site is a local run artifact; docs/demo remains the earlier Stage S demo. Nothing is published.

Screenshots:

- stageA0 (12): [desktop-compare.png](../stageA0/desktop-compare.png), [desktop-directory.png](../stageA0/desktop-directory.png), [desktop-profile.png](../stageA0/desktop-profile.png), [desktop-run-observation.png](../stageA0/desktop-run-observation.png), [desktop-source.png](../stageA0/desktop-source.png), [mobile-compare.png](../stageA0/mobile-compare.png), [mobile-directory.png](../stageA0/mobile-directory.png), [mobile-evidence-row.png](../stageA0/mobile-evidence-row.png), [mobile-financial-row.png](../stageA0/mobile-financial-row.png), [mobile-profile.png](../stageA0/mobile-profile.png), [mobile-run-observation.png](../stageA0/mobile-run-observation.png), [mobile-source.png](../stageA0/mobile-source.png).
- stageA (12): [desktop-compare.png](desktop-compare.png), [desktop-directory.png](desktop-directory.png), [desktop-profile.png](desktop-profile.png), [desktop-run-observation.png](desktop-run-observation.png), [desktop-source.png](desktop-source.png), [mobile-compare.png](mobile-compare.png), [mobile-directory.png](mobile-directory.png), [mobile-evidence-row.png](mobile-evidence-row.png), [mobile-financial-row.png](mobile-financial-row.png), [mobile-profile.png](mobile-profile.png), [mobile-run-observation.png](mobile-run-observation.png), [mobile-source.png](mobile-source.png).

Decisions are in [../DECISIONS.md](../DECISIONS.md). Hand-check:

- Recheck IREV's current source availability and compare the historical proof with its withheld final state; do not treat the old excerpt as fresh verification.
- Review SPEDIFY, BIEN and FOLKSOM own-footer social contexts in the inventory, plus the late-NAV native positive case.
- Review the 26 capacity-limited pass-2 company outcomes and whether more source-backed nominations can help within the existing ceilings; no live recall improvement is claimed.
- Review incomplete hiring scope, BIEN's failed accounts source, forced short-budget behavior and physical mobile/Safari layout. Tiny deadlines or externally suspended/stalled hosts cannot be promised an absolute completion time; accepted daily measurements must pass the completion/site guard.

Stopped after Stage A. No Stage B, git push or publication.
