"""Measure the frozen 100 with exactly the evaluator's seven flags and fresh state."""
from signalpost.portable_paths import expand, portable, portable_text, sanitize_file  # saved paths stay repo-relative
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timezone


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    stage = 'Defaults'
    project = Path(__file__).resolve().parents[3]
    base = project / 'reports/r5/baseline'
    dest = project / 'reports/r5/stageDefaults'
    out = project / '.data/r5/evaluator-defaults-run'
    if out.exists(): raise ValueError('Preserve prior run; output must be fresh')
    dest.mkdir(parents=True, exist_ok=True)
    settings = json.loads((base/'settings.json').read_text(encoding='utf8'))
    for name in ('sample','registry_subset'):
        item=settings['inputs'][name]
        assert sha(project/item['path'])==item['sha256']
    from signalpost.config import Config
    flags = {'organisations':base/'companies.jsonl', 'bulk':base/'registry100.csv',
             'output':out/'envelopes.jsonl', 'profiles_output':out/'profiles.jsonl',
             'report':out/'report.json', 'run_id':'r5-evaluator-defaults-seed20261017', 'expected_count':100}
    config = Config(**flags,site_dir=out/'site').model_dump(mode='json')
    # Only the seven official flags; the fresh working directory isolates default state/.
    args=[sys.executable,'-m','signalpost.cli','run']
    for k,v in flags.items():args.extend(['--'+k.replace('_','-'),str(v)])
    out.mkdir(parents=True)
    quote = lambda value: "'" + str(value).replace("'", "''") + "'"
    command = '# Run from '+out.as_posix()+' with the environment_overrides in settings.json.\n& '+' '.join(quote(arg) for arg in args)+'\n'
    (dest/'run.ps1').write_text(portable_text(command),encoding='utf8')
    metadata = {'stage': stage, 'parent_commit': subprocess.check_output(['git','rev-parse','HEAD'], text=True).strip(),
                'source_diff_sha256': hashlib.sha256(subprocess.check_output(['git','diff','HEAD','--','src','tests','docs'])).hexdigest(),
                'working_directory':out.as_posix(),'effective_state_dir':(out/'state').as_posix(),
                'command_argv':args,'exact_seven_flags':True,'resolved_config': config, 'environment_overrides': settings['environment_overrides'],
                'input_sha256': sha(base/'companies.jsonl'), 'registry_sha256': sha(base/'registry100.csv'),
                'started_at_utc': datetime.now(timezone.utc).isoformat()}
    (dest/'settings.json').write_text(portable_text(json.dumps(metadata, indent=2)+'\n'), encoding='utf8')
    env = os.environ.copy(); env.update(settings['environment_overrides'])
    began = time.perf_counter()
    with (dest/'process.txt').open('w', encoding='utf8') as log:
        result = subprocess.run(args, env=env, cwd=out, stdout=log, stderr=subprocess.STDOUT)
    sanitize_file(dest/'process.txt')  # keep captured paths repo-relative
    execution = {'exit_code': result.returncode, 'wall_seconds': time.perf_counter()-began,
                 'completed_at_utc': datetime.now(timezone.utc).isoformat()}
    (dest/'execution.json').write_text(portable_text(json.dumps(execution, indent=2)+'\n'), encoding='utf8')
    result.check_returncode()
    verify = [sys.executable,'scripts/verify_output.py','--first',config['output'],
              '--organisations',config['organisations'],'--count','100','--state-dir',str(out/'state'),'--report',config['report']]
    verified = subprocess.run(verify, env=env, capture_output=True, text=True, check=True)
    verification = {'command': verify, 'exit_code': 0, **json.loads(verified.stdout)}
    (dest/'verification.json').write_text(portable_text(json.dumps(verification, indent=2)+'\n'), encoding='utf8')
    summarize()


