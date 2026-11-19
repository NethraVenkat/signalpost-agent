# Saved 500-run repair and offline verification

Fix commit: `567eafe8a3f815740d5465f19e5217b27c5fd087`. Original live measurement: `f740933`, seed 20261125. **Full offline check passed (exit 0)** using the SAME saved 500 envelopes and source blobs. No new live 500 run, tags or push.

| Check | Result |
|---|---:|
| Full pytest before fix commit | 1,444 passed / 906.97 s |
| Privacy guard before fix commit | 5 passed / 2.98 s |
| Offline site rebuild wall | 45.09 s |
| Full saved-output checker wall / exit | 122.66 s / 0 |
| Company HTML pages / placeholders | 500 / 0 |
| Largest profile HTML | 249,270 bytes (<250,000) |
| Profile 968360302: before / after | 262,692 / 219,666 bytes |
| Target workplaces retained / deferred to local data | 42 / 42 |
| Available claims | 70,078 (unchanged) |
| Local published/cited facts / referenced evidence records | 77,610 / 117,159 |
| Workplace claims / deferred workplace claims | 453 / 44 |
| Complete cited briefing contracts | 500 |
| Unsupported synthesis / briefing values | 0 / 0 |
| Source blobs / financial inputs verified | 2,277 / 31,716 |
| Original run status / deadline hits | partial / 0 |
| Original process wall / margin under 2,100 s | 1,516.75 / 583.25 s |
| Activity available / failed | 500 / 0 |
| Websites / social URLs | 36 / 24 |
| Consolidated accounts: companies / claims | 5 / 336 |
| State aid: companies / claims | 33 / 205 |
| Stage S claims: aid / research / licences / inspections | 205 / 10 / 9 / 1 |
| Provider cost | $0 |

The live timing is the original failed-site run's timing, not a new measurement of the fixed application. The checker reads the original internal completion wall (1,512.343 s), while the externally measured process wall is 1,516.75 s. Offline rebuilding and checking are separate operations. The derived report replaces only site results and adds rebuild metadata; it retains original warnings/status/timing. Original envelope, profile and report files remain byte-identical by SHA-256.

Workplaces use the existing local-details loader, with first 10 inline by default and a smaller allowance when needed to fit the page. Every published/cited fact value and every referenced evidence field was compared against all 500 original envelopes. Target 968360302 retains all 42 workplace values and their evidence in its local data file. Generated site/data files remain local; committed receipts contain counts and hashes, not personal source content.

Adaptive errors now fail the affected company's section explicitly and let other companies continue. Tests cover nomination, discovery, post-proof activity and receipt-storage failure. The historical log lacks errno/message/traceback; its low-level OS cause cannot be proven. The original adaptive warning remains visible and that historical work was not rerun. [Diagnosis](DIAGNOSIS.md).

[Full pytest](pytest.txt) | [Privacy](privacy.txt) | [Rebuild](rebuild.json) | [Full checker](check_live_run.json) | [Checker execution](check-execution.json) | [Original output integrity](original-output-integrity.json) | [All local payload integrity](payload-integrity.json).

Offline reproduction with the retained original run in `.data/r5-gaps-final500/run`: run `python reports/r5/gaps/site-fix/rebuild.py` with a fresh `out/r5-site-fixes/offline500` destination, then `python reports/r5/gaps/site-fix/audit_payloads.py`. Both block network. The bounded committed source packet is separate; it does not contain all legacy run data needed for this full-site rebuild. [Clone-only new-claim reproduction](../EVIDENCE.md).
