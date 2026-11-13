"""Inventory every published company website/social URL for the daily smoke."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
DEST=ROOT/'reports/r5/release-v4'
path=ROOT/'.data/release-v4/daily/envelopes.jsonl'
rows=[json.loads(line) for line in path.read_text(encoding='utf8').splitlines()]
records=[]
for row in rows:
    org=row['organisation_number'];name=next((c['value'] for c in row['claims'] if c['field']=='identity.legal_name' and c['availability']=='available'),org)
    evidence={e['id']:e for e in row['evidence']}
    for c in row['claims']:
        if c['availability']!='available':continue
        field=c['field'];value=c['value'];kind=tier=url=prefix=None
        if field=='official_website':
            kind='verified company website';tier=value['identity_level'];url=value['final_url'];prefix='identity-proof:'
        elif field.startswith('social_profile.'):
            kind='verified company social profile';tier=value['proof_tier'];url=value['url'];prefix='company-link:'
        elif field.startswith('registry_social.'):
            kind='registry-asserted social URL';tier='REGISTRY_ASSERTED (not website ownership proof)';url=value['url']
        elif field=='identity.registered_website' or (field.startswith('subunits.detail.') and field.endswith('.registered_website')):
            kind='registry homepage field';tier='REGISTRY_FIELD_ONLY (not website ownership proof)';url=str(value)
        if not kind:continue
        refs=[evidence[eid] for eid in c['evidence_ids']]
        proof=next(e for e in refs if e['locator'].startswith(prefix)) if prefix else refs[0]
        supporting=[e for e in refs if e['id']!=proof['id'] and (
            e['locator'].startswith(('identity-proof:','registry-contact:'))
            or '/column:navn' in e['locator'] or '/column:telefon' in e['locator']
            or '/column:epostadresse' in e['locator'] or '/column:forretningsadresse' in e['locator']
            or e['locator'] in {'/navn','/telefon','/epostadresse','/forretningsadresse'})]
        records.append({'organisation_number':org,'name':name,'kind':kind,'url':url,'proof_tier':tier,
            'field':field,'claim_id':c['id'],'exact_excerpt':proof['claim_span'],'source_url':proof['source_url'],
            'retrieved_at':proof['retrieved_at'],'content_sha256':proof['content_sha256'],'locator':proof['locator'],
            'all_evidence_ids':c['evidence_ids'],'supporting_receipts':supporting,'proof_details':value if isinstance(value,dict) else None})
records.sort(key=lambda r:(r['kind'],r['organisation_number'],r['url'],r['field']))
text='''# Release v4 / v1.2.0 - published website and social URLs\n\nDaily smoke: new random 100, seed 20261113. Every semantic company website/social URL claim is listed, including registry homepage/social assertions separately from ownership-verified URLs. A registry field alone is not presented as a verified official website. Proof excerpts below are verbatim stored spans; source URL, retrieval date, hash and locator permit hand checking. Source receipt hashes/spans pass verify_output.py.\n\n'''
for kind in sorted({r['kind'] for r in records}):
    items=[r for r in records if r['kind']==kind]
    text+='## '+kind+' ('+str(len(items))+')\n\n'
    for r in items:
        text+='### '+r['organisation_number']+' - '+r['name']+'\n\n'
        for label,key in [('URL','url'),('Proof tier','proof_tier'),('Field','field'),('Source','source_url'),('Retrieved','retrieved_at'),('SHA-256','content_sha256'),('Locator','locator')]:
            text+='- '+label+': `'+str(r[key])+'`\n'
        text+='\nExact excerpt:\n\n```html\n'+r['exact_excerpt']+'\n```\n\n'
        if r['proof_details']:text+='Proof details: `'+json.dumps(r['proof_details'],ensure_ascii=False,sort_keys=True)+'`\n\n'
        if r['kind'].startswith('verified'):
            for receipt in r['supporting_receipts']:
                text+='Supporting receipt: '+receipt['source_url']+'; '+receipt['retrieved_at']+'; SHA-256 `'+receipt['content_sha256']+'`; locator `'+receipt['locator']+'`.\n\n```html\n'+receipt['claim_span']+'\n```\n\n'

if not records:text+='No website or social URL claims were published.\n'
(DEST/'urls.md').write_text(text,encoding='utf8')
result={'source_output':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'count_by_kind':{kind:sum(r['kind']==kind for r in records) for kind in sorted({r['kind'] for r in records})},'urls':records}
(DEST/'urls.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(result['count_by_kind']))
