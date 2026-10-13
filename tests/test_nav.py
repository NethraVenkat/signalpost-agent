import asyncio
import json
import base64
from datetime import datetime,timedelta,timezone
from pathlib import Path
import httpx
import respx
from signalpost.runner import run
from signalpost.sources.nav import BASE,allowed
from signalpost.budget import SourceFailure
from tests.test_registry import config,handler

ORG='923609016'; SUB='993578843'; OTHER='988258229'
UUID='00000000-0000-4000-8000-000000000001'
TOKEN='.'.join(base64.urlsafe_b64encode(part).decode().rstrip('=') for part in
               [b'{"alg":"HS256"}',b'{"sub":"offline-test"}',b'synthetic-signature'])


def execute(tmp,org=ORG,employer=ORG,status='ACTIVE',expired=False,partial=False,token_ok=True,previous=None,subunit=False,header_name=None,conditional_cache=False,asof=None,**options):
    cfg=config(tmp,[org],hiring=True,previous=previous,**options)
    calls=[]
    now=asof or datetime.now(timezone.utc)
    feed={'items':[{'id':UUID,'url':'/api/v1/feedentry/'+UUID,'date_modified':now.isoformat(),
                      '_feed_entry':{'uuid':UUID,'status':status,'businessName':header_name}}],
          'next_url':'/api/v1/feed/'+UUID if partial else None,'next_id':UUID if partial else None}
    def response(request):
        calls.append(str(request.url))
        if request.url.host=='data.brreg.no':
            if subunit and '/underenheter' in request.url.path:
                return httpx.Response(200,json={'_embedded':{'underenheter':[{'organisasjonsnummer':SUB,'overordnetEnhet':org,'navn':'Branch'}]},'page':{'totalPages':1}})
            return handler()(request)
        if request.url.path=='/api/publicToken':return httpx.Response(200,text='Current public token:\n'+TOKEN) if token_ok else httpx.Response(503,text='unavailable')
        assert request.headers['Authorization']=='Bearer '+TOKEN
        if '/feedentry/' in request.url.path:
            return httpx.Response(200,json={'uuid':UUID,'status':status,'ad_content':{'uuid':UUID,'title':'Employer vacancy',
                'published':(now-timedelta(days=2)).isoformat(),'expires':(now+timedelta(days=-1 if expired else 30)).isoformat(),
                'employer':{'name':'Example AS','orgnr':employer},'workLocations':[{'municipal':'OSLO','city':'Oslo'}]}})
        if conditional_cache and request.headers.get('If-None-Match')=='test-etag':return httpx.Response(304)
        return httpx.Response(200,json=feed,headers={'ETag':'test-etag'})
    with respx.mock(assert_all_called=False) as mock:
        mock.route().mock(side_effect=response)
        report=asyncio.run(run(cfg))
    row=json.loads(cfg.output.read_text(encoding='utf8').splitlines()[0])
    return report,row,cfg,calls


def test_name_prefilter_and_detail_cap(tmp_path):
    from signalpost.sources.nav import name_tokens,name_matches
    from tests.test_registry import entity
    legal=entity(ORG)['navn']
    assert name_tokens('  Distinctive SERVICES AS ') == {'distinctive'}
    assert name_matches('Distinctive Ventures AS','Distinctive Ventures ASA')
    assert not name_matches('Distinctive Unrelated AS','Distinctive Ventures AS')
    report,row,_,calls=execute(tmp_path/'no-match',header_name='Completely Unrelated Employer AS')
    assert report['nav_detail_requests']==0 and not any('/feedentry/' in url for url in calls)
    assert row['run']['sections']['hiring']=='not_available'
    report,row,_,_=execute(tmp_path/'matching-foreign',header_name=legal,employer=OTHER)
    assert report['nav_detail_requests']==1 and row['run']['sections']['hiring']=='not_available'
    for label,name in [('known',legal),('missing',None)]:
        report,row,_,_=execute(tmp_path/label,header_name=name,nav_max_details=0)
        assert report['nav_detail_requests']==0 and row['run']['sections']['hiring']=='failed'
        assert any('nav_detail_cap' in e['code'] for e in row['errors'])


def test_subunit_name_discovery(tmp_path):
    report,row,_,_=execute(tmp_path,header_name='Branch AS',employer=SUB,subunit=True)
    assert report['nav_detail_requests']==1 and row['run']['sections']['hiring']=='available'


def test_detail_retry_counts_against_cap_and_only_affected_company_fails(tmp_path):
    from signalpost.sources.nav import Index,prefetch
    from signalpost.sources.blobstore import BlobStore
    from signalpost.budget import Budget
    cfg=config(tmp_path,[ORG,OTHER],hiring=True,nav_max_details=1)
    index=Index(); detail_calls=[]
    now=datetime.now(timezone.utc).isoformat()
    async def names(): return {ORG:{'distinctive'},OTHER:{'unrelated'}}
    def response(request):
        if request.url.path=='/api/publicToken':return httpx.Response(200,text=TOKEN)
        if '/feedentry/' in request.url.path:
            detail_calls.append(str(request.url));return httpx.Response(500,json={})
        return httpx.Response(200,json={'items':[{'id':UUID,'url':'/api/v1/feedentry/'+UUID,'date_modified':now,
             '_feed_entry':{'uuid':UUID,'status':'ACTIVE','businessName':'Distinctive AS'}}],'next_url':None,'next_id':None})
    async def execute():
        async with httpx.AsyncClient(transport=httpx.MockTransport(response)) as client:
            await prefetch(client,cfg,Budget(cfg),BlobStore(cfg.state_dir),index,names)
    asyncio.run(execute())
    assert len(detail_calls)==1 and index.metrics['detail_requests']==1
    assert not index.company_complete(ORG) and index.company_complete(OTHER)


