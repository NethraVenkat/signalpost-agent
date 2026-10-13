"""Self-descriptions from already fetched pages of an accepted website."""
import re
from urllib.parse import urlsplit
from ..models.evidence import digest
from ..sources.extract import Source,add


LEVELS={'VERIFIED','HIGH','REGISTRY_DECLARED'}


def extract(section,org,proof_claim,pages):
    if proof_claim.availability!='available' or proof_claim.value.get('identity_level') not in LEVELS:
        return
    seen=set()
    for response,page in pages:
        candidates=[]
        for key,kind in [('description','meta_description'),('og:description','og_description')]:
            text=page.meta.get(key)
            if text:
                # Exact source-tag span; HTML attribute decoding is extraction.
                match=next((m for m in re.finditer(r'<meta\b[^>]*>',page.raw,re.I|re.S)
                            if re.search(r'(?:name|property)\s*=\s*[\'\"]'+re.escape(key)+r'[\'\"]',m.group(),re.I)),None)
                if match:candidates.append((kind,text,match.group()[:300],'meta:'+key+'@content'))
        if re.search(r'(?:^|/)(?:om[-_]?oss|om|about)(?:[/-]|$)',urlsplit(response.url).path,re.I) and page.paragraphs:
            text,span=page.paragraphs[0]
            candidates.append(('about_paragraph',text,span,'visible:p:first'))
        for kind,text,span,locator in candidates:
            text=text.strip()[:300]
            if len(text)<20 or '\ufffd' in text or (kind,text) in seen:continue
            seen.add((kind,text))
            value={'text':text,'kind':kind,'self_description':True,
                   'identity_level':proof_claim.value['identity_level'],'identity_claim_id':proof_claim.id}
            add(section,Source(response.url,response.body,response.sha,response.retrieved_at),org,'website',
                'website_description.'+kind+'.'+digest(response.url)[:16],value,locator,
                span=span,source_class='company_owned',method='signalpost.website_description.v1')
            section.claims[-1].evidence_ids=list(dict.fromkeys(section.claims[-1].evidence_ids+proof_claim.evidence_ids))
