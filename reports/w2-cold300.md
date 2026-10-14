# W2 cold 300 baseline — target missed

Seed 20261015, 300 ordered companies, 2,400-second run budget. New empty state directory `state/w2-cold300-stream`; no copied ETags, pages or blobs. This is the single completed cold baseline before W2b. An earlier stopped attempt is excluded.

| Measurement | Actual |
|---|---:|
| Feed pages completed | 129 |
| Feed complete | **false** |
| Cold feed seconds | 900.438 |
| Decoded feed body MB (decimal) | 63.552430 |
| Feed seconds/page | 6.980140 |
| Completed detail fetches / HTTP attempts | 22 / 22 |
| First detail start | 20.875 seconds, page 1 |
| NAV elapsed / configured cap | 902.750 / 900 seconds |
| Hiring failed | **300/300 (100%)** |
| Batch reported seconds | 938.234 |
| Handled / unhandled exceptions / deadline hits | 0 / 0 / 0 |

The failure cause is the NAV time cap with an incomplete forward scan of the full 185-day feed. No company is reported `not_available`. Partial-scan bookkeeping records 24 unusable-name scopes and 276 other unchecked scopes; those are not a final complete-feed distribution. The observed detail cap was 22 discovered candidates, within the unchanged default maximum of 600 attempts for this batch; three candidate versions remained unchecked. This does not establish that raising the detail cap would solve the baseline.

The website completion-spacing rule does not apply to NAV. Completed feed HTTP events total approximately 257.543 seconds (254.734 seconds response-read timing; 1.340 seconds blob storage); approximately 640.145 seconds accrued between feed requests in application scheduling/header processing. These timings overlap and must not be summed as independent phases. Thus the earlier 530-second full-body read is not a reliable prediction of this streaming name-based baseline. The machine also ran unit checks during the early part of this baseline; this is a diagnostic baseline, not an isolated official performance guarantee. Per instruction, no further name-path tuning follows: W2b replaces it as the primary discovery method.

No documented field projection was found in the official NAV docs/controller. Default page size remains 1,000; projection savings are **0 MB**. MB above measures decoded HTTP bodies, not compressed wire bytes. Earlier accepted NAV timings are marked warm-cache in README, EVAL, SOURCES and the historical smoke report.

The 900-second default is provisional pending a cold 1,000-company completion within 1,200 seconds (50% headroom against 2,400 seconds); otherwise restore 600 seconds and retain the open risk. The full-feed baseline is **not accepted as a passing W2 capability gate**. Exact live verification in W2b remains required.

Reproduction:

```sh
uv run signalpost run --organisations state/downloads/overnight300-new.jsonl --bulk state/downloads/overnight300-new.csv --output out/w2-cold300-stream-envelopes.jsonl --profiles-output out/w2-cold300-stream-profiles.jsonl --report dev-notes/w2-cold300-stream-report.json --site-dir dev-notes/site-w2-cold300-stream --state-dir state/w2-cold300-stream --websites --hiring --public-activity --expected-count 300 --time-budget-seconds 2400
```

Use a different nonexistent state path for any fresh reproduction. Source artifacts and the detailed machine report remain local. Independent verification passed all 300 envelopes, 22,146 available claims, 1,143 source bodies and 2,424 cited synthesis sentences, with zero unverified values. The run recorded a site-generation `AttributeError` caused by a new scalar registry-role metadata claim being treated as a role record. After correcting that interpretation offline, site replay hit the unchanged 250 KB profile-page gate; this remains a W3 size risk. The original report is preserved; no second live baseline was run.
