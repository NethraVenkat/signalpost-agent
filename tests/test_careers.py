import asyncio,json
from datetime import datetime,timezone
from types import SimpleNamespace
import pytest
from signalpost.web.careers import links,postings,fetch,ATS
from signalpost.web.html import Page
from signalpost.budget import SourceFailure

ORG='923609016'
NOW=datetime(2026,11,13,tzinfo=timezone.utc)

def page(**values):
    item={'@type':'JobPosting','title':'Software engineer','datePosted':'2026-11-01',**values}
    return Page(('<script type="application/ld+json">'+json.dumps(item)+'</script>').encode(),'https://example.no/jobs/engineer')

def test_own_navigation_and_vendor_allowlist():
    body=b'<article><a href="/careers">Careers</a></article><nav><a href="https://tenant.teamtailor.com/jobs/1">Jobs</a><a href="https://teamtailor.com.evil.no/jobs/1">Jobs</a></nav>'
    assert [url for _,url in links(Page(body,'https://example.no/'),'example.no')]==['https://tenant.teamtailor.com/jobs/1']
    assert len(ATS)==7

@pytest.mark.parametrize('changes',[{'validThrough':'2026-11-12'},{'validThrough':'2026-11-12T23:59:59Z'},
    {'validThrough':'2026-11-13T00:00:00Z'},{'datePosted':'2026-01-01'},{'datePosted':None},{'hiringOrganization':{'identifier':'991853995'}}])
def test_reject_expired_undated_or_foreign(changes):
    assert not postings(page(**changes),ORG,NOW)

def test_current_posting_requires_own_title_and_receipts():
    found=postings(page(),ORG,NOW)
    assert found[0][0]['title']=='Software engineer'
    assert all(span in page().raw for span in found[0][1])
    assert not postings(page(title=None),ORG,NOW)
    assert postings(page(datePosted=None,validThrough='2026-12-01'),ORG,NOW)


def test_explicit_open_status_belongs_to_posting():
    raw=page(datePosted=None).raw
    p=Page((raw+'<p>Software engineer: Applications open</p>').encode(),'https://example.no/jobs/engineer')
    assert postings(p,ORG,NOW)
    p=Page((raw+'<footer>Applications open</footer>').encode(),p.url)
    assert not postings(p,ORG,NOW)

def test_group_site_withheld():
    p=page();p.title='Example Group';assert not postings(p,ORG,NOW)


@pytest.mark.parametrize('robots,expected',[('Allow: /',1),('Disallow: /',0)])
def test_real_transport_robots_budget_and_saved_proof(tmp_path,robots,expected,monkeypatch):
    import httpx
    from signalpost.web.fetcher import WebsiteHttp
    from signalpost.sources.blobstore import BlobStore
    from signalpost.sources.http import Response
    from signalpost.models.evidence import utc_now
    from signalpost.budget import Budget
    from signalpost.models.claim import Claim
    from tests.test_registry import config
    from scripts.verify_output import verify_careers
    proof=Claim(field='official_website',availability='available',family='website',id='proof',evidence_ids=['website'],
        value={'identity_level':'VERIFIED','final_url':'https://example.no/'},first_observed_at=utc_now(),last_observed_at=utc_now())
    env=SimpleNamespace(claims=[proof],run=SimpleNamespace(refresh={}))
    cfg=config(tmp_path,[ORG]).model_copy(update={'website_politeness_seconds':0})
    blobs=BlobStore(cfg.state_dir)
    home=b'<nav><a href="https://tenant.teamtailor.com/jobs/engineer">Jobs</a></nav>'
    response=Response(home,200,'https://example.no/',utc_now(),blobs.put(home))
    def dispatch(request):
        if request.url.path=='/robots.txt':return httpx.Response(200,text='User-agent: *\n'+robots)
        return httpx.Response(200,text=page(validThrough='2099-12-01',url='https://tenant.teamtailor.com/jobs/engineer').raw)
    async def resolver(*args):return ['93.184.216.34']
    async def execute():
        async with httpx.AsyncClient(transport=httpx.MockTransport(dispatch)) as client:
            http=WebsiteHttp(client,cfg,Budget(cfg),blobs,resolver)
            result=await fetch(ORG,env,http,[(response,Page(home,response.url))])
            assert len(http.budget.events)==1+expected
            assert http.counts[ORG]==1+expected
            return result
    result=asyncio.run(execute());assert len(result.claims)==expected
    if expected:
        data={'claims':[proof.model_dump()]+[c.model_dump() for c in result.claims]}
        evidence={e.id:e.model_dump() for e in result.evidence}
        evidence['website']={'extraction_method':'test.website'}
        verify_careers({'organisation_number':ORG},data,evidence,lambda sha:blobs.read(sha).decode())
        data['claims'][-1]['value']['title']='Invented title'
        with pytest.raises(AssertionError):verify_careers({'organisation_number':ORG},data,evidence,lambda sha:blobs.read(sha).decode())

def test_budget_and_verified_site_gate():
    proof=SimpleNamespace(field='official_website',availability='available',carried_forward=False,
        value={'identity_level':'VERIFIED','final_url':'https://example.no/'},id='proof',evidence_ids=[])
    env=SimpleNamespace(claims=[proof],run=SimpleNamespace(refresh={}))
    response=SimpleNamespace(url='https://example.no/')
    p=Page(b'<nav><a href="/careers">Careers</a></nav>',response.url)
    class Http:
        calls=0
        async def get(self,*args,**kwargs):
            self.calls+=1;raise SourceFailure('website_budget_exhausted')
    http=Http()
    result=asyncio.run(fetch(ORG,env,http,[(response,p)]))
    assert not result.claims and http.calls==1
    assert env.run.refresh['careers']['reason']=='website_budget_exhausted'
    proof.value['identity_level']='HIGH'
    asyncio.run(fetch(ORG,env,http,[(response,p)]));assert http.calls==1


def test_index_maintenance_allowance_does_not_change_daily_budget(tmp_path,monkeypatch):
    import sys
    from pathlib import Path
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1]/'scripts'))
    from build_nav_index import build_budget
    from signalpost.budget import Budget
    from tests.test_registry import config
    cfg=config(tmp_path,[ORG],max_requests=10000)
    assert Budget(cfg).cap==18
    assert build_budget(cfg).cap==10000
    assert Budget(cfg).cap==18