def summarize():
    project=Path(__file__).resolve().parents[3]
    dest=project/'reports/r5/stageDefaults'
    saved=json.loads((dest/'settings.json').read_text(encoding='utf8'))
    config=saved['resolved_config'];out=Path(expand(saved['working_directory']));stage='Defaults'
    execution=json.loads((dest/'execution.json').read_text(encoding='utf8'))
    verification=json.loads((dest/'verification.json').read_text(encoding='utf8'))
    # Use exactly the baseline counting definitions, not aggregate section success.
    rows = [json.loads(x) for x in Path(expand(config['output'])).read_text(encoding='utf8').splitlines()]
    report = json.loads(Path(expand(config['report'])).read_text(encoding='utf8'))
    assert report['total_cost_usd'] == report['search']['queries'] == report['llm']['calls'] == 0
    per = []
    for row in rows:
        claims = [c for c in row['claims'] if c['availability']=='available']
        per.append({'organisation_number': row['organisation_number'],
                    'verified_websites': sum(c['field']=='official_website' for c in claims),
                    'social_profiles': sum(c['field'].startswith('social_profile.') for c in claims),
                    'activity_claims': sum(c['family']=='activity' for c in claims),
                    'total_facts': len(claims),
                    'locations': sum(c['field'].startswith('subunits.unit.') for c in claims),
                    'job_ads': sum(c['field'].startswith('hiring.job.') for c in claims),
                    'contacts': sum(c['field'].startswith('contact.') for c in claims),
                    'section_states': row['run']['sections']})
    metrics = {'verified_websites':sum(c['verified_websites']>0 for c in per),
               'social_profile_companies':sum(c['social_profiles']>0 for c in per),
               'activity_companies':sum(c['activity_claims']>0 for c in per),
               'activity_claims':sum(c['activity_claims'] for c in per),
               'total_facts':sum(c['total_facts'] for c in per), 'locations':sum(c['locations'] for c in per),
               'job_ad_companies':sum(c['job_ads']>0 for c in per), 'contacts':sum(c['contacts'] for c in per),
               'http_requests':report['requests'], 'runtime_seconds':report['runtime_ms']/1000,
               'process_wall_seconds':execution['wall_seconds']}
    baseline = json.loads((project/'reports/r5/stage4_7/stepreuse/counts.json').read_text(encoding='utf8'))
    states = {s:{v:sum(c['section_states'].get(s,'not_recorded')==v for c in per)
                    for v in sorted(set(values)|{'not_recorded'})}
              for s,values in baseline['counts_by_section_state'].items()}
    assert all(sum(values.values())==len(per) for values in states.values())
    counts = {'metrics':metrics,'counts_by_section_state':states,'per_company':per,
              'metric_definitions':baseline['metric_definitions'],
              'artifacts':{name:sha(out/name) for name in ('envelopes.jsonl','profiles.jsonl','report.json')}}
    (dest/'counts.json').write_text(portable_text(json.dumps(counts,indent=2)+'\n'),encoding='utf8')
    (dest/'report.json').write_bytes(Path(expand(config['report'])).read_bytes())
    table = f'| Metric | Best 4.7 | Stage {stage} | Delta |\n|---|---:|---:|---:|\n'
    for key,val in metrics.items():
        before = baseline['metrics'][key]
        table += f'| {key} | {before:.3f} | {val:.3f} | {val-before:+.3f} |\n' if isinstance(val,float) else f'| {key} | {before} | {val} | {val-before:+} |\n'
    table += '\n| Section / state | Best 4.7 | Stage '+str(stage)+' | Delta |\n|---|---:|---:|---:|\n'
    for section,values in states.items():
        for state,val in values.items():
            before = baseline['counts_by_section_state'][section].get(state,0)
            table += f'| {section} / {state} | {before} | {val} | {val-before:+} |\n'
    (dest/'table.md').write_text(portable_text(table),encoding='utf8')
    print(json.dumps({'stage':stage,'metrics':metrics,'verification':verification,'section_states':states}))


if __name__ == '__main__':
    if sys.argv[1:]==['--summarize-only']: summarize()
    else: main()

