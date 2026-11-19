"""One authorized guarded rerun: same sample, fresh clone/state, no clone pytest."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import sys

import qualify as q

HEAD = '2ac8a6b0efa1a80c8afdd37323253e786a85e6ff'
BASE = q.ROOT / '.data/r5/final500c-rerun-clean'
s = q.scale
q.WORK = BASE
s.CLONE = BASE / 'repo'
s.CLONE_PY = s.CLONE / '.venv/Scripts/python.exe'
s.work_dir = lambda label: BASE / ('run-' + label)
ARCHIVE = q.DEST / 'trials/disk-full'


def footprint(path):
    files = [p for p in path.rglob('*') if p.is_file()] if path.exists() else []
    return dict(files=len(files), bytes=sum(p.stat().st_size for p in files))


def prepare():
    assert s.git('rev-parse', 'HEAD') == HEAD
    assert not s.git('status', '--porcelain', '--', 'src', 'tests', 'scripts', 'pyproject.toml', 'uv.lock')
    assert not BASE.exists(), 'No retry or reused state permitted'
    old = json.loads((q.DEST / 'clean_clone.json').read_text(encoding='utf8'))
    assert s.sha(q.DEST/'companies500.jsonl') == old['sample_sha256']
    assert s.sha(q.DEST/'registry500.csv') == old['subset_sha256']
    assert old['overlap_with_committed_samples'] == 0
    ARCHIVE.mkdir(parents=True, exist_ok=False)
    names = ['SUMMARY.md','summary.json','urls.md','run.json','run.txt','clean_clone.json',
             'clone.json','clone.txt','clone_identity.json','extract.json','extract.txt',
             'source_manifest.json','uv-sync.json','uv-sync.txt','check_live_run.json',
             'check_live_run.txt','privacy.json','privacy.txt']
    for name in names:
        source = q.DEST/name
        if source.exists():
            shutil.copy2(source, ARCHIVE/name)
    s.save('disk_preflight.json', dict(
        measured_at_utc=datetime.now(timezone.utc).isoformat(), free_bytes=shutil.disk_usage(q.ROOT).free,
        failed_run=footprint(q.ROOT/'.data/r5/final500c-clean/run-final'),
        blocked_100=footprint(q.ROOT/'.data/r5/final500c-smoke100'),
        successful_100=footprint(q.ROOT/'.data/r5/final500c-smoke100-network'),
        uv_cache=footprint(q.ROOT/'.data/r5/final500c-uv-cache'),
        historical_limitation='No per-directory historical allocation series. Prior pytest-temp cleanup recovered about 10.3 GB; deleted clone sizes cannot be measured.',
        pytest_in_clone=False, abort_below_free_bytes=3*1024**3))
    assert shutil.disk_usage(q.ROOT).free > 3*1024**3
    BASE.mkdir()
    clone = s.command('clone', ['git','clone','--no-local','--depth','1','--single-branch',
                              '--branch','revision/r5',q.ROOT,s.CLONE])
    assert clone['exit_code'] == 0
    assert s.git('rev-parse','HEAD',cwd=s.CLONE) == HEAD
    s.git('config','--local','user.name','Nethra Venkat',cwd=s.CLONE)
    s.git('config','--local','user.email','nethravenkat510@gmail.com',cwd=s.CLONE)
    sync = s.command('uv-sync',['uv','sync','--frozen'],cwd=s.CLONE)
    assert sync['exit_code'] == 0
    probe = s.command('import-check',[s.CLONE_PY,'-c',
        'import json,sys,signalpost;print(json.dumps(dict(module=signalpost.__file__,prefix=sys.prefix,executable=sys.executable)))'],cwd=s.CLONE)
    assert probe['exit_code'] == 0
    installation = json.loads((q.DEST/'import-check.txt').read_text(encoding='utf8'))
    from signalpost.portable_paths import expand
    assert Path(expand(installation['module'])).resolve().is_relative_to((s.CLONE/'src').resolve())
    assert Path(expand(installation['prefix'])).resolve() == (s.CLONE/'.venv').resolve()
    assert s.git('status','--porcelain',cwd=s.CLONE) == ''
    identical = {p:s.sha(q.ROOT/p)==s.sha(s.CLONE/p) for p in
                 ('scripts/check_live_run.py','scripts/verify_output.py','scripts/precision_ledger.py','uv.lock')}
    assert all(identical.values())
    receipt = dict(old)
    receipt.update(tested_source_commit=HEAD, clone_head=HEAD, clone_directory=str(s.CLONE),
                   clone_status_clean=True, installation=installation, pytest_in_clone=False,
                   same_frozen_sample_as_disk_full_attempt=True,
                   clone_command='git clone --no-local --depth 1 --single-branch --branch revision/r5',
                   tools_identical_to_main_checkout=identical,
                   prepared_at_utc=datetime.now(timezone.utc).isoformat(),
                   disk_free_after_setup_bytes=shutil.disk_usage(q.ROOT).free,
                   setup_footprint=footprint(s.CLONE))
    s.save('clean_clone.json',receipt)
    s.save('clone_identity.json',dict(author=s.git('var','GIT_AUTHOR_IDENT',cwd=s.CLONE),
                                    committer=s.git('var','GIT_COMMITTER_IDENT',cwd=s.CLONE),
                                    local_name=s.git('config','--local','user.name',cwd=s.CLONE),
                                    local_email=s.git('config','--local','user.email',cwd=s.CLONE)))
    s.save('source_manifest.json',{p.relative_to(s.CLONE).as_posix():s.sha(p)
                                  for p in sorted((s.CLONE/'src').rglob('*'))
                                  if p.is_file() and '__pycache__' not in p.parts})
    print(json.dumps(dict(head=HEAD, free_bytes=receipt['disk_free_after_setup_bytes'],
                          setup=receipt['setup_footprint'], pytest_in_clone=False,
                          same_sample=True, excluded_numbers=old['excluded_unique_numbers'])))


def run():
    assert s.git('rev-parse','HEAD',cwd=s.CLONE) == HEAD
    assert s.git('status','--porcelain',cwd=s.CLONE) == ''
    meta=json.loads((q.DEST/'clean_clone.json').read_text(encoding='utf8'))
    assert s.sha(q.DEST/'companies500.jsonl')==meta['sample_sha256']
    assert s.sha(q.DEST/'registry500.csv')==meta['subset_sha256']
    work=s.work_dir('final')
    work.mkdir(exist_ok=False)
    argv=[s.CLONE_PY,q.DEST/'disk_guard_cli.py','run',
          '--organisations',q.DEST/'companies500.jsonl','--bulk',q.DEST/'registry500.csv',
          '--output',work/'envelopes.jsonl','--profiles-output',work/'profiles.jsonl',
          '--report',work/'report.json','--run-id','r5-final500c-seed20261123-authorized-rerun',
          '--expected-count',500]
    assert sum(str(a).startswith('--') for a in argv)==7
    env=dict(s.ENV,FINAL500C_GUARD_ROOT=str(q.ROOT),
             FINAL500C_GUARD_RECEIPT=str(q.DEST/'disk_guard.json'))
    print('Starting the single authorized 500-company rerun with 3 GiB disk guard.',flush=True)
    result=s.command('run',argv,cwd=work,env=env)
    guard=json.loads((q.DEST/'disk_guard.json').read_text(encoding='utf8'))
    if guard['stopped_for_low_space'] or result['exit_code']:
        s.save('summary.json',dict(status='stopped' if guard['stopped_for_low_space'] else 'failed',
                                  disk_guard=guard, execution=result, all_gates_pass=False,
                                  automatic_retry=False))
        raise SystemExit('Run stopped; artifacts preserved; no retry will occur.')
    s.evaluate('final','check_live_run')
    summary=q.audit('final')
    assert summary['all_gates_pass'],summary['gates']
    summary.update(status='passed', disk_guard=guard, full_pytest=json.loads((q.DEST/'pytest.json').read_text()),
                   pytest_in_clone=False, previous_disk_full_attempt='trials/disk-full/summary.json',
                   authorized_500_reruns_this_request=1, total_500_attempts=2,
                   cohort_reused_from_disk_full_attempt=True)
    s.save('summary.json',summary)
    finish(summary)


def finish(m):
    a=m['section_states']['activity']
    wall=m['wall_seconds']; margin=2100-wall; head=m['checker_clone_head']
    g=m['disk_guard']
    text=f'''# Final500c: successful authorized rerun

One fresh 500-company rerun used a clean shallow clone of `{head}`, exactly seven
evaluator flags, seed 20261123 and the identical frozen, disjoint sample from the
disk-full attempt. State was fresh. Clone setup ran only `uv sync --frozen` and an
import check; no clone pytest. The 1,396 passing main-checkout tests were carried forward.

| Metric | Final500c |
|---|---:|
| Wall time / fixed budget | {wall:.2f} / 2,100 seconds |
| Margin | {margin:.2f} seconds |
| Activity available / failed | {a.get('available',0)} / {a.get('failed',0)} |
| Websites / social URLs | {m['websites']} / {m['social_urls']} |
| Terminal envelopes / profiles / placeholders | 500 / 500 / {m['placeholders']} |
| Largest HTML profile | {m['site']['largest_profile_bytes']:,} bytes |
| Unsupported synthesis / briefing | 0 / 0 |
| HTTP requests | {m['http_requests']:,} |
| Provider cost | $0 |
| Minimum sampled free space | {g['minimum_free_bytes']/1024**3:.2f} GiB |

`check_live_run --count 500` passed. The guard sampled disk free space every two
seconds and would request SIGINT/asyncio cleanup below 3 GiB; it did not trigger.
The 2,100-second default, 1,700-second pass-2 cutoff, finalisation reserve,
exact-ID identity rules and evidence requirements were unchanged.
Full outputs and source blobs remain in `.data/r5/final500c-rerun-clean/run-final`.

## Retained earlier attempts

The original disk-full 500 attempt aborted at approximately 1,374.39 seconds,
before publishing terminal outputs. Its receipts are preserved under
[`trials/disk-full/`](trials/disk-full/SUMMARY.md); all original run state and
source blobs remain under `.data/r5/final500c-clean/run-final`.
Its retained state is only 70.08 MB. No historical per-directory disk series
exists; prior pytest-temp cleanup recovered about 10.3 GB. Deleted clone sizes
cannot now be reconstructed. See `disk_preflight.json` and `disk_guard.json`.

The earlier network-enabled standard 100 check remains 100 activity available /
0 failed, 8 websites, 351.63 seconds, zero unsupported values and $0. Its earlier
sandbox-blocked attempt and the environment-required network retry remain recorded.

[Activity diagnosis](DIAGNOSIS.md) · [URL inventory](urls.md) · [Gates and hashes](summary.json).
Repository-local author and committer: Nethra Venkat. Nothing was pushed.
'''
    (q.DEST/'SUMMARY.md').write_text(text,encoding='utf8',newline='\n')
    readme=q.ROOT/'README.md'; old=readme.read_text(encoding='utf8')
    start=old.index('The latest final500c attempt'); end=old.index('The identity firewall',start)
    replacement=f'''The successful final500c rerun used a clean clone of `{head[:7]}`, fresh state, seed 20261123 and the same frozen sample disjoint from 5,206 prior numbers. The saved-output checker passed all 500 companies. Clone setup ran `uv sync --frozen` and an import check; no clone pytest. [Final qualification and receipts](reports/r5/final500c/SUMMARY.md)

| Metric | Final500c | Six earlier 100-company samples combined |
|---|---:|---:|
| Company inputs | 500 | 600 |
| Websites | {m['websites']} | 45 |
| Social URLs | {m['social_urls']} | 28 |
| Activity available / failed | {a.get('available',0)} / {a.get('failed',0)} | — |
| Available claims | {m['facts']:,} | 82,563 |
| HTTP attempts | {m['http_requests']:,} | 6,549 |
| Unsupported synthesis / briefing | 0 / 0 | 0 / 0 |
| Provider cost | $0 | $0 |

| Final500c qualification gate | Result |
|---|---:|
| Wall time / fixed budget | {wall:,.2f} / 2,100 seconds |
| Remaining margin | {margin:.2f} seconds |
| Terminal envelopes / profiles / placeholders | 500 / 500 / {m['placeholders']} |
| Complete cited briefing contracts | 500 |
| Largest HTML profile | {m['site']['largest_profile_bytes']:,} bytes |
| Minimum sampled free disk space | {g['minimum_free_bytes']/1024**3:.2f} GiB |
| Existing main-checkout full pytest | 1,396 passed |

The original disk-full attempt and its evidence are retained in the [failure archive](reports/r5/final500c/trials/disk-full/SUMMARY.md). This one rerun was explicitly authorized after disk cleanup. A 3 GiB free-space guard remained active throughout. The earlier standard-seed 100 check returned 100 activity available / 0 failed, 8 websites and zero unsupported values in 351.63 seconds; its sandbox-blocked preliminary attempt is retained. The six historical samples remain separate from this qualification. [Six-sample measurements](reports/r5/stageW/new_websites.md)

'''
    old=old[:start]+replacement+old[end:]
    old=old.replace('reports/r5/final500b/urls.md','reports/r5/final500c/urls.md')
    old=old.replace('The final URL inventory retains 18 doubtful labels from the older ledger tool separately from the current validator\'s successful checks.',
                    'The final URL inventory retains automated ledger labels separately from the current saved-proof checks.')
    readme.write_text(old,encoding='utf8',newline='\n')
    print(json.dumps(dict(wall_seconds=wall,margin_seconds=margin,activity=a,
                          websites=m['websites'],social_urls=m['social_urls'],
                          placeholders=m['placeholders'],largest_profile_bytes=m['site']['largest_profile_bytes'],
                          minimum_free_bytes=g['minimum_free_bytes'],all_gates_pass=m['all_gates_pass'])))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase',choices=['prepare','run'])
    args=parser.parse_args()
    prepare() if args.phase=='prepare' else run()
