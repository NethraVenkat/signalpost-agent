# Corrected same-sample precision audit

Source application `4ca3443`; frozen seed **2026112601**, the same 200 claim IDs/values and population draw. No resampling or source replacement. The original `sample.jsonl`, `population.json.gz`, `proof.json.gz` and their manifest hashes are unchanged.

**200 correct / 0 incorrect / 0 unverifiable** under claim-specific saved-source replay. Nominal Wilson 95% lower bound: **98.12%**. This is a descriptive bound for the selected, disproportionately stratified sample; it is not a design-adjusted population guarantee or an independent human accuracy estimate.

## Correction

The previous audit treated supporting identity receipts as candidate value evidence and applied a whole-value literal-leaf test to formatted/structured projections. Its human list could choose the first Brreg CSV dependency as the displayed source. That result and its aggregate bound are withdrawn, not evidence of low factual precision. Historical artifacts remain in `trials/withdrawn-audit/`; README/SUBMISSION no longer publish the withdrawn number.

Primary receipts now resolve by each claim's own evidence IDs, field, extraction method and locator: website identity-proof page, social company-link/owner declaration, publisher public-name receipt, own description/contact span, or the exact official record. Auxiliary Brreg legal-name/address receipts remain dependencies; they cannot supply website/social/brand values. Original body SHA-256, verbatim span and primary URL/hash retrieval binding are checked. Production source validators shared with `check_live_run` re-derive values and exact owner identity. Structured metadata and normalized numbers/phones are re-derived rather than searched literally in an unrelated CSV or required to appear as a serialized object in a short excerpt. The per-item results retain the resolved primary URL, hash, span and locator.

| Type | Sample | Correct | Incorrect | Unverifiable | Wilson 95% lower |
|---|---:|---:|---:|---:|---:|
| brand | 9 | 9 | 0 | 0 | 70.09% |
| consolidated_accounts | 7 | 7 | 0 | 0 | 64.57% |
| entity_accounts | 42 | 42 | 0 | 0 | 91.62% |
| filing_years | 16 | 16 | 0 | 0 | 80.64% |
| group_parent | 1 | 1 | 0 | 0 | 20.65% |
| group_subsidiary | 4 | 4 | 0 | 0 | 51.01% |
| identity | 29 | 29 | 0 | 0 | 88.30% |
| inspections | 1 | 1 | 0 | 0 | 20.65% |
| lei | 2 | 2 | 0 | 0 | 34.24% |
| licences | 1 | 1 | 0 | 0 | 20.65% |
| locations_subunits | 15 | 15 | 0 | 0 | 79.61% |
| people_roles | 19 | 19 | 0 | 0 | 83.18% |
| prokura_combination | 1 | 1 | 0 | 0 | 20.65% |
| prokura_rule | 1 | 1 | 0 | 0 | 20.65% |
| public_activity | 20 | 20 | 0 | 0 | 83.89% |
| registry_website | 1 | 1 | 0 | 0 | 20.65% |
| signature_combination | 8 | 8 | 0 | 0 | 67.56% |
| signature_rule | 4 | 4 | 0 | 0 | 51.01% |
| social | 7 | 7 | 0 | 0 | 64.57% |
| state_aid | 3 | 3 | 0 | 0 | 43.85% |
| website | 7 | 7 | 0 | 0 | 64.57% |
| website_contact | 1 | 1 | 0 | 0 | 20.65% |
| website_description | 1 | 1 | 0 | 0 | 20.65% |

Selection remains square-root type-weighted, minimum one per available type, with a census of every published website/social/brand item. Zero-published types have no eligible claim. The immutable draw remains reproducible from the committed population index.

## Human review

**Nethra Venkat, 2026-11-20: all 26 listed items CORRECT.** Basis provided by the user: exact org number on own page or registry-declared site; social linked from own site. This user-provided human verdict is recorded separately in [human-review.json](human-review.json), bound to the existing claim IDs. [Complete reviewed checklist](HUMAN_REVIEW.md). Automated checks never manufacture or override that verdict.

## Clone reproduction

Install runtime dependencies with `uv sync --frozen --no-dev`, then run `uv run --no-sync python reports/r5/precision-sample/replay.py check`. The corrected checker uses the repository's production source auditors; the old stdlib-only reproduction description is superseded. It requires only committed proof and bundled data, never ignored run directories or a live network. The checker blocks network, validates the artifact hashes and redraws exactly the same 200 IDs before source replay. The final500 clean clone independently repeats this check after installation, with no pytest in that clone.

The packet retains original public response bytes so original hashes remain reproducible, including public business-role source fields; no credentials or local home paths. Attribution/licences remain in [SOURCES](../../../docs/SOURCES.md). [Frozen sample](sample.jsonl) | [Per-item results](results.jsonl) | [Aggregate/per-type results](results.json) | [Manifest](manifest.json).

Regression/privacy gate: **12 passed in 10.73 seconds** (7 own-source ordering/tampering cases and 5 privacy checks). [Receipt](correction-tests.txt). Full pytest follows the final500 run, as requested.
