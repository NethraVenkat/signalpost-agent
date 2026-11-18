# FX1 and FX2 runtime checks

The fresh, foreground run used frozen cohort `20261117`, the seven evaluator flags and the fixed 2,100-second default. The live checker verified 100 ordered envelopes and 100 generated HTML profiles. All 100 required profile records were present and there were zero placeholders. [Execution receipt](seed20261117/execution.json) · [Live verification](seed20261117/verification.txt)

| Metric | Stage W, same cohort | FX1 and FX2 |
|---|---:|---:|
| CLI wall time | 475.28 s | 337.16 s |
| Website pass-2 time | 190.13 s | 42.81 s |
| Website pass-2 HTTP attempts | 112 | 22 |
| Total HTTP attempts | 1,078 | 1,009 |
| Published websites | 9 | 9 |
| Companies with a website deadline | 0 | 37 |
| Largest profile HTML | 249,441 B | 248,461 B |
| Provider cost | $0 | $0 |

Website pass 2 began at 267.19 s and stopped at its 310.00 s cutoff. Its last HTTP attempt began at 309.27 s. All nine website URLs and all exact-ID claim identities matched the same-cohort baseline. Exact-ID section coverage was identical and none of those sections recorded a deadline. [Measured summary and artifact hashes](seed20261117/summary.json)

| Exact-ID family | Companies with available data | Published claims |
|---|---:|---:|
| GLEIF | 14 | 20 |
| TED procurement | 0 | 0 |
| State aid | 7 | 46 |
| Research | 1 | 1 |
| Licences | 0 | 0 |
| Inspections | 1 | 27 |

The runtime site build took 9.62 s. `check_live_run.py` read the emitted HTML sizes directly. A seven-flag integration test also passed an oversized contact-heavy response through the runtime builder. The page fit after duplicate shortcuts were deferred, and all 155 fixture contact values and the exact publisher URL were still present in the evidence data.

At 500 companies the website pass-2 cutoff is 1,550 s. The 250-second finalisation allowance targets completion by 1,800 s, leaving 300 s under the default budget when other crawl work finishes within that window. The allowance includes the previous F2 run’s roughly 192 s of post-crawl work. The 500-company margin awaits live verification after W3 and the seed hand-check. Check for at least 20 GB of free space immediately before launching that run.
