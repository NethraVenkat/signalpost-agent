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

## Queue

Next: X4 public brands, then X5 explicit dated filing/LEI activity, then R6a?f websites, then X2 owner-declared social, X3 site-builder audit first and X6 legal roles. None of these queued items is claimed implemented or measured by X1. User permits a clean stop after a completed priority item if time/budget becomes tight. No push.
