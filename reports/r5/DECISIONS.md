# R5 decisions

## Stage 4.2

- Publish typed business/postal/workplace locations from their exact registry fields and proven company/subunit scope. Preserve the compatible core address/workplace records; postal fallback is never relabelled as physical workplace. No map/geocoding source or new requests. Newly observed typed fields are coverage observations on refresh, not invented company moves.
- 4.2: 679 tests passed; total facts 7,320 versus Stage 3's 7,102; workplace records remain 73. Five websites/two social companies, no new URLs, zero unsupported values. Exact typed counts are in `step4_2/typed_locations.json`.

## Stage 4.0 and 4.1

- Diagnose first using Stage 3 saved envelopes/request logs only: 24 failed, 5 ambiguous, 1 blocked. Primary causes: 19 budget, 5 ambiguity, 2 timeout, 2 DNS, 1 access block, 1 transport/content refusal. Full company/domain/code lists are in `stage4/diagnosis.md` and machine diagnostics in `diagnosis.json`.
- Fix original-host DNS precheck preventing www/non-www fallback, retaining eight DNS nominations and unchanged HTTP/time caps. HTTPS is tried first even for HTTP nominations; plaintext still requires real TLS/connect failure. Private-address failures do not authorize fallback.
- Remove existing sitemap/RSS candidate discovery, and filter known non-HTML proof targets before requests. These are budget/policy fixes before recall expansion; no caps are raised. Exhausted proof work remains failed/ambiguous rather than absence.
- Keep exact-number VERIFIED, strictly corroborated registry-origin HIGH and default-off REGISTRY_DECLARED tiers. Group sites without the exact number are vetoed; parked domains, marketplaces and directories cannot become company sources. No AS masthead, unique-name or loose social rule is added.
- 4.1 verification: 671 tests passed. Frozen run retains five websites/two social companies, with no new URLs. Two-host DNS checking spends the unchanged eight-check allowance sooner: website failures are 41 rather than Stage 3's 24 (not_available 47 rather than 65). These are explicit incomplete checks, not a claimed coverage gain. HTTP attempts 870, provider cost $0, unsupported synthesis/briefing values zero. The old DNS test now asserts each hostname is cached exactly once across companies, preserves zero-HTTP and private-address veto assertions, and does not loosen timeout or proof checks.

## Stage 1

- The 32 baseline failed activity sections were caused by incomplete website checks (30) and website budget exhaustion (2). Both registry update calls returned 200. These failures are retained: the combined activity section must not imply that all enabled sources were checked. Separate `run.refresh.registry_activity` metadata records registry state, 36-month bounds and unavailable announcement types.
- Use the official Enhetsregisteret entity/subunit update APIs only. Formal announcement types/text are `not_available` with a reason in coverage metadata; no kunngjoringer HTML requests. This is a 36-month update history, not a promise of comprehensive formal announcements.
- Preserve strict pagination and date validation; duplicate events or invalid pages fail the affected scope while retaining verified earlier facts. Historical workplace changes without current registry parent proof abstain.
- Source: [official API documentation](https://data.brreg.no/enhetsregisteret/api/dokumentasjon/en/index.html), checked 12 November 2026. `dato` and `updatedBefore` bound API publication time. Registry effective dates remain separately labelled and are never relabelled publication dates.
- Stage 1 live comparison: activity companies 25 → 31, activity claims 72 → 89, total facts 6,907 → 6,924. All other fact metrics are unchanged. The aggregate activity failures changed 32 → 31 because live website activity outcomes can vary; no failure state was suppressed. The independent verifier passed with zero unsupported values. Full pytest: 545 passed.

## Stage 2

- Existing core/EXTRA/GROUPS fields already retain most requested examples. Preserve these fields and compatible compound records; add the useful dropped attributes listed explicitly in `registry_fields.py`, without duplicating every nested scalar to inflate fact counts.
- Use an explicit official-schema allowlist, excluding HAL navigation/response-class metadata and undocumented fields. Historical names and foreign register references are descriptive facts only, never identity/parent proof.
- Supplied nulls stay null; invalid optional field shapes are null/failed with a reason. Absent optional keys have no source claim, while section availability stays explicit. Do not invent empty lists or source dates. An explicit false employee-reporting flag suppresses the count; boolean values cannot masquerade as numeric zero/one.
- No additional API requests or provider calls for field depth. The frozen CSV is retained for the baseline comparison; fields absent from that snapshot are not backfilled using invented values or unrequested sources.
- Malformed deletion dates previously could become deletion flags or invalid evidence timestamps. R5 suppresses the flag and retains a failed/null optional date; no truth is inferred from a non-date value.
- Stage 2 full pytest: 654 passed. Fresh comparison: total facts 7,102 (baseline 6,907; Stage 1 6,924). Every other fact metric and section state is unchanged from Stage 1. HTTP attempts 871 versus 872 are live retry variation, not a claim of a code-level request saving. Verifier: zero unsupported values.
- Field-level audit: the frozen CSV has unsupported list encodings for 100 `registry_annotations` fields and seven `voluntary_vat_descriptions` fields. These remain null/failed with reasons, not guessed into arrays. Proper API JSON arrays are supported and tested. Section availability describes retained supported facts; inspect individual field states/errors for these optional attributes.

## Stage 3

- Add a separate template-only `synthesis.briefing` (four to six sentences when supported) while retaining the complete cited section catalog and summary. The profile displays the briefing first. Sparse companies remain shorter with an explicit reason; never invent facts to meet a sentence target.
- Briefing topics prioritize activity, scale, leadership, recent dated activity, evidence-backed gaps and registry context. No source claim is created by synthesis. Depth frames are bound to exact fields; financial-history limitations require all supported account claims to share one fiscal period; a missing employee-count statement requires a current false registry reporting flag.
- Keep the existing citation validator and extend it with exact frame checks and independent briefing checks. The output verifier also checks every briefing sentence; no LLM/provider call is enabled.
- Stage 3 full pytest: 663 passed. Live verification: 100 companies with exactly six briefing sentences each (600 total), zero short briefings and zero unsupported values; 1,203 full-catalog sentences also validate. Source facts remain 7,102 and provider cost is $0. Website state drift (ambiguous 6 → 5, failed 23 → 24) is retained as a live observation, not hidden or relabelled.
- The final summary was written after the Stage 3 commit so it can contain that commit's actual hash. The user subsequently requested a separate docs-only commit for the summary and decisions log. All application changes and stage measurements are committed. No Stage 4 work.
- Manual follow-up: inspect sample profiles, optional-field failures, the formal-announcement limitation and refresh migration from older schema versions. The fresh fixed-cohort comparisons are not a historical-schema migration audit; enriched address/form components should not be treated as proven historic company changes without review.
