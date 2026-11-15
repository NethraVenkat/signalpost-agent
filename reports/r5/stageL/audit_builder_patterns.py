"""Supplemental offline audit of all nine-digit builder patterns, including foreign IDs."""
import hashlib,json,re,sys
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from signalpost.identity.orgnr import valid
from signalpost.sources.text import decode_body
BUILDERS={'wix':r'wixBiSession|warmupData|viewerModel|wix-warmup-data','squarespace':r'SQUARESPACE_CONTEXT|Static\.SQUARESPACE_CONTEXT','next':r'__NEXT_DATA__','nuxt':r'__NUXT__|__NUXT_DATA__'}
def main():
    counts=Counter();items=[];seen=set()
    for seed in (20261017,20261113,20261114,20261115,20261116,20261117):
        base=ROOT/f'reports/r5/stageR7/R7/seed{seed}';work=Path(json.loads((base/'settings.json').read_text(encoding='utf8'))['working_directory'])
        rows={r['organisation_number']:r for r in map(json.loads,(work/'envelopes.jsonl').read_text(encoding='utf8').splitlines())}
        for e in json.loads((base/'report.json').read_text(encoding='utf8'))['request_log']:
            row=rows.get(e['organisation_number'])
            if not row or e.get('section')!='website' or e.get('status')!=200 or not e.get('content_sha256'):continue
            if any(c['field']=='official_website' and c['availability']=='available' for c in row['claims']):continue
            key=(seed,e['organisation_number'],e['content_sha256'])
            if key in seen:continue
            seen.add(key);raw=(work/'state/blobs'/e['content_sha256']).read_bytes();assert hashlib.sha256(raw).hexdigest()==e['content_sha256']
            text=decode_body(raw)
            for script in re.finditer(r'<script\b[^>]*>.*?</script\s*>',text,re.I|re.S):
                for builder,marker in BUILDERS.items():
                    if not re.search(marker,script.group(),re.I):continue
                    counts[builder+'_scripts']+=1;patterns=[]
                    for m in re.finditer(r'(?<![0-9])(?:[0-9][ .\u00a0]*){9}(?![0-9])',script.group()):
                        number=re.sub(r'\D','',m.group());excerpt=script.group()[max(0,m.start()-80):m.end()+80]
                        labelled=bool(re.search(r'org(?:anisasjons)?[ ._\\-]*(?:nr|nummer)|vat(?:ID)?|MVA',excerpt,re.I))
                        patterns.append({'number':number,'checksum_valid':valid(number),'label_nearby':labelled,'exact_target':number==row['organisation_number'],'excerpt':excerpt[:300]})
                    counts[builder+'_nine_digit_patterns']+=len(patterns)
                    counts[builder+'_valid_patterns']+=sum(p['checksum_valid'] for p in patterns)
                    counts[builder+'_labelled_valid_patterns']+=sum(p['checksum_valid'] and p['label_nearby'] for p in patterns)
                    if patterns:items.append({'seed':seed,'orgnr':row['organisation_number'],'url':e['url'],'body_sha256':e['content_sha256'],'builder':builder,'script_sha256':hashlib.sha256(script.group().encode()).hexdigest(),'patterns':patterns})
    result={'network_requests':0,'method':'All marker-bearing scripts from saved R7 unproved responses; raw 9-digit patterns are candidates, not identity proof. Checksum and nearby orgnr/VAT labels reported separately.','counts':dict(counts),'items':items}
    (ROOT/'reports/r5/stageL/builder_patterns.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(dict(counts)))
if __name__=='__main__':main()
