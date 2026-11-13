"""Measure the frozen 100 with exactly the evaluator's seven flags and fresh state."""
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


def stage_name():
    stage=sys.argv[1]
    assert stage in ('A2','B','D','I','F1','C')
    return stage


def main():
    stage = stage_name()
    attempt=sys.argv[3] if len(sys.argv)>3 and sys.argv[3]!='--summarize-only' else None
    if attempt:assert attempt.isalnum()
    project = Path(__file__).resolve().parents[2]
    sample=sys.argv[2]
    assert sample in ('frozen','daily')
    base = project / ('reports/r5/baseline' if sample=='frozen' else 'reports/r5/release-v4')
    dest = project / 'reports/r5' / ('stage'+stage) / sample
    out = project / '.data/r5' / ('stage'+stage+'-'+sample+'-run')
    if attempt:out=out.with_name(out.name+'-'+attempt)
    if out.exists(): raise ValueError('Preserve prior run; output must be fresh')
    dest.mkdir(parents=True, exist_ok=True)
    if sample=='frozen':
        settings=json.loads((base/'settings.json').read_text(encoding='utf8'))
        companies=base/'companies.jsonl'
        for name in ('sample','registry_subset'):
            item=settings['inputs'][name];assert sha(project/item['path'])==item['sha256']
    else:
        saved=json.loads((base/'clean_clone.json').read_text(encoding='utf8'))
        companies=base/'companies100.jsonl'
        assert sha(companies)==saved['sample_sha256'] and sha(base/'registry100.csv')==saved['subset_sha256']
        settings={'environment_overrides':saved['environment_overrides']}
    from signalpost.config import Config
    flags = {'organisations':companies, 'bulk':base/'registry100.csv',
             'output':out/'envelopes.jsonl', 'profiles_output':out/'profiles.jsonl',
             'report':out/'report.json', 'run_id':'r5-stage'+stage+'-'+sample+'-seed'+('20261017' if sample=='frozen' else '20261113')+('-'+attempt if attempt else ''), 'expected_count':100}
    config = Config(**flags,site_dir=out/'site').model_dump(mode='json')
    # Only the seven official flags; the fresh working directory isolates default state/.
    args=[sys.executable,'-m','signalpost.cli','run']
    for k,v in flags.items():args.extend(['--'+k.replace('_','-'),str(v)])
    out.mkdir(parents=True)
    quote = lambda value: "'" + str(value).replace("'", "''") + "'"
    command = '# Run from '+out.as_posix()+' with the environment_overrides in settings.json.\n& '+' '.join(quote(arg) for arg in args)+'\n'
    (dest/'run.ps1').write_text(command,encoding='utf8')
    source_manifest={p.relative_to(project).as_posix():sha(p) for p in sorted((project/'src').rglob('*'))
                     if p.is_file() and '__pycache__' not in p.parts}
    (dest/'source_manifest.json').write_text(json.dumps(source_manifest,indent=2)+'\n',encoding='utf8')
    metadata = {'stage': stage, 'parent_commit': subprocess.check_output(['git','rev-parse','HEAD'], text=True).strip(),
                'source_diff_sha256': hashlib.sha256(subprocess.check_output(['git','diff','HEAD','--','src','tests','docs'],stderr=subprocess.PIPE)).hexdigest(),
                'working_directory':out.as_posix(),'effective_state_dir':(out/'state').as_posix(),
                'command_argv':args,'exact_seven_flags':True,'resolved_config': config, 'environment_overrides': settings['environment_overrides'],
                'input_sha256': sha(companies), 'registry_sha256': sha(base/'registry100.csv'),
                'source_manifest_sha256':sha(dest/'source_manifest.json'),
                'started_at_utc': datetime.now(timezone.utc).isoformat()}
    (dest/'settings.json').write_text(json.dumps(metadata, indent=2)+'\n', encoding='utf8')
    env = os.environ.copy(); env.update(settings['environment_overrides'])
    began = time.perf_counter()
    with (dest/'process.txt').open('w', encoding='utf8') as log:
        result = subprocess.run(args, env=env, cwd=out, stdout=log, stderr=subprocess.STDOUT)
    execution = {'exit_code': result.returncode, 'wall_seconds': time.perf_counter()-began,
                 'completed_at_utc': datetime.now(timezone.utc).isoformat()}
    (dest/'execution.json').write_text(json.dumps(execution, indent=2)+'\n', encoding='utf8')
    result.check_returncode()
    verify = [sys.executable,'scripts/verify_output.py','--first',config['output'],
              '--organisations',config['organisations'],'--count','100','--state-dir',str(out/'state'),'--report',config['report']]
    verified = subprocess.run(verify, env=env, capture_output=True, text=True, check=True)
    verification = {'command': verify, 'exit_code': 0, **json.loads(verified.stdout)}
    (dest/'verification.json').write_text(json.dumps(verification, indent=2)+'\n', encoding='utf8')
    summarize()


