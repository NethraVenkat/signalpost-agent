import asyncio
from types import SimpleNamespace
from signalpost.budget import Budget
from signalpost.web.search import Search,SearchError
from tests.test_registry import config
from tests.test_nav import ORG
import pytest

class Fake:
    def __init__(self,fail=False):self.calls=[];self.fail=fail
    async def search(self,query,timeout):
        self.calls.append(query)
        if self.fail:raise RuntimeError('provider unavailable')
        return [
            {'url':'https://facebook.com/example','title':'Facebook','description':''},
            {'url':'https://www.linkedin.com/company/example','title':'LinkedIn','description':''},
            {'url':'https://proff.no/example','title':'Proff','description':''},
            {'url':'https://example.no/path','title':'Example AS','description':'Official website'},
            {'url':'https://example.no/other','title':'Example AS','description':'About page'},
            {'url':'http://another.no/','title':'Example AS - Oslo Division','description':'Official site'}
        ]

def http():return SimpleNamespace(counts={},dns_counts={})

def test_no_key_no_calls(tmp_path,monkeypatch):
    monkeypatch.delenv('BRAVE_SEARCH_API_KEY',raising=False)
    cfg=config(tmp_path,[ORG]);s=Search(None,cfg,Budget(cfg))
    assert asyncio.run(s.nominate(ORG,{'name':'Example AS'},http()))==[]
    assert s.metrics['status']=='not configured' and s.metrics['queries']==0

def test_nomination_only_filters_one_query_and_cost(tmp_path):
    cfg=config(tmp_path,[ORG]);provider=Fake();budget=Budget(cfg);s=Search(None,cfg,budget,provider)
    async def gate():
        rows=await s.nominate(ORG,{'name':'Example AS','municipality':'Oslo'},http())
        assert await s.nominate(ORG,{'name':'Example AS'},http())==[]
        return rows
    rows=asyncio.run(gate())
    assert [c.domain for c in rows]==['example.no','another.no']
    assert provider.calls==['example site:.no']
    assert s.metrics['queries']==1 and s.metrics['estimated_usd']==.005
    assert len(budget.events)==1 and budget.events[0]['section']=='search'
    assert not any('content_sha256' in e for e in budget.events)
    from signalpost.web.search import score_identity
    ctx = {'name': 'Acme Solutions AS', 'brand': 'Acme'}
    org = '912345678'
    s1, sig1 = score_identity({'url': 'https://acme.no/about', 'title': 'Acme Solutions', 'description': 'Official site'}, org, ctx)
    assert s1 >= 60 and 'legal_name_match' in sig1 and 'brand_match' in sig1
    s2, sig2 = score_identity({'url': 'https://acme-group.no', 'title': 'Portal', 'description': 'Org nr 912 345 678'}, org, ctx)
    assert s2 >= 60 and 'orgnr_in_snippet' in sig2
    s3, sig3 = score_identity({'url': 'https://proff.no/selskap/acme', 'title': 'Acme', 'description': 'Directory'}, org, ctx)
    assert s3 < 60 and 'generic_domain_penalty' in sig3
    s4, _ = score_identity({'url': 'https://dagensnyheter.no/news', 'title': 'Dagens Nyheter', 'description': 'Acme Solutions AS mentioned'}, org, ctx)
    assert s4 < 60

def test_caps_and_provider_error_preserve_no_search_behavior(tmp_path):
    for options in [{'search_max_queries':0},{'search_max_cost_usd':0}]:
        cfg=config(tmp_path,[ORG],**options);provider=Fake();s=Search(None,cfg,Budget(cfg),provider)
        assert asyncio.run(s.nominate(ORG,{'name':'Example AS'},http()))==[] and not provider.calls
    cfg=config(tmp_path,[ORG]);s=Search(None,cfg,Budget(cfg),Fake(True))
    assert asyncio.run(s.nominate(ORG,{'name':'Example AS'},http()))==[]
    assert s.metrics['errors']==1


@pytest.mark.parametrize('proven',[True,False])
def test_search_candidate_only_publishes_with_fetched_exact_orgnr(tmp_path,monkeypatch,proven):
    from tests.test_websites import execute_web,html
    monkeypatch.setenv('BRAVE_SEARCH_API_KEY','synthetic-test-only')
    monkeypatch.setattr('signalpost.web.search.Brave',lambda *args:Fake())
    monkeypatch.setattr('signalpost.web.collector.generate',lambda context:[])
    report,row,requests,cfg=execute_web(tmp_path,monkeypatch,body=html('Org nr '+ORG if proven else ''),website=None)
    published=[c for c in row['claims'] if c['field']=='official_website' and c['availability']=='available']
    assert bool(published)==proven
    assert report['search']['queries']==1
    assert all('search.brave.com' not in e['source_url'] for e in row['evidence'])
    if proven:
        assert published[0]['value']['candidate_origin']=='search_brave'
        refs=set(published[0]['evidence_ids']);assert all(e['source_class']=='company_owned' for e in row['evidence'] if e['id'] in refs)


def test_one_retry_is_budgeted_and_costed(tmp_path):
    class Retry(Fake):
        async def search(self,query,timeout):
            self.calls.append(query)
            if len(self.calls)==1:raise SearchError(503,'0')
            return ['https://example.no']
    cfg=config(tmp_path,[ORG],search_max_queries=2);s=Search(None,cfg,Budget(cfg),Retry())
    assert asyncio.run(s.nominate(ORG,{'name':'Example AS'},http()))
    assert s.metrics['queries']==2 and s.metrics['estimated_usd']==.01



