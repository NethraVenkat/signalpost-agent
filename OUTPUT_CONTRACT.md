# Output contract

Write UTF-8 JSONL with exactly one terminal JSON object per input record, in input order. Preserve duplicate and invalid input records. Normalize organisation identifiers as strings. An unreadable input file is an explicit error because its membership cannot be determined.

Required top-level keys:

| Key | Type | Meaning |
|---|---|---|
| `organisation_number` | string | Normalized input identifier, including an invalid identifier on its failed envelope |
| `run` | object | `run_id`, `started_at`, `completed_at`, `terminal_status`; timestamps are UTC |
| `claims` | array | Values and explicit availability, confidence and evidence links |
| `evidence` | array | Source receipts referenced by claims |
| `changes` | array | Verified changes against the previous supported snapshot |
| `errors` | array | Section, reason code and explanatory message |
| `operations` | object | HTTP attempts, runtime in milliseconds and third-party USD cost |

The default union form also includes reference-style `run_id`, `state`, timestamps, `modules` and `profile`. These mirrors do not add facts. Separate profiles are written only when `--profiles-output` is provided.

Each claim contains `field`, `value`, `availability`, `confidence` and `evidence_ids`. Availability is one of `available`, `not_available`, `blocked`, `not_applicable`, `ambiguous`, `failed`. An available claim must reference existing evidence. Unsupported values are `null`; do not substitute zero. Zero is valid only when explicitly supported by the source.

Every evidence record contains `id`, `source_url`, `source_class`, `retrieved_at`, `content_sha256` and `claim_span`. Published claims retain a bounded verbatim excerpt or precise locator, exact-company proof and source period where applicable. Hashes address saved original source bytes. A retrieval date is not an effective date.

`run.terminal_status` is `completed` or `failed`. Completion means processing reached a terminal result; section failures remain explicit. If every section failed, was blocked or remained ambiguous, the terminal status is `failed` and reference `state` cannot be `complete`. Invalid identifiers use `submission_error`. Other reference states are `complete`, `not_applicable`, `not_found`, `blocked_policy`, `blocked_robots`, `source_error` and `budget_exhausted`.

The batch report separately exposes `run_status` (`completed`, `partial`, `failed`, `aborted`), `successful_http_responses`, `available_claims`, `counts_by_state`, warnings and budget limits. Failed/aborted batches exit non-zero. A report must not treat well-formed empty failure envelopes as successfully researched companies.

Validation: `src/signalpost/models/shapes.py` checks schemas and evidence references. `scripts/verify_output.py` checks ordered membership, saved-body hashes, exact excerpts, company attribution, financial arithmetic and cited synthesis without network access.

This extends the minimal contract in the [official starter kit](https://www.builderr.ai/signalpost-starter-kit.tar.gz); extra union keys preserve reference compatibility.
