import io,json,hashlib
import httpx,pytest
from pypdf import PdfWriter
from pypdf.generic import DictionaryObject,NameObject,DecodedStreamObject
from signalpost.web.legal_pdf import extract_pages,MAX_BYTES
from signalpost.budget import SourceFailure
from tests.test_websites import execute_web,html,OUR,OTHER


def pdf(texts):
    writer=PdfWriter()
    for text in texts:
        page=writer.add_blank_page(width=612,height=792)
        font=DictionaryObject({NameObject('/Type'):NameObject('/Font'),NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')})
        page[NameObject('/Resources')]=DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/F1'):writer._add_object(font)})})
        stream=DecodedStreamObject();escaped=text.replace('\\','\\\\').replace('(','\\(').replace(')','\\)')
        stream.set_data(('BT /F1 10 Tf 20 750 Td ('+escaped+') Tj ET').encode('ascii'))
        page[NameObject('/Contents')]=writer._add_object(stream)
    out=io.BytesIO();writer.write(out);return out.getvalue()


def terms(owner=OUR):return 'Terms of sale. Example AS Org.nr '+owner+'. '+('These terms describe our company services and customer rights. '*10)


def run_pdf(tmp_path,monkeypatch,body=None,robots='User-agent: *\nAllow: /',foreign=False,hidden=False):
    document=body or pdf([terms()])
    def response(req):
        if req.url.path=='/robots.txt':return httpx.Response(200,text=robots)
        if req.url.path=='/terms.pdf':return httpx.Response(200,content=document,headers={'content-type':'application/pdf'})
        if req.url.path=='/':
            href='https://foreign.no/terms.pdf' if foreign else '/terms.pdf'
            return httpx.Response(200,text=html('',title='Services',extra='<footer><a '+('hidden ' if hidden else '')+'href="'+href+'">Terms</a></footer>'))
        return httpx.Response(404,text='missing')
    return execute_web(tmp_path,monkeypatch,response=response,website=None)


def test_linked_terms_pdf_exact_number_hash_page_and_independent_replay(tmp_path,monkeypatch):
    from scripts.verify_output import verify
    doc=pdf(['This cover page does not identify a company. '*10,terms()])
    report,row,urls,cfg=run_pdf(tmp_path,monkeypatch,doc)
    site=next(c for c in row['claims'] if c['field']=='official_website')
    receipt=site['value']['pdf_proof'];assert receipt['page_number']==2
    assert receipt['raw_pdf_sha256']==hashlib.sha256(doc).hexdigest()
    assert site['value']['identity_level']=='VERIFIED' and site['value']['proof_page_url'].endswith('/terms.pdf')
    assert any(e['locator']=='pdf:page:2/identity-proof:'+OUR for e in row['evidence'])
    assert report['max_requests_per_company']<=13
    verify(cfg.output,cfg.state_dir,1)
    receipt['page_number']=1;cfg.output.write_text(json.dumps(row)+'\n',encoding='utf8')
    with pytest.raises(AssertionError):verify(cfg.output,cfg.state_dir,1)

@pytest.mark.parametrize('doc',[pdf([terms(OTHER)]),pdf([terms(),terms(OTHER)]),pdf(['Undated terms without a company number. '*20]),b'not a PDF'])
def test_foreign_multicompany_or_absent_identifier_unreadable_rejected(tmp_path,monkeypatch,doc):
    _,row,_,_=run_pdf(tmp_path,monkeypatch,doc)
    assert not any(c['field']=='official_website' for c in row['claims'])

@pytest.mark.parametrize('kind',['robots','foreign','hidden','budget'])
def test_pdf_link_scope_robots_hidden_and_budget_enforced(tmp_path,monkeypatch,kind):
    if kind=='budget':
        report,row,urls,_=execute_web(tmp_path,monkeypatch,body=html('',extra='<footer><a href="/terms.pdf">Terms</a></footer>',title='Services'),website=None,website_request_cap=2)
    else:
        report,row,urls,_=run_pdf(tmp_path,monkeypatch,robots='User-agent: *\nDisallow: /terms.pdf' if kind=='robots' else 'User-agent: *\nAllow: /',foreign=kind=='foreign',hidden=kind=='hidden')
    assert not any(u.endswith('/terms.pdf') for u in urls)
    assert not any(c['field']=='official_website' for c in row['claims'])


def test_pdf_original_bytes_and_page_count_caps():
    with pytest.raises(SourceFailure,match='pdf_body_cap'):extract_pages(b'%PDF-'+b'x'*MAX_BYTES)
    with pytest.raises(SourceFailure,match='pdf_page_cap'):extract_pages(pdf(['x']*21))
    assert extract_pages(pdf(['']))==[(1,'')]


def test_hidden_or_article_pdf_on_legal_page_never_nominates():
    from signalpost.web.html import Page
    from signalpost.web.legal_pages import legal_links
    p=Page(b'<p>Terms</p><a hidden href="/terms.pdf">Terms</a><article><a href="/privacy.pdf">Privacy</a></article>','https://example.no/terms')
    assert legal_links(p,pdf=True)==[]

def test_pdf_linked_from_fetched_legal_html_and_no_derived_social(tmp_path,monkeypatch):
    document=pdf([terms()+' https://www.facebook.com/example '])
    def response(req):
        if req.url.path=='/robots.txt':return httpx.Response(200,text='User-agent: *\nAllow: /')
        if req.url.path=='/terms.pdf':return httpx.Response(200,content=document,headers={'content-type':'application/pdf'})
        if req.url.path=='/salgsbetingelser':return httpx.Response(200,text=html('',title='Terms',extra='<p><a href="/terms.pdf">Full conditions PDF</a></p>'))
        if req.url.path=='/':return httpx.Response(200,text=html('',title='Services',extra='<footer><a href="/salgsbetingelser">Terms</a></footer>'))
        return httpx.Response(404,text='missing')
    _,row,urls,cfg=execute_web(tmp_path,monkeypatch,response=response,website=None)
    c=next(c for c in row['claims'] if c['field']=='official_website')
    assert c['value']['pdf_proof']['linked_from']['source_url'].endswith('/salgsbetingelser')
    assert not any(c['field'].startswith('social_profile.') for c in row['claims'])
    from scripts.verify_output import verify
    verify(cfg.output,cfg.state_dir,1)
    c['value']['pdf_proof']['linked_from']['claim_span']='forged'
    cfg.output.write_text(json.dumps(row)+'\n',encoding='utf8')
    with pytest.raises(AssertionError):verify(cfg.output,cfg.state_dir,1)


def test_pdf_encrypted_and_transport_oversize_rejected(tmp_path,monkeypatch):
    writer=PdfWriter();writer.add_blank_page(width=612,height=792);writer.encrypt('secret');out=io.BytesIO();writer.write(out)
    with pytest.raises(SourceFailure,match='pdf_encrypted'):extract_pages(out.getvalue())
    _,row,_,_=run_pdf(tmp_path,monkeypatch,b'%PDF-'+b'x'*MAX_BYTES)
    assert not any(c['field']=='official_website' for c in row['claims'])
    assert any('body_cap' in e['message'] for e in row['errors'] if e['section']=='website')
