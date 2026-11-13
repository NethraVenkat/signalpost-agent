"""Audit saved D/I defaults, meters, unit provenance and filing-year access."""
import hashlib,json
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[3]

def main():
    result={}
    for stage in ('D','I'):
        for sample in ('frozen','daily'):
            settings=json.loads((ROOT/'reports/r5'/('stage'+stage)/sample/'settings.json').read_text(encoding='utf8'))
            out=Path(settings['working_directory']);report=json.loads((out/'report.json').read_text(encoding='utf8'))
            rows=[json.loads(x) for x in (out/'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
            flags=[x for x in settings['command_argv'] if x.startswith('--')]
            assert flags==['--organisations','--bulk','--output','--profiles-output','--report','--run-id','--expected-count']
            assert settings['resolved_config']['website_request_cap']==8 and settings['resolved_config']['website_total_request_cap']==13
            assert all(report['enrichment'].values())
            assert len(rows)==100 and len({r['organisation_number'] for r in rows})==100
            assert report['requests']<=1850 and report['total_cost_usd']==0
            assert report['site']['state']=='available' and report['site']['companies']==100
            assert report['completion']['within_effective_time_budget'] and report['completion']['within_requested_time_budget']
            assert all(r['state']=='complete' for r in rows)
            assert report['hiring_prefetch']['source_mode']=='declared_index'
            assert not any(r['run']['sections']['hiring']=='failed' for r in rows)
            requests=report['request_log']
            web=Counter(e['organisation_number'] for e in requests if e.get('section')=='website')
            assert max(web.values(),default=0)<=13
            if stage=='I':
                manifest=json.loads((ROOT/'reports/r5/stageI'/sample/'source_manifest.json').read_text(encoding='utf8'))
                assert all(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha for name,sha in manifest.items()),'Measured source differs from final source'
                for row in rows:
                    for claim in row['claims']:
                        if claim['family']=='accounts' and claim['availability']=='available' and claim.get('reporting_period'):
                            assert 'unit_basis' not in claim['reporting_period']
            years=[e for e in requests if '/aarsregnskap/kopi/' in e['url']]
            max_page=max(p.stat().st_size for p in (out/'site/c').glob('*.html'))
            assert max_page<250_000
            result[stage+' '+sample]={'requests':report['requests'],'year_http_statuses':dict(Counter(str(e.get('status',e.get('error'))) for e in years)),
                'year_request_count':len(years),'year_rate_limits':sum(e.get('status')==429 for e in years),
                'website_request_maximum':max(web.values(),default=0),'largest_profile_bytes':max_page,
                'available_year_lists':sum(any(c['field']=='accounts.filed_years' and c['availability']=='available' for c in row['claims']) for row in rows),
                'complete':len(rows),'cost_usd':0,'output_sha256':hashlib.sha256((out/'envelopes.jsonl').read_bytes()).hexdigest()}
    (ROOT/'reports/r5/stageI/release_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    print(json.dumps(result))

if __name__=='__main__':main()
