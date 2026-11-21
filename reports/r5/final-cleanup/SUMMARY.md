# Final compliance cleanup verification

Cleanup is implemented and remains uncommitted. Live validation was skipped because free disk was below the required 15 GB and two Python processes associated with the separately managed project were observed. No live run was started. No historical evidence, reports, replay drivers or jury receipts were removed.

Common Crawl and OSM nomination implementation, build tooling, bundled data and configuration were removed. The commercial search adapter, key-reading code, CLI controls, unused search-specific LinkedIn helper and related tests were removed. Historical receipts retain an offline exact-publisher validator. Historical documentation is marked non-operational. No new dependency was needed or orphaned runtime dependency identified.

The full automated suite passed 1,468 tests across four shards. The first pass found one documentation failure caused by an overly broad README edit. The text was restored and the affected shard passed all 450 tests. Other shards passed 327, 360 and 331. A separate privacy, CLI and robots run passed 27 tests. The 240,000-byte profile ceiling test passed in the focused gate and full suite.

The recorded clime.com robots fixture was hash-checked and all nine historical paths were denied without fetching their content. CLI tests exercised the actual runner and serializer through mocked live transport. Observed exits were total outage 1, partial success 0, recovered requests 0 and fully successful fixture 0. Existing RFC 9309 wildcard merging, longest match, Allow ties and fail-closed tests passed.

Static searches found no operational Common Crawl, OSM or commercial-search host or adapter configuration in source and scripts. Historical seed-origin strings remain exclusively for offline receipt validation. Credential names retained in benchmark environment stripping are defensive filtering. NAV public-token access remains supported. Reserved model-provider environment examples have no shipped network adapter. Source rights for company pages remain specific to their publishers.

The seven evaluator flags, fixed 2,100-second default and zero search-cost report fields remain. Live claim counts, website counts, timing, profile maximum and 200-claim precision for this cleanup are UNVERIFIED because validation was skipped. Earlier measured results are historical results for their own commits.

Branch and starting commit were verified. Repository-local author and committer configuration is the required identity. No commit, push or tag operation was performed. Existing unrelated untracked reports were left intact.

The baseline reported 1,499 collected cases and this checkout collects 1,468. Source comparison finds 31 removed test functions, all tied to the retired seed/search/unused search-result LinkedIn helper, plus one added CLI success scenario. Parameterized collection and the differing baseline run prevent a simple function-count reconciliation of the 31-case delta. No unrelated test function was removed. All 1,468 currently collected cases finished and passed.
