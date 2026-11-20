import asyncio
import json
import time
from datetime import datetime, timedelta, timezone
import httpx
import pytest
import respx
from scripts.verify_output import verify
from signalpost.runner import run
from signalpost.sources import nav
from signalpost.web import adaptive, collector, policy
from signalpost.web.candidates import Candidate, generate
from tests.test_registry import config, handler, entity
from tests.test_websites import OUR, OTHER, html

UUID='00000000-0000-4000-8000-000000000001'


def exercise(tmp_path, monkeypatch, *, first='missing', cap=8, global_cap=None, deadline=False,
             public_activity=False, registry=False, extra_budget=False):
    cfg=config(tmp_path,[OUR],websites=True,hiring=True,adaptive_websites=True,
               website_request_cap=cap,max_requests=global_cap,
               public_activity=public_activity,registry_changes=registry,adaptive_extra_budget=extra_budget)
    cfg=cfg.model_copy(update={'website_politeness_seconds':0})
    calls=[];pass1_done=asyncio.Event();original=collector.fetch
    async def collect(*args,**kwargs):
        section=await original(*args,**kwargs)
        if not kwargs.get('resume'):pass1_done.set()
        return section
    monkeypatch.setattr(collector,'fetch',collect)
    async def public(host,port=443):return ['93.184.216.34']
    monkeypatch.setattr(policy,'resolve_public',public)
    async def late_nav(client,config,budget,blobs,index,names_ready,previous):
        index.started.set()
        await pass1_done.wait()
        now=datetime.now(timezone.utc)
        homepage='https://missing.no/new-home' if first in {'veto','robots'} else 'https://good.no/'
        published=(now-timedelta(days=1)).isoformat();expires=(now+timedelta(days=30)).isoformat()
        raw={'uuid':UUID,'status':'ACTIVE','ad_content':{'uuid':UUID,'title':'Verified vacancy',
            'published':published,'expires':expires,'employer':{'orgnr':OUR,'homepage':homepage}}}
        sha=blobs.put(json.dumps(raw).encode())
        value={'uuid':UUID,'employer_orgnr':OUR,'title':'Verified vacancy','published':published,
            'expires':expires,'location':None,'occupation_categories':None,
            'url':'https://arbeidsplassen.nav.no/stillinger/stilling/'+UUID}
        index.ads[OUR]=[nav.Ad(value,sha,nav.BASE+'/api/v1/feedentry/'+UUID,
            now.isoformat().replace('+00:00','Z'),None,None,None,None)]
        index.complete=True;index.reason='complete'
        if deadline:
            import time
            budget.deadline=time.monotonic()-.001
    monkeypatch.setattr(nav,'prefetch',late_nav)
    if registry:
        from signalpost.sources import registry_changes as rc
        from tests.test_registry_changes import event, response as event_response
        async def feed(envelopes,http,blobs,started):
            raw=event();source=event_response({'event':raw});blobs.put(source.body)
            for envelope in envelopes.values():
                envelope.run.refresh['registry_activity']={'state':'available','errors':[]}
            return {OUR:rc.extract(raw,source,'/event',OUR,'enheter')}
        monkeypatch.setattr(rc,'fetch_batch',feed)
    def response(request):
        calls.append(str(request.url))
        if request.url.host=='data.brreg.no':
            if request.url.path.endswith('/enheter/'+OUR):
                data=entity(OUR);data['navn']='Example AS';data['hjemmeside']='https://missing.no/'
                return httpx.Response(200,json=data)
            return handler()(request)
        if request.url.path=='/robots.txt':
            return httpx.Response(200,text='User-agent: *\nDisallow: /' if first=='robots' and request.url.host=='missing.no' else 'User-agent: *\nAllow: /')
        if request.url.host=='missing.no':
            return httpx.Response(200,text=html('Org nr '+OTHER,title='Unrelated')) if first=='veto' else httpx.Response(404)
        if request.url.host=='good.no':
            return httpx.Response(200,text=html('Org nr '+OUR,
                extra='<footer><a href="https://www.linkedin.com/company/90123/">LinkedIn</a></footer>',title='Example AS'))
        return httpx.Response(404)
    with respx.mock(assert_all_called=False) as router:
        router.route().mock(side_effect=response)
        report=asyncio.run(run(cfg))
    row=json.loads(cfg.output.read_text(encoding='utf8').splitlines()[0])
    return report,row,calls,cfg


def test_late_verified_nav_nomination_gains_exact_website_and_social_with_same_receipts(tmp_path,monkeypatch):
    report,row,calls,cfg=exercise(tmp_path,monkeypatch)
    meter=report['adaptive_websites']
    assert meter['pass1']['verified_websites']==0 and meter['pass2']['websites_gained']==1
    assert meter['pass2']['requests']==2
    assert meter['pass1']['requests']+meter['pass2']['requests']==report['requests']
    assert sum(e['pass']=='pass2' for e in report['request_log'])==2
    website=next(c for c in row['claims'] if c['field']=='official_website')
    assert website['value']['identity_level']=='VERIFIED'
    assert website['value']['candidate_origin']=='nav_employer_homepage'
    assert any(c['field'].startswith('social_profile.') for c in row['claims'])
    assert sum('missing.no' in url for url in calls)==2
    result=verify(cfg.output,cfg.state_dir,1,cfg.organisations,cfg.report)
    assert result['synthesis_unverified_values']==0


