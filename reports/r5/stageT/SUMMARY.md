# Stages T and G - final summary

Branch revision/r5. Author/committer Nethra Venkat. Stage T: `06b17ccf3d8c516795f5692c9a62a61fa4c27c2e`. Stage G: `a7f3106a78d7db664dd1728ca744bfb66cae64fd`. No push, new tag, version bump or publication. No external application code copied. Paid API/model/search cost $0.

## Measured results

All three samples used exactly seven evaluator flags and fresh state. The default site, enrichment, website 8/13 caps and scaled 1850 HTTP / 35-minute hard ceilings remain active. All 100 ordered terminal envelopes, all five cited briefing topics and sites are present, exit 0, zero unsupported values. All three production source manifests match each other and final source bytes.

| Seed | Prior E facts | T facts | LEI companies | Parent companies / claims | Award companies | E HTTP -> T HTTP | T wall s |
|---|---:|---:|---:|---:|---:|---:|---:|
| 20261017 | 13325 | 13344 | 19 | 0 / 0 | 0 | 690 -> 700 | 370.777 |
| 20261113 | 13751 | 13763 | 12 | 0 / 0 | 0 | 785 -> 792 | 412.763 |
| 20261114 | 13248 | 13260 | 10 | 1 / 2 | 0 | 719 -> 736 | 354.648 |

| Seed | Websites | Social companies | Job companies | Activity claims | Ratios / YoY | GLEIF / TED HTTP |
|---|---:|---:|---:|---:|---:|---:|
| 20261017 | 5 | 3 | 0 | 1202 | 153 / 50 | 5 / 5 |
| 20261113 | 4 | 1 | 1 | 1137 | 169 / 63 | 5 / 6 |
| 20261114 | 3 | 2 | 0 | 1093 | 164 / 60 | 7 / 5 |

41 LEIs and 2 ACTIVE parent relationship claims were published. Exact-ID GLEIF records require registeredAs, RA000472, Norway and typed LEI; both compact/spaced ID variants are batched. Parent facts require the exact child, typed parent, correct direct/ultimate consolidation type and ACTIVE relationship record. Entity ACTIVE and registration LAPSED are preserved as different statuses. The parent LEI never authorizes parent websites/contacts/jobs or inferred ownership shares. [Every published new item and exact excerpts](items.md); machine-readable receipts in items.json.

TED published zero awards: frozen/mock exact-ID searches returned none; daily search nominated 3 companies but TED website robots returned an empty 202 access gate. All 3 stay explicitly blocked; no bypass or guessed XML. Search arrays never establish role/country/lot attribution. A known-winner positive control returned expected notices. Structured eForms tests cover exact Norwegian buyer/selected tenderer, linked organizations/tendering parties/tenders/lots/settled contracts with selec-w and reported award dates. Legacy/ambiguous structures abstain. No amount is published: notice/consortium totals are not allocated to the target winner. Zero awards means no measured live award precision coverage. [Withheld nominations](withheld_ted_nominations.json) are not published facts.

## Precision ledger

Every published website, social profile, job, LEI/parent and award from the latest sample output is included, with company, value/URL, original proof tier, all exact excerpts, source URL/date/hash and verdict/reasons. Audit does not mutate outputs or silently remove items.

| Type | Checked | Correct | Doubtful | Wrong |
|---|---:|---:|---:|---:|
| website | 12 | 10 | 2 | 0 |
| social | 12 | 11 | 1 | 0 |
| job | 1 | 1 | 0 | 0 |
| LEI | 41 | 40 | 1 | 0 |
| parent | 2 | 2 | 0 | 0 |
| award | 0 | 0 | 0 | 0 |

Totals: 68 checked, 64 correct under automated saved-evidence rules, 4 doubtful, 0 wrong. This is not independent human-labelled precision, universal accuracy, or current live truth. Exact source ID/country/role checks differ from requiring every counterparty in a batch to be Norwegian. Group/foreign owner signals, weaker site proof, missing name spelling and historical proofs flag hand review. Social own header/footer and founder/agency exclusion are replayed; jobs recheck current-at-retrieval employer/subunit or owned careers chain. [Full ledger](../precision/LEDGER.md) and [machine-readable checks](../precision/ledger.json). README/docs EVAL report method, denominators and limits.

## Decisions and validation

Official source policies, robots statuses, schema receipts and limitations: [SOURCES.md](../../../docs/SOURCES.md#stage-t-exact-id-gleif-and-ted-checked-2026-11-13), access/. GLEIF CC0; EU TED notices reuse under EU policy, editorial docs CC BY 4.0. Runtime robots checked afresh, fixed HTTPS host allowlist, no redirects, serialized 1-second politeness or longer Crawl-delay, remaining-budget timeouts, all calls metered; 401/403/429 closes the host for the run. GLEIF/procurement source states isolate failure from existing sections. No proof rule, safety cap or source access gate relaxed.

Stage T 24 focused tests and 940 full tests passed. Stage G 3 focused ledger tests and 943 combined full tests passed (precision/pytest-commit.txt final gate). Tests cover exact/wrong country and ID, active child-parent status/type, source-bound value verification/tampering, award links/date/amount abstention, pagination, robots and budgets. Historical offline fixtures retain their original source scope; new sources have isolated transports and no network fallback.

One development trial generated 19 exact LEIs but site failed at 250824 HTML bytes. Preserved under trials/discovery_trial. Final site initially renders 48 explorer rows instead of 50, with every remaining row in Show remaining/local data/exports and the unchanged 250000-byte gate. Final sample sites pass. Superseded tests/trials remain labelled. No extra browser dependency or source-side renderer.

Stage E refresh results are retained with explicit scope: 7/7 planted interventions, 40 supported field events/zero unexpected events, unchanged/idempotent changes 0, 112 stale claims preserved on transient failures. Corrected saved-pair and live frozen refresh changes/observations 0/0. They predate GLEIF/TED and do not claim new-source refresh coverage. No new refresh run was requested for T/G. Decisions: [DECISIONS.md](../DECISIONS.md), T and G sections.

## Hand checks

- **995194163 GLÅMDAL MASKIN AS (website, doubtful)**: No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration. Exact original receipts remain in the ledger.
- **922718059 BØNES BØNES AS (LEI, doubtful)**: Exact-ID GLEIF legal name differs from registry spelling; saved GLEIF name: VIRBON INVEST BERGEN AS; review source recency. Exact original receipts remain in the ledger.
- **988217867 CONCEDO AS (website, doubtful)**: No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration. Exact original receipts remain in the ledger.
- **988217867 CONCEDO AS (social, doubtful)**: No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration. Exact original receipts remain in the ledger.
- Review both ACTIVE direct/ultimate parent records for WESTERN BULK CARRIERS AS 979993609 (seed 20261114) in items.md; do not interpret consolidation as an ownership percentage.
- Inspect daily TED nominations VEKSTPARTNER 830009612 (203993-2024), ONZONZ 925293180 (817000-2025), H & K SANDNES 980038661 (749315-2025): they are withheld search hits, not published awards.
- Review lapsed LEI registration versus entity ACTIVE status and the reported legal-form codes; source retrieval dates matter.
- Automated verdicts require independent human review before treating counts as measured real-world precision.

Final summary packaging adds nested Git attribute exceptions for items.md and LEDGER.md to preserve exact excerpt line endings; production code is unchanged.

Stopped after T, G and this summary. Nothing pushed.
