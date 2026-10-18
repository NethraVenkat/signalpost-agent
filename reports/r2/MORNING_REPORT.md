# Revision 2 — ship frozen 27a3bb0 with the accepted FILMTEK issue

Recorded 2026-10-18T09:38:39+05:30. **Tested code SHA: `27a3bb0cc2e4a9cf3802da6eaaec761da623a5c9`.** Branch `revision/r2`; a docs-only evidence commit follows that source SHA. Its exact final SHA is supplied in the handoff. Main and v1.0.0 remain `3944c89`; v1.1.0 has not been tagged and no email has been sent.

## Verdict and scope

**Ready for your merge/tag under your latest release criteria, with a known single-company refresh instability.** The later FILMTEK deterministic fix is excluded. It and its later validation are preserved locally on `archive/r2-post-filmtek-356fb1c`. Revision 3 has not started and must wait until you confirm the revision email was sent.

No source, dependency or test changes were made on top of `27a3bb0`. This release retains R2's faster bulk preparation, evidence-localization/auditor hardening, availability recovery classification, five-area cited profiles, offline search/filter/compare, broader cited summaries and the previously implemented exact-proof external discovery/branch labels. It does not publish unverified offline jobs, weaken identity proof, scrape social platforms or enable paid search/models.

## Verified numbers

Same 1,000-company cohort; companies with ≥1 available claim / facts:

| Family | v1.0.0 | Frozen R2 |
|---|---:|---:|
| Accepted official website | 58 / 58 | 61 / 61 |
| Hiring | 6 / 13 | 6 / 13 |
| Dated activity | 7 / 44 | 9 / 55 |
| Company-site social profiles | 39 / 83 | 41 / 89 |

Available claims **69,447 → 69,479**. Frozen R2 websites comprise 47 VERIFIED and 14 legacy HIGH. These live sample counts are not organiser recall scores or a controlled attribution of coverage improvements.

| Capacity run | End-to-end wall s | HTTP attempts | Envelopes | Identity IDs |
|---|---:|---:|---:|---:|
| normal | 168.26 | 5452 | 1,000 | 28,726 |
| 30 | 17.48 | 388 | 1,000 | 28,726 |
| 120 | 57.10 | 1867 | 1,000 | 28,726 |
| 600 | 187.16 | 5344 | 1,000 | 28,726 |
| req3000 | 136.34 | 3000 | 1,000 | 28,726 |
| nationwide30 | 19.15 | 77 | 1,000 | 28,726 |
| nationwide-normal | 237.64 | 4830 | 1,000 | 28,726 |

Every run exited 0, emitted 1,000 profiles, preserved exact input order, validated schemas and retained every one of the 28,726 baseline identity IDs. Declared time + 5 s and request limits passed, including nationwide-file 30 seconds. These are measurements at `27a3bb0`; no later-source measurements are relabelled here. Normal pipeline runtime was 152.208 s; end-to-end wall was 168.26 s, leaving 93.0% of the declared 2,400 s unused. Normal company p50/p95 were 69.073/106.803 s; sampled peak process-tree RSS 1273.2 MiB. Company durations overlap; RSS sampling can miss peaks/double-count shared pages. No public numeric official RAM/CPU/time cap is known.

## Gates and explicit exception