@pytest.mark.parametrize('first',['veto','robots'])
def test_pass2_never_retries_vetoed_or_robots_denied_domain_even_at_another_path(tmp_path,monkeypatch,first):
    report,row,calls,_=exercise(tmp_path,monkeypatch,first=first)
    assert report['adaptive_websites']['pass2']['requests']==0
    assert not any('/new-home' in url for url in calls)
    assert not any(c['field']=='official_website' for c in row['claims'])


@pytest.mark.parametrize('kwargs,state',[({'cap':2},'website_budget_exhausted'),
                                       ({'global_cap':6},'budget_exhausted')])
def test_second_pass_never_resets_company_or_global_counters(tmp_path,monkeypatch,kwargs,state):
    report,row,calls,_=exercise(tmp_path,monkeypatch,**kwargs)
    assert report['adaptive_websites']['pass2']['requests']==0
    assert report['adaptive_websites']['pass2']['per_company'][OUR]['state']==state
    assert any(e['code']==state for e in row['errors'])
    assert not any('good.no' in url for url in calls)
    assert report['requests']<=kwargs.get('global_cap',7)


@pytest.mark.parametrize('mutation',['owner','expired','inactive','missing_body'])
def test_nav_index_or_foreign_stale_detail_alone_cannot_nominate(tmp_path,mutation):
    from tests.test_synthesis import envelope
    from signalpost.sources.blobstore import BlobStore
    row,cfg=envelope(tmp_path);blobs=BlobStore(cfg.state_dir);index=nav.Index()
    now=datetime.now(timezone.utc);body={'uuid':UUID,'status':'ACTIVE','ad_content':{
        'uuid':UUID,'published':(now-timedelta(days=1)).isoformat(),
        'expires':(now+timedelta(days=1)).isoformat(),'employer':{'orgnr':OUR,'homepage':'https://good.no'}}}
    if mutation=='owner':body['ad_content']['employer']['orgnr']=OTHER
    elif mutation=='expired':body['ad_content']['expires']=(now-timedelta(days=1)).isoformat()
    elif mutation=='inactive':body['status']='INACTIVE'
    sha=blobs.put(json.dumps(body).encode()) if mutation!='missing_body' else '0'*64
    index.ads[OUR]=[nav.Ad({'uuid':UUID,'employer_orgnr':OUR},sha,'https://nav.invalid',
        '2026-11-13T00:00:00Z',None,None,None,None)]
    assert adaptive.nav_homepages(row,index,blobs)==[]


def test_candidates_rank_authoritative_nomination_above_name_and_preserve_eight_first_pass_limit():
    context={'name':'Example Business AS','website':'registered.no','email':'x@email.no',
        'subunits':[{'orgnr':OTHER,'website':'branch.no'}],
        'nav_homepages':[{'url':'https://navnominee.no'}]}
    candidates=generate(context)
    assert [c.origin for c in candidates[:6]]==['registry_website','registry_email','legal_name_slug','legal_name_slug','subunit_registry_website','nav_employer_homepage']
    assert len(candidates)<=8 and len(generate(context,limit=32))<=32
    assert adaptive.priority(candidates[1])>adaptive.priority(Candidate('https://guess.no','guess.no','legal_name_slug'))


def test_pass2_keeps_original_deadline_and_emits_cutoff_state(tmp_path,monkeypatch):
    report,row,calls,_=exercise(tmp_path,monkeypatch,deadline=True)
    assert report['adaptive_websites']['stop_reason']=='deadline'
    assert report['adaptive_websites']['pass2']['requests']==0
    assert any(e['code']=='deadline' for e in row['errors'])
    assert not any('good.no' in url for url in calls)


def test_optional_pass2_cuts_inflight_website_work_and_leaves_exact_id_running(tmp_path, monkeypatch):
    from signalpost.sources import exact_public

    original_run = adaptive.run
    original_fetch = collector.fetch
    started = asyncio.Event()
    cancelled = asyncio.Event()
    exact_progress = []

    async def timed(envelopes, http, *args):
        http.budget.pass2_cutoff = time.monotonic() + 0.4
        return await original_run(envelopes, http, *args)

    async def hold_website(*args, **kwargs):
        if not kwargs.get('resume'):
            return await original_fetch(*args, **kwargs)
        started.set()
        try:
            await asyncio.sleep(3)
        finally:
            cancelled.set()

    async def finish_exact(envelopes, client, config, budget, blobs, update):
        await started.wait()
        exact_progress.append((budget.phase, budget.website_deadline == budget.deadline))
        await cancelled.wait()
        event = budget.reserve('https://api.gleif.org/api/v1/lei-records', 'api.gleif.org', OUR)
        event.update(section='gleif', status=404)
        # asyncio may dispatch a timer early within the loop clock resolution.
        # The cancellation handshake establishes the order of these events.
        exact_progress.append((event['pass'], budget.website_deadline == budget.deadline))

    monkeypatch.setattr(adaptive, 'run', timed)
    monkeypatch.setattr(collector, 'fetch', hold_website)
    monkeypatch.setattr(exact_public, 'enrich', finish_exact)
    report, row, _, cfg = exercise(tmp_path, monkeypatch)

    assert exact_progress == [('pass1', True), ('pass1', True)]
    assert cfg.report.is_file() and cfg.output.is_file() and report['emitted_envelopes'] == 1
    assert report['adaptive_websites']['stop_reason'] == 'deadline'
    pass2 = report['adaptive_websites']['pass2']
    assert pass2['per_company'][OUR]['state'] == 'deadline' and pass2['runtime_seconds'] < 3
    assert pass2['requests'] == 0 and report['adaptive_websites']['pass1']['requests'] == report['requests']
    assert any(e['section'] == 'website' and e['code'] == 'deadline' for e in row['errors'])


