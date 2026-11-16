"""Report actual legal-work cost and source failures without inferred gains."""
from signalpost.portable_paths import portable, portable_text  # saved paths stay repo-relative
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
DEST=Path(__file__).resolve().parent
SEEDS=(20261017,20261113,20261114,20261115,20261116,20261117)

def main():
    rows=[]
    for seed in SEEDS:
        base=DEST/'L'/f'seed{seed}'
        if not (base/'report.json').exists():continue
        report=json.loads((base/'report.json').read_text(encoding='utf8'))
        rows.append({'seed':seed,'legal_priority':report['adaptive_websites']['pass2']['legal_priority'],
            'pass1':report['adaptive_websites']['pass1'],'pass2':{k:v for k,v in report['adaptive_websites']['pass2'].items() if k!='per_company'},
            'official_failed_attempts':[{'url':e['url'],'orgnr':e['organisation_number'],'status':e.get('status'),'error':e.get('error')} for e in report['request_log']
                if e['host'] in {'data.brreg.no','pam-stilling-feed.nav.no','api.gleif.org'} and (e.get('error') or (e.get('status') or 0)>=500)]})
    data={'samples':rows,'legal_totals':{k:sum(r['legal_priority'][k] for r in rows) for k in ('resumes','requests','websites_gained')}}
    (DEST/'legal_work.json').write_text(portable_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n'),encoding='utf8')
    print(json.dumps(data,ensure_ascii=True))
if __name__=='__main__':main()
