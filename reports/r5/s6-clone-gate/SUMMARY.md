# S6 same-cohort live confirmation

Yes: same-cohort section outcomes regressed in website.

These are observed differences on identical inputs; live source changes and availability can also affect counts. No causal attribution or fix is asserted.

Code `81858364b02d5c1fa3e9ded456d071a4d7587352`; seed `20261126`; run ID `r5-s6-clone-gate-20261126-s6b`. Fresh clean clone and state. Registry and GLEIF probes inside that clone both returned HTTP 200 before any company run. Public robots probe also returned 200. Disk exceeded 15 GB and a two-second 3 GiB stop guard stayed active. Exactly seven evaluator flags, default 2,100-second budget; no scaled budget.

Counts are available / failed / not_available. Status events did not exist in final500e.

| Section | final500e | S6 | delta |
|---|---:|---:|---:|
| accounts | 497/3/0 | 497/3/0 | +0/+0/+0 |
| activity | 500/0/0 | 500/0/0 | +0/+0/+0 |
| gleif | 64/0/436 | 64/0/436 | +0/+0/+0 |
| group | 35/0/465 | 35/0/465 | +0/+0/+0 |
| hiring | 0/0/500 | 0/0/500 | +0/+0/+0 |
| identity | 500/0/0 | 500/0/0 | +0/+0/+0 |
| inspections | 7/0/493 | 7/0/493 | +0/+0/+0 |
| licences | 10/0/490 | 10/0/490 | +0/+0/+0 |
| procurement | 0/5/495 | 0/5/495 | +0/+0/+0 |
| prokura | 111/0/389 | 111/0/389 | +0/+0/+0 |
| research | 5/0/495 | 5/0/495 | +0/+0/+0 |
| roles | 498/0/2 | 498/0/2 | +0/+0/+0 |
| signature | 488/0/12 | 488/0/12 | +0/+0/+0 |
| state_aid | 55/0/445 | 55/0/445 | +0/+0/+0 |
| status_events | 0/0/0 | 500/0/0 | +500/+0/+0 |
| subunits | 401/0/99 | 401/0/99 | +0/+0/+0 |
| website | 39/180/252 | 38/184/251 | -1/+4/-1 |

Other states: {"website": {"ambiguous": 26, "blocked": 1}}

Wall: 1902.844 s; margin: 197.156 s. Claims: 76892 (baseline 71812). Largest profile: 234189 bytes. Envelopes/profiles/pages: 500/500/502. Placeholders: 0. Unsupported synthesis/briefing values: 0/0. Website deadline hits: 180 (baseline 173). run_status: partial. Process/checker exits: 0/0. Live HTTP successes: 4,656 of 6,196 measured requests. Cost: $0.

Input and bulk SHA-256 match final500e. The report preserves execution arguments, disk samples, checker receipts and output hashes. Every company diagnostic is listed by orgnr, section and code in company-errors.json. No code changes, fixes, tags or push. STOP after report.

Privacy guard: 17 passed. Both input hashes rechecked against the frozen final500e sampling manifest before report commit.
