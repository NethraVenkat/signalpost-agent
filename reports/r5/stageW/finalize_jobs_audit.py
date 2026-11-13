"""Merge the verified registry join into the final W0 report, retaining limits."""
import hashlib
import json
import re
from audit import DEST


def main():
    data = json.loads((DEST / 'rejections.json').read_text(encoding='utf8'))
    result = json.loads((DEST / 'nav_parent_join.json').read_text(encoding='utf8'))
    checked = json.loads((DEST / 'nav_parent_verification.json').read_text(encoding='utf8'))
    assert checked['unsupported_parent_values'] == 0 and result['http_requests'] <= 40
    jobs = data['jobs']
    jobs.update(initial_saved_parent_lower_bound_companies=3,
                mapped_index_employers=result['mapped_employers'], classified_index_employers=result['classified_employers'],
                distinct_registered_parents=result['distinct_parents'],
                proven_parent_employers_in_universe=checked['parent_companies_in_universe'],
                unique_represented_companies=checked['unique_expected_companies'],
                expected_per_1000_lower_bound=checked['confirmed_rate_per_1000'],
                expected_per_1000_upper_bound=checked['possible_upper_rate_per_1000'],
                exact_all_parent_point_estimate=result['expected_rate_per_1000'],
                deleted_index_employers_without_parent=result['deleted_unmapped_employers'],
                sample_index_matched_companies=checked['sample_index_matched_companies'],
                parent_join_http_requests=result['http_requests'], parent_join_active_runtime_seconds=result['runtime_seconds'],
                parent_join_receipts='nav_parent_join.json', parent_join_verification='nav_parent_verification.json',
                limitation='Index discovery expectation, not current job-posting proof. Three deleted-unit tombstones omit their former parent; no name-based parent inference. Interval allows at most one additional distinct eligible parent per unresolved unit. Index/registry retrieval dates differ; this targeted join is not a nationwide subunit snapshot.')
    (DEST / 'rejections.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
    path = DEST / 'rejections.md'; text = path.read_text(encoding='utf8')
    text = re.sub(r'(## NAV/universe overlap\n\n```json\n).*?(\n```)', lambda m: m.group(1) + json.dumps(jobs, ensure_ascii=False, indent=2) + m.group(2), text, count=1, flags=re.S)
    path.write_text(text, encoding='utf8', newline='\n')
    dns_path = DEST / 'dns_recheck.json'; dns = json.loads(dns_path.read_text(encoding='utf8'))
    dns['input_audit_sha256'] = hashlib.sha256((DEST / 'rejections.json').read_bytes()).hexdigest()
    dns['input_correction'] = 'Final report-only corrections and verified NAV-parent audit merged. Original DNS candidate records unchanged; no resolver query repeated.'
    dns_path.write_text(json.dumps(dns, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
    lower, upper = checked['confirmed_rate_per_1000'], checked['possible_upper_rate_per_1000']
    report = f'''# W0 saved-evidence audits

Baseline application: d66a177a on revision/r5. W0 committed reports only (bb2a919f); later report corrections use the tested R1 extraction without changing historical outputs. No publication, proof threshold or tier changed in W0. Full baseline pytest: 954 passed in 215.36s. No push; paid cost $0.

Six saved samples contain 600 distinct ordered inputs. They publish 29 websites: 26 VERIFIED and three HIGH. Registry declarations: 72 companies list a homepage; 13 publish that declared domain (18.06%), split 10 VERIFIED and three HIGH. Strict exact-number declared-domain recall is 10/72 (13.89%). HIGH is never relabelled VERIFIED. Declaration recall is not independent ownership ground truth.

Overlapping rejection categories: 24 companies with veto attempts, 44 ambiguous sections and 156 fetched-without-proof companies; union 176. rejections.md/json list every included company, recorded candidate rules, saved request/nomination URL basis, page titles/hashes and identity signals. Full legal names preserve punctuation and legal suffix, with case/Unicode/whitespace normalization only. Header/logo/footer/copyright/contact regions use R1 to avoid page-wide layout traits; ordinary body mentions remain distinct. Phone links, full emails/domains, street+postcode, declared domains, structured owner IDs, other forms, group and provider markers are audited. Candidate-level historic outcomes cannot be invented as per-page decisions. URLs/bodies not retained in old traces remain explicitly unknown.

DNS: 2,507 unique company/candidate nominations have OS name-not-found, plus seven generic historical failures (2,511 / seven attempt records before deduplication). OS errors do not preserve authoritative RCODEs; generic errors can also mean nomination cutoff. The seven unique non-name-not-found hosts were each re-resolved once through Google Public DNS, A query, DNSSEC enabled, zero ECS: all seven returned SERVFAIL and none returned an A address. Exact responses/UTC/hash in dns_recheck.json. An A-only failure is not proof that a domain does not exist. Seven diagnostic HTTP calls, separately counted from evaluator runs; no identity publication follows from DNS.

The resolver's [API documentation](https://developers.google.com/speed/public-dns/docs/doh/json), [terms](https://developers.google.com/speed/public-dns/terms) and [privacy](https://developers.google.com/speed/public-dns/privacy) were checked. No returned address was fetched. Original input audit hash remains recorded; report corrections did not repeat DNS queries.

Bundled NAV index: built {result['index_built_at']}; 9,511 ads and 6,012 employers. None of the workplace IDs directly matches the 411,160-company universe. An exact join against all 1,177,860 main-entity snapshot rows also finds none, so that snapshot cannot supply workplace parents (nav_bulk_join.json).

The optional bulk-download helper's root robots preflight disconnected twice; zero bulk requests followed. The documented, already-approved official registry REST policy supports exact orgnr array queries. The audit subsequently used that endpoint with 200 IDs/query, pinned public DNS, TLS verification, no redirects, one connection and five-second pacing. This is licensed machine-API access, not a website crawl or a robots-refusal bypass. [Official API documentation](https://data.brreg.no/enhetsregisteret/api/dokumentasjon/no/index.html), Brønnøysundregistrene / NLOD 2.0 attribution, raw hashes, dates and exact JSON field pairings are retained in nav_parent_join.json. No name joins or runtime enrichment changes.

| NAV / universe measure | Result |
|---|---:|
| Indexed employers classified | {result['classified_employers']:,} / 6,012 |
| Employers with exact returned parent | {result['mapped_employers']:,} |
| Distinct returned parents | {result['distinct_parents']:,} |
| Confirmed parent companies in universe | {checked['parent_companies_in_universe']:,} |
| Confirmed expected companies / 1,000 | {lower:.6f} |
| Upper bound if three absent parents were distinct eligible companies | {upper:.6f} |
| Measured job companies / 1,000 | 5.000000 (3 / 600) |
| Audit HTTP / active tool seconds | {result['http_requests']} / {result['runtime_seconds']:.3f} |

All three index-matched sample companies—DIGITALIQ, HIGHLAND LODGE and VALAKER—have a published job in the saved runs. This checks the sampled index-covered scope, not all jobs in Norway. Current-at-retrieval posting proof remains mandatory; index membership alone never creates a job claim.

Three missing search results are deleted-unit tombstones, with no former parent returned: 881521032 (source slettedato 2026-10-19), 983036961 (2026-05-05), 988083895 (2026-05-27). Their names are not used to infer a parent. The raw all-parent point estimate remains unknown; the narrow {lower:.3f}–{upper:.3f} interval makes the uncertainty visible. Direct record receipts and independent pointer/hash verification are retained. The first tombstone caused a strict parser assertion; that error is preserved and resolved as a legitimate deleted-record state, without granting a parent. Its saved response was reused, never re-requested.

The parent audit used {result['http_requests']} HTTP attempts within 40 and {result['runtime_seconds']:.3f} active seconds within 300; operator intervals and individual UTC receipts remain visible. Zero unsupported parent values. It ran after the final live qualifications, so its calls do not enter their timing/request totals. Combined ancillary attempts: seven DNS, two failed bulk preflights and 34 parent API calls, paid cost $0. Runtime profiles, NAV index and rarity bundle were not modified by this diagnostic join. A targeted 6,012-ID join is not a complete underenheter snapshot for frequency estimation.
'''
    (DEST / 'W0_REPORT.md').write_text(report, encoding='utf8', newline='\n')
    print(json.dumps({'expected_rate_interval_per_1000': [lower, upper], 'measured_rate_per_1000': 5, 'parent_http': result['http_requests']}))


if __name__ == '__main__':
    main()
