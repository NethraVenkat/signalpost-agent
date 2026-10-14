import asyncio,gzip,json
from datetime import datetime,timedelta,timezone
from pathlib import Path
import httpx,pytest
from signalpost.budget import Budget,SourceFailure
from signalpost.sources.nav import BASE,Index,prefetch,section
from signalpost.sources.nav_index import DEFAULT_PATH,load,write,validate,AD_FIELDS
from signalpost.sources.blobstore import BlobStore
from signalpost.models.evidence import utc_now
from signalpost.runner import placeholder
from tests.test_registry import config
from tests.test_nav import ORG,OTHER,SUB,TOKEN,UUID
from tests.test_nav_streaming import header,ad,SECOND


def artifact(tmp_path,ads=None,**overrides):
    ads=ads if ads is not None else [{'uuid':UUID,'employer_orgnr':ORG,'status':'ACTIVE',
        'published':'2026-10-01T00:00:00Z','expires':'2099-01-01T00:00:00Z',
        'last_modified':'2026-10-01T00:00:00Z','etag':None}]
    data={'schema_version':1,'index_version':'test-v1','built_at':utc_now(),
        'cursor':BASE+'/api/v1/feed/'+UUID,'source_urls':[BASE+'/api/v1/feed',BASE+'/api/v1/feedentry/{uuid}'],
        'ads_count':len(ads),'employer_count':len({a['employer_orgnr'] for a in ads}),
        'failed_details':0,'seeded_from_disk':len(ads),'fresh_fetched_ads':0,'ads':ads,**overrides}
    path=tmp_path/'index.json.gz';write(path,data);return path,data


@pytest.mark.parametrize('detail_denied',[False,True])
def test_cached_credentials_fallback_and_detail_denial(tmp_path,monkeypatch,detail_denied):
    path,_=artifact(tmp_path);cfg=config(tmp_path,[ORG],hiring=True,nav_index_path=path,nav_max_details=4)
    expired=TOKEN+'old';monkeypatch.setenv('NAV_API_TOKEN',expired)
    index=Index();calls=[]
    async def names():return {ORG:{'Rareone AS'}}
    names.initial_names={ORG:{'Rareone AS'}}
    def response(request):
        calls.append(request.url.path)
        if request.url.path=='/api/publicToken':return httpx.Response(200,text=TOKEN)
        if request.headers.get('Authorization')=='Bearer '+expired:return httpx.Response(401)
        if '/feedentry/' in request.url.path:
            return httpx.Response(403) if detail_denied else httpx.Response(200,json=ad(UUID,ORG))
        return httpx.Response(200,json={'items':[],'next_url':None})
    async def gate():
        async with httpx.AsyncClient(transport=httpx.MockTransport(response)) as client:
            await prefetch(client,cfg,Budget(cfg),BlobStore(cfg.state_dir),index,names)
    asyncio.run(gate())
    assert calls.count('/api/publicToken')==1
    assert index.blocked==detail_denied
    assert index.complete== (not detail_denied)
    assert index.reason==('token_unavailable' if detail_denied else 'complete')


def test_load_version_age_counts_and_personal_text_schema(tmp_path):
    path,data=artifact(tmp_path)
    assert load(path)[0]==data
    with pytest.raises(SourceFailure,match='index_missing'):load(tmp_path/'missing')
    old={**data,'built_at':(datetime.now(timezone.utc)-timedelta(days=22)).isoformat()}
    write(path,old)
    with pytest.raises(SourceFailure,match='index_stale'):load(path)
    assert load(path,max_age_days=23)[0]==old
    with pytest.raises(SourceFailure,match='index_version_invalid'):validate({**data,'schema_version':2})
    with pytest.raises(SourceFailure,match='index_ad_schema_invalid'):
        validate({**data,'ads':[{**data['ads'][0],'description':'must never ship'}]})
    shipped,_=load(DEFAULT_PATH,max_age_days=100000)
    assert DEFAULT_PATH.stat().st_size<1_000_000 and shipped['failed_details']==0
    assert all(set(a)==AD_FIELDS for a in shipped['ads'])


