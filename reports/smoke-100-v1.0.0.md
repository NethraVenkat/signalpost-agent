# 100-company smoke test — Signalpost v1.0.0

Run on 17 October 2026 (IST) from a **clean clone of the remote** (`https://github.com/NethraVenkat/signalpost-agent.git`), checked out at the code commit **`c7118e3cbfc36e01d0d6532eeab9eec595cf0731`** (GitHub Actions green on that commit: tests and live-20), with a fresh `.venv` created by the README install step only (`uv sync --frozen`, empty package cache). The commit that adds this report changes only files under `reports/`; the tag `v1.0.0` points at that documentation commit, so a report cannot contain its own SHA. Full machine-readable report: [smoke-100-v1.0.0.json](smoke-100-v1.0.0.json).

## Command (the README's one command, with its file names)

```sh
uv sync --frozen
uv run signalpost run --organisations batch.jsonl --bulk registry.csv --output envelopes.jsonl --profiles-output profiles.jsonl --report report.json --site-dir site --websites --hiring --public-activity
```

## Inputs
- `batch.jsonl`: 100 companies sampled uniformly from the 411,160-company public universe with `scripts/sample_universe.py --count 100 --seed 20261017` (SHA-256 `7d59169d3fd274ec576dca84430beac887b4a1cf06697e20ab7e875420673686`; universe archive and content hashes verified by the script).
- `registry.csv`: the 100 matching rows extracted with `scripts/extract_bulk.py` from the official BRREG bulk download captured on 17 October 2026 (100/100 found, SHA-256 `ba43cd709ad2debe7b6b8ead95bf39f5ebec260bda0561e511a44d594fd2c0d2`). This is a captured public subset, not an organiser-supplied frozen file.

## Result

| Measure | Value |
|---|---|
| Exit code | 0 |
| Envelopes / profiles | 100 / 100, input order exact |
| Wall time (whole command) | 59.6 s (pipeline `runtime_ms` 53,672) |
| HTTP requests | 505 (limit 2,000) |
| Envelope states | 100 complete |
| Deadline hits / unhandled exceptions | 0 / 0 |
| Schema validated; output verifier | yes; 100 lines, 6,850 claims, 378 source blobs verified, 791 synthesis sentences, 0 unverified values |
| Site | generated: 102 pages, largest profile 117,261 bytes |
| Provider cost | **$0.00** (LLM $0, search $0); network use only |

Available claims by family: identity 2,819 · accounts 2,154 · roles 1,268 · subunits 567 · activity 22 · website 20 (6,850 in total). Other claim availabilities: not_available 795 · not_applicable 67 · failed 47 · ambiguous 12 · blocked 2.

Section states (100 companies): identity 100 available · roles 100 available · subunits 70 available / 30 not_available · accounts 99 available / 1 failed · website 3 available / 67 not_available / 6 ambiguous / 23 failed / 1 blocked · hiring 100 not_available (declared NAV index and live forward feed complete, no matching ads) · activity runs only on verified sites (3 available).

Verified websites: 3 of 100; activity: 3 companies; hiring: 0. These are counts for this sample, not a recall estimate. `complete` describes processing; the failed website sections are visible in the section states and error codes.

The same command produced the same 505 requests and 6,850 claims in clean clones at `f4958e2`, `59f72d8` and `c7118e3`. The last two commits changed only configuration defaults that the CLI overrides, and tests.
