# R5 decisions

## Stage 1

- The 32 baseline failed activity sections were caused by incomplete website checks (30) and website budget exhaustion (2). Both registry update calls returned 200. These failures are retained: the combined activity section must not imply that all enabled sources were checked. Separate `run.refresh.registry_activity` metadata records registry state, 36-month bounds and unavailable announcement types.
- Use the official Enhetsregisteret entity/subunit update APIs only. Formal announcement types/text are `not_available` with a reason in coverage metadata; no kunngjoringer HTML requests. This is a 36-month update history, not a promise of comprehensive formal announcements.
- Preserve strict pagination and date validation; duplicate events or invalid pages fail the affected scope while retaining verified earlier facts. Historical workplace changes without current registry parent proof abstain.
- Source: [official API documentation](https://data.brreg.no/enhetsregisteret/api/dokumentasjon/en/index.html), checked 12 November 2026. `dato` and `updatedBefore` bound API publication time. Registry effective dates remain separately labelled and are never relabelled publication dates.
- Stage 1 live comparison: activity companies 25 → 31, activity claims 72 → 89, total facts 6,907 → 6,924. All other fact metrics are unchanged. The aggregate activity failures changed 32 → 31 because live website activity outcomes can vary; no failure state was suppressed. The independent verifier passed with zero unsupported values. Full pytest: 545 passed.
