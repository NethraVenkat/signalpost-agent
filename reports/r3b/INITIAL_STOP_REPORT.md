# Revision 3b ? DO NOT SHIP

**Stopped after the live 50-company gate failed. Revision 2 (`a704375`, v1.1.0) remains final.** Step 2 implementation SHA: `fd18394f726704e5c4386b474532262fb481bd0f`. Branch: `revision/r3b`, based directly on `a704375`. A documentation-only report commit follows; its final SHA is supplied in chat.

Stop recorded 2026-10-18T12:37:53+05:30, before the 16:30 IST hard stop. The user's instruction was: ?If anything fails or 16:30 is reached: stop; revision 2 stays final.? No remediation, further live gates, default enablement, push, merge, tag or email followed the failed pilot. Step 3 was not performed.

## Blocking failure ? code regression

Both new feed requests returned **HTTP 400**. The implementation serializes Python run timestamps with microseconds, for example `2026-10-18T07:04:40.345521Z`. BRREG requires the millisecond format `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'` for both `dato` and `updatedBefore`. The response explicitly identifies both parameters as invalid. This is an implementation error, **not a home-network loss or live-source change**.

No new registry activity claims were published by the live pilot. All 50 activity sections correctly became `failed`; previously obtained website activity facts remained present. All 50 envelopes were emitted in input order with exit 0, and all 1,433 pilot identity IDs were retained. Exit 0 does not pass the source-coverage gate.

The diagnosed fix would be to format query bounds with exactly three fractional digits and add a contract test, but it was **not applied**, honoring the stop instruction. The feature remains default **OFF** (`registry_changes=False`); `--registry-changes` explicitly enables this unshipped implementation, and `--no-registry-changes` disables it.

Evidence: [pilot request/results](pilot-results.json), [entity HTTP 400 body](http400-cf5511abe5fdf69f64e4c675ee330e0feb19e05a04706ea315c4a73f07e2daca.json), [subunit HTTP 400 body](http400-9b77c5e4c889b68ef4c6b1e6ba0ff91cbc10f0abc023354f30c01a42d03a6650.json). Those filenames are the original source-body SHA-256 values.

## Implemented scope, held locally

- Flag-controlled shared entity and subunit feeds, per-run acquisition, existing request/deadline/host policies, bounded 200-ID query chunks and checked pagination.
- Entity allowlist: business/postal address fields, `/navn`, `/kapital/belop`; add/replace retains the reported new value, remove reports field removal without inventing a new/old value.
- Subunit `Ny` / `Sletting` only for an exact parent mapping backed by retained source bytes and hash. `Ny` includes separately labelled `oppstartsdato` when present. Historical removed units absent from the current verified scope are skipped; the implementation does not infer their parent.
- No role notifications, annual accounts, NACE, employee metadata or bare updates. Publication timestamps are labelled ?registry publication time (not effective date)?; evidence effective dates remain unset.
- New facts carry source URL, event/field locator, retrieval time, source hash and extraction method. Newest registry change enters cited synthesis and Recent activity; existing source claims retain their values and IDs.

The source schema, existing website extraction/proof code and subunit registry extractor are unchanged from `a704375`. Default-on readiness is not established.

## Gates and actual evidence

