OVERNIGHT MASTER PROMPT: Signalpost revision 2 (8 hours, unattended)

ROLE: You are my lead engineer and strictest judge for the Builderr "Signalpost" challenge (builderr.ai/challenges/signalpost). I'm asleep. Work autonomously for up to 8 hours, then leave a morning report. Do not wait for me. Do not ask questions; take the safest reasonable choice and record it.

====================================================================
0. HARD RULES (never break these)
====================================================================
- Accuracy over volume. Zero new wrong-company facts. Never weaken exact org-number proof, identity matching, robots, SSRF/DNS policy, or request budgets to gain coverage.
- Never publish name-only or similarity-only matches. Search/guessing produces CANDIDATES; only exact org-number proof (or exact registered-subunit proof, labelled) publishes.
- No unofficial LinkedIn/Meta/Glassdoor/Indeed/Google clients; never fetch social platforms. No LLM, no paid API, no credential tied to my own account in the run path. Cost stays $0.
- Never convert missing to zero. Every input → exactly one terminal envelope, in input order.
- Don't touch `main` or tag `v1.0.0` (submitted, 3944c89). Work on branch `revision/r2`, created from `revision/r1` @ a05ffae.
- One change per commit. No Claude/AI attribution in commit messages or PRs.
- Don't send emails, don't delete anything outside the repo's out/ and reports/ folders, don't change global git config.
- Keep claim IDs stable: no change may alter canonical values of existing claims (Step 3 of r1 was reverted for this reason).
- If a step fails its gate and can't be fixed within its time box, revert it and move on. A smaller clean release beats a bigger broken one.

