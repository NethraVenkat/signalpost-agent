# Revision 3b ? Step 1 smoke test only

Verdict: **GO for a narrow, opt-in entity-change implementation; DO NOT SHIP yet.** Step 1 is complete and work stops here. Revision 2 at `a704375` remains final. No Step 2/3 code, release gates, push, merge, tag or email was performed.

Baseline inspected: `a704375`. The initial checkout was `revision/r3` at `a73f713`; preserved that branch and created `revision/r3b` directly from `a704375`. This commit adds only smoke evidence and reports. Source, tests, dependency files and existing claim values are unchanged. The final documentation SHA is supplied in chat.

Recorded on 18 October 2026, before 16:30 IST and within the 20-minute smoke budget. Raw response timestamps are UTC. First time checkpoint: 12:21:15 IST; report generated 2026-10-18T12:25:55.413033+05:30.

## Sample and observed coverage

First 20 rows of the existing 1,000-company input, without selecting for coverage. Its SHA-256 is `bba3114b5a611d05a80bbce11233aa3585c433a1580225dc5087a75372b9649a`, matching `reports/r2/inputs.json`. Exact sample, selection and source hash: [sample](smoke/sample.json). This small input-order sample is not a representative coverage estimate.

Window requested: `2024-10-18T00:00:00.000Z` through retrieval on 2026-10-18. This calendar-date window includes several hours before the exact rolling 24-month boundary; the earliest returned sample event is November 2024, so counts are unaffected.

| Feed | Events | Companies with >=1 event | Events with field details |
|---|---:|---:|---:|
| Entity | 121 | 20/20 | 44 |
| Subunit, using verified parent-to-subunit mappings | 36 | 13/20 | 16 |
| Roles | 45 | 15/20 | 0 |

All three final sample responses were HTTP 200 and complete for their query: entity/subunit `totalPages=1`; roles returned 45, below requested size 1000. Every returned entity/role number belongs to the sample; mapped subunit IDs were checked against exact `overordnetEnhet`. Current mappings found 15 subunits; historical subunits no longer linked today are not measured. Passing the parent org numbers directly to the subunit feed returned zero events, which does **not** mean zero subsidiary activity.

**Publishable potential is much smaller than raw coverage.** All 20 have some named entity detail, but many are annual-account fields, employee reporting metadata or industry-code changes. A conservative address/name/capital allowlist yields **4 events across 3/20 companies**. No claims have been published. Seventy-seven entity events have no details and must not become bare ?record updated? claims.

## Real contracts, history and dates

Entity and subunit responses are HAL objects: `_embedded.oppdaterteEnheter` / `_embedded.oppdaterteUnderenheter`, `_links`, and `page` with `number`, `size`, `totalElements`, `totalPages`. Events contain `organisasjonsnummer`, integer `oppdateringsid`, UTC `dato`, `endringstype`, a registry link, and optionally `endringer`. Observed entity types: 96 `Endring`, 20 `Ukjent`, 5 `Ny`.

`includeChanges=true` is verified live. Details are JSON Patch-like operations with `op`, `path`, and `value` for add/replace; remove may have no value. Do not assume an old value is present. Example: org `932525070`, event `23540812`, `2025-12-22T14:30:11.129Z`, replaces `/kapital/belop` with 11000000 and also changes capital registration date and statutes date. Address events are `23493349`, `23522825`, and `23562299`; full original bodies are retained.

Entity sample dates: 2024-11-18T14:05:12.971Z through 2026-09-15T22:01:20.888Z. Mapped subunit dates: 2024-11-19T05:00:50.525Z through 2026-09-15T22:01:22.937Z. Roles: 2024-11-18T14:05:11.773Z through 2026-10-12T22:21:46.382Z. These are API publication times, not necessarily the effective business-change dates.

Earliest accessible records observed using ascending ID/default roles order:

| Feed | Earliest observed timestamp | ID |
|---|---|---|
| Entity | 2018-04-23T06:03:29.443Z | 1 |
| Subunit | 2018-04-23T06:03:29.830Z | 50 |
| Roles | 2022-03-14T14:30:44.251Z | 1 |

These probes demonstrate accessible history, not a retention guarantee or proof of historical completeness. Earliest detailed entity event in this sample is September 13, 2025; older events lack details. The official changelog records the `includeChanges`/`endringer` addition on September 23, 2025.

Roles have a **different contract**: a plain array of CloudEvents containing `data.organisasjonsnummer`, string `id`, `source`, `specversion`, `time`, and `type=no.brreg.enhetsregisteret.rolle.oppdatert`. The working filter is `afterTime`, with cursor `afterId`, comma-separated `organisasjonsnummer`, and `size`. It rejects entity-feed parameters `dato`, `includeChanges`, and `sort`. These notifications do not identify a role type or historical role-holder change. Fetching current roles alone cannot prove which role changed at a past event. **Exclude role notifications from public activity unless independent historical comparison proves the named change.**

