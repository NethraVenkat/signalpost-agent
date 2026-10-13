# 100-company smoke summary

Measured 2026-10-13T13:21:48.070186Z. This is an offline replay of saved official registry responses, not a fresh live API run. The same 100-company input and bulk excerpt are processed with the current implementation; response bodies are supplied through a mock HTTP transport. Raw envelopes and bodies are intentionally excluded from this report.

| Check | Result |
|---|---:|
| Input companies / validated ordered envelopes |100 /100|
| Handled / unhandled exceptions |0 /0|
| Deadline hits |0|
| Section availability |373 available,27 checked unavailable|
| Available claims independently verified |2139|
| Matching source-body hashes |375|
| Whole-run runtime |32.265s|
| Companyp50 /p95 /max (mock transport) |0.015 /0.016 /0.063s|
| Simulated HTTP attempts / actual outbound requests |300 /0|
| Output size / decimalKB per company |5028593bytes /50.286|
| Original supported claim IDs preserved |yes|
| Rerun company / observation changes |0 /0|
| Provider cost |$0|

The total runtime includes streamed bulk preparation, model validation and output writing; per-company times exclude that preparation. Mock transport timings do not predict live latency. Verification checked exact membership/order, schemas, actual stored hashes, evidence spans and both rerun event categories.

[Machine-readable summary](smoke-100-report.json) contains metrics only. [Evaluation guide](../docs/EVAL.md) explains how to run a live smoke test and strict output verification.
