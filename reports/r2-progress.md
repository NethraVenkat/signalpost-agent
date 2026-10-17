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

NEXT: Commit A4 as an independently measured change, then run Phase A full suite, 100-company smoke and 24-company comparison before any RC tag.
