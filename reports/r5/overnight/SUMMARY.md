# Overnight P1-P3 outcome

- P1 committed as `35a547e`: 200 frozen seeded claims; strict verbatim-span audit 50 correct / 0 incorrect / 150 unverifiable; nominal Wilson 95% lower bound 19.51%. This is not a factual-accuracy estimate; the disproportionately stratified sample does not establish a population Wilson guarantee. Full source support differs from literal short-span certification. [Results, methods, committed proof and human checklist](../precision-sample/SUMMARY.md).
- P1 independently replayed in a fresh sparse clone of that commit, with no network, run directories or third-party dependencies. [Receipt](../precision-sample/fresh-clone-replay.json).
- P2 committed as `129ce84`: initial setup and the one allowed fresh retry failed the disk prerequisite (retry 11,009,769,472 bytes). No final500e sample, clone, network preflight, live run or qualification check. Requested seed 20261126 remains unused. No timing, margin, profile-size, coverage or unsupported-value result is invented. $0. All original historical run directories remain. [Failure receipts](../final500e/SUMMARY.md).
- P3 updates README, SUBMISSION and decisions to disclose both outcomes. Main-checkout full pytest: **1,464 passed in 980.90 seconds** ([receipt](pytest.txt)). Final privacy verification is recorded in [privacy.txt](privacy.txt). The two clone-only P1 tests did not run pytest; no final500 clone was created. No tags, merge or push.

P2 remains blocked, not qualified: no new 500-company research output or measurement exists. P1 and P3 are complete; the failed P2 prerequisite is preserved rather than bypassed. The source application remains `4ca3443`, with P1 proof at `35a547e` and blocked P2 at `129ce84`. All commits use the repo-local Nethra Venkat author/committer; no tags, merge or push.

Final privacy guard: **5 passed in 15.18 seconds** ([receipt](privacy.txt)); no full-suite retry was needed. P3 is complete; P2 remains resource-blocked.
