"""All published mock-run website/social/job claims with exact saved proof."""
from signalpost.portable_paths import portable, portable_text  # saved paths stay repo-relative
import hashlib,json
from collections import Counter
from pathlib import Path
from signalpost.sources.excerpt import pointer_bounds
ROOT=Path(__file__).resolve().parents[3]
DEST=ROOT/'reports/r5/release-v4b'
OUT=ROOT/'.data/release-v4b/daily'

def main():
    records=[]
    for row in map(json.loads,(OUT/'envelopes.jsonl').read_text(encoding='utf8').splitlines()):
        org=row['organisation_number'];name=next((c['value'] for c in row['claims'] if c['field']=='identity.legal_name' and c['availability']=='available'),org)
        evidence={e['id']:e for e in row['evidence']}
        for claim in row['claims']:
            if claim['availability']!='available':continue
            field,value=claim['field'],claim['value'];kind=tier=url=prefix=None
            if field=='official_website':kind='Ownership-verified website';tier=value['identity_level'];url=value['final_url'];prefix='identity-proof:'
            elif field.startswith('social_profile.'):kind='Ownership-verified social URL';tier=value['proof_tier'];url=value['url'];prefix='company-link:'
            elif field.startswith('hiring.job.'):
                kind='Current job';url=value['url'];tier='EXACT_NAV_EMPLOYER_OR_PROVEN_SUBUNIT' if value.get('source')!='verified_site_careers' else 'VERIFIED_SITE_OWN_LINK_CURRENT_POSTING'
            elif field.startswith('registry_social.'):kind='Registry social assertion';tier='REGISTRY_ASSERTED_ONLY';url=value['url']
            elif field=='identity.registered_website' or (field.startswith('subunits.detail.') and field.endswith('.registered_website')):
                kind='Registry homepage assertion';tier='REGISTRY_FIELD_ONLY';url=str(value)
            if kind is None:continue
            receipts=[evidence[eid] for eid in claim['evidence_ids']]
            primary=next(e for e in receipts if e['locator'].startswith(prefix)) if prefix else receipts[0]
            proof_receipts=[]
            for receipt in receipts:
                if receipt['id']!=primary['id'] and kind.startswith('Registry'):continue
                body=(OUT/'state/blobs'/receipt['content_sha256']).read_bytes()
                assert hashlib.sha256(body).hexdigest()==receipt['content_sha256']
                raw=body.decode('utf8',errors='replace');assert receipt['claim_span'] in raw
                item={k:receipt[k] for k in ('source_url','retrieved_at','content_sha256','locator','extraction_method')}
                item['exact_excerpts']=[receipt['claim_span']]
                if kind=='Current job' and receipt['extraction_method']=='signalpost.nav.v1' and receipt['locator']=='/ad_content':
                    # Only factual title/date/employer scalar spans: do not
                    # publish surrounding contact-person or description text.
                    item['exact_excerpts']=[]
                    for key in ('uuid','title','published','expires','employer/orgnr'):
                        bounds=pointer_bounds(raw,'/ad_content/'+key)
                        assert bounds is not None
                        item['exact_excerpts'].append(raw[bounds[0]:bounds[1]])
                proof_receipts.append(item)
            records.append({'organisation_number':org,'name':name,'kind':kind,'url':url,'proof_tier':tier,
                'claim_id':claim['id'],'field':field,'title':value.get('title') if isinstance(value,dict) else None,
                'published':value.get('published') if isinstance(value,dict) else None,'deadline':value.get('expires') if isinstance(value,dict) else None,
                'proof_receipts':proof_receipts})
    records.sort(key=lambda r:(r['kind'],r['organisation_number'],r['url'],r['field']))
    text='''# v1.3.0 / release-v4b URL and job hand-check inventory

New seed-20261114 sample, disjoint from both prior 100-company samples. Every published website/social/job claim is listed. Registry homepage/social assertions are separate and do not establish website ownership. Job publication requires current exact NAV employer/proven subunit or a current verified-site own posting link. Exact spans, source URL, retrieval time, SHA-256 and locator are retained; historical proof is never substituted. All receipts passed the independent verifier.

'''
    counts=Counter(r['kind'] for r in records)
    for kind in sorted(counts):
        text+='## '+kind+' ('+str(counts[kind])+')\n\n'
        for r in (r for r in records if r['kind']==kind):
            text+='### '+r['organisation_number']+' - '+r['name']+'\n\n'
            for key in ('url','proof_tier','field','title','published','deadline'):
                if r[key] is not None:text+='- '+key+': `'+str(r[key])+'`\n'
            text+='\n'
            for receipt in r['proof_receipts']:
                text+='Source: '+receipt['source_url']+'\n\nRetrieved: '+receipt['retrieved_at']+'; SHA-256 `'+receipt['content_sha256']+'`; locator `'+receipt['locator']+'`; method `'+receipt['extraction_method']+'`.\n\n'
                for span in receipt['exact_excerpts']:
                    text+='<pre>'+span.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')+'</pre>\n\n'
    if not records:text+='No website/social/job claims published.\n'
    (DEST/'urls.md').write_text(portable_text(text.rstrip()+'\n'),encoding='utf8',newline='\n')
    result={'output':str(OUT/'envelopes.jsonl'),'output_sha256':hashlib.sha256((OUT/'envelopes.jsonl').read_bytes()).hexdigest(),
        'count_by_kind':dict(counts),'records':records}
    (DEST/'urls.json').write_text(portable_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n'),encoding='utf8')
    print(json.dumps(dict(counts)))

if __name__=='__main__':main()
