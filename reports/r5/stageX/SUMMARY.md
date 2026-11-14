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

## X5 attempt - reverted at committed checkpoint

X5 is **not completed**. Its uncommitted runtime/test changes were restored to the X4 feature checkpoint after repeated interrupted measurements and a hard-time/site validation failure exceeded the inherited approximately90-minute stage allowance. All trial outputs and implementation snapshots remain in [X5 REPORT.md](X5/REPORT.md) and [REVERTED.json](X5/REVERTED.json). Earlier green tests and three partial verified samples are not represented as a completed six-sample stage. No dated filing or renewal is invented to fill source gaps.

## Remaining queue and current measurement plan

Resume X5 before R6a-f, R7a-f and X2. These items are unfinished; no R6/R7/X2 gains or tables are claimed. X3 and X6 are dropped. R6 and R7 each retain one green pytest commit per sub-step, followed by ONE six-sample stage measurement. Gains are attributed by proof type; a doubtful site requires reversal of its responsible sub-step and one stage remeasurement. R1/R2/R4 evidence, robot and budget safeguards remain. Never push. Only committed checkpoints may be used to pause.

Restored checkpoint full pytest: **1,067 passed in 183.47s (restored X4 runtime)**. Runtime source is restored; the reports-only checkpoint does not claim X5 completion.

## Unattended continuation result

A newly authorized X5 attempt exhausted its single fresh-state retry: initial time-validation failure, then structurally valid output under run-wide source outage (only2941 local facts, no site identities/activity). X5 runtime changes reverted; attempts retained in [UNATTENDED_RESULT.json](X5/UNATTENDED_RESULT.json). No further retries or feature-completion claims. Disk stayed above20GB, so nothing was deleted. R6/R7/X2 remain queued and incomplete; X3/X6 stay dropped.

Unattended retry-exhausted checkpoint: restored runtime full pytest **1,067 passed in166.86seconds**. No X5 feature committed; provider cost$0.
