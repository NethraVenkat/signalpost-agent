# Signalpost Revision 4 — local site gates

**Local status: passed with the user-authorized network exception.** Branch `ux/r4` is based on submitted `c28b580` (`v1.1.1`). No push, merge, tag, email, or remote smoke was performed. The final branch SHA is the commit containing this report; obtain it with `git rev-parse ux/r4`. Remote CI and clean-clone smoke remain pending until the branch is pushed by the user.

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

The default 1,000 run did **not** literally reach 28,726 available identity IDs. Its acceptance is limited to the exact network-loss condition the user specified. Remote CI and clean-clone/100-company smoke are unrun and require the user to push first.

## User-controlled release steps, after push and remote gates

These are review commands, **not actions performed here**. After pushing `ux/r4`, wait for CI green and run `uv sync --frozen` plus the README 100-company command from a clean GitHub clone. If those pass, the release can fast-forward `main` from `c28b580` to the branch SHA and tag `v1.1.2`:

```powershell
$r4Sha = git rev-parse ux/r4
git diff --exit-code c28b580 $r4Sha -- src/signalpost/sources src/signalpost/web src/signalpost/runner.py src/signalpost/cli.py pyproject.toml uv.lock
git switch main
git merge-base --is-ancestor c28b580 $r4Sha
git merge --ff-only $r4Sha
git tag v1.1.2 $r4Sha
```

Revision email draft for the existing thread:

> Subject: Re: Signalpost revision
>
> Revision 4, v1.1.2, replaces c28b580. The site now shows recent activity when verified events are present, supports four-company comparison, explains unknown data, and presents registry publication time and evidence more clearly. The fixed 50-company site audit and local test suite passed. The 1,000-company gate was accepted under the agreed network exception for 827248592. The release SHA is the tagged `ux/r4` commit.
