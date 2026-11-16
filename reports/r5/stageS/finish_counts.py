"""Write counts.json for a sample whose single run completed but whose in-run site
build failed the gate (seed 20261117). Same definitions as measure.py; reads the saved
run only (no recrawl). Site figures come from the re-render (resite.py)."""
from signalpost.portable_paths import portable_text
import json, sys, hashlib
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]; DEST = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'reports/r5/stageX'))
from measure import counts, identities  # noqa: E402
from signalpost.sources.exact_official import FAMILIES as F  # noqa: E402
seed = int(sys.argv[1]); out = DEST / f'seed{seed}'; work = ROOT / '.data/r5' / f'stageS-{seed}-final'
assert not (out / 'counts.json').exists()
rows = [json.loads(s) for s in open(work / 'envelopes.jsonl', encoding='utf8', newline='').read().split(chr(10)) if s.strip()]
run = json.loads((work / 'report-run.json').read_text(encoding='utf8')); site = json.loads((out / 'resite.json').read_text(encoding='utf8'))['site']
base = json.loads((ROOT / f'reports/r5/stageP0rb/seed{seed}/counts.json').read_text(encoding='utf8'))
key = lambda i: (i['orgnr'], i['kind'], str(i['identity']))
now = sorted([{k: v for k, v in i.items() if k != 'evidence'} for i in identities(rows).values()], key=key)
b = {key(i): i for i in base['identity_items']}; a = {key(i): i for i in now}
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
v = {'baseline': {k: base[k] for k in ('counts', 'HTTP', 'CLI_runtime_seconds', 'site')},
     'official_claims': {f: sum(c['family'] == f for r in rows for c in r['claims'] if c['availability'] == 'available') for f in F},
     'official_companies': {f: sum(any(c['family'] == f and c['availability'] == 'available' for c in r['claims']) for r in rows) for f in F},
     'official_sections': {f: dict(Counter(r['run']['sections'].get(f, 'not_recorded') for r in rows)) for f in F},
     'identity_changes': {'added': [a[k] for k in sorted(a.keys() - b.keys())], 'removed': [b[k] for k in sorted(b.keys() - a.keys())]},
     'seed': seed, 'counts': counts(rows), 'HTTP': run['requests'],
     'CLI_runtime_seconds': json.loads((out / 'execution.json').read_text(encoding='utf8'))['wall_seconds'],
     'cost_usd': run['total_cost_usd'], 'site': site, 'run_site': run['site'], 'identity_items': now,
     'envelopes_sha256': sha(work / 'envelopes.jsonl'), 'profiles_sha256': sha(work / 'profiles.jsonl')}
(out / 'counts.json').write_text(portable_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n'), encoding='utf8', newline='\n')
