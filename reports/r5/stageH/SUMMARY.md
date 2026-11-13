# Stage H - three clean-clone mock daily tests

Tested `revision/r5` HEAD `b3813f52d3b8030a70177b44cbae0426da6e50a5` (CI repair and four human verdicts), cloned locally with --no-hardlinks; uv sync --frozen succeeded. Interpreter/module paths and lock/source hashes are retained. No push, publication, tag or version change. Author/committer Nethra Venkat. No external implementation code copied; provider cost $0.

## Per-batch results

| Seed | Terminal / ordered | Websites | Social companies | Jobs / job companies | LEI companies | Parent companies | Awards | Activity claims | Facts | HTTP | Wall s | Site | Unsupported |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| 20261115 | 100 / yes | 5 | 4 | 0 / 0 | 10 | 0 | 0 | 982 | 13086 | 749 | 365.283 | generated | 0 |
| 20261116 | 100 / yes | 5 | 0 | 1 / 1 | 15 | 2 | 0 | 1241 | 13535 | 795 | 363.324 | generated | 0 |
| 20261117 | 100 / yes | 7 | 3 | 2 / 1 | 14 | 3 | 0 | 1084 | 13873 | 753 | 342.928 | generated | 0 |

Totals: 300 ordered terminal envelopes, 300 unique companies, 40494 published facts, 2297 HTTP across three independently bounded runs; 1071.535s combined sequential process wall, $0. Each run exited 0, used <=1850 HTTP and <=2100s wall, generated the site and all five cited briefing topics, and independently verified zero unsupported values. The totals do not replace per-batch safety checks.

Exactly seven evaluator flags per command: --organisations, --bulk, --output, --profiles-output, --report, --run-id, --expected-count. Default feature/cap/time settings; no cap/enable flags. Each run starts in a different empty working directory inside the clone; no state/cache copied. Search provider disabled explicitly in the environment, no model calls or paid API. Exact argv, cwd, runtime, report, output/source/input hashes and verifier receipts are in each seed folder.

Sampling: universe 411160 rows, archive/content/snapshot hashes verified. Exclude 327 unique earlier retained named sample/batch/CI inputs, explicitly including seeds 20261017/20261113/20261114; draw Random(seed).sample from remaining corpus order and exclude each preceding H batch before the next draw. Zero overlap with every recorded prior input and between the three H samples. Registry rows are extracted from the supplied snapshot without changing the seeded draws; absent rows are listed below and use the existing strict live identity fallback. No row is invented and no company is resampled. Full sampling inputs/exclusion manifests/order/hashes: clean_clone.json.

Snapshot extraction by batch:

- seed20261115: 99 CSV rows; missing snapshot IDs: 926078135.
- seed20261116: 100 CSV rows; missing snapshot IDs: none.
- seed20261117: 100 CSV rows; missing snapshot IDs: none.

## Failures and fixes

Before H, old pushed 1e93023 workflow was reproduced with original flags and failed its strict verifier on a site-size warning. Current code also reproduced the fixture size regression. CI-fix commit b3813f52d3b8030a70177b44cbae0426da6e50a5 changes workflow to seven flags/default scaled budget/fresh cwd and always-uploaded artifacts; its verifier rejects corrupt schema/evidence/order/unsupported values/missing actual site while permitting honest live-source outages. Renderer defers only duplicate audit rows through the existing local loader under the unchanged 250000-byte gate; no proof rule or fact removed. Fresh corrected CI20: 147 HTTP, 107.698s process wall, 20 ordered terminal envelopes/site, zero unsupported values. [Full CI reproduction](../ci-fix/SUMMARY.md).

All three initial Stage H daily batches passed the qualification checks; no daily batch rerun or production correction was needed. The first clean-clone test gate failed two fake-search tests because the measurement wrapper inherited its live search-disabled environment. Fix only the wrapper: offline tests clear provider/mock/key overrides while live runs keep paid search disabled. A focused regression test passes, followed by a fully green unchanged clone suite. Additional preparation-only issues were an invalid UTF-8 alias and an incorrect assumption that every universe draw exists in the older bulk snapshot. Both wrapper checks were corrected without editing clone production code, resampling or inventing rows. Missing bulk rows go through existing live identity checks. Regression tests verify environment isolation and found-plus-missing extraction counts. Original receipts are in trials/preparation-env, preparation-encoding and preparation-missing-snapshot; historical CI site failures are in trials/ci-site-regression. Legitimate source errors stay explicit; terminal does not mean every source succeeded.

## Precision and hand checks

All published websites, social profiles, jobs, LEIs/parents and awards were rechecked from saved hashes/excerpts and source-bound identity/link/role rules. Every item is retained, including flags. No live re-fetch or output modification. The four user-confirmed original T items remain confirmed in the old precision ledger; those sample/value-scoped verdicts are not transferred to new H companies. This is an automated evidence audit, not independently human-labelled real-world precision.

| Type | Checked | Automated correct | Doubtful | Wrong |
|---|---:|---:|---:|---:|
| website | 17 | 16 | 1 | 0 |
| social | 9 | 9 | 0 | 0 |
| job | 3 | 2 | 1 | 0 |
| LEI | 39 | 38 | 1 | 0 |
| parent | 10 | 10 | 0 | 0 |
| award | 0 | 0 | 0 | 0 |

Full per-item value/proof tier/exact excerpts/source URL/retrieval/hash/verdict: [precision/LEDGER.md](precision/LEDGER.md) and ledger.json. [Every flagged item with excerpts](doubtful_items.md), doubtful_items.json.

- **20261115 / 917455104 / SOLLIA GJESTEGÅRD AS / LEI (doubtful)**: Exact-ID GLEIF legal name differs from registry spelling; saved GLEIF name: SOLLIA GJESTEGARD AS; review source recency.
- **20261116 / 991658807 / SISSENER AS / website (doubtful)**: No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review; Published identity tier is below exact-number VERIFIED; Saved page proof needs review: corroboration.
- **20261117 / 948039958 / VALAKER BAKERI OG KONDITORI AS / job (doubtful)**: NAV employer spelling differs; exact employer/subunit proof passes, hand-check spelling.

## Validation and limits

Human-review follow-up, 2026-11-13: the user confirmed all three automated-doubtful items above as correct. SOLLIA's å/a spelling is transliteration with exact orgnr; VALAKER's job has exact NAV employer orgnr through the proven subunit with a spelling variant. SISSENER's recorded website is `https://www.sissener.no`, so the user's sissener.no-only approval applies; the user cites own fund documents naming Sissener AS at www.sissener.no. No other domain is approved. The separate human-review column in precision/LEDGER.md and scoped entries in ../precision/human_reviews.json record the verdicts. Automated flags, original proof tiers and published evidence/outputs are unchanged.

Clean-clone full pytest: 952 passed (pytest.txt/pytest.json). Parent checkout final full pytest including both wrapper environment/extraction regression tests: 954 passed (pytest-parent-commit.txt). CI source gates: 952 passing tests and 33 focused site/gate tests before commit; all proof/access/robots/politeness/global/time rules unchanged. Stage H clone package remains version 1.3.0; lockfile frozen, no new dependency. GLEIF CC0, TED EU reuse policy, official registry/NAV and verified site terms remain in docs/SOURCES.md. Some live APIs may block cloud runners; current published claims must still pass the same saved-evidence validation. Local Windows qualification is not a GitHub Linux execution or official score.

Decisions: [DECISIONS.md](../DECISIONS.md), CI and H entries. Historical reports remain historical. Stopped after H summary commit; nothing pushed.
