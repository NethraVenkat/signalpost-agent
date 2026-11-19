# Final 500-company qualification

The clean clone of `b341b8019acfcd20cb6f66c170661c99388b472b` passed `check_live_run --count 500`. Seed 20261122 selected 500 unique valid organization numbers after excluding 4,706 numbers found in committed and on-disk sample files, including the earlier 500-company cohorts. Overlap was zero. The hash-checked 2026-11-16 snapshot supplied 499 rows. The remaining organization, 932891468, used live identity lookup. All 500 identity sections are available.

The run used fresh state, exactly seven evaluator flags and the fixed 2,100-second default, with seeds disabled by default. One attempt completed. The full test suite ran concurrently in the clone and passed 1,393 tests in 946.86 seconds using workspace-local basetemp.

| Metric | Final 500 |
|---|---:|
| Ordered terminal envelopes / profiles | 500 / 500 |
| Wall time | 1649.67 s |
| Margin under 2,100 seconds | 450.33 s |
| Placeholders | 0 |
| Websites / social URLs | 33 / 5 |
| HTTP requests | 5,158 / 9,250 |
| Largest HTML profile | 245,912 bytes |
| Unsupported synthesis / briefing values | 0 / 0 |
| Provider cost | $0 |

## Source coverage and deadlines

| Source section | Available | No matching item | Blocked | Failed | Deadline companies |
|---|---:|---:|---:|---:|---:|
| accounts | 499 | 0 | 0 | 1 | 0 |
| activity | 280 | 0 | 0 | 220 | 0 |
| gleif | 58 | 442 | 0 | 0 | 0 |
| hiring | 3 | 496 | 0 | 1 | 0 |
| identity | 500 | 0 | 0 | 0 | 0 |
| inspections | 8 | 492 | 0 | 0 | 0 |
| licences | 3 | 497 | 0 | 0 | 0 |
| procurement | 0 | 493 | 7 | 0 | 0 |
| research | 7 | 493 | 0 | 0 | 0 |
| roles | 499 | 1 | 0 | 0 | 0 |
| state_aid | 42 | 458 | 0 | 0 | 0 |
| subunits | 374 | 126 | 0 | 0 | 0 |
| website | 33 | 257 | 2 | 169 | 202 |

All 202 deadline hits occurred in website work. There were no deadline hits in GLEIF, TED procurement, or any Stage S section. TED's seven blocked companies retain their explicit access state. The 39 ambiguous and two blocked website sections are additional to the available, no-match and failed counts shown above. GLEIF published 64 claims for 58 companies. Stage S published 296 state-aid claims, seven research claims, three licence claims and 20 inspection claims.

The checker verified 68,530 available claims, 2,112 source blobs, 500 complete briefing contracts and the generated offline site. Unsupported synthesis and briefing values were zero. Startup Brreg, accounts, NAV and GLEIF health checks were reachable. The report preserves three unrecovered individual transient attempts. Explicit source failures remain visible in the coverage table.

## Website and social audit

All 38 URLs are in [urls.md](urls.md), with the 18 automated-doubtful items first, followed by 20 rated correct. These are older ledger-tool labels, separate from the current saved-proof validator, which passed every published claim. No new human verdict is inferred. The full inventory retains proof tiers, exact excerpts, retrieval timestamps and content hashes.

## Reproduction and evidence

The exact invocation is in `run.json`, sample exclusion manifest and clone identity in `clean_clone.json`, and all artifact hashes and gates in `summary.json`. Run outputs and source blobs remain under the local `.data/r5/final500b-clean/run-final` directory. No evidence was deleted. Paths in committed receipts use portable markers. Repository-local author and committer are Nethra Venkat. Nothing was pushed.