====================================================================
1. CONTEXT (what's true now)
====================================================================
- Submitted: v1.0.0 @ 3944c89. Scoring: recall 50 (per external family: 70% companies covered + 30% facts), precision/evidence 30, synthesis 12, UX 8. Qualify at 65. Leader 70.43 (recall 35.77, synthesis 7.2, UX 0). Leaderboard synthesis moves in steps of 2.4 and UX in steps of 1.6, which suggests 5 pass/fail checks each (inference). Almost nobody scores UX.
- Builderr's own sample site (builderr.ai/signalpost) organises profiles into: Company brief / Latest financials / Who runs it? / Working here / Recent activity; has search (⌘K), a directory sorted by "Most data found" or A–Z, an "All five areas" filter, "Check the evidence", and an "Ask Signalpost" box answering only from shown sources; missing evidence stays missing.
- r1 @ a05ffae (local, not shipped): safe changes worth keeping — NAV-first + retained verified jobs after deadline, branch-site label, footer recovery, email-domain label, 8-candidate cap, social labels, HTML activity fallback with dedupe, short-budget reserve. Coverage vs baseline: websites 58→58, hiring 6→6, activity 7→9, social 39→40.
- Known issues: (a) nationwide bulk file + 30 s budget loses ALL identity (bulk load ~40 s happens inside the deadline); (b) refresh marks 6 recovered facts as material changes; (c) SØRARKITEKTER evidence span falls back to document start (escaped JSON-LD URL); (d) two auditor false positives (own EHF invoice number; deleted flag vs deletion date); (e) short budgets use only ~50% of the budget (reserve too conservative); (f) legal-name domain guessing is a dead end (3,919 tries → 24 sites; 3,094 NXDOMAIN).

====================================================================
2. TIMELINE (IST, approximate; keep a release candidate ready at every checkpoint)
====================================================================
- T+0:00–0:30  Phase 0: setup, inventory, progress log
- T+0:30–2:00  Phase A: robustness → RC-A (quick gate)
- T+2:00–4:30  Phase B: UX → RC-B (quick gate)
- T+4:30–5:30  Phase C: synthesis → RC-C (quick gate)
- T+5:30–6:30  Phase D: brand-name website discovery → keep only if net positive and clean
- T+6:30–8:00  Phase E: full release gate + feature audit on the best candidate, push branch, CI, morning report
If behind schedule: skip Phase D first, then trim optional UX items (Ask box, compare) — never skip Phase E.

====================================================================
3. PROGRESS LOG (mandatory)
====================================================================
Maintain reports/r2-progress.md: after every commit, append time (IST), commit SHA, step, result, and what's next. After each phase, tag a local candidate (rc-a, rc-b, rc-c, rc-d) ONLY if its quick gate passed, and note it in the log.

====================================================================
4. GATES
====================================================================
QUICK GATE (after each phase, ~15 min):
- Full test suite passes.
- 100-company smoke run (one command, JSONL + CSV): 100 envelopes in order, exit 0, site builds.
- 24-company audit baseline: no code-caused lost claim IDs, no schema change.
- Site checks for that phase (see each phase).

FULL RELEASE GATE (Phase E only):
- Five 1,000-company runs on the frozen SHA (same 1,000 inputs + 999-row CSV used before): normal 2,400 s, 30 s, 120 s, 600 s, 3,000-request cap → each exactly 1,000 envelopes in order, exit 0, wall ≤ budget + 5 s, all 28,726 identity IDs.
- Nationwide-file runs: 30 s and normal → all 28,726 identity IDs in both.
- Live comparison vs the v1.0.0 baseline: classify EVERY lost claim ID as live-source variance (DNS/HTTP/timeout/robots/registry value change, with evidence) or code regression. Only code regressions block. Report both counts.
- Refresh with retained state: 0 lost IDs, 0 duplicates, 0 false material changes.
- Wrong-company check: reopen the source for EVERY new website claim (or a random 60 if more) plus 20 random existing ones; zero mismatches.
- Stored-source audit: no new flags vs baseline; explain any remaining.
- Clean clone from the pushed branch at the exact SHA → empty venv → `uv sync --frozen` → README one command on 100 companies → pass; commit the smoke report.
- CI green on the pushed branch SHA (push `revision/r2` only; if the workflow only runs on main, run the workflow's commands locally on Python 3.12 and say so).
- Screenshots (Playwright) at 1440 px and 375 px for 3 profiles: one large (Equinor 923609016), one small, one mostly missing data; plus the directory and the compare view.

====================================================================
5. PHASE 0 — Setup (≤30 min)
====================================================================
- Create revision/r2 from revision/r1 @ a05ffae. Confirm main and v1.0.0 untouched.
- Inventory: CLI flags, output schema, site generator, synthesis module, refresh classifier, bulk loader. Record in the progress log.
- Freeze inputs: reuse the existing 1,000-company sample, 999-row CSV, nationwide file, and 24-company batch. Record their hashes.

====================================================================
6. PHASE A — Robustness (time box 90 min; each item its own commit)
====================================================================
A1. Bulk loader: stream the --bulk file (gz or csv) and keep only rows for org numbers in the batch; run it BEFORE and OUTSIDE the crawl deadline; fall back to live lookup only for companies missing from the file. Verify nationwide + 30 s keeps all identity IDs, and measure load time.
A2. Refresh: a claim ID that reappears after existing in prior history = "recovered" (availability change), not material. Verify the 6 known cases.
A3. Evidence span: fix escaped JSON-LD URL localisation (SØRARKITEKTER). Fix the two auditor false positives without hiding real defects; add tests.
A4. Short-budget reserve: replace the percentage reserve with measured output-writing time + 5 s margin; skip the optional site under short budgets and record it. Verify 30 s and 120 s use ≥80% of the budget for research while wall ≤ budget + 5 s, and report hiring/website/activity availability at 120 s before → after.
→ Quick gate → tag rc-a.

====================================================================
7. PHASE B — UX (time box 150 min; model on builderr.ai/signalpost)
====================================================================
Static, self-contained site (no external CDNs), works offline, every page < 250 KB (progressive loading for large companies).
B1. Profile layout in 5 sections, in order:
   1) Company brief: what it does (NACE + verified site description), legal form, status, founded, address, website + company-owned profiles (with relationship labels).
   2) Latest financials: latest filed figures with reporting period; trend vs previous year if history exists; source link.
   3) Who runs it?: CEO, chair, board from official roles, with dates.
   4) Working here: NAV jobs and careers page with dates; registered employee count + period; workplaces/subunits.
   5) Recent activity: dated news/press items + registry changes since the last run.
   Every empty section shows an explicit state with reason: Not found / Blocked / Ambiguous / Not applicable / Failed. Never blank, never zero.
B2. Global search by name or org number on every page (keyboard shortcut "/" and Ctrl/⌘+K).
B3. Directory: sort by "Most data found" and Name A–Z; filters: "All five areas" and per-section availability.
B4. "Check the evidence" on every fact: source URL, retrieval date (UTC), reporting period, evidence span/quote, method (registry / org number on site / registered subunit / NAV), confidence state.
B5. Compare 2–3 companies side by side across the 5 sections (selection persists via URL parameters, not storage).
B6. Responsive and accessible: no horizontal scroll at 375 px, tappable controls ≥ 40 px, readable tables (stacked on mobile), keyboard navigable, visible focus, sufficient contrast; dark mode kept if present.
B7. Optional if time remains: a static "Ask about this company" box that answers only by matching the question to the 5 sections and quoting cited claims; otherwise "Not in the evidence". No LLM.
Site checks: Playwright screenshots at 1440 and 375 for the 3 profiles + directory + compare; page-size report; a test that every fact on a sample profile has an evidence link.
→ Quick gate → tag rc-b.

