# Event-loop refactor equivalence gate

The offline replay uses the accepted 300-company seed-20261014 output and its saved official response bodies. No live requests were made. Pending W3 field additions were preserved separately and excluded from this refactor.

| Check | Result |
|---|---|
| Companies, membership/order | 300, identical |
| Claim IDs, values, availability, evidence references and order | Identical |
| Evidence spans, content hashes, locators and metadata | Identical |
| Synthesis bytes | Identical for all 300 |
| Site output | All 606 files byte-identical |
| Company changes from replay against accepted output | 0 |
| Unit suite | 239 passed |

Official extraction replay reproduced 3,897 available identity claims, 1,208 role claims, 262 subunit claims and 2,006 accounts claims. Recorded observation times are used for replay. Website, hiring and activity facts from the accepted source output remain unchanged; no new discovery is performed by this saved-source gate. Site rendering compares the accepted output using the pre-refactor renderer with the replay using the current renderer.

CPU and disk work is moved off the research event loop: official extraction, HTML parsing/proof/extraction, activity XML parsing, template synthesis, evidence hashing/storage, finalization and output/site generation. JSON pointer bounds are indexed once per source response; the strict replay confirms exact excerpt equivalence. NAV header scoring runs on its own serial worker while paging continues. Shutdown waits for in-flight worker state before settling coverage; the existing request, time, evidence, URL and publication rules remain in force.

Each real NAV feed request records response-header timing, response completion, actual request-header send timing and its gap from the previous completed response. A 100 ms heartbeat records whole-run event-loop lag, including its p95. The next diagnostic is a fresh-state cold 100 with a 2,400-second budget; performance targets are a feed inter-request gap below 0.2 seconds and loop-lag p95 below 100 ms. No cold-performance pass is claimed here.

The site regression test covers scalar role metadata. Existing tests confirm a site failure is reported while preserving envelopes and CLI exit zero. The W2 baseline's original site error remains in its historical report.
