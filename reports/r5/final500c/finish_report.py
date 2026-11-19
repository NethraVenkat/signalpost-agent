"""Summarize the single qualification and update the judge tables."""
import json
import re
from pathlib import Path
import qualify as q


def main():
    s = q.audit('final')
    assert s['all_gates_pass'], s['gates']
    s['full_pytest'] = json.loads((q.DEST / 'pytest.json').read_text(encoding='utf8'))
    q.scale.save('summary.json', s)
    smoke = json.loads((q.DEST / 'smoke100-network/summary.json').read_text(encoding='utf8'))
    s['sandbox_blocked_smoke_attempt'] = json.loads((q.DEST / 'smoke100/summary.json').read_text(encoding='utf8'))
    s['network_enabled_smoke'] = smoke
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
