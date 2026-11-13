# W0 saved-evidence audits

Baseline application: d66a177a on revision/r5. W0 committed reports only (bb2a919f); later report corrections use the tested R1 extraction without changing historical outputs. No publication, proof threshold or tier changed in W0. Full baseline pytest: 954 passed in 215.36s. No push; paid cost $0.

Six saved samples contain 600 distinct ordered inputs. They publish 29 websites: 26 VERIFIED and three HIGH. Registry declarations: 72 companies list a homepage; 13 publish that declared domain (18.06%), split 10 VERIFIED and three HIGH. Strict exact-number declared-domain recall is 10/72 (13.89%). HIGH is never relabelled VERIFIED. Declaration recall is not independent ownership ground truth.

Overlapping rejection categories: 24 companies with veto attempts, 44 ambiguous sections and 156 fetched-without-proof companies; union 176. rejections.md/json list every included company, recorded candidate rules, saved request/nomination URL basis, page titles/hashes and identity signals. Full legal names preserve punctuation and legal suffix, with case/Unicode/whitespace normalization only. Header/logo/footer/copyright/contact regions use R1 to avoid page-wide layout traits; ordinary body mentions remain distinct. Phone links, full emails/domains, street+postcode, declared domains, structured owner IDs, other forms, group and provider markers are audited. Candidate-level historic outcomes cannot be invented as per-page decisions. URLs/bodies not retained in old traces remain explicitly unknown.

DNS: 2,507 unique company/candidate nominations have OS name-not-found, plus seven generic historical failures (2,511 / seven attempt records before deduplication). OS errors do not preserve authoritative RCODEs; generic errors can also mean nomination cutoff. The seven unique non-name-not-found hosts were each re-resolved once through Google Public DNS, A query, DNSSEC enabled, zero ECS: all seven returned SERVFAIL and none returned an A address. Exact responses/UTC/hash in dns_recheck.json. An A-only failure is not proof that a domain does not exist. Seven diagnostic HTTP calls, separately counted from evaluator runs; no identity publication follows from DNS.

The resolver's [API documentation](https://developers.google.com/speed/public-dns/docs/doh/json), [terms](https://developers.google.com/speed/public-dns/terms) and [privacy](https://developers.google.com/speed/public-dns/privacy) were checked. No returned address was fetched. Original input audit hash remains recorded; report corrections did not repeat DNS queries.

Bundled NAV index: built 2026-11-13T08:23:53.796625Z; 9,511 ads and 6,012 employers. None of the workplace IDs directly matches the 411,160-company universe. An exact join against all 1,177,860 main-entity snapshot rows also finds none, so that snapshot cannot supply workplace parents (nav_bulk_join.json).

The optional bulk-download helper's root robots preflight disconnected twice; zero bulk requests followed. The documented, already-approved official registry REST policy supports exact orgnr array queries. The audit subsequently used that endpoint with 200 IDs/query, pinned public DNS, TLS verification, no redirects, one connection and five-second pacing. This is licensed machine-API access, not a website crawl or a robots-refusal bypass. [Official API documentation](https://data.brreg.no/enhetsregisteret/api/dokumentasjon/no/index.html), Brønnøysundregistrene / NLOD 2.0 attribution, raw hashes, dates and exact JSON field pairings are retained in nav_parent_join.json. No name joins or runtime enrichment changes.

| NAV / universe measure | Result |
|---|---:|
| Indexed employers classified | 6,012 / 6,012 |
| Employers with exact returned parent | 6,009 |
| Distinct returned parents | 3,407 |
| Confirmed parent companies in universe | 2,133 |
| Confirmed expected companies / 1,000 | 5.187761 |
| Upper bound if three absent parents were distinct eligible companies | 5.195058 |
| Measured job companies / 1,000 | 5.000000 (3 / 600) |
| Audit HTTP / active tool seconds | 34 / 234.000 |

All three index-matched sample companies—DIGITALIQ, HIGHLAND LODGE and VALAKER—have a published job in the saved runs. This checks the sampled index-covered scope, not all jobs in Norway. Current-at-retrieval posting proof remains mandatory; index membership alone never creates a job claim.

Three missing search results are deleted-unit tombstones, with no former parent returned: 881521032 (source slettedato 2026-10-19), 983036961 (2026-05-05), 988083895 (2026-05-27). Their names are not used to infer a parent. The raw all-parent point estimate remains unknown; the narrow 5.188–5.195 interval makes the uncertainty visible. Direct record receipts and independent pointer/hash verification are retained. The first tombstone caused a strict parser assertion; that error is preserved and resolved as a legitimate deleted-record state, without granting a parent. Its saved response was reused, never re-requested.

The parent audit used 34 HTTP attempts within 40 and 234.000 active seconds within 300; operator intervals and individual UTC receipts remain visible. Zero unsupported parent values. It ran after the final live qualifications, so its calls do not enter their timing/request totals. Combined ancillary attempts: seven DNS, two failed bulk preflights and 34 parent API calls, paid cost $0. Runtime profiles, NAV index and rarity bundle were not modified by this diagnostic join. A targeted 6,012-ID join is not a complete underenheter snapshot for frequency estimation.