def summarize():
    project=Path(__file__).resolve().parents[2]
    stage=stage_name();sample=sys.argv[2]
    dest=project/'reports/r5'/('stage'+stage) / sample
    saved=json.loads((dest/'settings.json').read_text(encoding='utf8'))
    config=saved['resolved_config'];out=Path(saved['working_directory'])
    execution=json.loads((dest/'execution.json').read_text(encoding='utf8'))
    verification=json.loads((dest/'verification.json').read_text(encoding='utf8'))
    # Use exactly the baseline counting definitions, not aggregate section success.
    rows = [json.loads(x) for x in Path(config['output']).read_text(encoding='utf8').splitlines()]
    report = json.loads(Path(config['report']).read_text(encoding='utf8'))
    assert report['total_cost_usd'] == report['search']['queries'] == report['llm']['calls'] == 0
    assert report['requests']<=report['limits']['max_requests']==1850
    assert report['completion']['within_requested_time_budget'] and report['completion']['within_effective_time_budget']
    assert report['site']['state']=='available' and report['site']['companies']==100
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
    if stage in ('B','D','I','F1','C'):
        prior={'B':'A2','D':'B','I':'D','F1':'I','C':'F1'}[stage]
        baseline=json.loads((project/('reports/r5/stage'+prior)/sample/'counts.json').read_text(encoding='utf8'))
    elif sample=='frozen':baseline=json.loads((project/'reports/r5/stageA/counts.json').read_text(encoding='utf8'))
    else:
        old=json.loads((project/'reports/r5/release-v4/daily-summary.json').read_text(encoding='utf8'))
        oldrun=json.loads((project/'reports/r5/release-v4/daily.json').read_text(encoding='utf8'))
        oldrows=[json.loads(line) for line in (Path(oldrun['cwd'])/'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
        oldclaims=[[c for c in r['claims'] if c['availability']=='available'] for r in oldrows]
        baseline={'metrics':dict(metrics),'counts_by_section_state':old['section_states'],
                  'metric_definitions':json.loads((project/'reports/r5/stageA/counts.json').read_text(encoding='utf8'))['metric_definitions']}
        for k,oldkey in [('verified_websites','websites'),('activity_claims','activity_claims'),('total_facts','facts'),('http_requests','http_requests'),('runtime_seconds','runtime_seconds'),('process_wall_seconds','wall_seconds'),('contacts','contacts')]:baseline['metrics'][k]=old[oldkey]
        baseline['metrics'].update(social_profile_companies=sum(any(c['field'].startswith('social_profile.') for c in cs) for cs in oldclaims),
            activity_companies=sum(any(c['family']=='activity' for c in cs) for cs in oldclaims),
            locations=sum(c['field'].startswith('subunits.unit.') for cs in oldclaims for c in cs),
            job_ad_companies=sum(any(c['field'].startswith('hiring.job.') for c in cs) for cs in oldclaims))
    
    states = {s:{v:sum(c['section_states'].get(s,'not_recorded')==v for c in per)
                    for v in sorted(set(values)|{'not_recorded'}|{c['section_states'].get(s,'not_recorded') for c in per})}
              for s,values in baseline['counts_by_section_state'].items()}
    assert all(sum(values.values())==len(per) for values in states.values())
    counts = {'metrics':metrics,'counts_by_section_state':states,'per_company':per,
              'metric_definitions':baseline['metric_definitions'],
              'artifacts':{name:sha(out/name) for name in ('envelopes.jsonl','profiles.jsonl','report.json')}}
    (dest/'counts.json').write_text(json.dumps(counts,indent=2)+'\n',encoding='utf8')
    (dest/'report.json').write_bytes(Path(config['report']).read_bytes())
    table = f'| Metric | Prior measured run | Stage {stage} | Delta |\n|---|---:|---:|---:|\n'
    for key,val in metrics.items():
        before = baseline['metrics'][key]
        table += f'| {key} | {before:.3f} | {val:.3f} | {val-before:+.3f} |\n' if isinstance(val,float) else f'| {key} | {before} | {val} | {val-before:+} |\n'
    table += '\n| Section / state | Prior measured run | Stage '+str(stage)+' | Delta |\n|---|---:|---:|---:|\n'
    for section,values in states.items():
        for state,val in values.items():
            before = baseline['counts_by_section_state'][section].get(state,0)
            table += f'| {section} / {state} | {before} | {val} | {val-before:+} |\n'
    (dest/'table.md').write_text(table,encoding='utf8')
    print(json.dumps({'stage':stage,'metrics':metrics,'verification':verification,'section_states':states}))


if __name__ == '__main__':
    if '--summarize-only' in sys.argv[3:]: summarize()
    else: main()

