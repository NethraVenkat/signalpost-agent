# S6 same-cohort confirmation: invalid live result

**STOP: no successful live HTTP responses. This run is not a valid live confirmation and its coverage loss cannot establish a code regression.** Preflight from the main checkout returned live HTTP 200 responses, but the clone run recorded 5,221 requests with no HTTP status; 5,217 were ConnectError, three TimeoutError and one dns_timeout. No retry or implementation change was made.

Code `81858364b02d5c1fa3e9ded456d071a4d7587352`; seed `20261126`; run ID `r5-s6-live500-20261126-s6`. Fresh clean clone and state, seven evaluator flags, fixed 2,100-second budget. Cohort and bulk bytes match final500e SHA-256 exactly. At least 15 GB free before start; 3 GiB disk stop guard armed throughout, never fired.

| Section state | final500e | S6 | delta |
|---|---:|---:|---:|
| accounts: available | 497 | 0 | -497 |
| accounts: failed | 3 | 500 | +497 |
| accounts: not_available | 0 | 0 | +0 |
| activity: available | 500 | 0 | -500 |
| activity: failed | 0 | 500 | +500 |
| activity: not_available | 0 | 0 | +0 |
| gleif: available | 64 | 0 | -64 |
| gleif: failed | 0 | 500 | +500 |
| gleif: not_available | 436 | 0 | -436 |
| group: available | 35 | 0 | -35 |
| group: failed | 0 | 500 | +500 |
| group: not_available | 465 | 0 | -465 |
| hiring: available | 0 | 0 | +0 |
| hiring: failed | 0 | 500 | +500 |
| hiring: not_available | 500 | 0 | -500 |
| identity: available | 500 | 499 | -1 |
| identity: failed | 0 | 1 | +1 |
| identity: not_available | 0 | 0 | +0 |
| inspections: available | 7 | 0 | -7 |
| inspections: failed | 0 | 1 | +1 |
| inspections: not_available | 493 | 499 | +6 |
| licences: available | 10 | 0 | -10 |
| licences: failed | 0 | 1 | +1 |
| licences: not_available | 490 | 0 | -490 |
| licences: blocked | 0 | 499 | +499 |
| procurement: available | 0 | 0 | +0 |
| procurement: failed | 5 | 500 | +495 |
| procurement: not_available | 495 | 0 | -495 |
| prokura: available | 111 | 0 | -111 |
| prokura: failed | 0 | 500 | +500 |
| prokura: not_available | 389 | 0 | -389 |
| research: available | 5 | 5 | +0 |
| research: failed | 0 | 1 | +1 |
| research: not_available | 495 | 494 | -1 |
| roles: available | 498 | 0 | -498 |
| roles: failed | 0 | 500 | +500 |
| roles: not_available | 2 | 0 | -2 |
| signature: available | 488 | 0 | -488 |
| signature: failed | 0 | 500 | +500 |
| signature: not_available | 12 | 0 | -12 |
| state_aid: available | 55 | 55 | +0 |
| state_aid: failed | 0 | 1 | +1 |
| state_aid: not_available | 445 | 444 | -1 |
| status_events: available | 0 | 0 | +0 |
| status_events: failed | 0 | 500 | +500 |
| status_events: not_available | 0 | 0 | +0 |
| subunits: available | 401 | 0 | -401 |
| subunits: failed | 0 | 500 | +500 |
| subunits: not_available | 99 | 0 | -99 |
| website: available | 39 | 0 | -39 |
| website: failed | 180 | 310 | +130 |
| website: not_available | 252 | 190 | -62 |
| website: ambiguous | 27 | 0 | -27 |
| website: blocked | 2 | 0 | -2 |

Observed same-cohort section losses: accounts, activity, gleif, group, hiring, identity, inspections, licences, procurement, prokura, research, roles, signature, state_aid, status_events, subunits, website. Live confirmation is INVALID because all run HTTP requests failed; code regression is unproven.

| Metric | S6 |
|---|---:|
| External process wall seconds | 954.406 |
| Margin seconds | 1145.594 |
| Available claims | 16013 |
| Largest profile bytes | 90442 |
| Envelopes / profiles / pages | 500 / 500 / 502 |
| Placeholders | 0 |
| Unsupported synthesis / briefing values | 0 / 0 |
| Website deadline hits | 0 |
| run_status | partial |
| Live HTTP successes | 0 |
| Cost USD | 0 |

Process and artifact checker both exited 0. The checker validates saved proof and permits explicit source failures; it does not certify outbound connectivity. Zero websites/deadline hits here do not prove live performance. All company error codes are in company-errors.json. The report warning is preserved in summary.json. No push, tags, fixes, or second live run.

Privacy guard: 17 passed.
