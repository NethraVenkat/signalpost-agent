# R5 decisions

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
