# Revision 3b - SHIP

**SHIP under the user's network-loss exception.** Tested default-on code: `a2e7b70fd4fe2ec1757eaf6c97c52a4249afdb85`, branch `revision/r3b`, based directly on revision 2 `a704375` (v1.1.0). All required gates passed for membership, identity, source correctness and code regression. Source coverage remained incomplete in some runs, as disclosed below. Gates completed at 13:45 IST on 2026-10-18, before the 16:30 hard stop. A documentation-only evidence commit follows; its final handoff SHA is supplied in chat. Main and tags remain untouched; no email was sent.

A transient GitHub DNS failure delayed the final-code push, and a connection reset interrupted the first final clone. The same code was subsequently pushed, passed CI, and passed a fresh clone/frozen-install/100-company smoke. These were network retries, not additional implementation fixes. [Failed clone evidence](retry/clone-network-failure.json), [log](retry/clone-network-failure.log).

The user authorized ONE timestamp fix and a retry after the [initial stopped attempt](INITIAL_STOP_REPORT.md). Commit `9d9d806` formats both BRREG query bounds as UTC with exactly three fractional digits, and adds contract/HTTP-400 tests. No second extraction or acquisition fix was made. Candidate gates then passed, including remote CI and a clean-clone smoke, before commit `a2e7b70` enabled the release default and updated package metadata to 1.1.1. The final default-on configuration was tested again.

## Scope and default

Registry activity is ON by default in CLI and Config; disable with `--no-registry-changes` / `Config(registry_changes=False)`. Historical R2 fixture runners explicitly opt out because their transport fixtures lack this feed.

- Entity `includeChanges=true`: only business/postal address, registered name and share-capital amount changes. Each claim retains the changed path and reported new value. Removal reports field removal without inventing values.
- Subunit `Ny` / `Sletting`: exact source-backed `overordnetEnhet` parent proof required. `Ny` includes separately labelled `oppstartsdato` when present. Historical removed units absent from the current verified mapping are skipped.
- Claims include BRREG URL, retrieval time, source hash, locator, extraction method and API timestamp labelled **registry publication time (not effective date)**. Effective dates remain unset. No roles, accounts-filing, NACE, employee-metadata notifications or bare updates.
- Checked pagination fails explicitly on incomplete/inconsistent pages. Error/timeout makes activity `failed`; verified partial facts can remain visible. The newest event enters cited synthesis and Recent activity.
- Step 3 was skipped. Existing website proof, identity rules, source policies, budgets and existing claim canonical values are unchanged.

## Same-50 decision gate: PASS

Same inputs include FILMTEK, Equinor and five known website controls. R2 ran from `git archive a704375`; both runs used the same frozen bulk subset and normal resource defaults. Only R3b added the registry flag.

| Companies with at least one available fact | R2 | R3b retry |
|---|---:|---:|
| Website | 1 | 1 |
| Activity | 0 | 11 |
| Social | 0 | 0 |
| Jobs | 0 | 0 |
| New registry activity | 0 | 11 |
| Envelopes in input order | 50 | 50 |

**11/50 gained registry activity; all 11 new claims matched the raw BRREG responses with zero mismatches.** This passes the user's threshold of at least five companies and every new claim (or 20) checked. No existing available pilot IDs were lost and no other new claims appeared. Checks cover exact company/parent proof, field/value, timestamp/date label, retrieval evidence and hashes. [Decision](retry/pilot-decision.json), [claim values and evidence](retry/pilot-claim-details.json), [raw audit bodies](retry/audit-bodies), [same inputs](retry/pilot50.jsonl).

The entity feed timed out; the subunit feed returned HTTP 200. All 50 activity sections correctly remained `failed` for incomplete coverage despite the 11 valid claims. This is a network acquisition loss, not all-source success. Subsequently, both feeds returned HTTP 200 in the 24-company baseline, which verified two address-field claims and one share-capital claim.

## Final default 1,000-company run

**1,000 ordered envelopes, exit 0, all 28,726 identity IDs retained.** No enable flag was supplied. Pipeline runtime 248.523 s; command wrapper 272.341 s; 5,511 HTTP attempts, no deadline hits or warnings. All 15 registry-feed requests, including pagination, returned HTTP 200.

