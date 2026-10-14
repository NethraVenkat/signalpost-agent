# Registry coverage: saved-source 300

Seed 20261014, accepted saved response bodies only; zero live requests. The private field inventory records every observed JSON leaf/CSV column, frequency and prior extraction coverage. Link metadata and personal identifiers/birth/death dates are excluded.

| Available official claims | Before | After |
|---|---:|---:|
| Identity | 3,897 | 8,654 |
| Roles | 1,208 | 3,493 |
| Subunits | 262 | 2,063 |
| Accounts | 2,006 | 6,579 |
| Total | 7,373 | 20,789 |

Existing official claims retain identical IDs, values and evidence spans/hashes/locators. Additional claims cover reported registry flags/dates/contact and sector/capital metadata, subunit dates/contact/address/registration metadata, role metadata and reported financial line items. Missing optional attributes are omitted, not invented as zero; reported false and zero remain facts. Financial values are never calculated, and exact parent, latest entity period and currency/unit rules are unchanged. New extractor coverage is an observation change rather than a company event.

Independent verification passes 300 envelopes, 20,998 available claims including unchanged non-registry families, 1,170 source bodies and 2,426 cited sentences: zero unverified values and zero synthesis drops. Replaying against the accepted output creates zero company changes.

The full extraction/output rerun is byte-identical using recorded observation clocks (SHA-256 `bb2913c2fcede05d0a397e15eb1203fafd9a24bab4674f41844275b2af49a69d`). All 606 generated site files also match between repeated renders.

Additional role/subunit metadata uses the existing offline per-company data file, rendered with text nodes and the same source panels. All attributes remain accessible offline. HTML limit stays 250 KB: largest HTML 78,881 bytes; largest data file 173,128 bytes; total site 32,236,115 bytes. A real file-protocol browser check verifies 121 metadata facts on a sampled profile and a working verbatim source panel. Site generation errors remain isolated from envelope output and CLI exit status.