def test_pass2_cannot_raise_dns_nomination_ceiling():
    from types import SimpleNamespace
    cfg=SimpleNamespace(dns_precheck=True)
    http=SimpleNamespace(config=cfg,dns_counts={OUR:8},dns_cache={},dns_nominations=set())
    candidate=Candidate('https://guess.no','guess.no','legal_name_slug')
    assert not adaptive.dns_room(http,OUR,candidate)
    http.dns_cache['guess.no']=['93.184.216.34']
    assert adaptive.dns_room(http,OUR,candidate)
    assert http.dns_counts[OUR]==8


def test_adaptive_exception_preserves_mandatory_output_and_is_reported(tmp_path,monkeypatch):
    async def broken(*args,**kwargs):raise RuntimeError('synthetic scheduler error')
    monkeypatch.setattr(adaptive,'run',broken)
    report,row,_,cfg=exercise(tmp_path,monkeypatch)
    assert report['adaptive_websites']['state']=='failed'
    assert 'adaptive website pass failed: RuntimeError' in report['warnings']
    assert row['organisation_number']==OUR and cfg.output.exists() and cfg.report.exists()


def test_new_pass2_website_activity_cannot_drop_existing_registry_activity(tmp_path,monkeypatch):
    report,row,_,cfg=exercise(tmp_path,monkeypatch,public_activity=True,registry=True)
    assert report['adaptive_websites']['pass2']['websites_gained']==1
    assert any(c['field'].startswith('registry_change.') and c['availability']=='available' for c in row['claims'])
    assert row['run']['sections']['activity']=='available'  # The verified registry timeline remains available.
    assert any(e['section']=='activity' and e['code']=='website_budget_exhausted' for e in row['errors'])
    assert verify(cfg.output,cfg.state_dir,1,cfg.organisations,cfg.report)['synthesis_unverified_values']==0


def test_replacing_website_proof_does_not_authorize_previous_sites_activity(tmp_path):
    from tests.test_synthesis import envelope
    row,_=envelope(tmp_path)
    seed=next(c for c in row.claims if c.field=='identity.legal_name')
    current=seed.model_copy(update={'field':'official_website','family':'website','id':'current-proof'})
    stale=seed.model_copy(update={'field':'dated_item.old','family':'activity','id':'stale',
        'value':{'identity_claim_id':'old-proof'}})
    supported=seed.model_copy(update={'field':'dated_item.new','family':'activity','id':'supported',
        'value':{'identity_claim_id':'current-proof'}})
    formal=seed.model_copy(update={'field':'registry_change.example','family':'activity','id':'formal'})
    row.claims.extend([current,stale,supported,formal])
    adaptive.discard_stale_activity(row)
    assert 'stale' not in {c.id for c in row.claims}
    assert {'current-proof','supported','formal'}<={c.id for c in row.claims}


def test_planning_skip_keeps_completed_pass1_scope_and_explicit_pass2_budget_state(tmp_path):
    from tests.test_synthesis import envelope
    from signalpost.budget import Budget
    from signalpost.sources.blobstore import BlobStore
    from signalpost.web.fetcher import WebsiteHttp
    row,cfg=envelope(tmp_path);row.run.sections['website']='not_available'
    async def go():
        async with httpx.AsyncClient() as client:
            http=WebsiteHttp(client,cfg,Budget(cfg),BlobStore(cfg.state_dir))
            http.counts[OUR]=8
            http.discovery_sessions[OUR]={'context':{'name':'Example AS'},'attempted':set(),'vetoed':set()}
            def no_update(*args):pytest.fail('A planning skip must not overwrite the completed source check')
            async def no_activity(*args):pytest.fail('No new website was proved')
            return await adaptive.run({OUR:row},http,nav.Index(),{}, {},no_update,no_activity)
    result=asyncio.run(go())
    assert result['pass2']['requests']==0
    assert result['pass2']['per_company'][OUR]['state']=='website_budget_exhausted'
    assert any(e.code=='website_budget_exhausted' for e in row.errors)
    assert row.run.sections['website']=='not_available'
