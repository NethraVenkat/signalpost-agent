# F2 qualification after HC1

One fresh run at `e185130` completed in **1,978.15 seconds**, with **121.85 seconds** under the fixed 2,100-second budget. It emitted all 500 required envelopes and profiles with zero placeholders. `check_live_run --count 500` failed because an oversized profile prevented the optional site from generating in the measured run. The required outputs passed the independent saved-output verifier. The site was fixed and rebuilt from the same envelopes offline. [Measured run](run.json) · [Original checker result](check_live_run.txt) · [Required-output verification](required_outputs.json)

The clean clone installed with `uv sync --frozen` and passed 1,379 tests, including the F1 guard. The foreground evaluator used exactly the seven prescribed flags. Seed `20261121` selected 500 distinct organisations with zero overlap against 4,206 organisation numbers excluded from committed and on-disk samples, including the previous F2 cohort. The frozen 2026-11-16 Brreg subset provided 496 rows. Live lookups returned HTTP 200 for `923013636`, `926046101`, `933539911` and `939747117`. [Clone and inputs](clean_clone.json) · [Frozen-row preflight](bulk-preflight.txt)

| Metric | Measured run |
|---|---:|
| End-to-end CLI wall time | 1,978.15 s |
| Margin under the fixed 2,100 s budget | 121.85 s |
| Terminal envelopes / profiles | 500 / 500 |
| Output placeholders | 0 |
| Companies with a deadline hit | 173 |
| Website pass 2 cutoff | 173 |
| Published claims | 67,942 |
| Websites | 38 |
| Company-owned social URLs | 15 across 8 companies |
| Registry-declared social URLs | 0 |
| HTTP attempts | 5,115 / 9,250 |
| Provider cost | $0 |

The saved-output verifier rechecked 2,134 source blobs and found all five cited briefing topics for every company, with zero unsupported synthesis or briefing values. One company's accounts source returned HTTP 500 on all three attempts. All four run-level source-health probes were reachable. [Measured report](report.json)

## Section coverage and deadlines

| Section | Companies with available data | Companies with a deadline |
|---|---:|---:|
| Accounts | 499 | 0 |
| Activity | 302 | 0 |
| GLEIF | 76 | 0 |
| Hiring | 5 | 0 |
| Identity | 500 | 0 |
| Inspections | 5 | 0 |
| Licences | 12 | 0 |
| TED procurement | 0 | 0 |
| Research | 6 | 0 |
| Roles | 495 | 0 |
| State aid | 46 | 0 |
| Subunits | 355 | 0 |
| Website | 38 | 173 |

| Exact-ID source | Section states | Published claims |
|---|---|---:|
| GLEIF | 76 available, 424 not available | 80 |
| TED procurement | 3 robots-blocked, 497 not available | 0 |
| State aid | 46 available, 454 not available | 305 |
| Research | 6 available, 494 not available | 15 |
| Licences | 12 available, 488 not available | 25 |
| Inspections | 5 available, 495 not available | 29 |

## Optional site replay

Organisation `817066542` exceeded the size gate at 286,550 bytes after the original trims. The follow-up in `a796b44` defers duplicate source links to their evidence panels when those trims leave a page above the cap. The same page rendered at 241,286 bytes offline. The replay took 53.13 seconds, verified all 500 profiles and their evidence files, and measured a largest profile of **249,406 bytes**. The original report and its failed site check are preserved. The replay used the same saved envelopes and made no evaluator requests. [Offline site replay](site_replay.json)

## URL review

The inventory lists all 53 website and social URLs with hash-verified receipts. The legacy ledger flagged 15 URLs as doubtful. Its two wrong labels came from the older contact-page rule, and both passed the current saved-proof verifier. Zero wrong labels remain unresolved in that verifier comparison. No published website came from a seed-index candidate. [Full URL inventory](urls.md)

The first checkout preparation ran out of disk space before evaluation. The successful checkout followed lossless compression of earlier local archives. The one foreground measurement used a fresh state directory. [Checkout preparation receipt](checkout-failed.json)
