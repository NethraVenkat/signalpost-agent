# Stage E - measured refresh correctness

Refresh comparison now treats equivalent aware registry publication timestamps as the same instant and orders uncertain-section value comparisons by field. Publisher strings/evidence remain unchanged. C2 was reverted because the extension gained no websites. The new offline harness runs production proof/extraction/refresh/verification/site code with saved responses, fixed clock and isolated source mutations.

| Check | Result |
|---|---:|
| planted_causal_changes | 7 |
| true_positives | 7 |
| false_positives | 0 |
| false_negatives | 0 |
| supported_field_events | 40 |
| precision | 1.0 |
| recall | 1.0 |
| unchanged_changes | 0 |
| false_change_rate_unchanged | 0.0 |
| idempotent_changes | 0 |

Transient replay: 112 prior claims retained, original evidence IDs/times preserved, stale markers visible, zero company changes. Each of the seven changed snapshots repeated with zero company changes and zero coverage observations; unchanged snapshots also had zero observations.

Live-driven regression: pre-fix registry APIs alternated +01/+02 offsets and UTC Z representations of identical publication instants. This caused 620 false minor changes and 25 false coverage observations, overflowing the unchanged 250 KB page gate. Exact saved 100-company pair replay after comparison normalization yields zero changes/observations, all 1202 registry event receipts verified and site largest profile 249314 bytes; no rendering/evidence gate was loosened. See saved_live_pair_replay.json and the archived pre_timezone_fix trial.

Scope: one company from saved seed-20261113 receipts. Event precision and causal-intervention recall have different declared denominators. Synthetic empty NAV forward tail is explicit and supplies no job fact; exact saved ad detail is mandatory. This is not whole-feed coverage validation or a population-wide accuracy claim. No network fallback or paid model.

| Seed | C2 trial sites -> retained-policy sites | Social companies | Facts | HTTP | Wall seconds | Unsupported values |
|---|---:|---:|---:|---:|---:|---:|
| 20261017 | 5 -> 5 | 3 | 13325 | 690 | 368.169 | 0 |
| 20261113 | 4 -> 4 | 1 | 13751 | 785 | 399.116 | 0 |
| 20261114 | 3 -> 3 | 2 | 13248 | 719 | 347.072 | 0 |

All three are fresh state, exactly seven flags, 100 ordered terminal envelopes, generated sites, all five briefing topics, HTTP <=1850, within the default time limit, and $0. Exact commands, resolved defaults, source/input/output hashes, failures and verifier receipts are in each sample directory. Different observation times can change network outcomes; no causal coverage gain is claimed.

Live frozen refresh: 684 HTTP, 368.449s wall, 0 company changes (0 material, 0 minor), 0 coverage observations, 0 carried-forward claims. Seven evaluator flags **plus explicitly requested --previous** pointing to the latest frozen envelopes; no feature/cap flags. Fresh runtime cache. Missing archived evidence bodies are added only after the run for verification, never used as current proof. Full before/after evidence and observations: live_refresh/results.json. Zero unsupported values and $0.

Hand check: inspect all seven mutation receipts and repeated results in refresh_results.json; verify NAV inactive proof and the website 404 removal versus timeout carry-forward; inspect any live material events individually before treating them as real-world effective dates. Company value changes and coverage observations remain separate. New/removed website/social proof excerpts: new_websites.md (unchanged inventory in url_inventory.json). No publication or push.
