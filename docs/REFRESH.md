# Refresh and previous snapshots

Supply `--previous prior.jsonl` in any supported envelope shape. Without it, each company is a baseline with empty changes. Previous rows are validated independently; malformed rows become warnings. Invalid current organisation numbers cannot inherit company facts.

Claim IDs are deterministic hashes of organisation, field, normalized source value, availability and original reporting metadata. Evidence IDs retain source URL/hash/locator/extractor identity and exclude retrieval time. Case, whitespace and collection ordering are normalized. Address abbreviations are not rewritten.

`changes[]` contains supported company value changes only when the section was successfully checked in both runs: available, not_available or not_applicable. Types are added, removed, changed and closed_job; changes carry both values/evidence-ID sets, source hashes, materiality and observation times. A role replacement is one material family event. Registered-website changes are minor. Website comparison uses registrable domain; proof strength, WWW, HTTPS and proof-page changes alone do not indicate a company move.

Any transition involving failed, blocked, ambiguous or a previously absent section is an observation in `run.refresh.observation_changes`, with section, previous/current state and reason. Identical uncertain states with identical supported values emit no observation. Disabled opt-in families do not establish removals.

Uncertain sections retain prior supported claims missing from the current check, marked carried_forward with original evidence. Newly verified claims take precedence. Older evidence metadata remains available to support both sides of changes. A fresh state directory does not require historical bodies or authorize new domains from old evidence. `--state-dir` stores bodies/cache; it does not implicitly select a prior run.

Known inactive/deleted/expired jobs are not carried forward. A missing ad from complete company candidate coverage can emit closed_job; partial coverage cannot prove closure. A previously supported active ad whose header no longer matches a known name remains uncertain. Historical carried-forward jobs must not be displayed as freshly verified active listings.

Accounts comparison includes the value, fiscal year/period, currency, account type and original source unit. Empirical whole-NOK annotation alone changes neither company-change meaning nor legacy claim identity.

Fixed-source reruns must produce identical claim IDs, zero company changes and zero observation changes. Live APIs and websites can legitimately change between requests; reproducibility of the extraction does not imply immutable internet content.
