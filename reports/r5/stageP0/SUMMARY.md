# Stage P0 ? official-source outage resilience

Measured runtime: parent `521f9cf77a943ca87a5f471f526d81df4dc8c259` plus the P0 source/verification manifests saved here. Fresh state; exact seven evaluator flags; seed 20261017. No paid models/search, cost $0.

| Metric | X2 frozen 100 | P0 frozen 100 |
|---|---:|---:|
| Verified websites | 6 | 6 |
| Declared-homepage recall | 4/11 | 4/11 |
| Social claims / companies | 10 / 4 | 10 / 4 |
| Activity claims | 1,392 | 1,392 |
| Published facts | 13,551 | 13,551 |
| HTTP requests | 924 | 928 |
| Full-process seconds | 547.484 | 543.313 |
| Unsupported briefing/synthesis values | 0 | 0 |

100 ordered terminal envelopes, exit 0, all five briefing topics, generated site; largest profile HTML 239,535 bytes, below 250,000. No added or removed website/social items. All four reachability probes succeeded (accounts HEAD 404 indicates reachability, not available company data). Three accounts HTTP 500 responses for BIEN SPAREBANK 991853995 remained explicit failures after two bounded retries; no false recovery or fabricated values. Health probes and retries count in the unchanged hard budgets. No rerun was needed: this persistent source failure was already present in the comparison coverage, which remains identical.

The new policy retries transient DNS/connect/timeout/protocol/5xx at most twice, using 5/20-second waits clipped by the original deadline and global request ceiling. Bounded startup HEAD checks may defer a genuinely unavailable official source; they never provide fact evidence. Authentication, robots, schema, exact-ID and unsupported-value rules remain strict. Reports expose source health and each transient attempt. Stale website proof can retain its original, hashed registry dependencies only when explicitly carried forward; a fresh proof cannot borrow stale identity.

Full pytest: **1,283 passed in 600.85 seconds**, process 601.688 seconds. Earlier integration failures and fixes are retained under `trials/`; source files were unchanged between this green gate and measurement. Tests cover DNS/connect retries, backoff/deadline/global limits, health outages, explicit NAV states, partial identity and refresh/carried evidence. Original immutable source blobs remain necessary to verify carried proof.

Exact evaluator command (from settings.json):

```text
C:\Users\<USER>\signal-nethra\.venv\Scripts\python.exe -m signalpost.cli run --organisations C:\Users\<USER>\signal-nethra\reports\r5\baseline\companies.jsonl --bulk C:\Users\<USER>\signal-nethra\reports\r5\baseline\registry100.csv --output C:\Users\<USER>\signal-nethra\.data\r5\stageP0-20261017-final\envelopes.jsonl --profiles-output C:\Users\<USER>\signal-nethra\.data\r5\stageP0-20261017-final\profiles.jsonl --report C:\Users\<USER>\signal-nethra\.data\r5\stageP0-20261017-final\report.json --run-id r5-stageP0-seed20261017-final --expected-count 100
```

Evidence: `verification.json`, `counts.json`, `report.json`, source/verification manifests, execution logs and pytest receipts. Original response bodies and ordered envelopes remain at the working directory recorded in `settings.json`. APIs/licences remain those documented in docs/SOURCES.md; no external code/data, paid API, publication or git push. Human hand-check: no new identity item; inspect the explicit persistent BIEN accounts 500 and outage summary if desired.
