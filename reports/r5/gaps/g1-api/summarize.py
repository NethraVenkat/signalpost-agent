"""Summarize qualifier-level counts without making network requests."""
from collections import Counter
import hashlib
import json
from pathlib import Path
from signalpost.portable_paths import portable_text

ROOT=Path(__file__).resolve().parents[4]
DEST=Path(__file__).resolve().parent
WORK=ROOT/'out/g1-api-standard100-normal-network'


def main():
    rows=[json.loads(line) for line in (WORK/'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
    report=json.loads((WORK/'report.json').read_text(encoding='utf8'))
    counts=json.loads((DEST/'standard100-counts.json').read_text(encoding='utf8'))
    assert json.loads((DEST/'standard100-check-execution.json').read_text())['exit_code']==0
    types={key:{'companies':[],'claims':0} for key in ('signature_registered_rule','signature_possible_combination','prokura_registered_rule','prokura_possible_combination','group_parent','group_subsidiary')}
    for row in rows:
        claims=[c for c in row['claims'] if c['availability']=='available']
        for kind in types:
            family,detail=kind.split('_',1)
            prefix=family+('.rule' if detail=='registered_rule' else '.combination.' if detail=='possible_combination' else '.'+detail+'.')
            matched=[c for c in claims if c['field'].startswith(prefix)]
            if matched:types[kind]['companies'].append(row['organisation_number'])
            types[kind]['claims']+=len(matched)
    for value in types.values():value['companies_covered']=len(value['companies'])
    requests=[e for e in report['request_log'] if '/fullmakt/enheter/' in e['url'] or '/api/konsernstruktur/' in e['url']]
    corporate=sum(counts['current'][k]['claims'] for k in ('signature','prokura','group'))
    difference=counts['current']['total']['claims']-counts['baseline']['total']['claims']
    result={'types':types,'corporate_claims':corporate,'available_claim_delta':difference,'other_available_claim_delta':difference-corporate,
            'corporate_request_attempts':len(requests),'corporate_http_statuses':dict(Counter(str(e.get('status')) for e in requests)),
            'successful_live_http_responses':sum(isinstance(e.get('status'),int) and 200<=e['status']<300 for e in report['request_log']),
            'corporate_section_errors':{family:dict(Counter(e['code'] for row in rows for e in row['errors'] if e['section']==family)) for family in ('signature','prokura','group')},
            'warnings':report['warnings'],'output_sha256':{name:hashlib.sha256((WORK/name).read_bytes()).hexdigest() for name in ('envelopes.jsonl','profiles.jsonl','report.json')},
            'corporate_source_replay':'Every available corporate claim passed brreg_corporate.verify inside check_live_run; see code at measured commit and checker exit 0.',
            'baseline_scope':'Prior measured standard100 at f740933, retained by ac88ab0; no new live baseline measurement.'}
    (DEST/'standard100-details.json').write_text(portable_text(json.dumps(result,ensure_ascii=False,indent=2))+'\n',encoding='utf8',newline='\n')
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':
    main()
