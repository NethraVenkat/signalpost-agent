"""Measure the earlier website cutoff and runtime site guard on one frozen cohort."""

import argparse
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

from signalpost.budget import PASS2_FINALISATION_SECONDS, PASS2_MARGIN_SECONDS, SECONDS_PER_100
from signalpost.portable_paths import sanitize_file

DEST = Path(__file__).resolve().parent
ROOT = DEST.parents[2]
sys.path.insert(0, str(DEST.parent / 'stageW'))
import measure_seed_index as measurement

SEED = 20261117
WORK = ROOT / '.data/r5/stageFX'
BASELINE = ROOT / '.data/r5/stageW-measurements' / f'seed{SEED}'


def output_counts(work):
    states = {}
    claims = Counter()
    deadlines = {}
    with (work / 'envelopes.jsonl').open(encoding='utf8') as stream:
        for line in stream:
            row = json.loads(line)
            for section, state in row['run']['sections'].items():
                states.setdefault(section, Counter())[state] += 1
            for claim in row['claims']:
                if claim['availability'] == 'available':
                    claims[claim['family']] += 1
            for error in row['errors']:
                if error['code'] == 'deadline':
                    deadlines.setdefault(error['section'], set()).add(row['organisation_number'])
    return states, claims, {section: len(orgs) for section, orgs in sorted(deadlines.items())}


def measure(retry):
    measurement.WORK = WORK
    measurement.RECEIPTS = DEST
    label = f'seed{SEED}' + ('-retry' if retry else '')
    work, receipts = WORK / label, DEST / label
    settings = measurement.read(measurement.p3_directory(SEED) / 'settings.json')
    baseline_receipts = DEST.parent / 'stageW/seed_index_measurements' / f'seed{SEED}'
    baseline = measurement.read(BASELINE / 'report.json')
    baseline_execution = measurement.read(baseline_receipts / 'execution.json')
    baseline_result = measurement.read(baseline_receipts / 'result.json')
    assert measurement.sha(BASELINE / 'envelopes.jsonl') == baseline_result['envelopes_sha256']
    old_states, old_claims, old_deadlines = output_counts(BASELINE)
    status = measurement.measure(SEED, retry, run_id_prefix='r5-stageFX')
    report_path = work / 'report.json'
    if not report_path.is_file():
        return status or 1
    shutil.copyfile(report_path, receipts / 'report.json')
    sanitize_file(receipts / 'report.json')
    report = measurement.read(report_path)
    execution = measurement.read(receipts / 'execution.json')
    states, claims, deadlines = output_counts(work)
    exact = ('gleif', 'procurement', 'state_aid', 'research', 'licences', 'inspections')
    pass2 = report['adaptive_websites'].get('pass2', {})
    prior = baseline['adaptive_websites']['pass2']
    last_pass2 = max((e['attempt_started'] for e in report['request_log'] if e.get('pass') == 'pass2'), default=None)
    largest = report['site'].get('largest_profile_bytes')
    verified = measurement.read(receipts / 'result.json')['verification'] if not status else {}
    gates = {
        'live_checker_passed': not status,
        'fixed_budget': report['limits']['effective_time_budget_seconds'] == 2100
                        and report['limits']['deadline_fraction'] == 0.85,
        'frozen_subset_used': report.get('bulk_snapshot_sha256') == settings['bulk_sha256'],
        'required_outputs': report['emitted_envelopes'] == report['profiles_output']['rows'] == 100
                            and not report['output_limited_companies'],
        'pass2_within_cutoff': 'cutoff_seconds' in pass2 and (last_pass2 is None or last_pass2 <= pass2['cutoff_seconds']),
        'exact_id_no_deadlines': all(family not in deadlines for family in exact),
        'profile_html_cap': largest is not None and largest == verified.get('largest_profile_bytes') < 250_000,
        'cost_zero': report['total_cost_usd'] == 0 and report['llm']['calls'] == report['search']['queries'] == 0,
    }
    cutoff_500 = SECONDS_PER_100 - PASS2_MARGIN_SECONDS - PASS2_FINALISATION_SECONDS
    summary = {
        'seed': SEED, 'inputs': {field: settings[field] for field in ('input_sha256', 'bulk_sha256')},
        'wall_seconds': execution['wall_seconds'], 'baseline_wall_seconds': baseline_execution['wall_seconds'],
        'http_requests': report['requests'], 'baseline_http_requests': baseline['requests'],
        'envelopes': report['emitted_envelopes'], 'profiles': report['profiles_output']['rows'],
        'placeholders': len(report['output_limited_companies']), 'largest_profile_bytes': largest,
        'baseline_largest_profile_bytes': baseline['site'].get('largest_profile_bytes'),
        'baseline_report_sha256': measurement.sha(BASELINE / 'report.json'),
        'total_cost_usd': report['total_cost_usd'], 'website_claims_available': states.get('website', {}).get('available', 0),
        'baseline_website_claims_available': old_states.get('website', {}).get('available', 0),
        'exact_id_sources': {family: {'states': states.get(family, {}), 'published_claims': claims[family],
                                      'baseline_states': old_states.get(family, {}), 'baseline_published_claims': old_claims[family]}
                             for family in exact},
        'deadline_companies_by_section': deadlines, 'baseline_deadline_companies_by_section': old_deadlines,
        'pass2': {k: pass2[k] for k in ('started_seconds', 'finished_seconds', 'cutoff_seconds', 'runtime_seconds',
                                        'website_requests', 'websites_gained', 'states') if k in pass2},
        'last_pass2_request_started_seconds': last_pass2,
        'baseline_pass2': {k: prior[k] for k in ('runtime_seconds', 'website_requests', 'websites_gained', 'states')},
        'projected_500': {'cutoff_seconds': cutoff_500, 'finalisation_allowance_seconds': PASS2_FINALISATION_SECONDS,
                          'completion_target_seconds': cutoff_500 + PASS2_FINALISATION_SECONDS,
                          'margin_target_seconds': PASS2_MARGIN_SECONDS},
        'source_health': report.get('official_source_outages', {}).get('health_checks', []),
        'gates': gates, 'artifacts': {name: measurement.sha(work / name)
                                    for name in ('envelopes.jsonl', 'profiles.jsonl', 'report.json')},
    }
    measurement.save(receipts / 'summary.json', summary)
    print(json.dumps({'gates': gates, 'wall_seconds': summary['wall_seconds'], 'largest_profile_bytes': largest}), flush=True)
    return 0 if all(gates.values()) else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--retry', action='store_true', help='Use a separate state directory for an authorised outage retry')
    raise SystemExit(measure(parser.parse_args().retry))
