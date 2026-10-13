# 100-company live smoke summary

Measured 2026-10-13T19:02:10.468494Z; fresh seed 20261017. Implementation commit `9c8a523d3cfa90cb5f6e76b48ab2796ee822c5ba`. All source features and the offline site were enabled. Provider cost was $0; no model calls were made. Raw company envelopes, source bodies and per-request logs are excluded from publication.

```sh
uv run signalpost run --organisations state/downloads/release100.jsonl --bulk state/downloads/release100.csv --output out/release100.jsonl --report dev-notes/release100-report.json --websites --hiring --public-activity --synthesis template --envelope-shape contract --site-dir dev-notes/site-release100 --expected-count 100 --time-budget-seconds 2400
```

The input and bulk excerpt were prepared with the hash-checked universe sampler and official bulk extractor described in [EVAL](../docs/EVAL.md#sampling-and-bulk-preparation). Paths in the command name local generated artifacts.

| Check | Result |
|---|---:|
| Input records / ordered validated envelopes | 100 / 100 |
| Handled / unhandled exceptions | 0 / 0 |
| Deadline hits | 0 |
| HTTP requests / amortized per company | 1134 / 11.340 |
| DNS resolver invocations | 586 |
| Reported runtime | 343.234 s |
| Company p50 / p95 | 332.859 / 332.890 s |
| NAV pages / feed seconds / total seconds | 378 / 193.203 / 332.875 |
| NAV feed complete | true |
| Output size | 5562306 bytes |
| Provider cost | $0 |

| Information type | Companies with supported information / 100 |
|---|---:|
| legal identity | 100 |
| accounts | 99 |
| roles | 100 |
| subunits | 70 |
| official website | 6 |
| social profiles | 3 |
| fresh job ads | 0 |
| website activity | 4 |
| registry activity | 11 |
| public activity | 15 |
| website self description | 4 |
| synthesis | 100 |

| Source section | Available | Checked unavailable | Failed | Blocked | Not applicable | Ambiguous |
|---|---:|---:|---:|---:|---:|---:|
| identity | 100 | 0 | 0 | 0 | 0 | 0 |
| roles | 100 | 0 | 0 | 0 | 0 | 0 |
| subunits | 70 | 30 | 0 | 0 | 0 | 0 |
| accounts | 99 | 0 | 1 | 0 | 0 | 0 |
| website | 6 | 82 | 6 | 1 | 0 | 5 |
| hiring | 0 | 89 | 11 | 0 | 0 | 0 |
| activity | 4 | 2 | 6 | 1 | 82 | 5 |

The independent verifier passed ordered membership, schema, stored-body hashes, verbatim evidence spans and cited summary checks. Incomplete sources remain explicitly failed or blocked; a complete NAV header index does not establish complete detail coverage. These measurements are sample observations, not an official score or a guarantee about unknown evaluator budgets. The saved legacy proxy scorer expects a different evidence dictionary and does not parse the canonical list; official shape acceptance remains open.

[Machine report](smoke-100-report.json) contains aggregate states, coverage and measured NAV/runtime/request metrics.
