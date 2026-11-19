# Historical revision references after the privacy rewrite

Repository history was rewritten for privacy after the final500c reports were written. Those reports retain their original revision labels as historical provenance. An old label in a receipt is not a promise that the old object is fetchable from the current branch, and it must not be silently replaced with an unrelated new hash.

| Historical label | Meaning | Surviving reference and assurance |
|---|---|---|
| `2ac8a6b` (`2ac8a6b0efa1a80c8afdd37323253e786a85e6ff`) | Code used for the archived final500c run | `372d4cab17e786479cb27663a463079d71b25f68`, the surviving pre-fix submission at `v1.5.0`. Before the evaluator fixes, a local tree comparison found no differences in `src/`, `tests/`, `scripts/`, `pyproject.toml` or `uv.lock`; later report/README additions do not establish additional live measurements. |
| `06ebe1e` | Historical checkpoint cited by retained receipts | No exact one-to-one mapping independently established. Interpret the receipt in its recorded context; do not assert code equivalence to the revised entry. |
| `b10e531` | Historical checkpoint cited by retained receipts | No exact one-to-one mapping independently established. The surviving pre-fix submission is a reference point, not a substitute proof of this checkpoint. |
| `7eb9bba` (`7eb9bba21d4225d0008d22c112d0d5a0abe9a38e`) | Frozen R5 baseline measurement | Its cohort and readable reports remain under `reports/r5/baseline/`. No exact rewritten commit equivalence is asserted. |

The evaluator fixes are new code changes after `372d4ca`; they are not claimed to have produced the historical final500c numbers. Use the revised commit hash supplied with the current submission and the current [run instructions](SUBMISSION.md).

Historical timings, human-review verdicts and measurements whose original source bodies are absent remain historical assertions. The [committed replay fixture](reports/evaluator-fixes/EVIDENCE.md) states exactly which saved-output counts and original-source checks can be reproduced from the current clone alone.

Generated JSON removed during cleanup is indexed by its original path and Git blob ID in the [pruning manifest](reports/evaluator-fixes/PRUNED_DATA.json). Git history was not rewritten by the evaluator-fix work. Removed historical generated files are not inputs to the committed replay check.
