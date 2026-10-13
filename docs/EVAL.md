# Evaluation and smoke checks

Install pinned dependencies and run the offline suite:

```sh
uv sync --frozen
uv run pytest
```

The suite currently has 117 tests covering checksum/input membership, isolation/deadlines/budgets, missing versus reported zero, all envelope shapes, stored provenance, refresh/carry-forward, website proof/robots/SSRF/politeness, NAV exact matches/caps/ETags, output verification, synthesis citations/values/counts and fake-provider placeholders/cache/caps/fallback. Fixtures are small and local; no credentials or internet are required for these tests.

## Live 20-company registry smoke

```sh
uv run signalpost run --organisations tests/fixtures/ci20.jsonl --bulk tests/fixtures/ci20.csv --output out/smoke20.jsonl --report out/smoke20-report.json --expected-count 20 --time-budget-seconds 180
uv run python scripts/verify_output.py --first out/smoke20.jsonl --organisations tests/fixtures/ci20.jsonl --count 20 --state-dir state --report out/smoke20-report.json --require-clean
```

The committed public fixtures provide identity rows. Roles, subunits and accounts are freshly requested from official APIs. Websites and NAV are disabled for this short CI check. `--require-clean` requires complete checked sections, zero exceptions/deadlines/warnings, valid membership and output bounds. HTTP/network failure makes this gate fail rather than silently accepting a terminal output.

