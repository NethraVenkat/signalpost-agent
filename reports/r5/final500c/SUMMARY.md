# Final500c: successful authorized rerun

Historical measurement before the evaluator fixes. The original `2ac8a6b` label maps to the surviving pre-fix code reference described in [HISTORY_MAPPING.md](../../../HISTORY_MAPPING.md). This is not a measurement of the revised agent; original full source bodies remain outside the clone.

One fresh 500-company rerun used a clean shallow clone of `2ac8a6b0efa1a80c8afdd37323253e786a85e6ff`, exactly seven
evaluator flags, seed 20261123 and the identical frozen, disjoint sample from the
disk-full attempt. State was fresh. Clone setup ran only `uv sync --frozen` and an
import check; no clone pytest. The 1,396 passing main-checkout tests were carried forward.

| Metric | Final500c |
|---|---:|
| Wall time / fixed budget | 1875.24 / 2,100 seconds |
| Margin | 224.76 seconds |
| Activity available / failed | 500 / 0 |
| Websites / social URLs | 29 / 5 |
| Terminal envelopes / profiles / placeholders | 500 / 500 / 0 |
| Largest HTML profile | 248,788 bytes |
| Unsupported synthesis / briefing | 0 / 0 |
| HTTP requests | 5,201 |
| Provider cost | $0 |
| Minimum sampled free space | 20.08 GiB |

`check_live_run --count 500` passed. The guard sampled disk free space every two
seconds and would request SIGINT/asyncio cleanup below 3 GiB; it did not trigger.
The 2,100-second default, 1,700-second pass-2 cutoff, finalisation reserve,
exact-ID identity rules and evidence requirements were unchanged.
Final main-checkout privacy guard: **5 passed** with workspace-local basetemp.
Full outputs and source blobs remain in `.data/r5/final500c-rerun-clean/run-final`.

## Retained earlier attempts

The original disk-full 500 attempt aborted at approximately 1,374.39 seconds,
before publishing terminal outputs. Its receipts are preserved under
[`trials/disk-full/`](trials/disk-full/SUMMARY.md); all original run state and
source blobs remain under `.data/r5/final500c-clean/run-final`.
Its retained state is only 70.08 MB. No historical per-directory disk series
exists; prior pytest-temp cleanup recovered about 10.3 GB. Deleted clone sizes
cannot now be reconstructed. See `disk_preflight.json` and `disk_guard.json`.

The earlier network-enabled standard 100 check remains 100 activity available /
0 failed, 8 websites, 351.63 seconds, zero unsupported values and $0. Its earlier
sandbox-blocked attempt and the environment-required network retry remain recorded.

[Activity diagnosis](DIAGNOSIS.md) · [URL inventory](urls.md) · [Gates and hashes](summary.json).
Repository-local author and committer: Nethra Venkat. Nothing was pushed.
