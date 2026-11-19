# Standard 100-company comparison

Baseline `45afc2b`; candidate `f740933af530a9756f07c236a79bceae069eb862`. Same ordered standard seed-20261017 cohort, fresh state and exactly seven flags. The baseline is our saved earlier run, not a new baseline execution.

| Information type | Baseline companies / claims | Candidate companies / claims | Claim change |
|---|---:|---:|---:|
| Signature/prokura rules | 0 / 0 | 0 / 0 | +0 |
| Brreg group relationships | 0 / 0 | 0 / 0 | +0 |
| Consolidated accounts | 0 / 0 | 4 / 180 | +180 |
| State aid | 0 / 0 | 8 / 51 | +51 |
| All available claims | 100 / 13,567 | 100 / 13,799 | +232 |

Process wall time: **558.28 s**, margin **1541.72 s** under the fixed 2,100 s budget. Exit 0; 100 envelopes; zero deadline hits; run status `partial`; provider cost $0. Largest HTML profile: 242,559 bytes.

`check_live_run --count 100` passed: 473 source blobs, 6,296 financial inputs and 66 exact-official claims checked. Unsupported synthesis/briefing values: 0 / 0. No unfinished section placeholders. New gap claims are 180 consolidated + 51 state-aid claims; the additional one-claim total difference is in live website information.

Signature/prokura and Brreg group-tree lookups remain pending because canonical origin robots could not be fetched after retries. Consolidated statements come from the existing approved accounts response; state aid uses the dated official bulk extract. A passing output checker does not imply full source coverage or an official score.

[Counts](counts.json) | [Execution and seven flags](execution.json) | [Saved-output check](check_live_run.txt) | [Baseline provenance](../baseline-45afc2b-source.json)
