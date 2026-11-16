# Release v4b - Revision 5 / v1.3.0

PASS for the requested technical release checks. No new application features, push or publication. Author/committer: Nethra Venkat <nethravenkat510@gmail.com>. The local annotated v1.3.0 tag identifies the release commit; its annotation records that commit SHA. The report names the exact tested source commit below; a commit cannot embed its own final hash.

## Clean clone and tested source

Exact tested revision/r5 HEAD: `7ff7c031508036d5fd65737c1a6d93915cebe9fe`; source tree `aeab38688a4bd83d684a4b234d1abbd050fe61a5`. Clone: `<REPO>\.data\r5\release-v4b-20261113-183129\repo`. It was created with git clone --no-hardlinks --single-branch --branch revision/r5 from the local repository into a new temporary workspace directory. It began with no tracked changes or copied runtime state. uv sync --frozen installed an isolated .venv; installation-smoke.json records interpreter/prefix/module/version and dependency licences, proving the clone was loaded. Initial full pytest and every sample/extraction/smoke/verification command run from this clone. No external application code was copied.

The new 100-company smoke tested metadata version 1.2.0; the accepted exact-prior-input edge rerun tested version 1.3.0. Between them, only pyproject/uv.lock editable project metadata and README/evidence changed to 1.3.0. A second uv sync --frozen and full pytest passed; all application source bytes and third-party dependency versions remain unchanged. installation-final.json and release_checks.json verify this identity. No lock upgrade or source behavior change is hidden in the release.

Full unchanged pytest: 912 passed before the metadata bump (197.221 seconds wrapper wall) and 912 passed after (210.589 seconds wrapper wall). The first environmental trial incorrectly applied the live-smoke search-disable override to tests that expect a fake provider; its two failures are preserved as pytest-environment-trial.*. Removing that override only for pytest restored the existing test contract; no application/test assertion changed. Both live smokes kept search disabled and cost $0. The final environment omits real Brave credentials for tests; the search cases inject synthetic credentials and a fake provider.

## New disjoint sample

Hash-checked existing official snapshots, not a newly downloaded universe. Uniform random.Random(20261114).sample of the original corpus order after excluding both prior 100-company cohorts. Universe 411160; excluded 200; eligible 410960. Sample is 100 unique valid identifiers, zero overlap with seeds 20261017 and 20261113; all 100 bulk rows extracted.

- Universe archive SHA-256: `1c89710e5b01f8617e86d09fbdff4a52f2f8dbbba297e74f7164b5984f5a0384`
- Universe content SHA-256: `b82d6a3e7231d1759a958c282bc4366b80ec2fab8095053d8ed7fa9cd01bc838`
- Registry snapshot SHA-256: `5b0df27c5567a655320b8dfb8975049b76c46ba93d748a8a763f8db7050b7862`
- Sample SHA-256: `0bd18780b153a1deee92ad206a03f9a1843a16b2ebb4a26b2bba6b4b2ea1bc60`
- Bulk subset SHA-256: `e19cf6e47d266b6a605b0b3dd14f1cbf08b31a78fb32820182fbb91753d96b4f`

## Smoke results

Both commands use exactly the seven evaluator flags, default enrichment/site/caps, independent fresh working directories and default state/. Search is disabled through the recorded environment, template synthesis is default and no model/API key is needed. No cap, feature, state, time or synthesis flag is added.

| Check | New 100 | Edge 10 rows |
|---|---:|---:|
| Ordered terminal envelopes | 100 | 10 |
| Unique input IDs | 100 | 9 |
| Duplicates | 0 | 1 |
| Exit | 0 | 0 |
| HTTP | 718 | 50 |
| HTTP ceiling | 1850 | 166 |
| Wall seconds | 387.864 | 33.225 |
| Websites | 3 | 0 |
| Owned social URLs | 2 | 0 |
| Jobs | 0 | 0 |
| Facts | 13248 | 1071 |
| Provider cost USD | 0.000 | 0.000 |

The 100-company smoke is well below 45 minutes, <=1850 HTTP, within the effective/requested deadline, exit 0, site generated. verify_output.py validates hashed source receipts, supported values, financial arithmetic, filing years, registry events, current exact-employer jobs and all five cited briefing topics. Unsupported synthesis/briefing values: zero. Every envelope mirrors run.synthesis/profile.synthesis; all 100 daily and 10 edge contracts have activity/change/unknown/financial/takeaway topics. The accepted edge batch is byte-identical to the previous release-v4 ten-row input and uses its hash-checked bulk subset, with a fresh edge-repeat state. It preserves two invalid checksums and one duplicate at their input positions, emits ten terminal rows, performs no requests for invalid orgs and has identical duplicate envelopes. Invalid checksum profiles remain explicitly failed placeholders. An earlier same-pattern edge trial using seven companies from the new cohort is retained under trials/new_cohort_edge; it is not substituted for the exact prior-input rerun.

## Exact run commands

From the working directories in daily.json/edge.json, using recorded environment overrides:

### daily

Working directory: `<REPO>\.data\r5\release-v4b-20261113-183129\repo\.data\release-v4b\daily`

