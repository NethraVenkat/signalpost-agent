import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
import httpx
import pytest

from signalpost.budget import Budget, SourceFailure
from signalpost.sources.blobstore import BlobStore
from signalpost.web.fetcher import WebsiteHttp
from signalpost.web.candidates import Candidate, generate
from signalpost.web.activity import parse
from signalpost.sources.nav import candidate_score, name_tokens, Index, prefetch
from tests.test_registry import config
from tests.test_websites import execute_web, html, OUR

NOW = datetime(2026, 10, 13, tzinfo=timezone.utc)


@pytest.mark.parametrize('failure,code', [('no_such_domain','no_such_domain'), ('dns_error','dns_unavailable'), ('dns_timeout','dns_unavailable'), ('empty','no_such_domain'), ('private','ssrf')])
def test_dns_no_http_and_cached_failure(tmp_path, failure, code):
    calls=[];dns=[]
    async def resolver(host, port):
        dns.append(host)
        if failure=='empty': return []
        if failure=='private': return ['127.0.0.1']
        raise SourceFailure(failure)
    def response(request): calls.append(request.url);return httpx.Response(200)
    cfg=config(tmp_path,[OUR],websites=True)
    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(response)) as client:
            http=WebsiteHttp(client,cfg,Budget(cfg),BlobStore(cfg.state_dir),resolver)
            for org in [OUR, '993578843']:
                with pytest.raises(SourceFailure) as exc: await http.candidate(Candidate('https://missing.no/','missing.no','legal_name_slug'),org)
                assert exc.value.code==code
            assert http.dns_lookups==1
    asyncio.run(run())
    assert dns==['missing.no'] and not calls


def test_dns_cap_eight_and_ssrf_recheck(tmp_path):
    async def resolver(host, port): return ['93.184.216.34']
    cfg=config(tmp_path,[OUR],websites=True)
    async def run():
        async with httpx.AsyncClient() as client:
            http=WebsiteHttp(client,cfg,Budget(cfg),BlobStore(cfg.state_dir),resolver)
            for i in range(8): await http.precheck(Candidate(f'https://example{i}.no/', f'example{i}.no','registry_email'),OUR)
            with pytest.raises(SourceFailure): await http.precheck(Candidate('https://ninth.no/','ninth.no','registry_email'),OUR)
            assert http.dns_lookups==8
    asyncio.run(run())


def test_candidate_order_and_stop_after_verified(tmp_path, monkeypatch):
    candidates=generate({'website':'declared.no','email':'a@email.no','name':'Distinctive AS'})
    assert [c.origin for c in candidates][:3]==['registry_website','registry_email','legal_name_slug']
    report,row,requests,_=execute_web(tmp_path,monkeypatch)
    assert row['run']['sections']['website']=='available'
    assert not any('exampleas' in url or 'example.com' in url for url in requests)
    assert len([url for url in requests if 'data.brreg.no' not in url])==2
    assert report['dns_precheck_lookups']==0 and report['dns_lookups']==2


def test_rank_rare_tokens_suffixes_and_transliteration():
    assert name_tokens('Gjøvik Åsheim Ægir SERVICES AS')==name_tokens('Gjoevik Aasheim Aegir ASA')
    assert candidate_score('Rare Common AS','Rare Ventures ASA',{'rare':1,'common':50}) > candidate_score('Common AS','Common Ventures',{'common':50})
    assert candidate_score('Generic Service AS','Other Services',{})==0