====================================================================
8. PHASE C — Synthesis (time box 60 min)
====================================================================
Per-profile summary at the top, 4–8 sentences, every sentence cited to claim IDs:
what it does; who runs it; where it operates; latest numbers with period and trend; whether it's hiring; recent dated activity; what changed since the last run; what remains unknown/blocked. Deterministic templates only. Omit a sentence rather than guess. The existing synthesis verifier must report 0 unverified values.
→ Quick gate → tag rc-c.

====================================================================
9. PHASE D — Brand-name website discovery (time box 60 min; keep only if it helps)
====================================================================
D1. Brand candidates per company from data already held: registered subunit names; NAV employer names matched by org number/subunit; Organization name/title from already-verified related sites. Normalise (strip AS/ASA/avd./location suffixes; æ→ae ø→o å→a + IDNA), generate bounded .no/.com candidates.
D2. Publish only with exact org-number proof (or exact registered-subunit proof, labelled). Method: "brand name (source: subunit/NAV/site)".
D3. Measure on the 1,000 cohort: candidates, DNS-resolved, verified, rejected by reason, new website companies. Reopen EVERY new website claim at source; any mismatch → revert Phase D entirely.
D4. Trademark register (Patentstyret, NLOD 2.0): research only — does it need an API key, do records carry owner org numbers, could an offline org-number→brand index be shipped as a declared cache? Write findings; don't build.
Keep Phase D only if new verified websites ≥ 5 and zero mismatches; otherwise revert and record why. → tag rc-d if kept.

====================================================================
10. PHASE E — Full release gate + feature audit (≥90 min, mandatory)
====================================================================
E1. Pick the best candidate (rc-d > rc-c > rc-b > rc-a). Freeze it.
E2. Run the FULL RELEASE GATE (section 4).
E3. FEATURE AUDIT — verify each and record pass/fail with evidence:
   CLI/contract: all 7 evaluator flags; JSONL and text inputs; invalid/8-digit/spaced/non-existent org numbers handled; --expected-count mismatch handled; exit codes meaningful; report JSON includes runtime, requests, cost, warnings.
   Envelopes: exactly one per input, order kept; all 6 availability states used correctly; every claim has source URL, retrieval time, period where relevant, content hash, method, evidence span; no zeros for missing values.
   Sections: identity, accounts, roles, subunits, website, hiring, activity, social — each produces available or an honest state.
   Refresh: idempotent; recovered vs material distinguished; prior evidence preserved.
   Budgets: time and request caps; deadline cancellation safe; site skipped and recorded when needed.
   Site: all Phase B features; page sizes; mobile; evidence on every fact.
   Synthesis: 0 unverified values; all 8 topics covered where data exists.
   Security/rights: no secrets in repo or history (scan); robots honoured; SSRF/DNS pinning on; sources and licences documented (BRREG NLOD 2.0, NAV terms + public token disclosure, website owners' terms); search off by default; no prohibited platforms fetched.
   Reproducibility: pinned uv.lock; clean clone works; README accurate (install, one command, flags, outputs, cost $0, sources, test count).
E4. Update README and docs to match the shipped behaviour (versions, counts, commands). Bump version to 1.1.0.
E5. Push branch revision/r2 (not main). Wait for CI; fix if red (time box 30 min), else note it.
E6. Commit smoke report + gate report + screenshots under reports/r2/; push.

====================================================================
11. MORNING DELIVERABLE: reports/r2/MORNING_REPORT.md
====================================================================
Top of the file, in this order:
1. Verdict: SHIP / SHIP WITH NOTES / DON'T SHIP, and the recommended SHA (branch revision/r2).
2. What's in it vs v1.0.0 (bullets), and what was dropped and why.
3. Coverage table (companies with ≥1 claim, before → after): websites, hiring, activity, social profiles; plus totals.
4. Gate table (every gate: pass/fail + one-line evidence).
5. Feature audit table (pass/fail).
6. Screenshot paths (1440/375).
7. Risks and open issues, honestly stated.
8. Exact commands for me to release in the morning:
   merge revision/r2 → main (fast-forward or merge commit), tag v1.1.0 at the gated SHA, push main and tag, confirm CI green on main.
   (If merging changes the SHA, say so and tell me to wait for CI on main before emailing.)
9. Revision email draft (reply in my thread to submit@builderr.ai): subject "Re: Signalpost v1 Submission - Norwegian Company Research Agent: Revision 2, v1.1.0 (replaces 3944c89)", with commit hash placeholder for the main SHA, smoke report URL, one-command run, models/APIs/licences, cost $0, what changed, verified results.
Also print a 10-line summary in the terminal at the end.

START NOW with Phase 0. Keep going until Phase E is complete or 8 hours have passed; if time runs out, finish Phase E on the best candidate you have.