| Check | Actual result |
|---|---|
| Suite at frozen source | PASS: 497 tests, 72.14 s; [provenance](full-suite.json) |
| Seven capacity runs | PASS as above; [metrics](capacity-gates.json) |
| Cold 1,000 comparison | 9 lost / 41 added / 0 duplicates; each loss classified below, not silently declared zero |
| Retained-state refresh | **Known issue: 1 lost / 0 duplicates / 6 material events**, all FILMTEK; 7 added and 175 availability observations |
| 24-company comparison | PASS: exact 24-row order; 1,231 available claims; 0 lost/added/duplicate IDs |
| Envelope schema | PASS; no model change from v1.0.0 |
| Stored-source audit | PASS: 69,479 reviewed/correct; zero incorrect, unsupported, unverifiable or wrong-company flags |
| Independent ownership reopening | PASS: all 4 new website claims plus 20 others, zero mismatches/unresolved; additional exact subunit-site check |
| Exact source CI | PASS: [GitHub Actions](https://github.com/NethraVenkat/signalpost-agent/actions/runs/39095848518) |
| Clean remote clone + frozen install + README production command | PASS: exact source SHA, fresh Python 3.12 environment; 100 complete envelopes/profiles in order; site built; zero unverified synthesis values |

The old zero-loss/zero-material refresh gate is **not met**. Its single-company selection instability is accepted explicitly by your latest instruction, not converted into a factual change or a passing result. No blocking regression publishing wrong or unsupported facts was found in this scope; this is limited assurance, not a universal factual certification.

## Each of the nine cold losses

[Per-ID evidence and classification](cold-nine-review.json) contains exact claim IDs, old/current source hashes, locators and company-specific acquisition attempts:

- **Two IDs, org 963070276:** `roles.role.b6ffd901f45c686b19952ea4.0` and `roles.detail.b6ffd901f45c686b19952ea4.0.order`. Live-source variance: the old BRREG body contains a DAGL group; the new body removes it while retaining STYR. Registry extraction is unchanged.
- **One ID, org 913300564:** `subunits.unit.913309472`. Live-source variance: BRREG changes that unit's NACE `62.200` to `64.323`; both source hashes and values are retained.
- **Six IDs, org 988330752:** `official_website`, both `website_description.*.fb53b933d9b051d1`, `social_profile.bf7baa658b98e6deb5b3`, `contact.email.95630f353b39561b8b2e`, `public_brand`. Acquisition variance: the old baseline obtained the branch site; the cold run ended that company's unchanged website allowance during redirects/robots work before obtaining its final page. A same-hash page fetched for another organisation was not counted as successful acquisition for FILMTEK. No stale facts were reinserted.

## Known FILMTEK issue — not wrong-company publication

The cold run selected registry-declared `www.filmtek.no` under legacy HIGH corroboration. Refresh instead selected exact-number-proven `www.audioped.no` through registered subunit `933248380`, causing one website-ID loss and six material classifications. This is a known single-company main-versus-subunit selection instability; it is not evidence that the company actually changed sites.

Independent reopening confirmed the main site's legal-name/address corroboration and the subunit site's exact number. A separate live official BRREG lookup confirmed `933248380` has parent `988330752` and email `post@audioped.no`. The subunit site remains explicitly labelled as such; it is not represented as parent-number proof. [Ownership evidence](ownership-checks.json), [independent branch/parent check](filmtek-branch-check.json). Four of the 24 sampled sites use the legacy HIGH rule; 20 show exact numbers. HIGH remains corroboration, not exact-number verification.

The deterministic selection fix belongs to revision 3 only after your email-sent confirmation.

## Fresh remote smoke and artifacts

The actual [smoke report](smoke-report.json) is committed under `reports/r2/`; [provenance](smoke-provenance.json) records the exact cloned SHA, input/output hashes, frozen install, Python version, full command and exits. It used JSONL plus frozen BRREG CSV and all seven evaluator flags, with websites, hiring, public activity and site output enabled. Pipeline runtime **41.078 s**, **512 HTTP attempts**, **$0 provider fees**, 100 complete envelopes in exact order, 100 profiles and 102 site pages. Terminal complete is not all-source success; [section states](smoke-section-states.json) preserve failed/blocked/unavailable sources. Provider fees exclude hosting, compute and network.

[Cold comparison](cold-comparison.json), [refresh comparison](refresh-comparison.json), [24-company comparison](baseline24-comparison.json), [command exits](gate-commands.json), [audit summary and full-artifact hash](source-audit-summary.json), [source CI](source-ci.json). Full source bodies and item audit remain local under `out/r2-check-*`. Stored-source agreement is not independent current-live verification of all 69,479 facts. External coverage is limited; sources can time out or change; per-host contractual clearance is not certified by robots alone. [Source limits](sources.md).

## Your merge/tag commands

Confirm fetched `origin/revision/r2` equals the final handoff SHA. This ensures production code/tests/dependencies still equal the tested source:

```powershell
git fetch origin
git diff --exit-code 27a3bb0cc2e4a9cf3802da6eaaec761da623a5c9 origin/revision/r2 -- src scripts tests pyproject.toml uv.lock
git switch main
git pull --ff-only origin main
git merge --ff-only origin/revision/r2
git tag -a v1.1.0 -m "Signalpost revision 2"
git push origin main v1.1.0
```

## Unsent reply draft

Reply in your original thread to `submit@builderr.ai`, after your merge/tag:

> Revision 2, v1.1.0, replaces 3944c89.
>
> Please evaluate the final revision/r2 SHA supplied with this report. The tested code is 27a3bb0; the following commit contains release evidence only. R2 improves bulk/budget delivery, evidence handling and cited offline profiles with search/compare. On our retained 1,000-company cohort, website publishers increased 58→61, activity 7→9 and social profiles 39→41; hiring remains six. The normal run emitted all 1,000 envelopes in 168.26 s, with all 28,726 identity IDs. Source CI and the fresh remote-clone 100-company smoke passed; provider fees were $0.
>
> Known issue: FILMTEK may select its registry-declared main site in one run and its explicitly labelled registered-subunit site on refresh. Both relationships were checked; this produces one lost website ID and six material classifications, not a wrong-company finding. The deterministic selection fix is deferred to revision 3.
>
> Smoke report and full measured limitations: https://github.com/NethraVenkat/signalpost-agent/tree/revision/r2/reports/r2

No email has been sent. Await your explicit email-sent confirmation before starting `revision/r3`.
