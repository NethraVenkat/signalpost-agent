# Single fresh 500-company verification

**FAILED full gate: HTML site was not published.** No second live run was made.

Application commit: `f740933af530a9756f07c236a79bceae069eb862`; seed `20261125`.
Fresh clean clone, frozen installation, exactly seven CLI flags, expected count 500; no pytest in clone. Excluded 6,207 prior input numbers; overlap 0. Source universe contains 411,160 rows; eligible population 406,510. The bulk subset held 499 rows; `933762394` was retained for normal live lookup.

| Metric | Result |
|---|---:|
| Process wall / fixed budget | 1,516.75 / 2,100 seconds |
| Margin | 583.25 seconds |
| CLI exit / check_live_run exit | 0 / 1 |
| Run status | partial |
| Deadline hits | 0 |
| JSON envelopes / profiles / placeholders | 500 / 500 / 0 |
| Published HTML profiles | 0 |
| Largest reconstructed HTML | 262,692 bytes (not published) |
| Activity available / failed | 500 / 0 |
| Websites / social URLs | 36 / 24 |
| Signature/prokura: companies / claims | 0 / 0 |
| Brreg group relationships: companies / claims | 0 / 0 |
| Consolidated accounts: companies / claims | 5 / 336 |
| State aid: companies / claims | 33 / 205 |
| All available claims | 70,078 |
| Stage S claims: state aid / research / licences / inspections | 205 / 10 / 9 / 1 |
| Stage S total claims | 225 |
| State-aid data HTTP requests | 0 (dated licensed bulk extract) |
| HTTP attempts | 4,426 |
| Unsupported synthesis / briefing values, separate source check | 0 / 0 |
| Minimum sampled free disk | 17.11 GiB |
| Provider cost | $0 |

## Failures retained

1. Adaptive website pass 2 recorded `OSError` after 61 requests, without its detailed per-company summary. The original report retains the warning; the cause cannot be established from that warning alone. The pass was not rerun.
2. Site generation failed before publishing any page: `ValueError: Profile page exceeds 250 KB gate`. The original `check_live_run --count 500` exited 1 for this reason. [Original checker](check_live_run.txt).
3. The reporting helper initially assumed a completed pass-2 summary and raised `KeyError: per_company`. Only this reader was fixed; it reused the original failed checker receipt, without rerunning the checker or application. [Postprocessing receipt](finish-first-error.json).

An offline reconstruction with the same measured renderer found one oversized page, organisation `968360302`: 262,692 bytes, 42 workplaces, zero consolidated claims and one state-aid claim. All existing size fallbacks had been exhausted. No application code was changed to conceal this failure. [Every reconstructed profile size](html-size-diagnostic.json).

A separate network-blocked source-only verification passed: 500 schemas/order, 70,078 claims and 2,277 source blobs, with zero unsupported synthesis/briefing values. It does not check or repair the failed site. [Result](source-only-verification.json) and [execution](source-only-execution.json).

[Exact command and wall time](run.json) | [Clean clone / exclusion / input hashes](clean_clone.json) | [Disk guard](disk_guard.json) | [Per-type counts](counts.json) | [Application summary and warnings](summary.json)