async def execute(cfg,path,details=None,items=None,scopes=None,feed_error=False,token_ok=True):
    index=Index();blobs=BlobStore(cfg.state_dir);calls=[]
    async def names():return {ORG:{'Rareone AS'}}
    async def scope():return scopes or {ORG:{ORG}}
    names.initial_names={ORG:{'Rareone AS'}};names.scopes_ready=scope
    def response(request):
        calls.append(request.url.path)
        if request.url.path=='/api/publicToken':return httpx.Response(200,text=TOKEN if token_ok else 'not available')
        if '/feedentry/' in request.url.path:
            uuid=request.url.path.rsplit('/',1)[-1]
            value=(details or {}).get(uuid,ad(uuid,ORG))
            return httpx.Response(503,json={}) if value is None else httpx.Response(200,json=value)
        if feed_error:return httpx.Response(400,json={})
        return httpx.Response(200,json={'items':items or [],'next_url':None})
    async with httpx.AsyncClient(transport=httpx.MockTransport(response)) as client:
        await prefetch(client,cfg,Budget(cfg),blobs,index,names)
    row=placeholder(ORG,'test',utc_now(),('identity','roles','subunits','accounts','hiring'))
    row.run.sections['subunits']='not_available'
    if scopes and SUB in scopes[ORG]:
        from signalpost.sources.extract import Section,Source,add
        s=Section();body=json.dumps({'unit':SUB}).encode();sha=blobs.put(body)
        add(s,Source('https://data.brreg.no/example',body,sha,utc_now()),ORG,'subunits','subunits.unit.'+SUB,{'organisation_number':SUB},'/unit')
        row.claims.extend(s.claims);row.evidence.extend(s.evidence);row.run.sections['subunits']='available'
    result=section(row,index,blobs)
    return index,result,calls


@pytest.mark.parametrize('kind',['valid','inactive','expired','foreign','missing_detail'])
def test_every_published_index_candidate_requires_live_exact_detail(tmp_path,kind):
    path,_=artifact(tmp_path);cfg=config(tmp_path,[ORG],hiring=True,nav_index_path=path)
    value=ad(UUID,OTHER if kind=='foreign' else ORG)
    if kind=='inactive':value['status']='INACTIVE'
    if kind=='expired':value['ad_content']['expires']='2020-01-01T00:00:00Z'
    if kind=='missing_detail':value=None
    index,result,calls=asyncio.run(execute(cfg,path,{UUID:value}))
    assert '/api/v1/feedentry/'+UUID in calls
    assert index.metrics['source_mode']=='declared_index' and index.metrics['feed_complete']
    assert result.state==('available' if kind=='valid' else 'failed' if kind=='missing_detail' else 'not_available')
    if kind=='valid':
        claim=result.claims[0];assert claim.value['employer_orgnr']==ORG
        assert json.loads(result.evidence[0].source_identifier)['candidate_origin']=='declared_cache'
        assert len(claim.evidence_ids)==1 and result.evidence[0].source_url.endswith('/feedentry/'+UUID)
        assert result.evidence[0].content_sha256 and len(result.evidence[0].claim_span)<=300
    else:assert not result.claims
    if kind in {'inactive','expired'}:assert UUID in index.live_closed


def test_exact_subunit_match_and_forward_new_item(tmp_path):
    a={'uuid':UUID,'employer_orgnr':SUB,'status':'ACTIVE','published':None,'expires':None,'last_modified':None,'etag':None}
    path,_=artifact(tmp_path,[a]);cfg=config(tmp_path,[ORG],hiring=True,nav_index_path=path)
    index,result,_=asyncio.run(execute(cfg,path,{UUID:ad(UUID,SUB),SECOND:ad(SECOND,ORG)},
        [header(SECOND,'Rareone AS')],{ORG:{ORG,SUB}}))
    assert result.state=='available' and len(result.claims)==2
    assert {json.loads(e.source_identifier)['candidate_origin'] for e in result.evidence}=={'declared_cache','forward_feed'}
    assert any(c.value['matched_via']=='subunit '+SUB for c in result.claims)


