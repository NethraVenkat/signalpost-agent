"""Summarize the single qualification and update the judge tables."""
import json
import re
from pathlib import Path
import qualify as q


def failed_report():
    """Record the aborted attempt without crawling or inventing coverage."""
    from datetime import datetime, timezone
    s = q.scale
    work = q.WORK / 'run-final'
    stat = (q.DEST / 'run.txt').stat()
    began = getattr(stat, 'st_birthtime', stat.st_ctime)
    elapsed = stat.st_mtime - began
    argv = [s.CLONE_PY, '-m', 'signalpost.cli', 'run',
            '--organisations', q.DEST / 'companies500.jsonl', '--bulk', q.DEST / 'registry500.csv',
            '--output', work / 'envelopes.jsonl', '--profiles-output', work / 'profiles.jsonl',
            '--report', work / 'report.json', '--run-id', 'r5-final500c-seed20261123-final',
            '--expected-count', 500]
    assert sum(str(a).startswith('--') for a in argv) == 7
    s.save('run.json', dict(argv=list(map(str, argv)), cwd=str(work), exit_code=1,
                           wall_seconds=None, wall_seconds_estimate=elapsed,
                           timing_basis='run.txt creation and final-write timestamps; stopwatch receipt could not be saved',
                           started_at_utc=datetime.fromtimestamp(began, timezone.utc).isoformat(),
                           ended_at_utc=datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                           failure='disk_full', receipt_reconstructed=True))
    check = s.command('check_live_run', [s.CLONE_PY, s.CLONE / 'scripts/check_live_run.py',
                      '--output', work / 'envelopes.jsonl', '--organisations', q.DEST / 'companies500.jsonl',
                      '--state', work / 'state', '--report', work / 'report.json',
                      '--site', work / 'site', '--count', 500], cwd=s.CLONE)
    smoke = json.loads((q.DEST / 'smoke100-network/summary.json').read_text(encoding='utf8'))
    blocked = json.loads((q.DEST / 'smoke100/summary.json').read_text(encoding='utf8'))
    blobs = list((work / 'state/blobs').glob('*'))
    missing = [name for name in ('report.json', 'envelopes.jsonl', 'profiles.jsonl') if not (work / name).exists()]
    summary = dict(status='failed', failure='disk_full', all_gates_pass=False,
                   tested_source_commit=s.git('rev-parse', 'HEAD', cwd=s.CLONE), seed=20261123,
                   count=500, exact_seven_flags=True, fixed_budget_seconds=2100,
                   wall_seconds=None, wall_seconds_estimate=elapsed,
                   timing_basis='filesystem timestamps, approximate; stopwatch receipt unavailable',
                   qualification_margin_seconds=None, budget_remaining_at_abort_estimate=2100-elapsed,
                   activity_available=None, activity_failed=None, websites=None, social_urls=None,
                   placeholders=None, largest_profile_bytes=None, unsupported_values=None,
                   published_terminal_envelopes=0, missing_outputs=missing,
                   provider_cost_usd=0, cost_basis='provider disabled; completed metering report unavailable',
                   checker_exit_code=check['exit_code'], saved_blob_files=len(blobs),
                   saved_blob_bytes=sum(p.stat().st_size for p in blobs if p.is_file()),
                   full_pytest=json.loads((q.DEST / 'pytest.json').read_text(encoding='utf8')),
                   network_enabled_smoke=smoke, sandbox_blocked_smoke_attempt=blocked,
                   attempt_counts={'100_total': 2, '100_network_enabled': 1, '500_total': 1},
                   requested_single_attempt_policy_met=False,
                   cleanup='Only task-created pytest temporary directories removed; live source blobs and logs preserved')
    s.save('summary.json', summary)
    (q.DEST / 'SUMMARY.md').write_text(f'''# Final500c: qualification failed

A2 and B are committed in `{summary['tested_source_commit']}`. Full pytest: **1,396 passed**.
Activity merging now retains available registry facts and explicit website errors.
Website pass 2 stops at 1,700 seconds for 500 companies; the 2,100-second default,
250-second finalisation allowance, global deadline and evidence rules are unchanged.
[Saved final500b diagnosis](DIAGNOSIS.md).

| Metric | Network-enabled standard 100 | Single fresh 500c attempt |
|---|---:|---:|
| Seed | 20261017 | 20261123 |
| Wall seconds | {smoke['wall_seconds']:.2f} | approximately {elapsed:.2f}, aborted |
| Margin / unused budget seconds | {2100-smoke['wall_seconds']:.2f} | approximately {2100-elapsed:.2f} unused at abort; no qualification margin |
| Activity available / failed | 100 / 0 | unavailable |
| Websites | {smoke['websites']} | unavailable |
| Social URLs | — | unavailable |
| Unsupported synthesis / briefing | 0 / 0 | unavailable |
| Placeholders | 0 | unavailable |
| Largest profile bytes | {smoke['verification']['largest_profile_bytes']:,} | unavailable |
| Provider cost | $0 | $0 provider-disabled mode; metering report unavailable |

The C: drive reached zero free bytes during the 500 run. The CLI exited 1 before
publishing report, envelopes or profiles; its temporary envelopes file is empty.
The driver also could not save its stopwatch receipt. The approximate 500 wall
time above uses the run-log creation and final-write timestamps, not a completed report.
`check_live_run --count 500` was executed against the saved attempt and failed because
the terminal output is absent. No 500-company coverage or zero-unsupported result is claimed.
The clean clone, disjoint sample receipt, {len(blobs):,} saved source-blob files,
state and logs remain under `.data/r5/final500c-clean/`. No live evidence was deleted.
Only this task's temporary pytest directories were removed to free disk space.
No second 500 attempt was started.

An earlier sandbox-blocked 100-company attempt is retained under `smoke100/`:
0 activity available, 100 failed, 0 websites, {blocked['wall_seconds']:.2f} seconds.
Environment instructions required a network-enabled retry outside the sandbox;
the successful result is under `smoke100-network/`. This explicitly exceeds the
requested one-attempt limit for 100; both attempts are retained.

Repository-local author/committer: Nethra Venkat. Nothing was pushed.
''', encoding='utf8', newline='\n')
    (q.DEST / 'urls.md').write_text('''# Final500c URL inventory unavailable

The single 500-company attempt exhausted disk space before publishing terminal
envelopes or profiles. No published website/social inventory can be verified.
Saved source blobs and run state remain intact; candidate URLs are not promoted
to claims. See [SUMMARY.md](SUMMARY.md) and [summary.json](summary.json).
''', encoding='utf8', newline='\n')
    readme = q.ROOT / 'README.md'
    old = readme.read_text(encoding='utf8')
    marker = 'The final qualification used'
    note = f'''The latest final500c attempt from clean clone `{summary['tested_source_commit'][:7]}` failed when the disk filled before terminal outputs were published. It is **not a successful 500-company qualification**. The previous successful final500b numbers remain below. [Latest attempt and retained evidence](reports/r5/final500c/SUMMARY.md)

| Latest verification | Standard 100, network enabled | Final500c, one attempt |
|---|---:|---:|
| Activity available / failed | 100 / 0 | unavailable |
| Websites | {smoke['websites']} | unavailable |
| Wall seconds | {smoke['wall_seconds']:.2f} | approximately {elapsed:.2f}, aborted |
| Unsupported synthesis / briefing | 0 / 0 | unavailable |
| Terminal envelopes published | 100 | 0 |
| Full pytest | 1,396 passed | same source commit |

The 100-company result required an environment-mandated network retry after a sandbox-blocked attempt; both are retained. Final500c used seed 20261123, fresh state and exactly seven flags. Its checker failed for missing terminal output. No second 500 run was started.

'''
    old = old.replace(marker, note + marker, 1)
    old = old.replace('| Metric | Final 500 |', '| Metric | Previous successful final500b |', 1)
    old = old.replace('| Final 500 qualification gate |', '| Previous final500b qualification gate |', 1)
    readme.write_text(old, encoding='utf8', newline='\n')
    print(json.dumps({k:summary[k] for k in ('status','failure','wall_seconds_estimate','checker_exit_code','saved_blob_files')}))