Official contract and changelog: [BRREG documentation](https://data.brreg.no/enhetsregisteret/api/dokumentasjon/no/index.html). Exact URLs, UTC retrieval times, timings and SHA-256 values are in adjacent `*.meta.json` files; [summary](smoke/summary.json) includes conservative meaningful events and per-company counts.

## Latency, failures and request implications

Saved probe metadata: 31 requests, 27 HTTP 200, 4 HTTP 400 from deliberate/initial contract probes. Successful request wall times: min 1.035 s, median 1.245 s, max 3.712 s, using at most 3 concurrent requests. Twenty of these requests establish current parent/subunit mappings. One additional initial entity reachability call succeeded and one official documentation fetch succeeded; their bodies/latencies are not part of the measured dataset. No 429 or rate-limit headers were observed in the saved initial successful responses; service throughput limits were not load-tested.

The first sandbox attempt failed with Windows socket permission error 10013; the authorized network retry succeeded. This was an environment restriction, not a flaky-network loss or code regression. Four HTTP 400s are query-contract errors, not source downtime. No remaining live network losses occurred. There is no implementation under test, so no code regression is asserted.

Bulk entity filtering and detail retrieval are feasible in one request for this 20-company cohort. Do **not** promise <=10 requests for 1,000 companies from this smoke: URL length, number of events, pagination, subsidiary mapping and cursor handling need bounded planning. Reuse already acquired subunit mappings; keep all errors explicit. Large event histories must not silently truncate at 10,000.

## What revision 2 already uses (inspection at a704375)

| Proposed improvement | Existing behavior |
|---|---|
| Subunit `hjemmeside` candidates | Already implemented: `sources/brreg_underenheter.py` DETAILS; collector builds subunit context; `web/candidates.py:75` nominates with subunit ID. Exact subunit proof is labelled. |
| NAV `employer.homepage` candidates | Not implemented: no `homepage` field use in the NAV sources and no NAV candidate origin in website generation. Recruiter exclusions would need implementation before nomination. |
| Extra proof pages | Already implemented: ranked contact/about/privacy/terms links plus six fallback paths (`/kontakt`, `/kontakt-oss`, `/om-oss`, `/om`, `/personvern`, `/personvernerklaering`), within existing page limits. `/vilkar` is not a fixed fallback. |
| schema.org `vatID` / `taxID` | Already implemented with `identifier`, excluding Person objects. Explicit string identifiers normalize NO/MVA wrappers; object identifiers inspect `value`. |
| Spaced, dotted, NBSP numbers / mod-11 | Already implemented via `orgnrs()` and `identity.orgnr.valid()`. Hyphens and adjacent NO/MVA wrappers in ordinary visible text are not generally handled. |
| Wix inline data | No general Wix inline-state extraction; parser admits `application/ld+json`, not arbitrary scripts. |
| Agency/parent/footer guard | Partial: foreign-number rejection, directory/multi-entity checks and entity-card rules exist, but no general agency/parent ownership attribution guard; visible footer text remains in owner text. Do not claim this proposed guard is complete. |

Baseline source references: `web/proof.py:9,217`, `web/collector.py:139,152,192`, `web/candidates.py:75`, `web/html.py:56,112`, `sources/brreg_underenheter.py:8`. Existing tests/source were inspected; no full suite is needed for this documentation-only smoke.

## Recommendation and release status

Proceed only with an explicitly enabled, conservative entity-change source that publishes named, meaningful fields; skip generic role notifications. Prioritize preserving exact proof, IDs, schema, budgets and explicit failed-section behavior. Most Step 3 suggestions already exist and should be skipped; new candidates/proof expansions require their own strict precision checks.

Risk: **registry change events may not count as public activity in Builderr's pool**. Reporting metadata, mass NACE migrations and account filing years are not automatically meaningful business news. Never synthesize an effective event date or old value that the feed does not provide.

All implementation/release gates (full suite, source replay, live 50, fault 100, default 1,000, 24 baseline, pushed CI and clean clone) are **NOT RUN**. Pilot coverage comparisons, final implementation SHA, release commands and revision email draft are not yet applicable. No release recommendation beyond Step 1 is made. Stop here as requested.

## Per-company raw event counts

| Org | Entity | Mapped subunit | Roles |
|---|---:|---:|---:|
| 925181536 | 4 | 0 | 0 |
| 829577372 | 4 | 0 | 0 |
| 932525070 | 13 | 1 | 7 |
| 919263601 | 3 | 0 | 0 |
| 988963259 | 3 | 1 | 5 |
| 915188389 | 15 | 12 | 4 |
| 934485718 | 5 | 2 | 4 |
| 936035523 | 6 | 3 | 1 |
| 936349676 | 7 | 3 | 4 |
| 935962196 | 5 | 2 | 2 |
| 997095987 | 5 | 2 | 1 |
| 950310499 | 9 | 0 | 3 |
| 948639416 | 4 | 0 | 3 |
| 927439794 | 5 | 1 | 0 |
| 975514412 | 4 | 2 | 1 |
| 918843183 | 3 | 0 | 0 |
| 934216385 | 6 | 1 | 2 |
| 935647142 | 3 | 1 | 2 |
| 930621927 | 3 | 0 | 2 |
| 946595845 | 14 | 5 | 4 |
