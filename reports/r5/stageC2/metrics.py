"""Measure exhausted scopes and proof gains without equating live drift to causality."""
from signalpost.portable_paths import portable, portable_text  # saved paths stay repo-relative
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]

def load_run(folder,release=False):
    meta=json.loads((folder/('daily.json' if release else 'settings.json')).read_text(encoding='utf8'))
    out=Path(meta['cwd'] if release else meta['working_directory'])
    rows=[json.loads(x) for x in (out/'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
    report=json.loads((out/'report.json').read_text(encoding='utf8'))
    limited={r['organisation_number'] for r in rows if not any(c['field']=='official_website' and c['availability']=='available' for c in r['claims'])
        and any(e['section']=='website' and e['code'] in {'website_budget_exhausted','dns_budget_exhausted','budget_exhausted','deadline'} for e in r['errors'])}
    sites={r['organisation_number']:c['value'] for r in rows for c in r['claims'] if c['field']=='official_website' and c['availability']=='available'}
    return out,rows,report,limited,sites

def main():
    result={}
    for sample in ('frozen','daily','mock'):
        before=ROOT/('reports/r5/release-v4b' if sample=='mock' else 'reports/r5/stageC/'+sample)
        after=ROOT/'reports/r5/stageC2'/sample
        a,ar,ap,al,asites=load_run(before,sample=='mock');b,br,bp,bl,bsites=load_run(after)
        pass2=bp['adaptive_websites']['pass2'];records=pass2['per_company'];extended={o:r for o,r in records.items() if r.get('c2_extended')}
        result[sample]={'prior_budget_exhausted_companies':len(al),'experiment_budget_exhausted_companies':len(bl),
            'prior_sites':len(asites),'experiment_sites':len(bsites),'added_orgs':sorted(bsites.keys()-asites.keys()),'removed_orgs':sorted(asites.keys()-bsites.keys()),
            'extended_companies':len(extended),'extension_verified_gains':sum(r['websites_gained'] for r in extended.values()),
            'pass2_websites_gained':pass2['websites_gained'],'http':bp['requests'],
            'wall_seconds':json.loads((after/'execution.json').read_text(encoding='utf8'))['wall_seconds'],
            'pass2_requests':pass2['requests'],'pass2_states':pass2['states'],'extended_records':extended,
            'website_http_max':max(Counter(e['organisation_number'] for e in bp['request_log'] if e.get('section')=='website').values(),default=0),
            'output_sha256':json.loads((after/'counts.json').read_text(encoding='utf8'))['artifacts']['envelopes.jsonl']}
        assert result[sample]['website_http_max']<=23 and bp['requests']<=1850 and bp['total_cost_usd']==0
    dest=ROOT/'reports/r5/stageC2/metrics.json';dest.write_text(portable_text(json.dumps(result,indent=2)+'\n'),encoding='utf8')
    print(json.dumps({s:{k:v for k,v in r.items() if k!='extended_records'} for s,r in result.items()}))

if __name__=='__main__':main()
