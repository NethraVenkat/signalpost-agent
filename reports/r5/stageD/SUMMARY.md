# Stages D and I - final summary

Completed on revision/r5 as Nethra Venkat. Local commits only; no push, publication or Stage C. This summary is committed separately after the two implementation commits.

| Stage | Commit | Result |
|---|---|---|
| D | `5fd4f0ba2401edc6ecdc3da133aee947f1cb81ca` | Fresh official NAV index, exact-employer hiring and bounded owned-careers discovery |
| I | `f5876bd4be905ad17813ec8e37edb27e343edea8` | Evidence-linked filing years, all returned entity periods, source-only units, polite metered access |

[D implementation/evidence report](D_REPORT.md), [I implementation/evidence report](../stageI/I_REPORT.md), [decisions](../DECISIONS.md), [final source/budget audit](../stageI/release_audit.json).

Each final run uses exactly --organisations, --bulk, --output, --profiles-output, --report, --run-id and --expected-count, with fresh state, original hash-checked inputs and a new run ID. No enrichment/cap flags. Defaults remain all enrichment on and 8/13, with the existing bounded adaptive allowance.

## Frozen seed 20261017

| Metric | B baseline | D | I final |
|---|---:|---:|---:|
| verified_websites | 6 | 6 | 6 |
| social_profile_companies | 3 | 3 | 3 |
| job_ad_companies | 0 | 0 | 0 |
| activity_companies | 100 | 100 | 100 |
| activity_claims | 1226 | 1226 | 1226 |
| total_facts | 10517 | 10517 | 13354 |
| http_requests | 943 | 583 | 685 |
| process_wall_seconds | 341.881 | 115.011 | 344.325 |

## Seed 20261113

| Metric | B baseline | D | I final |
|---|---:|---:|---:|
| verified_websites | 4 | 3 | 4 |
| social_profile_companies | 1 | 0 | 1 |
| job_ad_companies | 0 | 1 | 1 |
| activity_companies | 100 | 100 | 100 |
| activity_claims | 1147 | 1147 | 1147 |
| total_facts | 10726 | 10722 | 13760 |
| http_requests | 1026 | 633 | 770 |
| process_wall_seconds | 384.284 | 163.190 | 386.778 |

## Accounts and validation

| Metric | D frozen | I frozen | D daily | I daily |
|---|---:|---:|---:|---:|
| Accounts facts | 4208 | 7045 | 4361 | 7394 |
| Companies with >=2 figure periods | 92 | 92 | 92 | 92 |
| YoY sentences | 0 | 0 | 0 | 0 |
| Companies with >=2 filed years | 0 | 93 | 0 | 92 |
| Filing-year facts | 0 | 929 | 0 | 1040 |
| Successful year lookups | 0 | 100 | 0 | 100 |
| Newer-filing flags | 0 | 0 | 0 | 0 |

Every final run exits 0 with 100 ordered terminal envelopes and a 100-company site. Both I outputs have zero unsupported values and all five briefing topics in run.synthesis/profile.synthesis. Final requests are 685/770, wall time 344.325/386.778 seconds, cost $0, and no hiring failures. Final I source manifests match the committed implementation. Full pytest: 895 passed in 199.25 seconds (stageI/pytest-green.txt). D's own full gate was 879 green. Desktop/mobile QA: 20 checks, 18 screenshots, >=44px targets, no horizontal overflow or JavaScript errors; external browser requests blocked. Largest profiles: 248114/222972 bytes, below the unchanged 250000-byte gate.

## Decisions and limits

