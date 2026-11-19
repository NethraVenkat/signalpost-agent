# Signalpost: evaluator instructions

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

Latest gap check: application `f740933`, standard seed-20261017 cohort and one fresh clean-clone 500-company run with seed 20261125. Both commands used exactly seven flags and fresh state. **The 100-company full check passed; the 500-company full check failed because no HTML site was published.** No live rerun or clone pytest. [Gap reports and original failure receipts](reports/r5/gaps/SUMMARY.md).

| Metric | Standard 100 | Fresh 500 |
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
| Published HTML profiles | 100 | 0 |
| Largest HTML profile | 242,559 bytes | 262,692 bytes, offline reconstruction; not published |
| Run status / CLI exit / full checker exit | partial / 0 / 0 | partial / 0 / 1 |
| Source-check unsupported synthesis / briefing values | 0 / 0 | 0 / 0 |
| Activity available / failed | 100 / 0 | 500 / 0 |
| Websites / social URLs | 8 / 7 | 36 / 24 |
| Stage S claims: state aid / research / licences / inspections | 51 / 0 / 11 / 4 | 205 / 10 / 9 / 1 |
| Stage S claims total | 66 | 225 |
| State-aid data HTTP requests | 0 (dated bulk extract) | 0 (dated bulk extract) |
| HTTP attempts | 1,041 | 4,426 |
| Provider cost | $0 | $0 |

**Remaining limits:** signature/prokura and Brreg group-tree API enablement remain pending the canonical robots access gate. The fresh 500 run recorded adaptive website pass-2 `OSError` after 61 requests; the cause and detailed loss telemetry are unavailable. One reconstructed profile (`968360302`) still exceeded the 250,000-byte gate after all existing fallbacks, so the site was not published and `check_live_run --count 500` failed. Zero deadline hits and the shorter wall time do not establish complete recall or a speed improvement. Minimum sampled free disk was 17.11 GiB; the 3 GiB stop guard did not trigger.

The standard 100 cohort had 13,567 available claims at baseline `45afc2b`; the new total is 13,799. [Per-type comparison](reports/r5/gaps/standard100/SUMMARY.md). All 772 new consolidated/state-aid claims and both field-count inventories replay from the [committed bounded evidence packet](reports/r5/gaps/EVIDENCE.md), without network or local run directories. The separate saved-source check passed; it does not make the failed 500-company site gate pass.

The earlier [final500d measurement](reports/evaluator-fixes/final500d/SUMMARY.md), using `3de9edd` and seed 20261124, remains historical evidence.
