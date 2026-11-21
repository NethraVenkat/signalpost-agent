# Licence API and per-period audit confirmation

Run `r5-licence-audit-20261126` used seed 20261126 and the unchanged final500e input hashes, fresh state, exactly seven evaluator flags and a 2,100-second budget. The process exited 0 after 1,627.015 seconds, leaving 472.985 seconds. Minimum free disk was 8,817,459,200 bytes. Live robots, Brreg and GLEIF preflight requests returned 200 outside the socket-restricted sandbox.

| Measure | Result |
|---|---|
| Envelopes / profiles / site pages | 500 / 500 / 502 |
| Available claims | 79,601 |
| Licence claims / companies | 22 / 10, recovered from 0 in the preceding run |
| Audit flags / companies | 2,750 / 497 |
| Websites / exact-number VERIFIED | 41 / 33 |
| Website deadline hits | 0 |
| Unsupported synthesis / briefing values | 0 / 0 |
| Output gate | passed, 3,134 source blobs verified |
| Largest profile HTML | 234,793 bytes |
| Run status | partial |
| Cost | $0 |
| Stored-evidence sample | 200 supported, 0 contradicted, 0 missing blobs/hash mismatches |
| Wilson 95% lower bound | 98.1155%, passes the 95% gate |

The sample seed is 202611200628, stratified across all 15 published families. The full sample results and per-section states are in the adjacent JSON files. Section failures remain visible, including three accounts failures, four signature failures, three prokura failures, two group failures, five procurement failures and 182 website failures. An exit code of zero accompanies a partial result.

The official schema documents `/{index}/revisjon/ikkeRevidertAarsregnskap` and `/{index}/revisjon/fravalgRevisjon`. Claims publish literal boolean flags per period. Their evidence retains the existing response URL, UTC retrieval time, SHA-256, individual JSON pointer, verbatim span and extraction method. No accounts requests were added. Missing, non-boolean, conflicting duplicate or doubly affirmative flags are withheld. The last condition is our conservative ambiguity rule.

Finanstilsynet's named public registry routes use the documented official-API policy, with serial requests and at least one second spacing after completion. Official API robots probes elsewhere have five attempts with 5/20/40/60-second backoff, subject to the existing deadline. Crawled sites retain fail-closed robots handling.

All 1,499 full-suite tests passed across four shards after correcting the affected shard, including the updated independent boolean auditor. A separate privacy/public-name/overflow run passed 19 tests. The 25 status-event and consolidated regression tests also passed. No website pilot was implemented.

[Publisher API and limits](https://api.finanstilsynet.no/registry/index.html), [NLOD 2.0 catalogue entry](https://data.norge.no/en/data-services/71714342-89e3-3f0b-9ffd-94cd5952f287/api-for-finanstilsynets-registry), [Accounts schema](https://data.brreg.no/regnskapsregisteret/regnskap/v3/api-docs).
