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
| Largest rebuilt profile HTML | 249,428 bytes (<250,000) |
| Additional HTTP requests, including cached | 0 |
| New claims / new evidence records | 0 / 0 |
| Local timeline projection | 2.38 s |
| Full offline site render | 22.62 s |

The saved S1-derived final500e envelopes were used without a live rerun. Their original file hash is unchanged. These local timings are not a new live-run budget measurement. [Machine-readable measurement](measurement.json) and [offline driver](measure.py); the latter requires the retained saved envelopes. Source claims/evidence were compared before/after and remain unchanged.

Tests cover precision, invalid dates, own-evidence completeness/inheritance, omission under two claims, stable ordering, no source-name copying, no retrieval-date inference, duplicate filed-year suppression, network interception, briefing section, tampering and the local-data overflow path. Full pytest: **1,506 passed in 901.62 seconds** ([receipt](pytest.txt)). Privacy checks: **17 passed in 8.28 seconds** across the no-home-path and public-name guards ([receipt](privacy.txt)). The suite's initial run had one refresh-equivalence failure caused by equivalent timezone representations in S1 event dates; the comparison now normalizes instants for status-event meaning while preserving the original date and evidence text. The corrected full suite passed. No tags or push.
