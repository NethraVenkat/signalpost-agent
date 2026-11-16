"""List every website/social URL delta with the exact saved proof receipt."""
from signalpost.portable_paths import expand, portable, portable_text  # saved paths stay repo-relative
import hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
import sys
STAGE=sys.argv[1]
assert STAGE in ('A2','B','D','I','C','C2','E')
DEST=ROOT/'reports/r5'/('stage'+STAGE)

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def inventory(stage):
    if stage in ('release','release-v4b'):
        saved=json.loads((ROOT/('reports/r5/release-v4b' if stage=='release-v4b' else 'reports/r5/release-v4')/'daily.json').read_text(encoding='utf8'))
        path=Path(expand(saved['cwd']))/'envelopes.jsonl'
    else:
        settings=json.loads((ROOT/'reports/r5'/stage/'settings.json').read_text(encoding='utf8'))
        path=Path(expand(settings['cwd']))/'envelopes.jsonl' if stage=='stageE/live_refresh' else Path(expand(settings['resolved_config']['output']))
    if not path.is_absolute():path=ROOT/path
    rows=[json.loads(line) for line in path.read_text(encoding='utf8').splitlines()]
    records={};states={}
    for row in rows:
        org=row['organisation_number'];states[org]=row['run']['sections']
        name=next(c['value'] for c in row['claims'] if c['field']=='identity.legal_name' and c['availability']=='available')
        evidence={e['id']:e for e in row['evidence']}
        for claim in row['claims']:
            if claim['availability']!='available':continue
            kind='website' if claim['field']=='official_website' else 'social' if claim['field'].startswith('social_profile.') else None
            if not kind:continue
            value=claim['value'];url=value['final_url'] if kind=='website' else value['url']
            receipts=[evidence[eid] for eid in claim['evidence_ids']]
            prefix='identity-proof:' if kind=='website' else 'company-link:'
            receipt=next(e for e in receipts if e['locator'].startswith(prefix))
            assert receipt['claim_span'] and len(receipt['claim_span'])<=300
            records[(org,kind,url)]={'organisation_number':org,'name':name,'kind':kind,'url':url,
                'proof_tier':value.get('identity_level') if kind=='website' else value.get('proof_tier'),
                'candidate_origin':value.get('candidate_origin'),'claim_id':claim['id'],
                'exact_excerpt':receipt['claim_span'],'source_url':receipt['source_url'],
                'retrieved_at':receipt['retrieved_at'],'content_sha256':receipt['content_sha256'],
                'locator':receipt['locator'],'evidence_ids':claim['evidence_ids']}
    return {'output':str(path),'sha256':sha(path),'records':records,'states':states}


def main():
    pairs=[('stageA','stageA2/frozen'),('release','stageA2/daily')] if STAGE=='A2' else [('stageA2/frozen','stageB/frozen'),('stageA2/daily','stageB/daily')]
    if STAGE in ('D','I','C'):
        prior={'D':'B','I':'D','C':'F1'}[STAGE]
        pairs=[('stage'+prior+'/'+s,'stage'+STAGE+'/'+s) for s in ('frozen','daily')]
    if STAGE=='C2':pairs=[('stageC/frozen','stageC2/frozen'),('stageC/daily','stageC2/daily'),('release-v4b','stageC2/mock')]
    if STAGE=='E':pairs=[('stageC2/'+s,'stageE/'+s) for s in ('frozen','daily','mock')]+[('stageE/frozen','stageE/live_refresh')]
    data={stage:inventory(stage) for pair in pairs for stage in pair}
    comparisons={}
    text='# Stage '+STAGE+' website/social URL changes\n\nAll deltas use exact saved proof excerpts; removed receipts are historical, not current proof. Unchanged URLs are fully inventoried in url_inventory.json.\n\n'
    for before,after in pairs:
        a,b=data[before],data[after];label=before+' to '+after
        added=[b['records'][key] for key in sorted(b['records'].keys()-a['records'].keys())]
        removed=[a['records'][key] for key in sorted(a['records'].keys()-b['records'].keys())]
        comparisons[label]={'added':added,'removed':removed}
        text+='## '+label+'\n\n'
        if not added and not removed:text+='No website/social URL changes.\n\n'
        for action,items in [('Added',added),('Removed',removed)]:
            for item in items:
                text+='### '+action+': '+item['organisation_number']+' - '+item['name']+'\n\n'
                for key in ['kind','url','proof_tier','source_url','retrieved_at','content_sha256','locator']:
                    text+='- '+key+': `'+str(item[key])+'`\n'
                text+='\nExact excerpt:\n\n```html\n'+item['exact_excerpt']+'\n```\n\n'
    result={'inputs':{stage:{'output':info['output'],'sha256':info['sha256'],
                            'website_urls':sum(r['kind']=='website' for r in info['records'].values()),
                            'social_urls':sum(r['kind']=='social' for r in info['records'].values()),
                            'records':list(info['records'].values())} for stage,info in data.items()},
            'comparisons':comparisons}
    (DEST/'url_inventory.json').write_text(portable_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n'),encoding='utf8')
    (DEST/'new_websites.md').write_text(portable_text(text.rstrip()+'\n'),encoding='utf8',newline='')
    print(json.dumps({k:{action:len(items) for action,items in value.items()} for k,value in comparisons.items()}))

if __name__=='__main__':main()
