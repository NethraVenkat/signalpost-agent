# The agent loop

Signalpost is a tool-using company-research agent. Source planning, identity verification, publication and template summaries use deterministic rules. Optional synthesis providers are constrained to approved claim placeholders; only a fake provider is tested in this release.

```mermaid
flowchart TD
    Input[Organisation numbers] --> Reserve[Reserve every input record; share unique research]
    Reserve --> Plan[Plan sources within budgets]
    Plan --> Tools[Registry, roles, subunits, accounts]
    Tools --> Optional[Optional website candidates and shared NAV feed]
    Optional --> Verify[Verify company identity and stored evidence]
    Verify --> Publish[Publish supported claims or abstain with explicit states]
    Publish --> Diff[Compare with the previous run]
    Diff --> Synthesis[Build cited summary or explicit unknowns]
    Synthesis --> Check[Validate sentence values and record counts]
    Check --> Output[Validate and write envelopes plus a run report]
```

For each company:

1. Normalize the nine-digit organisation number and verify its mod-11 checksum. Reserve its output before requests. Invalid inputs retain failed envelopes without network access.
2. Plan identity lookup from the supplied bulk snapshot first, then the official live endpoint if absent. Read roles, subunits and exact-company annual accounts after identity succeeds.
3. Generate bounded website candidates from registry website/email and legal-name slugs. The bundled Common Crawl/OSM website seed index is experimental and disabled by default. Set `SIGNALPOST_WEBSITE_SEEDS=1` to include its nominations. Fetch candidates under robots, public-IP, timeout and request policies. Await the shared NAV index only at the hiring step; waiting releases registry worker slots.
4. Verify exact company/parent identifiers. Website corroboration can qualify only under the documented identity rules. Link claims to exact stored source bodies, locators and short verbatim spans.
5. Publish verified values, or an explicit availability state and null. Each source section and company is isolated. A global deadline preserves completed claims and marks incomplete work failed.
6. Compare supported values with the supplied previous envelopes. Separate company changes from observation failures, retaining non-expired prior supported facts when appropriate.
7. Build a template summary of activity, scale, leadership, changes and unknowns. Quote registered activity/purpose and accepted-site self-descriptions. Read website description tags and already-fetched about paragraphs without additional requests.
8. Check citations, evidence, identity thresholds, verbatim quotes and value tokens. Derived counts must equal distinct cited records of the declared type. Drop rejected sentences and explain empty sections. Synthesis never adds source claims, changes company events or turns a source envelope into a failure.

Template mode is the default. An injected provider can order approved placeholder frames; raw values or misbound citations trigger template fallback. Calls are bounded, cached and metered. No live provider adapter or API calls are enabled. A baseline summary includes the first-observation notice; reproducibility compares identical source claims, changes and prior-snapshot context.

The final writer preserves input order and input-record multiplicity, validates every envelope and the whole output, and publishes atomically. Research is shared for duplicates; `--deduplicate` explicitly emits unique identifiers. Exit zero means output was written; it does not mean every source succeeded.

See [identity rules](IDENTITY_RESOLUTION.md), [schema](DATA_SCHEMA.md), [refresh semantics](REFRESH.md) and [evaluation](EVAL.md).

## Bounded recall and public activity

A completed, evidence-backed registry activity timeline remains available when optional website activity cannot be checked. Website section states and activity error diagnostics retain that incomplete check. A failed registry activity acquisition still marks the combined activity section failed.

The 100-company W3 paired measurement used the same frozen cohort and seven evaluator flags. Seeds ON published 11 websites from 909 HTTP requests. Seeds OFF published 40 websites from 1,160 requests. Five websites appeared only with seeds enabled, while 34 appeared only with seeds disabled. Seed candidates can use per-company candidate capacity needed by registry/name candidates, so the experimental index remains opt-in pending a better recall/precision result. The saved comparison and hand-check excerpts are in [the W3 report](../reports/r5/stageW/seed_recall.md).

Guessed email/slug domains receive a cached three-second DNS pre-check, with at most eight candidate lookups per company. NXDOMAIN spends no HTTP request; resolver failures leave the company check incomplete. Website candidates retain registry-site, email-domain, then slug order and stop after exact organisation-number proof. Connection-time public-IP checks remain mandatory.

NAV headers are ranked by distinctive-token overlap, with rare tokens weighted more heavily across the current feed. Legal suffixes and Norwegian/ASCII spelling variants affect discovery only. Details are fetched in rank order, including retries, within a configurable cap defaulting to min(candidate ads, max(300, 2 × unique companies)). Unchecked affected candidates remain failed; only exact company/listed-subunit employer numbers authorize publication.

With public activity enabled, accepted websites can supply dated news through linked same-domain RSS/Atom or bounded dated own-site HTML. Sitemaps nominate contact/about/privacy/imprint proof pages only; they never supply news or activity dates. All work shares the existing company/global counters, robots policy and domain pacing. Author, category/tag and bare news-listing paths are excluded. Recent evidence-backed registry dates use no new requests. Site presentation and synthesis retain explicit source states and cite the original evidence. The weaker registry-declared website path is default-off after group-identity ambiguities in the audit.

## Optimizations and recall expansions (v1.1 - v4)

### Part A: NAV Performance and Registry Decoupling
- **Subunit pre-caching**: Subunit employer orgnr-to-parent mappings are extracted during initial bulk loading before registry API calls begin, preventing registry latency from blocking NAV candidate matching.
- **Producer/consumer worker queue**: Subunit scopes are pushed to an async queue as each company resolves, streaming candidate ads to detail workers immediately.
- **Detail concurrency tuning**: NAV detail concurrency supports up to 12 workers ; the current default is `--nav-concurrency 4`. A historical eight-worker tuning trial recorded 196.1s versus 57.77s; those are sample measurements, not current runtime guarantees.

### Part B: Brave Search Integration & Strict Scoring
- **External web discovery**: Integrated Brave Search API (`api.search.brave.com`) candidate queries with query limits and cost tracking; results still require permitted-source fetching and company proof.
- **Mock provider**: Available only through explicit test/experimental configuration. With no search key, normal production search is disabled; mock results are not enabled automatically.
- **Identity proof**: Search results nominate domains only. Current publisher-conflict checks and exact-number or documented legal-name/contact corroboration govern publication; an old numeric candidate score is not company proof.

### Part C: Recall Expansion and UX Polish
- **Subunit ad coverage**: NAV advertisements matching subunit employer numbers are linked to parent legal entities with `matched_via = 'subunit <orgnr>'` claims, expanding hiring recall without false positives.
- **Sitemaps and feeds**: Own-site sitemaps nominate bounded identity-proof pages. Dated public activity comes from linked RSS/Atom or bounded dated HTML, with explicit source and attribution checks.
- **Interactive offline UI**: The static site generated in `--site-dir` includes live multi-field client-side search with filters, sorting (by claims, A-Z, score, revenue, employees) with sessionStorage persistence, mobile-responsive layout (375px/768px/1024px), and persistent dark mode toggle.
