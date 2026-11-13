# W0 / R1 / R2 / R4 foundations

Branch revision/r5. Author Nethra Venkat. No push, publication, model or paid search. Provider cost $0. No new proof tier.

## W0 saved-output baseline

| Seed | Sites | Registry homepage | Declared domain published | Veto | Ambiguous | Fetched without proof |
|---|---:|---:|---:|---:|---:|---:|
| 20261017 | 5 | 11 | 4 | 3 | 6 | 22 |
| 20261113 | 4 | 11 | 3 | 4 | 10 | 29 |
| 20261114 | 3 | 8 | 3 | 2 | 8 | 27 |
| 20261115 | 5 | 14 | 1 | 3 | 5 | 25 |
| 20261116 | 5 | 17 | 2 | 6 | 9 | 27 |
| 20261117 | 7 | 11 | 0 | 6 | 6 | 26 |

Declared-homepage domain recall: 13/72 = 18.06%. This is declaration recall, not independently established current ownership. Rejection categories overlap: {"fetched-without-proof": 156, "ambiguous": 44, "veto": 24}. rejections.md/json retain all company/candidate/page details and identity locations.

The saved baseline contains 26 VERIFIED and three HIGH websites. Declared-domain publications split 10 VERIFIED / three HIGH; strict exact-number declaration recall is 10/72 (13.89%). HIGH remains a distinct existing tier.

Historical DNS attempt records: {"NXDOMAIN/name-not-found": 2511, "unknown (resolver error or DNS nomination budget)": 7}. Unique company/candidate nominations: {"NXDOMAIN/name-not-found": 2507, "unknown (resolver error or DNS nomination budget)": 7}. Generic errors can include a nomination cutoff and cannot honestly be split into old SERVFAIL versus timeout. Public resolver once-only A checks: 7 unique hosts; {"SERVFAIL": 7}; 7 separately reported diagnostic HTTP, $0. Two failed official bulk robots attempts are separately retained; zero bulk download requests. No positive DNS answer becomes proof.

## Jobs index overlap

```json
{
  "index_built_at": "2026-11-13T08:23:53.796625Z",
  "ads": 9511,
  "index_employers": 6012,
  "universe_size": 411160,
  "direct_employers_in_universe": 0,
  "proven_parent_employers_in_universe": 2133,
  "unique_represented_companies": 2133,
  "expected_per_1000_lower_bound": 5.187761455394494,
  "measured_job_companies": 3,
  "measured_inputs": 600,
  "measured_per_1000": 5.0,
  "limitation": "Index discovery expectation, not current job-posting proof. Three deleted-unit tombstones omit their former parent; no name-based parent inference. Interval allows at most one additional distinct eligible parent per unresolved unit. Index/registry retrieval dates differ; this targeted join is not a nationwide subunit snapshot.",
  "index_file_sha256": "ba4d5df8a8fa4ebae0c9ed77d16bdb55de82632c64b855853d60bd61b2a36a43",
  "universe_archive_sha256": "1c89710e5b01f8617e86d09fbdff4a52f2f8dbbba297e74f7164b5984f5a0384",
  "initial_saved_parent_lower_bound_companies": 3,
  "mapped_index_employers": 6009,
  "classified_index_employers": 6012,
  "distinct_registered_parents": 3407,
  "expected_per_1000_upper_bound": 5.19505788500827,
  "exact_all_parent_point_estimate": null,
  "deleted_index_employers_without_parent": [
    {
      "employer_orgnr": "881521032",
      "content_sha256": "ae8963693dfbe18a0edce14ba7bf614950750a34833b5e391227633b08cb8c84",
      "locator": "/organisasjonsnummer",
      "exact_excerpt": "\"organisasjonsnummer\":\"881521032\"",
      "registry_deleted_at": "2026-10-19",
      "response_class": "SlettetUnderEnhet",
      "parent_state": "not_returned; no name-based inference"
    },
    {
      "employer_orgnr": "983036961",
      "content_sha256": "5b792c5db6446ca10469917f2da4be87bc818e7dfaa156cb3aeae189e0189425",
      "locator": "/organisasjonsnummer",
      "exact_excerpt": "\"organisasjonsnummer\":\"983036961\"",
      "registry_deleted_at": "2026-05-05",
      "response_class": "SlettetUnderEnhet",
      "parent_state": "not_returned; no name-based inference"
    },
    {
      "employer_orgnr": "988083895",
      "content_sha256": "3996bbb8d02b4816d703d581210d39ce095ace11c1b1dc5c8c7ddb4fd3de10c2",
      "locator": "/organisasjonsnummer",
      "exact_excerpt": "\"organisasjonsnummer\":\"988083895\"",
      "registry_deleted_at": "2026-05-27",
      "response_class": "SlettetUnderEnhet",
      "parent_state": "not_returned; no name-based inference"
    }
  ],
  "sample_index_matched_companies": [
    {
      "seed": 20261113,
      "orgnr": "918266917",
      "name": "DIGITALIQ AS",
      "job_published": true
    },
    {
      "seed": 20261116,
      "orgnr": "919543604",
      "name": "HIGHLAND LODGE AS",
      "job_published": true
    },
    {
      "seed": 20261117,
      "orgnr": "948039958",
      "name": "VALAKER BAKERI OG KONDITORI AS",
      "job_published": true
    }
  ],
  "parent_join_http_requests": 34,
  "parent_join_active_runtime_seconds": 233.9999999999709,
  "parent_join_receipts": "nav_parent_join.json",
  "parent_join_verification": "nav_parent_verification.json"
}
```

