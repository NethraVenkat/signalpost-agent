# Final500e: fresh clean-clone qualification

**Full check passed on the first live attempt.** Application commit `40813fecdfc6536579d456a1622f260c3bf6044c`; seed **20261126**. Exactly seven flags, `--expected-count 500`, fixed 2,100-second budget, fresh state and clean clone; runtime-only frozen install, pytest absent from clone. No second live run, offline site repair, tags or push.

| Metric | Result |
|---|---:|
| CLI / check_live_run exit | 0 / 0 |
| Process wall / margin under 2,100 s | 1828.86 / 271.14 s |
| Run status / warnings | partial / none |
| Envelopes / JSON profiles / company HTML pages | 500 / 500 / 500 |
| Placeholders | 0 |
| Deadline-hit companies | 173 (all website) |
| Largest profile HTML | 249,279 bytes (<250,000) |
| Unsupported synthesis / briefing values | 0 / 0 |
| Complete cited briefing contracts | 500 |
| Available claims | 71,812 |
| HTTP attempts / successful 2xx responses | 6,151 / 4,607 |
| Activity available / failed | 500 / 0 |
| Minimum free bytes sampled | 17,716,875,264 |
| Provider cost | $0 |

| Information type | Companies | Claims |
|---|---:|---:|
| signature | 488 | 1457 |
| signature_rule | 382 | 382 |
| prokura | 111 | 224 |
| prokura_rule | 90 | 90 |
| group | 35 | 67 |
| consolidated | 5 | 334 |
| state_aid | 55 | 379 |
| websites | 39 | 39 |
| social | 10 | 17 |
| all_available | 500 | 71812 |

Signature/prokura totals include explicitly labelled publisher possible combinations; registered free-text rules are separate rows and subsets. Group claims are direct parent/subsidiary edges involving the exact requested orgnr. The 173 website deadline hits are incomplete recall, not successful negative checks; [every affected company and section](deadline-losses.json). Zero unsupported values does not mean complete source coverage. The full checker permits honest unavailable/failed sections and partial run status.

Sampling excluded **6,808** prior numbers, with zero overlap and 500 unique valid IDs. The hash-checked universe has 411,160 rows; eligible pool 405,937. The bulk snapshot covers 499; `918032320` remained in the frozen sample and resolved through the normal live identity path. No replacement draw. Inputs and bulk extract are committed with raw hashes. [Sampling](sampling.json) and [exclusions](exclusions.json).

The revised user start threshold was >=10,000,000,000 bytes, with the conservative 3 GiB stop guard retained. Setup actually began with 20,329,242,624 bytes free; after setup 19,454,918,656 remained. No disk stop occurred. Earlier failed 15 GiB setup attempts remain under trials and are superseded by this new authorization and measured run.

Network preflight returned 200 for Brreg, NAV HEAD and the selected company robots URL through the production safe transport. The final500 clean clone also replayed the corrected P1 committed packet: 200 correct / 0 incorrect / 0 unverifiable, nominal Wilson lower bound 98.12%, with no network and no pytest. [P1 clone replay](P1-clone-replay.json).

Source checker verified 3,133 saved blobs, 31,436 financial inputs, 1,128 derived financial metrics, 6,844 registry events and 448 exact-official items. All 500 briefing contracts passed. Internal completion wall is 1,825.282 s; external process wall is 1,828.86 s. Source outputs and hashes remain unchanged after measurement. The generated HTML cap passed directly, so no application repair or offline rebuild was needed.

[Clean clone and source hashes](clean-clone.json) | [Exact seven-flag command and wall](attempt1-execution.json) | [Disk guard](attempt1-disk-guard.json) | [Preflight](preflight-1.json) | [Full checker](attempt1-check.json) | [Checker execution](attempt1-check-execution.json) | [All counts/states/output hashes](summary.json) | [Run log](attempt1-run.txt).

Full pytest and final privacy receipts are recorded after the run in the main checkout; neither runs in the qualification clone.

Final main-checkout full pytest: **1,471 passed in 976.77 seconds** ([receipt](pytest.txt)). No pytest ran in the clean qualification clone. Final report privacy scan is recorded in [privacy-final.txt](privacy-final.txt).

Final privacy guard: **5 passed in 9.86 seconds**. Qualification used one live run; no retry or offline site repair. Original saved outputs remain unchanged, and all code/test checks are complete.
