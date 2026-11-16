# P2 — new 500-company clean-clone qualification

Seed **20261118**, 500 mod-11-valid organisation numbers drawn uniformly (`random.Random(20261118).sample`) from the verified 411,160-row universe after excluding all 705 numbers found in any committed sample/batch input, including `tests/fixtures/ci20.jsonl`. Overlap 0, asserted. Registry rows were extracted from the **new 2026-11-16 Brreg snapshot** (`56922f51…8693e1`). 498/500 were found; 928822125 and 929035445 are absent from today's register and used the runner's live-lookup fallback within the same limits. Inputs: `companies500.jsonl`, `registry500.csv`, provenance in `clean_clone.json`.

## Clean clone

`git clone --no-hardlinks --branch revision/r5` into `.data/r5/scale500-clean/repo` at e9c067a, status clean, `uv sync --frozen`. signalpost imports from the clone's own `.venv`/`src` (`clean_clone.json` → `installation`). The checker/verifier/ledger/extraction scripts were byte-identical to the main checkout. Full pytest inside the clone: **1292 passed in 614.88s** (`pytest-clone.txt`).

## Run — exactly seven evaluator flags, from the clone

`run.json`: `python -m signalpost.cli run --organisations companies500.jsonl --bulk registry500.csv --output … --profiles-output … --report … --run-id r5-scale500-seed20261118-final --expected-count 500`, fresh working directory, no other flags. Exit 0.

| Gate | Result |
|---|---|
| 500 ordered terminal envelopes | pass |
| Five cited briefing topics, complete contracts 500/500 | pass |
| 0 unsupported synthesis/briefing values | pass |
| HTTP ≤ 9,250 | **4,156** |
| Wall ≤ scaled time budget (effective 2,100 s = min(requested 2,100, 21 s × 500)) | **1,838.9 s** |
| Largest profile < 250,000 bytes | **222,718** (site available, 500 companies) |
| $0, zero LLM/search calls | pass |
| Official-source health | enhetsregisteret, accounts, NAV, GLEIF reachable; no outage, so no retry |

**Verification history (no recrawl, no union).** The first `check_live_run.py --count 500` (`check_live_run.txt`, exit 1) rejected one published claim, a correct HIGH publisher receipt on a page declaring windows-1252, because the verifiers double-decoded stored text. That was a verifier defect, fixed and gated separately in **1e0fd6b** (DECISIONS: "P2 finding"). The clone was fast-forwarded to 1e0fd6b, whose `src/` differs from the measured e9c067a only by the optional `Page(..., text=)` parameter, which the runtime never uses. The **same saved run** was then re-verified: `check_live_run-reverify.txt`, exit 0, all gates above (`summary.json`).

## Coverage at this scale (explicit states, not hidden)

| Section | States (companies) |
|---|---|
| identity | available 485, failed 15 |
| website | available 37, ambiguous 28, blocked 5, failed 169, not_available 261 |
| activity | available 290, failed 210 |
| hiring | available 2, failed 15, not_available 483 |
| gleif / procurement | failed 500 (`deadline`) |

- **Output-size valve:** 15 companies were reduced to terminal placeholders ("Envelope reduced to terminal placeholders by max-output-mb"; error `output/budget_exhausted`) once the default 256 MiB output safety ceiling was reached. Their state is `budget_exhausted`, with no facts; the other 485 are complete. This is the documented safety behaviour, but it means the default output ceiling cannot hold 500 full union envelopes plus profiles. It is recorded as a limitation, not altered here.
- **Deadline:** the crawl deadline (85% of 2,100 s) arrived with optional work still pending for all 500 companies (`deadline_hits` 500). GLEIF/TED therefore did not start (`deadline` for every company), and 190 website checks ended at the deadline. No state was converted to absence.

Published: 65,784 facts; 37 websites; 16 social URLs across 10 companies; 2 jobs; 5,819 activity claims.

## URL inventory

`urls.md` / `urls.json` list every published website (37) and social URL (16), with exact excerpts, proof tier, retrieval time and SHA-256, each re-hashed from the saved body with its excerpt found verbatim. Automated verdicts (existing `precision_ledger.recheck`): websites 23 correct / 13 doubtful / 1 wrong; social 10 / 1 / 5. **All 20 non-correct items are listed first for your hand-check.** The 6 "wrong" labels are ledger-tool limitations, not identity findings: the PDF-proven TOTEN FORSIKRING site and its social link raise `StopIteration`, and four X2 owner-declaration social tiers predate the legacy recheck. The full independent verifier passed all of them. Labels are kept as produced.

Receipts: `run.json`/`run.txt`, `check_live_run*.json|txt`, `summary.json`, `report.json`, `source_manifest.json` (clone `src/` at the measured commit), `pytest-clone.txt`, `verifier-fix/pytest.txt`. Envelopes, profiles, state and site stay local under `.data/r5/scale500-clean/run-final` (hashes in `summary.json`).
