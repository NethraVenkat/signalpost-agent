"""Self-descriptions from already fetched pages of an accepted website."""
import html
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
        # Exclude legal / terms / privacy / cookies pages from description extraction
        url_path = urlsplit(response.url).path.lower()
        if re.search(r'(?:vilkar|vilk[aå]r|betingelser|terms|privacy|personvern|cookie)', url_path):
            continue

        candidates=[]
        for key,kind in [('description','meta_description'),('og:description','og_description')]:
            text=page.meta.get(key)
            if text:
                text = html.unescape(text).strip()
                # Exclude short navigation or form titles e.g. "Kontakt Oss Spørreskjema", "Hjemmeside"
                if len(text) < 30 or len(text.split()) < 4:
                    continue
                if re.match(r'^(?:kontakt\s+oss|spørreskjema|hjemmeside|forside|om\s+oss|formelle\s+vilk[aå]r|vilk[aå]r)\b', text, re.I):
                    continue
                # Exact source-tag span; HTML attribute decoding is extraction.
                match=next((m for m in re.finditer(r'<meta\b[^>]*>',page.raw,re.I|re.S)
                            if re.search(r'(?:name|property)\s*=\s*[\'\"]'+re.escape(key)+r'[\'\"]',m.group(),re.I)),None)
                if match:candidates.append((kind,text,match.group()[:300],'meta:'+key+'@content'))

        if re.search(r'(?:^|/)(?:om[-_]?oss|om|about)(?:[/-]|$)', url_path) and page.paragraphs:
            # Find the first paragraph that is genuine descriptive prose
            for p_text, p_span in page.paragraphs:
                cleaned = p_text.strip()
                words = cleaned.split()
                # Must be descriptive prose: >= 40 chars, >= 6 words
                if len(cleaned) < 40 or len(words) < 6:
                    continue
                # Exclude paragraphs that look like address blocks (e.g. "Lasta 50\r\n4405 Flekkefjord")
                if re.search(r'\b\d{4}\b\s+[A-ZÆØÅa-zæøå]+', cleaned) and any(char.isdigit() for char in words[0]):
                    continue
                # Exclude contact prefix blocks
                if re.match(r'^(?:telefon|tlf|tlf\.|phone|mobil|kontakt)\s*:', cleaned, re.I):
                    continue
                if '\ufffd' in cleaned:
                    continue
                candidates.append(('about_paragraph', cleaned, p_span, 'visible:p:first'))
                break

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
