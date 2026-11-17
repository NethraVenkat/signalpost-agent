# P3g — 500-company re-measure at the fixed default time budget

Seed **20261120**: 500 mod-11-valid numbers from the verified universe after excluding 1,705 numbers (every committed sample and every sample file under `reports/`, including P2's and P3e's 500). Overlap 0. Rows come from the 2026-11-16 Brreg snapshot; 499/500 were found, and 912766349 used the live lookup. Clean clone of `aceb24b` (P3f), full pytest inside the clone **1360 passed**. One run, exactly seven flags, no retry.

| | P2 (2,100 s, before P3) | P3e (scaled 10,500 s) | **P3g (fixed 2,100 s default)** |
|---|---|---|---|
| all gates incl. `check_live_run --count 500` | pass after verifier fix | pass | **pass** |
| wall | 1,838.9 s | 2,591.1 s | **1,893.5 s (90% of 2,100; 206.5 s margin)** |
| crawl stop (0.85 x 2,100) | 1,792 s | — | 1,786 s, then outputs 63.6 s + site 38.9 s |
| companies with any deadline-cut section | 500 | 0 | **177, website pass 2 only** |
| output placeholders | 15 | 0 | **0** (all 500 `complete`, 214.0 MB) |
| GLEIF | `deadline` x 500 | finished 500 (78 found) | **finished 500 (68 found)** |
| TED | `deadline` x 500 | finished, 3 robots-blocked | **finished, 10 robots-blocked** |
| Stage S state aid / research / licences / inspections | n/a | finished 500: 46 / 4 / 14 / 7 | **finished 500: 44 / 11 / 11 / 4** |
| accounts | — | 499 + 1 failed | 500 |
| HTTP | 4,156 | 5,651 | 5,267 / 9,250 |
| facts / websites / social URLs | 65,784 / 37 / 16 | 67,567 / 36 / 22 | 69,178 / 47 / 40 (19 companies) |
| largest profile | 222,718 B | 247,906 B | 248,810 B |
| cost | $0 | $0 | $0 |

The samples differ, so coverage is not a before/after comparison. Under the same fixed budget as P2, the deadline now only cuts optional website pass-2 work. 176 companies still had website candidates pending (`pass2.states`: deadline 176, no_pending_candidates 244, already_verified 37, checked_no_gain 43). Every exact-ID source finished for all 500 companies, with no section converted to absence. The TED `blocked` states are TED robots refusals (`public_robots_blocked`), honoured as such.

## URL inventory

`urls.md` / `urls.json`: every published website (47) and social URL (40), with exact excerpts, tier, retrieval time and SHA-256. Automated verdicts (legacy `precision_ledger` recheck): websites 36 correct / 11 doubtful / 0 wrong; social 20 / 6 / 14. **All 31 non-correct items are listed first for hand-check.** All 14 "wrong" labels are tiers the legacy recheck predates (`own_contact_follow_us_v1` 9, `owner_jsonld_sameas_v1` 5), the same tool limitation as in P2 and P3e. `check_live_run`/`verify_output` independently verified all of them. Labels are kept as produced.