| Companies / available facts | R2 saved baseline | R3b default |
|---|---:|---:|
| Website | 61 / 61 | 66 / 66 |
| Activity | 9 / 55 | 240 / 597 |
| Social | 41 / 89 | 44 / 96 |
| Jobs | 6 / 13 | 6 / 13 |
| Registry activity | 0 / 0 | 232 / 542 |

**All 542 new registry claims were independently matched to retained BRREG bytes with zero mismatches.** The output verifier checked 70,050 available claims, 3,888 source-body hashes and 8,365 synthesis sentences with zero unverified synthesis values. Site output: 1,000 profiles / 1,002 pages. Activity section states: 143 available, 483 not_available, 374 failed; valid facts in failed sections remain partial results. These counts are live observations, not an organiser recall score or controlled attribution of website/social gains. [Comparison and 542 checks](retry/default1000-comparison.json), [output verification](retry/default1000-verification.json), [command and runtime](retry/default1000-run.json).

Twelve existing available IDs were lost, all website-family: five for FILMTEK (988330752) reflect R2's existing main/subunit selection instability after different acquisition outcomes; seven for Infoss (998788870) follow a website timeout and unchanged budget exhaustion. Website code is byte-for-byte unchanged, and the new feed runs after website research. These are acquisition variance under the user's network exception, not a newly implemented website-selection change. No actual website change is asserted. [Every lost ID and errors](retry/default1000-lost-claims.json).

## Gates and provenance