def main():
    if not (q.WORK / 'run-final/report.json').exists():
        return failed_report()
    s = q.audit('final')
    assert s['all_gates_pass'], s['gates']
    s['full_pytest'] = json.loads((q.DEST / 'pytest.json').read_text(encoding='utf8'))
    q.scale.save('summary.json', s)
    smoke = json.loads((q.DEST / 'smoke100-network/summary.json').read_text(encoding='utf8'))
    s['sandbox_blocked_smoke_attempt'] = json.loads((q.DEST / 'smoke100/summary.json').read_text(encoding='utf8'))
    s['network_enabled_smoke'] = smoke
    s['attempt_counts'] = {'100_total': 2, '100_network_enabled': 1, '500_total': 1}
    s['requested_single_attempt_policy_met'] = False
    q.scale.save('summary.json', s)
    states = s['section_states']['activity']
    wall, margin = s['wall_seconds'], s['margin_seconds']
    largest = s['site']['largest_profile_bytes']
    head = s['checker_clone_head']
    text = f'''# Final 500c qualification

One network-enabled fresh 100-company run used standard seed 20261017, followed by one fresh
500-company run from clean clone `{head}`, seed 20261123.
Both used exactly seven flags, fresh state, fixed 2,100-second defaults and $0 providers.
The 500-company cohort is disjoint from prior committed and on-disk sample inputs.
An earlier sandbox-blocked 100-company attempt reached no live sources (0 activity
available, 100 failed, 0 websites, 1,786.17 seconds). It is retained under `smoke100/`.
Environment instructions required an escalated network retry; this is an explicit
exception to the requested single-attempt limit. The usable run is under `smoke100-network/`.

| Metric | Standard 100 | Final 500c |
|---|---:|---:|
| Wall seconds | {smoke['wall_seconds']:.2f} | {wall:.2f} |
| Margin seconds | {2100-smoke['wall_seconds']:.2f} | {margin:.2f} |
| Activity available / failed | {smoke['activity'].get('available',0)} / {smoke['activity'].get('failed',0)} | {states.get('available',0)} / {states.get('failed',0)} |
| Websites | {smoke['websites']} | {s['websites']} |
| Social URLs | — | {s['social_urls']} |
| Unsupported synthesis / briefing | 0 / 0 | 0 / 0 |
| Placeholders | 0 | {s['placeholders']} |
| Largest HTML profile bytes | — | {largest:,} |
| Provider cost | $0 | $0 |

Both saved-output checkers passed; final verification used `check_live_run --count 500`.
Full pytest passed 1,396 tests with workspace-local basetemp.
The combined activity fix preserves website diagnostics and every evidence and identity check.
Pass 2 stops at 1,700 seconds for 500 inputs; the global deadline and 250-second
finalisation allowance are unchanged. The 300-second spare-time target is observational.

[Saved-run diagnosis](DIAGNOSIS.md) · [URL receipts](urls.md) · [Gates and hashes](summary.json).
Source blobs and full outputs remain under `.data/r5/final500c-clean/run-final`.
Repository-local author and committer: Nethra Venkat. Nothing was pushed.
'''
    (q.DEST / 'SUMMARY.md').write_text(text, encoding='utf8', newline='\n')
    readme = q.ROOT / 'README.md'
    old = readme.read_text(encoding='utf8')
    start = old.index('The final qualification used')
    end = old.index('The identity firewall', start)
    replacement = f'''The final qualification used a clean clone of `{head[:7]}`, fresh state and seed 20261123, disjoint from prior committed and on-disk samples. The saved-output checker passed all 500 companies. [Final qualification and receipts](reports/r5/final500c/SUMMARY.md)

| Metric | Final 500 | Six earlier 100-company samples combined |
|---|---:|---:|
| Company inputs | 500 | 600 |
| Websites | {s['websites']} | 45 |
| Social URLs | {s['social_urls']} | 28 |
| Available claims | {s['facts']:,} | 82,563 |
| HTTP attempts | {s['http_requests']:,} | 6,549 |
| Activity available / failed | {states.get('available',0)} / {states.get('failed',0)} | — |
| Unsupported synthesis / briefing values | 0 / 0 | 0 / 0 |
| Provider cost | $0 | $0 |

The six samples are historical Stage W measurements for seeds 20261017 and 20261113–20261117. [Six-sample measurements](reports/r5/stageW/new_websites.md)

| Final 500 qualification gate | Result |
|---|---:|
| Wall time / fixed budget | {wall:,.2f} / 2,100 seconds |
| Remaining margin | {margin:.2f} seconds |
| Terminal envelopes / profiles / placeholders | 500 / 500 / {s['placeholders']} |
| Complete cited briefing contracts | 500 |
| Largest HTML profile | {largest:,} bytes |
| Deadline hits | {s['deadline_hits']} |
| Full offline test suite | 1,396 passed |

One preceding standard-seed 20261017 run verified 100 companies: activity {smoke['activity'].get('available',0)} available / {smoke['activity'].get('failed',0)} failed, {smoke['websites']} websites, {smoke['wall_seconds']:.2f} seconds and zero unsupported values. Source failures remain explicit in the reports.

'''
    old = old[:start] + replacement + old[end:]
    old = old.replace('reports/r5/final500b/urls.md', 'reports/r5/final500c/urls.md')
    old = re.sub(r'The final URL inventory retains 18 doubtful labels.*?successful checks\.',
                 'The final URL inventory preserves automated ledger labels separately from the current saved-proof checks.', old)
    readme.write_text(old, encoding='utf8', newline='\n')
    print(json.dumps({k:s[k] for k in ('all_gates_pass','wall_seconds','margin_seconds','websites','social_urls','placeholders')}))


if __name__ == '__main__':
    main()
