# S2: claim-only dated timeline

A synthesis view, not additional recall. No source, host, HTTP request, cached request, blob read or new evidence/claim is added by timeline construction. Inputs are existing available claims and their attached evidence metadata only. [Exact code-derived field inventory](DATED_FIELDS.md).

The dated section is `run.synthesis.sections.timeline`, mirrored by the existing profile synthesis serialization. Each entry has the original date, explicit year/day/timestamp precision, a fixed name-free label, source claim ID, original evidence IDs and source field. It inherits the complete existing evidence set without creating receipts. Missing URL, UTC retrieval time, SHA-256, locator, span or extraction method causes omission. Timeline verification re-derives the view from the claims and rejects tampered entries.

The section is omitted in the profile if there are fewer than two distinct dated source claims; two date attributes on one role record do not count as two facts. Empty synthesis arrays are not rendered. Year-only filed-copy facts are labelled accounting years, never actual submission dates; accounting-period boundaries and retrieval timestamps are not filing events. Signature/prokura claims without a reported change date create no entry. A filed-year list and its individual year claims are not double counted. Entries sort oldest first with stable tie-breaks and preserve the original date text. Labels contain no person names, claim text, inferred causal account or commentary.

The offline profile contains only a compact Dated records section and local loader target. All entries live in the already-loaded company data file; source buttons resolve the original fact/evidence records. No fetch is added, even on expansion. Fewer than two facts produce no heading or target. The existing HTML overflow path and limit remain unchanged.

## Offline final500e/S1 replay

| Metric | Result |
|---|---:|
| Companies with a timeline | 500 / 500 |
| Median entries, all companies / companies with a timeline | 26 / 26 |
| Total derived entries | 13,415 |
| Largest rebuilt profile HTML before headroom adjustment | 249,428 bytes (<250,000) |
| Additional HTTP requests, including cached | 0 |
| New claims / new evidence records | 0 / 0 |
| Local timeline projection | 2.38 s |
| Full offline site render | 22.62 s |

The saved S1-derived final500e envelopes were used without a live rerun. Their original file hash is unchanged. These local timings are not a new live-run budget measurement. [Machine-readable measurement](measurement.json) and [offline driver](measure.py); the latter requires the retained saved envelopes. Source claims/evidence were compared before/after and remain unchanged.

## Profile headroom adjustment

The effective page budget is now 235,000 bytes, with a 240,000-byte regression ceiling and the original 250,000-byte hard gate. When needed, the renderer defers duplicate Explorer rows, older official records and workplace rows into the existing company-local data file; it also keeps original-source shortcuts available through each existing evidence panel. No fact or evidence record is dropped.

| Rank | Before adjustment | After adjustment |
|---:|---|---|
| 1 | `916329717` — 249,428 bytes | `964389020` — 234,853 bytes |
| 2 | `981400224` — 245,960 bytes | `981400224` — 234,653 bytes |
| 3 | `974529106` — 245,640 bytes | `991095500` — 233,610 bytes |
| 4 | `920203450` — 245,201 bytes | `985335699` — 233,202 bytes |
| 5 | `964389020` — 244,577 bytes | `913939964` — 232,929 bytes |

All 500 rebuilt profile pages are at or below 235,000 bytes. The largest is **234,853 bytes**, leaving 147 bytes under the effective budget and 15,147 bytes below the 250,000-byte cap. The offline audit confirms every local payload retains all expected claim IDs, values, evidence references and evidence records. Rendering took 25.16 seconds; no network call, claim or evidence was added.

Tests cover precision, invalid dates, own-evidence completeness/inheritance, omission under two claims, stable ordering, no source-name copying, no retrieval-date inference, duplicate filed-year suppression, network interception, briefing section, tampering, local-data overflow, and a 240,000-byte site regression guard. S2 full pytest: **1,506 passed in 901.62 seconds** ([receipt](pytest.txt)); original privacy checks: **17 passed in 8.28 seconds** ([receipt](privacy.txt)). After the headroom adjustment, full pytest: **1,506 passed in 988.89 seconds** ([receipt](headroom-pytest.txt)); privacy checks: **17 passed in 6.77 seconds** ([receipt](headroom-privacy.txt)). The suite's initial run had one refresh-equivalence failure caused by equivalent timezone representations in S1 event dates; the comparison now normalizes instants for status-event meaning while preserving the original date and evidence text. The corrected full suite passed. No tags or push.
