# Signalpost: evaluator instructions

Overnight review: precision packet `35a547e` reproduces the seeded 200-claim audit from committed data alone. **50 correct / 0 incorrect / 150 unverifiable** under the strict literal-span test; nominal Wilson 95% lower bound **19.51%**. This is a direct-verbatim certification result, **not** an estimate that only 25% of business facts are true. Composite metadata, numeric/date formatting and short excerpts cause abstentions even when full-source semantic verification passed. [Methods and per-type results](reports/r5/precision-sample/SUMMARY.md); [website/social/brand human checklist](reports/r5/precision-sample/HUMAN_REVIEW.md), human review pending.

**Final500e was not run.** Initial setup and the single fresh setup retry failed the disk prerequisite: roughly 11.01 GB free on retry, below the requested 15 GB (the helper enforces 15 GiB). No sample was drawn with seed 20261126, no final500 clone was created, and no live or offline final500e qualification was claimed. Timing, coverage, largest profile and unsupported-value figures are **not measured**. Provider cost: **$0**. Original historical evidence was retained. [Failure/retry receipts at `129ce84`](reports/r5/final500e/SUMMARY.md). Earlier 100/500 measurements below remain separate historical results.

P3 verification: **1,464 pytest tests passed in 980.90 seconds** and **5 privacy checks passed** in the main checkout; [verification receipts](reports/r5/overnight/SUMMARY.md). No pytest ran in a final500 clone; none was created.

Use the exact revised commit hash supplied with this submission. Install in a fresh checkout with Python 3.12+ and uv:

```sh
uv sync --frozen
```

Run this command with the organiser's files. This example expects 100 input records:

```sh
uv run signalpost run --organisations batch.jsonl --bulk registry.csv --output out/envelopes.jsonl --profiles-output out/profiles.jsonl --report out/report.json --run-id evaluator --expected-count 100
```

Set `--expected-count` to the supplied membership. The agent does not choose its own companies. `--bulk` is optional; omit it for live identity lookups. The minimum invocation is:

```sh
uv run signalpost run --organisations batch.jsonl --output out/envelopes.jsonl --report out/report.json
```

No credentials, `.env` file, model service or separately downloaded bulk dataset are required. Default provider cost is USD 0, excluding compute, storage and network. Bundled discovery datasets and their source terms are declared in [SOURCES](docs/SOURCES.md). Optional paid-search support requires explicit environment configuration and is not required by these commands.

The default total budget is fixed at 2,100 seconds. HTTP attempts are capped at floor(1,850 × unique normalized input records / 100); overrides can only lower that cap. Website pass 2 ends by 1,700 seconds for default batches of 100 or more, inside the original crawl deadline, retaining finalisation time. Existing per-company limits, robots checks and domain pacing apply throughout.

Outputs:

| Path | Content |
|---|---|
| `out/envelopes.jsonl` | One ordered terminal envelope per input record, including duplicates and malformed identifiers |
| `out/profiles.jsonl` | Scorer-compatible profiles from the same claims and provenance |
| `out/report.json` | Run status, section counts, request log, budget use, warnings and site status |
| `out/site/` | Searchable offline site when the remaining budget permits rendering |
| `state/` | Saved sources and prior results; use a fresh working directory for an independent run |

Read `run_status`, `counts_by_state`, section availability, `warnings` and `site.state`. `partial` means outputs were written but some checks failed, were blocked or remained ambiguous. A partial run can exit 0. `failed` and `aborted` runs exit 1; a company whose sections all failed or were blocked is never counted as complete. Missing facts are not zeroes.

When the first 25 required live identity lookups all fail with network errors, the agent pauses 15 seconds and retries three. Only three further network failures confirm the outage and abort the run, naming `data.brreg.no`. Failed envelopes are still written for the entire input. Scattered failures and a recovered startup continue normally. The pause and retries consume the existing budgets.

Unknown CLI arguments produce a warning and are preserved in `unrecognized_arguments` and `warnings` in the report. They do not change configured safety limits.

The [output contract](OUTPUT_CONTRACT.md) defines the envelope. Source verification uses saved bytes:

```sh
uv run python scripts/verify_output.py --first out/envelopes.jsonl --organisations batch.jsonl --count 100 --state-dir state --report out/report.json
```

This verifier does not fetch the network. An independently completed official run, organiser score and at least 95% checked claim precision are required to establish qualification; local smoke tests do not establish those results.

For a check that needs only the clone, run `uv run python scripts/replay_committed_evidence.py`. The [committed evidence description](reports/evaluator-fixes/EVIDENCE.md) states which counts and original-source checks this bounded fixture reproduces and which historical measurements remain unverified.

