"""Evidence inventory and stage comparisons, using saved responses only."""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

from declared_audit import ROOT,SEEDS,records,save,sites
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from signalpost.sources.text import decode_body
from scripts.accuracy_audit import audit_website_claim,audit_social_claim,extract_org_context_and_leaders


def inventory(stage,seed):
    settings,work,registry,rows,report=records(stage,seed)
    result={}
    for row in rows:
        org=row['organisation_number'];evidence={e['id']:e for e in row['evidence']}
        context,leaders=extract_org_context_and_leaders(row['claims'])
        website=next(iter(sites(row)),None)
        units={org:{c['value']['organisation_number'] for c in row['claims'] if c['field'].startswith('subunits.unit.') and c['availability']=='available'}}
        for c in row['claims']:
            if c['availability']!='available' or not (c['field']=='official_website' or c['field'].startswith('social_profile.')):continue
            kind='website' if c['field']=='official_website' else 'social'
            value=c['value'];url=value['final_url'] if kind=='website' else value['url']
            receipts=[evidence[ref] for ref in c['evidence_ids']]
            own=[e for e in receipts if e['source_class']=='company_owned' and e['extraction_method']=='signalpost.website.v1'
                 and (e['source_url']==value['proof_page_url'] if kind=='website' else e['locator']=='company-link:'+url)]
            checks=[]
            for e in own:
                body=(work/'state/blobs'/e['content_sha256']).read_bytes()
                assert hashlib.sha256(body).hexdigest()==e['content_sha256']
                assert e['claim_span'] in decode_body(body)
                if kind=='website':
                    status,reason,_=audit_website_claim(org,c,e,decode_body(body),context=context,leaders=leaders,subunit_map=units)
                else:
                    status,reason,_=audit_social_claim(org,c,e,decode_body(body),website_claim=website,context=context)
                checks.append({'status':status,'reason':reason,'source_url':e['source_url'],'content_sha256':e['content_sha256']})
            # The social claim can carry its site's proof page as a dependency;
            # at least the exact own-link receipt must pass the existing rule.
            verdict='correct' if any(c['status']=='CORRECT' for c in checks) else 'doubtful'
            reg_fields={'identity.legal_name','identity.registered_website','identity.registered_phone','identity.registered_mobile','identity.registered_email'}
            registry_receipts={c['field']:{'value':c['value'],'evidence':[evidence[e] for e in c['evidence_ids']]} for c in row['claims']
                               if c['field'] in reg_fields and c['availability']=='available'}
            result[(org,kind,url)]={'seed':seed,'orgnr':org,'legal_name':context['name'],'kind':kind,'url':url,
                'tier':value.get('proof_type') if kind=='website' else value.get('proof_tier'),'value':value,
                'own_receipts':own,'registry_receipts':registry_receipts,'automated_verdict':verdict,'checks':checks}
    return result


def main():
    stage=sys.argv[1];assert stage in {'stageR5','stageR3'}
    previous='stageW' if stage=='stageR5' else 'stageR5'
    dest=ROOT/'reports/r5'/stage
    added,removed,all_items,tables=[],[],[],[]
    for seed in SEEDS:
        old=inventory(previous,seed);new=inventory(stage,seed)
        added.extend(new[k] for k in new.keys()-old.keys());removed.extend(old[k] for k in old.keys()-new.keys())
        all_items.extend(new.values())
        tables.append(json.loads((dest/f'seed{seed}/counts.json').read_text(encoding='utf8')))
    checks={'stage':stage,'previous_stage':previous,'samples':tables,'added':sorted(added,key=lambda x:(x['seed'],x['orgnr'],x['kind'],x['url'])),
            'removed':removed,'all_published_items':all_items,'new_doubtful':[i for i in added if i['automated_verdict']!='correct'],
            'limits':'Saved-evidence rule recheck, not independent live ownership confirmation. No items removed by the report generator.'}
    save(dest/'items.json',checks)
    lines=['# New/removed websites and social profiles — '+stage,'',
           f'Comparison with {previous}; all changes included, including live-source recoveries/losses under existing tiers. Complete receipts, hashes and dates in items.json. No paid source or model.','']
    for change,items in [('Added',checks['added']),('Removed',removed)]:
        lines += [f'## {change}: {len(items)}','']
        for i in items:
            lines += [f"### {i['seed']} / {i['orgnr']} / {i['legal_name']} / {i['kind']}",'',
                      f"URL: {i['url']}",f"Tier: `{i['tier']}`; saved-evidence recheck: {i['automated_verdict']}.",'']
            if r:=i['value'].get('publisher_identity'):
                lines += ['Publisher location: '+r['publisher_location'],'','Exact extracted publisher-block text:','',r['publisher_excerpt'],'']
                if r.get('contact'):lines += ['Contact/rarity receipt:','',json.dumps(r['contact'],ensure_ascii=False),'']
            for e in i['own_receipts']:
                lines += [f"Source: {e['source_url']} / retrieved {e['retrieved_at']} / SHA-256 `{e['content_sha256']}`",'', 'Exact verbatim response excerpt:','',e['claim_span'],'']
            lines += ['Registry receipts:','','```json',json.dumps(i['registry_receipts'],ensure_ascii=False,indent=2),'```','']
    if checks['new_doubtful']:
        lines += ['## Requires withholding/review','',json.dumps(checks['new_doubtful'],ensure_ascii=False,indent=2)]
    (dest/'new_websites.md').write_text('\n'.join(lines)+'\n',encoding='utf8',newline='\n')
    print(json.dumps({'added':dict(Counter(i['kind'] for i in added)),'removed':dict(Counter(i['kind'] for i in removed)),
                      'new_doubtful':[(i['orgnr'],i['url']) for i in checks['new_doubtful']],
                      'websites':sum(t['websites_after'] for t in tables),'declared_recall':sum(t['declared_recall_after'] for t in tables),
                      'http':sum(t['http_after'] for t in tables),'runtime':sum(t['runtime_seconds'] for t in tables)},ensure_ascii=False))


if __name__=='__main__':main()