GitHub Actions has two Ubuntu jobs: tests and live-20. Both run frozen installation. Source failures can make the live job red independently of deterministic unit tests. Check the [Actions page](https://github.com/NethraVenkat/signalpost-agent/actions) for the actual results of the published revision.

## Output verification and refresh

The verifier checks schemas, exact input membership/order, available-claim evidence links, actual stored-body SHA-256 and verbatim spans. When synthesis is present, it checks sentence citations/values, counters, concatenated text, change citations and the union mirror without dropping or rewriting rejected output. It requires the corresponding blobs, including archives for carried-forward claims. No network request is made by verification.

```sh
uv run signalpost run --organisations batch.jsonl --bulk registry.csv --output out/first.jsonl --report out/first-report.json
uv run signalpost run --organisations batch.jsonl --bulk registry.csv --output out/second.jsonl --report out/second-report.json --previous out/first.jsonl
uv run python scripts/verify_output.py --first out/first.jsonl --second out/second.jsonl --organisations batch.jsonl --count 100 --state-dir state
```

Fixed-source refresh expects identical claim IDs and zero company and observation changes. Live sources can legitimately change; inspect every company event against both evidence sides rather than forcing a zero-change result.

## Sampling and bulk preparation

Download the public universe archive from [the company-universe resource](https://builderr.ai/signalpost-company-universe-2025.jsonl.gz). The sampling helper verifies its published archive and decompressed hashes and samples uniformly with a fixed seed:

```sh
uv run python scripts/sample_universe.py --universe downloads/universe.jsonl.gz --output out/batch100.jsonl --count 100 --seed 20261013
uv run python scripts/extract_bulk.py --bulk downloads/registry.csv --batch out/batch100.jsonl --output out/registry100.csv
```

Obtain the bulk snapshot from the [official registry CSV endpoint](https://data.brreg.no/enhetsregisteret/api/enheter/lastned/csv). The extractor accepts plain/gzip CSV and reports requested rows absent from the snapshot; the runner keeps those companies and uses live fallback. Snapshots, outputs and blobs are ignored locally and not distributed here.

## Latest measurements

### Evidence-checked synthesis, saved 300-company sources

Measured on 13 October 2026: exact saved registry/NAV HTTP statuses and bodies were replayed; accepted website claims/states and same-host archived pages were restored. No network or DNS requests and no model calls were made. This checks summary construction without claiming fresh website verification.

| Check | Result |
|---|---:|
| Ordered valid envelopes with synthesis |300|
| Unhandled exceptions / synthesis-caused envelope failures |0 / 0|
| What-it-does / scale / leadership coverage |99.667% / 100% / 99.667%|
| At least one unknown entry |100%|
| Incomplete-source companies with every required unknown listed |299 / 299|
| Retained sentences / cited / unverified / dropped |3256 / 3256 / 0 / 0|
| Registered activity / statutory purpose coverage |299 / 300; 292 / 300|
| Website self-description claims / companies |34 / 16|
| Template rerun with the same prior snapshot |Byte-identical; 0 company changes|
| Union output before / after synthesis |56.599 / 64.287 decimal KB/company|
| Saved-source preparation, synthesis, rerun and hash verification |201.687s|

The size comparison removes only synthesis from the same enriched union envelopes; source claims/evidence are otherwise identical. Union output mirrors synthesis in run and profile. The public verifier confirmed 7,105 available claims, 1,168 matching source blobs, all 3,256 summary sentences, identical rerun claim IDs and zero company/observation events. Fifteen mixed rendered examples are kept locally for review, outside the published tree. No one-employee company is supported in the sample; the small-firm example is labelled by its reported records instead. Template provider cost is $0. Live model execution was deliberately excluded; fake-provider tests verify valid frames, raw-number/missing-citation rejection, untrusted quoted instructions, timeout, caps and cache hits.

For reproducible summary checks with local inputs, run the same command twice with `--synthesis template` and the **same** `--previous` file, then compare run.synthesis. The offline unit suite exercises this without downloaded archives. Baseline first-observation wording is separately tested. Live source bytes can change and legitimately alter summaries.

The [100-company replay summary](../reports/smoke-100.md) and [summary JSON](../reports/smoke-100-report.json) measure current code on exact saved official source bodies, verify original supported IDs and zero rerun events. This is an offline reproducibility check.

Separate live measurements from 13 October 2026:

| Workload | Result |
|---|---|
|100 companies, registry + websites |100 valid envelopes,435 requests,25.766s; companyp50/p95 9.797/19.688s;48.029decimalKB/company;0 unhandled exceptions|
|300 companies, registry + websites |20 official websites (6.667%):14 exact visible orgnr,1 JSON-LD,5 signal proof; all20 reviewed,0 remaining doubtful;1517 requests,101.047s; companyp50/p95 39.734/76.188s;49.240KB/company; website request max6/company|
|300-company live refresh |0 company events,5 observation events;0 false company changes|
|300 companies, registry + NAV |377 feed pages,375764 updates,9537 active headers;2 name candidates,2 detail requests,2 indexed ads,1 verified subunit ad; hiring available1/not_available281/failed18;1281 total requests,234.672s;51.374KB/company|

NAV's 18 failed companies had no usable distinctive name; name-filtered negatives do not cover unknown trading names. Detail requests were0.006667/company, within the default300 cap. Exact saved-status/body NAV replay preserved every live claim ID and produced zero company/observation events on rerun. Website recall is a development goal; identity correctness and evidence checks remain publication gates.

These measurements are smoke/recall observations, not an official competition score or performance guarantee. Bodies, company-level envelopes and internal audit material are not included in the published reports.

## Live recall and bounded activity

The two 300-company checks used seeds 20261014/20261015, `--websites --hiring --public-activity --time-budget-seconds 2400`, and no model calls. The first refreshed against the latest saved snapshot; the second was a fresh baseline. The weaker registry-declared path is default-off after group-company ambiguities. Final reviewed populations: 24 website rows, one NAV match and 33 dated website items; zero doubtful rows remained and all available-claim stored hashes/spans verified.

| Metric | Saved sample | Fresh sample |
|---|---:|---:|
| Verified websites | 20 / 300 (6.67%) | 19 / 300 (6.33%) |
| Companies with social profiles | 12 | 13 |
| Companies with fresh exact-number ads | 1 | 0 |
| Companies with public activity, including registry dates | 33 | 31 |
| Website dated items / registry date events | 19 / 68 | 14 / 52 |
| HTTP / DNS resolver invocations | 2,202 / 2,042 | 2,190 / 1,995 |
| Total reported runtime | 348.843 s | 336.406 s |
| NAV feed pages / feed seconds | 378 / 194.703 s | 378 / 190.484 s |
| NAV feed complete | yes | yes |
| False company changes on saved-sample refresh | 0 | baseline |

The saved-sample refresh had four coverage observations and zero company events. All runs had zero unhandled exceptions and no deadline hits. A complete header feed does not imply complete candidate details: ranked caps leave affected companies failed, never checked-negative. DNS counts include preflight and pinned connection resolutions, not just guessed-domain checks. Registry dates and website updates are reported separately so discovery coverage is not overstated.

## Profile site verification

Offline site tests cover all envelope shapes, membership, escaped untrusted content, safe links, evidence completeness, citation anchors, deterministic bytes and isolated template errors. The saved 300-company generation produces 302 pages; profiles must stay below 250 KB. Inspect index, BRANDO, a borettslag and compare at 1280 and 375 px, including file:// initialization, pagination, diacritics search, source toggles and overflow. Use installed browsers only; no browser dependency is required. Light/dark state chips include words, inputs have labels, toggles expose aria-expanded, and keyboard focus is visible. Browser QA supplements the offline suite; it is not a complete accessibility certification.
