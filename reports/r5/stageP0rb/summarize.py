"""Summarize the P0 re-baseline on new machine (six samples, no comparison)."""
from signalpost.portable_paths import portable_text  # saved paths stay repo-relative
import json
from pathlib import Path

DEST = Path(__file__).resolve().parent
SEEDS = (20261017, 20261113, 20261114, 20261115, 20261116, 20261117)
METRICS = ('websites', 'declared_homepage_recall', 'declared_homepages', 'social_companies', 'social_claims',
           'activity_companies', 'activity_claims', 'brand_companies', 'brand_claims', 'role_change_claims', 'facts')


def load(path):
    return json.loads(path.read_text(encoding='utf8'))


def main():
    rows = []
    for seed in SEEDS:
        d = DEST / f'seed{seed}'
        c, v, r, s, e = (load(d / n) for n in ('counts.json', 'verification.json', 'report.json', 'settings.json', 'execution.json'))
        outages = r.get('official_source_outages') or {}
        health = {h['source']: h['state'] for h in outages.get('health_checks', [])}
        gates = {
            'exit_0': e['exit_code'] == 0, 'seven_flags': s['exact_seven_flags'],
            'terminal_100': v['terminal_envelopes'] == 100 and v['lines'] == 100, 'schema_valid': v['schema_valid'],
            'unsupported_0': v['synthesis_unverified_values'] == 0 and v['briefing_unverified_values'] == 0,
            'five_topics_100': all(n == 100 for n in v['briefing_topic_coverage'].values()) and v['complete_briefing_contracts'] == 100,
            'site_available_lt_250000': c['site']['state'] == 'available' and c['site']['largest_profile_bytes'] < 250000,
            'http_le_1850': c['HTTP'] <= r['limits']['scaled_hard_request_cap'] == 1850,
            'time_le_2100': e['wall_seconds'] <= r['limits']['scaled_hard_time_seconds'] == 2100.0,
            'cost_0': c['cost_usd'] == 0 and v['cost_usd'] == 0}
        rows.append({'seed': seed, **{m: c['counts'][m] for m in METRICS}, 'HTTP': c['HTTP'],
                     'process_seconds': round(e['wall_seconds'], 3), 'largest_profile_bytes': c['site']['largest_profile_bytes'],
                     'cost_usd': c['cost_usd'], 'health': health, 'gates': gates,
                     'envelopes_sha256': c['envelopes_sha256'], 'parent_commit': s['parent_commit']})
    assert len({r['parent_commit'] for r in rows}) == 1
    totals = {m: sum(r[m] for r in rows) for m in METRICS + ('HTTP',)}
    totals['process_seconds'] = round(sum(r['process_seconds'] for r in rows), 3)
    totals['cost_usd'] = sum(r['cost_usd'] for r in rows)
    all_pass = all(all(r['gates'].values()) for r in rows)
    out = {'label': 'P0 re-baseline on new machine', 'comparison': 'none; earlier run folders were not transferred',
           'parent_commit': rows[0]['parent_commit'], 'samples': rows, 'totals': totals, 'all_gates_pass': all_pass}
    (DEST / 'totals.json').write_text(portable_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n'), encoding='utf8', newline='\n')
    head = '| Seed | Sites | Declared recall | Social cos/claims | Activity claims | Brands | Facts | HTTP | Process s | Largest page | Gates |'
    lines = [head, '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|']
    for r in rows:
        lines.append(f"| {r['seed']} | {r['websites']} | {r['declared_homepage_recall']}/{r['declared_homepages']} | "
                     f"{r['social_companies']}/{r['social_claims']} | {r['activity_claims']:,} | {r['brand_claims']} | {r['facts']:,} | "
                     f"{r['HTTP']} | {r['process_seconds']:.1f} | {r['largest_profile_bytes']:,} | {'pass' if all(r['gates'].values()) else 'FAIL'} |")
    t = totals
    lines.append(f"| **Total** | {t['websites']} | {t['declared_homepage_recall']}/{t['declared_homepages']} | "
                 f"{t['social_companies']}/{t['social_claims']} | {t['activity_claims']:,} | {t['brand_claims']} | {t['facts']:,} | "
                 f"{t['HTTP']:,} | {t['process_seconds']:.1f} | — | {'all pass' if all_pass else 'FAIL'} |")
    print('\n'.join(lines))
    print(json.dumps({'all_gates_pass': all_pass, 'cost_usd': totals['cost_usd'],
                      'health_not_reachable': {r['seed']: {k: v for k, v in r['health'].items() if v != 'reachable'} for r in rows}}))


if __name__ == '__main__':
    main()
