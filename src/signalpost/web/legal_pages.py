"""Own-site legal-page nominations; never an identity acceptance rule."""
import re
from urllib.parse import urlsplit,unquote
from .policy import domain,normalize_url

LEGAL=re.compile(r'salgsbetingelser|kj.psbetingelser|kj.psvilk.r|handelsbetingelser|vilk.r|betingelser|personvern|personvernerkl.ring|cookies|angrerett|impressum|juridisk|om[-_ ]nettstedet|terms|privacy|conditions',re.I)
FIXED=('/salgsbetingelser','/kjopsbetingelser','/vilkar','/personvern','/personvernerklaering','/terms','/privacy','/impressum')

def is_legal(value):return bool(LEGAL.search(unquote(str(value))))

def legal_links(page,*,pdf=False):
    result=[]
    for link in page.links:
        if not link.visible_context:continue
        url=normalize_url(link.href)
        if not url or domain(url)!=domain(page.url):continue
        if not (link.owned_context or is_legal(urlsplit(page.url).path)):continue
        if not is_legal(unquote(urlsplit(url).path)+' '+link.text):continue
        is_pdf=bool(re.search(r'\.pdf$',urlsplit(url).path,re.I))
        if is_pdf!=pdf:continue
        if not pdf and re.search(r'\.(?:docx?|xlsx?|zip|jpe?g|png)$',urlsplit(url).path,re.I):continue
        if url not in result:result.append(url)
    return result


def pdf_receipts(response,page):
    targets=set(legal_links(page,pdf=True))
    return {url:{'source_url':response.url,'content_sha256':response.sha,'retrieved_at':response.retrieved_at,
                 'claim_span':next(link.span for link in page.links if normalize_url(link.href)==url and link.visible_context)}
            for url in targets}