def test_ranked_cap_order_and_incomplete_companies(tmp_path):
    from tests.test_nav import TOKEN, ORG, OTHER
    cfg=config(tmp_path,[ORG,OTHER],hiring=True,nav_max_details=1)
    ids=['00000000-0000-4000-8000-00000000000'+str(i) for i in range(1,4)]
    names=['Common AS','Rare Common AS','Common AS']
    calls=[];index=Index()
    async def company_names(): return {ORG:{'Rare AS'},OTHER:{'Common AS'}}
    def response(request):
        if request.url.path=='/api/publicToken': return httpx.Response(200,text=TOKEN)
        if '/feedentry/' in request.url.path:
            calls.append(request.url.path.rsplit('/',1)[-1]);return httpx.Response(404,json={})
        return httpx.Response(200,json={'items':[{'id':uuid,'url':'/api/v1/feedentry/'+uuid,'date_modified':NOW.isoformat(),'_feed_entry':{'uuid':uuid,'status':'ACTIVE','businessName':name}} for uuid,name in zip(ids,names)],'next_url':None})
    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(response)) as client:
            await prefetch(client,cfg,Budget(cfg),BlobStore(cfg.state_dir),index,company_names)
    asyncio.run(run())
    assert calls==[ids[1]] and index.metrics['cap_hits']==2
    assert not index.company_complete(ORG) and not index.company_complete(OTHER)


@pytest.mark.parametrize('xml', [
    '<urlset><url><loc>https://example.no/news/update</loc><lastmod>2026-10-10</lastmod></url></urlset>',
    '<rss><channel><item><title>Update</title><link>https://example.no/news/update</link><pubDate>Sat, 10 Oct 2026 00:00:00 GMT</pubDate></item></channel></rss>',
    '<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Update</title><link href="https://example.no/news/update"/><updated>2026-10-10</updated></entry></feed>'
])
def test_activity_formats_dates_and_verbatim_span(xml):
    items,children=parse(xml.encode(),'https://example.no/sitemap.xml',NOW)
    assert not children and len(items)==1
    value,_,span=items[0]
    assert value['date']=='2026-10-10' and value['url']=='https://example.no/news/update'
    assert span in xml and len(span)<=300


@pytest.mark.parametrize('url,date',[('https://other.no/news/item','2026-10-10'),('https://example.no/products/item','2026-10-10'),('https://example.no/news/item','2026-10-20'),('https://example.no/news/item','1999-12-31'),('https://example.no/news/item','invalid')])
def test_activity_filters(url,date):
    xml=f'<urlset><url><loc>{url}</loc><lastmod>{date}</lastmod></url></urlset>'
    assert parse(xml.encode(),'https://example.no/sitemap.xml',NOW)==([],[])


@pytest.mark.parametrize('path',['/artikler/author/thanh/','/da/artikler/forfatter/thanh/','/fi/artikkelit/kirjoittaja/thanh/','/news/category/latest/','/blog/tag/offer/','/news/','/en/news/'])
def test_non_article_paths_are_not_updates(path):
    xml=f'<urlset><url><loc>https://example.no{path}</loc><lastmod>2026-10-10</lastmod></url></urlset>'
    assert parse(xml.encode(),'https://example.no/sitemap.xml',NOW)==([],[])


def test_sitemap_index_depth_and_domain():
    xml='<sitemapindex><sitemap><loc>https://example.no/news.xml</loc></sitemap><sitemap><loc>https://other.no/map.xml</loc></sitemap></sitemapindex>'
    assert parse(xml.encode(),'https://example.no/sitemap.xml',NOW)==([],['https://example.no/news.xml'])
    with pytest.raises(ValueError): parse(b'<!DOCTYPE x [<!ENTITY x "unsafe">]><urlset/>','https://example.no/sitemap.xml',NOW)


