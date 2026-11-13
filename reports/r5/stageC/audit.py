"""Audit both final C runs, retained proof nominations and cap usage."""
import json,hashlib
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[3]

def main():
    result={}
    for sample in ('frozen','daily'):
        folder=ROOT/'reports/r5/stageC'/sample
        settings=json.loads((folder/'settings.json').read_text(encoding='utf8'));out=Path(settings['working_directory'])
        rows=[json.loads(x) for x in (out/'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
        report=json.loads((out/'report.json').read_text(encoding='utf8'));verify=json.loads((folder/'verification.json').read_text(encoding='utf8'))
        assert len(rows)==100 and report['requests']<=1850 and report['total_cost_usd']==0
        assert report['site']['state']=='available' and report['site']['companies']==100
        assert report['site']['largest_profile_bytes']<250000
        assert report['completion']['within_effective_time_budget'] and report['completion']['within_requested_time_budget']
        assert verify['synthesis_unverified_values']==verify['briefing_unverified_values']==0
        assert [v for v in settings['command_argv'] if v.startswith('--')]==['--organisations','--bulk','--output','--profiles-output','--report','--run-id','--expected-count']
        manifest=json.loads((folder/'source_manifest.json').read_text(encoding='utf8'))
        assert all(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha for name,sha in manifest.items())
        web=Counter(e['organisation_number'] for e in report['request_log'] if e.get('section')=='website')
        assert max(web.values())<=13
        maps=Counter();nominated=Counter();blocked=[];verified=[]
        for row in rows:
            org=row['organisation_number'];targets=set()
            for attempt in row['run']['refresh'].get('proof_sitemaps',{}).get('attempts',[]):
                maps[attempt['state']]+=1
                targets.update(attempt['targets'])
            assert len(targets)<=2
            nominated[len(targets)]+=1
            if any(e['section']=='website' and e['code']=='block_page' for e in row['errors']):blocked.append(org)
            for claim in row['claims']:
                if claim['availability']=='available' and claim['field']=='official_website' and claim['value'].get('proof_page_url') in targets:verified.append({'orgnr':org,**claim['value']})
                if claim['family']=='activity' and claim['availability']=='available' and claim['field'].startswith('dated_item.'):
                    assert claim['value'].get('date_source')!='lastmod'
                    assert not any('/url/' in e['locator'] for e in row['evidence'] if e['id'] in claim['evidence_ids'])
        result[sample]={'http':report['requests'],'website_http_max':max(web.values()),'largest_profile_bytes':report['site']['largest_profile_bytes'],
            'sitemap_attempt_states':dict(maps),'companies_by_nominated_page_count':dict(nominated),
            'sitemap_proof_successes':verified,'challenge_companies':blocked,'source_manifest_matches':True,'cost_usd':0}
    (ROOT/'reports/r5/stageC/audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8');print(json.dumps(result))

if __name__=='__main__':main()
