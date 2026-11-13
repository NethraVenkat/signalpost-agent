# Stage D ? hiring measurement

Implementation commit: this commit; exact hash will be recorded in the combined D/I summary. No push or publication.

The official-only NAV rebuild completed with 9,511 active ads / 6,012 employers, zero failed details, no disk seed, and 439,336 compressed bytes. Built-at 2026-11-13T08:23:53.796625Z; 10,139 maintenance HTTP attempts / 1,393.25 seconds. This explicit whole-feed maintenance build is separate from evaluator limits; its complete request ledger is index_build.json. The installed gzip SHA-256 is ba4d5df8a8fa4ebae0c9ed77d16bdb55de82632c64b855853d60bd61b2a36a43.

Diagnosis: the stale bundled index forced full-feed fallback. Frozen B had 11 nav_name_unusable hiring failures; daily B had six nav_detail_cap failures. The builder itself incorrectly inherited a zero-input daily request clamp. Its existing explicit maintenance allowance is now restored without changing daily Budget. Fresh declared-index runs use two forward pages and mandatory live exact-employer details; neither sample has a hiring failure. A complete declared index is not proof that no vacancy exists anywhere.

Careers: current exact-number VERIFIED site only, own navigation/footer link chain, seven ATS roots, own JobPosting title, non-expired/current date or title-linked explicit-open status. No name publication, no group-site postings, no query-dependent ATS URL reconstruction. Four pages at most inside unchanged cumulative robots/HTTP/global limits. Unsupported HTML layouts are withheld. SPEDIFY?s linked open application invites future opportunities and does not establish an active titled vacancy; no claim was invented.

| Metric | B frozen | D frozen | B daily | D daily |
|---|---:|---:|---:|---:|
| job_ad_companies | 0 | 0 | 0 | 1 |
| verified_websites | 6 | 6 | 4 | 3 |
| social_profile_companies | 3 | 3 | 1 | 0 |
| total_facts | 10517 | 10517 | 10726 | 10722 |
| http_requests | 943 | 583 | 1026 | 633 |
| runtime_seconds | 334.375 | 107.594 | 374.968 | 157.406 |
| process_wall_seconds | 341.881 | 115.011 | 384.284 | 163.190 |
| Job claims | 0 | 0 | 0 | 1 |
| Hiring failed | 11 | 0 | 6 | 0 |

Both new runs use exactly seven flags, hash-checked original cohorts, a new run ID and isolated state; exit 0, ordered 100 envelopes, available 100-company site, HTTP <1850, completion inside 2100 seconds, $0 and zero unsupported synthesis/briefing values. They overlapped on this host, so runtime deltas are observational rather than a causal benchmark. Exact argv, config, source/output hashes, request reports and verifier receipts are in frozen/ and daily/.

Validation: full pytest 879 passed in 164.40s (pytest-gate.txt); final installed-index focused tests 16 passed. Earlier green gates are retained. Positive and negative careers tests cover own links, ATS suffix spoofing, date expiry including timestamps, undated rejection, group/foreign owner rejection, explicit-open context, robots, global/per-company accounting and saved-proof tampering.

Hand checks: jobs.md lists the sole job with title/date/exact receipts; DIGITALIQ 918266917, NAV 52c02dd7-b354-4765-a221-a594aca6b2d6. Frozen website/social sets are unchanged. Daily SUNNCOM 918031502 website plus Facebook/LinkedIn are withheld after website_source_unavailable / budget exhaustion; removed historical receipts are in new_websites.md, not reused as current proof. No careers claim was published. All 200 five-topic briefings verify. Stage I follows next.