| Gate | Outcome |
|---|---|
| Full suite plus new tests | 516 passed in 104.36 s during implementation. Subsequently added site-index/verifier changes received a focused 20-test pass; no final full-suite rerun after the failed live gate. |
| Saved R2 bodies replay | PASS within declared replay scope: 1,000 saved envelopes, 69,479 available source facts retained, 4,114 bodies hash-checked, zero lost available R2 fact IDs / changed existing values; 24 new offline registry claims independently matched to source, zero wrong-company findings. |
| Live 50 pilot | **FAIL: new code sends invalid timestamp precision; both feeds HTTP 400; zero new registry claims.** |
| 20 new live activity claims checked | NOT SATISFIED: no new live claims existed. Offline 24-claim checks are not substituted for this gate. |
| Forced-failure 100-company run | Unit integration test PASS: 100/100 ordered schema-valid envelopes, identity available, activity failed under forced HTTP 503. Separate real-cohort CLI fault run NOT RUN. |
| Default 1,000-company run / 28,726 identity IDs | NOT RUN after failed pilot. The offline 1,000 snapshot replay is not a default production run. |
| 24-company baseline | NOT RUN after failed pilot. |
| Push / CI / clean remote clone / frozen install / 100 smoke | NOT RUN. Branch remains local. |
| Wrong-company new facts | 24 offline new claims checked with zero mismatches. Live new registry claims: zero, so no live precision certification. |

[Offline replay evidence](offline-replay.json) records scope explicitly: production registry acquisition/extraction/merge and synthesis ran against saved source bytes and R2 envelope snapshots. Existing external discovery was not rerun because historical redirects lack retained response headers. All original source-body hashes were checked. This is not a claim of a complete HTTP transport replay. Source-backed available fact IDs were compared; availability placeholders are section-state outputs, not retained source facts.

The already-running replay completed during shutdown/diagnostic collection; no new gate was started after the live failure. Its local reproduction command is `$env:PYTHONPATH = (Get-Location).Path; .\.venv\Scripts\python.exe out/r3b-gates/replay.py`. Raw replay output/state are under `out/r3b-gates/replay-*`.

## Same-50 live coverage

The sample includes FILMTEK `988330752`, Equinor `923609016`, five known exact-proof website controls (`991853995`, `927094266`, `964398003`, `846870792`, `937893655`), then remaining input-order cohort members. R2 control uses code archived from `a704375`; both runs use the same 50 inputs, frozen bulk subset and existing defaults, with external families enabled. Only R3b adds `--registry-changes`.

| Companies with >=1 available fact | R2 | R3b |
|---|---:|---:|
| Website | 6 | 6 |
| Activity (existing website facts) | 3 | 3 |
| Social | 4 | 5 |
| Jobs | 0 | 0 |
| New registry activity | 0 | 0 |
| Envelopes in input order | 50 | 50 |
| Identity claim IDs | 1,433 | 1,433 |
| HTTP requests | 297 | 299 |
| Pipeline runtime | 38.083 s | 32.126 s |

These availability counts do not override failed activity section states. The 1,000-company live coverage comparison is unavailable because that gate was not run.

Five lost available IDs and six added IDs are all FILMTEK website-family claims. R2 accepted `www.filmtek.no` by its existing HIGH rule after the audioped candidate exhausted its allowance; R3b obtained `www.audioped.no`, exact registered subunit `933248380`, and selected it by the unchanged R2 policy. This is acquisition/budget variance exposing R2's already disclosed main/subunit selection instability, not a change to company identity or a new website-selection implementation. The extra social profile is linked to that selected subunit site. The source code for website collection/proof is byte-for-byte unchanged, and the new feed runs after website research. This attribution does not certify every live website fact; fresh reopening was not continued after the blocking gate failure. [Per-ID comparison and acquisition errors](pilot-diff.json).

## Step 1 and known risks

The earlier [Step 1 smoke report](STEP1_REPORT.md) is preserved separately. It found 121 entity events across 20 companies, 44 with details; the conservative address/capital filter covered 4 events across 3 companies. Mapped subunits had 36 events across 13 companies. Roles lacked named role-change details and were excluded. Earliest observed history was April 2018 for entity/subunit feeds and March 2022 for roles; these are observations, not retention guarantees.

**Registry change events may not count as public activity in Builderr's pool.** Deleted workplaces absent from exact verified scope are abstentions. Query pagination and wrong-company unit cases pass, but tests missed the live timestamp serialization contract. Gate coverage remains incomplete, so there is no SHIP SHA, merge/tag instruction or revision email draft. Do not merge or tag this candidate.
