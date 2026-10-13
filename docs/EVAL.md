# Evaluation and smoke checks

Install pinned dependencies and run the offline suite:

```sh
uv sync --frozen
uv run pytest
```

The suite currently has 98 tests covering checksum/input membership, isolation/deadlines/budgets, missing versus reported zero, all envelope shapes, stored provenance, refresh/carry-forward, website proof/robots/SSRF/politeness, NAV exact matches/caps/ETags and independent output verification. Fixtures are small and local; no credentials or internet are required for these tests.

## Live 20-company registry smoke

```sh
uv run signalpost run --organisations tests/fixtures/ci20.jsonl --bulk tests/fixtures/ci20.csv --output out/smoke20.jsonl --report out/smoke20-report.json --expected-count 20 --time-budget-seconds 180
uv run python scripts/verify_output.py --first out/smoke20.jsonl --organisations tests/fixtures/ci20.jsonl --count 20 --state-dir state --report out/smoke20-report.json --require-clean
```

The committed public fixtures provide identity rows. Roles, subunits and accounts are freshly requested from official APIs. Websites and NAV are disabled for this short CI check. `--require-clean` requires complete checked sections, zero exceptions/deadlines/warnings, valid membership and output bounds. HTTP/network failure makes this gate fail rather than silently accepting a terminal output.

GitHub Actions has two Ubuntu jobs: tests and live-20. Both run frozen installation. Source failures can make the live job red independently of deterministic unit tests. Check the [Actions page](https://github.com/NethraVenkat/signalpost-agent/actions) for the actual results of the published revision.

## Output verification and refresh

The verifier checks schemas, exact input membership/order, available-claim evidence links, actual stored-body SHA-256 and verbatim spans. It requires the corresponding blobs, including archives for carried-forward claims. No network request is made by verification.

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
