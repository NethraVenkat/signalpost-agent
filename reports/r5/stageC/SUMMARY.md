# F1 and Stage C - final summary

Completed on revision/r5 as Nethra Venkat. Local commits only; no push, publication or subsequent stage.

| Stage | Commit | Result |
|---|---|---|
| F1 | `7453c7d1a46ee54e4a3648d202f87fba43d6298f` | Restored sourced, dimensionless ratios and comparable-period YoY; no absolute-scale invention |
| C | `661716797e0d47e71aae5195777df39f62526818` | Bounded own-sitemap proof discovery, challenge classification and explicit diagnosis/cutoffs |

[F1 report](../stageF1/REPORT.md), [C report](C_REPORT.md), [before diagnosis](diagnosis.md), [after diagnosis](diagnosis_after.md), [URL changes with exact excerpts](new_websites.md), [all website/social proofs](url_inventory.json), [decisions](../DECISIONS.md), [source/budget audit](audit.json).

## Financial result

| Metric | I frozen | F1 frozen | C frozen | I daily | F1 daily | C daily |
|---|---:|---:|---:|---:|---:|---:|
| Derived ratios | 0 | 153 | 153 | 0 | 169 | 169 |
| Comparable revenue YoY metrics | 0 | 50 | 50 | 0 | 63 | 63 |
| Distinct cited YoY sentence instances within profiles | 0 | 100 | 100 | 0 | 125 | 125 |

F1/C restore 55/70 operating margins and 98/99 equity ratios, plus YoY on 50/63 companies. Ratios cite two values from the same exact-company statement, period, declared currency and unit-field value; matching absent units cancel. YoY requires comparable consecutive annual periods, positive prior revenue, matching declared currency and matching units, or both units absent from the same approved entity schema. Absolute amounts remain raw/unknown-scale where the source omits units; headline/sentence validation cannot invent whole NOK. Independent verification repeats source-value, period, currency, unit, statement/schema and arithmetic checks. C preserves the restored result.

## Frozen seed 20261017

| Metric | I | F1 | C final recovery |
|---|---:|---:|---:|
| verified_websites | 6 | 6 | 5 |
| social_profile_companies | 3 | 3 | 3 |
| contacts | 12 | 12 | 11 |
| job_ad_companies | 0 | 0 | 0 |
| activity_companies | 100 | 100 | 100 |
| activity_claims | 1226 | 1225 | 1202 |
| total_facts | 13354 | 13353 | 13325 |
| http_requests | 685 | 692 | 689 |
| runtime_seconds | 332.360 | 593.000 | 347.984 |
| process_wall_seconds | 344.325 | 606.647 | 359.686 |

## Seed 20261113

| Metric | I | F1 | C final recovery |
|---|---:|---:|---:|
| verified_websites | 4 | 4 | 4 |
| social_profile_companies | 1 | 1 | 1 |
| contacts | 8 | 8 | 8 |
| job_ad_companies | 1 | 1 | 1 |
| activity_companies | 100 | 100 | 100 |
| activity_claims | 1147 | 1147 | 1137 |
| total_facts | 13760 | 13760 | 13751 |
| http_requests | 770 | 775 | 773 |
| runtime_seconds | 374.109 | 383.782 | 369.500 |
| process_wall_seconds | 386.778 | 405.137 | 379.164 |

Every accepted run uses exactly the seven evaluator flags, a new run ID and fresh isolated state with the original hash-checked inputs. Enrichment defaults and 8/13 caps remain unchanged, with only the previously authorized adaptive allowance. Website counts retain the prior accepted-tier definition; exact sitemap gains count only VERIFIED proof. Both C runs exit 0 with 100 terminal envelopes in input order, available 100-company sites, complete five-topic cited briefings, zero unsupported values and $0 provider fees. C HTTP is 689/773 and wall time 359.686/379.164 seconds, inside 1850 requests and 2100 seconds. Full resolved settings, exact argv, source/output hashes, request ledgers and independent verifier receipts are under frozen/ and daily/.

## Website result and decisions

No website/social URL was added. Final website count is 5/4 versus F1's 6/4: no recall gain is claimed. NAPOLITANA 998340888, https://napolitana.no, is withheld after HTTPS connect failures and refused plaintext redirects; the historical exact-number excerpt in new_websites.md is not reused as current proof. Other website/social URL sets are unchanged. Site/contact/description fields and activity may vary with current source responses; these counts are observational, not a causal performance claim or official score.

The F1 diagnosis has 94/96 companies without a site. Primary causes: DNS 54/39, budget 15/24, ambiguous 6/9, veto 6/13, robots/access 3/4, timeout/connect/5xx 1/1, fetched-no-proof 5/3, no recorded candidate 4/3. diagnosis.md explains the exclusive priority and overlapping signals and lists every org's receipts. External DNS/access/veto outcomes are not bypassed. The two actionable gaps addressed are budget ordering and fetched-no-proof discovery: own links, then bounded own-map nominations, then fixed guesses; common privacy aliases precede redundant bare /om. A late blind alias can remain unchecked at the original cap.

Sitemaps only nominate contact/about/privacy/impressum pages. One map and at most one non-news page-map child per candidate; at most two sitemap-nominated HTML pages per company across both passes. The fetched HTML must pass the unchanged proof scorer and all foreign/group vetoes. There is no new HTTP/DNS/time allowance. The final samples nominate one proof page each for three/two companies; none reaches new exact-number proof. audit.json records every cutoff/nomination summary, and run.refresh.proof_sitemaps retains per-company attempts.

