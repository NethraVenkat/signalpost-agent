# R2 progress

2026-10-17 23:57:32 IST — Phase 0: created revision/r2 from a05ffae; saved overnight prompt verbatim (SHA256 3d7bae9e9eae7b612d1c0e8448ce58ce41ddd1dc5269c92cade8caca4f38670d). No active Signalpost Python/uv run found. Main and v1.0.0 unchanged. No morning completion marker created.

2026-10-17T23:59:51+05:30 ? Inventory: evaluator flags in cli.py; models schemas unchanged; site.py/site_assets; deterministic synthesis/template.py; refresh/diff.py; sources/bulk_registry.py. Frozen input hashes: reports/r2/inputs.json. A1 focused checks 52 passed; bulk checks 9 passed. One nationwide 30-second benchmark active at out/r2-a1-nationwide30. Preparation is outside crawl deadline but included in measured wall time.

2026-10-18T00:00:33+05:30 ? A1 measurement: nationwide preparation 17.953 s (previous first HTTP ~40.7 s); all 1,000 envelopes and all 28,726 identity IDs retained. Wall 42.288 s FAILS 35 s gate; output 9.11 s. Kept provisionally for Phase A reserve work; not release-qualified. Focused tests pass.

2026-10-18T00:01:22+05:30 — A1 committed as 9ffff34; wall gate remains pending A4. A2 adds observed claim-ID history without copying facts from history; targeted refresh tests running.

2026-10-18T00:02:00+05:30 — 9ffff34 A1 committed. A2: 10 refresh tests pass; all six saved recovery cases replayed as availability observations, not material changes (reports/r2/a2-recovery-replay.json). History stores only IDs, never supplies facts or relaxes live proof.

2026-10-18T00:02:35+05:30 — A2 regression checks: 10 passed. Six saved recoveries replay as observations when explicit older-baseline ID history is supplied. Initial replay also carried unchecked-page facts and therefore did not exercise recovery; corrected replay preserves saved middle-run content. Legacy files cannot reveal forgotten history automatically.

2026-10-18T00:03:43+05:30 — 1ac8703 A2 committed. A3: 58 auditor/adversarial tests pass. Escaped JSON-LD URLs now retain verbatim local spans; social auditor parses sameAs; deletion=true requires an actual valid source date; own-invoice reference instructions no longer trigger generic partner heuristic, while customer negatives remain rejected.

2026-10-18T00:04:59+05:30 — 92e9975 A3 committed; 58 audit tests passed. A4 provisional measured reserve uses 10 ms/company plus 5 s, with optional site skipped when not reserved; 13 cancellation/output checks pass. Active 120 s benchmark out/r2-a4-120. The 30 s >=80% research and nationwide wall constraints remain unresolved; no RC tag.

2026-10-18T00:06:37+05:30 — Heartbeat: still running the sole A4 1,000-company 120 s benchmark; research reached 101 s (previous R1 run stopped much earlier). Required terminal outputs are being awaited. No duplicate run started.

2026-10-18T00:07:06+05:30 — A4 120 s measurement: exit 0; 1,000 envelopes, 28,726 identity IDs; wall 116.62 s; research 102.84 s; mandatory output 11.70 s; optional site skipped explicitly. Website availability 3->34, hiring 6->6, activity 1->3 versus saved R1 120 s run. Source/network variation limits causality. 30 s >=80% research target not met by measured mandatory-output reserve; nationwide wall still failing.

2026-10-18T02:35:06+05:30 — cb0b0e2 A4 committed; Phase A full suite 483 passed in 70.73 s. Starting single serialized 100-company smoke + 24-company baseline; no RC tag yet.

2026-10-18T02:35:06+05:30 — Heartbeat: a quick gate smoke100 running, PID 14300.

2026-10-18T02:35:51+05:30 — Heartbeat: a quick gate smoke100 running, PID 14300.

2026-10-18T02:36:10+05:30 — Heartbeat: a quick gate verify-smoke100 running, PID 25000.

2026-10-18T02:36:19+05:30 — Heartbeat: a quick gate baseline24 running, PID 23148.

2026-10-18T02:37:04+05:30 — Heartbeat: a quick gate baseline24 running, PID 23148.

2026-10-18T02:37:08+05:30 — Heartbeat: a quick gate verify-baseline24 running, PID 3200.

2026-10-18T02:37:09+05:30 — Heartbeat: a quick gate compare24 running, PID 25380.

2026-10-18T02:37:21+05:30 — Phase A full suite 483 passed; quick gate finished: 100-company delivery/site/schema/synthesis passed; 24-company run and verifier completed. All three prior audit flags pass corrected semantic checks (reports/r2/a3-known-flags.json). Full nationwide wall and 30 s research-share constraints remain open.

2026-10-18T02:37:37+05:30 — Phase A QUICK GATE PASS: 483 tests, 100 ordered envelopes and site, 24 ordered envelopes with 0 lost/added/duplicate IDs and 0 schema changes. Local rc-a marks this checkpoint only; full release gate remains unpassed. Optional discovery will be trimmed first to prioritize UX and Phase E.

2026-10-18T02:38:09+05:30 — f1281cd Phase A checkpoint, local rc-a. B1 five profile areas implemented while retaining old anchors, evidence controls and every claim; 24 site tests pass.

