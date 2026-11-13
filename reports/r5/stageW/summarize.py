"""Finalize measured foundation report from saved artifacts, never alter output."""
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from audit import DEST, ROOT, SAMPLES, load_runs


def read(path):
    return json.loads(path.read_text(encoding='utf8'))


def urls(rows):
    result = {}
    for row in rows:
        evidence = {e['id']: e for e in row['evidence']}
        name = (row['run'].get('legal_identity') or {}).get('legal_name')
        for c in row['claims']:
            if c['availability'] != 'available' or not (c['field'] == 'official_website' or c['field'].startswith('social_profile.')):
                continue
            value = c['value']
            url = value.get('final_url') if c['field'] == 'official_website' else value.get('url')
            result[(row['organisation_number'], c['field'], url)] = {'orgnr': row['organisation_number'], 'name': name, 'url': url,
                    'field': c['field'], 'proof_tier': value.get('identity_level') or value.get('proof_tier'),
                    'evidence': [evidence[e] for e in c['evidence_ids']]}
    return result


def main():
    audit = read(DEST / 'rejections.json'); dns = read(DEST / 'dns_recheck.json'); rarity = read(DEST / 'rarity.json')
    all_deltas = []; rows_md = []; unchanged_sites = 0
    inventory = {}
    for seed, previous, registry, before_rows, before_report in load_runs():
        folder = DEST / ('seed' + str(seed)); config = read(folder / 'settings.json'); work = Path(config['working_directory'])
        counts = read(folder / 'counts.json'); verification = read(folder / 'verification.json'); report = read(folder / 'report.json')
        assert verification['complete_briefing_contracts'] == 100 and verification['synthesis_unverified_values'] == verification['briefing_unverified_values'] == 0
        assert verification['site_verified'] and counts['http_after'] <= 1850 and counts['runtime_seconds'] <= 2100 and counts['cost_usd'] == 0
        assert report['llm']['calls'] == report['search']['queries'] == 0
        current = [json.loads(line) for line in (work / 'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
        # Early wrapper logs mislabeled all-section counts as website_states.
        # Correct the derived counts from immutable saved envelopes, never the
        # underlying report, output or original execution log.
        counts['section_availability_counts'] = report['counts_by_availability']
        counts['website_states'] = dict(Counter(r['run']['sections']['website'] for r in current))
        counts['counts_note'] = 'Website states recomputed from envelopes; global availability counts retained separately. Raw execution logs unchanged.'
        (folder / 'counts.json').write_text(json.dumps(counts, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
        old, new = urls(before_rows), urls(current)
        added = [new[k] for k in sorted(new.keys() - old.keys())]; removed = [old[k] for k in sorted(old.keys() - new.keys())]
        all_deltas.append({'seed': seed, 'added': added, 'removed': removed})
        inventory[str(seed)] = list(new.values())
        unchanged_sites += sum(k[1] == 'official_website' for k in old.keys() & new.keys())
        rows_md.append(f"| {seed} | {counts['websites_before']} | {counts['websites_after']} | {counts['http_before']} | {counts['http_after']} | {counts['runtime_seconds']:.3f} | 0 |")
    out = {'comparisons': all_deltas, 'published_inventory': inventory}
    (DEST / 'r4_url_inventory.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
    lines = ['# R4 website/social URL changes', '', 'Each removed item uses the prior saved proof, never proof of current closure. Each added item uses the new saved proof. No new proof tier is introduced.', '']
    for delta in all_deltas:
        lines += [f"## {delta['seed']}", '']
        for direction in ('added', 'removed'):
            lines += [f"{direction.title()}: {len(delta[direction])}.", '']
            for item in delta[direction]:
                lines += [f"### {item['orgnr']} / {item['name']} / {item['field']}", '', f"URL: {item['url']}; proof tier: {item['proof_tier']}.", '']
                for e in item['evidence']:
                    lines += [f"Source: {e['source_url']}; retrieved {e['retrieved_at']}; SHA-256 `{e['content_sha256']}`; locator `{e['locator']}`.", '', '```text', e['claim_span'], '```', '']
    (DEST / 'new_websites.md').write_text('\n'.join(lines), encoding='utf8', newline='\n')
    summary = ['# W0 / R1 / R2 / R4 foundations', '', 'Branch revision/r5. Author Nethra Venkat. No push, publication, model or paid search. Provider cost $0. No new proof tier.', '',
               '## W0 saved-output baseline', '', '| Seed | Sites | Registry homepage | Declared domain published | Veto | Ambiguous | Fetched without proof |', '|---|---:|---:|---:|---:|---:|---:|']
    for s in audit['samples']:
        summary.append('| ' + ' | '.join(str(s.get(k, 0)) for k in ('seed', 'websites', 'declared_homepage', 'declared_domain_published', 'veto', 'ambiguous', 'fetched-without-proof')) + ' |')
    total_declared = sum(s.get('declared_homepage', 0) for s in audit['samples']); total_published = sum(s.get('declared_domain_published', 0) for s in audit['samples'])
    summary += ['', f"Declared-homepage domain recall: {total_published}/{total_declared} = {total_published / total_declared:.2%}. This is declaration recall, not independently established current ownership. Rejection categories overlap: {json.dumps(audit['category_counts'], ensure_ascii=False)}. rejections.md/json retain all company/candidate/page details and identity locations.", '',
                'The saved baseline contains 26 VERIFIED and three HIGH websites. Declared-domain publications split 10 VERIFIED / three HIGH; strict exact-number declaration recall is 10/72 (13.89%). HIGH remains a distinct existing tier.', '',
                f"Historical DNS attempt records: {json.dumps(audit['dns_historical_counts'])}. Unique company/candidate nominations: {json.dumps(audit['dns_unique_candidate_counts'])}. Generic errors can include a nomination cutoff and cannot honestly be split into old SERVFAIL versus timeout. Public resolver once-only A checks: {dns['completed']} unique hosts; {json.dumps(dns['counts'])}; {dns['http_requests']} separately reported diagnostic HTTP, $0. Two failed official bulk robots attempts are separately retained; zero bulk download requests. No positive DNS answer becomes proof.", '',
                '## Jobs index overlap', '', '```json', json.dumps(audit['jobs'], ensure_ascii=False, indent=2), '```', '',
                'The licensed official exact-ID REST query resolved 6,009 employer-parent pairs and classified all 6,012 employers. The other three are deleted-unit tombstones without former parents; no name join fills them. Confirmed index/universe coverage is 2,133 companies: 5.187761 per 1,000, with an optimistic upper bound 5.195058 if those three missing parents were distinct eligible companies. Measured coverage is three job companies / 600 = 5 per 1,000. All three currently index-matched sample companies (DIGITALIQ, HIGHLAND LODGE, VALAKER) publish a job. This is an index-discovery expectation, not proof that every indexed ad remains current. Source hashes, exact record pairings, deleted records and independent recount are in nav_parent_join.json / nav_parent_verification.json. Auxiliary API cost: 34 HTTP attempts, 234 active tool seconds, $0; separate from evaluator runs. The optional bulk robots preflight failed; the existing approved licensed REST policy supplied the targeted audit without a website crawl or access-refusal bypass.', '',
                '## R1 and R2', '', 'R1 isolates labelled publisher context from customer/partner/reference/article/news/hidden/script/agency-credit content. Seven focused fixtures; full gate 961 passed. It does not add positive evidence. R1_REPORT.md details limitations.', '',
                f"R2 bundle: {rarity['entity_count']:,} distinct entities; {rarity['bytes']:,} bytes; source/table hashes and dates in rarity.json. Runtime lookup is local-only and dormant for proof scoring. No subunit snapshot is represented as present. Duplicate entity/key pairs count once.", '', '| Key | 1 entity | 2 | 3–4 | ≥5 |', '|---|---:|---:|---:|---:|']
    for kind, dist in rarity['distribution'].items():
        summary.append('| ' + kind + ' | ' + ' | '.join(str(dist.get(k, 0)) for k in ('1', '2', '3–4', '≥5')) + ' |')
    summary += ['', '## R4 conflict guard and six fresh measurements', '',
                'The guard rejects conflicting publisher IDs (proven target/subunits excepted), incompatible legal forms (AS/ASA excepted), explicit group branding without the target number, placeholders/default hosting, and third-party service publishers. It precedes positive scoring. Every previous veto and positive threshold is retained. Subunit fallback cannot override a publisher conflict. The local rarity table never promotes a candidate.', '',
                'Exact historical proof-page replay: all 29 published websites survive the new guard. All 73 fetched pages on those accepted candidates, including follow-ups, also pass the new guard (r4_all_published_pages.json). A false SISSENER group match on “as part of the selection process” was caught and narrowed to explicit group/parent markers. The first live six-sample trial exposed a second false veto on SISSENER’s about page: a page-wide header-over-content layout class made employee biographies look like publisher branding. Region detection now matches actual header/footer components, including underscore separators, rather than generic layout modifiers. Stronger HIGH-without-number fixtures exposed compound wrappers aggregating footer contacts or copyright; only actual contact blocks and atomic copyright lines contribute. All three retained buggy extractors fail the fixture with its footer copyright line, while the final extractor passes HIGH at unchanged thresholds (r4_regression_before_after.json). Exact failure receipts, old sources and superseded runs remain under trials/. Intermediate drivers were stopped to avoid more superseded calls; their current CLI children completed all mandatory outputs and independently verified, with uncaptured exit codes/source-import windows left unknown. All six accepted runs were repeated with fresh state and final source; no trial substitutes for an accepted run and no historical proof was carried forward. The synthetic multi-company group fixtures now test withholding and downstream suppression. Exact NAV jobs remain independent of website rejection. Replay imports lazy NAV modules before freezing time, fixing first/second replay expiry inconsistency without production behavior changes.', '',
                '| Seed | Prior sites | R4 sites | Prior HTTP | R4 HTTP | Wall seconds | Cost USD |', '|---|---:|---:|---:|---:|---:|---:|'] + rows_md
    summary += ['', f"Unchanged prior website URLs across live runs: {unchanged_sites} / 29; zero removals. Every run uses exactly the seven evaluator flags, original ordered inputs, a new run ID and fresh state. Each independently passes 100 ordered terminal envelopes, all five cited briefing elements, zero unsupported values, site membership, <=1,850 HTTP and <=2,100 seconds. Settings, complete reports, verifier results and hashes are in each seed folder. r4_source_manifest.json identifies the actual measured production bytes; parent commits in settings may precede the R4 commit because measurements happen before commit.", '',
                'The literal zero-additions condition against historical outputs is not met: LOOPYTY AS 933519708 recovered from an earlier timeout on the same already-nominated loopyty.com candidate. The final site contains the exact target number in its own copyright footer. Unmodified pre-R4 code from committed R2 (81a76b8d) verifies and localizes that exact saved response as VERIFIED (legacy_addition_replay.json). R4 introduces no new positive rule/tier and rarity is unused; this recovery is not attributed to a foundation proof improvement. Final publication is 30 sites (27 VERIFIED / three HIGH), retaining all 29 originals. The historical +1 is disclosed rather than hidden by rewriting output or hard-coding a sample-specific veto. Hand-check the exact new URL/receipt in new_websites.md. No social URL addition/removal is expected; the actual delta inventory is authoritative.', '',
                'Website/social URL deltas and exact proof receipts are in new_websites.md / r4_url_inventory.json. Inspect the source-timeout recovery exception when assessing the requested no-additions measurement; no zero-addition claim is made for the historical URL set.', '',
                '## Commits and validation', '', '```text', subprocess.check_output(['git', 'log', '-3', '--format=%h %s'], cwd=ROOT, text=True).strip(), '```', '',
                'R4 implementation and this final summary share the final stage commit; git log -1 supplies its hash after commit. A commit cannot contain its own final hash. W0 gate: 954 passed; R1 gate: 961 passed; R2 working-tree gate: 979 passed, followed by an independent exact committed-R2 worktree gate: 964 passed (r2_committed_tree_check.json). Final R4 full gate: 983 passed in 153.18 seconds (pytest-R4-release.txt), with 26 focused publisher tests and all 73 fetched pages on 29 historical published sites replayed. The biography regression exercises the corroborated HIGH path without an exact number, matching the actual SISSENER failure. Trial failures remain in pytest-*.txt; none authorized a stage commit.', '',
                '## Hand checks and limits', '',
                '- Inspect every rule/page association in rejections.json; old output saved candidate-level outcomes, so per-page rejection attribution is not invented.',
                '- Check the seven public DNS responses. OS name-not-found is not an authoritative saved RCODE, and an A-only check is not a complete DNS-existence test.',
                '- Review the three deleted NAV workplace IDs and their absent former-parent fields. The expected-rate interval is bounded; names never establish a missing parent.',
                '- Hand-check LOOPYTY AS 933519708 / https://loopyty.com: one historical source-timeout recovery, accepted by unchanged pre-R4 proof code. This is the disclosed exception to a literal zero-additions result.',
                '- Review r4_published_replay.json, including human-reviewed SISSENER, CONCEDO and GLÅMDAL; human verdicts and existing proof tiers remain distinct.',
                '- Publisher extraction cannot evaluate CSS-computed visibility or infer unmarked customer-list semantics. Existing independent proof vetoes remain active.',
                '- Registry snapshot dates and the current live sources differ; this is a measured sample comparison, not an accuracy guarantee. No model calls, paid APIs or search; source licences/terms remain in docs/SOURCES.md. Stop after these foundations; no new proof tier or next stage.']
    (DEST / 'SUMMARY_FOUNDATIONS.md').write_text('\n'.join(summary) + '\n', encoding='utf8', newline='\n')
    print(json.dumps({'url_changes': [{ 'seed': d['seed'], 'added': len(d['added']), 'removed': len(d['removed'])} for d in all_deltas], 'unchanged_sites': unchanged_sites}))


if __name__ == '__main__':
    main()
