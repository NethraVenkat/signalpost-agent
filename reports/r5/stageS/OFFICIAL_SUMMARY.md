# Stage S - exact-ID official sources: six-sample measurement

One fresh exact-seven-flag run per sample (`measure.py`), compared with the P0 re-baseline on new machine (`reports/r5/stageP0rb`). Sub-steps: S1 Wikidata skipped (robots), S2 Støtteregisteret, S3 RCN + SkatteFUNN, S4 Finanstilsynet (DiBK skipped, robots), S5 Smilefjes, S6 signatur/prokura skipped (not in open API). Sources, licences, terms and robots: `docs/SOURCES.md`.

| seed | HTTP (base) | runtime s (base) | facts (base) | websites (base) | official claims | official verified | largest profile B |
|---|---|---|---|---|---|---|---|
| 20261017 | 1173 (973) | 922 (733) | 13622 (13560) | 7 (8) | 66 | 66 | 243340 |
| 20261113 | 1142 (927) | 887 (666) | 14069 (13993) | 6 (6) | 76 | 76 | 227495 |
| 20261114 | 1144 (950) | 905 (606) | 13529 (13464) | 6 (6) | 65 | 65 | 226344 |
| 20261115 | 1166 (951) | 880 (561) | 13328 (13287) | 9 (9) | 41 | 41 | 225120 |
| 20261116 | 1212 (1007) | 968 (653) | 13880 (13787) | 8 (8) | 93 | 93 | 239436 |
| 20261117 | 1109 (907) | 911 (575) | 14142 (14068) | 9 (9) | 74 | 74 | 249326 |

Totals: state aid 337, research 10, licences 26, inspections 42 = 415 published official claims, all independently re-verified (`exact_official_items_verified`); 0 unsupported/unverified synthesis or briefing values. HTTP 6946 vs 5715 baseline (+1231, 1158 per 100 companies, within 1,850). Cost $0.

Site gate: seed 20261117's single run completed (exit 0, 100 envelopes) but its in-run site build raised the 250 KB profile gate: company 948039958 was at 249,037 B in the re-baseline and gained 27 inspections + 9 state-aid records. Fix (S7, `src/signalpost/site.py`): show the newest 8 records per official family inline and defer older ones to the local data file (same `data-registry-details` loader as registry attributes), halving further only if a page is still over the gate. No fact, anchor or receipt is dropped; the gate is unchanged. All six sites were then rebuilt from their saved envelopes with the final code (`resite.py`, no recrawl, no union) and `check_live_run` passed for all six (`seed*/verification-resite.json`; the run's own report is `report-run.json`). Seed 20261117 counts were written from its saved run by `finish_counts.py`.

Identity items: none added; one removal (seed 20261017, Bellas Burrito website + brand) from live robots variation - see `new_items.md`.

Runtime rose ~250-330 s per sample: politeness delays on the live Støtteregisteret and Finanstilsynet APIs.
