# CI context validation

Removed runner.temp from job-level env. The smoke run step derives LIVE_WORK from shell RUNNER_TEMP and records it in GITHUB_ENV; verification and artifact upload reuse that variable. Existing seven flags, fresh state, scaled time budget, timeout and artifact behavior remain.

Local validator: uvx --from actionlint-py actionlint .github/workflows/ci.yml (actionlint 1.7.12). Exit 0, no diagnostics. Exact version/commands/workflow SHA-256: validation.json. Initial installation/build warnings in actionlint.txt belong to uv packaging; workflow-stdout.txt and workflow-stderr.txt are empty for the clean validation. Pytest full gate: pytest.txt. No remote GitHub run or push performed.
