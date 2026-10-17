# Phase 1 BRREG safety groundwork — release gates pending

The proposed 90% reduction is **not implemented or measured**. This change adds
verification controls and registry provenance without changing the claim schema.
It does not qualify as a Phase 1 release.

## Findings

The existing bulk loader already streams plain/gzip CSV, detects delimiters,
indexes only requested companies, and stores exact selected records as evidence.
CSV hits already avoid identity requests. Roles and subunits still use API calls.

BRREG's official API documents roles per company at
`/enhetsregisteret/api/enheter/{orgnr}/roller`. The proposed `/roller?orgnr=...`
batch endpoint is not documented. Concurrent calls are still separate requests;
there is no implemented or verified ten-company batching mechanism.

Sources checked on 2026-10-17:

- https://data.brreg.no/enhetsregisteret/api/dokumentasjon/no/index.html
- https://www.brreg.no/bruke-data-fra-bronnoysundregistrene/datasett-og-api/roller-i-virksomheten/

## Implemented behavior

`signalpost run --verify-bulk ...` requires API identity verification even when
the CSV contains that company. The API extractor supplies all identity claims;
CSV values cannot override an API conflict or fill an absent API field. A failed,
blocked, missing or wrong-company identity response cannot fall back to CSV.
Refresh cannot carry forward old identity claims in this mode either.

This is opt-in to retain existing default behavior for saved-source replay.
Without the flag, CSV identity claims remain snapshot-backed, not live verified.
The flag adds identity requests and is a correctness control, not a request-saving
optimization. Existing roles, subunit pagination, accounts, retry accounting and
global request budgets remain in force.

The report's `registry_provenance` links registry claim IDs and evidence IDs to
`source_types`, and counts request attempts by registry family, including retries
and pagination. `csv_cache` means CSV evidence; `live_verified` requires a
successful current-run request matching both source URL and body hash.
Injected clients, including offline replay, use `api_checked` rather than claiming
live verification. Carried API claims use `historical_api`; unmatched evidence
uses `unverified` or `unknown`. These are provenance classifications, not an
independent factual audit. Website and hiring claims are outside this report
section's scope.

Attribution is stored in the report instead of adding `source_type` to claims:
adding a serialized claim field would conflict with the requested byte-identical
legacy claim contract. This is a disclosed deviation from the proposed schema.

## Validation and outstanding gates

- Original registry and integration determinism subset: 42 passed.
- Final registry, new safety, integration determinism and execution diagnostics
  subset after moving provenance reporting off the event loop: 51 passed.
- New safety tests: 7 passed, covering 1,000 CSV rows with stored evidence,
  CSV/API conflicts and request counts, failed/blocked/wrong-company verification,
  refresh carry-forward prevention and injected transport attribution.
- Full suite: 429 passed, 3 failed in 69.75 seconds. Failures were
  `test_analyze_envelopes_coverage`,
  `TestExtractLinkedinFromBraveResult.test_match_with_existing_evidence`, and
  `TestDiscoverLinkedinUrls.test_discover_single_match`. Their tests and production
  dashboard/LinkedIn modules were not changed. The all-tests-pass gate is failed.
- Strict production replay using the six recorded responses in the declared
  integration bundle completed with four output envelopes (three distinct input
  identifiers). Stored-source audit reviewed 182 claims: 182 correct, zero
  incorrect, unverifiable, unsupported or wrong-company claims. All 427 hash,
  span and locator checks passed, with no missing blobs or attribution errors.
  Artifacts are under `out/phase1-replay/`; they are local generated outputs.
  The audit explicitly did not evaluate independent current-live factual truth.
- The existing determinism test compares four fixture envelopes semantically.
  Passing it does **not** establish byte-identical replay of 300 v4 envelopes.
- The supplied paths `state/downloads/wednesday100.jsonl` and
  `state/downloads/wednesday100.csv` are absent from this checkout. No 1,000-company
  cold cohort or v4 68,993-claim baseline was supplied here either.
- Cold 100 and cold 1,000 audits, the 300-envelope byte comparison, unchanged
  68,993-claim coverage, sub-50-second runtime and <=2,000 requests remain
  **unverified**. No release commit or push is justified by the available evidence.

Run the actual production entry point as `python -m signalpost.cli`; the audit
is `python scripts/accuracy_audit.py --help`, not the nonexistent
`src.signalpost.scripts.accuracy_audit` module in the proposed commands.

To continue, obtain the original cohort files, baseline envelopes and source
blobs, then measure the existing CSV-first baseline and strict verification mode
in separate empty state directories. Request reduction beyond existing CSV hits
requires a documented bulk API or a separately validated source strategy. Do not
skip role or subunit verification to reach the numerical target.
