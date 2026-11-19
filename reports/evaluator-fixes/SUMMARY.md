# Evaluator fixes and verification

Local work on the revised entry; no push or deployment. Runtime fixes and the bounded replay bundle are committed in `46e8dd408501c129a611149443c65e1f2dc6925c`. The later documentation/receipt commit records the final state. No official score or qualification is claimed.

| Fix | Result |
|---|---|
| 1. Unknown flags | `parse_known_args`, stderr warning, report argument inventory; real CLI tests pass |
| 2. Honest failure / outage guard | Failed/blocked companies are not complete; 25 failed live identity lookups, 15-second pause, three recovery checks; confirmed outage exits 1 and preserves membership |
| 3. Website deadlines | Removed the N/500 multiplier from the fixed-budget website window; [company-level diagnosis](DEADLINE_LOSSES.md); fresh live check has zero deadline hits |
| 4. Robots | Unreachable robots blocks the origin; reset/timeout/cache tests pass; fresh live run made zero Støtteregisteret data requests |
| 5. Judge instructions | Root [SUBMISSION](../../SUBMISSION.md) and [OUTPUT_CONTRACT](../../OUTPUT_CONTRACT.md) added |
| 6. Size | Final cleanup removes 210 generated JSON files / 1,176,765,747 bytes; [manifest](PRUNED_DATA.json), [size receipts](SIZE.md); one original source body restored during final review |
| 7. Clone-only replay | [Committed scope and licences](EVIDENCE.md), [fresh-clone receipt](FRESH_CLONE.json), [replay result](REPLAY.json); no local research state needed |
| 8. Rewritten history | [Mapping and verification limits](../../HISTORY_MAPPING.md); no invented equivalence for unmapped labels |
| 9. Documentation | Current defaults checked against code and NAV metadata; [scan](DOCUMENTATION_SCAN.json); dated measurements retained as historical |
| 10. OSM licence | Shipped 18,592-byte database explicitly attributed to © OpenStreetMap contributors under ODbL 1.0, including share-alike, in [SOURCES](../../docs/SOURCES.md) |

## Sequential 100-company checks

All runs below used the same 100 valid organisation numbers from the committed baseline cohort, with independent state. The first four are the requested checks immediately after fixes 1–2; the last is a fresh check after the runtime window/robots corrections. These are observational reruns against changing live sources.

| Case | Exit | Envelopes | Deadline hits | Status | HTTP attempts | Process wall s |
|---|---:|---:|---:|---|---:|---:|
| After 1–2: documented command | 0 | 100 | 96 | partial | 985 | 674.97 |
| After 1–2: minimum flags | 0 | 100 | 44 | partial | 1158 | 362.06 |
| After 1–2: three invented flags | 0 | 100 | 45 | partial | 1156 | 363.26 |
| After 1–2: external network blocked | 1 | 100 | 0 | aborted | 28 | 18.13 |
| After 3–4: documented command | 0 | 100 | 0 | partial | 1075 | 537.83 |

The blocked test denied external sockets and DNS, permitting only loopback IPC required by Windows asyncio. It made 25 initial attempts and three recovery attempts, waited 15 seconds, produced zero available claims, and reported 100 `source_error` envelopes with no `complete` companies. No host outage was inferred from budget expiry or a mere HTTP response error.

The final normal run remained `partial`: lack of deadline hits is not proof that every source succeeded. Per-company request/DNS ceilings, source refusals and unavailable facts remain explicit. Removing the early cutoff did not relax proof, robots, pacing or global budgets.

## Validation

- Targeted CLI/startup/resilience tests: 14 passed.
- Targeted budget and finalisation tests: 19 passed.
- Targeted public-source and fail-closed robots tests: 44 passed.
- Current documentation and seed/licence checks: 3 passed.
- Fresh clone: frozen install on Python 3.13.16; offline committed replay passed, with no `.data/` or `state/` directories.
- Full fresh-clone offline suite at `46e8dd4`: 1,404 passed, one failed. The failing CLI-default comparison did not evaluate Pydantic default factories; that test was corrected and passed on rerun alongside the three documentation/licence checks. No runtime change was needed.
- Full saved-source verification of the final 100-company run: passed; 421 source blobs, 13,567 published claims, 100 complete briefing contracts, zero unverified synthesis/briefing values. [Receipt](FINAL_SOURCE_VERIFICATION.json).

The replay archive deliberately represents the earlier after-1–2 baseline, not the later corrected run. It reproduces all 100 saved-output counts, while original-source byte checks cover only three official identity/accounts extracts. Historical final500c source bodies remain outside the clone and are not independently replayed by this fixture.
