# Stage 4 summary

Sub-steps 4.0–4.6 are complete on `revision/r5`. No Stage 5 work was started. No push or Git identity configuration changes were made. Each implementation sub-step has one commit after a green full pytest suite, a fresh frozen-100 comparison and independent output verification. All runs used $0 provider cost.

## Commits and tests

| Sub-step | Commit | Author | Message | Full pytest |
|---|---|---|---|---|
| 4.1 | `eddfe8c5e85236484b865f848ea07423d50a0ebc` | Nethra Venkat <nethravenkat510@gmail.com> | Fix website hostname fallback and enforce source vetoes | 671 passed in 127.39s |
| 4.2 | `c56b6db3572e736ddfa591543c708150e731c8ae` | Nethra Venkat <nethravenkat510@gmail.com> | Publish typed registry business postal and workplace locations | 679 passed in 80.40s |
| 4.3 | `529cfdad1a3c427c905c50a0313a126045002114` | Nethra Venkat <nethravenkat510@gmail.com> | Add bounded brand and full-name spelling variants as candidates | 686 passed in 82.73s |
| 4.4 | `304c649002cc851c0ac4a95438a9239ef98840e7` | Nethra Venkat <nethravenkat510@gmail.com> | Prioritize bounded proof pages and validate explicit owner identifiers | 703 passed in 91.10s |
| 4.5 | `73c5649aeb0e9d31196c1a2b9ad29a4d51e1c840` | Nethra Venkat <nethravenkat510@gmail.com> | Require exact registry contact agreement for corroborated website proof | 719 passed in 79.77s |
| 4.6 | `7ac223b450c8c1ea268bfd776f5ac764a8a155a8` | Nethra Venkat <nethravenkat510@gmail.com> | Require exact-name social profiles from the verified site header or footer | 737 passed in 79.09s |

No timeout was increased. The DNS cache test now requires exact per-host caching for the requested fallback, still with zero HTTP on DNS failure and immediate private-address refusal. Two legacy social tests now reject publication from navigation/sameAs-only or shared-group sources, while retaining nomination, provenance and integration checks. New positive and adversarial strict-social cases cover the replacement policy.

## Stage 3 versus every sub-step

All runs reuse the exact frozen seed-20261017 company list and registry subset; their hashes are checked before execution. Only output/state paths and run ID differ from the original resolved settings. State is fresh, with no previous envelopes or copied responses. The stale shipped NAV index triggers the same default full-feed fallback. Budgets remain 2,000 HTTP attempts / 2,400 seconds, with unchanged per-company website/DNS caps. Source/retry variation is retained; small runtime/HTTP changes are not claimed as causal speedups.

