# Final500c: qualification failed

A2 and B are committed in `7b2b476732161cf1b1ee9454f3fa948f532fc256`. Full pytest: **1,396 passed**.
Activity merging now retains available registry facts and explicit website errors.
Website pass 2 stops at 1,700 seconds for 500 companies; the 2,100-second default,
250-second finalisation allowance, global deadline and evidence rules are unchanged.
[Saved final500b diagnosis](DIAGNOSIS.md).

| Metric | Network-enabled standard 100 | Single fresh 500c attempt |
|---|---:|---:|
| Seed | 20261017 | 20261123 |
| Wall seconds | 351.63 | approximately 1374.39, aborted |
| Margin / unused budget seconds | 1748.37 | approximately 725.61 unused at abort; no qualification margin |
| Activity available / failed | 100 / 0 | unavailable |
| Websites | 8 | unavailable |
| Social URLs | — | unavailable |
| Unsupported synthesis / briefing | 0 / 0 | unavailable |
| Placeholders | 0 | unavailable |
| Largest profile bytes | 242,988 | unavailable |
| Provider cost | $0 | $0 provider-disabled mode; metering report unavailable |

The C: drive reached zero free bytes during the 500 run. The CLI exited 1 before
publishing report, envelopes or profiles; its temporary envelopes file is empty.
The driver also could not save its stopwatch receipt. The approximate 500 wall
time above uses the run-log creation and final-write timestamps, not a completed report.
`check_live_run --count 500` was executed against the saved attempt and failed because
the terminal output is absent. No 500-company coverage or zero-unsupported result is claimed.
The clean clone, disjoint sample receipt, 3,636 saved source-blob files,
state and logs remain under `.data/r5/final500c-clean/`. No live evidence was deleted.
Only this task's temporary pytest directories were removed to free disk space.
No second 500 attempt was started.

An earlier sandbox-blocked 100-company attempt is retained under `smoke100/`:
0 activity available, 100 failed, 0 websites, 1786.17 seconds.
Environment instructions required a network-enabled retry outside the sandbox;
the successful result is under `smoke100-network/`. This explicitly exceeds the
requested one-attempt limit for 100; both attempts are retained.

Repository-local author/committer: Nethra Venkat. Nothing was pushed.
