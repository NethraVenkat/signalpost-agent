"""List every published website/social URL new against the saved Stage 3 run."""
from signalpost.portable_paths import expand, portable, portable_text  # saved paths stay repo-relative
import json
from pathlib import Path


def load(path):
    return [json.loads(x) for x in path.read_text(encoding='utf8').splitlines()]


def urls(row):
    return {(c['field'].split('.')[0], c['value'].get('final_url') or c['value'].get('url'))
            for c in row['claims'] if c['availability']=='available' and
            (c['field']=='official_website' or c['field'].startswith('social_profile.'))}


def main():
    baseline={r['organisation_number']:urls(r) for r in load(Path('.data/r5/stage3-run/envelopes.jsonl'))}
    entries=[]
    for step in ('4_1','4_2','4_3','4_4','4_5','4_6'):
        path=Path(f'.data/r5/stage4/step{step}-run/envelopes.jsonl')
        settings=Path(f'reports/r5/stage4/step{step}/settings.json')
        if settings.exists(): path=Path(expand(json.loads(settings.read_text(encoding='utf8'))['resolved_config']['output']))
        if not path.exists():continue
        for row in load(path):
            org=row['organisation_number']; evidence={e['id']:e for e in row['evidence']}
            name=next((c['value'] for c in row['claims'] if c['field']=='identity.legal_name'),org)
            for c in row['claims']:
                if c['availability']!='available' or not (c['field']=='official_website' or c['field'].startswith('social_profile.')):continue
                value=c['value'];url=value.get('final_url') or value.get('url');kind=c['field'].split('.')[0]
                if (kind,url) in baseline[org]:continue
                sources=[evidence[eid] for eid in c['evidence_ids'] if evidence[eid]['source_class']=='company_owned']
                assert sources
                for e in sources:
                    import hashlib
                    body=(path.parent/'state'/'blobs'/e['content_sha256']).read_bytes()
                    assert hashlib.sha256(body).hexdigest()==e['content_sha256']
                    from signalpost.sources.text import decode_body
                    assert e['claim_span'] in decode_body(body) and len(e['claim_span'])<=300
                entries.append({'step':step.replace('_','.'),'org':org,'company':name,'url':url,
                    'tier':value.get('identity_level') or value.get('proof_tier') or 'linked social',
                    'kind':kind,'sources':sources})
    dest=Path('reports/r5/stage4')
    (dest/'new_websites.json').write_text(portable_text(json.dumps(entries,indent=2,ensure_ascii=False)+'\n'),encoding='utf8')
    text='# New websites and social profiles versus Stage 3\n\nEvery row is a newly published URL against Stage 3, including intermediate sub-steps. Repeated rows across steps are intentional. Exact excerpts and full provenance are retained in new_websites.json. Final retention must be checked against step4_6; removed intermediate matches are not final publications.\n\n'
    for e in entries:
        text+=f"## Step {e['step']} — {e['org']} — {e['company']}\n\nURL: {e['url']}\n\nKind: {e['kind']}; proof tier: {e['tier']}.\n\n"
        for s in e['sources']:
            text+=f"Source: {s['source_url']}\n\nVerbatim proof excerpt (at most 300 characters):\n\n```text\n{s['claim_span']}\n```\n\n"
    if not entries:text+='No website or social profile URL new versus Stage 3 was published.\n'
    (dest/'new_websites.md').write_text(portable_text(text),encoding='utf8')
    print(json.dumps(entries,ensure_ascii=True))


if __name__=='__main__':main()
