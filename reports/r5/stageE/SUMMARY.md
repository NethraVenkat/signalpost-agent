# Stages C2 and E - final summary

Branch revision/r5. Stage C2: `dde5da7b91c5ef97495ea3df8bbe5e50c3f17671`. Stage E: `8ab8004f4977f6ceb34052c54d21ce5acacb010a`. Author and committer: Nethra Venkat. No push, tag change or publication. Expected and measured enrichment cost: $0; no paid models/search. Production discovery retains the release allowance because C2 gained no website; refresh comparison fixes equivalent publication-time formatting.

| Seed | Prior sites | C2 trial sites | Retained-policy E sites | Budget-limited prior -> C2 trial | C2 HTTP / wall s | E HTTP / wall s |
|---|---:|---:|---:|---:|---:|---:|
| 20261017 | 5 | 5 | 5 | 18 -> 17 | 690 / 398.807 | 690 / 368.169 |
| 20261113 | 4 | 4 | 4 | 24 -> 18 | 793 / 447.791 | 785 / 399.116 |
| 20261114 | 3 | 3 | 3 | 22 -> 20 | 719 / 333.011 | 719 / 347.072 |

C2 experimentally permitted another +10 HTTP/+6 DNS (absolute 23 website HTTP/18 DNS) only for capped companies with untried ranked candidates and remaining global budget. Extensions: 2/8/5 companies, zero extension-proved sites; no added/removed website or social URL. Some extensions spent only DNS attempts; additional HTTP fetches did not establish exact-number proof. As required, restore +5 HTTP/+4 DNS byte-for-byte and archive the experimental patch/tests. Budgets/states can drift with live networking; do not interpret fewer cutoff states as causal recall gains. Full evidence: [C2 results](../stageC2/RESULTS.md), [URL changes](../stageC2/new_websites.md), metrics.json and each run directory.

All six three-cohort trial/final runs used exactly seven evaluator flags with fresh state: 100 ordered terminal envelopes and generated sites, five cited briefing topics, zero unsupported values, <=1850 requests and within default time limits, $0. All four E measurements, including live refresh, have identical production source hashes. Failures remain explicit; no source, proof, veto, robots, politeness, once-only cache or identity rule was relaxed.

| Offline refresh check | Result |
|---|---:|
| Causal interventions detected | 7/7 |
| Supported field events | 40 |
| Unexpected field events | 0 |
| Event precision | 1.0 |
| Causal recall | 1.0 |
| Unchanged changes / false-change rate | 0 / 0.0 |
| Idempotent changes (also every changed replay) | 0 |
| Prior claims preserved on transient failure | 112 |

Replay tests use one exact-identity company from saved seed-20261113 responses, not population-wide ground truth. Production proof/extraction code runs directly; every response is hashed, unrecorded routes fail offline. Seven isolated mutations: employees, address, accounting year, name, proven subunit, inactive NAV ad and site 404. Unchanged/repeated snapshots emit zero company changes and zero coverage observations. Transient failures preserve prior evidence IDs/times and immutable bodies with visible stale markers. The synthetic empty NAV forward tail is explicit and supplies no claim: real saved ad detail is mandatory; full-feed discovery completeness is not tested. CI collects the new offline tests automatically. [Refresh documentation](../../../docs/REFRESH.md).

Live frozen refresh: 0 company changes (0 material, 0 minor), separately 0 coverage observations; 0 carried claims; 684 HTTP, 368.449s wall, zero unsupported values, $0. This user-requested check uses seven flags plus --previous (explicit documented exception), latest frozen envelopes and a fresh runtime cache. Historical bodies copied only after runtime for independent verification. Full events/evidence and exact command in live_refresh/. Observed changes are not a ground-truth precision measurement.

The first live check exposed 620 false minor registry events plus 25 false observations from equivalent offset/Z timestamps, which overflowed the unchanged 250 KB page gate. Normalize aware registry publication instants only for comparison and compare uncertain-section semantic values by field; preserve publisher text/evidence and all real field/instant differences. Exact saved 100-company pair replay then emitted zero changes/observations, verified all 1202 registry events and produced a largest profile of 249314 bytes. Pre-fix evidence and regression results are retained. No renderer or proof gate was weakened.

Validation: experimental C2 full pytest 920 passed; rollback/current full pytest 914 passed; Stage E final full pytest 916 passed; final offline/timestamp checks 4 passed. Earlier gates had only an optional pytest cache-write permission warning; the final gate disabled that cache and passed without warnings. [Stage E measurements](RESULTS.md), [machine-readable refresh results](refresh_results.json), [URL changes](new_websites.md), full unchanged URL receipts in url_inventory.json. No screenshots were required or newly captured for these backend stages.

Decisions: [DECISIONS.md](../DECISIONS.md), C2 and E sections. No copied external application code or new API source. Existing official registry/NAV and verified-site source policies and licences remain unchanged.

Hand check:

- Review the C2 archived patch, extension records and required rollback; no new URL needs approval.
- Inspect all seven planted source mutations and their before/after evidence, particularly proven subunit parent, inactive NAV detail, site 404 removal versus timeout staleness.
- Check the fixture scope and synthetic NAV forward-tail disclosure before generalizing precision/recall.
- Review live material events and coverage observations separately in live_refresh/results.json; source publication times are not inferred effective dates.
- Reproduce the offline harness from its pinned fixture and inspect stale markers on the generated transient profile.

Stopped after C2, E and this summary. No further stage started.