| Gate | Result |
|---|---|
| Timestamp fix full suite | PASS: 523 tests, 106.74 s. Exact format tests cover both endpoints, offsets and whole seconds; HTTP 400 makes activity failed. [Record](retry/full-suite.json) |
| Final default-on full suite | PASS: 526 tests, 97.73 s, including default and explicit on/off switch. [Record](retry/default-full-suite.json) |
| Saved R2 bodies | PASS within declared scope: 1,000 envelopes, 69,479 available source facts retained, 4,114 bodies hash-checked, zero lost available IDs/changed values; 24 new offline claims matched source, zero wrong-company findings. [Evidence](offline-replay.json) |
| Live 50 decision | PASS: 11 companies gained, every one of 11 claims checked, zero mismatches. |
| Real-100 forced feed failure | PASS: 100/100 ordered schema-valid envelopes, exit 0, identity available in all 100, zero lost R2 identity IDs, all activity failed. Four feed attempts forced to HTTP 503. [Result](retry/fault100.json), [verification](retry/fault100-verification.json) |
| Default 1,000 final code | PASS as above; 28,726 identity IDs, all 542 registry claims source-checked. |
| 24-company baseline | PASS: all 1,231 existing available IDs retained; three new registry claims across two companies, all checked. 24 envelopes in order, no schema change. [Comparison](retry/baseline24-comparison.json), [verification](retry/baseline24-verification.json) |
| Candidate push/CI | PASS at `9d9d806`: [GitHub Actions](https://github.com/NethraVenkat/signalpost-agent/actions/runs/39107979614). |
| Candidate clean remote clone | PASS: fresh Python 3.12.15, frozen install, 100-company README command plus feature flag, 100 envelopes, 58 registry claims checked with zero mismatches. [Provenance](retry/candidate-smoke100.json) |
| Final default-on push / CI | PASS at `a2e7b70`: [GitHub Actions](https://github.com/NethraVenkat/signalpost-agent/actions/runs/39109704314). |
| Final default-on clean-clone 100 smoke | PASS for delivery/identity/evidence: exact `a2e7b70`, fresh Python 3.12.15, `uv sync --frozen`, README command without an enable flag, 100/100 envelopes, all identity available, 100 profiles / 102 pages, exit 0. Pipeline 69.891 s, 376 requests. Both feeds hit DNS failures: zero registry claims, all activity failed. [Provenance](retry/final-smoke100-retry.json), [section states and feed attempts](retry/final-smoke100-sections.json). |

The saved-body replay is production registry acquisition/extraction/merge/synthesis over retained R2 envelopes, not a complete historical external HTTP transport replay: redirect headers were unavailable. Availability placeholders are section-state outputs, not retained available source facts. The replay's declared scope is unchanged by the retry.

An earlier candidate 1,000 run (explicit feature flag) also preserved all identity IDs but lost 40,567 nonidentity IDs during widespread DNS/connection/read failures. Website/social/jobs/activity company coverage was zero; all activity sections failed. The later final default run above supersedes it for release measurements. Both outcomes are retained, not selectively omitted. [Earlier comparison and loss-artifact hash](retry/normal1000-comparison.json).

## Known limits

**Registry change events may not count as public activity in Builderr's pool.** Exact current-parent mapping misses historical removed workplaces. Available facts in failed activity sections do not imply full source coverage. FILMTEK's known R2 main/subunit selection instability remains. Provider fees are $0; no email has been sent.

Step 1 observed 121 entity events across 20 companies, 44 with details; its conservative address/capital filter covered four events across three companies. Mapped subunits had 36 events across 13 companies. Roles lacked named change detail and were excluded. Earliest observed entity/subunit history was April 2018; this is not a retention guarantee. [Step 1 report](STEP1_REPORT.md).

## Merge/tag commands for the user

Confirm `origin/revision/r3b` equals the final handoff SHA supplied in chat. The code diff must be empty before merging. These commands have **not** been run by the agent:

```powershell
git fetch origin
git diff --exit-code a2e7b70fd4fe2ec1757eaf6c97c52a4249afdb85 origin/revision/r3b -- src scripts tests pyproject.toml uv.lock
git switch main
git pull --ff-only origin main
git merge --ff-only origin/revision/r3b
git rev-parse HEAD
git tag -a v1.1.1 -m "Signalpost revision 3"
git push origin main v1.1.1
```

## Unsent revision email draft

Reply in the original thread to `submit@builderr.ai` after merging/tagging.

**Subject:** Re: Signalpost v1 Submission - Norwegian Company Research Agent: Revision 3, v1.1.1 (replaces a704375)

Revision 3 of 4: v1.1.1 replaces submitted revision 2 (`a704375`). The tested code is `a2e7b70fd4fe2ec1757eaf6c97c52a4249afdb85`; the following documentation-only handoff commit contains release evidence.

This narrow revision enables registry activity by default: named business/postal address, registered-name and share-capital changes, and new/removed workplaces with exact parent proof. Every event carries its BRREG source, retrieval time and hash; timestamps are labelled registry publication time, not effective date. The latest event is cited in the summary and Recent activity. `--no-registry-changes` disables the feature. No role notifications, bare updates or website-proof changes were added.

Validation: 526 tests passed. In the same-50 pilot, 11 companies gained registry activity and all 11 claims matched raw source responses. The default 1,000-company run emitted every envelope in order, retained all 28,726 identity IDs, and found 542 registry claims across 232 companies; all 542 were source-checked with zero mismatches. Total activity coverage was 240 companies / 597 facts versus R2's 9 / 55. The real-100 forced-failure test, 24-company baseline, exact-code CI and clean-clone/frozen-install 100-company smoke passed. Provider fees were $0.

Coverage is network-sensitive: the final clean-clone smoke had DNS failures on both new feeds, emitted all 100 envelopes with identity intact, and correctly marked activity failed. It produced no registry claims; the successful default 1,000 run supplies the coverage evidence. Twelve website-family IDs were lost to acquisition variance, including FILMTEK's existing main/subunit selection instability. Historical removed workplaces lacking current exact-parent proof are skipped. Registry change events may not count as public activity in Builderr's pool; these measurements are not an official recall score.

After `uv sync --frozen`, the README command for 100 inputs is:

```sh
uv run signalpost run --organisations batch.jsonl --bulk registry.csv --output envelopes.jsonl --profiles-output profiles.jsonl --report report.json --site-dir site --websites --hiring --public-activity --run-id signalpost-example --expected-count 100
```

Set `--expected-count` to the actual input count. Release evidence: https://github.com/NethraVenkat/signalpost-agent/tree/revision/r3b/reports/r3b
