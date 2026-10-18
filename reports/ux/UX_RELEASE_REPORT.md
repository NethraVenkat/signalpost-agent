# Signalpost Revision 4 — local site gates

**Release candidate `fa23555abf0944353029706dc9ef429d6911fed4` (`ux/r4`): local gates passed with the user-authorized network exception; GitHub CI is green per the user; the clean GitHub clone and 100-company smoke passed.** Branch `ux/r4` is based on submitted `c28b580` (`v1.1.1`). The user pushed `ux/r4`; this follow-up performed no push, merge, tag or email. This report update is intentionally local and uncommitted, so it does not change the tested/pushed release SHA.

## Changes and scorecard

The five approved site gaps were implemented in the requested order, one gap commit each:

| Gap | Commit | Result |
|---|---|---|
| G1 | `81fba67` | Dashboard recent activity is populated from existing dated claims; the empty message and scoped no-change wording no longer contradict available events. |
| G6 | `a6b561b` | Profile disclosure controls meet the 40 px mobile hit-area target. |
| G2 | `4d6e6ea` | Four comparison companies render and survive URL reload, with five area rows. |
| G5 | `bed477e` | Registry publication time uses the exact label `registry publication time (not effective date)`; evidence shows provider names and compare missing cells show reasons. |
| G3 | `0e112dc` | A labelled unknowns block shows each statement's state and reason, with a link to the relevant source-status entry. The older publication-label test was updated in this commit to match G5. |

The Phase 1 [audit](UX_AUDIT.md) recorded **3 PASS, 5 PARTIAL, 2 FAIL**. The fixed-data, offline after-audit records **9 PASS, 1 PARTIAL, 0 FAIL**:

| Check | Before → after | After evidence |
|---|---|---|
| UX-1 Find | PASS → PASS | Name/number search, keyboard shortcut and directory filters work in [DOM audit](dom-after.json). |
| UX-2 Compare | FAIL → PASS | Four cards and four selectors survive reload at 1440/375/320 with no overflow; [DOM audit](dom-after.json). |
| UX-3 Verify | PARTIAL → PASS | Nine sampled evidence types open with source, retrieval, method, hash and excerpt; exact publication label and 16 compare reasons checked in [deep audit](deep-after.json). |
| UX-4 Desktop | PASS → PASS | All nine page cases load without console or page errors; [DOM audit](dom-after.json). |
| UX-5 Mobile | PARTIAL → PASS | No document overflow, sampled contrast below 4.5, or sampled 375 px tap target below 40 px; [DOM](dom-after.json) and [accessibility checks](a11y-after.json). This is a sample, not a full WCAG certification. |
| SYN-1 What it does | PASS → PASS | Existing cited purpose and industry prose is unchanged. |
| SYN-2 What changed | PARTIAL → PASS | Fifteen index records have recent events, matching the dashboard KPI; newest events appear in the list and empty wording is scoped; [deep audit](deep-after.json). |
| SYN-3 What is unknown | PARTIAL → PASS | Sampled Equinor, registry and sparse profiles have labelled unknown statements, reasons and source-status links; [DOM audit](dom-after.json). |
| SYN-4 Every sentence cited | PARTIAL → PARTIAL | All 420 factual synthesis sentences have resolvable claim citations. The 257 state-backed unknown statements now link to their source-status entries, but still have no direct claim IDs; [sentence audit](synthesis-checks.json). |
| SYN-5 No unsupported claims | FAIL → PASS | Dashboard no longer says there are no recent registry filings when its own index has activity; [deep audit](deep-after.json). |

The before/after browser artifacts are local at `screenshots/before/` and `screenshots/after/`, with their paths recorded in the JSON audits. The site works via `file://`; the audit blocked all non-file requests. G4 was explicitly not approved and no data-loading restructuring was done. The corrected official size gate is HTML ≤250 KB and no generated page or asset growth >10%, not an initial-load budget.

## Local gates

| Gate | Result |
|---|---|
| Full suite and new site tests | **PASS: 532 passed** after the final test assertion correction. |
| Guard diff from `c28b580` | **PASS:** changed paths are confined to `src/signalpost/site.py`, `src/signalpost/site_assets/*`, `tests/*` and `reports/ux/*`. The protected sources/web/runner/CLI/dependency diff is empty. |
| Fixed 50-company regeneration | **PASS:** `signalpost site --input reports/ux/sample/out/envelopes.jsonl --out reports/ux/sample/site-after` produced 49 company data scripts byte-identical to the before site; therefore their claim IDs and values are identical. The 50-envelope input SHA-256 is `827b6972d1f459cffc06dab0ebcd166050e844cf96c1d7f6a3abfbb732a8d4d4`. [Size and equality gate](site-gate.json). |
| HTML and growth limits | **PASS:** largest HTML 129,133 bytes; largest generated file growth 3.85%; no file exceeds 10%. The run-time-only `progress.json` is excluded from site-only regeneration comparison. [Site gate](site-gate.json). |
| Offline browser | **PASS:** 27 page/viewport cases at 1440/375/320, zero load/console/page/request errors, zero attempted external requests, zero document-level horizontal overflow; [DOM audit](dom-after.json). |
| Default 1,000 run | **ACCEPTED under the user's explicit exception:** first and retry each emitted 1,000 distinct ordered envelopes and 28,723 available identity IDs. The only three absent baseline IDs belong to `827248592` (`identity.legal_name`, `identity.organisation_form`, `identity.deleted`). This company is absent from the frozen CSV; both runs mark identity `failed`/`network_error`, with four BRREG `ConnectError` attempts and no HTTP status. The retry verifier passed: 1,000 schema-valid lines, 999 source blobs checked, zero unverified synthesis values. No third run was made. [Compact request and count evidence](default1000-gate.json); full local report: `gates/default1000-retry/report.json`. |

