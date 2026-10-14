# Cold 100 event-loop diagnostics

All three diagnostics use seed20261017, fresh empty state directories, the full185-day feed method and a2,400-second run budget. No warm page cache is reused. The declared index is intentionally bypassed for method comparison. Pending W3 source-field additions are excluded. The strict saved-source300 equivalence gate passed before these changes: exact claims/provenance/synthesis,606byte-identical site files,0company changes.

| Implementation | Pages | Cold feed seconds | Decoded MB | Seconds/page | Mean response→next-send gap | Gap p95 | Loop-lag p95 |
|---|---:|---:|---:|---:|---:|---:|---:|
| loop-cold100 | 378 | 319.984 | 185.374745 | 0.846519 | 194.483 ms | 297.000 ms | 134.000 ms |
| loop-cold100-bounded | 378 | 319.532 | 185.374745 | 0.845323 | 166.191 ms | 266.000 ms | 103.000 ms |
| loop-cold100-process | 378 | 380.000 | 185.378265 | 1.005291 | 91.204 ms | 235.000 ms | 72.000 ms |

The final diagnostic meets the **mean** gap target below200ms and the loop-lag p95 target below100ms. Gap p95 remains235ms; there is no claim that every individual gap is below200ms. Its full measured feed/runtime includes a76.141-second timed-out attempt and retry, and maximum heartbeat lag75.493seconds. Windows Kernel-Power506/507 messages record entering/exiting Modern Standby at10:38:54.268–10:40:17.585 Asia/Kolkata, spanning this stall. No sleep time or request timeout is removed from runtime, feed seconds, seconds/page or maximum lag.

The original trace had a measurement bug: after the timeout, the retry was measured from the preceding successful response again, incorrectly counting in-flight request time as idle. The table recomputes the requested response-completion→next-send interval directly from preserved timestamps. The retry's separate390ms post-error dispatch gap remains recorded. New instrumentation consumes each response marker at the next send and records a new marker on failed-attempt completion; a regression test preserves the timeout duration while checking the retry gap.

CPU extraction, HTML parsing, synthesis, hashing and output generation run in bounded workers. Pure NAV header scoring runs in one CPU process, with a test proving unchanged native scores. NAV parsing/storage have a separate two-thread pool; company work has four threads. The name-discovery rules and source/request/time budgets are unchanged by scheduling work. Index discovery remains a separate W2b feature.

Temporary Windows idle-sleep prevention is now requested for active batches and the previous thread state restored afterward. It makes no persistent power or display changes and can be disabled with `--allow-system-sleep`. Native API verification returned requested/restored true. Explicit user sleep and power-policy overrides remain possible. See [source and execution notes](../docs/SOURCES.md).

All100envelopes were written in each diagnostic, with0batch-level handled/unhandled exceptions or deadline hits. The final HTTP log includes the timeout/retry above; the batch exception counters do not mean every HTTP attempt succeeded. All sites generated successfully; the final batch reported401.547seconds. A short mocked-index regression suite ran briefly alongside the process diagnostic, so these are shared-machine measurements rather than isolation guarantees. Historical failed/missed diagnostic reports are preserved.