| Metric / section state | Stage 3 | 4.1 | 4.2 | 4.3 | 4.4 | 4.5 | 4.6 |
|---|---:|---:|---:|---:|---:|---:|---:|
| verified_websites | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| social_profile_companies | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| activity_companies | 31 | 31 | 31 | 30 | 31 | 31 | 31 |
| activity_claims | 89 | 89 | 89 | 79 | 89 | 89 | 89 |
| total_facts | 7,102 | 7,102 | 7,320 | 7,310 | 7,320 | 7,320 | 7,318 |
| locations | 73 | 73 | 73 | 73 | 73 | 73 | 73 |
| job_ad_companies | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| contacts | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| http_requests | 872 | 870 | 873 | 866 | 867 | 866 | 866 |
| runtime_seconds | 240.578 | 240.046 | 244.203 | 243.360 | 240.438 | 241.937 | 237.625 |
| process_wall_seconds | 243.774 | 243.775 | 248.041 | 247.617 | 244.372 | 245.094 | 240.849 |
| Provider cost (USD) | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| identity / available | 100 | 100 | 100 | 100 | 100 | 100 | 100 |
| identity / not_available | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| identity / blocked | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| identity / ambiguous | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| identity / failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| identity / not_applicable | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| roles / available | 100 | 100 | 100 | 100 | 100 | 100 | 100 |
| roles / not_available | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| roles / blocked | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| roles / ambiguous | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| roles / failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| roles / not_applicable | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| subunits / available | 71 | 71 | 71 | 71 | 71 | 71 | 71 |
| subunits / not_available | 29 | 29 | 29 | 29 | 29 | 29 | 29 |
| subunits / blocked | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| subunits / ambiguous | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| subunits / failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| subunits / not_applicable | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| accounts / available | 99 | 99 | 99 | 99 | 99 | 99 | 99 |
| accounts / not_available | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| accounts / blocked | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| accounts / ambiguous | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| accounts / failed | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| accounts / not_applicable | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| website / available | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| website / not_available | 65 | 47 | 47 | 46 | 46 | 46 | 46 |
| website / blocked | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| website / ambiguous | 5 | 6 | 6 | 6 | 6 | 6 | 6 |
| website / failed | 24 | 41 | 41 | 42 | 42 | 42 | 42 |
| website / not_applicable | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| hiring / available | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| hiring / not_available | 89 | 89 | 89 | 89 | 89 | 89 | 89 |
| hiring / blocked | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| hiring / ambiguous | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| hiring / failed | 11 | 11 | 11 | 11 | 11 | 11 | 11 |
| hiring / not_applicable | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| activity / available | 20 | 17 | 17 | 15 | 16 | 16 | 16 |
| activity / not_available | 49 | 34 | 34 | 34 | 34 | 34 | 34 |
| activity / blocked | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| activity / ambiguous | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| activity / failed | 31 | 49 | 49 | 51 | 50 | 50 | 50 |
| activity / not_applicable | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Definitions match Stage 3: total facts count available source claims only; locations count workplace records, not typed address attributes; activity counts retain verified partial positives even in incomplete sections. The typed-location expansion adds 100 business, 45 postal and 73 workplace attributes without inventing extra workplace records or using geocoding.

## Verification and precision

| Check | Stage 3 | 4.1 | 4.2 | 4.3 | 4.4 | 4.5 | 4.6 |
|---|---:|---:|---:|---:|---:|---:|---:|
| lines | 100 | 100 | 100 | 100 | 100 | 100 | 100 |
| source_blobs_verified | 383 | 383 | 383 | 382 | 383 | 383 | 383 |
| synthesis_sentences | 1203 | 1203 | 1203 | 1202 | 1203 | 1203 | 1203 |
| synthesis_unverified_values | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| briefing_sentences | 600 | 600 | 600 | 600 | 600 | 600 | 600 |
| briefing_unverified_values | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

The precision audit lists 0 newly published URL rows against Stage 3 across all sub-steps in [new_websites.md](new_websites.md), with exact excerpts and full provenance in its JSON companion. No new URL was published, so there is no unreviewed recall gain. The stricter social policy can remove earlier positives; this is not hidden by reclassifying source failures as absence.

| Removed earlier social URL | Organisation | Company |
|---|---|---|
| https://www.linkedin.com/company/123301 | 991853995 | BIEN SPAREBANK ASA |
| https://www.linkedin.com/company/2534098 | 964398003 | FOLKSOM AS |

These URLs are withheld rather than asserted to be inactive or closed.

## Files and coverage

- 4.0: saved company/domain/error diagnosis and primary-cause counts, without code or new network calls.
- 4.1: hostname DNS/HTTPS fallback, source/group vetoes, non-HTML target filtering and removal of collector sitemap/RSS nomination work.
- 4.2: registry location typing, profile labels and refresh coverage classification.
- 4.3: complete-name/brand/subunit nomination spellings and ordering within existing caps.
- 4.4: contact/about/privacy proof-page priority, explicit metadata/owner JSON-LD and bounded organisation-number parsing.
- 4.5: exact contact matching, stricter signal-tier acceptance and page-plus-registry corroboration evidence.
- 4.6: own header/footer context, full-name profile-handle agreement, group/founder/agency rejection and refresh safeguards.

Each step directory contains the exact command/settings, full test result, original run report, counts, Stage 3 delta table and independent verification result. Raw envelopes/profiles/source bodies/sites remain local in `.data/r5/stage4/step4_N-run/`; output hashes are recorded in the committed counts.