2026-10-18T02:38:40+05:30 — 030c9f0 B1 committed. B2 adds offline global name/orgnr search on every page with / and Ctrl/Command+K, native modal focus handling and bounded results. JS syntax and 24 site tests pass; browser gate pending.

2026-10-18T02:39:12+05:30 — 496d09c B2 committed. B3/B5: directory supports Most data found and all-five/per-area availability; compare persists 2-3 selections in URL query parameters while reading old hashes. Five areas displayed in comparison. 32 site/dashboard tests and JS syntax pass.

2026-10-18T02:39:40+05:30 — 796e987 directory/compare committed. B4 evidence buttons explicitly say Check the evidence; expanded panels retain URL, UTC retrieval, period, verbatim quote, locator, method and hash, and now show claim confidence/availability. 24 site tests pass.

2026-10-18T02:40:28+05:30 — 04fbfbc B4 committed. B6 browser check PASS: ten 1440/375 screenshots, no horizontal overflow across large/small/missing profiles, directory and compare; keyboard search works, two-company query selection survives load. Equinor 127,629 bytes; claims retained separately. Optional Ask omitted to prioritize release gate.

2026-10-18T02:41:10+05:30 — 0646721 B6 committed with ten screenshots. Phase B full suite running; no duplicate performance job. Capacity follow-up planned: preparation must not receive a second whole crawl budget; charge it to total wall time while preserving completed CSV facts and a bounded missing-row lookup opportunity.

2026-10-18T02:42:11+05:30 — Phase B full suite 483 passed in 71.39 s. Security heuristic scan: 242 tracked files plus reachable history diffs, no matching private-key/AWS/GitHub/OpenAI patterns (not an exhaustive secret certification). Single nationwide 30 s follow-up active after targeted regressions; bulk preparation now charged to total wall time with bounded missing-row lookup grace.

2026-10-18T02:42:47+05:30 — Nationwide A1 follow-up PASS: 23.15 s wall, exit 0, all 28,726 baseline identity IDs retained. Preparation no longer grants another full research budget. 13 targeted checks pass. Research-share >=80% at 30 s remains unmet and will be reported rather than hidden.

2026-10-18T02:42:48+05:30 — Heartbeat: b quick gate smoke100 running, PID 7976.

2026-10-18T02:43:07+05:30 — CORRECTION to preceding nationwide line: the asserted identity comparison failed: 28,723 IDs, three missing, all from the CSV-absent deleted company. Wall 23.15 s passed, identity gate did NOT. A shell continued after the failed assertion; c70ece2 is provisional and not release-qualified. Single Phase B smoke/24 gate active; no duplicate run.

2026-10-18T02:43:33+05:30 — Heartbeat: b quick gate smoke100 running, PID 7976.

2026-10-18T02:43:41+05:30 — Heartbeat: b quick gate verify-smoke100 running, PID 11528.

2026-10-18T02:43:50+05:30 — Heartbeat: b quick gate baseline24 running, PID 22152.

2026-10-18T02:44:35+05:30 — Heartbeat: b quick gate baseline24 running, PID 22152.

2026-10-18T02:44:38+05:30 — Heartbeat: b quick gate verify-baseline24 running, PID 4508.

2026-10-18T02:44:40+05:30 — Heartbeat: b quick gate compare24 running, PID 21116.

2026-10-18T02:45:25+05:30 — Phase B quick gate PASS: smoke100/site/verifier succeeded; baseline24 retains all 1,231 IDs in order with no duplicates/schema change. Missing-row grace fix now starts at actual network scheduling; 10 bulk regressions pass. One nationwide 30 s retest active at out/r2-a1c-nationwide30.

2026-10-18T02:46:14+05:30 — Nationwide corrected recheck PASS (asserted): 30.389 s wall <=35, exit 0, all 28,726 identity IDs, zero missing. Bulk 15.564 s, output 7.37 s. Missing-row grace now begins at network scheduling; 10 regressions pass. Earlier 28,723-ID failure remains recorded. Phase B quick gate passed 100/24, 0 lost IDs.

2026-10-18T02:47:03+05:30 — 3b46f78 fixes the CSV-absent live lookup boundary; nationwide30 asserted PASS. Phase C: top overview selects up to eight existing validated/cited sentences across business, leadership, location, finances, jobs, dated activity and changes; remaining sentences remain available. Sparse profiles are never padded. 41 focused tests pass.

2026-10-18T02:47:08+05:30 — Phase C overview committed as 535-style checkpoint (see git log for exact SHA). Visual review found a pre-existing header label issue: role-entity deleted attributes were included by substring matching. Header now restricts legal-status chips to the three company identity fields; role facts remain in their section.

2026-10-18T02:48:02+05:30 — Correction: Phase C overview commit is 846c45d; narrow legal-status UI fix a5800a8. Full suite active. Reserve tuning A4 does not meet the requested 30 s >=80% research threshold, so it will be dropped under the master prompt fail-and-drop rule; bulk loader and bounded missing-row fix are independent and retained.

2026-10-18T02:49:34+05:30 — Phase C full suite 486 passed in 89.87 s before A4 drop. A4 reserve tuning now reverted independently because its 30 s >=80% research gate failed; 23 reserve/cancellation/bulk checks pass on the reduced candidate. The measured 120 s improvement is historical experimental evidence, not shipped behavior.

NEXT: Commit A4 drop, add conservative newly-checked-page refresh classification, then run final full/100/24 gate and freeze.
