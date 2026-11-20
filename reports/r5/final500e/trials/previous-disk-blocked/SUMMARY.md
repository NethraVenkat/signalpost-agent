# Final500e: setup blocked by disk threshold

**No live 500-company run was started.** Initial setup and the single fresh setup retry both failed the free-disk prerequisite before cloning, sampling or network preflight. Requested seed `20261126` was not drawn. No tags or push.

The enforced threshold was 15 GiB (16,106,127,360 bytes), which also exceeds the requested 15 GB. Initial free space: 11,549,683,712 bytes. The [retry receipt](trials/setup-disk-retry/initial-disk.json) records the final free-space value, also below **15,000,000,000 bytes**. Thus interpreting GB as decimal would not change the outcome. The 3 GiB live guard never became active because no live run began.

Only reversible cleanup within our workspace was considered. Disposable test folders were too small to bridge the shortfall. Completed historical run files were already NTFS-compressed, so their logical sizes overstated reclaimable space. A slow lossless archive attempt was stopped before a verified archive or original-directory removal. All original historical run directories and all measured evidence remain in place. [Remediation receipt](trials/setup-disk/archival-stopped.json). Unrelated user data and the six pre-existing untracked paths were untouched.

| Requested qualification metric | Result |
|---|---|
| Setup attempts / live runs | 2 / 0 |
| Clean final500 clone / clone pytest | Not created / not run |
| Seed / disjointness qualification | 20261126 requested; no draw or run |
| Wall time / margin / placeholders / run status | Not measured; blocked before run |
| Deadline hits / largest profile / per-type claims | Not measured |
| Unsupported values / `check_live_run --count 500` | Not measured / not run |
| Provider cost | $0 |

Historical 500 runs and the successful standard-100 run are not substituted as new qualification results. There was no site failure to repair offline and no live retry, because no live run started. Under the overnight instruction, P3 documentation/tests continue with this blocked status disclosed.

[Machine-readable outcome](summary.json) | [First failure](trials/setup-disk/initial-disk.json) | [One retry](trials/setup-disk-retry/initial-disk.json). Preparation/run helpers are retained as reviewable work; they refuse to start below the threshold and would use the unchanged seven flags, fixed 2,100-second budget, a clean clone, production-transport preflight and a 3 GiB stop guard. Re-run preparation only under a later instruction once disk space is available.
