# F2 final 500-company qualification

The authorized fresh retry passed the local qualification gates at `1722b89`. The foreground evaluator command used exactly seven flags. The clean clone installed with `uv sync --frozen` and passed 1,368 tests before the first attempt.

Seed `20261121` selected 500 distinct mod-11-valid organisation numbers with zero overlap across 2,205 excluded numbers from tracked and on-disk samples. The verified 2026-11-16 Brreg subset supplied 499 rows. Organisation `935674743` used live lookup.

| Metric | Retry |
|---|---:|
| End-to-end CLI wall time | 1,871.92 s |
| Margin under the fixed 2,100 s budget | 228.08 s |
| Terminal envelopes | 500 |
| Output placeholders | 0 |
| Companies with any deadline hit | 172 |
| Website pass 2 cutoff | 171 |
| Websites | 41 |
| Social URLs on company-owned evidence | 28 across 16 companies |
| Registry-declared social URLs | 0 |
| HTTP attempts | 5,243 / 9,250 |
| Largest profile HTML | 249,012 B |
| Provider cost | $0 |

## Section coverage and deadlines

Available counts are companies with an available section. Other source states are preserved in the saved summary.

| Section | Available | Deadline |
|---|---:|---:|
| accounts | 500 | 0 |
| activity | 306 | 0 |
| gleif | 56 | 0 |
| hiring | 2 | 0 |
| identity | 500 | 0 |
| inspections | 7 | 0 |
| licences | 10 | 0 |
| procurement | 0 | 0 |
| research | 5 | 0 |
| roles | 499 | 0 |
| state_aid | 42 | 0 |
| subunits | 388 | 0 |
| website | 41 | 172 |

Exact-ID families by reported section state and published claim count.

| Section | States | Claims |
|---|---|---:|
| gleif | available 56, not_available 444 | 64 |
| procurement | blocked 6, not_available 494 | 0 |
| state_aid | available 42, not_available 458 | 313 |
| research | available 5, not_available 495 | 13 |
| licences | available 10, not_available 490 | 31 |
| inspections | available 7, not_available 493 | 7 |

## URL review

The inventory lists all 69 published website and social URLs with saved evidence excerpts. The legacy ledger returned 7 wrong labels that the current validators resolve and 0 unresolved wrong verdicts. It flagged 17 URLs for review. 0 published sites came from the seed index, with zero indexed organisations in the frozen sample.

## First attempt retained

The first run took 604.64 s and passed the structural verification. A run-wide OSError loading the frozen Brreg snapshot caused full live fallback, so it failed the frozen-input gate. The offline preflight then successfully wrote all 499 snapshot receipts. The single fresh retry used the same frozen inputs, the same clean commit and a new state directory. The first attempt contributes no measurements to the retry.

The first attempt receipts are in this directory. The selected retry receipts are in `trials/retry/`. The complete URL inventory is in `urls.md`.
