# P3e — 500-company scale measurement at HEAD (incl. Stage S)

Seed **20261119**, 500 mod-11-valid numbers drawn with `random.Random(20261119).sample` from the verified 411,160-row universe after excluding **1,205** numbers: every committed sample/batch input plus every sample file on disk under `reports/`. That includes P2's 500, whose inputs were never committed because `.gitignore` excludes `*.jsonl`/`*.csv`. Overlap 0, asserted (a first draw that used committed files only overlapped P2 by 2 and was discarded before any run). Rows come from the 2026-11-16 Brreg snapshot (`56922f51…8693e1`); 498/500 were found, and 992666595 / 997863712 used the runner's live lookup. Inputs `companies500.jsonl` / `registry500.csv` are committed here, and P2's are added to `reports/r5/scale500/` in the same commit.

Clean clone of `d61014e` at `.data/r5/p3e-clean/repo`, `uv sync --frozen`; full pytest inside the clone **1359 passed** (`pytest-clone.txt`). One run, exactly seven flags, `--expected-count 500`, no retry needed.

| | P2 (seed 20261118, e9c067a) | **P3e (seed 20261119, d61014e)** |
|---|---|---|
| all gates incl. `check_live_run --count 500` | pass (after verifier fix) | **pass, first check** |
| effective time budget | 2,100 s (fixed default) | 10,500 s (scaled, P3a) |
| wall | 1,838.9 s | **2,591.1 s (24.7% of limit)** |
| deadline hits | 500 | **0** |
| output placeholders | 15 | **0** (all 500 `complete`) |
| envelope output | 267.1 MB | **211.2 MB** (cap 268.4 MB) |
| GLEIF / TED | `deadline` for all 500 | **finished for 500 / 497 + 3 blocked** |
| Stage S (state aid, research, licences, inspections) | not in code | **finished for all 500**: 46 / 4 / 14 / 7 companies |
| HTTP | 4,156 / 9,250 | 5,651 / 9,250 |
| largest profile | 222,718 B | 247,906 B |
| facts / websites / social | 65,784 / 37 / 16 | 67,567 / 36 / 22 (12 companies) |
| cost | $0 | $0 |

Different samples, so coverage is not a before/after comparison. Wall is longer than P2 because nothing was cut off this time. P2 stopped at its 2,100 s deadline with optional work pending for all 500 companies; P3e ran every section to completion, including website pass 2 (1,259 s). Exact-ID sources started at 24 s (P2: never reached).

The 3 TED `blocked` sections are TED's robots refusal of one request (`public_robots_blocked`), honoured as such. One accounts section failed (source error, explicit). Official-source transients: 3 attempts, 3 unrecovered.

## URL inventory

`urls.md` / `urls.json`: every published website (36) and social URL (22) with exact excerpts, proof tier, retrieval time and SHA-256. Automated verdicts (legacy `precision_ledger` recheck): websites 22 correct / 14 doubtful / 0 wrong; social 14 / 3 / 5. **All 22 non-correct items are listed first for hand-check.** The 5 "wrong" labels are the tool limitation already seen in P2: tiers `own_contact_follow_us_v1` (927612372 LinkedIn + Facebook) and `owner_jsonld_sameas_v1` (970545204 Facebook, Instagram, YouTube) postdate the legacy recheck. `check_live_run`/`verify_output` independently verified all of them. Labels are kept as produced.

Receipts: `run.json`/`run.txt`, `check_live_run.json|txt`, `summary.json`, `report.json`, `source_manifest.json`, `clean_clone.json`, `pytest-clone.txt`. Envelopes, profiles, state and site stay local under `.data/r5/p3e-clean/run-final`.
