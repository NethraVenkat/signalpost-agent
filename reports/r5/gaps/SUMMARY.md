# Gap implementation and verification

Latest official API follow-up: `4ca3443`, signature/prokura and direct group relationships implemented through the existing registry client. Standard-100 full checker passed: 95/291 signature companies/claims (registered text 72/72), 10/20 prokura (registered text 8/8), 9/60 group, 14,165 total available claims versus 13,799 retained by `ac88ab0`; zero unsupported values, deadlines and placeholders; largest HTML 247,950 bytes; $0. No new 500 run. [Policy and complete comparison](g1-api/SUMMARY.md).

The original gap measurements below used baseline `45afc2b`, documentation follow-up `528e05a`, and application `f740933`; their historical counts and failures remain separate.

**The original full 500-company gate failed; the same saved outputs now pass the full offline check after repair at `567eafe`.** The CLI exited 0 and its source verification passed, but no HTML site was published because one reconstructed profile exceeds 250,000 bytes. Adaptive website pass 2 also raised `OSError`; its cause and per-company loss details were not recorded. Zero deadline hits do not establish complete website work or a performance improvement.

The network-blocked rebuild took 45.09 s, produced 500 company pages with a 249,270-byte maximum, and passed `check_live_run --count 500` (exit 0, 122.66 s). All original output hashes and published facts/evidence are unchanged. No new live run. [Repair and receipts](site-fix/SUMMARY.md).

## Changes and access limits

- G1 (`13e7108`): recorded the inaccessible canonical Brreg robots gate. Signature/prokura remains unimplemented; no usable authority response or real-response fixture was obtained. [Access checks](G1.md).
- G2 (`22846b8`): publish separately scoped consolidated statements already in the ordinary exact-orgnr accounts response. Brreg group-tree lookups remain pending the same robots gate. [Source and tests](G2.md).
- G3 (`f740933`): restore state aid from our own licensed official bulk extract, with exact recipients, dated evidence and full source replay. No competitor code or data used; no state-aid HTTP request occurs during a run. [Source, licence and build](G3.md).
- Final full pytest: **1,438 passed in 1,014.72 seconds**. No pytest ran in the clean verification clone. No tags, merge of `competitors-local`, or push.

## Measured outputs

| Information type | Standard 100: companies / claims | Fresh 500: companies / claims |
|---|---:|---:|
| Signature/prokura rules | 0 / 0 | 0 / 0 |
| Brreg group relationships | 0 / 0 | 0 / 0 |
| Consolidated accounts | 4 / 180 | 5 / 336 |
| State aid | 8 / 51 | 33 / 205 |
| All available claims | 100 / 13,799 | 500 / 70,078 |

| Metric | Standard 100 | Fresh 500 |
|---|---:|---:|
| Process wall / fixed budget, seconds | 558.28 / 2,100 | 1516.75 / 2,100 |
| Margin, seconds | 1541.72 | 583.25 |
| CLI exit / full checker exit | 0 / 0 | 0 / 0 (offline repair; originally 1) |
| Run status | partial | partial |
| Deadline hits | 0 | 0 |
| JSON envelopes / JSON profiles / placeholders | 100 / 100 / 0 | 500 / 500 / 0 |
| Published HTML profiles | 100 | 500 (offline rebuild) |
| Largest HTML profile | 242,559 bytes | 249,270 bytes (offline rebuild) |
| Unsupported synthesis / briefing values (saved-source check) | 0 / 0 | 0 / 0 |
| Provider cost | $0 | $0 |

The same ordered standard seed-20261017 cohort had 13,567 available claims at `45afc2b`, versus 13,799 now: 180 consolidated + 51 state-aid claims, plus one other live website-information claim. [Full comparison](standard100/SUMMARY.md).

The single clean-clone 500 run used seed **20261125**, 500 inputs disjoint from 6,207 preserved prior input numbers, exactly seven flags and `--expected-count 500`. Setup and run checked for at least 15 GiB; the 3 GiB guard sampled a minimum of 17.11 GiB and did not trigger. One input missing from the bulk subset was retained and resolved by the normal live identity path; no replacement draw. [Setup and original checker failure](final500/SUMMARY.md).

The oversized organisation is **968360302**, with 42 workplace claims, zero consolidated claims and one state-aid claim. Its original 262,692-byte reconstruction was oversized with explorer rows and inline official facts both at zero and source shortcuts disabled. The subsequent repair at `567eafe` reduces it to 219,666 bytes, retaining all 42 workplaces in local data. The live cohort was not rerun.

The separate offline saved-source check passed all 500 envelopes: 70,078 available claims, 2,277 original source blobs, 31,716 financial inputs, 225 exact-official claims, and zero unsupported synthesis/briefing values. That source-only check did not repair the site; the later offline rebuild and full check did. [Source-only check](final500/source-only-verification.json).

The committed 686,790-byte evidence packet reproduces both field-count inventories and all **772 new consolidated/state-aid claims**, with 265 original evidence bodies. It replayed offline against the clean clone without local run directories or pytest. Legacy values, timings and historical sampling-universe bytes are outside that packet's source-replay scope. [Reproduction instructions](EVIDENCE.md).