The licensed official exact-ID REST query resolved 6,009 employer-parent pairs and classified all 6,012 employers. The other three are deleted-unit tombstones without former parents; no name join fills them. Confirmed index/universe coverage is 2,133 companies: 5.187761 per 1,000, with an optimistic upper bound 5.195058 if those three missing parents were distinct eligible companies. Measured coverage is three job companies / 600 = 5 per 1,000. All three currently index-matched sample companies (DIGITALIQ, HIGHLAND LODGE, VALAKER) publish a job. This is an index-discovery expectation, not proof that every indexed ad remains current. Source hashes, exact record pairings, deleted records and independent recount are in nav_parent_join.json / nav_parent_verification.json. Auxiliary API cost: 34 HTTP attempts, 234 active tool seconds, $0; separate from evaluator runs. The optional bulk robots preflight failed; the existing approved licensed REST policy supplied the targeted audit without a website crawl or access-refusal bypass.

## R1 and R2

R1 isolates labelled publisher context from customer/partner/reference/article/news/hidden/script/agency-credit content. Seven focused fixtures; full gate 961 passed. It does not add positive evidence. R1_REPORT.md details limitations.

R2 bundle: 1,177,860 distinct entities; 10,853,314 bytes; source/table hashes and dates in rarity.json. Runtime lookup is local-only and dormant for proof scoring. No subunit snapshot is represented as present. Duplicate entity/key pairs count once.

| Key | 1 entity | 2 | 3–4 | ≥5 |
|---|---:|---:|---:|---:|
| phone | 363794 | 33024 | 8123 | 2135 |
| email | 277476 | 11472 | 2337 | 836 |
| domain | 76131 | 9334 | 3771 | 2589 |
| name | 1095275 | 34983 | 2717 | 577 |

## R4 conflict guard and six fresh measurements

The guard rejects conflicting publisher IDs (proven target/subunits excepted), incompatible legal forms (AS/ASA excepted), explicit group branding without the target number, placeholders/default hosting, and third-party service publishers. It precedes positive scoring. Every previous veto and positive threshold is retained. Subunit fallback cannot override a publisher conflict. The local rarity table never promotes a candidate.

Exact historical proof-page replay: all 29 published websites survive the new guard. All 73 fetched pages on those accepted candidates, including follow-ups, also pass the new guard (r4_all_published_pages.json). A false SISSENER group match on “as part of the selection process” was caught and narrowed to explicit group/parent markers. The first live six-sample trial exposed a second false veto on SISSENER’s about page: a page-wide header-over-content layout class made employee biographies look like publisher branding. Region detection now matches actual header/footer components, including underscore separators, rather than generic layout modifiers. Stronger HIGH-without-number fixtures exposed compound wrappers aggregating footer contacts or copyright; only actual contact blocks and atomic copyright lines contribute. All three retained buggy extractors fail the fixture with its footer copyright line, while the final extractor passes HIGH at unchanged thresholds (r4_regression_before_after.json). Exact failure receipts, old sources and superseded runs remain under trials/. Intermediate drivers were stopped to avoid more superseded calls; their current CLI children completed all mandatory outputs and independently verified, with uncaptured exit codes/source-import windows left unknown. All six accepted runs were repeated with fresh state and final source; no trial substitutes for an accepted run and no historical proof was carried forward. The synthetic multi-company group fixtures now test withholding and downstream suppression. Exact NAV jobs remain independent of website rejection. Replay imports lazy NAV modules before freezing time, fixing first/second replay expiry inconsistency without production behavior changes.

