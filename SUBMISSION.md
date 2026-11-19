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
