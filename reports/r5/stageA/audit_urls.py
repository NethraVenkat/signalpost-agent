"""List every website/social URL delta with the exact saved proof receipt."""
import hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
DEST=ROOT/'reports/r5/stageA'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def inventory(stage):
    settings=json.loads((ROOT/'reports/r5'/stage/'settings.json').read_text(encoding='utf8'))
    path=Path(settings['resolved_config']['output'])
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
    data={stage:inventory(stage) for stage in ['stageS','stageA0','stageA']}
    comparisons={}
    text='''# Stage A website and social URL changes\n\nEvery delta is listed by organisation number, legal name, URL and proof tier. Added entries cite the new snapshot; removed entries cite the historical snapshot and do not claim that the old proof is current. Excerpts below are exact saved spans, with source URL, retrieval time and SHA-256. The independent output verifier checks these spans against the saved bodies. Unchanged URLs are inventoried in url_inventory.json.\n\n'''
    for before,after in [('stageS','stageA0'),('stageA0','stageA'),('stageS','stageA')]:
        a,b=data[before],data[after];label=before+' to '+after
        added=[b['records'][key] for key in sorted(b['records'].keys()-a['records'].keys())]
        removed=[a['records'][key] for key in sorted(a['records'].keys()-b['records'].keys())]
        comparisons[label]={'added':added,'removed':removed}
        text+='## '+label+'\n\n'
        if not added and not removed:text+='No website or social URL was added or removed.\n\n'
        for action,items in [('Added',added),('Removed',removed)]:
            for item in items:
                text+='### '+action+': '+item['organisation_number']+' — '+item['name']+'\n\n'
                text+='- Kind: '+item['kind']+'\n- URL: '+item['url']+'\n- Proof tier: `'+str(item['proof_tier'])+'`\n'
                text+='- Source: '+item['source_url']+'\n- Retrieved: '+item['retrieved_at']+'\n- SHA-256: `'+item['content_sha256']+'`\n- Locator: `'+item['locator']+'`\n'
                text+='- '+after+' section states: `'+json.dumps(b['states'][item['organisation_number']],sort_keys=True)+'`\n\nExact excerpt:\n\n```html\n'+item['exact_excerpt']+'\n```\n\n'
    result={'inputs':{stage:{'output':info['output'],'sha256':info['sha256'],
                            'website_urls':sum(r['kind']=='website' for r in info['records'].values()),
                            'social_urls':sum(r['kind']=='social' for r in info['records'].values()),
                            'records':list(info['records'].values())} for stage,info in data.items()},
            'comparisons':comparisons}
    (DEST/'url_inventory.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    (DEST/'new_websites.md').write_text(text,encoding='utf8')
    print(json.dumps({k:{action:len(items) for action,items in value.items()} for k,value in comparisons.items()}))

if __name__=='__main__':main()
