# X / R6 measured stages

Author/committer Nethra Venkat; revision/r5; never pushed. Human-verdict update committed as ca9ab655 (1,042 green tests). New user order: X1 ? X4 ? X5 ? R6a ? R6b ? R6c ? R6d ? R6e ? R6f ? X2 ? X3 audit-first ? X6. One green measured commit per item. No external-repository code/data, paid model or paid API.

## Completed X1 ? public role-registry publication events

X1 implementation, tests, source review and measurements are in this commit; no self-referential hash is invented. Full gate: 1,055 passed. All six accepted runs used exactly seven evaluator flags, fresh state and new run IDs, with unchanged production source, zero unsupported values, 100 ordered terminal envelopes, five cited briefing topics, generated site and profile HTML below250000 bytes. All per-run HTTP/time limits respected; cost $0.

| Seed | Websites | Declared recall / N | Activity companies / claims | Role-event claims | Brand claims | Social companies | Facts | HTTP | Process seconds |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 20261017 | 5 | 4/11 | 100/1398 | 232 | 0 | 3 | 13540 | 701 | 437.469 |
| 20261113 | 6 | 5/11 | 100/1344 | 219 | 1 | 1 | 13976 | 775 | 485.578 |
| 20261114 | 6 | 4/8 | 100/1263 | 182 | 1 | 4 | 13462 | 745 | 357.859 |
| 20261115 | 8 | 3/14 | 100/1153 | 183 | 1 | 4 | 13267 | 756 | 371.781 |
| 20261116 | 6 | 3/17 | 100/1475 | 253 | 3 | 0 | 13771 | 793 | 369.953 |
| 20261117 | 8 | 0/11 | 100/1248 | 172 | 2 | 4 | 14052 | 751 | 370.781 |

Totals: {"HTTP": 4521, "CLI_runtime_seconds": 2393.421000000002, "role_events": 1241, "activity_claims": 7881, "facts": 82068}. Websites39/600; declared-homepage recall19/72, unchanged from R3. No added/removed website/social/brand identity.

Role detail limitation: the documented open CloudEvent feed supplies company ID, event ID, exact event type/source and publication time, but no changed role type or person. All1,241 role-event claims are honestly generic registry-role updates, not inferred appointments or leadership changes. Publication time is explicitly not effective date. Current rosters are not joined onto past events to invent who changed. Source types include role and role-entity record updates; no effective date or person is inferred. [Official source review / diagnostics](sources/X1_SOURCE_REVIEW.md).

Every event has source hashes, exact locators/excerpts and reconstruction validation. Role and company/subunit events share the newest50 registry cap; source namespaces prevent ID collisions, duplicate events deduplicate, repeated/conflicting pagination fails. Source errors stay explicit. [X1 full report](X1/REPORT.md), [validation](X1/VALIDATION.json).

## Source-outage trial and capability limit

An initial seed-20261114 run experienced run-wide DNS failures for Brreg/NAV/web sources: 0 websites, 0 activity claims, 3,005 local bulk facts, 311 HTTP attempts, 13.656 process seconds (11.891 reported completion seconds), $0. Its 100 ordered terminal envelopes/site remained structurally valid with zero unsupported values. It is explicitly retained under trials/source_outage rather than hidden. A new fresh-state seven-flag source-recovery run, same final production source, restored 6 websites / declared recall4/8 / 182 generic role events. No DNS fallback or proof change. Normal-source results in the table are the rerun; they are not a guarantee against live-source outages.

Full pytest gate: 1,055 passed. Role-specific titles, changed appointees/departures and leadership preference remain unavailable because the public feed does not supply these details. All1241 role claims are generic publication events; no named leadership claim is inferred. No website/social/brand item was added or removed in accepted X1 measurements.

## Identity hand checks

[Every added/removed website, social URL and brand, with full exact receipts](new_items.md). X1 adds no identity item and therefore no doubtful new identity. The original role update diagnostic used2 separately counted free HTTP attempts (robots ReadError, API200). The outage trial used311 additional attempts, disclosed above. Neither is silently included in the normal-source accepted-run totals.

## Completed X4 ? public names

X1 commit c4f42860 precedes X4. X4 implementation, evidence ledger and summary are in this commit. Full pytest: **1,067 passed**. All six accepted fresh seven-flag runs passed terminal/order/schema/evidence/five-topic/site checks, with zero unsupported values and unchanged runtime source. Profile HTML remains below250000 bytes. No new source request or website identity tier was added.

Registered workplace names differing from the legal name are published with exact parent/subunit/name registry evidence and labelled as workplace names, not assumed trademarks or legal renames. Current VERIFIED/HIGH sites may supply an own publisher og:site_name or title brand corroborated in publisher branding. Generic templates/page headings, legal-name-only, customer/article and domain-only guesses abstain. The older heuristic is replaced and any withdrawn alias remains in the ledger. Names appear in profile facts and the cited activity briefing. Name changes in coverage are observations, not invented dated company renames.

| Seed | Websites | Declared recall / N | Brand companies / claims | Activity claims | Social companies | Facts | HTTP | Process seconds | Largest profile HTML |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 20261017 | 6 | 4/11 | 6/8 | 1398 | 3 | 13552 | 703 | 374.578 | 241093 |
| 20261113 | 6 | 5/11 | 9/10 | 1344 | 1 | 13997 | 770 | 402.781 | 224442 |
| 20261114 | 6 | 4/8 | 8/10 | 1263 | 4 | 13471 | 741 | 354.782 | 221597 |
| 20261115 | 7 | 3/14 | 5/7 | 1153 | 4 | 13270 | 740 | 384.281 | 222056 |
| 20261116 | 5 | 3/17 | 8/12 | 1475 | 0 | 13777 | 785 | 395.359 | 229166 |
| 20261117 | 8 | 0/11 | 6/24 | 1248 | 4 | 14074 | 723 | 329.016 | 249152 |

