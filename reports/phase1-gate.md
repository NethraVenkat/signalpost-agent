# Phase 1 gate — version 1.0.0

17 October 2026 (IST). Branch `revision/judge-fixes`. Gate run on commit `7f197cb`; this report and the README line were added afterwards. Nothing pushed.

> Commit IDs below are the ones in use when this was written. The history was later rewritten (messages only); the mapping is in [v1.0.0-gate-checks.md](v1.0.0-gate-checks.md#commit-ids-after-the-history-rewrite).

## What "the gate" was
The master prompt did not reach this session, so the gate is the one defined from the approved Step 1 plan, stated here so it can be corrected:
1. Full test suite passes.
2. Same uniform 1,000-company sample as Step 1 (seed 20261017, input SHA-256 `bba3114b…9649a`, captured public bulk subset), fresh state per run, websites + hiring + public activity, no paid search/LLM.
3. For each run: exit 0 on its own, exactly 1,000 envelopes and 1,000 profiles in input order, wall time ≤ budget + 5 s, no unhandled exception, no harness kill, all 28,726 baseline identity claim IDs preserved.
4. Output verifier on the normal run; site generated or explicitly recorded as skipped.
5. Includes the 3,000-request cap on the final code.

## Result: all five runs pass

| Run | Wall s | Limit | Exit | Envelopes / order | States | Identity IDs | HTTP | Deadline hits | Site |
|---|---:|---:|---:|---|---|---:|---:|---:|---|
| Normal (2,400 s, 20,000 req) | 248.7 | 2,405 | 0 | 1000 / exact | 1000 complete | 28,726 / 28,726 | 5,380 | 0 | available |
| 30 s | 29.3 | 35 | 0 | 1000 / exact | 1000 complete | 28,726 / 28,726 | 395 | 1000 | skipped, recorded |
| 120 s | 103.1 | 125 | 0 | 1000 / exact | 1000 complete | 28,726 / 28,726 | 2,429 | 696 | available |
| 600 s | 270.9 | 605 | 0 | 1000 / exact | 1000 complete | 28,726 / 28,726 | 4,998 | 0 | available |
| 3,000 requests | 164.0 | 2,405 | 0 | 1000 / exact | 1000 complete | 28,726 / 28,726 | 3,000 | 0 | available |

- Profiles: 1,000 in every run. Peak sampled process-tree RSS 0.34–1.31 GB (sampled, not a certified ceiling).
- Hiring under the 30 s and 120 s limits is `failed`/`deadline` where the NAV feed was not reached; registry sections are intact.
- Output verifier (normal run): 1,000 lines, schema valid, 69,447 published claims, 3,861 source blobs verified, 8,104 synthesis sentences, 0 unverified values.
- Tests: 458 passed.
- The wall-time comparison with Step 1 (375 s) is not an optimisation claim: the sources are live and vary.

## Phase 1 items
- **Site, Equinor** (`9942805`): 332,392 → 125,439 bytes. 50 Evidence Explorer rows are rendered, the other 351 come from the company data file on a button click. All 401 claims stay reachable; exports and schemas unchanged. Chrome check at desktop and mobile widths: 50 → 401 rows, no horizontal overflow.
- **Site, malformed input** (`79358cc`): a malformed identifier gets no page and is listed in a notice; the audit's 24-row batch now builds 23 pages.
- **P1a, registry-website normalisation: not implemented, premise did not hold.** My earlier "59 of 112" counted name-slug guesses. For the registry website itself, 6 of the 86 unverified companies had a domain that does not resolve, and the code already tries https/http and www/non-www for each. Registry-website outcomes were mostly page-level: proof not found (23), foreign number (13), declared but unverified (9), timeouts (8), URL refused (6; cause not examined, a redirect off the declared domain is the likely one). Nothing in the 6 was fixable by path stripping or IDNA. The 6 still fail after this work.
- **P1b, website request budget: not in effect, withdrawn.** Commit `3fe57cb` changed the `Config` defaults to 8/13, but the CLI passes its own argparse defaults (6/9, deadline fraction 0.85) explicitly, so no CLI run, including every gate run, used 8/13. Found while preparing the release; the `Config` defaults are back to the CLI values (6/9/0.85), the README says so, and a test now fails if the CLI and `Config` defaults differ. Raising the caps is a Phase 2 item: it was never measured. The flags `--website-request-cap 8 --website-total-request-cap 13` work but are untested. Feed and sitemap guessing keeps its effective ceiling via `WebsiteHttp.discovery_cap` (equal to the old ceiling at 6/9).
- **P1c, standard proof pages** (`ca459dd`): `/kontakt`, `/kontakt-oss`, `/om-oss`, `/om`, `/personvern` and `/personvernerklaering` are tried after home-page links, **within the per-company cap of 6 that the CLI uses**, so typically the first three or four. Proof rules unchanged (a foreign number still rejects). With a higher cap all six are reachable (tested).
- **P1c effect (caps 6/9), normal run, same sample:** verified websites 51 → 58 (8 new, 1 lost to a transient DNS failure on a company that made no website request); HTTP 4,953 → 5,380 (+8.6%); no website claim was lost to a rule change. Companies recording `website_budget_exhausted` rose from 103 to 277 because the extra pages are probed until the cap, so the cap of 6 is reached more often, not less. Verified-website gain is 7 on a sample of 1,000, which is within live variation; a paired rerun is needed before calling it an effect.

## Ambiguous mapping (`15a0252`)
Ambiguous modules map to `source_error`; claims and sections stay `ambiguous`; `submission_error` is only for invalid input. All 1,000 envelopes are `complete` in the normal run (was 931 + 69).

## Open
- Version tag and push are not done; the version is committed as 1.0.0.
- Live variation: single runs only. Differences of a few companies are not measurements of an effect.
- Phase 2 items are not started.
