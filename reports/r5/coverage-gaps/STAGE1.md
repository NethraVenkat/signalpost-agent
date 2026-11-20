# Stage 1: robots and live connectivity

The website crawler combines all matching robots groups. It uses wildcard groups when the crawler has no specific group and resolves overlapping rules by specificity. Empty directives still separate groups. The same policy reader serves the official clients that already consult robots. Existing sitemap declarations and crawl delays remain available.

Replayed the nine paths from the saved S6 request log against the original robots response, SHA-256 `f746e6bb107cdcef4d19a5903b1491098eedfcedd21f68bcdbc12311206c8195`. Before, all nine reached the publisher and returned HTTP 200. After, all nine were denied locally and only the mocked robots request ran. No published S6 claim cites that host.

The seven-flag CLI returns 1 when the completed report records zero successful HTTP responses. In the bulk-anchored outage fixture it preserves a partial report and one terminal envelope. A single-section failure and a transient error followed by recovery both return 0. The offline site command retains its previous exit behavior.

The saved S6 baseline has 38 verified website sections across 500 companies and 76,892 published claims. This stage adds no claims. It measures the changed access and exit behavior with stored and synthetic receipts. New live coverage is measured in Stage 2.

Stored-evidence gate at seed `202611200628`: the same 200 claim IDs replayed as supported, with zero contradictions and zero missing or mismatched blobs. Two-sided Wilson 95% lower bound **98.12%**.

Validation: full suite **1,519 passed**. Separate privacy and profile-size checks **17 + 2 passed**. The first full run exposed a missing sitemap accessor in the replacement policy. The corrected reader preserves sitemap handling, and the full rerun passed.
