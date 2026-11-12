# R5 overnight summary

Stages 1–3 are complete on `revision/r5`. No Stage 4 work was started. No push or Git identity configuration changes were made. All three stage commits passed the full pytest suite before committing, then retained a fresh-state 100-company comparison and independent evidence verification. Provider cost was $0 in every run.

## Commits

| Commit | Author | Message |
|---|---|---|
| `4c4655638efb61f7633c2158f138aeddda0658bb` | Nethra Venkat <nethravenkat510@gmail.com> | Record R5 fixed 100-company baseline and isolated test results |
| `a08ab8d4618b4b2659c89839bd565e39b276338d` | Nethra Venkat <nethravenkat510@gmail.com> | Extend official registry activity to 36 months with explicit coverage |
| `de6c9285cbfbcc692b514801e575649134e5d6c1` | Nethra Venkat <nethravenkat510@gmail.com> | Retain useful registry field depth with typed evidence and profile labels |
| `0a99a0182bd270b619d9aec51856dd9883d449e3` | Nethra Venkat <nethravenkat510@gmail.com> | Add independently validated six-sentence analyst briefings |

The final summary was saved after the Stage 3 commit so it can name that immutable commit hash. At the user's request, the summary and decisions log are recorded in a separate docs-only commit. All application changes and stage measurements are committed.

## Fixed comparison

The exact frozen `baseline/companies.jsonl` (seed 20261017) and `baseline/registry100.csv` were reused with their SHA-256 hashes checked before every run. Only output/state paths and run ID changed from `baseline/settings.json`. Each stage used empty runtime state, the unchanged shipped NAV index/default age limit, a 2,000-attempt HTTP budget, a 2,400-second time budget, template synthesis and disabled paid providers. The stale index triggered full-feed fallback. Live source changes/retries mean deltas are observations, not causal proof of recall/performance improvements.

| Metric / section state | Baseline | Stage 1 | Stage 2 | Stage 3 |
|---|---:|---:|---:|---:|
| verified_websites | 5 | 5 | 5 | 5 |
| social_profile_companies | 2 | 2 | 2 | 2 |
| activity_companies | 25 | 31 | 31 | 31 |
| activity_claims | 72 | 89 | 89 | 89 |
| total_facts | 6,907 | 6,924 | 7,102 | 7,102 |
| locations | 73 | 73 | 73 | 73 |
| job_ad_companies | 0 | 0 | 0 | 0 |
| contacts | 10 | 10 | 10 | 10 |
| http_requests | 872 | 872 | 871 | 872 |
| runtime_seconds | 260.954 | 272.157 | 240.032 | 240.578 |
| process_wall_seconds | 265.561 | 280.551 | 243.966 | 243.774 |
| identity / available | 100 | 100 | 100 | 100 |
| identity / not_available | 0 | 0 | 0 | 0 |
| identity / blocked | 0 | 0 | 0 | 0 |
| identity / ambiguous | 0 | 0 | 0 | 0 |
| identity / failed | 0 | 0 | 0 | 0 |
| identity / not_applicable | 0 | 0 | 0 | 0 |
| roles / available | 100 | 100 | 100 | 100 |
| roles / not_available | 0 | 0 | 0 | 0 |
| roles / blocked | 0 | 0 | 0 | 0 |
| roles / ambiguous | 0 | 0 | 0 | 0 |
| roles / failed | 0 | 0 | 0 | 0 |
| roles / not_applicable | 0 | 0 | 0 | 0 |
| subunits / available | 71 | 71 | 71 | 71 |
| subunits / not_available | 29 | 29 | 29 | 29 |
| subunits / blocked | 0 | 0 | 0 | 0 |
| subunits / ambiguous | 0 | 0 | 0 | 0 |
| subunits / failed | 0 | 0 | 0 | 0 |
| subunits / not_applicable | 0 | 0 | 0 | 0 |
| accounts / available | 99 | 99 | 99 | 99 |
| accounts / not_available | 0 | 0 | 0 | 0 |
| accounts / blocked | 0 | 0 | 0 | 0 |
| accounts / ambiguous | 0 | 0 | 0 | 0 |
| accounts / failed | 1 | 1 | 1 | 1 |
| accounts / not_applicable | 0 | 0 | 0 | 0 |
| website / available | 5 | 5 | 5 | 5 |
| website / not_available | 65 | 65 | 65 | 65 |
| website / blocked | 1 | 1 | 1 | 1 |
| website / ambiguous | 6 | 6 | 6 | 5 |
| website / failed | 23 | 23 | 23 | 24 |
| website / not_applicable | 0 | 0 | 0 | 0 |
| hiring / available | 0 | 0 | 0 | 0 |
| hiring / not_available | 89 | 89 | 89 | 89 |
| hiring / blocked | 0 | 0 | 0 | 0 |
| hiring / ambiguous | 0 | 0 | 0 | 0 |
| hiring / failed | 11 | 11 | 11 | 11 |
| hiring / not_applicable | 0 | 0 | 0 | 0 |
| activity / available | 16 | 20 | 20 | 20 |
| activity / not_available | 52 | 49 | 49 | 49 |
| activity / blocked | 0 | 0 | 0 | 0 |
| activity / ambiguous | 0 | 0 | 0 | 0 |
| activity / failed | 32 | 31 | 31 | 31 |
| activity / not_applicable | 0 | 0 | 0 | 0 |

