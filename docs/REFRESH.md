# Refresh and previous snapshots

Synthesis is derived output and does not create company changes. A baseline includes the first-observation sentence; refreshed runs compare with their supplied prior snapshot. Identical claims, events, source states and baseline/refresh context produce identical templates. To test synthesis idempotency, supply the same prior snapshot to both runs. Retrieval timestamps do not affect summary text. Recent-registration inclusion is evaluated against the observation date and can age out across days.

Supply `--previous prior.jsonl` in any supported envelope shape. Without it, each company is a baseline with empty changes. Previous rows are validated independently; malformed rows become warnings. Invalid current organisation numbers cannot inherit company facts.

Claim IDs are deterministic hashes of organisation, field, normalized source value, availability and original reporting metadata. Evidence IDs retain source URL/hash/locator/extractor identity and exclude retrieval time. Case, whitespace and collection ordering are normalized. Address abbreviations are not rewritten.

`changes[]` contains supported company value changes only when the section was successfully checked in both runs: available, not_available or not_applicable. Types are added, removed, changed and closed_job; changes carry both values/evidence-ID sets, source hashes, materiality and observation times. A role replacement is one material family event. Registered-website changes are minor. Website comparison uses registrable domain; proof strength, WWW, HTTPS and proof-page changes alone do not indicate a company move.

Any transition involving failed, blocked, ambiguous or a previously absent section is an observation in `run.refresh.observation_changes`, with section, previous/current state and reason. Identical uncertain states with identical supported values emit no observation. Disabled opt-in families do not establish removals.

Uncertain sections retain prior supported claims missing from the current check, marked carried_forward with original evidence. Newly verified claims take precedence. Older evidence metadata remains available to support both sides of changes. A fresh state directory does not require historical bodies or authorize new domains from old evidence. `--state-dir` stores bodies/cache; it does not implicitly select a prior run.

Known inactive/deleted/expired jobs are not carried forward. A missing ad from complete company candidate coverage can emit closed_job; partial coverage cannot prove closure. A previously supported active ad whose header no longer matches a known name remains uncertain. Historical carried-forward jobs must not be displayed as freshly verified active listings.

Accounts comparison includes the value, fiscal year/period, currency, account type and original source unit. Empirical whole-NOK annotation alone changes neither company-change meaning nor legacy claim identity.

Fixed-source reruns must produce identical claim IDs, zero company changes and zero observation changes. Live APIs and websites can legitimately change between requests; reproducibility of the extraction does not imply immutable internet content.

Dated website items use stable URL fields. New or removed items from successful activity checks are minor changes. Failed/blocked checks emit observations and can retain prior support, clearly marked as historical. First enablement of activity has no previous checked section and is an observation. Newly introduced founding/VAT fields absent from older extractors are coverage observations, not inferred historical company events. Registry presentation dates are included only within 24 calendar months of the observation date; their ageing does not create source-claim changes.

Fresh website proof does not establish that every historical supporting page was checked. Missing contact/social/description claims whose company-owned source URLs were not successfully fetched are carried forward with original evidence and a page-coverage observation. A checked page can still establish removal. Description comparison excludes website proof IDs/levels, which describe verification rather than a changed self-description.


## Measured refresh correctness

The offline CI replay uses saved seed-20261113 receipts for DIGITALIQ AS (918266917), with exact body SHA-256 validation and production extraction, refresh, verification, synthesis and site code. Transport has no network fallback. Seven separately planted source changes cover employee count, business address, a new accounts year, legal name, a proven new subunit, a NAV ad made inactive, and a verified website returning 404. Every changed snapshot is replayed twice.

Measured result: 7/7 causal interventions detected (recall 100%); 40 supported field events and zero unexpected field events (event precision 100%). The unchanged replay emitted zero changes (false-change rate 0); identical-snapshot repetition emitted zero changes, including all seven changed scenarios. This is a bounded one-company test, not an estimate of population accuracy.

Timeout replay preserved 112 prior supported claims with their original evidence IDs and observation times, copied immutable receipt bodies, and visible stale markers. It emitted zero company changes. Unknown source routes fail rather than use the network. A synthetic empty NAV forward-tail scaffold is explicitly identified: saved ad detail supplies the job fact; this does not test full-feed discovery coverage.

Reproduce with `python scripts/refresh_proof_harness.py <new-work-directory>` or the offline-only CI test `pytest tests/test_refresh_proof_harness.py`. The seven CLI flags select inputs/outputs; the harness injects prior output and fixed clock programmatically. Live refresh requires the additional, explicit `--previous` flag. Machine-readable offline and live measurements, exact commands, hashes and coverage observations are retained in `reports/r5/stageE/`.


A live Stage E check exposed publisher timestamp-format instability: offsets and UTC representations of the same instant produced 620 false registry event changes and 25 false coverage observations. Refresh comparison now normalizes only timezone-aware registry publication timestamps to the same UTC instant and compares uncertain-section values by field/semantic meaning. Original publisher timestamps and receipts are preserved; genuinely different instants, fields and labels still differ, and naive dates acquire no inferred timezone.

Replaying the exact saved 100-company before/after pair offline produced zero changes and zero observations after this fix, verified all 1202 registry events with zero unsupported values, and generated a site whose largest profile was 249314 bytes under the unchanged 250000-byte gate. This is a second, nontrivial regression measurement alongside the seven planted source interventions; source response bytes were not edited. Reproduce with `python reports/r5/stageE/replay_saved_live_pair.py <new-work-directory>` using the retained local runs.

Live frozen-100 measurement (Stage E): 0 material and 0 minor company changes, separately from 0 coverage observations; 684 HTTP and 368.449s wall, zero unsupported values and $0. See `reports/r5/stageE/live_refresh/results.json` for evidence and exact categories. This observational run does not provide a known-ground-truth precision estimate.
