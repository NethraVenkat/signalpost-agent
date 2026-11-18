# W3 seed index recall hand-check

## Paired measurement

Both variants used the same frozen 100-company input and registry subset, fresh state, and exactly seven evaluator CLI flags. The default-on run was compared with `SIGNALPOST_WEBSITE_SEEDS=0`; this config override changes only whether the bundled website seed index is loaded.

- Cohort: `86ad22303145a2efca1980dcc63678cb3192afcbd4dc9e3959e633a1ed02b79a` (100 organizations; CC 54, OSM 46).
- Frozen registry subset: `9613083ec10d124ff6f0a009ec210e2a26ca7a9a4ec0ef4890653e11146e2331` (2026-11-16 snapshot; 100/100 rows).
- Seeds on: 1786.5s; 0 published websites; checker HTTP count 1169; verifier site build True.
- Seeds off: 1786.8s; 0 published websites; checker HTTP count 994; verifier site build True.
- Websites published only by the seeds-on run: 0; seed-index-attributed additions: 0.

Both runs used about 1,785 seconds, reached website verification, and completed output/site publishing. Neither published a website (on section states: `{'failed': 97, 'not_available': 3}`; off: `{'failed': 72, 'not_available': 28}`). Website diagnostics were on `{'website_source_unavailable': 97, 'website_candidates': 100, 'website_budget_exhausted': 6, 'dns_budget_exhausted': 12}` and off `{'website_source_unavailable': 72, 'website_candidates': 100, 'website_budget_exhausted': 3, 'dns_budget_exhausted': 3}`. The checker verified 100 terminal envelopes and 100 complete briefings in each run, 102 source blobs for seeds on and 102 for seeds off, and the offline site in each. Observed extra published websites: zero. Because the website stage had many `website_source_unavailable` / budget failures and published no claims in either run, this comparison is inconclusive about seed-index recall and supplies no seed-only pages for hand-check; it does not establish that the index has no useful candidates.

## Seed-only websites for human hand-check

Automated-doubtful entries are listed first.

No seed-only website was published by either run, so there are no website claims to hand-check from this cohort.
## Disposition

The paired runs are complete and their claims are pinned in `seed_recall_summary.json`. No seed-only site was published, so there is no URL for the reviewer to hand-check from this cohort. The observed zero is inconclusive because the website section had widespread source/budget failures. The full pytest suite passed (1,393 tests; see `seed_recall_pytest.txt`). No 500-company run was started.
