# R5 fixed 100-company baseline

This directory freezes the comparison cohort and current-code measurement for revision R5. Application code and tests are unchanged. Source commit: `7eb9bba21d4225d0008d22c112d0d5a0abe9a38e`.

## Inputs and commands

- `companies.jsonl`: uniform sample of 100 companies from the hash-checked 411,160-company public universe, using the existing `scripts/sample_universe.py` and seed **20261017**. SHA-256: `7d59169d3fd274ec576dca84430beac887b4a1cf06697e20ab7e875420673686`.
- `registry100.csv`: all 100 matching rows extracted with the existing `scripts/extract_bulk.py` from the local registry snapshot downloaded on 13 October 2026. This is a frozen registry cache, not current live verification of identity fields. SHA-256: `bd244f0fe6ad92bfcadcbce9ba545863c0ca0afa8b9b5b4c5e3425830a63186d`.
- `settings.json`: exact sampling/extraction commands, source paths and hashes, source commit, Python version, environment overrides and every resolved runner setting.
- `run.ps1`: exact measured run command, executed from the repository root. It refuses an existing output directory. Paid search and model calls are disabled. Requests are capped at 2,000 and total run time at 2,400 seconds.

The baseline uses an empty runtime state with no previous envelopes or copied runtime responses. The unchanged shipped NAV index remains subject to its default 21-day age limit; on 12 November 2026 it is stale, so the current code selects full-feed fallback. No index freshness override or rebuild was applied. The old smoke-100 measurement used a fresh index and is not the baseline for R5.

## Results and verification

The run exited zero with 100 ordered envelopes, 6,907 available facts, 872 HTTP attempts and $0 provider cost. Runner runtime was 260.954 seconds; whole-command wall time was 265.561 seconds. The independent verifier checked 382 stored source bodies and 817 cited sentences, with zero unsupported synthesis values. The site generated all 100 company pages.

Source coverage is incomplete: accounts failed for 1 company, websites for 23 (plus 1 blocked and 6 ambiguous), hiring for 11, and activity for 32. The NAV fallback completed 357 feed pages, but 11 company scopes remain incomplete. These are retained baseline outcomes, not silently converted to absence. There are available activity facts for 25 companies, while only 16 have an available aggregate activity section; partial positives survive incomplete source checks.

- `table.md`: requested count table and all six section states.
- `counts.json`: the same counts with exact metric definitions, per-company counts/states, identity-level breakdown and hashes of the retained full outputs.
- `report.json`: original runner report, including HTTP attempts, source failures, budgets, NAV diagnostics and provider cost.
- `execution.json`: UTC run timestamps, whole-command wall time and exit code.
- `verification.json`: existing `scripts/verify_output.py` checks of all 100 ordered envelopes, schema, evidence hashes, verbatim spans and synthesis citations.
- `test-reruns.md`: the three isolated test results and the unchanged-timeout decision.

Raw source bodies, envelopes, projected profiles and the generated site remain local under `.data/r5/baseline-run/`; they are not committed. Their output hashes are recorded in `counts.json`. The baseline commit contains only this directory.

The table counts available source claims, not placeholders or synthesis sentences. Locations count `subunits.unit.*` records rather than their detail fields. Activity companies/claims include all available `activity` claims, even when another activity source is incomplete. Website companies follow the current accepted `official_website` publication policy; proof levels are recorded separately. Zero available claims in a failed or blocked section does not establish source absence.

For every later feature, reuse these exact company and registry input bytes, run with fresh state and matching settings, and compare against `counts.json`. Preserve the baseline output directory and give each comparison its own output paths/run ID. Live source content and availability can change; retain acquisition dates and source-state differences when interpreting deltas.

Registry data attribution: Bronnoysundregistrene, NLOD 2.0. Other sources retain the access and reuse policies documented in `docs/SOURCES.md`.
