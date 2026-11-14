import httpx,pytest
from tests.test_websites import execute_web,html,OUR,OTHER
from scripts.verify_output import verify


def exercise(tmp_path,monkeypatch,*,cap=2,global_cap=None,owner=OUR,extra=True,homepage_veto=False,first_missing=False):
    def response(req):
        if req.url.path=='/robots.txt':return httpx.Response(200,text='User-agent: *\nAllow: /')
        if req.url.host!='example.no':return httpx.Response(404)
        if req.url.path=='/':return httpx.Response(200,text=html('Org.nr '+OTHER if homepage_veto else '',title='Services',extra='<footer><a href="'+('/vilkar' if first_missing else '/salgsbetingelser')+'">Terms</a></footer>'))
        if req.url.path=='/salgsbetingelser':return httpx.Response(200,text=html('Org.nr '+owner))
        return httpx.Response(404,text='missing')
    return execute_web(tmp_path,monkeypatch,response=response,website=None,website_request_cap=cap,max_requests=global_cap,adaptive_websites=True,adaptive_extra_budget=extra)


def test_leftover_budget_prioritises_unvisited_legal_page_without_refetch(tmp_path,monkeypatch):
    report,row,urls,cfg=exercise(tmp_path,monkeypatch)
    p=report['adaptive_websites']['pass2'];assert p['legal_priority']=={'resumes':1,'requests':1,'websites_gained':1}
    c=next(c for c in row['claims'] if c['field']=='official_website')
    assert c['value']['proof_page_url'].endswith('/salgsbetingelser') and c['value']['identity_level']=='VERIFIED'
    assert urls.count('https://example.no/')==1 and urls.count('https://example.no/robots.txt')==1
    events=[e for e in report['request_log'] if e['pass']=='pass2' and e.get('section')=='website']
    assert events[0]['url']=='https://example.no/salgsbetingelser'
    assert sum(e.get('section')=='website' for e in report['request_log'])<=7
    verify(cfg.output,cfg.state_dir,1,cfg.organisations,cfg.report)

@pytest.mark.parametrize('kwargs',[{'extra':False},{'global_cap':6}])
def test_no_extra_or_no_global_room_never_spends_legal_allowance(tmp_path,monkeypatch,kwargs):
    report,row,urls,_=exercise(tmp_path,monkeypatch,**kwargs)
    assert report['adaptive_websites']['pass2']['legal_priority']['requests']==0
    assert not any(c['field']=='official_website' for c in row['claims'])
    assert not any(u.endswith('/salgsbetingelser') for u in urls)

@pytest.mark.parametrize('mode',['home','legal'])
def test_foreign_publisher_veto_not_overridden_by_legal_resume(tmp_path,monkeypatch,mode):
    report,row,urls,_=exercise(tmp_path,monkeypatch,owner=OTHER,homepage_veto=mode=='home')
    assert not any(c['field']=='official_website' for c in row['claims'])
    if mode=='home':assert report['adaptive_websites']['pass2']['legal_priority']['resumes']==0


def test_previously_checked_legal_404_not_repeated(tmp_path,monkeypatch):
    report,row,urls,_=exercise(tmp_path,monkeypatch,cap=4,first_missing=True)
    assert urls.count('https://example.no/vilkar')==1
    assert next(c for c in row['claims'] if c['field']=='official_website')['value']['proof_page_url'].endswith('/salgsbetingelser')
    assert report['adaptive_websites']['pass2']['legal_priority']['websites_gained']==1

def test_pending_own_terms_pdf_can_use_leftover_legal_budget(tmp_path,monkeypatch):
    from tests.test_legal_pdf import pdf,terms
    doc=pdf([terms()])
    def response(req):
        if req.url.path=='/robots.txt':return httpx.Response(200,text='User-agent: *\nAllow: /')
        if req.url.host!='example.no':return httpx.Response(404)
        if req.url.path=='/terms.pdf':return httpx.Response(200,content=doc,headers={'content-type':'application/pdf'})
        if req.url.path=='/':return httpx.Response(200,text=html('',title='Services',extra='<footer><a href="/terms.pdf">Terms</a></footer>'))
        return httpx.Response(404)
    report,row,urls,cfg=execute_web(tmp_path,monkeypatch,response=response,website=None,website_request_cap=2,adaptive_websites=True,adaptive_extra_budget=True)
    c=next(c for c in row['claims'] if c['field']=='official_website')
    assert c['value']['pdf_proof']['page_number']==1
    assert report['adaptive_websites']['pass2']['legal_priority']=={'resumes':1,'requests':1,'websites_gained':1}
    verify(cfg.output,cfg.state_dir,1,cfg.organisations,cfg.report)
