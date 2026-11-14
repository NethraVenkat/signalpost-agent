"""Read-only full publisher review packet for every added measured website."""
import json,hashlib,sys,re
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
from signalpost.web.html import Page
from signalpost.web.publisher import extract_publisher
from scripts.accuracy_audit import extract_org_context_and_leaders

ROOT=Path.cwd()

def main():
    stage=sys.argv[1];seed=int(sys.argv[2]);base=ROOT/f'reports/r5/stage{stage}/{stage}/seed{seed}'
    settings=json.loads((base/'settings.json').read_text(encoding='utf8'));work=Path(settings['working_directory'])
    counts=json.loads((base/'counts.json').read_text(encoding='utf8'));rows={r['organisation_number']:r for r in map(json.loads,(work/'envelopes.jsonl').read_text(encoding='utf8').splitlines())}
    items=[]
    for item in counts['changes']['added']:
        if item['kind'] not in {'website','social'}:continue
        row=rows[item['orgnr']];context,_=extract_org_context_and_leaders(row['claims']);pages=[]
        for e in item['evidence']:
            if e['source_class']!='company_owned':continue
            raw=(work/'state/blobs'/e['content_sha256']).read_bytes();assert hashlib.sha256(raw).hexdigest()==e['content_sha256']
            p=Page(raw,e['source_url'])
            page={'url':p.url,'sha256':e['content_sha256'],'title':p.title,'publisher':[(f.location,f.text) for f in extract_publisher(p).fragments],
                'visible_context':p.visible[:16000],'exact_receipt_excerpt':e['claim_span']}
            if not any(x['url']==page['url'] and x['sha256']==page['sha256'] for x in pages):pages.append(page)
        items.append({'orgnr':item['orgnr'],'name':item['legal_name'],'kind':item['kind'],'url':item['identity'],'value':item['value'],'registry_context':context,'pages':pages,'review_status':'pending_saved_publisher_review'})
    (base/'publisher_review.json').write_text(json.dumps({'seed':seed,'items':items,'method':'Full saved publisher context for assistant inspection; no network or human-verdict claim'},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    for i in items:
        print(json.dumps({**i,'pages':[{**p,'visible_context':re.sub(r'\s+',' ',p['visible_context'])} for p in i['pages']]},ensure_ascii=True))

if __name__=='__main__':main()