def test_activity_live_pipeline_synthesis_and_refresh(tmp_path,monkeypatch):
    from signalpost.models.envelope import Envelope
    from signalpost.synthesis.validate import sentence_error
    now=datetime.now(timezone.utc).date().isoformat()
    xml=f'<urlset><url><loc>https://example.no/news/update</loc><lastmod>{now}</lastmod></url></urlset>'
    def response(request):
        if request.url.path=='/robots.txt': return httpx.Response(200,text='User-agent: *\nAllow: /')
        if request.url.path=='/sitemap.xml': return httpx.Response(200,text=xml,headers={'content-type':'application/xml'})
        return httpx.Response(200,text=html())
    report,row,requests,cfg=execute_web(tmp_path/'first',monkeypatch,response=response,public_activity=True)
    assert row['run']['sections']['activity']=='available'
    assert len([u for u in requests if 'data.brreg.no' not in u])==3
    env=Envelope.model_validate(row)
    sentence=next(s for s in env.run.synthesis.sections.changes if s.text.startswith('Latest dated'))
    assert sentence_error(sentence,env) is None
    assert sentence_error(sentence.model_copy(update={'text':sentence.text.replace(now,'2001-01-01')}),env)
    report,rerun,_,_=execute_web(tmp_path/'rerun',monkeypatch,response=response,public_activity=True,previous=cfg.output)
    assert report['changes']==0 and report['observation_changes']==0
    def missing(request):
        if request.url.path=='/sitemap.xml':return httpx.Response(404)
        return response(request)
    report,removed,_,_=execute_web(tmp_path/'removed',monkeypatch,response=missing,public_activity=True,previous=cfg.output)
    assert any(c['type']=='removed' and c['materiality']=='minor' for c in removed['changes'])
    def failed(request):
        if request.url.path=='/sitemap.xml':return httpx.Response(500)
        return response(request)
    report,failed_row,_,_=execute_web(tmp_path/'failed',monkeypatch,response=failed,public_activity=True,previous=cfg.output)
    assert report['changes']==0 and report['observation_changes']==1
    assert any(c['family']=='activity' and c['carried_forward'] for c in failed_row['claims'])
    from signalpost.refresh.diff import apply
    from signalpost.sources.blobstore import BlobStore
    changed_scope=env.model_copy(deep=True)
    changed_scope.claims=[c for c in changed_scope.claims if c.family!='activity']
    changed_scope.run.sections['activity']='not_available'
    changed_scope.run.refresh['activity']={'checked_urls':['https://example.no/different-feed.xml']}
    apply(changed_scope,row,BlobStore(cfg.state_dir))
    assert not changed_scope.changes
    assert any(c.family=='activity' and c.carried_forward for c in changed_scope.claims)


def test_uncertain_website_is_not_an_activity_removal(tmp_path,monkeypatch):
    def response(request):
        if request.url.path=='/robots.txt':return httpx.Response(200,text='User-agent: *\nAllow: /')
        raise httpx.ReadTimeout('synthetic')
    _,row,_,_=execute_web(tmp_path,monkeypatch,response=response,public_activity=True)
    assert row['run']['sections']['website']=='failed'
    assert row['run']['sections']['activity']=='failed'


def test_activity_robots_and_budget(tmp_path,monkeypatch):
    def response(request):
        if request.url.path=='/robots.txt': return httpx.Response(200,text='User-agent: *\nDisallow: /sitemap.xml')
        return httpx.Response(200,text=html())
    _,row,requests,_=execute_web(tmp_path/'robots',monkeypatch,response=response,public_activity=True)
    assert row['run']['sections']['activity']=='blocked'
    assert not any('/sitemap.xml' in u for u in requests)
    _,row,requests,_=execute_web(tmp_path/'budget',monkeypatch,public_activity=True,website_request_cap=2)
    assert row['run']['sections']['activity']=='failed' # Allowed extra fetch is HTML, not sitemap XML.
    assert len([u for u in requests if 'data.brreg.no' not in u])<=3


def test_recent_registry_dates_are_cited_without_requests(tmp_path):
    from tests.test_synthesis import envelope
    from tests.test_synthesis_readability import available
    from signalpost.synthesis.template import generate
    from signalpost.synthesis.validate import sentence_error
    row,_=envelope(tmp_path)
    row.run.completed_at='2026-10-13T00:00:00Z'
    claim=available(row,'identity.founding_date','2025-10-13')
    result=generate(row)
    sentence=next(s for s in result.sections.changes if s.text=='Founded: 2025-10-13.')
    assert sentence.claim_ids==[claim.id] and sentence_error(sentence,row) is None
    assert sentence_error(sentence.model_copy(update={'text':'Founded: 2024-10-12.'}),row)
    claim.value='2020-10-13'
    assert not any(s.text.startswith('Founded:') for s in generate(row).sections.changes)