- Rebuild NAV from official feed/details only: 9511 active ads, 6012 employers, zero failed details, built 2026-11-13T08:23:53.796625Z. Maintenance build: 10139 requests / 1393.25 seconds, separate from daily ceilings. The builder's explicitly bounded maintenance allowance was restored; daily global limits remain unchanged. Stale-index fallback caused B's 11/6 hiring failures; fresh declared-index runs eliminate them. No indexed match is not exhaustive vacancy absence.
- Hiring requires current live exact employer/proven-subunit details. Careers require a current VERIFIED site's own navigation/footer, same-site/allowed ATS target, a titled current posting and full link/date receipts. Group, expired, undated and name-only matches are rejected. Unsupported layouts/query-dependent ATS URLs remain limitations; no careers job was published. The SPEDIFY invitation for future opportunities was withheld.
- Retain every earlier returned SELSKAP period with its own raw values, currency and unit, plus cited available-copy years. This is not lifetime filing coverage. No PDFs or year-by-year requests. Missing units stay unknown, including NOK; current and legacy carry-forward inference is removed. Hence live ratios/YoY remain unavailable, while positive declared-unit/comparable-period cases are tested. No newer-filing flag occurred in these samples; positive/source-tampering cases pass.
- Initial year bursts hit 429 and are preserved under stageI/trials/burst. A shared gate now spaces new lookups by >=2.1 seconds and honors >=60 seconds/longer Retry-After after 429 without immediate retry. Final samples each have 100 HTTP-200 year lookups and zero 429s. Failures stay explicit; refresh never invents filing deletions. Waiting grants no time/request capacity.
- A rejected full-history site exceeded its size gate. Compact year rows link to the common year-list evidence panel, while all claims/receipts remain locally inspectable. The rejected run and passing pre-legacy-unit run are retained as trials; final comparisons use only release runs with final source. Strict offline replay adds explicitly synthetic availability failures, not historical filing facts.
- SUNNCOM's site/two social URLs were withheld in D after fresh proof failed, then restored with current proof in I. [D URL changes](new_websites.md) and [I URL changes](../stageI/new_websites.md) retain exact current/historical receipts. Frozen URLs did not change. Live runtime/recall variation is not treated as a causal benchmark or official score.

Code/dependency licences remain MIT; Brreg data NLOD 2.0, NAV official reuse terms, SSB CC BY 4.0, website excerpts their own terms. Models and paid search: zero calls. Provider cost: $0; compute/storage/network excluded. Official API schema/access/terms review is in stageI/source_review. No application code from another repository was copied.

## Hand checks

1. [Every D job](jobs.md) and [every I job](../stageI/jobs.md): DIGITALIQ AS 918266917, NAV job 52c02dd7-b354-4765-a221-a594aca6b2d6; title, publication/deadline and exact employer/title/date excerpts included. One daily job, no frozen job.
2. SPEDIFY 926818317: open the compact year link and year-list panel; compare URL, exact array excerpt, retrieval date and hash. The future-opportunity application is not represented as an active job.
3. INNLANDET REVISJON IKS 987769386: three figure periods, individual unit labels, available-copy years and full receipts on the largest profile. Check mobile-history and mobile-filed-years screenshots below.
4. BIEN SPAREBANK 991853995: unavailable figures remain explicit alongside available filing years. No guessed units, ratios or YoY.
5. SUNNCOM 918031502: hand-check the restored website/Facebook/numeric LinkedIn own-footer proof in I's URL inventory.
6. Inspect the exact seven-flag commands, ordered-input verifier receipts, source/output hashes and complete request ledgers in each stage/sample directory. Generated final sites are under .data/r5/stageI-{frozen,daily}-run-release/site locally; no site was published.

## Final screenshots

- [desktop-compare.png](../stageI/browser-final/desktop-compare.png)
- [desktop-directory.png](../stageI/browser-final/desktop-directory.png)
- [desktop-filed-years.png](../stageI/browser-final/desktop-filed-years.png)
- [desktop-history.png](../stageI/browser-final/desktop-history.png)
- [desktop-profile.png](../stageI/browser-final/desktop-profile.png)
- [desktop-registry-event.png](../stageI/browser-final/desktop-registry-event.png)
- [desktop-run-observation.png](../stageI/browser-final/desktop-run-observation.png)
- [desktop-source.png](../stageI/browser-final/desktop-source.png)
- [mobile-compare.png](../stageI/browser-final/mobile-compare.png)
- [mobile-directory.png](../stageI/browser-final/mobile-directory.png)
- [mobile-evidence-row.png](../stageI/browser-final/mobile-evidence-row.png)
- [mobile-filed-years.png](../stageI/browser-final/mobile-filed-years.png)
- [mobile-financial-row.png](../stageI/browser-final/mobile-financial-row.png)
- [mobile-history.png](../stageI/browser-final/mobile-history.png)
- [mobile-profile.png](../stageI/browser-final/mobile-profile.png)
- [mobile-registry-event.png](../stageI/browser-final/mobile-registry-event.png)
- [mobile-run-observation.png](../stageI/browser-final/mobile-run-observation.png)
- [mobile-source.png](../stageI/browser-final/mobile-source.png)

[Browser checks](../stageI/browser-final/browser_results.json). Both final sample execution/verification receipts, all source/request reports, proof inventories and retained trials are committed. Required work ends here; Stage C has not started.
