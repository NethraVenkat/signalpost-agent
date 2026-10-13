# The agent loop

Signalpost is a tool-using company-research agent. Source planning, identity verification, publication and template summaries use deterministic rules. Optional synthesis providers are constrained to approved claim placeholders; only a fake provider is tested in this release.

```mermaid
flowchart TD
    Input[Organisation numbers] --> Reserve[Reserve one envelope per unique input]
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
3. When enabled, generate bounded website candidates from registry website/email and legal-name slugs. Fetch under robots, public-IP, timeout and request policies. Await the shared NAV index only at the hiring step; waiting releases registry worker slots.
4. Verify exact company/parent identifiers. Website corroboration can qualify only under the documented identity rules. Link claims to exact stored source bodies, locators and short verbatim spans.
5. Publish verified values, or an explicit availability state and null. Each source section and company is isolated. A global deadline preserves completed claims and marks incomplete work failed.
6. Compare supported values with the supplied previous envelopes. Separate company changes from observation failures, retaining non-expired prior supported facts when appropriate.
7. Build a template summary of activity, scale, leadership, changes and unknowns. Quote registered activity/purpose and accepted-site self-descriptions. Read website description tags and already-fetched about paragraphs without additional requests.
8. Check citations, evidence, identity thresholds, verbatim quotes and value tokens. Derived counts must equal distinct cited records of the declared type. Drop rejected sentences and explain empty sections. Synthesis never adds source claims, changes company events or turns a source envelope into a failure.

Template mode is the default. An injected provider can order approved placeholder frames; raw values or misbound citations trigger template fallback. Calls are bounded, cached and metered. No live provider adapter or API calls are enabled. A baseline summary includes the first-observation notice; reproducibility compares identical source claims, changes and prior-snapshot context.

The final writer preserves input order, validates every envelope and the whole output, and publishes atomically. Deduplication is the default; `--emit-duplicates` preserves input-row multiplicity. Exit zero means output was written; it does not mean every source succeeded.

See [identity rules](IDENTITY_RESOLUTION.md), [schema](DATA_SCHEMA.md), [refresh semantics](REFRESH.md) and [evaluation](EVAL.md).