Totals: 71 brand claims / 42 companies, 38 websites / 600 inputs, declared recall19/72, 7,881 activity claims, 82,141 supported facts. 4462 requests and 2240.797 summed process seconds; $0. Each run stays within its hard1850HTTP/35min limit.

Saved-evidence recheck: 65 added brand claims and one added website all correct; zero doubtful additions. Full source excerpts, URLs, retrieval dates, hashes and exact registry dependencies in [new_items.md](new_items.md) and [X4 identity_items.json](X4/identity_items.json). This is source/rule replay, not an independent human verdict. Review site names as publisher self-description and workplace names as registry declarations. Withdrawals are explicit.

Live-source changes are not X4 identity-policy gains: one existing-rule website recovered, while LOOPYTY933519708 and AURSJ?KRAFT925700398 timed out. Two older brand aliases were withdrawn by the stricter publisher-name extractor. No social URL changes. An incomplete seed20261115 attempt had no final report/exit receipt and its process disappeared; cause/finalHTTP/runtime unknown. Its raw state and trial settings are retained under X4/trials/interrupted_seed20261115. A new-ID fresh-state recovery passed, then seeds20261116/17 completed with the same runtime source. No interrupted output is counted as an accepted run.

## R6 measured checkpoint and current queue

X5 remains dropped. R6a/d/e were implemented with green gates then individually reverted after doubtful publisher attribution; all rejected receipts are retained. R6b/c/f remain. See [R6 measured table and decisions](../stageR6/SUMMARY.md) and [every added/removed/withheld URL](../stageR6/new_websites.md).

R6 accepted result: 37 websites / 600, declared-homepage recall 19/72; 4,424 requests and 2,781.080 summed process seconds, $0. Zero unsupported values; all six site/order/five-topic gates pass. One old exact-number site recovered and two old sites withdrew with live source failures. No retained new-tier website gain.

Remaining authorized order: R7a?g (including root-only, own branding and company-contact guardrails), Stage L0?L4 legal-disclosure proof, X2 owner-declared social, P0 official-source outage resilience, P2 new non-overlapping 500-company clean-clone scale test. X3/X5/X6 remain dropped. One full six-sample measurement per R7 and L stage; green pytest commit per sub-step. Foreground one sample at a time, exactly seven flags, fresh state/new IDs, strict proof/robots/global limits; never push. Review every new saved publisher context and revert only the responsible doubtful rule.

## R7 completed measured checkpoint

R7a/b/c/d/f/g are retained; R7e was individually reverted after a stock-template false attribution. Final qualification:40websites/600 (R6:37), declared recall20/72(R6:19/72),26social/17companies,4,949HTTP,2,884.172summed process seconds,$0. Zero unsupported values; all600ordered terminal/five-topic/site checks pass. Full final serialpytest1,164green. [R7 complete table, commits, safety rollback and costs](../stageR7/SUMMARY.md); [every added/removed/withheld URL and exact publisher review](../stageR7/new_websites.md).

Next authorized work: StageL0?L4, thenX2, P0, P2NEW500-company clean-clone qualification. Never push. X3/X5/X6 remain dropped.

## L completed before X2

[StageL measured table and limitations](../stageL/SUMMARY.md): 38/600websites, declared21/72, 5456HTTP,$0. [Every new/removed site](../stageL/new_websites.md). Full greenL4runtime unchanged. X2?P0?P2new500remain queued.

## R6/R7/L/X2 accepted measurements

| Stage | Websites /600 | Declared homepage recall /72 | Social companies / claims | HTTP | Summed process seconds |
|---|---:|---:|---:|---:|---:|
| R6 | 37 | 19 | 16 / 25 | 4424 | 2781.080 |
| R7 | 40 | 20 | 17 / 26 | 4949 | 2884.172 |
| L | 38 | 21 | 15 / 24 | 5456 | 4064.377 |
| X2 | 40 | 21 | 16 / 26 | 5540 | 3385.844 |

Six samples20261017/20261113/20261114/20261115/20261116/20261117, fresh state, exact seven flags, source manifests and per-run receipt hashes. Each accepted run passes100ordered terminal envelopes, five cited briefing topics, zero unsupported values, generated site below250000bytes/profile, hard HTTP/time limits,$0. Live-source recoveries and failures are not attributed to new proof rules.

R6retainsb/c/f; a/d/e were reverted after doubtful sites. R7retainsa/b/c/d/f/g; ewas reverted after a stock-template site. Ladds exact-number legal HTML and bounded linkedPDFverification; no speculative builder parser or new identity tier. X2adds exact owner declarations/contactFollowus, preserving numericLinkedIn exclusions. Every new/removed URL and brand is in[new_items.md](new_items.md), with complete new publisher review packets per seed.

New X2website/social publication labels: {"own_contact_follow_us_v1": 1, "own_header_footer_exact_name_v1": 1, "orgnr_on_page": 2}. Full gate1,246passed/155.60seconds; failed integration gate and fixes preserved. Saved-context reviews are assistant inspection, not independent human verification. Human hand checks remain pending.

X5/X3/X6 remain dropped. Next authorized items are P0source-outage resilience and P2fresh-clean-clone500company scale qualification; no push.
