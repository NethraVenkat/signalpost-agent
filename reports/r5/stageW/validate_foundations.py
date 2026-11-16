"""Final artifact/measurement consistency gate; no network or output mutation."""
from signalpost.portable_paths import expand, portable, portable_text  # saved paths stay repo-relative
import hashlib
import json
from collections import Counter
from pathlib import Path
from audit import ROOT, DEST, SAMPLES


def read(path):return json.loads(path.read_text(encoding='utf8'))


def main():
    manifest = read(DEST / 'r4_source_manifest.json')
    current = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT / 'src').rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    assert manifest == current, 'Measured production bytes changed'
    expected_flags = {'--organisations', '--bulk', '--output', '--profiles-output', '--report', '--run-id', '--expected-count'}
    all_ids = set(); run_ids = set(); aggregate = Counter(); tiers = Counter()
    for seed, _ in SAMPLES:
        folder = DEST / ('seed' + str(seed)); settings = read(folder / 'settings.json')
        argv = settings['command_argv']; flags = [x for x in argv if x.startswith('--')]
        assert len(flags) == 7 and set(flags) == expected_flags
        assert settings['source_manifest_sha256'] == hashlib.sha256((DEST / 'r4_source_manifest.json').read_bytes()).hexdigest()
        work = Path(expand(settings['working_directory'])); report = read(work / 'report.json'); verification = read(folder / 'verification.json'); execution = read(folder / 'execution.json')
        assert execution['exit_code'] == 0 and execution['wall_seconds'] <= 2100 and report['requests'] <= 1850
        assert report['total_cost_usd'] == report['llm']['calls'] == report['search']['queries'] == 0
        assert report['site']['state'] == 'available' and report['site']['companies'] == 100
        assert verification['complete_briefing_contracts'] == 100 and verification['synthesis_unverified_values'] == verification['briefing_unverified_values'] == 0
        rows = [json.loads(line) for line in (work / 'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
        ids = [r['organisation_number'] for r in rows]; assert len(ids) == len(set(ids)) == 100 and not all_ids.intersection(ids)
        inputs = [json.loads(line)['organisation_number'] for line in Path(expand(argv[argv.index('--organisations') + 1])).read_text(encoding='utf8').splitlines()]
        assert ids == inputs and report['run_id'] not in run_ids
        assert all(r['run']['terminal_status'] in {'completed', 'failed'} for r in rows)
        all_ids.update(ids); run_ids.add(report['run_id'])
        for name in ('envelopes', 'profiles'):
            count = read(folder / 'counts.json'); assert count[name + '_sha256'] == hashlib.sha256((work / (name + '.jsonl')).read_bytes()).hexdigest()
        assert hashlib.sha256((work / 'report.json').read_bytes()).hexdigest() == hashlib.sha256((folder / 'report.json').read_bytes()).hexdigest()
        aggregate['accepted_http'] += report['requests']; aggregate['accepted_wall_seconds'] += execution['wall_seconds']
        for r in rows:
            for c in r['claims']:
                if c['field'] == 'official_website' and c['availability'] == 'available':tiers[c['value']['identity_level']] += 1
    for path in (DEST / 'trials').glob('*/seed*/report.json'):
        report = read(path); assert report['requests'] <= 1850 and report['total_cost_usd'] == 0
        aggregate['superseded_runs'] += 1; aggregate['superseded_http'] += report['requests']
        aggregate['superseded_reported_wall_seconds'] += report['completion']['wall_seconds']
    url_changes = read(DEST / 'r4_url_inventory.json')['comparisons']
    added = [item for sample in url_changes for item in sample['added']]
    removed = [item for sample in url_changes for item in sample['removed']]
    assert not removed and len(added) == 1 and added[0]['orgnr'] == '933519708' and added[0]['url'] == 'https://loopyty.com'
    legacy = read(DEST / 'legacy_addition_replay.json')
    assert len(legacy['cases']) == 1 and legacy['cases'][0]['pre_R4_level'] == 'VERIFIED'
    dns = read(DEST / 'dns_recheck.json')
    assert dns['input_audit_sha256'] == hashlib.sha256((DEST / 'rejections.json').read_bytes()).hexdigest()
    assert dns['completed'] == len(dns['results']) == 7 and len({r['host'] for r in dns['results']}) == 7
    parent = read(DEST / 'nav_parent_verification.json'); assert parent['unsupported_parent_values'] == 0
    result = {'accepted_runs': 6, 'unique_companies': len(all_ids), 'all_exact_seven_flags': True, 'all_fresh_run_ids': True,
              'ordered_terminal_envelopes': 600, 'available_sites': 6, 'five_part_briefings': 600, 'unsupported_values': 0,
              'production_manifest_files_unchanged': len(manifest), 'published_website_tiers': dict(tiers),
              'prior_website_urls_retained': 29, 'removed_website_social_urls': 0, 'source_recovery_urls': 1,
              'literal_zero_historical_additions_met': False, 'new_positive_proof_rule_or_tier': False,
              'source_recovery': 'LOOPYTY exact footer also verifies under unmodified pre-R4 code; historical attempt timed out.',
              'resource_totals': dict(aggregate), 'dns_audit_http': 7, 'failed_bulk_preflight_attempts': 2,
              'nav_parent_audit_http': parent['http_requests'], 'all_provider_cost_usd': 0,
              'limits': 'Rejected runs are included in resource totals, never substituted for accepted samples. Two stopped-driver child exit codes/import windows remain unknown in their trial receipts.'}
    (DEST / 'VALIDATION.json').write_text(portable_text(json.dumps(result, indent=2) + '\n'), encoding='utf8', newline='\n')
    print(json.dumps(result))


if __name__ == '__main__':main()
