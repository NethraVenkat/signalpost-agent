# Stage 2 website timing and coverage

The same 500 companies as S6 were run once with seed `20261126`, run ID `r5-gap-stage2-20261126`, fresh state, the seven evaluator flags and the fixed 2,100-second budget. Live robots, Brønnøysund and GLEIF probes each returned HTTP 200 before the run. The run used a 10 GB initial disk floor and kept the 3 GiB stop guard armed. The lowest reading was 12.22 GB. It exited 0 with 4,672 successful HTTP responses and $0 provider cost. The run status was `partial`.

| Metric | S6 | Stage 2 | Change |
|---|---:|---:|---:|
| Elapsed seconds | 1,902.844 | 1,852.468 | −50.376 |
| Seconds left in budget | 197.156 | 247.532 | +50.376 |
| Terminal envelopes | 500 | 500 | 0 |
| Company profile pages | 500 | 500 | 0 |
| Placeholders | 0 | 0 | 0 |
| Largest profile HTML in bytes | 234,189 | 234,189 | 0 |
| Companies with an available official website claim | 38 | 38 | 0 |
| Companies with a current website labelled `VERIFIED` | 32 | 31 | −1 |
| Available website-family claims | 221 | 224 | +3 |
| Available claims across all families | 76,892 | 76,895 | +3 |
| Companies cut off in website pass 2 | 180 | 183 | +3 |
| Pass 2 start in seconds | 1,268.234 | 1,317.828 | +49.594 |
| Pass 2 website HTTP requests | 217 | 205 | −12 |
| Additional verified websites from pass 2 | 0 | 0 | 0 |

The available website coverage set gained `911821834` and lost `927733714`. The coverage and claim deltas are observations from two live runs on the same inputs. Source responses may have changed between runs. [S6 baseline receipt](../s6-clone-gate/summary.json)

The 45-second cumulative limit covers active candidate discovery across both passes, including pass 1 nomination work. The report records the pass, active seconds, attempted HTTP requests, handled request timeouts and the last classified wait at interruption for each company. The initial shared slot queue is measured separately. Activity and careers enrichment are outside the company cap, under the existing run deadlines. The site finalisation reserve and website proof rules stay in place.

| Time in seconds across 500 companies | Median | 95th percentile | Maximum |
|---|---:|---:|---:|
| Active discovery | 5.985 | 26.469 | 45.001 |
| Shared slot queue | 116.054 | 214.015 | 222.187 |

One company, `915955711`, reached its cap waiting for an HTTP response on its ninth discovery request. Another in-flight discovery was waiting for an HTTP response at the batch deadline. No company was interrupted in the initial shared slot queue. Request-level timeouts were handled separately, with 78 for robots responses and four for page responses. Pass 2 used 382.234 seconds on 104 legal-page resumptions, at a total of 205 HTTP requests, and gained zero verified websites. Of the 183 companies with nominations left at the cutoff, 114 had no pass 2 attempt and 69 had at least one. That second group includes the company that hit its individual cap earlier.

The benchmark's top-level `deadline_hits` field reported three because the final envelope loop checked for duplicate errors on the previous company. The saved per-company scheduler receipts show 183 cutoffs, of which 180 were missing the website deadline error in their envelopes. Reconciling the two sources yields 183 unique deadline-hit companies. The committed loop uses each company's own envelope, and a two-company regression test checks that both companies receive one error each. This correction runs after the website scheduler and leaves the benchmark's requests, elapsed crawl time and website claims as measured.

## Proposed coverage experiment

Trial two pass 2 workers on the same cohort, with one candidate in flight per company and existing per-host limits. Include a separate, bounded allocation for queued registry-declared candidates where present, so legal-page resumptions cannot use the entire window. Retain the 45-second company cap, the 1,700-second website cutoff, the 2,100-second run budget and the proof requirements. Measure first attempts, deadline hits and incremental verified companies for each candidate group. Repeat the stored-evidence gate. The trial would test whether reaching more companies produces more verified sites. The proposal requires approval before discovery changes.

## Evidence and validation

At seed `202611200628`, the original 200 jury claim IDs all replayed as supported. A separate stratified 200-claim draw from the new live output using the same seed and method also found 200 supported. Both had zero contradictions and zero missing or mismatched blobs. Both Wilson 95% lower bounds were **98.12%**.

The live output checker passed on all 500 envelopes and profiles, with zero unsupported synthesis or briefing values. The [comparison receipt](stage2-comparison.json) contains section counts and checker results. The [per-company timing receipt](stage2-website-measurement.json) contains attempts, waits and cap records for every input.

The full test suite passed 1,522 tests. The separate privacy and profile checks passed 17 and 2 tests, respectively.
