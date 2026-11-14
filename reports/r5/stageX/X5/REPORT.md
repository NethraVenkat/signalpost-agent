# X5 attempted stage - reverted

No X5 runtime feature is committed. Runtime has been restored to the tested X4 implementation. The attempted implementation and test snapshots are preserved in trials/reverted_stage. The inherited approximately90-minute stage rule applies: repeated interrupted runs and a hard-time/site validation failure prevented a correct measured completion. Earlier green1,074 tests describe the reverted attempted implementation, not completed six-sample acceptance.

## Source capability observations

The already-saved GLEIF records provide explicit initialRegistrationDate; their lastUpdateDate is not proof of renewal, and nextRenewalDate is a scheduled date. No explicit lastRenewalDate appeared in the saved audit. Accounts period ends and year lists do not provide a filing-availability timestamp. No fabricated filing or renewal date is retained in runtime.

## Failure evidence

First incomplete seed20261114 and later seed20261115 attempts had no final report or captured exit code when inspected; causes and final request/runtime totals remain unknown. Fresh runs/newIDs were attempted while preserving their state. The detached seed20261115 attempt subsequently completed terminal envelopes but failed independent validation because elapsed wall time exceeded35minutes and site generation was skipped. The saved report states 5122.563 completion seconds and 466 requests; its site state is skipped. No measurement is promoted to success based on exit0 alone. The separate CLI log may show different pre-final report figures; preserve both receipts without fabricating agreement.

Only seeds20261017,20261113 and a source-recovery20261114 have completed verified partial measurements. They are diagnostic receipts, not a complete six-sample X5 table. R6/R7/X2 are not started or claimed implemented. $0 provider cost; never pushed.

Restored checkpoint full pytest: **1,067 passed in 183.47s (restored X4 runtime)**. Runtime source is restored; the reports-only checkpoint does not claim X5 completion.
