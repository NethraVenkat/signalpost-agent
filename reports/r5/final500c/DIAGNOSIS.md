# A1: saved final500b activity diagnosis

- Source: saved `report.json` and envelopes only; no new acquisition.
- Activity failed: 220/500; codes: `website_check_incomplete` 210, `website_budget_exhausted` 9, `website_connect_error` 1.
- All 500 official registry timelines were available with no registry activity errors.
- Roles: 381 available, 119 no matching item; no failures. Stage S did not cause these activity errors.
- All 71 registry/role update requests returned HTTP 200, at approximately 1,243–1,282 seconds into the crawl.
- Failed envelopes were finalized from 1,550 seconds; individual activity-error timestamps are not stored.
- Website work had 202 deadline-hit companies; incomplete website discovery propagated into the combined activity status.
- Cause: a code bug in status merging, not registry deadline, 429, 5xx or timeout failure.
- The separate website-budget and connection diagnostics remain explicit; supported registry evidence must stay available.