def test_incomplete_forward_feed_never_establishes_absence(tmp_path):
    path,_=artifact(tmp_path,[]);cfg=config(tmp_path,[ORG],hiring=True,nav_index_path=path)
    index,result,_=asyncio.run(execute(cfg,path,feed_error=True))
    assert result.state=='failed' and not index.metrics['feed_complete']
    index,result,_=asyncio.run(execute(cfg,path,token_ok=False))
    assert result.state=='blocked'


def test_stale_index_falls_back_to_full_feed(tmp_path):
    path,_=artifact(tmp_path,[],built_at='2020-01-01T00:00:00Z')
    cfg=config(tmp_path,[ORG],hiring=True,nav_index_path=path)
    index,result,calls=asyncio.run(execute(cfg,path))
    assert index.metrics['source_mode']=='full_feed_fallback'
    assert index.metrics['index_fallback_reason']=='index_stale'
    assert '/api/v1/feed' in calls and result.state=='not_available'


def test_forward_inactive_is_not_itself_live_closure_proof(tmp_path):
    path,_=artifact(tmp_path);cfg=config(tmp_path,[ORG],hiring=True,nav_index_path=path)
    item=header(UUID,'Rareone AS');item['_feed_entry']['status']='INACTIVE'
    index,result,_=asyncio.run(execute(cfg,path,{UUID:None},[item]))
    assert UUID in index.closed and UUID not in index.live_closed
    assert result.state=='failed' and not result.claims


def test_index_cannot_publish_from_cached_dates_or_employer_alone(tmp_path):
    path,_=artifact(tmp_path);cfg=config(tmp_path,[ORG],hiring=True,nav_index_path=path,nav_max_details=0)
    index,result,calls=asyncio.run(execute(cfg,path))
    assert result.state=='failed' and not result.claims
    assert not any('/feedentry/' in url for url in calls)


def test_index_version_is_provenance_not_a_changed_ad_fact(tmp_path):
    path,data=artifact(tmp_path);cfg=config(tmp_path,[ORG],hiring=True,nav_index_path=path)
    _,first,_=asyncio.run(execute(cfg,path))
    write(path,{**data,'index_version':'test-v2'})
    _,second,_=asyncio.run(execute(cfg,path))
    assert first.claims[0].id==second.claims[0].id and first.claims[0].value==second.claims[0].value
    assert first.evidence[0].source_identifier!=second.evidence[0].source_identifier


def test_refresh_closure_has_live_evidence_and_no_unverified_ad_carry(tmp_path):
    from signalpost.runner import run
    from tests.test_registry import handler
    path,_=artifact(tmp_path)
    async def one(label,value,previous=None):
        cfg=config(tmp_path/label,[ORG],hiring=True,nav_index_path=path,previous=previous)
        def response(request):
            if request.url.host!='pam-stilling-feed.nav.no':return handler()(request)
            if request.url.path=='/api/publicToken':return httpx.Response(200,text=TOKEN)
            if '/feedentry/' in request.url.path:
                return httpx.Response(503,json={}) if value is None else httpx.Response(200,json=value)
            return httpx.Response(200,json={'items':[],'next_url':None})
        async with httpx.AsyncClient(transport=httpx.MockTransport(response)) as client:report=await run(cfg,client)
        return cfg,json.loads(cfg.output.read_text()),report
    first,_,_=asyncio.run(one('first',ad(UUID,ORG)))
    _,closed,_=asyncio.run(one('closed',{'uuid':UUID,'status':'INACTIVE'},first.output))
    event=next(e for e in closed['changes'] if e['type']=='closed_job')
    assert event['new_evidence_ids'] and event['new_content_sha256']
    proof=next(e for e in closed['evidence'] if e['id']==event['new_evidence_ids'][0])
    assert proof['locator']=='/status' and 'INACTIVE' in proof['claim_span']
    assert proof['content_sha256']==event['new_content_sha256']
    for label,value in [('foreign',ad(UUID,OTHER)),('unverified',None)]:
        _,row,report=asyncio.run(one(label,value,first.output))
        assert not any(e['type']=='closed_job' for e in row['changes'])
        assert report['observation_changes']>0
        assert not any(c['family']=='hiring' and c['availability']=='available' for c in row['claims'])

