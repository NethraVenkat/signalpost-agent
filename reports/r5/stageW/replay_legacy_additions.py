"""Replay any live recovery with the exact committed pre-R4 proof code."""
import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
DEST = Path(__file__).resolve().parent
OLD = ROOT / '.data/r5/stageR2-commit-check'


def main():
    if '--old-code' not in sys.argv:
        env = os.environ.copy(); env['PYTHONPATH'] = str(OLD / 'src') + os.pathsep + str(OLD)
        result = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--old-code'], cwd=OLD, env=env, capture_output=True, text=True, encoding='utf8')
        print(result.stdout, end=''); print(result.stderr, end='', file=sys.stderr)
        raise SystemExit(result.returncode)
    import signalpost
    from signalpost.web.html import Page
    from signalpost.web.proof import score
    from signalpost.web.candidates import context_from_bulk
    assert Path(signalpost.__file__).resolve().is_relative_to((OLD / 'src').resolve())
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=OLD, text=True).strip()
    assert head.startswith('81a76b8d')
    cases = []
    for counts_path in sorted(DEST.glob('seed*/counts.json')):
        counts = json.loads(counts_path.read_text(encoding='utf8'))
        settings = json.loads((counts_path.parent / 'settings.json').read_text(encoding='utf8'))
        if not counts['changes']['added']:
            continue
        argv = settings['command_argv']; bulk = Path(argv[argv.index('--bulk') + 1])
        with bulk.open(encoding='utf-8-sig', newline='') as f:
            registry = {r['organisasjonsnummer']: r for r in csv.DictReader(f)}
        work = Path(settings['working_directory'])
        rows = {r['organisation_number']: r for line in (work / 'envelopes.jsonl').read_text(encoding='utf8').splitlines() if (r := json.loads(line))}
        prior = {r['organisation_number']: r for line in (Path(settings['previous_working_directory']) / 'envelopes.jsonl').read_text(encoding='utf8').splitlines() if (r := json.loads(line))}
        for org in counts['changes']['added']:
            row = rows[org]; claim = next(c for c in row['claims'] if c['field'] == 'official_website' and c['availability'] == 'available')
            evidence = {e['id']: e for e in row['evidence']}
            receipt = next(evidence[e] for e in claim['evidence_ids'] if evidence[e]['locator'].startswith('identity-proof:'))
            body = (work / 'state/blobs' / receipt['content_sha256']).read_bytes()
            assert hashlib.sha256(body).hexdigest() == receipt['content_sha256']
            page = Page(body, receipt['source_url']); context = context_from_bulk(registry[org])
            proof = score(page, org, context, claim['value']['candidate_origin'], [])
            assert proof.level == 'VERIFIED' and proof.token == org
            assert page.proof_span(org) and receipt['claim_span'] in page.raw
            errors = [e for e in prior[org]['errors'] if e['section'] == 'website']
            cases.append({'seed': counts['seed'], 'orgnr': org, 'name': context['name'], 'url': claim['value']['final_url'],
                          'proof_page': page.url, 'content_sha256': receipt['content_sha256'], 'exact_excerpt': receipt['claim_span'],
                          'retrieved_at': receipt['retrieved_at'], 'pre_R4_level': proof.level, 'pre_R4_proof_type': proof.proof_type,
                          'pre_R4_token': proof.token, 'historical_errors': errors,
                          'classification': 'Existing exact-number policy also publishes this saved response; historical candidate was already attempted but timed out. Live source recovery, not a new positive proof rule.'})
    data = {'pre_R4_commit': head, 'application_module': signalpost.__file__, 'network_requests': 0,
            'method': 'Unmodified pre-R4 score and localization functions from the isolated committed R2 worktree, applied to the exact new saved response bytes.', 'cases': cases}
    (DEST / 'legacy_addition_replay.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(data, ensure_ascii=True))


if __name__ == '__main__':
    main()
