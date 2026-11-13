# Saved-source refresh proof fixture

Subset: DIGITALIQ AS (918266917), seed 20261113, from the saved Stage C recovery run. manifest.json identifies source run, observation clock, receipt routes/status/content types and SHA-256 hashes. bodies.json.gz contains original response bytes keyed by SHA-256, base64 encoded. No live network or external model is used. build_refresh_fixture.py reconstructs the fixture from retained local receipts; it does not download.

The subset NAV index preserves this employer's saved ad identifier and exact detail response. Original forward feed page bodies were not persisted, so the replay supplies a **synthetic empty completed forward tail**. It supplies no ad fact and is explicitly recorded in execution aliases. This validates removed-ad refresh, not completeness of full-feed discovery. Registry update batch query aliases reuse exact saved batch bytes containing this company.

The harness injects prior output and a fixed observation clock programmatically while invoking the seven-flag CLI. All extraction, proof, refresh, synthesis, budgets and site logic are production code. Offline DNS and transport allow only recorded routes; unknown URLs fail, without network fallback. Offline-only politeness sleep is zero. Each replay has fresh state; only immutable historical proof bodies are carried for verification. No current cache/result is reused.

Seven isolated source interventions are employee count, business address, accounts year, legal name, proven subunit, inactive NAV ad and verified-site HTTP 404. New accounts year is planted test data, not a claim about a real filing. Every scenario is replayed twice. Baseline/unchanged/idempotent and timeout-driven stale carry-forward are checked independently. Precision is at field-event level; recall is at the seven predeclared causal intervention level. This one-company fixture is not a population-wide precision estimate.

Run: `.venv/Scripts/python.exe scripts/refresh_proof_harness.py .data/r5/refresh-new-run` (new directory required). CI: `pytest tests/test_refresh_proof_harness.py`.