The default 1,000 run did **not** literally reach 28,726 available identity IDs. Its acceptance is limited to the exact network-loss condition the user specified.

## GitHub clone and final guard, 2026-10-18

GitHub `refs/heads/ux/r4` resolved to `fa23555abf0944353029706dc9ef429d6911fed4`. A fresh clone at `out/ux-r4-github-clone` had that exact HEAD and a clean starting status. Remote `main` remained `c28b580763e550aa1d74a8899edfd072a1b94148`; `v1.1.2` did not exist. `uv sync --frozen` installed the locked environment without changing `uv.lock` (a workspace-local uv cache was used because the default cache was inaccessible in the sandbox).

The README `signalpost run` command was run on the first 100 frozen cohort inputs, with the frozen `bulk1000.csv`, all three external flags, profiles, report and site enabled. It exited 0 in 49.718 s, emitted **100/100 ordered, schema-valid envelopes**, and generated an available **102-page site**. The largest HTML profile was 118,979 bytes. The independent schema/synthesis check validated 100 companies and all **817 synthesis sentences**, with 2,819 available identity IDs. The run made 514 requests and reported no run warnings or deadline hits. Section states accurately recorded one accounts, 23 website and 30 activity failures; this smoke confirms output and site integrity, not universal external-source availability.

From the clean clone, after copying the first 100 lines of the frozen `batch1000.jsonl` to `out/smoke100/batch.jsonl`, the command was:

```powershell
$env:UV_CACHE_DIR = Join-Path (Get-Location) '.uv-cache'
uv sync --frozen
uv run --frozen signalpost run --organisations out/smoke100/batch.jsonl --bulk C:\Users\Manish\Downloads\Signalpost-v5\out\capacity-inputs\bulk1000.csv --output out/smoke100/envelopes.jsonl --profiles-output out/smoke100/profiles.jsonl --report out/smoke100/report.json --site-dir out/smoke100/site --websites --hiring --public-activity --run-id ux-r4-github-smoke100 --expected-count 100
```

Local evidence remains under `out/ux-r4-github-clone/out/smoke100/`: input `batch.jsonl` SHA-256 `7d59169d3fd274ec576dca84430beac887b4a1cf06697e20ab7e875420673686`, `envelopes.jsonl` SHA-256 `8b094560db61643d0bd57b921e8836b573603f1d2191f4a9a20d23bdf60b5b10`, and `report.json` SHA-256 `ad951624bb010d5dc51e9671c3922dfe318be731f6dcca61bcaf2669c65261dd`. The clean-clone guard diff from `c28b580` had 29 changed paths, all within `src/signalpost/site.py`, `src/signalpost/site_assets/*`, `tests/*` or `reports/ux/*`. The exact protected-path diff command below exited 0 with no output.

## User-controlled merge, tag and push steps

These are **commands for the user, not actions performed here**. They assume CI remains green. The guards stop if the remote release candidate or `main` has moved:

```powershell
$r4Sha = 'fa23555abf0944353029706dc9ef429d6911fed4'
git fetch origin
if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }
if ((git rev-parse origin/ux/r4).Trim() -ne $r4Sha) { throw 'ux/r4 moved; review again' }
if ((git rev-parse origin/main).Trim() -ne 'c28b580763e550aa1d74a8899edfd072a1b94148') { throw 'main moved; review again' }
git diff --exit-code c28b580 $r4Sha -- src/signalpost/sources src/signalpost/web src/signalpost/runner.py src/signalpost/cli.py pyproject.toml uv.lock
if ($LASTEXITCODE -ne 0) { throw 'Protected path diff is not empty' }
git switch main
if ($LASTEXITCODE -ne 0) { throw 'Could not switch to main' }
git merge --ff-only origin/main
if ($LASTEXITCODE -ne 0) { throw 'Could not align local main with origin/main' }
git merge --ff-only $r4Sha
if ($LASTEXITCODE -ne 0) { throw 'Fast-forward merge failed' }
git tag -a v1.1.2 $r4Sha -m 'Signalpost v1.1.2'
if ($LASTEXITCODE -ne 0) { throw 'Tag creation failed' }
git push origin main
if ($LASTEXITCODE -ne 0) { throw 'Main push failed' }
git push origin refs/tags/v1.1.2
if ($LASTEXITCODE -ne 0) { throw 'Tag push failed' }
```

Revision email draft for the existing thread:

> Subject: Re: Signalpost revision
>
> Revision 4, v1.1.2, replaces c28b580. The site now shows recent activity when verified events are present, supports four-company comparison, explains unknown data, and presents registry publication time and evidence more clearly. The fixed 50-company audit, 532-test suite, GitHub CI and clean-clone 100-company smoke passed. The 1,000-company gate was accepted under the agreed network exception for 827248592. Release SHA: fa23555abf0944353029706dc9ef429d6911fed4.
