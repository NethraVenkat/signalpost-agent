# P3 six-sample no-regression check

One fresh exact-seven-flag run per sample at the P3 source (`measure.py`, derived from Stage S), compared with the Stage S measurement of the same frozen sample (`reports/r5/stageS/seed<seed>/counts.json`).

| seed | runtime s (Stage S) | HTTP (Stage S) | facts (Stage S) | websites (Stage S) | official claims | largest profile B | identity changes |
|---|---|---|---|---|---|---|---|
| 20261017 | 513 (922) | 1151 (1173) | 13622 (13622) | 7 (7) | 66 | 242988 | none |
| 20261113 | 486 (887) | 1118 (1142) | 14070 (14069) | 6 (6) | 76 | 227495 | none |
| 20261114 | 502 (905) | 1131 (1144) | 13529 (13529) | 6 (6) | 65 | 226344 | none |
| 20261115 | 465 (880) | 1137 (1166) | 13327 (13328) | 9 (9) | 41 | 225505 | none |
| 20261116 | 510 (968) | 1185 (1212) | 13879 (13880) | 8 (8) | 93 | 240730 | +813911442 website https://www.californiainvest.no ; -813911442 website https://californiainvest.no |
| 20261117 (retry) | 495 (911) | 1091 (1109) | 14143 (14142) | 9 (9) | 74 | 249441 | none |

All six pass `check_live_run` and the site gate, with 0 unsupported values and $0. Runtime is about halved (465-513 s vs 880-968 s) with the same websites, facts within ±1 and the same official claims.

Identity change: 813911442 website now resolves to `https://www.californiainvest.no` instead of `https://californiainvest.no`. Same site, different live final URL; live variation.

Seed 20261117: the first attempt (`seed20261117/`, kept) failed `check_live_run` with "Hard time budget exceeded" at 16,399 s wall. Its last request started at 161 s, and event-loop lag reached 9,639 s: the whole process was frozen for ~2.7 h overnight while the machine was suspended, despite the run's idle-sleep request. This is an environment outage, so per the standing rule it got one fresh retry in a new directory (`trials/seed20261117-retry/`), which passed. The two runs were not combined.
