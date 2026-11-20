# S5 live 500 verification

Code: `98e6de1ef6d2438ea33e37fbad73953a2e1064b6`. Seed: `2026112705`. Run ID: `r5-s5-live500-2026112705`. Fresh clean clone, fresh state, exactly seven evaluator flags, default fixed 2,100-second budget; no scaled budget. No code changed during the run.

Live production-transport preflight returned HTTP 200 for the registry API and a public website robots file. Registry robots closed connections after retries; this is retained in preflight.json and the existing official-API access policy applies. Initial disk exceeded 15 GB; disk was checked every two seconds with a 3 GiB stop threshold. No guard fired.

| Metric | final500e | S5 |
|---|---:|---:|
| Process wall seconds | 1828.8589999999967 | 1880.8120000000054 |
| Remaining margin seconds | 271.14100000000326 | 219.18799999999464 |
| Envelopes | 500 | 500 |
| Profiles | 500 | 500 |
| Pages | 502 | 502 |
| Placeholders | 0 | 0 |
| Available claims | 71812 | 76213 |
| Largest profile bytes | 249279 | 234728 |
| Website deadline hits | 173 | 136 |
| Run status | partial | partial |

Live exit code 0; check_live_run --count 500 exit code 0. Checker measured run wall 1,875.531 seconds; the conservative external process wall includes startup/preparation and is used above. Unsupported synthesis values: 0; unsupported briefing values: 0. Source failure is permitted by the checker and does not mean complete source coverage. $0 measured cost.

## S1, S2 and S4

- S1: 3,919 status-event claims across 500 companies.
- S2: 12,890 derived timeline entries across 500 companies; median 25. These entries inherit existing evidence and are not additional claims.
- S4: 500 explicit identity-number claims and 451 explicit subunit-parent claims (378 companies).

## Section outcomes

| Section | final500e states | S5 states |
|---|---|---|
| accounts | {"available": 497, "failed": 3} | {"available": 497, "failed": 3} |
| activity | {"available": 500} | {"available": 500} |
| gleif | {"available": 64, "not_available": 436} | {"available": 78, "not_available": 422} |
| group | {"available": 35, "not_available": 465} | {"available": 27, "not_available": 473} |
| hiring | {"not_available": 500} | {"available": 4, "not_available": 496} |
| identity | {"available": 500} | {"available": 500} |
| inspections | {"available": 7, "not_available": 493} | {"available": 3, "not_available": 497} |
| licences | {"available": 10, "not_available": 490} | {"available": 7, "not_available": 493} |
| procurement | {"failed": 5, "not_available": 495} | {"failed": 10, "not_available": 490} |
| prokura | {"available": 111, "not_available": 389} | {"available": 99, "not_available": 401} |
| research | {"available": 5, "not_available": 495} | {"available": 7, "not_available": 493} |
| roles | {"available": 498, "not_available": 2} | {"available": 497, "not_available": 3} |
| signature | {"available": 488, "not_available": 12} | {"available": 473, "not_available": 27} |
| state_aid | {"available": 55, "not_available": 445} | {"available": 41, "not_available": 459} |
| status_events | {} | {"available": 500} |
| subunits | {"available": 401, "not_available": 99} | {"available": 378, "not_available": 122} |
| website | {"ambiguous": 27, "available": 39, "blocked": 2, "failed": 180, "not_available": 252} | {"ambiguous": 20, "available": 37, "blocked": 3, "failed": 168, "not_available": 272} |

## Errors and stop decision

All 500 envelopes contain at least one diagnostic/error record, including explicit snapshot absence and website-candidate diagnostics. This does not mean all companies failed. Every company and its section/error codes is listed in company-errors.json; invalid-registry-field records include their field. Website deadline records are listed in deadline-losses.json. Error-code totals and every section with lower available coverage or increased failures are in comparison.json.

The cohorts are disjoint, so raw coverage differences cannot establish a causal code regression. Lower counts nevertheless trigger the requested stop gate: group, inspections, licences, prokura, roles, signature, state aid, subunits and websites; procurement failures increased. Margin exceeds 120 seconds. STOP: no implementation changes or second live run.

Evidence checker validated 76,213 published claims and 2,948 source blobs; complete receipts remain in the local saved run. Source output SHA-256 values are in summary.json. The compact committed report does not contain raw company evidence.

Privacy guard: 17 passed. Accounts HTTP 500 failures: `993386146`, `977148162`, `969199009`. There were 542 invalid-registry-field diagnostics; these are explicit omissions, not unsupported published values. Minimum monitored free disk: 25,847,848,960 bytes.
