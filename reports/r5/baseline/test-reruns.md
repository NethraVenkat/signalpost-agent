# Isolated baseline test reruns

Source commit: `7eb9bba21d4225d0008d22c112d0d5a0abe9a38e`.
Environment: Windows, CPython 3.12.15, pytest 9.1.1, uv frozen environment.

The original full-suite baseline was **531 passed, 1 failed in 171.79 seconds**.
The failure was `tests/test_link_evidence_spans.py::test_large_boolean_attribute_does_not_stall_link_localization`, whose child process exceeded the existing five-second timeout.

Each requested rerun used the exact command below, sequentially, without a concurrent pytest run:

```powershell
uv run pytest -k test_large_boolean_attribute_does_not_stall_link_localization
```

| Run | Result | Selected | Deselected | Pytest elapsed seconds |
|---|---|---:|---:|---:|
| 1 | passed | 1 | 531 | 1.96 |
| 2 | passed | 1 | 531 | 7.57 |
| 3 | passed | 1 | 531 | 1.30 |

All commands exited zero. Pytest elapsed time includes collection and is not the child process's timeout measurement. Per the requested decision rule, the original failure is recorded as machine-load related. No test, timeout or application source was changed.