Sitemaps never supply news: public activity now uses linked RSS/Atom and bounded dated HTML. This intentionally removes sitemap-derived updates; registry activity remains supported. Candidate ordering, robots/terms, public-IP pinning/TLS, politeness, proof thresholds and once-only veto/cache rules remain intact.

Challenge bodies are blocked before status retries/fallback and scoring, including 403/503/text/plain gates; blocked proof exceptions stop the walk. Ordinary recaptcha contact forms and passive Cloudflare JSD on usable pages are not gates. The first broad matcher falsely removed DIGITALIQ; that trial is preserved and corrected, with positive/negative tests, vendor documentation and replay of the exact-number body in passive_jsd_review.json. No scripts are executed or challenge solved. Each run still requires fresh publication proof.

## Validation, failures and reproducibility

- F1 full pytest: 899 green. Final C full pytest: 912 green, in 337.62 seconds (pytest-release.txt); final focused set: 96 green. Existing identity/robots/SSRF/politeness/cap gates remain. Legacy tests were updated for the explicit new sitemap policy, not by increasing budgets or lowering proof.
- Final C source manifests match the implementation. Audit confirms 100 companies/sites, exact seven flags, <=13 cumulative website HTTP, <=2 map-nominated HTML pages/company, no sitemap news and unchanged <250000-byte profiles. Largest profiles: 249666/224950 bytes. Independent verifiers report zero unsupported values in every accepted profile/briefing.
- Final recovered frozen site passes 20 headless Chromium checks at 1280/360 px, with 18 screenshots: search name/org, profiles, source URL/excerpt/retrieval/hash, restored arithmetic, year-list jumps, complete retained registry timeline, all evidence and comparison. Tap targets >=44px; no horizontal scroll/JavaScript errors; external browser requests blocked. Browser scripts use an installed Playwright dependency; application/QA code was implemented in this repo without copying another repository's application code.
- Retained trials cover proof-only discovery, HTML-only challenge handling, the passive-JSD false block, a host no-progress interval, and a superseded wrapper report-folder collision. That trial's own complete output was independently reverified and its counts reconstructed separately. A temporary approval-review timeout delayed launch; its authorized retry succeeded.
- The same-source DNS-failure pair is retained under trials/dns_outage. Frozen: 15 role, 16 figure and 19 filing-year OS name-not-found failures; daily: seven incomplete subunit/hiring scopes. One fresh unchanged-code recovery run per sample followed. No DNS override, failed-state promotion or historical publication proof was used. The final recovery pair has no hiring failures. The daily table helper also needed a fix to include states absent from the baseline; counts were regenerated from saved output without crawling again.

Code/Playwright: MIT. Brreg data: NLOD 2.0 with attribution; NAV: official reuse terms/current exact-employer details; SSB: CC BY 4.0; website factual excerpts retain their own terms. Models/paid search: zero calls. Expected provider cost: $0; compute/storage/network excluded as in prior reports. No push or publication.

## Hand checks

1. NAPOLITANA 998340888: inspect the removed URL's historical exact excerpt and current connect/refused-redirect attempts. Do not interpret the withholding as a closure.
2. DIGITALIQ 918266917: confirm fresh exact-number website proof and the existing live NAV job. Passive JSD is not an interstitial; active/visible gates remain blocked.
3. SPEDIFY 926818317 and INNLANDET REVISJON IKS 987769386: follow both inputs for derived margin/equity/YoY, then inspect raw values whose absolute unit remains unknown. Check comparable dates/currency/unit fields, not just percentages.
4. Review every final map nomination in audit.json/diagnosis_after.json. A contact/about URL nomination does not establish identity. Inspect source states and both before/after cause tables.
5. Compare the exact seven-flag run commands, source/output hashes, complete request ledgers, verifier receipts and retained outage/trial results. Final generated sites remain local under .data/r5/stageC-{frozen,daily}-run-recovery/site.

## Final screenshots

- [desktop-compare.png](browser-release/desktop-compare.png)
- [desktop-directory.png](browser-release/desktop-directory.png)
- [desktop-filed-years.png](browser-release/desktop-filed-years.png)
- [desktop-history.png](browser-release/desktop-history.png)
- [desktop-profile.png](browser-release/desktop-profile.png)
- [desktop-registry-event.png](browser-release/desktop-registry-event.png)
- [desktop-run-observation.png](browser-release/desktop-run-observation.png)
- [desktop-source.png](browser-release/desktop-source.png)
- [mobile-compare.png](browser-release/mobile-compare.png)
- [mobile-directory.png](browser-release/mobile-directory.png)
- [mobile-evidence-row.png](browser-release/mobile-evidence-row.png)
- [mobile-filed-years.png](browser-release/mobile-filed-years.png)
- [mobile-financial-row.png](browser-release/mobile-financial-row.png)
- [mobile-history.png](browser-release/mobile-history.png)
- [mobile-profile.png](browser-release/mobile-profile.png)
- [mobile-registry-event.png](browser-release/mobile-registry-event.png)
- [mobile-run-observation.png](browser-release/mobile-run-observation.png)
- [mobile-source.png](browser-release/mobile-source.png)

[Browser checks](browser-release/browser_results.json). This summary is committed separately after F1 and C. Work stops here; no further stage has started.