## Decisions and hand checks

- Website recall did not improve on this cohort. The unchanged eight-DNS-check allowance is spent sooner when checking both hostnames; higher incomplete website counts are explicit, not a claim of checked absence. Review the budget tradeoff before considering a separately authorized budget change.
- Manually inspect representative generated profiles and any social removals. Profile-name evidence is the linked handle matching the full registered name; no platform display-name lookup or manual browser accuracy audit is claimed.
- Registry contact details corroborate but never replace the identity firewall. Formal source outages, robots, transport failures and unsupported proof remain explicit.
- No AS masthead shortcut, unique-name shortcut, loose footer social publication, OpenStreetMap, new sitemap-news recall, paid search or model integration was added. Existing accepted-site public activity remains under its prior bounded policy; collector sitemap/RSS domain nomination was removed.
- Typed address attributes are descriptive registry facts, not extra offices, geocoded points or proof of domain ownership.
- No sub-step exceeded its limit or required reverting. Final report is a separate docs-only commit as explicitly requested. Stage 5 was not started.

## Complete Stage 4 decisions log

## Stage 4.0 and 4.1

- Diagnose first using Stage 3 saved envelopes/request logs only: 24 failed, 5 ambiguous, 1 blocked. Primary causes: 19 budget, 5 ambiguity, 2 timeout, 2 DNS, 1 access block, 1 transport/content refusal. Full company/domain/code lists are in `stage4/diagnosis.md` and machine diagnostics in `diagnosis.json`.
- Fix original-host DNS precheck preventing www/non-www fallback, retaining eight DNS nominations and unchanged HTTP/time caps. HTTPS is tried first even for HTTP nominations; plaintext still requires real TLS/connect failure. Private-address failures do not authorize fallback.
- Remove existing sitemap/RSS candidate discovery, and filter known non-HTML proof targets before requests. These are budget/policy fixes before recall expansion; no caps are raised. Exhausted proof work remains failed/ambiguous rather than absence.
- Keep exact-number VERIFIED, strictly corroborated registry-origin HIGH and default-off REGISTRY_DECLARED tiers. Group sites without the exact number are vetoed; parked domains, marketplaces and directories cannot become company sources. No AS masthead, unique-name or loose social rule is added.
- 4.1 verification: 671 tests passed. Frozen run retains five websites/two social companies, with no new URLs. Two-host DNS checking spends the unchanged eight-check allowance sooner: website failures are 41 rather than Stage 3's 24 (not_available 47 rather than 65). These are explicit incomplete checks, not a claimed coverage gain. HTTP attempts 870, provider cost $0, unsupported synthesis/briefing values zero. The old DNS test now asserts each hostname is cached exactly once across companies, preserves zero-HTTP and private-address veto assertions, and does not loosen timeout or proof checks.

## Stage 4.2

- Publish typed business/postal/workplace locations from their exact registry fields and proven company/subunit scope. Preserve the compatible core address/workplace records; postal fallback is never relabelled as physical workplace. No map/geocoding source or new requests. Newly observed typed fields are coverage observations on refresh, not invented company moves.
- 4.2: 679 tests passed; total facts 7,320 versus Stage 3's 7,102; workplace records remain 73. Five websites/two social companies, no new URLs, zero unsupported values. Exact typed counts are in `step4_2/typed_locations.json`.

## Stage 4.3

- Prioritize the requested ae/oe/aa and a/o/a spellings, with hyphen/no-hyphen full-name variants and suffix stripping. Registry URL/email origins remain first; the eight-candidate and DNS/HTTP ceilings are unchanged. Existing native IDNA and legacy spellings remain bounded alternatives.
- Brand strings from previous supported public-brand claims and registry-proven subunit names nominate candidates only. None changes the legal-name proof context or authorizes publication. No token-only/unique-name shortcut, leading-AS masthead rule, search provider or sitemap discovery is added.
- 4.3: 686 tests passed; five websites/two social companies, no new URLs. Facts 7,310 and activity claims 79 (versus 7,320/89 in 4.2) reflect incomplete live website activity, not manufactured replacement facts. All 100 envelopes and 600 briefing sentences verify with zero unsupported values. HTTP attempts 866; provider cost $0.