```powershell
# Run from <REPO>\.data\r5\release-v4b-20261113-183129\repo\.data\release-v4b\daily with recorded environment overrides.
& '<REPO>\.data\r5\release-v4b-20261113-183129\repo\.venv\Scripts\python.exe' '-m' 'signalpost.cli' 'run' '--organisations' '<REPO>\.data\r5\release-v4b-20261113-183129\repo\reports\r5\release-v4b\companies100.jsonl' '--bulk' '<REPO>\.data\r5\release-v4b-20261113-183129\repo\reports\r5\release-v4b\registry100.csv' '--output' '<REPO>\.data\r5\release-v4b-20261113-183129\repo\.data\release-v4b\daily\envelopes.jsonl' '--profiles-output' '<REPO>\.data\r5\release-v4b-20261113-183129\repo\.data\release-v4b\daily\profiles.jsonl' '--report' '<REPO>\.data\r5\release-v4b-20261113-183129\repo\.data\release-v4b\daily\report.json' '--run-id' 'release-v4b-daily-seed20261114' '--expected-count' '100'
```

### edge

Working directory: `<REPO>\.data\r5\release-v4b-20261113-183129\repo\.data\release-v4b\edge-repeat`

```powershell
# Run from <REPO>\.data\r5\release-v4b-20261113-183129\repo\.data\release-v4b\edge-repeat with recorded environment overrides.
& '<REPO>\.data\r5\release-v4b-20261113-183129\repo\.venv\Scripts\python.exe' '-m' 'signalpost.cli' 'run' '--organisations' '<REPO>\.data\r5\release-v4b-20261113-183129\repo\reports\r5\release-v4b\companies10.jsonl' '--bulk' '<REPO>\.data\r5\release-v4b-20261113-183129\repo\reports\r5\release-v4\registry100.csv' '--output' '<REPO>\.data\r5\release-v4b-20261113-183129\repo\.data\release-v4b\edge-repeat\envelopes.jsonl' '--profiles-output' '<REPO>\.data\r5\release-v4b-20261113-183129\repo\.data\release-v4b\edge-repeat\profiles.jsonl' '--report' '<REPO>\.data\r5\release-v4b-20261113-183129\repo\.data\release-v4b\edge-repeat\report.json' '--run-id' 'release-v4b-edge-repeat-prior' '--expected-count' '10'
```

## Prior samples and new mock

| Metric | Frozen 20261017 (C) | Seed 20261113 (C) | New mock 20261114 |
|---|---:|---:|---:|
| Websites | 5 | 4 | 3 |
| Social companies | 3 | 1 | 2 |
| Job companies | 0 | 1 | 0 |
| Contacts | 11 | 8 | 4 |
| Activity claims | 1202 | 1137 | 1093 |
| Facts | 13325 | 13751 | 13248 |
| HTTP | 689 | 773 | 718 |
| Wall seconds | 359.686 | 379.164 | 387.864 |
| Derived ratios | 153 | 169 | 164 |
| YoY metrics | 50 | 63 | 60 |

These are different cohorts and live retrieval times. Counts do not imply exhaustive real-world coverage; exit zero does not mean every source succeeded. Section states/failure codes remain explicit in daily-summary.json and the complete report. No previous proof is reused to improve the mock. Ratios/YoY are dimensionless supported arithmetic, not forecasts. Absolute unit/scale is never inferred.

Additional audit: profiles-output IDs preserve input order; every envelope mirrors run.synthesis/profile.synthesis; website HTTP maxima are 13/8 and both sites stay below the unchanged 250000-byte gate. The bundled NAV discovery source is declared_index, built 2026-11-13T08:23:53.796625Z, with 9511 indexed ads. No index rebuild or feed fallback was substituted during release. See final_audit.json.

## Hand checks, APIs, licences and cost

urls.md/urls.json list every mock published website, social URL and job with company/org number, tier and exact saved excerpts, publisher URL, retrieval date, hash and locator. Registry homepage/social assertions are separately marked and are not ownership-verified sites. Review weaker HIGH proof separately from exact VERIFIED proof. Jobs include title/publication/deadline and exact employer/proven-subunit evidence. No contact-person text or job descriptions are republished by the inventory.

APIs: official Brreg Enhetsregisteret company/roles/subunits and shared 36-month update calls; official Regnskapsregisteret figures and annual-accounts available-copy years; official NAV feed/detail/public-token service and bundled discovery index; bounded public company-owned HTML/linked feeds/careers and proof-only maps. Robots/terms, SSRF/public-IP pinning/TLS, vetoes, politeness, per-company/global budgets and current identity rules are unchanged. No social platform crawl, paid search, model call, PDF purchase, login or subscription.

Licences: code MIT; Brreg NLOD 2.0 with attribution; NAV official feed/reuse terms; SSB KLASS CC BY 4.0; company factual excerpts their own terms. Installed dependencies and precise metadata/versions are in installation-final.json: HTTPX/httpcore/respx use BSD licences, tldextract/idna BSD-3-Clause, Pydantic/pytest/urllib3 and several utilities MIT, Requests/requests-file Apache-2.0, certifi MPL-2.0, Pygments BSD-2-Clause, typing_extensions PSF-2.0; others per recorded distribution. Lockfile and dependency metadata are authoritative for exact versions. No LLM models or paid APIs are used. Expected provider cost $0 for both smokes and normal default runs; excludes local compute/storage/network.

Full test/installation/smoke/verification logs, exact argv/config, hash-checked inputs, source manifest, output hashes, dependency licences and request reports are committed. Raw runtime blobs and generated sites remain in the clean clone .data/release-v4b/daily and .data/release-v4b/edge-repeat; no publication occurred. Decisions are recorded in reports/r5/DECISIONS.md. Stop after the local commit/tag; never push.