def test_active_old_job_with_changed_header_name_is_not_false_closure(tmp_path):
    _,_,first,_=execute(tmp_path/'first')
    report,row,_,_=execute(tmp_path/'second',header_name='Unrelated Business AS',previous=first.output)
    assert row['run']['sections']['hiring']=='failed'
    assert not any(c['type']=='closed_job' for c in row['changes'])


def test_etag_304_uses_exact_cached_page(tmp_path):
    execute(tmp_path)
    report,row,_,_=execute(tmp_path,conditional_cache=True)
    assert report['hiring_prefetch']['complete'] and row['run']['sections']['hiring']=='available'
    assert any(e['status']==304 for e in report['request_log'])


def test_fixed_nav_sources_are_idempotent(tmp_path):
    now=datetime.now(timezone.utc)
    _,before,first,_=execute(tmp_path/'first',asof=now)
    report,after,_,_=execute(tmp_path/'second',asof=now,previous=first.output)
    assert report['changes']==report['observation_changes']==0
    assert sorted(c['id'] for c in before['claims'])==sorted(c['id'] for c in after['claims'])


def test_exact_org_and_shared_requests(tmp_path,monkeypatch):
    monkeypatch.delenv('NAV_API_TOKEN',raising=False)
    report,row,cfg,calls=execute(tmp_path)
    claim=next(c for c in row['claims'] if c['family']=='hiring' and c['availability']=='available')
    assert claim['value']['employer_orgnr']==ORG and claim['value']['matched_via']=='organisation '+ORG
    assert row['run']['sections']['hiring']=='available' and report['hiring_prefetch']['complete']
    assert report['shared_requests']==3 and report['requests_per_company']==4
    assert TOKEN not in json.dumps(report) and TOKEN not in cfg.output.read_text()
    assert not any(TOKEN.encode() in p.read_bytes() for p in (cfg.state_dir/'blobs').iterdir())
    assert not any('arbeidsplassen.nav.no' in url for url in calls)


def test_subunit_and_name_only_rejection(tmp_path):
    _,row,_,_=execute(tmp_path/'sub',employer=SUB,subunit=True)
    assert next(c for c in row['claims'] if c['family']=='hiring')['value']['matched_via']=='subunit '+SUB
    for label,employer in [('foreign',OTHER),('missing',None)]:
        _,row,_,_=execute(tmp_path/label,employer=employer)
        assert row['run']['sections']['hiring']=='not_available'
        assert not any(c['family']=='hiring' and c['availability']=='available' for c in row['claims'])


def test_inactive_expired_and_partial(tmp_path):
    for label,kwargs in [('inactive',{'status':'INACTIVE'}),('expired',{'expired':True})]:
        _,row,_,_=execute(tmp_path/label,**kwargs)
        assert row['run']['sections']['hiring']=='not_available'
    report,row,_,_=execute(tmp_path/'partial',partial=True,nav_max_pages=1)
    assert not report['hiring_prefetch']['complete'] and row['run']['sections']['hiring']=='failed'
    assert any(c['family']=='hiring' and c['availability']=='available' for c in row['claims'])


def test_token_unavailable_and_zero_page_cap(tmp_path,monkeypatch):
    monkeypatch.delenv('NAV_API_TOKEN',raising=False)
    report,row,_,_=execute(tmp_path/'token',token_ok=False)
    assert row['run']['sections']['hiring']=='blocked'
    assert any(e['code']=='token_unavailable' for e in row['errors'])
    _,row,_,_=execute(tmp_path/'pages',nav_max_pages=0)
    assert row['run']['sections']['hiring']=='failed'


def test_closed_job_only_from_complete_index(tmp_path):
    _,_,first,_=execute(tmp_path/'first')
    report,row,_,_=execute(tmp_path/'closed',status='INACTIVE',previous=first.output)
    assert len([c for c in row['changes'] if c['type']=='closed_job'])==1
    report,row,_,_=execute(tmp_path/'partial',partial=True,status='INACTIVE',nav_max_pages=1,previous=first.output)
    assert not any(c['type']=='closed_job' for c in row['changes'])
    assert report['observation_changes']>=1


def test_known_expired_not_carried_and_url_policy(tmp_path):
    _,_,first,_=execute(tmp_path/'first')
    report,row,_,_=execute(tmp_path/'partial',partial=True,expired=True,nav_max_pages=1,previous=first.output)
    assert not any(c['family']=='hiring' and c['availability']=='available' for c in row['claims'])
    for url in ['http://pam-stilling-feed.nav.no/api/v1/feed','https://evil.no/api/v1/feed','https://pam-stilling-feed.nav.no/admin','https://pam-stilling-feed.nav.no/api/v1/feed?token=secret']:
        try:allowed(url)
        except SourceFailure:pass
        else:raise AssertionError('URL was not refused')
