# Official Brreg authority and group API implementation

Baseline `ac88ab0`. Official API policy follows the user-confirmed existing registry client policy; earlier crawler robots gating of G1 is superseded. Website crawling keeps its robots policy. See [policy decision](../../DECISIONS.md) and [sources](../../../../docs/SOURCES.md).

All nine exact-orgnr probes returned 200: Equinor `923609016`, DNB Bank `984851006`, Norsk Hydro `914778271`, each at fullmakt/signatur, fullmakt/prokura and konsernstruktur. [Probe receipt](probe.json) and [driver](probe.py). Equinor authority routine status NA remains explicitly unavailable; no successful authority claims are inferred from HTTP 200 alone.

Real-response test fixtures are in `tests/fixtures/brreg_corporate/`, with original-response and sanitized fixture-body hashes. Only personal birth-date/identifier field values are redacted; company identifiers, rules, names, combinations and hierarchy edges are retained. Original unmodified responses remain local, with no credential material committed. Extraction and the saved-output auditor use the same exact-orgnr extractor; tampering and wrong-company tests exercise both. Group tests exclude siblings and indirect descendants and check explicit parent pointers. A runner/site integration test proves default-on calls use the registry client without robots, retain every new fact, and defer large authority collections into company-local data under the unchanged HTML cap.

Full pytest: **1,464 passed in 976.14 seconds** ([receipt](pytest.txt)); separate privacy guard: **5 passed in 10.60 seconds** ([receipt](privacy.txt)). Twenty new cases cover saved real responses, wrong identity/URL, value tampering, direct group scope and nesting, HTTP failures, full prokura combinations, default enablement and runner/site integration. Archived synthetic replay helpers explicitly retain their original source scope; no missing API response is fabricated. Measured implementation commit: `4ca3443`. The normal-network standard-100 comparison below completed after that commit. No 500 run, tags or push.


## Standard 100 comparison

The same standard seed-20261017 membership and bulk input were used with exactly seven evaluator flags, fresh state and the fixed 2,100-second budget. Baseline `ac88ab0` retains the earlier standard-100 measurement at `f740933`; its later application changes repaired rendering and adaptive I/O isolation. This comparison reuses those saved baseline counts; it is not a new live baseline run. Input SHA-256 matches the prior execution receipt.

| Available information | Baseline: companies / claims | Current `4ca3443`: companies / claims |
|---|---:|---:|
| Signature: registered rules + publisher possible combinations | 0 / 0 | 95 / 291 |
| Signature: registered rule text only | 0 / 0 | 72 / 72 |
| Signature: possible combinations only | 0 / 0 | 94 / 219 |
| Prokura: registered rules + publisher possible combinations | 0 / 0 | 10 / 20 |
| Prokura: registered rule text only | 0 / 0 | 8 / 8 |
| Prokura: possible combinations only | 0 / 0 | 9 / 12 |
| Direct group relationships | 0 / 0 | 9 / 60 |
| Direct parent relationships | 0 / 0 | 4 / 4 |
| Direct subsidiary relationships | 0 / 0 | 7 / 56 |
| All available claims | 100 / 13,799 | 100 / 14,165 |

Subtype rows overlap in company coverage; they are not summed as distinct companies. Possible combinations are the publisher's qualified machine output, not an assertion that a combination overrides a registered free-text restriction. Five signature lookups and five prokura lookups returned routine NA; these remain unavailable. Another 85 prokura checks yielded no publishable rule/combination. The group endpoint returned 404 for 91 companies. None is reported as a successful authority/group claim.

There are **371 new corporate claims**, versus a **366 net claim increase**. Other families are unchanged except five website claims for `998340888`: the official website, public brand, phone and two descriptions were withheld after current candidate checks timed out (`napolitana.no`/`.com`). This is retained as a fresh-source coverage difference, not hidden or offset with unsupported data. Websites are 7 versus 8 previously; social URLs remain 7. [Family deltas](standard100-family-deltas.json).

| Verification metric | Result |
|---|---:|
| Process wall / margin under 2,100 s | 490.16 / 1,609.84 s |
| CLI / full `check_live_run --count 100` exit | 0 / 0 |
| Run status / warnings | partial / none |
| Envelopes / JSON profiles / company HTML pages | 100 / 100 / 100 |
| Placeholders / deadline hits | 0 / 0 |
| Largest HTML profile | 247,950 bytes (<250,000) |
| Unsupported synthesis / briefing values | 0 / 0 |
| Complete cited briefing contracts | 100 |
| Saved source blobs / financial inputs verified | 586 / 6,296 |
| Corporate claims re-derived from original saved responses | 371 |
| All HTTP attempts / successful 2xx responses | 1,281 / 954 |
| Corporate HTTP attempts: 200 / 404 | 300: 209 / 91 |
| Provider cost | $0 |

The internal completion wall in the checker is 487.531 s; 490.16 s is the external process wall. The checker re-derives every available signature/prokura/group value from the exact saved response and validates its URL, orgnr, JSON locator and verbatim evidence span. Existing section failures remain explicit in partial status; a checker pass permits honest source unavailability. The 95/10/9 corporate sections marked available exactly match companies with available corresponding claims.

One earlier restricted-network attempt had **zero successful HTTP responses**, 2,992 bulk/bundled claims and no corporate claims; it is not live-recall evidence despite passing the saved-output checker. Its outputs and receipts are preserved in [network-restricted trial](trials/network-restricted/SUMMARY.json). A production-safe-transport preflight on normal network returned 200 before the fresh-state normal-network retry. The measured application code was unchanged; only the measurement helper's output/state directory and execution environment changed. No third 100 run or any 500 run was performed.

[Exact command, code/input/output hashes and wall](standard100-execution.json) | [Counts and section states](standard100-counts.json) | [Qualifier-level counts and original output hashes](standard100-details.json) | [Full checker](standard100-check.json) | [Checker execution](standard100-check-execution.json) | [Run log](standard100-run.txt). Reproduction drivers: [standard run](standard100.py) and [qualifier census](summarize.py); they require the saved baseline/run data at the recorded local relative paths. No generated site or personal response blobs are committed.

No 500 run, tags, merge or push. Stop after committing these receipts.

Final report/privacy scan: [privacy-final.txt](privacy-final.txt). Application source files remain unchanged from `4ca3443`; the normal-network retry changed only measurement directories/environment.
