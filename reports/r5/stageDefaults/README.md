# Evaluator defaults: 8/13

The separate queued change makes the tested 8/13 website caps both CLI and library defaults and enforced maxima. Lower caps are supported. Website/hiring/public website activity remain opt-in; identity proof, DNS nominations, robots/terms, host limits and $0 budget are unchanged.

`tests/test_r5_defaults.py` exercises exactly the seven official flags at the CLI-to-Config boundary and checks limits; the existing Stage U test exercises the real CLI/runner/site with the seven flags against mocked sources. The complete green pytest log is `tests.txt`.

After the defaults commit, run `python reports/r5/stageDefaults/measure.py` from the project root with the project environment. It uses a new run ID, verifies frozen input hashes, sends exactly seven flags (no cap or enrichment flags), and uses a fresh output directory as the working directory so the default relative state/ is also fresh. It refuses to overwrite a prior run. The environment disables paid search, and the CLI's default total provider budget is $0. Original command/config, report, state counts, source verification and comparisons are saved here; see `../OVERNIGHT2_SUMMARY.md` for the final result. Raw bodies/output stay under `.data/r5/evaluator-defaults-run/`.
