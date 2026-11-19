# Final500d: single fresh 500-company scale check

Measured the runtime at `3de9edd7fe6fa9ddebc50bf11b8fdfe8dae9f105` on 19 November 2026, after the website-window and robots-retry fixes. One 500-company run only; no automatic retry. The clean shallow clone used `uv sync --frozen` and an import check, with **no pytest in the clone**. Seed **20261124** sampled 500 valid, unique identifiers disjoint from **5,706** prior sampled numbers found in committed and local cohorts. The sample and 497-row bulk subset are saved here; the three selected identifiers absent from the newer bulk snapshot stayed in the sample and were resolved by the normal live lookup. All 500 identity sections were available.

| Metric | Final500d |
|---|---:|
| Process wall time / fixed budget | 1,840.81 / 2,100 seconds |
| Margin under budget | 259.19 seconds |
| Deadline hits (website pass 2) | 215 |
| Activity available / failed | 500 / 0 |
| Websites / social URLs | 30 / 9 |
| Terminal envelopes / profiles / placeholders | 500 / 500 / 0 |
| Largest HTML profile | 240,192 bytes |
| Run status / CLI exit / checker exit | partial / 0 / 0 |
| Available claims | 68,586 |
| State-aid claims / data requests | 0 / 0 |
| Stage S claims: research / licences / inspections | 4 / 16 / 12 |
| Stage S claims total (including state aid) | 32 |
| Unsupported synthesis / briefing values | 0 / 0 |
| HTTP attempts | 4,517 |
| Provider cost | $0 |
| Minimum sampled free disk | 23.36 GiB |

The process wall time includes launch and report-flush overhead; the application's completion receipt reports **1,833.879 seconds**. `check_live_run --count 500` passed, including 2,056 saved source blobs and 500 complete cited briefing contracts. A passing output check permits honest source failures; it does not establish complete source coverage, zero recall loss, an official score or claim precision on an independently judged population.

## Website deadline losses

The 215 hits are retained explicitly, not counted as resolved. Pass 2 began at **1,374.168 seconds** and stopped at **1,700.061 seconds**, against its **1,700-second** cutoff. It made **105** website requests and gained **zero** websites in pass 2. States were 260 no-pending-candidates, 215 deadline, eight checked-no-gain and 17 already-verified. The total published website count is 30, including the other accepted proof tiers. [Company-level deadline receipt](deadline_losses.json) lists every affected identifier and its pending work. This scale result shows that the time-window correction did **not eliminate deadline losses at 500 companies**. No further runtime change or rerun was made.

## State aid and Stage S

St?tteregisteret robots failed with `ReadError` three times. Requests began at 20.958, 27.620 and 49.364 seconds, with 5/20-second backoff. The origin then remained blocked: **zero state-aid data requests, zero state-aid claims, 500 blocked state-aid sections**. This network-enabled scale check does not confirm resumed state-aid access. [Exact request receipt](state_aid_requests.json); [small-check and test result](../robots-retry/SUMMARY.md). No persistent robots failure was bypassed.

Stage S produced 32 available claims: research 4, licences 16, inspections 12, state aid 0. They appeared in three research, seven licence and eight inspection sections. Other failures include one accounts section and six procurement sections; see the complete section counts in [summary.json](summary.json).

## Setup, command and retained evidence

Disk preflight required at least 15 GiB; the measured initial free space was **25.05 GiB**. The network-enabled preflight reached identity (200), accounts (404, reachable) and NAV (200). The preliminary sandbox preflight failed before cloning or crawling and is retained separately. The guard sampled every two seconds and would stop the process tree below 3 GiB; it never triggered.

The installed clone ran the equivalent of this command with exactly seven flags, independent fresh state and the default budgets:

```sh
python -m signalpost.cli run --organisations companies500.jsonl --bulk registry500.csv --output envelopes.jsonl --profiles-output profiles.jsonl --report report.json --run-id evaluator-fixes-final500d-seed20261124 --expected-count 500
```

No paid provider was enabled. [Clean-clone/sample hashes](clean_clone.json), [execution](run.json), [checker invocation](check_live_run.json), [checker result](check_live_run.txt), [disk guard](disk_guard.json), [network preflight](network_preflight.json) and the [measurement driver](measure.py) are saved here. Full outputs and original source bytes remain locally under `.data/evaluator-fixes-final500d/run/`; their hashes are in summary.json. These full 500-company source bodies are not bundled in the repository and this run is separate from the bounded historical clone-only replay fixture. Nothing was pushed.
