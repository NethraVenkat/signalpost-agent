# Evaluation and smoke checks

The optional `--profiles-output` file now parses with the untouched supplied proxy scorer. A saved100-company parse check independently verified union, contract and reference envelopes and produced foundation14.96/15, raw proxy18.96/100, awardable0 and qualificationfalse. Only measured batch facts were supplied; external/refresh/research/UX aggregate inputs were deliberately unqualified, and optional resume/sentiment inputs were omitted. These are parsing/measurement results, not an official score. Website/roles/location terminal-key points do not measure actual fact coverage. The measured company p95 of332.890 seconds fails the proxy's separate10-second threshold; no scoring threshold was changed.

Saved1000 union output is67,198,940bytes versus56,212,586contract bytes (1.195443×), with no company reductions under the configurable256MiB output safety valve. Envelope evidence stays a list; the separate raw profiles file has the reference dictionary records and exact verified claim/provenance index. All seven common reference-runner flag names are accepted verbatim.

Install pinned dependencies and run the offline suite:

```sh
uv sync --frozen
uv run pytest
```

The offline suite covers input membership and multiplicity, isolation/deadlines/budgets, missing versus reported zero, all envelope shapes, stored provenance, refresh/carry-forward, website proof/robots/SSRF/politeness, NAV exact matches/caps/ETags, output verification, synthesis citations/values/counts and provider fallback. Fixtures are small and local; no credentials or internet are required for these tests.

## Current resource defaults

The default time budget is a fixed 2,100 seconds for any batch size (smaller batches: 21 seconds per unique input). `--deadline-fraction 0.85` stops source work at 1,785 seconds. `--scaled-time-budget` (off by default) opts in to 35 minutes per 100 unique inputs. The hard HTTP ceiling is floor(1,850 × unique normalized input identifiers / 100); duplicates share requests. `--max-requests` can only lower this ceiling. Requested time remains bounded by the scaled hard limit; inspect `report.limits` for effective values. Workers default to 64, registry host concurrency to 10 and request timeout to 10 seconds. Website discovery uses one pass with 8 website requests, 13 overall company slots, 8 DNS nominations, and 45 seconds of active discovery per company. The shared website pool has 16 slots. Requests have an 8-second bound, with at least one-second domain politeness and two requests in flight per domain. Default batches of 100 or more retain a 1,700-second website cutoff inside the original global crawl deadline. Override the website caps with `--website-request-cap` and `--website-total-request-cap`; `--no-dns-precheck` disables candidate prechecks.

NAV starts before website work on a separate connection pool. Defaults: 512 header pages, 185-day lookback, 4 detail workers, 30-second request timeout, min(candidate ads, max(300, 2 × unique companies)) detail attempts including retries, and a total time cap of min(900 seconds, 40% of the run budget). Override with `--nav-max-pages`, `--nav-lookback-days`, `--nav-concurrency`, `--nav-request-timeout`, `--nav-max-details` and `--nav-time-cap-seconds`. A partial index always remains failed rather than checked-negative. Reports include `feed_complete`, pages, feed seconds and seconds per page.

Historical measurement at the older release settings: the 1,000-company run used 488.679 seconds wall time and 5,975 HTTP requests. Against its then-used 2,400-second and 20,000-request limits, this leaves 79.64% time and 70.13% request headroom (76.05% before the source watchdog). This is a measurement, not a guarantee about an unknown official budget. That historical run used a 64 MiB output limit and reduced one large company to explicit output-limit failures. The current default is 256 MiB (`--max-output-mb`). Contract output avoids the redundant reference profile. Source failures preserve terminal envelopes. Partial research can exit zero; all-failed or confirmed-outage batches exit non-zero and are never counted as complete. Inspect `run_status`, section outcomes, warnings and site state.

## Live 20-company registry smoke

```sh
uv run signalpost run --organisations tests/fixtures/ci20.jsonl --bulk tests/fixtures/ci20.csv --output out/smoke20/envelopes.jsonl --profiles-output out/smoke20/profiles.jsonl --report out/smoke20/report.json --run-id ci20 --expected-count 20
uv run python scripts/check_live_run.py --output out/smoke20/envelopes.jsonl --organisations tests/fixtures/ci20.jsonl --count 20 --state state --report out/smoke20/report.json --site out/smoke20/site
```

The public fixtures provide identity rows. The workflow runs the seven evaluator flags in a fresh working directory; normal website, hiring and public-source defaults are enabled. The saved-output gate requires all input members, supported claims, cited briefings and site bounds, while retaining honest source failures. The separate optional `verify_output --require-clean` mode additionally rejects incomplete sections and warnings; it is not the workflow command above.

