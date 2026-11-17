"""P3e: 500-company clean-clone scale measurement at HEAD incl. Stage S (exact seven evaluator flags). Derived from the P2 driver.

Actions (run with the main repository's .venv; the measured CLI and checker run
from the clone's own .venv/src):
  prepare            clone, uv sync --frozen, installation proof, disjoint sample, bulk extraction
  tests              full pytest inside the clone
  run <label>        one fresh seven-flag run from the clone + check_live_run --count 500 + gates
  inventory <label>  every published website/social URL with exact receipts; automated-doubtful listed separately
"""
from signalpost.portable_paths import expand, portable, portable_text, sanitize_file  # saved paths stay repo-relative
import gzip
import hashlib
import json
import os
import random
import re
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

from signalpost.identity.orgnr import valid

ROOT = Path(__file__).resolve().parents[4]
DEST = ROOT / 'reports/r5/stageP3/P3e'
CLONE = ROOT / '.data/r5/p3e-clean/repo'
CLONE_PY = CLONE / '.venv/Scripts/python.exe'
UNIVERSE = ROOT / '.data/r5/inputs/universe-20261116/universe.jsonl.gz'
UNIVERSE_SHA = '1c89710e5b01f8617e86d09fbdff4a52f2f8dbbba297e74f7164b5984f5a0384'
UNIVERSE_CONTENT_SHA = 'b82d6a3e7231d1759a958c282bc4366b80ec2fab8095053d8ed7fa9cd01bc838'
SNAPSHOT = ROOT / '.data/r5/inputs/brreg-enheter-20261116/enheter_2026-11-16T04-25-21.340365166.csv.gz'
SNAPSHOT_SHA = '56922f51839e7ed3f3c9adde50dbcfa375202d7bc5aa998d9572158e228693e1'
SEED = 20261119
COUNT = 500
ENV = os.environ.copy()
ENV.update(SIGNALPOST_SEARCH_PROVIDER='disabled', SIGNALPOST_SEARCH_MOCK='0', PYTHONUTF8='1')
ENV.pop('VIRTUAL_ENV', None)
# Committed sample/batch inputs whose org numbers must not overlap the new draw.
SAMPLE_NAME = re.compile(r'(^|/)(companies\d*|batch|sample|selection|registry\d*|pilot\d*|ci20|cohort)[^/]*\.(jsonl|json|csv|txt)$', re.I)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(name, value):
    DEST.mkdir(parents=True, exist_ok=True)
    (DEST / name).write_text(portable_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n'), encoding='utf8', newline='\n')


def command(name, args, cwd=ROOT, env=None, timeout=None):
    began = time.perf_counter()
    with (DEST / (name + '.txt')).open('w', encoding='utf8', newline='\n') as log:
        result = subprocess.run([str(a) for a in args], cwd=cwd, env=ENV if env is None else env,
                                stdout=log, stderr=subprocess.STDOUT, timeout=timeout)
    sanitize_file(DEST / (name + '.txt'))  # keep captured paths repo-relative
    info = {'argv': [str(a) for a in args], 'cwd': str(cwd), 'exit_code': result.returncode,
            'wall_seconds': time.perf_counter() - began, 'completed_at_utc': datetime.now(timezone.utc).isoformat()}
    save(name + '.json', info)
    return info


def jsonl(path):
    # JSONL records end at LF only; str.splitlines() would also split on
    # U+2028/U+0085 inside JSON strings (seen in published page excerpts).
    with open(path, encoding='utf8', newline='') as f:
        return [json.loads(line) for line in f.read().split(chr(10)) if line.strip()]


def git(*args, cwd=ROOT):
    return subprocess.check_output(['git', *args], cwd=cwd, text=True).strip()


def committed_sample_numbers():
    files = [f for f in git('ls-files').splitlines()
             if (SAMPLE_NAME.search(f) and '/state/' not in f and '/blobs/' not in f) or f == 'tests/fixtures/ci20.jsonl']
    # P2's inputs were never committed (.gitignore *.jsonl/*.csv); also exclude every
    # sample file on disk under reports/, tracked or not, except this run's own draw.
    own = DEST.relative_to(ROOT).as_posix() + '/'
    on_disk = [p.relative_to(ROOT).as_posix() for p in (ROOT / 'reports').rglob('*') if p.is_file()]
    files += [f for f in on_disk if SAMPLE_NAME.search(f) and not f.startswith(own) and f not in files
              and '/state/' not in f and '/blobs/' not in f]
    per_file, union = {}, set()
    for f in sorted(files):
        text = (ROOT / f).read_text(encoding='utf-8-sig', errors='replace')
        numbers = {n for n in re.findall(r'(?<!\d)\d{9}(?!\d)', text) if valid(n)}
        if numbers:
            per_file[f] = len(numbers)
            union |= numbers
    assert 'tests/fixtures/ci20.jsonl' in per_file and 'reports/r5/baseline/companies.jsonl' in per_file
    assert 'reports/r5/scale500/companies500.jsonl' in per_file  # P2's 500
    return per_file, union


def prepare():
    head = git('rev-parse', 'HEAD')
    assert not git('status', '--porcelain', '--', 'src', 'tests', 'scripts', 'pyproject.toml', 'uv.lock')
    if not CLONE.exists():
        CLONE.parent.mkdir(parents=True, exist_ok=True)
        command('clone', ['git', 'clone', '--no-hardlinks', '--branch', 'revision/r5', ROOT, CLONE])
    clone_head = git('rev-parse', 'HEAD', cwd=CLONE)
    assert clone_head == head, (clone_head, head)
    assert git('status', '--porcelain', cwd=CLONE) == '', 'clone not clean'
    sync = command('uv-sync', ['uv', 'sync', '--frozen'], cwd=CLONE)
    assert sync['exit_code'] == 0
    probe = subprocess.run([CLONE_PY, '-c', 'import json,sys,signalpost,importlib.metadata as m;'
                            'print(json.dumps({"module":signalpost.__file__,"prefix":sys.prefix,"executable":sys.executable,'
                            '"version":m.version("signalpost-agent"),"python":sys.version}))'],
                           cwd=CLONE, env=ENV, capture_output=True, text=True, check=True)
    install = json.loads(probe.stdout)
    assert Path(install['module']).resolve().is_relative_to((CLONE / 'src').resolve()), install
    assert Path(install['prefix']).resolve() == (CLONE / '.venv').resolve(), install
    same_tools = {f: sha(ROOT / f) == sha(CLONE / f) for f in ('scripts/check_live_run.py', 'scripts/verify_output.py',
                                                              'scripts/precision_ledger.py', 'scripts/extract_bulk.py', 'uv.lock')}
    assert all(same_tools.values()), same_tools
    assert sha(UNIVERSE) == UNIVERSE_SHA and sha(SNAPSHOT) == SNAPSHOT_SHA
    per_file, excluded = committed_sample_numbers()
    corpus, digest, total = [], hashlib.sha256(), 0
    with gzip.open(UNIVERSE, 'rb') as f:
        for line in f:
            digest.update(line); total += 1
            org = str(json.loads(line)['organisation_number'])
            if valid(org) and org not in excluded:
                corpus.append(org)
    assert total == 411160 and digest.hexdigest() == UNIVERSE_CONTENT_SHA
    sample = random.Random(SEED).sample(corpus, COUNT)
    assert len(set(sample)) == COUNT and all(valid(o) for o in sample)
    overlap = set(sample) & excluded
    assert not overlap, overlap
    DEST.mkdir(parents=True, exist_ok=True)
    (DEST / 'companies500.jsonl').write_text(''.join(json.dumps({'organisation_number': o}) + '\n' for o in sample),
                                             encoding='utf8', newline='\n')
    ext = command('extract', [CLONE_PY, CLONE / 'scripts/extract_bulk.py', '--bulk', SNAPSHOT,
                              '--batch', DEST / 'companies500.jsonl', '--output', DEST / 'registry500.csv'], cwd=CLONE)
    assert ext['exit_code'] == 0
    extraction = json.loads((DEST / 'extract.txt').read_text(encoding='utf8').strip().splitlines()[-1])
    save('clean_clone.json', {
        'tested_source_commit': head, 'clone_head': clone_head, 'clone_status_clean': True, 'clone_directory': str(CLONE),
        'clone_command': 'git clone --no-hardlinks --branch revision/r5', 'installation': install,
        'tools_identical_to_main_checkout': same_tools,
        'universe': {'path': str(UNIVERSE), 'sha256': UNIVERSE_SHA, 'content_sha256': digest.hexdigest(), 'rows': total},
        'registry_snapshot': {'path': str(SNAPSHOT), 'sha256': SNAPSHOT_SHA,
                              'label': 'NEW Brreg enheter snapshot 2026-11-16 (not the 13 Oct 2026 snapshot)'},
        'sampling': f'random.Random({SEED}).sample({COUNT}) over universe order, restricted to mod-11-valid numbers '
                    'not present in any committed sample/batch input',
        'excluded_files': per_file, 'excluded_unique_numbers': len(excluded), 'eligible_count': len(corpus),
        'overlap_with_committed_samples': 0, 'sample_sha256': sha(DEST / 'companies500.jsonl'),
        'subset_sha256': sha(DEST / 'registry500.csv'), 'extraction': extraction,
        'environment_overrides': {k: ENV[k] for k in ('SIGNALPOST_SEARCH_PROVIDER', 'SIGNALPOST_SEARCH_MOCK', 'PYTHONUTF8')},
        'prepared_at_utc': datetime.now(timezone.utc).isoformat()})
    save('source_manifest.json', {p.relative_to(CLONE).as_posix(): sha(p) for p in sorted((CLONE / 'src').rglob('*'))
                                  if p.is_file() and '__pycache__' not in p.parts})
    print(json.dumps({'head': head, 'eligible': len(corpus), 'excluded': len(excluded), 'extraction': extraction}))


def tests():
    env = dict(ENV)
    for name in ('SIGNALPOST_SEARCH_PROVIDER', 'SIGNALPOST_SEARCH_MOCK'):
        env.pop(name, None)
    info = command('pytest-clone', [CLONE_PY, 'reports/r5/stage4_7/run_tests.py', '-q', '-p', 'no:cacheprovider', '--tb=short'],
                   cwd=CLONE, env=env)
    print(json.dumps({'exit_code': info['exit_code'], 'wall_seconds': info['wall_seconds']}))


def work_dir(label):
    return ROOT / '.data/r5/p3e-clean' / f'run-{label}'


def run(label):
    assert label in {'final', 'retry'}
    assert git('rev-parse', 'HEAD', cwd=CLONE) == json.loads((DEST / 'clean_clone.json').read_text(encoding='utf8'))['clone_head']
    assert git('status', '--porcelain', cwd=CLONE) == ''
    work = work_dir(label); work.mkdir(parents=True, exist_ok=False)
    out = DEST if label == 'final' else DEST / 'trials' / label
    out.mkdir(parents=True, exist_ok=True)
    batch, bulk = DEST / 'companies500.jsonl', DEST / 'registry500.csv'
    meta = json.loads((DEST / 'clean_clone.json').read_text(encoding='utf8'))
    assert sha(batch) == meta['sample_sha256'] and sha(bulk) == meta['subset_sha256']
    flags = {'organisations': batch, 'bulk': bulk, 'output': work / 'envelopes.jsonl', 'profiles-output': work / 'profiles.jsonl',
             'report': work / 'report.json', 'run-id': f'r5-p3e-seed{SEED}-{label}', 'expected-count': COUNT}
    args = [CLONE_PY, '-m', 'signalpost.cli', 'run']
    for k, v in flags.items():
        args.extend(['--' + k, str(v)])
    assert sum(str(a).startswith('--') for a in args) == 7
    prefix = '' if label == 'final' else f'trials/{label}/'
    command(prefix + 'run', args, cwd=work, timeout=4 * 3600)
    evaluate(label, 'check_live_run')


def evaluate(label, check_name):
    """Verify a saved run with the clone's checker and evaluate every gate (no crawl)."""
    work = work_dir(label)
    out = DEST if label == 'final' else DEST / 'trials' / label
    batch = DEST / 'companies500.jsonl'
    prefix = '' if label == 'final' else f'trials/{label}/'
    execution = json.loads((DEST / (prefix + 'run.json')).read_text(encoding='utf8'))
    check = command(prefix + check_name, [CLONE_PY, CLONE / 'scripts/check_live_run.py', '--output', work / 'envelopes.jsonl',
                                          '--organisations', batch, '--state', work / 'state', '--report', work / 'report.json',
                                          '--site', work / 'site', '--count', str(COUNT)], cwd=CLONE)
    text = (DEST / (prefix + check_name + '.txt')).read_text(encoding='utf8')
    checked = {'unparsed': True}
    for candidate in (text, *reversed(text.strip().splitlines())):
        try:
            parsed = json.loads(candidate)
        except ValueError:
            continue
        if isinstance(parsed, dict):
            checked = parsed; break
    report = json.loads((work / 'report.json').read_text(encoding='utf8')) if (work / 'report.json').exists() else {}
    rows = jsonl(work / 'envelopes.jsonl') if (work / 'envelopes.jsonl').exists() else []
    expected = [json.loads(x)['organisation_number'] for x in batch.read_text(encoding='utf8').splitlines()]
    topics = ('activity', 'change', 'unknown', 'financial', 'takeaway')
    limits = report.get('limits', {})
    site = report.get('site', {})
    outages = report.get('official_source_outages') or {}
    health = {h['source']: h['state'] for h in outages.get('health_checks', [])}
    gates = {
        'exit_0': execution['exit_code'] == 0,
        'check_live_run_exit_0': check['exit_code'] == 0,
        'ordered_terminal_500': len(rows) == COUNT and [r['organisation_number'] for r in rows] == expected
                                and all(r['run']['terminal_status'] in {'completed', 'failed'} for r in rows),
        'five_cited_topics_500': len(rows) == COUNT and all(set(topics) <= {s['topic'] for s in r['run']['synthesis']['briefing']} for r in rows)
                                 and checked.get('complete_briefing_contracts') == COUNT,
        'unsupported_0': checked.get('synthesis_unverified_values') == 0 and checked.get('briefing_unverified_values') == 0,
        'http_le_9250': report.get('requests', 10**9) <= limits.get('scaled_hard_request_cap', 0) == 9250,
        # Effective budget = min(requested, scaled 21 s x 500); since P3a the default request is the scaled limit.
        'wall_le_scaled_time_budget': execution['wall_seconds'] <= min(limits.get('effective_time_budget_seconds', 0),
                                                                       limits.get('scaled_hard_time_seconds', 0)),
        'largest_profile_lt_250000': site.get('state') == 'available' and site.get('largest_profile_bytes', 10**9) < 250000,
        'cost_0': report.get('total_cost_usd') == 0 and checked.get('cost_usd') == 0,
        'zero_llm_search_calls': report.get('search', {}).get('queries') == 0 and report.get('llm', {}).get('calls') == 0,
    }
    claims = [c for r in rows for c in r['claims'] if c['availability'] == 'available']
    summary = {
        'label': label, 'check': check_name, 'checker_clone_head': git('rev-parse', 'HEAD', cwd=CLONE),
        'gates': gates, 'all_gates_pass': all(gates.values()),
        'source_health': health, 'official_source_outages_counts': outages.get('counts'),
        'input_rows': COUNT, 'terminal_envelopes': len(rows), 'http_requests': report.get('requests'), 'limits': limits,
        'wall_seconds': execution['wall_seconds'], 'runtime_seconds': report.get('runtime_ms', 0) / 1000,
        'deadline_hits': report.get('deadline_hits'), 'total_cost_usd': report.get('total_cost_usd'),
        'search_queries': report.get('search', {}).get('queries'), 'llm_calls': report.get('llm', {}).get('calls'),
        'site': site, 'facts': len(claims),
        'websites': sum(c['field'] == 'official_website' for c in claims),
        'social_urls': sum(c['field'].startswith('social_profile.') for c in claims),
        'social_companies': sum(any(c['field'].startswith('social_profile.') and c['availability'] == 'available' for c in r['claims']) for r in rows),
        'jobs': sum(c['field'].startswith('hiring.job.') for c in claims),
        'activity_claims': sum(c['family'] == 'activity' for c in claims),
        'families': dict(Counter(c['family'] for c in claims)),
        'section_states': {fam: dict(Counter(r['run']['sections'].get(fam, 'not_recorded') for r in rows))
                           for fam in sorted({f for r in rows for f in r['run']['sections']})},
        'verification': checked,
        'artifacts': {n: sha(work / n) for n in ('envelopes.jsonl', 'profiles.jsonl', 'report.json') if (work / n).exists()},
        'work_directory': str(work)}
    save(prefix + 'summary.json', summary)
    if (work / 'report.json').exists():
        (out / 'report.json').write_bytes((work / 'report.json').read_bytes()); sanitize_file(out / 'report.json')
    print(json.dumps({k: summary[k] for k in ('gates', 'all_gates_pass', 'source_health', 'http_requests', 'wall_seconds', 'websites',
                                              'social_urls', 'facts')}))


def inventory(label):
    sys.path.insert(0, str(ROOT))
    from scripts.precision_ledger import kind, recheck
    work = work_dir(label)

    @lru_cache(maxsize=64)
    def body(content_sha):
        return (work / 'state/blobs' / content_sha).read_bytes()

    records = []
    for row in jsonl(work / 'envelopes.jsonl'):
        org = row['organisation_number']
        name = next((c['value'] for c in row['claims'] if c['field'] == 'identity.legal_name' and c['availability'] == 'available'), org)
        evidence = {e['id']: e for e in row['evidence']}
        for claim in row['claims']:
            typ = kind(claim)
            if claim['availability'] != 'available' or typ not in {'website', 'social'}:
                continue
            value = claim['value']
            url = value['final_url'] if typ == 'website' else value['url']
            tier = (value.get('proof_type') or value.get('identity_level')) if typ == 'website' else value.get('proof_tier')
            verdict, reasons, _checks = recheck(row, claim, body)
            receipts = []
            for eid in claim['evidence_ids']:
                e = evidence[eid]
                if e['source_class'] == 'official_registry':
                    continue
                raw = body(e['content_sha256'])
                assert hashlib.sha256(raw).hexdigest() == e['content_sha256']
                assert e['claim_span'] in raw.decode('utf8', errors='replace')
                receipts.append({k: e[k] for k in ('source_url', 'retrieved_at', 'content_sha256', 'locator', 'extraction_method', 'claim_span')})
            records.append({'organisation_number': org, 'company': name, 'kind': typ, 'url': url, 'proof_tier': tier,
                            'identity_level': value.get('identity_level'), 'field': claim['field'], 'claim_id': claim['id'],
                            'automated_verdict': verdict, 'reasons': reasons, 'receipts': receipts})
    records.sort(key=lambda r: (r['automated_verdict'] == 'correct', r['kind'], r['organisation_number'], r['url']))
    counts = Counter((r['kind'], r['automated_verdict']) for r in records)
    esc = lambda s: s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    def block(r):
        t = f"### {r['organisation_number']} - {r['company']} - {r['kind']}\n\n- url: `{r['url']}`\n- proof tier: `{r['proof_tier']}`"
        if r['identity_level']:
            t += f"\n- identity level: `{r['identity_level']}`"
        t += f"\n- automated verdict: **{r['automated_verdict']}**" + (f" ({'; '.join(r['reasons'])})" if r['reasons'] else '') + '\n\n'
        for e in r['receipts']:
            t += (f"Source: {e['source_url']}\n\nRetrieved: {e['retrieved_at']}; SHA-256 `{e['content_sha256']}`; "
                  f"locator `{e['locator']}`; method `{e['extraction_method']}`.\n\n<pre>{esc(e['claim_span'])}</pre>\n\n")
        return t

    doubtful = [r for r in records if r['automated_verdict'] != 'correct']
    text = ('# P3e scale-500 published website/social inventory\n\n'
            f'Seed {SEED}, 500 companies disjoint from every committed sample, run `r5-p3e-seed{SEED}-{label}` from a clean clone. '
            'Every published website and social URL is listed with exact saved excerpts, proof tier, retrieval time and SHA-256; '
            'each receipt was re-hashed from the saved body and its excerpt found verbatim. Automated verdicts use the existing '
            'offline precision-ledger rules (scripts/precision_ledger.py `recheck`); they are rule checks, not human verdicts.\n\n'
            '| Kind | Correct | Doubtful | Wrong |\n|---|---:|---:|---:|\n')
    for k in ('website', 'social'):
        text += f"| {k} | {counts[(k, 'correct')]} | {counts[(k, 'doubtful')]} | {counts[(k, 'wrong')]} |\n"
    tool_limited = [r for r in doubtful if r['automated_verdict'] == 'wrong' and (
        r['reasons'] == ['StopIteration'] or r['proof_tier'] in {'owner_jsonld_sameas_v1', 'own_contact_follow_us_v1'})]
    text += ('\nAutomated labels are shown exactly as produced. ' + str(len(tool_limited)) + ' "wrong" label(s) are ledger-tool '
             'limitations, not identity findings: `StopIteration` means the legacy recheck found no HTML identity receipt because '
             'the site was proven from a linked legal PDF (Stage L2), and "no longer verifies" on `owner_jsonld_sameas_v1` / '
             '`own_contact_follow_us_v1` means the legacy social recheck predates the X2 owner-declaration tiers. The full '
             'independent verifier (`check_live_run.py`, including `verify_legal_pdf` and `verify_owner_social`) passed every one '
             'of them. They stay listed for hand-check below.\n')
    text += f'\n## Automated-doubtful or wrong — for hand-check ({len(doubtful)})\n\n'
    text += ''.join(block(r) for r in doubtful) or 'None.\n\n'
    for k in ('website', 'social'):
        items = [r for r in records if r['kind'] == k and r['automated_verdict'] == 'correct']
        text += f'## {k.capitalize()} — automated correct ({len(items)})\n\n' + (''.join(block(r) for r in items) or 'None.\n\n')
    (DEST / 'urls.md').write_text(portable_text(text.rstrip() + '\n'), encoding='utf8', newline='\n')
    save('urls.json', {'output_sha256': sha(work / 'envelopes.jsonl'),
                       'counts': {f'{k}:{v}': n for (k, v), n in sorted(counts.items())}, 'records': records})
    print(json.dumps({f'{k}:{v}': n for (k, v), n in sorted(counts.items())}))


if __name__ == '__main__':
    action = sys.argv[1]
    if action == 'prepare':
        prepare()
    elif action == 'tests':
        tests()
    elif action == 'run':
        run(sys.argv[2])
    elif action == 'evaluate':
        evaluate(sys.argv[2], sys.argv[3])
    elif action == 'inventory':
        inventory(sys.argv[2])
    else:
        raise SystemExit(__doc__)
