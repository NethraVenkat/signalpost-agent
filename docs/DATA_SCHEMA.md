# Data schema

JSONL output contains one validated envelope per unique normalized input, in input order. Pydantic v2 rejects unknown keys. `--emit-duplicates` optionally repeats envelopes for duplicate input rows.

## Envelope shapes

| Shape | Exact root keys |
|---|---|
| contract | organisation_number, run, claims, evidence, changes, errors, operations |
| reference | run_id, organisation_number, state, started_at, completed_at, modules, profile |
| union (default) | The union of the two root-key sets above |

Contract `run` holds ID, timestamps, terminal status, legal identity, section states and refresh metadata. Reference `modules` have `state`, `retry_count`, `final_timestamp`. Its profile holds full claims/evidence/changes/errors/sections/refresh/operations. Union profile is compact: organisation_number, field-to-value `values`, and evidence_ids; it does not duplicate source bodies.

## Claims and evidence

Claims contain `id`, `family`, `field`, `value`, `availability`, `confidence`, `evidence_ids`, reporting_period, carried_forward, first/last_observed_at and reasons. Confidence is an extraction annotation, not a calibrated probability. Missing values are null, never a fabricated zero, empty string or omitted field. Reported numeric zero and boolean false remain valid.

Available facts require evidence. Checked absence can have source evidence; failures without a retrieved source have null placeholders and error records, without invented provenance.

Evidence contains deterministic `id`, source_url, source_class, retrieved_at (UTC with Z), content_sha256, claim_span (verbatim, at most 300 characters), locator, versioned extraction_method, source_identifier, effective_at and reporting_period. Hashes cover the exact stored body at `state/blobs/<sha256>`. Bulk evidence hashes an exact header plus selected CSV record; its source identifier separately includes the whole archive hash. Financial calibration evidence uses short extracted fact records and identifiers containing the original PDF hashes/page locators.

Raw bodies are never serialized into current envelopes. Legacy embedded-body input is accepted for compatibility. Previous evidence metadata can be retained without retrieving its historical body again. Full independent hash verification needs the corresponding archived blobs.

## Availability and terminal states

| Availability | Reference state | Meaning / exception |
|---|---|---|
| available | complete | Supported value |
| not_available | not_found | Checked absence within declared scope |
| blocked | blocked_policy | Policy/access refusal; robots uses blocked_robots |
| not_applicable | not_applicable | Explicitly supported exemption only |
| ambiguous | submission_error | Lossy mapping; original ambiguity remains in claims/sections |
| failed | source_error | Incomplete/unreliable check; budget_exhausted overrides; invalid input, not-started or deadline maps to submission_error |

Terminal entity `complete` describes processing, not full coverage. It can coexist with source-error modules. Inspect section states and errors to assess coverage.

## Field families

- Identity: legal name/form, registration date, registered/postal address, municipality, NACE codes/text, employee count, registered website, bankruptcy/liquidation/deletion flags and latest submitted accounts year. Missing flags/counts are not manufactured.
- Roles: one role claim per stable role/name/entity key with source-item locator, role type and available effective dates. Person birth dates are excluded.
- Subunits: one claim per organisation number with reported name, address, NACE and employee data; every page is checked against its parent.
- Accounts: latest exact-company SELSKAP filing. Revenue, operating result, result before tax, net result, equity, assets and liabilities are reported values only. Carry fiscal year, period dates, currency, unit and account type. Missing metrics are null. No legal-form-only exemption is inferred.
- Websites (opt-in): official_website proof object; own-domain email/phone, public brand and company social-profile links. Registered website identity fields remain unchanged. Proof records final/proof URL, identity level, proof type, signals, points, origin and relationship.
- Hiring (opt-in): one hiring.job.UUID with UUID, employer_orgnr, title, municipality/city, published, expires, occupation categories, public URL and matched_via. Missing location/categories are null with nested availability. Evidence links both detail `/ad_content` and feed-page `/items/N`. Descriptions and contact-person details are excluded.

NOK accounts with absent source unit carry empirical whole-NOK metadata, source_unit=null and a four-ratio calibration basis. No multiplier is applied. Other/missing currencies remain unknown unless reported. Claim identity excludes this enrichment annotation; original reporting period and source unit remain meaningful. [Calibration](SOURCES.md#financial-unit-calibration).

## Section scope and reports

Website states distinguish publication, ambiguity, registered-site policy blocks, unresolved source/budget failures and checked negatives. Guessed NXDOMAIN is a normal rejection. Failed optional follow-ups preserve already established proof.

Hiring completeness is scoped per company to known name candidates. Page/time failure affects everyone; detail cap/error affects associated companies, or everyone for nameless headers. Unusable names stay failed. Known-subunit coverage must also be checked before absence. `run.refresh.hiring` records completeness, reason and known closed previous UUIDs.

Run reports include membership/duplicate/invalid counts; terminal/availability counts; requests by host and attempt logs; direct, shared and amortized requests/company; company runtime p50/p95/max; deadlines/errors; output size/cap; company and observation changes; zero third-party cost per 100 and per declared official-batch size. Hiring reports add pages/items/bytes, candidate counts, names present/missing, detail cap/count, attribution, indexed ads and incomplete-company scope. Attribution can count one shared detail toward several discovery candidates.
