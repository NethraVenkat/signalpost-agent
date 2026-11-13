import httpx
import pytest
from signalpost.web.fetcher import WebsiteHttp
from tests.test_websites import execute_web, html, OUR, OTHER
from tests.test_r5_stage_a import exercise


@pytest.mark.parametrize('kind',['timeout','connect','5xx'])
def test_strong_transient_candidate_retried_once_and_verified(tmp_path,monkeypatch,kind):
    original=WebsiteHttp.candidate;phase={};hits=[]
    async def tracked(self,candidate,*args,**kwargs):
        phase['value']=self.budget.phase
        return await original(self,candidate,*args,**kwargs)
    monkeypatch.setattr(WebsiteHttp,'candidate',tracked)
    def response(request):
        if request.url.host.endswith('example.no'):
            hits.append((phase['value'],str(request.url)))
            if request.url.path=='/robots.txt':return httpx.Response(200,text='User-agent: *\nAllow: /')
            if phase['value']=='pass1':
                if kind=='timeout':raise httpx.ReadTimeout('synthetic timeout')
                if kind=='connect':raise httpx.ConnectError('synthetic connect failure')
                return httpx.Response(503)
            return httpx.Response(200,text=html())
        return httpx.Response(404)
    report,row,_,_=execute_web(tmp_path,monkeypatch,response=response,
        adaptive_websites=True,adaptive_extra_budget=True)
    a=report['adaptive_websites']
    assert a['pass1']['verified_websites']==0 and a['pass2']['websites_gained']==1
    assert a['pass2']['retry_attempts']==1 and a['pass2']['retry_outcomes']=={'verified':1}
    assert next(c for c in row['claims'] if c['field']=='official_website')['value']['identity_level']=='VERIFIED'
    assert sum(p=='pass2' and not u.endswith('/robots.txt') for p,u in hits)==1
    assert report['requests']<=report['limits']['max_requests']


def test_timeout_retry_is_not_repeated_inside_second_pass(tmp_path,monkeypatch):
    original=WebsiteHttp.candidate;phase={};hits=[]
    async def tracked(self,candidate,*args,**kwargs):
        phase['value']=self.budget.phase
        return await original(self,candidate,*args,**kwargs)
    monkeypatch.setattr(WebsiteHttp,'candidate',tracked)
    def response(request):
        if request.url.path=='/robots.txt':return httpx.Response(200,text='User-agent: *\nAllow: /')
        if request.url.host=='example.no':
            hits.append(phase['value']);raise httpx.ReadTimeout('synthetic')
        return httpx.Response(404)
    report,row,_,_=execute_web(tmp_path,monkeypatch,response=response,
        adaptive_websites=True,adaptive_extra_budget=True)
    assert hits.count('pass1')==2 and hits.count('pass2')==1
    assert report['adaptive_websites']['pass2']['retry_attempts']==1
    assert report['adaptive_websites']['pass2']['retry_outcomes']=={'website_timeout':1}
    assert not any(c['field']=='official_website' for c in row['claims'])


@pytest.mark.parametrize('mode',['robots','foreign','404'])
def test_access_refusals_vetoes_and_permanent_errors_not_retried(tmp_path,monkeypatch,mode):
    hits=[]
    def response(request):
        if request.url.host=='example.no':hits.append(request.url.path)
        if request.url.path=='/robots.txt':
            return httpx.Response(200,text='User-agent: *\nDisallow: /' if mode=='robots' else 'User-agent: *\nAllow: /')
        return httpx.Response(200,text=html('Org nr '+OTHER)) if mode=='foreign' else httpx.Response(404)
    report,row,_,_=execute_web(tmp_path,monkeypatch,response=response,
        adaptive_websites=True,adaptive_extra_budget=True)
    assert report['adaptive_websites']['pass2']['retry_attempts']==0
    assert hits.count('/robots.txt')==1 and hits.count('/')<=1
    assert not any(c['field']=='official_website' for c in row['claims'])


def test_extra_allowance_makes_previously_capped_late_nav_useful(tmp_path,monkeypatch):
    report,row,_,_=exercise(tmp_path,monkeypatch,cap=2,extra_budget=True)
    a=report['adaptive_websites']['pass2']
    assert a['websites_gained']==1 and a['requests']>=2
    assert a['per_company'][OUR]['extra_allowance']=={'http':5,'dns':4}
    assert sum(e.get('section')=='website' for e in report['request_log'])<=7


def test_leftover_global_budget_cannot_be_raised_by_extra_allowance(tmp_path,monkeypatch):
    report,row,calls,_=exercise(tmp_path,monkeypatch,global_cap=6,extra_budget=True)
    assert report['requests']==6 and report['adaptive_websites']['pass2']['requests']==0
    assert report['adaptive_websites']['stop_reason']=='budget_exhausted'
    assert not any('good.no' in url for url in calls)


def test_extended_ceiling_is_phase_local_and_never_resets_counters(tmp_path):
    from tests.test_registry import config
    from signalpost.budget import Budget
    from signalpost.sources.blobstore import BlobStore
    cfg=config(tmp_path,[OUR],adaptive_extra_budget=True)
    http=WebsiteHttp(None,cfg,Budget(cfg),BlobStore(cfg.state_dir))
    http.counts[OUR]=8;http.dns_counts[OUR]=8
    http.pass2_allowances[OUR]={'http':5,'dns':4}
    assert http.company_cap(OUR)==8 and http.dns_limit(OUR)==8
    http.budget.phase='pass2'
    assert http.company_cap(OUR)==13 and http.dns_limit(OUR)==12
    assert http.counts[OUR]==http.dns_counts[OUR]==8
    http.budget.phase='pass1'
    assert http.company_cap(OUR)==8 and http.dns_limit(OUR)==8
