"""Saved-run inventories and extra hiring/accounts metrics; no network calls."""
from signalpost.portable_paths import expand, portable, portable_text  # saved paths stay repo-relative
import json,sys
from pathlib import Path
from signalpost.sources.excerpt import pointer_bounds

ROOT=Path(__file__).resolve().parents[2]

def main():
    stage=sys.argv[1];assert stage in {'D','I'}
    lines=['# Stage '+stage+' published jobs','',
           'Every available job in both independent samples. Excerpts below are verbatim saved-source substrings; no employer-name matching.','']
    metrics={}
    for sample in ('frozen','daily'):
        directory=ROOT/'reports/r5'/('stage'+stage)/sample
        settings=json.loads((directory/'settings.json').read_text(encoding='utf8'))
        out=Path(expand(settings['working_directory']));rows=[json.loads(x) for x in (out/'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
        jobs=[];years=0;yoy=0;accounts=0;careers={};hiring={};filed=0;year_facts=0;unscaled=0;flags=0
        for row in rows:
            available=[c for c in row['claims'] if c['availability']=='available']
            evidence={e['id']:e for e in row['evidence']}
            name=next((c['value'] for c in available if c['field']=='identity.legal_name'),'Unknown')
            periods={c['reporting_period']['period_end'] for c in available if c['family']=='accounts' and c.get('reporting_period') and c['reporting_period'].get('period_end')}
            years+=len(periods)>=2
            accounts+=sum(c['family']=='accounts' for c in available)
            filed+=any(c['field']=='accounts.filed_years' and isinstance(c['value'],list) and len(c['value'])>=2 for c in available)
            year_facts+=sum(c['field'].startswith('accounts.filed_year') for c in available)
            unscaled+=sum(bool(c['family']=='accounts' and c.get('reporting_period') and c['reporting_period'].get('unit') is None) for c in available)
            flags+=bool(((row['run'].get('synthesis') or {}).get('financial_year_check') or {}).get('newer_filing_exists'))
            yoy+=sum(m['formula']=='revenue_yoy' for m in (row['run'].get('synthesis') or {}).get('financial_metrics',[]))
            status=row['run']['sections'].get('hiring','disabled');hiring[status]=hiring.get(status,0)+1
            state=row['run'].get('refresh',{}).get('careers',{}).get('reason','not_checked');careers[state]=careers.get(state,0)+1
            for claim in available:
                if not claim['field'].startswith('hiring.job.'):continue
                value=claim['value'];jobs.append((row['organisation_number'],name,value['url']))
                lines.extend(['## '+sample+' — '+row['organisation_number']+' — '+name,'',
                    '- URL: '+value['url'],'- Title: '+value['title'],
                    '- Published: '+str(value.get('published'))+'; deadline: '+str(value.get('expires')),
                    '- Proof: '+('exact NAV employer number / proven subunit' if value.get('source')!='verified_site_careers' else 'current VERIFIED website own navigation → posting'), ''])
                for eid in claim['evidence_ids']:
                    e=evidence[eid];body=(out/'state/blobs'/e['content_sha256']).read_bytes()
                    spans=[e['claim_span']]
                    if e['extraction_method']=='signalpost.nav.v1' and e['locator']=='/ad_content':
                        raw=body.decode('utf8')
                        for key in ('title','published','expires','employer/orgnr'):
                            start,end=pointer_bounds(raw,'/ad_content/'+key)
                            spans.append(raw[start:end])
                    lines.extend(['Source: '+e['source_url'],'',
                        'Retrieved: '+e['retrieved_at']+'; SHA-256: `'+e['content_sha256']+'`; locator: `'+e['locator']+'`',''])
                    for span in dict.fromkeys(spans):
                        assert span and span in body.decode('utf8',errors='replace')
                        lines.extend(['<pre>'+span.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')+'</pre>',''])
        report=json.loads((out/'report.json').read_text(encoding='utf8'))
        metrics[sample]={'job_claims':len(jobs),'job_ad_companies':len({o for o,n,u in jobs}),
            'accounts_facts':accounts,'companies_with_two_figure_periods':years,'yoy_sentences':yoy,
            'companies_with_two_filed_years':filed,'filed_year_facts':year_facts,'figures_with_undeclared_unit':unscaled,'newer_filing_flags':flags,
            'hiring_states':hiring,'careers_reasons':careers,'http_requests':report['requests'],
            'runtime_seconds':report['runtime_seconds'] if 'runtime_seconds' in report else json.loads((directory/'counts.json').read_text())['metrics']['runtime_seconds']}
    destination=ROOT/'reports/r5'/('stage'+stage)
    (destination/'jobs.md').write_text(portable_text('\n'.join(lines).rstrip()+'\n'),encoding='utf8',newline='\n')
    (destination/'extra_metrics.json').write_text(portable_text(json.dumps(metrics,indent=2)+'\n'),encoding='utf8')
    print(json.dumps(metrics))

if __name__=='__main__':main()
