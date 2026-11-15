"""Rebuild PDF text proof and original own legal-link chain from saved bytes."""
import hashlib,json
from urllib.parse import urlsplit
from signalpost.web.legal_pdf import extract_pages,render_text,METHOD,MAX_BYTES
from signalpost.web.legal_pages import pdf_receipts
from signalpost.web.html import Page
from signalpost.web.policy import domain
from signalpost.web.publisher_veto import conflict
from signalpost.web.collector import candidate_proof
from signalpost.web.candidates import Candidate
from types import SimpleNamespace
from scripts.verify_publisher_identity import registry_context


def verify(org,data,evidence,stored_body,read_blob):
    count=0
    for c in data['claims']:
        if c['field']!='official_website' or c['availability']!='available' or not c['value'].get('pdf_proof'):continue
        value=c['value'];receipt=value['pdf_proof']
        assert value['identity_level']=='VERIFIED' and value['proof_type'] in {'orgnr_on_page','jsonld_vatid'}
        assert receipt['method']==METHOD and receipt['extractor']=='pypdf'
        assert type(receipt['page_number']) is int and receipt['page_number']>0
        assert domain(receipt['pdf_url'])==domain(value['final_url']) and value['proof_page_url']==receipt['pdf_url']
        raw=read_blob(receipt['raw_pdf_sha256']);assert len(raw)<=MAX_BYTES and hashlib.sha256(raw).hexdigest()==receipt['raw_pdf_sha256']
        original=next(evidence[x] for x in c['evidence_ids'] if evidence[x]['extraction_method']==METHOD and evidence[x]['locator']=='pdf:original')
        assert original['content_sha256']==receipt['raw_pdf_sha256'] and original['source_url']==receipt['pdf_url']
        assert json.loads(original['source_identifier'])==receipt
        context,refs=registry_context(org,data,evidence,stored_body,allow_carried=bool(c.get('carried_forward')))
        link=receipt['linked_from'];assert domain(link['source_url'])==domain(value['final_url'])
        parent_raw=read_blob(link['content_sha256']);assert hashlib.sha256(parent_raw).hexdigest()==link['content_sha256']
        parent=Page(parent_raw,link['source_url']);source=SimpleNamespace(url=parent.url,sha=link['content_sha256'],retrieved_at=link['retrieved_at'])
        assert pdf_receipts(source,parent).get(receipt['pdf_url'])==link,'PDF lacks own footer/legal-page link receipt'
        parent_e=next(evidence[x] for x in c['evidence_ids'] if evidence[x]['extraction_method']==METHOD and evidence[x]['locator']=='legal-pdf-link:'+receipt['pdf_url'])
        assert parent_e['claim_span']==link['claim_span'] and parent_e['content_sha256']==link['content_sha256']
        pages=extract_pages(raw);text=dict(pages)[receipt['page_number']]
        assert hashlib.sha256(text.encode()).hexdigest()==receipt['page_text_sha256']
        derived=render_text(text);sha=hashlib.sha256(derived).hexdigest();assert sha==receipt['derived_html_sha256']
        assert read_blob(sha)==derived,'PDF-derived proof text differs from raw extraction'
        proof_e=next(evidence[x] for x in c['evidence_ids'] if evidence[x]['content_sha256']==sha and evidence[x]['locator']=='pdf:page:'+str(receipt['page_number'])+'/identity-proof:'+str(value.get('matched_via_subunit') or org))
        assert proof_e['source_url']==receipt['pdf_url']
        context['publisher_company_orgnr']=org
        assert not conflict(Page(render_text('\n'.join(t for _,t in pages)),receipt['pdf_url']),org,context)[0],'PDF publisher conflict'
        p=Page(derived,receipt['pdf_url']);candidate=Candidate(value['final_url'],domain(value['final_url']),value['candidate_origin'],value.get('matched_via_subunit'))
        checked=candidate_proof(p,org,context,candidate,[])
        assert checked.level=='VERIFIED' and checked.token==(value.get('matched_via_subunit') or org)
        count+=1
    return count