GitHub Actions has two Ubuntu jobs: tests and live-20. Both run frozen installation. Source failures can make the live job red independently of deterministic unit tests. Check the [Actions page](https://github.com/NethraVenkat/signalpost-agent/actions) for the actual results of the published revision.

## Output verification and refresh

The verifier checks schemas, exact input membership/order, available-claim evidence links, actual stored-body SHA-256 and verbatim spans. When synthesis is present, it checks sentence citations/values, counters, concatenated text, change citations and the union mirror without dropping or rewriting rejected output. It requires the corresponding blobs, including archives for carried-forward claims. No network request is made by verification.

```sh
uv run signalpost run --organisations batch.jsonl --bulk registry.csv --output out/first.jsonl --report out/first-report.json
uv run signalpost run --organisations batch.jsonl --bulk registry.csv --output out/second.jsonl --report out/second-report.json --previous out/first.jsonl
uv run python scripts/verify_output.py --first out/first.jsonl --second out/second.jsonl --organisations batch.jsonl --count 100 --state-dir state
```

Fixed-source refresh expects identical claim IDs and zero company and observation changes. Live sources can legitimately change; inspect every company event against both evidence sides rather than forcing a zero-change result.

## Sampling and bulk preparation

Download the public universe archive from [the company-universe resource](https://builderr.ai/signalpost-company-universe-2025.jsonl.gz). The sampling helper verifies its published archive and decompressed hashes and samples uniformly with a fixed seed:

```sh
uv run python scripts/sample_universe.py --universe downloads/universe.jsonl.gz --output out/batch100.jsonl --count 100 --seed 20261013
uv run python scripts/extract_bulk.py --bulk downloads/registry.csv --batch out/batch100.jsonl --output out/registry100.csv
```

Obtain the bulk snapshot from the [official registry CSV endpoint](https://data.brreg.no/enhetsregisteret/api/enheter/lastned/csv). The extractor accepts plain/gzip CSV and reports requested rows absent from the snapshot; the runner keeps those companies and uses live fallback. Snapshots, outputs and blobs are ignored locally and not distributed here.

## Latest measurements

### Evidence-checked synthesis, saved 300-company sources

Measured on 13 October 2026: exact saved registry/NAV HTTP statuses and bodies were replayed; accepted website claims/states and same-host archived pages were restored. No network or DNS requests and no model calls were made. This checks summary construction without claiming fresh website verification.

| Check | Result |
|---|---:|
| Ordered valid envelopes with synthesis |300|
| Unhandled exceptions / synthesis-caused envelope failures |0 / 0|
| What-it-does / scale / leadership coverage |100% / 100% / 99.667%|
| At least one unknown entry |100%|
| Incomplete-source companies with every required unknown listed |299 / 299|
| Retained sentences / cited / unverified / dropped |2356 / 2356 / 0 / 0|
| Registered activity / statutory purpose coverage |299 / 300; 292 / 300|
| Website self-description claims / companies |34 / 16|
| Template rerun with the same prior snapshot |Byte-identical; 0 company changes|
| Union output before / after synthesis |56.598 / 64.312 decimal KB/company|
| Saved-source preparation, synthesis, rerun and hash verification |163.594s|

The size comparison removes only synthesis from the same enriched union envelopes; source claims/evidence are otherwise identical. Union output mirrors synthesis in run and profile. The public verifier confirmed 7,105 available claims, 1,168 matching source blobs, all 2,356 summary sentences, identical rerun claim IDs and zero company/observation events. Fifteen mixed rendered examples are kept locally for review, outside the published tree. No one-employee company is supported in the sample; the small-firm example is labelled by its reported records instead. Template provider cost is $0. Live model execution was deliberately excluded; fake-provider tests verify valid frames, raw-number/missing-citation rejection, untrusted quoted instructions, timeout, caps and cache hits.

For reproducible summary checks with local inputs, run the same command twice with `--synthesis template` and the **same** `--previous` file, then compare run.synthesis. The offline unit suite exercises this without downloaded archives. Baseline first-observation wording is separately tested. Live source bytes can change and legitimately alter summaries.

The [live 100-company smoke summary](../reports/smoke-100.md) and [machine report](../reports/smoke-100-report.json) describe the fresh release check. Raw envelopes and source bodies are not published.

## Live recall and bounded activity

The two 300-company checks used seeds 20261014/20261015, `--websites --hiring --public-activity --time-budget-seconds 2400`, and no model calls. The first refreshed against the latest saved snapshot; the second was a fresh baseline. The weaker registry-declared path is default-off after group-company ambiguities. Final reviewed populations: 24 website rows, one NAV match and 33 dated website items; zero doubtful rows remained and all available-claim stored hashes/spans verified.

| Metric | Saved sample | Fresh sample |
|---|---:|---:|
| Verified websites | 20 / 300 (6.67%) | 19 / 300 (6.33%) |
| Companies with social profiles | 12 | 13 |
| Companies with fresh exact-number ads | 1 | 0 |
| Companies with public activity, including registry dates | 33 | 31 |
| Website dated items / registry date events | 19 / 68 | 14 / 52 |
| HTTP / DNS resolver invocations | 2,202 / 2,042 | 2,190 / 1,995 |
| Total reported runtime | 348.843 s | 336.406 s |
| NAV feed pages / feed seconds (warm cache) | 378 / 194.703 s | 378 / 190.484 s |
| NAV feed complete | yes | yes |
| False company changes on saved-sample refresh | 0 | baseline |

The saved-sample refresh had four coverage observations and zero company events. All runs had zero unhandled exceptions and no deadline hits. A complete header feed does not imply complete candidate details: ranked caps leave affected companies failed, never checked-negative. DNS counts include preflight and pinned connection resolutions, not just guessed-domain checks. Registry dates and website updates are reported separately so discovery coverage is not overstated.

## Profile site verification

Offline site tests cover all envelope shapes, membership, escaped untrusted content, safe links, evidence completeness, citation anchors, deterministic bytes and isolated template errors. The saved 300-company generation produces 302 pages; profiles must stay below 250 KB. Inspect index, BRANDO, a borettslag and compare at 1280 and 375 px, including file:// initialization, pagination, diacritics search, source toggles and overflow. Use installed browsers only; no browser dependency is required. Light/dark state chips include words, inputs have labels, toggles expose aria-expanded, and keyboard focus is visible. Browser QA supplements the offline suite; it is not a complete accessibility certification.

## Historical scale and external compatibility

The 1,000-company run took 488.679 seconds wall / 483.469 seconds reported, 5,975 HTTP requests and 6,770 DNS resolver invocations. The rerun took 479.360 seconds wall, with zero company changes and 34 observations. Both read 378 NAV pages completely: 191.297 and 234.141 feed seconds, with total NAV times 419.922 and 460.422 seconds. Detail caps remain separate from header completeness. The offline regenerated site is 53.515 MB, largest profile 73.440 KB, with exact evidence metadata stored once per response in per-company data scripts. The 64 MiB union envelope ceiling reduced one large company to explicit output-limit failures in both runs; contract output avoids the redundant profile.

Compatibility tests cover ten input encodings across union, contract and reference output, including extra keys, numeric identifiers, BOM/CRLF, duplicates and invalid records. Output order and repeated envelopes are independently verified. Eleven offline fault drills cover network, token, partial feed, storage, previous-input and budget failures. Before the raw-profile adapter was added, a read-only starter-kit proxy scorer rejected canonical envelope evidence lists with AttributeError. The current separate profiles adapter addresses that parsing difference, as recorded at the top of this document. No official score is claimed and final evaluator shape acceptance remains an open review risk.

The final contract release check preserved 1,000 ordered valid envelopes without any output-limit reduction under the unchanged 64 MiB ceiling. It used 5,980 HTTP requests, 6,800 DNS invocations and 494.094 reported seconds (company p50/p95 478.421/478.453 seconds). Warm-cache header feed (not a cold-run estimate): 378 pages, 239.968 feed seconds / 478.406 total NAV seconds, feed_complete true, 0.635 seconds/page. All 25,038 supported claims, 3,866 stored bodies and 8,092 cited sentences passed independent verification; zero exceptions or deadline hits. Coverage: 59 websites, 33 social-profile companies, two fresh exact-company ad companies and 118 public-activity companies. Output is 56.213 MB; site is 53.649 MB / 77.686 KB largest profile. Time/request headroom against 2,400 seconds/20,000 requests is 79.41%/70.10%. Four accounts and 301 hiring sections remain incomplete; the 500-detail cap is not an exhaustive national ad search.

## Wednesday cold release measurements

The historical [cold 1,000-company gate](../reports/release-1000.md) and [cold 100 smoke](../reports/smoke-100.md) supersede historical warm-cache estimates above. Default union plus separate raw profiles parse in the supplied proxy; canonical envelope evidence stays a list. All three envelope shapes verify. Final cold 1,000: 268.875 seconds, 5,074 HTTP, 6,809 DNS, 0 exceptions/deadline hits/reductions, feed complete, hiring failed 0%. Union 140.000 MB / contract123.854 MB (1.130363 ratio). NAV 2 forward pages /2.547feed seconds /0.279161decoded MB /141.312total seconds, above the120-second target; retain as open performance risk. Total time headroom88.80% meets the50% condition for retaining900-second NAV cap. Optional search is not configured, cost$0. Official evaluator acceptance remains unverified.


## Measured precision

Automated re-check of every published website, social profile, job, LEI, parent and procurement award in the latest three Stage T samples (300 company inputs). Counts are published items per sample, not unique companies across types. [Complete verdict ledger](../reports/r5/precision/LEDGER.md) preserves every value, proof tier, exact excerpt, URL, retrieval time, hash and review reason; no item was silently removed.

| Type | Checked | Correct | Doubtful | Wrong |
|---|---:|---:|---:|---:|
| website | 12 | 10 | 2 | 0 |
| social | 12 | 11 | 1 | 0 |
| job | 1 | 1 | 0 | 0 |
| LEI | 41 | 40 | 1 | 0 |
| parent | 2 | 2 | 0 | 0 |
| award | 0 | 0 | 0 | 0 |

Method: saved body hashes and verbatim spans; exact company ID, registry spelling, owner identifiers and group-site flags; strict own header/footer social links with founder/agency exclusions; current-at-retrieval exact NAV employer/proven subunit or owned careers chain; GLEIF exact NO/RA000472 and ACTIVE child-parent link; TED exact Norwegian buyer/selected tenderer through lot/contract award links. A legitimate foreign parent or notice counterparty is not a foreign attribution to the target. Doubtful/wrong items require hand review and remain in outputs.

These are automated rule-verification verdicts, not independently human-labelled precision or a population accuracy claim. Saved samples are small, live sources can change, and a correct saved receipt does not establish current internet truth. Zero published items for a type is zero measured precision coverage for that type, not 100% precision. Source absence, blocking and incomplete pagination stay explicit. No notice amount is published without proven sole-winner lot attribution; this implementation abstains from all amounts.

Human hand review (explicit user confirmation, 2026-11-13): 4 original Stage T items confirmed correct: GLÅMDAL MASKIN AS 995194163 website, CONCEDO AS 988217867 website and LinkedIn, and BØNES BØNES AS 922718059 LEI. All four automated-doubtful items are human-confirmed; automated counts and original proof tiers remain unchanged. This is a reviewed subset, not a broader precision estimate. See the separate ledger human-review column and human_reviews.json.

### Current three-sample measured results

| Metric | Frozen 20261017 (T) | Seed 20261113 (T) | Seed 20261114 (T) |
|---|---:|---:|---:|
| Websites | 5 | 4 | 3 |
| Social companies | 3 | 1 | 2 |
| Job companies | 0 | 1 | 0 |
| Contacts | 11 | 8 | 4 |
| Activity companies | 100 | 100 | 100 |
| Activity claims (registry/site) | 1202 | 1137 | 1093 |
| Facts | 13344 | 13763 | 13260 |
| LEI companies | 19 | 12 | 10 |
| Parent companies | 0 | 0 | 1 |
| Procurement award companies | 0 | 0 | 0 |
| HTTP | 700 | 792 | 736 |
| Reported seconds | 357.609 | 404.109 | 345.094 |
| Wall seconds | 370.777 | 412.763 | 354.648 |
| Derived ratios | 153 | 169 | 164 |
| Comparable YoY metrics | 50 | 63 | 60 |
| Unsupported values | 0 | 0 | 0 |
| Provider cost | $0 | $0 | $0 |
| Site / ordered terminal envelopes | 100 / 100 | 100 / 100 | 100 / 100 |

Refresh correctness (Stage E scope, before GLEIF/TED): 7/7 planted source interventions detected, 40 supported field events and zero unexpected events; unchanged/repeated false-change rate 0; 112 prior claims retained with stale markers on transient failures. Exact saved 100-company timestamp-format regression and final live frozen refresh both emitted 0 company changes and 0 coverage observations. This does not validate new-source refresh coverage. [Measured refresh correctness](REFRESH.md#measured-refresh-correctness).

Each item is present in the machine-readable ledger with its verdict checks and original run/output SHA-256. Reproduce with `python scripts/precision_ledger.py`; this performs no HTTP requests, uses the latest Stage T settings paths and never rewrites envelopes. Three offline ledger tests cover broken bytes/URL substitution, retained doubtful group-site attribution and strict social header/footer context. Full pytest gate: reports/r5/precision/pytest.txt. No independent human hand-check is claimed.