| Seed | Prior sites | R4 sites | Prior HTTP | R4 HTTP | Wall seconds | Cost USD |
|---|---:|---:|---:|---:|---:|---:|
| 20261017 | 5 | 5 | 700 | 696 | 349.625 | 0 |
| 20261113 | 4 | 4 | 792 | 777 | 367.953 | 0 |
| 20261114 | 3 | 3 | 736 | 723 | 321.672 | 0 |
| 20261115 | 5 | 6 | 749 | 748 | 361.140 | 0 |
| 20261116 | 5 | 5 | 795 | 787 | 363.750 | 0 |
| 20261117 | 7 | 7 | 753 | 734 | 311.110 | 0 |

Unchanged prior website URLs across live runs: 29 / 29; zero removals. Every run uses exactly the seven evaluator flags, original ordered inputs, a new run ID and fresh state. Each independently passes 100 ordered terminal envelopes, all five cited briefing elements, zero unsupported values, site membership, <=1,850 HTTP and <=2,100 seconds. Settings, complete reports, verifier results and hashes are in each seed folder. r4_source_manifest.json identifies the actual measured production bytes; parent commits in settings may precede the R4 commit because measurements happen before commit.

The literal zero-additions condition against historical outputs is not met: LOOPYTY AS 933519708 recovered from an earlier timeout on the same already-nominated loopyty.com candidate. The final site contains the exact target number in its own copyright footer. Unmodified pre-R4 code from committed R2 (81a76b8d) verifies and localizes that exact saved response as VERIFIED (legacy_addition_replay.json). R4 introduces no new positive rule/tier and rarity is unused; this recovery is not attributed to a foundation proof improvement. Final publication is 30 sites (27 VERIFIED / three HIGH), retaining all 29 originals. The historical +1 is disclosed rather than hidden by rewriting output or hard-coding a sample-specific veto. Hand-check the exact new URL/receipt in new_websites.md. No social URL addition/removal is expected; the actual delta inventory is authoritative.

Website/social URL deltas and exact proof receipts are in new_websites.md / r4_url_inventory.json. Inspect the source-timeout recovery exception when assessing the requested no-additions measurement; no zero-addition claim is made for the historical URL set.

## Commits and validation

```text
81a76b8d Stage R2: bundle local registry identity frequency counts
45f4d43d Stage R1: extract publisher context without changing proof rules
bb2a919f Stage W0: audit six saved samples without publication changes
```

R4 implementation and this final summary share the final stage commit; git log -1 supplies its hash after commit. A commit cannot contain its own final hash. W0 gate: 954 passed; R1 gate: 961 passed; R2 working-tree gate: 979 passed, followed by an independent exact committed-R2 worktree gate: 964 passed (r2_committed_tree_check.json). Final R4 full gate: 983 passed in 153.18 seconds (pytest-R4-release.txt), with 26 focused publisher tests and all 73 fetched pages on 29 historical published sites replayed. The biography regression exercises the corroborated HIGH path without an exact number, matching the actual SISSENER failure. Trial failures remain in pytest-*.txt; none authorized a stage commit.

## Hand checks and limits

- Inspect every rule/page association in rejections.json; old output saved candidate-level outcomes, so per-page rejection attribution is not invented.
- Check the seven public DNS responses. OS name-not-found is not an authoritative saved RCODE, and an A-only check is not a complete DNS-existence test.
- Review the three deleted NAV workplace IDs and their absent former-parent fields. The expected-rate interval is bounded; names never establish a missing parent.
- Hand-check LOOPYTY AS 933519708 / https://loopyty.com: one historical source-timeout recovery, accepted by unchanged pre-R4 proof code. This is the disclosed exception to a literal zero-additions result.
- Review r4_published_replay.json, including human-reviewed SISSENER, CONCEDO and GLÅMDAL; human verdicts and existing proof tiers remain distinct.
- Publisher extraction cannot evaluate CSS-computed visibility or infer unmarked customer-list semantics. Existing independent proof vetoes remain active.
- Registry snapshot dates and the current live sources differ; this is a measured sample comparison, not an accuracy guarantee. No model calls, paid APIs or search; source licences/terms remain in docs/SOURCES.md. Stop after these foundations; no new proof tier or next stage.

## Resource accounting including rejected trials

Accepted six-run total: 4465 HTTP and 2075.25 process wall seconds. Superseded 14 runs: 10353 HTTP and 4902.514 reported completion seconds. Their reports/outputs remain available and are not substituted for accepted samples. Ancillary audit attempts: 7 public DNS + 2 failed bulk preflights + 34 official parent lookups. All provider fees $0, model calls 0, paid search 0. Every company run keeps its own scaled 1,850 HTTP / 2,100-second limit; final runs each exit 0.
