# Single-pass website confirmation

One fresh 500-company run used the frozen seed `20261126`, run ID `r5-single-pass-20261126`, exactly seven evaluator flags, and a fixed 2,100-second process budget. Robots, Brønnøysund, and GLEIF preflight checks each returned HTTP 200. The run exited 0, produced 500 terminal envelopes and profiles, had zero placeholders, and cost $0. The lowest free disk reading was 16.17 GB. The live output checker passed with zero unsupported synthesis and briefing values.

| Metric | Stage 2 live | Stage 2 corrected offline | Single pass live |
|---|---:|---:|---:|
| Wall time (seconds) | 1,852.468 | — | 1,489.860 |
| Margin under 2,100 seconds | 247.532 | — | 610.140 |
| Deadline hits | 183 | — | 0 |
| Available claims | 76,895 | 76,888 | 76,873 |
| Companies with an available official website | 38 | 37 | 37 |
| Companies with a current `VERIFIED` website | 31 | 31 | 29 |
| Largest profile HTML (bytes) | 234,189 | 234,189 | 234,983 |
| Run status | `partial` | — | `partial` |

The process reclaimed **362.608 seconds** versus Stage 2. The second scheduler occupied 382.234 seconds and yielded zero verified websites in that run. Its deletion removed the second check and its allowances. The remaining website pass uses the 1,700-second cutoff and the existing 45-second company cap, 16 company slots, and two in-flight requests per host. The shared slot wait was 110.851 seconds at the median, 255.640 at the 95th percentile, and 267.578 at the maximum. Stage 2 deadline hits use the reconciled receipts.

The website coverage count held at the corrected offline baseline of 37. Four companies entered and four left the availability set. `999582214`, whose saved website was withdrawn in the offline replay, gained a `HIGH` website claim from a different page with a unique registry-phone publisher receipt in the live run. The `VERIFIED` subset fell by two on the identical inputs. The two live runs may have received different publisher responses.

Finanstilsynet robots requests recorded three `ConnectTimeout` failures. The existing fail-closed rule blocked the licence section for all 500 companies. Stage 2 had 22 licence claims across 10 companies. Relative to the corrected offline baseline, live website-family claims increased by seven and licence claims fell by 22. All other families kept the same available claim totals.

The stratified 200-claim stored-evidence sample used seed `202611200628`. It yielded **200 supported**, **0 contradicted**, and **0 missing or mismatched blobs**. The Wilson 95% lower bound was **98.12%**, above the 95% gate. The sampler capped a stratum quota at its available population and redistributed the remaining sample slots across the other strata. Every populated family was included.

All 1,491 collected tests passed across four batches. The separate privacy and profile checks passed 17 and 2 tests, respectively.

[Machine-readable receipt](single-pass-confirmation.json) · [Stage 2 results](STAGE2.md) · [Publisher receipt correction](PUBLISHER-RECEIPTS.md)
