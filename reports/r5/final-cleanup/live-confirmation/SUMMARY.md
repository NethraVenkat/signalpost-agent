# Interrupted live confirmation

The single authorized clean-clone run used commit `5af744d883ce62f81461d07ece235b3948e45421`, seed 20261126, exactly seven evaluator flags, a fixed 2,100-second budget, fresh state, a 12 GB pre-run floor and a two-second disk guard stopping below 3 GiB. The clone was clean at launch. Robots, Brreg and GLEIF preflight requests each returned HTTP 200.

The last saved heartbeat was at 1,105.23 seconds with 437/500 successful company tasks, 63 in flight and none failed. Free disk at that check was 14,639,902,720 bytes, above the 3 GiB stop guard. The supervising tool session disappeared and neither the CLI process nor the driver remained. The log was empty, `execution.json` was never written, and final envelopes, profiles and report were absent. The progress file still says `running`, which is stale. The cause of process termination and its exit code are UNVERIFIED.

Run outcome is **interrupted and incomplete**. Wall time, margin, published claim and website counts, deadline hits, largest profile, run_status, placeholders, unsupported values, and the 200-claim precision lower bound are UNVERIFIED. The precision gate cannot be evaluated. The saved state and partial site data remain under the ignored clean-clone run directory. No second live attempt was made.

The preflight and last-progress receipts are committed beside this note. This run does not validate the cleanup for submission.
