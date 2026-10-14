# Cold 1000-company release check

Seed 20261018, implementation `de2f6fa29f8ea80f1cc654460dc0672ca0f155c7`, measured 2026-10-14T06:33:03.155607Z. A fresh empty state directory was used; the declared shipped NAV discovery index was supplied. No runtime responses were copied. Search was not configured; provider cost $0. No model calls. Historical full-feed 304 measurements are warm-cache results and do not describe this method.

```sh
uv run signalpost run --organisations batch.jsonl --bulk registry.csv --output envelopes.jsonl --profiles-output profiles.jsonl --report report.json --site-dir site --websites --hiring --public-activity
```

Default budget 2,400 seconds; NAV cap min(900 seconds, 40% of budget). Omit bulk for live identity fallback. Both output files preserve input-record order; the offline site opens under file://. Raw company/source artifacts remain private.

| Check | Measured |
|---|---:|
| Ordered valid envelopes | 1000 |
| Supported claims / verified source bodies / cited sentences | 69007 / 3846 / 8020 |
| Unverified values / dropped sentences | 0 / 0 |
| Handled / unhandled exceptions / deadline hits | 0 / 0 / 0 |
| Runtime | 268.875 seconds |
| HTTP / DNS resolutions | 5074 / 6809 |
| Time / request headroom | 88.80% / 74.63% |
| Envelope bytes / raw profile bytes | 140000335 / 95473075 |
| Output reductions | 0 |
| Site bytes / largest HTML / largest data file | 106754783 / 69326 / 122134 |
| NAV index bytes / age days | 403768 / 0.085875 |
| Cold forward feed pages / seconds / decoded MB | 2 / 2.547 / 0.279161 |
| Feed seconds per page | 1.273500 |
| Feed complete / header processing complete | True / True |
| Candidates / live details / published ads / ad companies | 9 / 9 / 9 / 6 |
| Hiring failed | 0.0% |
| NAV total / cap | 141.312 / 900 seconds |
| Whole-run loop lag p95 | 88.000 ms |

Index `nav-20261014T042640.758720Z-v1`, built 2026-10-14T04:26:40.758720Z: 9,015 active discovery entries, 5,769 employers, 6,791 disk-seeded and 2,224 fetched entries, zero failed build details. Every published ad requires current live exact employer proof. MB denotes decoded decimal response bodies, not compressed wire bytes. Unknown forward-item trading names remain a nomination risk; fallback-name diagnostics are not a claim of national exhaustiveness.

| Coverage | Companies |
|---|---:|
| legal identity | 1000 |
| accounts | 998 |
| roles | 997 |
| subunits | 767 |
| official website | 47 |
| social profiles | 29 |
| fresh job ads | 6 |
| website activity | 4 |
| registry activity | 114 |
| public activity | 118 |
| website self description | 38 |

| Section | Available | Not available | Failed | Blocked | Ambiguous | Not applicable |
|---|---:|---:|---:|---:|---:|---:|
| identity | 1000 | 0 | 0 | 0 | 0 | 0 |
| roles | 997 | 3 | 0 | 0 | 0 | 0 |
| subunits | 767 | 233 | 0 | 0 | 0 | 0 |
| accounts | 998 | 0 | 2 | 0 | 0 | 0 |
| website | 47 | 759 | 113 | 5 | 76 | 0 |
| hiring | 6 | 994 | 0 | 0 | 0 | 0 |
| activity | 4 | 29 | 127 | 5 | 76 | 759 |

Union 140,000,335 bytes versus contract 123,854,273: ratio 1.130363, below 1.25. No company reduced. Nine published ads independently audited, zero doubtful. The two bulk-missing inputs were retained and resolved through live identity fallback.

**Open performance risk:** NAV total 141.312 seconds misses the 120-second target by 21.312 seconds. First detail starts at 134.594 seconds as the listed-subunit scopes become ready; no qualifying detail started during the short forward read. The full batch finishes within 1,200 seconds, so the provisional 900-second cap is retained. No timing is subtracted or redefined to meet a target.

Incomplete sources remain explicit failures/abstentions. Partial NAV discovery never establishes checked absence. Earlier warm benchmarks, the failed cold W2 baseline and missed diagnostic targets remain documented. Measurements share the workstation; they do not promise isolated hardware performance or final evaluator acceptance.

[Machine report](release-1000-report.json).
