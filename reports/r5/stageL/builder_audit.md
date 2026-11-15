# L3 — site-builder audit result

Offline source set: the six accepted post-rollback R7 samples, exactly the hashes listed in [audit.json](audit.json). No network requests.

| Builder data | Saved script matches containing exact target orgnr |
|---|---:|
| Wix warmup/viewer data | 0 |
| Squarespace static context | 0 |
| __NEXT_DATA__ | 0 |
| Nuxt | 0 |

The requested condition for implementing a builder footer/contact extractor is not met. No parser or arbitrary script-string proof is introduced. Existing HTML/JSON-LD exact-owner rules are unchanged. This is a measured absence in the saved unproved-page scope, not a claim that all builders or future responses lack identifiers.

Runtime is identical to green L2. This report-only checkpoint reuses the full green pytest result recorded in pytest-L2.txt; no runtime edit or new test condition warrants repeating it. L4 follows.

## Broader numeric-pattern audit correction

The initial audit above counted exact target identifiers, not all numeric patterns. A supplemental zero-network audit, [builder_patterns.json](builder_patterns.json), includes every marker-bearing script and records every candidate excerpt and original page/script hash.

| Builder | Script instances | Raw nine-digit fragments | Checksum-valid fragments | Labelled valid orgnr | Qualifying footer/contact orgnr |
|---|---:|---:|---:|---:|---:|
| Wix | 343 | 716 | 33 | 0 | 0 |
| Squarespace | 23 | 35 | 0 | 0 | 0 |
| Next | 8 | 17 | 1 | 0 | 0 |
| Nuxt | 4 | 0 | 0 | 0 | 0 |

Saved-context inspection of all 34 checksum-valid fragments found one latitude decimal and 33 opaque build fingerprints, asset identifiers or UUID tails. None is footer/contact text or the target organisation number. These arbitrary script strings cannot trigger identity proof. There is still no qualifying footer/contact component containing an orgnr to implement and validate against; no speculative runtime builder parser is added. The earlier exact-target count remains zero, but must not be read as zero arbitrary numeric fragments. Runtime and the six-sample measurement manifest remain unchanged.
