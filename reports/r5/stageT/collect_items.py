"""Saved-output measurements and full GLEIF/TED proof inventory; no network."""
from signalpost.portable_paths import expand, portable, portable_text  # saved paths stay repo-relative
import hashlib,json
import sys
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from signalpost.sources.exact_public import org_id,TED


def collect():
    dest=ROOT/'reports/r5/stageT';items=[];metrics={};inputs={};withheld=[]
    for sample,seed in [('frozen',20261017),('daily',20261113),('mock',20261114)]:
        folder=dest/sample;settings=json.loads((folder/'settings.json').read_text(encoding='utf8'))
        work=Path(expand(settings['working_directory']));output=work/'envelopes.jsonl'
        rows=[json.loads(x) for x in output.read_text(encoding='utf8').splitlines()]
        report=json.loads((folder/'report.json').read_text(encoding='utf8'))
        base=json.loads((folder/'counts.json').read_text(encoding='utf8'))['metrics']
        inputs[sample]={'seed':seed,'output':str(output),'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
            'source_manifest_sha256':settings['source_manifest_sha256'],'command_argv':settings['command_argv']}
        assert sum(x.startswith('--') for x in settings['command_argv'])==7
        public=[]
        for row in rows:
            evidence={e['id']:e for e in row['evidence']}
            name=next(c['value'] for c in row['claims'] if c['field']=='identity.legal_name' and c['availability']=='available')
            for c in row['claims']:
                if c['availability']!='available' or c['family'] not in {'gleif','procurement'}:continue
                typ='LEI' if c['field']=='gleif.record' else 'parent' if c['field'].startswith('gleif.parent.') else 'award'
                item={'sample':sample,'seed':seed,'organisation_number':row['organisation_number'],'company':name,'kind':typ,
                    'field':c['field'],'value':c['value'],'claim_id':c['id'],
                    'proof_tier':'exact_NO_RA000472' if typ=='LEI' else 'exact_child_LEI_ACTIVE_relationship' if typ=='parent' else 'exact_NO_role_selected_lot_contract',
                    'evidence':[evidence[e] for e in c['evidence_ids']]}
                items.append(item);public.append(item)
        base.update({t.lower()+'_companies':len({i['organisation_number'] for i in public if i['kind']==t}) for t in ('LEI','parent','award')})
        base.update({t.lower()+'_claims':sum(i['kind']==t for i in public) for t in ('LEI','parent','award')})
        base['source_http']=dict(Counter(e.get('section') for e in report['request_log'] if e.get('section') in {'gleif','procurement'}))
        base['source_states']={s:dict(Counter(r['run']['sections'].get(s,'not_recorded') for r in rows)) for s in ('gleif','procurement')}
        base['source_error_codes']={s:dict(Counter(e['code'] for r in rows for e in r['errors'] if e['section']==s)) for s in ('gleif','procurement')}
        base['ratios']=sum(m['formula']!='revenue_yoy' for r in rows for m in (r['run'].get('synthesis') or {}).get('financial_metrics',[]))
        base['yoy']=sum(m['formula']=='revenue_yoy' for r in rows for m in (r['run'].get('synthesis') or {}).get('financial_metrics',[]))
        base['activity_claims_including_procurement']=base['activity_claims']+base['award_claims']
        metrics[sample]=base
        lookup={r['organisation_number']:r for r in rows};nominations={}
        for event in report['request_log']:
            if event['url']!=TED or event.get('status')!=200:continue
            document=json.loads((work/'state/blobs'/event['content_sha256']).read_bytes())
            for notice in document.get('notices',[]):
                for role in ('winner-identifier','buyer-identifier'):
                    for value in notice.get(role,[]):
                        org=org_id(value)
                        if org not in lookup:continue
                        row=lookup[org]
                        if row['run']['sections'].get('procurement')=='available':continue
                        key=(org,notice['publication-number'],role)
                        nominations[key]={'sample':sample,'organisation_number':org,
                            'company':next(c['value'] for c in row['claims'] if c['field']=='identity.legal_name' and c['availability']=='available'),
                            'notice':notice['publication-number'],'search_role':role,'raw_search_id':value,
                            'url':'https://ted.europa.eu/en/notice/-/detail/'+notice['publication-number'],
                            'state':row['run']['sections']['procurement'],'reason_codes':[e['code'] for e in row['errors'] if e['section']=='procurement'],
                            'search_response_sha256':event['content_sha256'],'published':False,
                            'warning':'Search nomination only; XML country/role/lot proof was not obtained. Not a published award or verified company relationship.'}
        withheld+=list(nominations.values())
    text='# Stage T: every published LEI, parent and award\n\nExact saved excerpts, not fresh verification. Parent means the specified ACTIVE GLEIF accounting-consolidation relationship, not an inferred ownership share. TED search hits without structured exact-role proof are withheld and their source failures remain in reports. No procurement amount is published.\n\n'
    text+='| Seed | LEI companies | Parent companies | Award companies / claims | GLEIF / TED HTTP | All HTTP | Wall s |\n|---|---:|---:|---:|---:|---:|---:|\n'
    for sample,seed in [('frozen',20261017),('daily',20261113),('mock',20261114)]:
        m=metrics[sample];text+=f"| {seed} | {m['lei_companies']} | {m['parent_companies']} | {m['award_companies']} / {m['award_claims']} | {m['source_http'].get('gleif',0)} / {m['source_http'].get('procurement',0)} | {m['http_requests']} | {m['process_wall_seconds']:.3f} |\n"
    for i,item in enumerate(items,1):
        text+=f"\n## {i}. {item['kind']}: {item['organisation_number']} - {item['company']} (seed {item['seed']})\n\n"
        text+='Proof tier: `'+item['proof_tier']+'`.\n\nPublished value:\n\n```json\n'+json.dumps(item['value'],ensure_ascii=False,indent=2)+'\n```\n\n'
        for e in item['evidence']:
            text+=f"Source: {e['source_url']}\n\nRetrieved: {e['retrieved_at']}; SHA-256: `{e['content_sha256']}`; locator: `{e['locator']}`.\n\nExact excerpt:\n\n```text\n{e['claim_span']}\n```\n\n"
    (dest/'items.md').write_text(portable_text(text),encoding='utf8',newline='')
    (dest/'items.json').write_text(portable_text(json.dumps({'inputs':inputs,'items':items},ensure_ascii=False,indent=2)+'\n'),encoding='utf8')
    (dest/'metrics.json').write_text(portable_text(json.dumps(metrics,indent=2)+'\n'),encoding='utf8')
    (dest/'withheld_ted_nominations.json').write_text(portable_text(json.dumps(withheld,ensure_ascii=False,indent=2)+'\n'),encoding='utf8')
    print(json.dumps(metrics))


if __name__=='__main__':collect()
