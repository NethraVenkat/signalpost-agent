# X1 measured item

Author/committer Nethra Venkat; revision/r5; no push; $0. Exactly seven flags, fresh state/new IDs, all six samples; unchanged runtime source. Settings, input/output hashes, request logs and independent verification are retained per seed.

| Seed | Sites before → after | Declared recall before → after / N | Activity companies / claims | Brand companies / claims | Social companies | Facts | HTTP | Runtime seconds | Largest profile bytes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 20261017 | 5 → 5 | 4 → 4 / 11 | 100 / 1398 | 0 / 0 | 3 | 13540 | 701 | 437.469 | 240762 |
| 20261113 | 6 → 6 | 5 → 5 / 11 | 100 / 1344 | 1 / 1 | 1 | 13976 | 775 | 485.578 | 223994 |
| 20261114 | 6 → 6 | 4 → 4 / 8 | 100 / 1263 | 1 / 1 | 4 | 13462 | 745 | 357.859 | 219756 |
| 20261115 | 8 → 8 | 3 → 3 / 14 | 100 / 1153 | 1 / 1 | 4 | 13267 | 756 | 371.781 | 222056 |
| 20261116 | 6 → 6 | 3 → 3 / 17 | 100 / 1475 | 3 / 3 | 0 | 13771 | 793 | 369.953 | 229596 |
| 20261117 | 8 → 8 | 0 → 0 / 11 | 100 / 1248 | 2 / 2 | 4 | 14052 | 751 | 370.781 | 247401 |

Totals: {"activity_claims": 7881, "activity_companies": 600, "brand_claims": 8, "brand_companies": 8, "declared_homepage_recall": 19, "declared_homepages": 72, "facts": 82068, "role_change_claims": 1241, "social_claims": 25, "social_companies": 16, "websites": 39}.

All runs exit 0, 100 ordered terminal envelopes, five cited briefing topics, zero unsupported values, generated site with profile HTML below 250,000 bytes, and hard HTTP/time budgets respected. No doubtful new identity item. [Full new/removed identity receipts](../new_items.md).

Source capability limitation: the open role-update feed publishes generic role-registry events with exact event type/company/ID/publication time. It does not supply changed role types or persons, so these remain explicitly unknown; a current role roster is never used to invent a past leadership appointment. Leadership-specific preference cannot be applied without source evidence. The timeline and briefing can cite the generic role-registry update. Shared 50-event cap and source-namespaced IDs remain. [Official terms/docs and diagnostic response review](../sources/X1_SOURCE_REVIEW.md).

## Source-outage trial and capability limit

An initial seed-20261114 run experienced run-wide DNS failures for Brreg/NAV/web sources: 0 websites, 0 activity claims, 3,005 local bulk facts, 311 HTTP attempts, 13.656 process seconds (11.891 reported completion seconds), $0. Its 100 ordered terminal envelopes/site remained structurally valid with zero unsupported values. It is explicitly retained under trials/source_outage rather than hidden. A new fresh-state seven-flag source-recovery run, same final production source, restored 6 websites / declared recall4/8 / 182 generic role events. No DNS fallback or proof change. Normal-source results in the table are the rerun; they are not a guarantee against live-source outages.

Full pytest gate: 1,055 passed. Role-specific titles, changed appointees/departures and leadership preference remain unavailable because the public feed does not supply these details. All1241 role claims are generic publication events; no named leadership claim is inferred. No website/social/brand item was added or removed in accepted X1 measurements.
