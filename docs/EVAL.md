# Evaluation and smoke checks

Install pinned dependencies and run the offline suite:

```sh
uv sync --frozen
uv run pytest
```

The offline suite covers input membership and multiplicity, isolation/deadlines/budgets, missing versus reported zero, all envelope shapes, stored provenance, refresh/carry-forward, website proof/robots/SSRF/politeness, NAV exact matches/caps/ETags, output verification, synthesis citations/values/counts and provider fallback. Fixtures are small and local; no credentials or internet are required for these tests.

## Release resource defaults

The default time budget is 2,400 seconds; `--deadline-fraction 0.85` stops source work at 2,040 seconds. `--max-requests` derives 20 HTTP requests per unique normalized input identifier; duplicates share requests. Set either flag explicitly to override it. Workers default to 64, registry host concurrency to 10 and request timeout to 10 seconds. Website fetching defaults to 6 requests plus bounded supporting work within a total cap of 9 per company, 8 candidate DNS checks, 8-second requests, one-second domain politeness and two requests in flight per domain. Override the website caps with `--website-request-cap` and `--website-total-request-cap`; `--no-dns-precheck` disables candidate prechecks.

NAV starts before website work on a separate connection pool. Defaults: 512 header pages, 185-day lookback, 8 detail workers, 30-second request timeout, max(300, ceil(unique companies / 2)) detail attempts including retries, and a total time cap of min(600 seconds, 35% of the run budget). Override with `--nav-max-pages`, `--nav-lookback-days`, `--nav-concurrency`, `--nav-request-timeout`, `--nav-max-details` and `--nav-time-cap-seconds`. A partial index always remains failed rather than checked-negative. Reports include `feed_complete`, pages, feed seconds and seconds per page.

The measured 1,000-company run used 488.679 seconds wall time and 5,975 HTTP requests. Against the release defaults of 2,400 seconds and 20,000 requests, this leaves 79.64% time and 70.13% request headroom (76.05% before the source watchdog). This is a measurement, not a guarantee about an unknown official budget. Output defaults to 64 MiB (`--max-output-mb`); the union run reduced one large company to explicit output-limit failures. Contract output avoids the redundant reference profile. Source failure, exhausted budgets and optional site failures preserve complete envelopes and exit zero; inspect the report and verifier for success.

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
| What-it-does / scale / leadership coverage |100% / 100% / 99.667%|
| At least one unknown entry |100%|
| Incomplete-source companies with every required unknown listed |299 / 299|
| Retained sentences / cited / unverified / dropped |2356 / 2356 / 0 / 0|
| Registered activity / statutory purpose coverage |299 / 300; 292 / 300|
| Website self-description claims / companies |34 / 16|
| Template rerun with the same prior snapshot |Byte-identical; 0 company changes|
| Union output before / after synthesis |56.598 / 64.312 decimal KB/company|
| Saved-source preparation, synthesis, rerun and hash verification |163.594s|

The size comparison removes only synthesis from the same enriched union envelopes; source claims/evidence are otherwise identical. Union output mirrors synthesis in run and profile. The public verifier confirmed 7,105 available claims, 1,168 matching source blobs, all 2,356 summary sentences, identical rerun claim IDs and zero company/observation events. Fifteen mixed rendered examples are kept locally for review, outside the published tree. No one-employee company is supported in the sample; the small-firm example is labelled by its reported records instead. Template provider cost is $0. Live model execution was deliberately excluded; fake-provider tests verify valid frames, raw-number/missing-citation rejection, untrusted quoted instructions, timeout, caps and cache hits.

For reproducible summary checks with local inputs, run the same command twice with `--synthesis template` and the **same** `--previous` file, then compare run.synthesis. The offline unit suite exercises this without downloaded archives. Baseline first-observation wording is separately tested. Live source bytes can change and legitimately alter summaries.

The [live 100-company smoke summary](../reports/smoke-100.md) and [machine report](../reports/smoke-100-report.json) describe the fresh release check. Raw envelopes and source bodies are not published.

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

## Scale and external compatibility

The 1,000-company run took 488.679 seconds wall / 483.469 seconds reported, 5,975 HTTP requests and 6,770 DNS resolver invocations. The rerun took 479.360 seconds wall, with zero company changes and 34 observations. Both read 378 NAV pages completely: 191.297 and 234.141 feed seconds, with total NAV times 419.922 and 460.422 seconds. Detail caps remain separate from header completeness. The offline regenerated site is 53.515 MB, largest profile 73.440 KB, with exact evidence metadata stored once per response in per-company data scripts. The 64 MiB union envelope ceiling reduced one large company to explicit output-limit failures in both runs; contract output avoids the redundant profile.

Compatibility tests cover ten input encodings across union, contract and reference output, including extra keys, numeric identifiers, BOM/CRLF, duplicates and invalid records. Output order and repeated envelopes are independently verified. Eleven offline fault drills cover network, token, partial feed, storage, previous-input and budget failures. A read-only external starter-kit proxy scorer did not parse the canonical evidence list: it expects a legacy dictionary and raises AttributeError. No official score is claimed and final evaluator shape acceptance remains an open review risk.

The final contract release check preserved 1,000 ordered valid envelopes without any output-limit reduction under the unchanged 64 MiB ceiling. It used 5,980 HTTP requests, 6,800 DNS invocations and 494.094 reported seconds (company p50/p95 478.421/478.453 seconds). Header feed: 378 pages, 239.968 feed seconds / 478.406 total NAV seconds, feed_complete true, 0.635 seconds/page. All 25,038 supported claims, 3,866 stored bodies and 8,092 cited sentences passed independent verification; zero exceptions or deadline hits. Coverage: 59 websites, 33 social-profile companies, two fresh exact-company ad companies and 118 public-activity companies. Output is 56.213 MB; site is 53.649 MB / 77.686 KB largest profile. Time/request headroom against 2,400 seconds/20,000 requests is 79.41%/70.10%. Four accounts and 301 hiring sections remain incomplete; the 500-detail cap is not an exhaustive national ad search.
