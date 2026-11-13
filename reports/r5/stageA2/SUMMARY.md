# Stage A2 - bounded second-pass extensions

Pass 1 remains at 8/13 HTTP and eight DNS nominations. Unfinished companies may use at most +5 HTTP/+4 DNS nominations in pass 2, from leftover global capacity; cumulative absolute maxima are 13 website HTTP, 18 overall company slots and 12 DNS nominations. All candidates share the same extension. Global 1850/100 and original time limits remain enforced. Counters, proof, vetoes, robots, politeness and TLS/SSRF rules never reset.

Strong registry homepage/email, subunit and NAV candidates with transient timeout/connect/5xx failures receive one second-pass retry. Only transient cache entries are evicted; successes, NXDOMAIN and refusals are retained. A shared candidate is retried freshly at most once across companies. Optional --no-adaptive-extra-budget reproduces the earlier bounded scheduler.

| Metric | Frozen 100 | Seed-20261113 100 |
|---|---:|---:|
| verified_websites | 6 | 5 |
| social_profile_companies | 3 | 1 |
| contacts | 12 | 11 |
| job_ad_companies | 0 | 0 |
| activity_companies | 31 | 32 |
| activity_claims | 90 | 97 |
| total_facts | 9381 | 9683 |
| http_requests | 615 | 684 |
| runtime_seconds | 1200.688 | 1255.234 |
| process_wall_seconds | 1208.433 | 1264.436 |

| Sample / pass | All HTTP | Website HTTP | Exact websites gained | Retry outcomes |
|---|---:|---:|---:|---|
| frozen / pass1 | 586 | 242 | 6 | {} |
| frozen / pass2 | 29 | 29 | 0 | {"website_timeout": 1} |
| daily / pass1 | 623 | 305 | 3 | {} |
| daily / pass2 | 61 | 61 | 1 | {"website_timeout": 2, "failed": 2, "verified": 1, "ambiguous": 1} |

Both runs use exactly seven flags, new run IDs, fresh default state and the hash-checked sample/registry fixtures. Independent verification passes 100 complete briefing contracts per cohort, zero unsupported values and $0. Website counts include accepted HIGH sites; pass gains count exact VERIFIED sites. The daily sample has one exact second-pass gain and one successful strong retry. URL deltas/excerpts and historical removed receipts are in new_websites.md; full inventories are in url_inventory.json.

A host/tool no-progress interval inflated wall times to roughly 20/21 minutes. Both are inside the default 35-minute ceiling, but NAV prefetch time expired and all hiring sections are incomplete. Do not interpret lower HTTP or zero jobs as a scheduler speedup or complete absence. The first full test gate had a registry-only fixture miss its tiny deadline during that interruption; preserve its log and rerun unchanged. The comparison postprocessor initially lacked daily baseline metric definitions; its saved-output summary was corrected without another crawl.

Final green full pytest: **848 passed in 139.44s**, recorded in tests.txt; focused A2/website/adaptive tests pass 66 cases. Tests exercise transient recovery, only one retry on repeated timeout, no retry after robots/veto/404, phase-local extra ceilings, inherited lower caps and global exhaustion. Decisions are in ../DECISIONS.md. No push.