## Stage 4.4

- Prioritize linked proof pages, then /kontakt, /om-oss and /personvern before alternate spellings; retain original request ceilings and robots checks. No sitemap news or browser rendering is added.
- Accept bounded organisation-number forms with NO/MVA, spaces and dots in owner/footer content, explicit identifier meta fields and owner JSON-LD nodes. Generic SEO descriptions, Person nodes (including mixed-type lists), nested customer/about objects, ISBN/LEI and arbitrary scripts cannot prove ownership. Hidden display:none text is still excluded; this sub-step supports structured metadata, not arbitrary hidden instructions.
- 4.4: 703 tests passed, including long numeric-run suffix rejection. Frozen comparison: five websites/two social companies, no new URLs; 7,320 facts, 867 HTTP attempts, zero unsupported values and $0 provider cost. More permissive hidden-text or generic SEO matching was not enabled to increase recall.

## Stage 4.5

- Exact Norwegian registry phone normalization or exact full corporate email-domain agreement can corroborate a website. No fuzzy phone match, parent-domain/subdomain substring, free-mail-domain match or name similarity substitutes for it. HIGH/default-off registry-declared signal tiers now also require this contact agreement; exact organisation-number proof remains the stronger tier.
- Contact agreement alone cannot establish exact-entity ownership. Parked, foreign-number, directory/marketplace and group-without-exact-number vetoes win. Shared management-provider phones/domains do not bypass the firewall. This deliberately conservative interpretation preserves the earlier exact-entity rule.
- Published agreement metadata links both the current registry field evidence and a bounded verbatim page span with extractor version `signalpost.registry_contact.v1`. Group pages with multiple entity numbers do not receive contact-agreement metadata. No extra request or paid provider.
- 4.5: 719 tests passed; frozen run retains five websites/two social companies and 7,320 facts, with no new URLs. Exact agreement records are saved in `step4_5/contact_agreements.json`. 866 HTTP attempts, $0 cost, zero unsupported values. Contact agreement was not used as a recall shortcut without entity proof.

## Stage 4.6

- Publish social profiles only from the verified site's own header/footer (or semantic equivalents), with exact full-name handle agreement after bounded spelling/format normalization. Founder/agency-credit/hidden/article contexts, loose navigation, sameAs-only nominations, wrong-name handles and shared group-site profiles abstain. No platform page is fetched; profile-name support is the literal linked handle, not a claimed platform display-name lookup.
- Attach registry legal-name, website identity and verbatim source-link evidence. Legacy loose social facts cannot be carried forward, even on failed refresh. Tightening the proof policy is an observation rather than a company event. No new domain guessing or AS masthead rule.
- Two legacy publication tests expected nav/sameAs-only or shared-group social claims. Their assertions now explicitly reject those publications under the user's stricter rule; the discovery-only nominations and all other integration/provenance checks are retained. Positive own-header/footer publication and negative founder/agency/group/hidden cases are separately tested. No timing or safety assertion is relaxed.
- Before committing 4.6, a non-Latin-name normalization edge case was found: removing all non-ASCII letters could leave a misleading partial name or corporate suffix. Preserve Unicode letters, normalize only the requested Norwegian spellings/formatting, reject suffix-only names, and add positive/negative Unicode tests. Repeat the frozen run in a new `-final` state/output directory and run ID; preserve the first run locally rather than overwrite its source artifacts.
- Final 4.6: 737 tests passed. Fresh `-final` run: five verified website companies, two social-profile companies, 7,318 facts, 866 HTTP attempts, 100 ordered envelopes, 600 briefing sentences, $0 cost and zero unsupported values. Two older social URLs are withheld under the stricter rule; the number of companies with at least one qualifying profile remains two. No new website/social URL was published versus Stage 3 in any sub-step. Budget/DNS-limited website failures remain explicit (42 final versus 24 in Stage 3).
