# Committed gap evidence

`evidence.json.gz` is a 686,790-byte bounded packet, SHA-256
`7449c9dcbb4d2e915b3d2c960e7a7ed90baeafeb349d1903d66657458c4c7918`.

It contains ordered input membership and available-field inventories for both
measured cohorts, plus every new available consolidated/state-aid claim, its
receipts and its complete saved evidence body. All 772 new claims are re-derived:
516 consolidated financial line claims and 256 state-aid award claims, backed by
265 distinct bodies. State-aid record membership is additionally checked against
the committed official bulk extract. Financial records retain their original
API response bytes; the state-aid bodies are the exact non-personal extract
records whose CSV hash and source row lineage are documented in G3.md.

This packet excludes legacy claim values, role source text and company HTML.
It reproduces all field counts, but does not independently source-check legacy
values, remeasure wall time, establish precision, or recreate the historical
sampling universe. It does not make the failed 500-company site gate pass.

After `uv sync --frozen`, no network or local research directories are needed:

```sh
uv run python reports/r5/gaps/evidence.py replay --bundle reports/r5/gaps/evidence.json.gz
```

The replay blocks network access and binds source verification to the installed
checkout. It passed against the clean verification clone at `f740933`, with the
helper and packet supplied as explicit input files; no `state`, `out` or `.data`
run directories were present inside that clone and no pytest ran there.
[Result](evidence-replay.json) | [Execution and limits](evidence-replay-execution.json)
| [Input order / overlap](evidence-membership.json).

Official financial and state-aid evidence: contains NLOD 2.0 data provided by
Brønnøysundregistrene, with source URLs and retrieval times preserved. This
project filtered and reformatted the state-aid extract; no endorsement is
implied. [Source terms and attribution](../../../docs/SOURCES.md).