Counts use the exact definitions in `baseline/counts.json`. Total facts count available source claims only, including compound claims as one fact. Locations count workplace records, excluding detail attributes. Activity companies/claims include positive verified facts in incomplete sections. Section availability must be read with field states and errors; it does not promise that every optional attribute is usable.

## Tests and verification

| Stage | Full suite | Extra checks |
|---|---|---|
| 1 | 545 passed in 104.22 s | 13 new registry cases; targeted registry suite 42 passed |
| 2 | 654 passed in 84.87 s | 109 new field-depth cases |
| 3 | 663 passed in 85.81 s | 9 new briefing cases; targeted synthesis suite 41 passed |

The original baseline suite had 531 passes and one five-second child-process timeout. All three requested isolated reruns passed; no timeout or existing test was weakened or changed. The timing-sensitive test passed in each stage’s full suite.

| Verification | Baseline | Stage 1 | Stage 2 | Stage 3 |
|---|---:|---:|---:|---:|
| lines | 100 | 100 | 100 | 100 |
| published_claims | 6907 | 6924 | 7102 | 7102 |
| source_blobs_verified | 382 | 383 | 383 | 383 |
| synthesis_sentences | 817 | 834 | 834 | 1203 |
| synthesis_unverified_values | 0 | 0 | 0 | 0 |

Stage 3 briefings: 100 companies, 600 sentences, 0 companies below four sentences, 0 unsupported values. The verifier checks every briefing citation and sentence independently as well as the full summaries.

## Files and tests by stage

- Stage 1: `registry_activity.py`, `sources/registry_changes.py`, source policy documentation, `tests/test_r5_registry_activity.py`, the reusable `reports/r5/measure_stage.py`, and stage comparison reports. Added date-window/leap-day, missing-date, pagination/duplicate/short-page, partial-positive and parent-proof tests.
- Stage 2: `sources/registry_fields.py`, entity/subunit/CSV extractors, `refresh/diff.py`, profile labels in `site.py`, schema documentation, `tests/test_r5_fact_depth.py`, and comparison reports. Tests cover every newly retained field, absent/null/odd values, JSON/CSV parity, provenance, employee zero/false and address distinctions.
- Stage 3: `models/synthesis.py`, `synthesis/brief.py`, `template.py`, `validate.py`, profile briefing selection, `scripts/verify_output.py`, schema documentation, `tests/test_r5_briefings.py`, and comparison reports. Tests cover all topics, missing citations, invented values, wrong bindings, contradictory gaps, sparse profiles and all three envelope shapes.

Each stage directory contains `run.ps1`, resolved settings, execution timestamps, the original runner report, exact metric definitions/per-company counts, independent verification results, test results and `table.md`. Raw envelopes, profiles, source bodies and sites remain local under `.data/r5/stageN-run/`; output hashes are retained in the committed counts files.

## Manual review and limits

- Formal announcement text/types are not available through the chosen public update APIs. They are explicitly marked not_available; no robots-blocked kunngjoringer HTML was fetched. Confirm whether this narrower official update history meets your downstream requirement.
- Website recall remains five companies and hiring remains zero published ad companies. Failed/blocked/ambiguous source checks are retained. These counts do not establish national absence of websites or jobs.
- The frozen CSV contains unsupported optional list encodings: all 100 registry-annotation fields and seven voluntary-VAT-description fields were retained as null/failed with reasons. They were not decoded by guessing. API JSON lists are supported and tested. Review these field-level failures if these attributes matter.
- Manually review a few generated profiles, especially group/subunit attribution, new historical/foreign-register attributes, partial activity results and briefing wording. Automated schema, identity-policy, citation and evidence checks passed; no new manual browser/visual audit was claimed.
- Review refresh migration against older releases before using enriched address/form components to interpret historical diffs. The fixed comparisons here are fresh runs, not a historical-schema migration audit.
- Local `.data/` working artifacts remain uncommitted; the final summary, decisions log, three stage implementations and their comparison reports are committed. You will push manually if desired.

## Complete decisions log


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
