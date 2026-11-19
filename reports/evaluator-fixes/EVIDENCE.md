# Committed offline evidence

`evidence.zip` is a 6,989,192-byte extract of the **documented 100-company run after fixes 1–2**, before the website-window and robots corrections. It is a frozen regression fixture, not a measurement of the final revised agent.

SHA-256: `3a1ea042a360e69051aa5080e87558b487ffe37234d43149162b3b6c75880272`.

From a fresh clone with only the documented installation:

```sh
uv run python scripts/replay_committed_evidence.py
```

No `.data/`, previous `state/`, network, credentials or local run directories are required. The script reads the committed archive and uses an automatically removed temporary directory.

| Check reproducible from committed bytes | Scope |
|---|---|
| Membership, envelope schemas, evidence references and missing-value rules | All 100 saved envelopes |
| Available claims by family, websites and social URLs | 13,566 claims, 6 websites, 7 social URLs |
| HTTP attempt count and per-host totals | 985 attempts, recalculated from the saved request log |
| Deadline-affected companies | 96, recalculated from saved envelope errors |
| Original-source hashes, verbatim spans, company ownership, financial values and arithmetic | Three identity/accounts extracts: 314 claims, nine original source blobs |
| Cited synthesis and briefing support | Three extracted companies; zero unsupported values |

The full saved-output count checks establish what was emitted. **They do not independently establish the correctness of every published website, social profile, role or other external claim.** Original source bodies are bundled only for the three official identity/accounts examples. The archive deliberately excludes raw company HTML and role birth-date records. Live timing is a retained historical receipt, not a performance result that offline replay can reproduce.

The historical final500c source bodies and its full 500-company run are not included. Its archived measurements remain separately labelled historical; this fixture does not turn them into independently replayed evidence.

## Sources and licences

The original raw extract bodies are Brønnøysundregistrene Enhetsregisteret and Regnskapsregisteret data under [NLOD 2.0](https://data.norge.no/nlod/no/2.0). Attribution: Brønnøysundregistrene. Their source URLs, retrieval times, periods, exact excerpts and SHA-256 values remain in the envelopes. The extract selects companies and the identity/accounts families and regenerates supported summaries; it is not represented as an unchanged complete research envelope.

Other saved factual outputs and short excerpts retain their original source attribution and terms in [SOURCES](../../docs/SOURCES.md). The repository's MIT licence does not replace third-party terms. Historical source-policy behavior is preserved in the baseline fixture: its state-aid requests preceded the fail-closed robots correction.

## Rebuild from a new saved run

```sh
uv run python scripts/build_evidence_extract.py --envelopes out/run/envelopes.jsonl --state out/run/state --output reports/evaluator-fixes/evidence.zip
uv run python scripts/replay_committed_evidence.py
```

Rebuilding requires a retained run, but **checking the committed archive does not**. The builder verifies selected source hashes and rejects local home-directory paths and personal birth-date fields in the original-body extract. After rebuilding, update this receipt's size, hash, scope and measured counts.
