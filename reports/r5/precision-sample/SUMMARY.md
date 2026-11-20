# Seeded precision sample: strict saved-evidence audit

Source application `4ca3443`; standard-100 envelopes SHA-256 `3c7a410c9459cafa79e1c3a22b20c31db4384d3df2096b22311c7dea78dccc3b`. Seed **2026112601**; 200 published claims selected without replacement from 14,165 available claims. Selection was frozen before verification; no outcome-based resampling.

**50 correct / 0 incorrect / 150 unverifiable** under the strict checks below. Nominal two-sided Wilson 95% lower bound: **19.51%**, treating unverifiable items as unverified. This is not a 25% factual-accuracy estimate or a claim of population precision.

## Design and interpretation

Each published claim belongs to one information-type stratum. Allocation uses square-root population weights, at least one per available type, and a census of all published website/social/brand items (including registered workplace brands). Remaining seats use deterministic divisor allocation; records are sorted before the seeded draw. Zero-published types have no eligible claim: research, procurement, jobs and ticker/ISIN. Allocation, full population index, sample values and source envelope hash are committed. The disproportionately stratified sample and census components mean the pooled Wilson bound describes selected-item certification; it is not a design-adjusted population confidence guarantee. Per-type bounds are nominal and small samples remain weak.

Correct requires: original response SHA-256 matches; cited span occurs verbatim in original response; URL is bound to that hash in the saved HTTP ledger (or the documented bundled/bulk provenance); exact company identity is independently established; and every non-null scalar leaf of the full published value appears literally in cited spans. Numeric tokens require boundaries: `100.0` is not silently treated as the verbatim token `100.00`. No case folding, whitespace normalization, date conversion or metadata suppression makes a value pass. Incorrect is a proven hash/span/identity contradiction. Unverifiable means the strict checks cannot certify the item, not that the underlying business fact is false.

The strict criterion is substantially stronger than the existing complete-source semantic auditor. Composite values include reformatted dates/numbers, assembled names, provenance/status labels and metadata; the 300-character display span often omits part of an otherwise supported full-source record. Thus all sampled financial values fail this literal-presentation test even though the earlier full-source auditor passed them. Website identity spans often show the orgnr rather than the final URL; signing combinations and group records contain scoped metadata absent from the short display span. Independent record-owner reconstruction also abstains for some bundled/location records. These limitations remain unverifiable rather than being converted to precision successes. See every missing value and reason in `results.jsonl`.

| Type | Sample | Correct | Incorrect | Unverifiable | Wilson 95% lower |
|---|---:|---:|---:|---:|---:|
| brand | 9 | 5 | 0 | 4 | 26.67% |
| consolidated_accounts | 7 | 0 | 0 | 7 | 0.00% |
| entity_accounts | 42 | 0 | 0 | 42 | 0.00% |
| filing_years | 16 | 0 | 0 | 16 | 0.00% |
| group_parent | 1 | 0 | 0 | 1 | 0.00% |
| group_subsidiary | 4 | 0 | 0 | 4 | 0.00% |
| identity | 29 | 27 | 0 | 2 | 78.04% |
| inspections | 1 | 0 | 0 | 1 | 0.00% |
| lei | 2 | 2 | 0 | 0 | 34.24% |
| licences | 1 | 0 | 0 | 1 | 0.00% |
| locations_subunits | 15 | 0 | 0 | 15 | 0.00% |
| people_roles | 19 | 10 | 0 | 9 | 31.71% |
| prokura_combination | 1 | 0 | 0 | 1 | 0.00% |
| prokura_rule | 1 | 1 | 0 | 0 | 20.65% |
| public_activity | 20 | 0 | 0 | 20 | 0.00% |
| registry_website | 1 | 1 | 0 | 0 | 20.65% |
| signature_combination | 8 | 0 | 0 | 8 | 0.00% |
| signature_rule | 4 | 4 | 0 | 0 | 51.01% |
| social | 7 | 0 | 0 | 7 | 0.00% |
| state_aid | 3 | 0 | 0 | 3 | 0.00% |
| website | 7 | 0 | 0 | 7 | 0.00% |
| website_contact | 1 | 0 | 0 | 1 | 0.00% |
| website_description | 1 | 0 | 0 | 1 | 0.00% |

## Clone-only reproduction

Run `python reports/r5/precision-sample/replay.py check` with Python 3.12+. No installation, network, API key, `.data/`, `out/` or prior run directory is required. The script hash-checks original proof bodies and the population/sample artifacts, redraws exactly the same 200 IDs, then rewrites deterministic results and the human checklist. [Clean data-only replay](clean-data-replay.json) passed with byte-identical results; the final-500 clean clone will independently replay the committed packet.

`proof.json.gz` holds original full saved response bytes for the selected facts and exact registry/site identity context. Original bytes are retained to make the original hash test possible; public business-role responses may contain publisher birth-date fields, which are not projected claim values. No local filesystem paths or credentials are included. Publisher attribution and applicable licences remain as in [SOURCES](../../../docs/SOURCES.md); Brreg NLOD attribution is preserved in source URLs. The packet is evidence for local replay, not a new data source or independent human validation.

[Human checklist: every selected website/social/brand/contact item](HUMAN_REVIEW.md). **Human review pending**; no automatic label is a human verdict. All website/social/brand strata are censuses; registered website, description and contact strata have selected items too.

[Frozen sample](sample.jsonl) | [Per-item outcomes](results.jsonl) | [Totals](results.json) | [Selection manifest](manifest.json).
