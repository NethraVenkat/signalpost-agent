"""Diagnose saved missing-site outcomes; never fetch or relax proof."""
import json,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
CAUSES=('no candidate','DNS fail','timeout','robots','fetched-no-proof','veto','budget','ambiguous')

def classify(row,requests):
    attempts=[]
    for error in row['errors']:
        if error['code']=='website_candidates':attempts.extend(json.loads(error['message']))
    reasons={a.get('reason','') for a in attempts}
    signals=set()
    if not attempts:signals.add('no candidate')
    if reasons & {'no_such_domain','dns_unavailable','dns_timeout','dns_error'}:signals.add('DNS fail')
    if reasons & {'website_timeout','website_connect_error','website_http_5xx'}:signals.add('timeout')
    if reasons & {'robots','robots_unavailable','http_blocked','block_page'}:signals.add('robots')
    if any(a.get('level') in {'LOW','MEDIUM','HIGH','REGISTRY_DECLARED'} and a.get('reason') in {'corroboration','short_or_js_shell','registry_contact_missing','foreign_orgnr'} for a in attempts):signals.add('fetched-no-proof')
    if any(a.get('level')=='REJECT' or a.get('reason') in {'ssrf','url_refused'} for a in attempts):signals.add('veto')
    if reasons & {'website_budget_exhausted','budget_exhausted','deadline','dns_budget_exhausted'} or any(e['section']=='website' and e['code'] in {'website_budget_exhausted','dns_budget_exhausted','budget_exhausted','deadline'} for e in row['errors']):signals.add('budget')
    if row['run']['sections']['website']=='ambiguous':signals.add('ambiguous')
    # Terminal cutoff/ambiguity first; table of overlapping signals also exposes
    # the DNS and fetched-page work hidden by a later cutoff.
    priority=('no candidate','ambiguous','budget','robots','fetched-no-proof','veto','timeout','DNS fail')
    primary=next((c for c in priority if c in signals),'fetched-no-proof')
    name=next(c['value'] for c in row['claims'] if c['field']=='identity.legal_name' and c['availability']=='available')
    return {'orgnr':row['organisation_number'],'name':name,'state':row['run']['sections']['website'],
            'primary':primary,'signals':sorted(signals),'reasons':dict(Counter(a.get('reason','status:'+str(a.get('status'))) for a in attempts)),
            'attempts':attempts,'website_http':[e for e in requests if e['organisation_number']==row['organisation_number'] and e.get('section')=='website']}

def main():
    stage=sys.argv[1] if len(sys.argv)>1 else 'F1';result={}
    text='# Missing-website diagnosis before Stage C\n\nSource: Stage '+stage+' saved runs. No network calls. Primary buckets are exclusive; signal counts overlap. Budget/ambiguity are terminal outcomes and can mask underlying DNS/no-proof failures. Robots includes access challenges; timeout includes connect/5xx. A veto is preserved, not a candidate for weaker proof.\n\n'
    for sample in ('frozen','daily'):
        settings=json.loads((ROOT/'reports/r5'/('stage'+stage)/sample/'settings.json').read_text(encoding='utf8'));out=Path(settings['working_directory'])
        rows=[json.loads(x) for x in (out/'envelopes.jsonl').read_text(encoding='utf8').splitlines()];report=json.loads((out/'report.json').read_text(encoding='utf8'))
        missing=[classify(row,report['request_log']) for row in rows if not any(c['field']=='official_website' and c['availability']=='available' for c in row['claims'])]
        primary=Counter(m['primary'] for m in missing);signals=Counter(s for m in missing for s in m['signals'])
        result[sample]={'missing':len(missing),'primary':dict(primary),'signals':dict(signals),'companies':missing}
        text+='## '+sample+'\n\n| Cause | Primary companies | Companies with signal |\n|---|---:|---:|\n'
        for cause in CAUSES:text+=f'| {cause} | {primary[cause]} | {signals[cause]} |\n'
        text+='\n| Org number | Company | Primary | Signals |\n|---|---|---|---|\n'
        for m in missing:text+='| '+m['orgnr']+' | '+m['name'].replace('|','/')+' | '+m['primary']+' | '+', '.join(m['signals'])+' |\n'
        text+='\n'
    text+='## Action boundary\n\nDNS NXDOMAIN, upstream timeouts and robots denials are external outcomes; no proof rule or access refusal is bypassed. Investigate budget ordering and fetched-no-proof discovery: own-page links should precede blind guessed paths, and the requested bounded own-sitemap discovery should expose contact/privacy paths absent from navigation. Challenge pages should stop proof walks rather than consume guess-page slots. Per-company attempt/request receipts are retained in diagnosis.json.\n'
    dest=ROOT/'reports/r5/stageC';dest.mkdir(parents=True,exist_ok=True)
    name='diagnosis_after' if stage=='C' else 'diagnosis'
    if stage=='C':text=text.replace('diagnosis before Stage C','diagnosis after Stage C')
    (dest/(name+'.md')).write_text(text,encoding='utf8');(dest/(name+'.json')).write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    print(json.dumps({s:{k:v for k,v in data.items() if k!='companies'} for s,data in result.items()}))

if __name__=='__main__':main()
