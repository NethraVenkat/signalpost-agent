# Cold 100-company release check

Seed 20261017, implementation `de2f6fa29f8ea80f1cc654460dc0672ca0f155c7`, measured 2026-10-14T06:36:29.619139Z. A fresh empty state directory was used; the declared shipped NAV discovery index was supplied. No runtime responses were copied. Search was not configured; provider cost $0. No model calls. Historical full-feed 304 measurements are warm-cache results and do not describe this method.

```sh
uv run signalpost run --organisations batch.jsonl --bulk registry.csv --output envelopes.jsonl --profiles-output profiles.jsonl --report report.json --site-dir site --websites --hiring --public-activity
```

Default budget 2,400 seconds; NAV cap min(900 seconds, 40% of budget). Omit bulk for live identity fallback. Both output files preserve input-record order; the offline site opens under file://. Raw company/source artifacts remain private.

| Check | Measured |
|---|---:|
| Ordered valid envelopes | 100 |
| Supported claims / verified source bodies / cited sentences | 6861 / 381 / 799 |
| Unverified values / dropped sentences | 0 / 0 |
| Handled / unhandled exceptions / deadline hits | 0 / 0 / 0 |
| Runtime | 47.703 seconds |
| HTTP / DNS resolutions | 467 / 608 |
| Time / request headroom | 98.01% / 76.65% |
| Envelope bytes / raw profile bytes | 13886929 / 9439042 |
| Output reductions | 0 |
| Site bytes / largest HTML / largest data file | 10613333 / 94088 / 177375 |
| NAV index bytes / age days | 403768 / 0.089729 |
| Cold forward feed pages / seconds / decoded MB | 2 / 2.265 / 0.285160 |
| Feed seconds per page | 1.132500 |
| Feed complete / header processing complete | True / True |
| Candidates / live details / published ads / ad companies | 0 / 0 / 0 / 0 |
| Hiring failed | 0.0% |
| NAV total / cap | 12.359 / 900 seconds |
| Whole-run loop lag p95 | 25.000 ms |

Index `nav-20261014T042640.758720Z-v1`, built 2026-10-14T04:26:40.758720Z: 9,015 active discovery entries, 5,769 employers, 6,791 disk-seeded and 2,224 fetched entries, zero failed build details. Every published ad requires current live exact employer proof. MB denotes decoded decimal response bodies, not compressed wire bytes. Unknown forward-item trading names remain a nomination risk; fallback-name diagnostics are not a claim of national exhaustiveness.

| Coverage | Companies |
|---|---:|
| legal identity | 100 |
| accounts | 99 |
| roles | 100 |
| subunits | 70 |
| official website | 6 |
| social profiles | 3 |
| fresh job ads | 0 |
| website activity | 3 |
| registry activity | 11 |
| public activity | 14 |
| website self description | 4 |

| Section | Available | Not available | Failed | Blocked | Ambiguous | Not applicable |
|---|---:|---:|---:|---:|---:|---:|
| identity | 100 | 0 | 0 | 0 | 0 | 0 |
| roles | 100 | 0 | 0 | 0 | 0 | 0 |
| subunits | 70 | 30 | 0 | 0 | 0 | 0 |
| accounts | 99 | 0 | 1 | 0 | 0 | 0 |
| website | 6 | 80 | 8 | 1 | 5 | 0 |
| hiring | 0 | 100 | 0 | 0 | 0 | 0 |
| activity | 3 | 2 | 9 | 1 | 5 | 80 |

Union, contract and reference envelope files independently verify with identical values and provenance. The raw profiles match their envelopes exactly and parse in the unmodified kit scorer, run read-only from scratch outside the repository: foundation 14.96/15, daily terminal batch 4/4, raw 18.96/100, awardable 0, qualification false. Other side reports remain deliberately unqualified, not fabricated; latency p95 25,203 ms still exceeds its 10,000 ms threshold. These are proxy measurements, never an official score.

Incomplete sources remain explicit failures/abstentions. Partial NAV discovery never establishes checked absence. Earlier warm benchmarks, the failed cold W2 baseline and missed diagnostic targets remain documented. Measurements share the workstation; they do not promise isolated hardware performance or final evaluator acceptance.

[Machine report](smoke-100-report.json).
