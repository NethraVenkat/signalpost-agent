# Stage A0 - default enrichment

The exact seven evaluator flags now enable website discovery, hiring and public website activity, with unchanged 8/13 website ceilings. CLI negative opt-outs and library booleans disable them; positive flags remain compatible. README's command now uses only the seven official flags. Registry changes remain enabled.

The shared request meter enforces floor(1,850 ? unique inputs / 100) including shared NAV, robots, redirects and retries; explicit limits may only lower it. Time defaults to 2,100 seconds, clamped to 21 seconds per unique input with output/site reserves. Missing CSV lookups cannot extend the original deadline. Reports expose effective limits, enrichment switches and end-to-end completion. Duplicate rows cannot inflate limits. Slow/uninterruptible input or filesystem work and unrealistically tiny budgets remain explicitly reported limitations, not promises of impossible timing.

## Fresh seven-flag measurement

Exactly seven flags, no cap or enrichment flags, fresh working directory/default state, new run ID and hash-checked frozen inputs. All source facts equal Stage S's full-feature run; zero job-ad companies is the actual source outcome, not a disabled hiring switch. NAV retains 11 incomplete hiring sections; BIEN accounts remains HTTP 500. Website/activity failures are 16/23 versus S's 18/25; these are live source variations, not demonstrated causal gains.

| Metric | Stage S full-feature | A0 seven flags |
|---|---:|---:|
| verified_websites | 6 | 6 |
| social_profile_companies | 3 | 3 |
| activity_companies | 31 | 31 |
| activity_claims | 90 | 90 |
| total_facts | 9381 | 9381 |
| locations | 73 | 73 |
| job_ad_companies | 0 | 0 |
| contacts | 12 | 12 |
| http_requests | 887 | 904 |
| runtime_seconds | 255.094 | 299.625 |
| process_wall_seconds | 262.766 | 325.795 |
| Provider cost USD | 0 | 0 |

The independent verifier passes 100 complete briefing contracts, 4,208 financial inputs, 153 derived ratios and zero unsupported synthesis/briefing values. Original reports, source/output hashes, exact argv/resolved configuration and per-company state tables are retained here. Completion includes outputs and site at 322.704s; process wall is 325.795s, both inside 2,100 seconds. HTTP 904 is below 1,850.

The site is available for 100 companies / 102 HTML pages. Authored headless Chromium checks pass at 1280/360 px (14 checks, 12 screenshots), with source receipts, five visible briefing elements, comparison, 44px controls, no horizontal page overflow/JS errors and external requests blocked.

## Tests and decisions

Final green full suite: **822 passed in 198.07s**, see tests.txt. Focused A0/evaluator/budget tests: 33 passed. Tests cover CLI/library defaults, compatibility and opt-outs, 8/13 caps, scaled request/time hard stops, downward-only overrides, duplicates, explicit cutoff errors, preserved outputs and a complete site. Legacy source fixtures explicitly disable unrelated tools; seven-flag integration tests use production defaults.

The first full attempt found an outdated NAV time assertion (900 vs the new 840 seconds); it was corrected to the new default. The second attempt hit the unchanged five-second HTML localization subprocess timeout; that test passes alone in 1.01s. Failed logs are retained. No timing assertions or proof rules were loosened. Decisions are in ../DECISIONS.md. This stage is committed only after the complete suite is green; Stage A follows separately.