## Latest gap verification and limits

Latest official-API check: `4ca3443`, standard 100 cohort versus the saved counts retained by `ac88ab0`. Signature covers **95 companies / 291 claims** (registered rule text: **72 / 72**); prokura **10 / 20** (registered rule text: **8 / 8**); direct group relationships **9 / 60**. Total available claims: **14,165 versus 13,799**. The 371 corporate claims are partly offset by five website claims withheld after current timeouts. Full checker exit 0, zero unsupported values/deadlines/placeholders, largest HTML **247,950 bytes**, process wall **490.16 s**, partial status, **$0**. Full pytest: **1,464 passed**. One restricted-network attempt is retained separately; no new 500 run. [Policy, qualifiers, counts and receipts](reports/r5/gaps/g1-api/SUMMARY.md).

Earlier gap check: application `f740933`, standard seed-20261017 cohort and one fresh clean-clone 500-company run with seed 20261125. Both commands used exactly seven flags and fresh state. **The 100-company full check passed. The original 500-company site gate failed; rebuilding the same saved outputs offline at `567eafe` now passes `check_live_run --count 500` (exit 0).** No new live run or clone pytest. The offline rebuild took 45.09 s; the checker took 122.66 s, separately from the original live wall time. [Gap reports and original failure receipts](reports/r5/gaps/SUMMARY.md).

| Metric | Standard 100 | Saved fresh 500 + offline site repair |
|---|---:|---:|
| Process wall / fixed budget | 558.28 / 2,100 s | 1,516.75 / 2,100 s |
| Margin under budget | 1,541.72 s | 583.25 s |
| Deadline hits | 0 | 0 |
| JSON envelopes / JSON profiles / placeholders | 100 / 100 / 0 | 500 / 500 / 0 |
| Signature/prokura: companies / claims | 0 / 0 | 0 / 0 |
| Brreg group relationships: companies / claims | 0 / 0 | 0 / 0 |
| Consolidated accounts: companies / claims | 4 / 180 | 5 / 336 |
| State aid: companies / claims | 8 / 51 | 33 / 205 |
| All available claims | 13,799 | 70,078 |
| Published HTML profiles | 100 | 500 (offline rebuild) |
| Largest HTML profile | 242,559 bytes | 249,270 bytes (offline rebuild) |
| Run status / CLI exit / full checker exit | partial / 0 / 0 | partial / 0 / 0 (offline; originally 1) |
| Source-check unsupported synthesis / briefing values | 0 / 0 | 0 / 0 |
| Activity available / failed | 100 / 0 | 500 / 0 |
| Websites / social URLs | 8 / 7 | 36 / 24 |
| Stage S claims: state aid / research / licences / inspections | 51 / 0 / 11 / 4 | 205 / 10 / 9 / 1 |
| Stage S claims total | 66 | 225 |
| State-aid data HTTP requests | 0 (dated bulk extract) | 0 (dated bulk extract) |
| HTTP attempts | 1,041 | 4,426 |
| Provider cost | $0 | $0 |

**Historical measurement limits:** signature/prokura and Brreg group-tree calls were absent from the original runs below; they are now enabled under the documented official API policy and verified separately above. The fresh 500 run recorded adaptive website pass-2 `OSError` after 61 requests; the cause and detailed loss telemetry are unavailable. The original site failed the size gate. At `567eafe`, workplace overflow moves to company-local data; the same saved 500 outputs pass the full offline check with all facts/evidence retained. Profile `968360302` is 219,666 bytes. Company-local OSError handling and diagnostics are tested; the historical pass was not rerun. Zero deadline hits and the shorter wall time do not establish complete recall or a speed improvement. Minimum sampled free disk was 17.11 GiB; the 3 GiB stop guard did not trigger.

The standard 100 cohort had 13,567 available claims at baseline `45afc2b`; the new total is 13,799. [Per-type comparison](reports/r5/gaps/standard100/SUMMARY.md). All 772 new consolidated/state-aid claims and both field-count inventories replay from the [committed bounded evidence packet](reports/r5/gaps/EVIDENCE.md), without network or local run directories. The subsequent network-blocked site rebuild and full check passed on unchanged original outputs. [Repair, integrity and checker receipts](reports/r5/gaps/site-fix/SUMMARY.md).

The earlier [final500d measurement](reports/evaluator-fixes/final500d/SUMMARY.md), using `3de9edd` and seed 20261124, remains historical evidence.
