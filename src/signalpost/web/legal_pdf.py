"""Bounded text receipts from linked own-site PDF terms; exact ID only."""
import io,html,hashlib,json,re
from types import SimpleNamespace
from .html import Page
from ..budget import SourceFailure

METHOD='signalpost.legal_pdf.v1'
MAX_BYTES=2*1024*1024
MAX_PAGES=20
MAX_TEXT=200_000


def extract_pages(body):
    from pypdf import apply_configuration
    limit=8*1024*1024
    with apply_configuration(maximum_declared_stream_length=limit,array_based_stream_maximum_output_length=limit,
            jbig2_maximum_output_length=limit,lzw_maximum_output_length=limit,run_length_maximum_output_length=limit,
            zlib_maximum_output_length=limit,brotli_maximum_output_length=limit,image_maximum_buffer_size=limit,
            stream_decoding_work_maximum_length=16*1024*1024,stream_parsing_work_maximum_count=100_000,
            page_tree_maximum_entries=200,page_tree_maximum_page_entries=200,xform_maximum_invocations_per_extraction=100):
        return _extract_pages(body)


def _extract_pages(body):
    if len(body)>MAX_BYTES:raise SourceFailure('pdf_body_cap')
    if not body.startswith(b'%PDF-'):raise SourceFailure('pdf_signature')
    from pypdf import PdfReader
    try:
        reader=PdfReader(io.BytesIO(body),strict=True)
        if reader.is_encrypted:raise SourceFailure('pdf_encrypted')
        if len(reader.pages)>MAX_PAGES:raise SourceFailure('pdf_page_cap')
        result=[];total=0
        for number,page in enumerate(reader.pages,1):
            content=page.get_contents()
            if content and len(content.get_data())>8*1024*1024:raise SourceFailure('pdf_stream_cap')
            text=(page.extract_text() or '').replace(chr(0),'')
            total+=len(text)
            if total>MAX_TEXT:raise SourceFailure('pdf_text_cap')
            result.append((number,text))
        return result
    except SourceFailure:raise
    except Exception as exc:raise SourceFailure('pdf_unreadable') from exc


def render_text(text):
    # Derived text is explicitly labelled; it is not claimed to be original HTML.
    return ('<html><head><title>Extracted legal PDF text</title></head><body><footer>'+html.escape(text,quote=False)+'</footer></body></html>').encode('utf8')


def prove(response,org,context,candidate,leaders,link):
    from .collector import candidate_proof
    pages=extract_pages(response.body)
    alltext='\n'.join(text for _,text in pages)
    from .publisher_veto import conflict
    if conflict(Page(render_text(alltext),response.url),org,context)[0]:raise SourceFailure('pdf_publisher_conflict')
    for number,text in pages:
        raw=render_text(text);page=Page(raw,response.url)
        proof=candidate_proof(page,org,context,candidate,leaders)
        if proof.level!='VERIFIED':continue
        receipt={'raw_pdf_sha256':response.sha,'page_number':number,'page_text_sha256':hashlib.sha256(text.encode('utf8')).hexdigest(),
            'derived_html_sha256':hashlib.sha256(raw).hexdigest(),'pdf_url':response.url,'linked_from':link,
            'extractor':'pypdf','method':METHOD}
        derived=SimpleNamespace(body=raw,url=response.url,sha=receipt['derived_html_sha256'],retrieved_at=response.retrieved_at,pdf_receipt=receipt)
        return derived,page,proof
    return None


def attach(section,claim,response):
    from ..models.evidence import Evidence,digest
    receipt=response.pdf_receipt
    raw=Evidence(id=digest([receipt['pdf_url'],receipt['raw_pdf_sha256'],'pdf:original',METHOD]),source_url=receipt['pdf_url'],
        content_sha256=receipt['raw_pdf_sha256'],retrieved_at=response.retrieved_at,source_class='company_owned',
        claim_span='%PDF-',locator='pdf:original',extraction_method=METHOD,source_identifier=json.dumps(receipt,ensure_ascii=False,sort_keys=True))
    link=receipt['linked_from']
    parent=Evidence(id=digest([link['source_url'],link['content_sha256'],'legal-pdf-link:'+receipt['pdf_url'],METHOD]),
        source_url=link['source_url'],content_sha256=link['content_sha256'],retrieved_at=link['retrieved_at'],source_class='company_owned',
        claim_span=link['claim_span'],locator='legal-pdf-link:'+receipt['pdf_url'],extraction_method=METHOD)
    section.evidence.extend([raw,parent]);claim.evidence_ids.extend([raw.id,parent.id])
