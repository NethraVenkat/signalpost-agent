"""Controlled transitions through the actual runner, not only the diff helper."""
import asyncio
import json
import httpx
import pytest
from signalpost.runner import run
from signalpost.models.shapes import validate
from tests.test_registry import config,handler,entity
from tests.test_websites import html,OUR


def test_registry_changes_failures_recovery_and_duplicate_idempotency(tmp_path):
    base=handler(missing_accounts=False)
    def source(version=0,failure=None):
        def dispatch(request):
            if request.url.path=='/enhetsregisteret/api/enheter/'+OUR:
                if failure=='timeout':raise httpx.ReadTimeout('declared transition',request=request)
                if failure=='dns':raise httpx.ConnectError('declared DNS failure',request=request)
                if isinstance(failure,int):return httpx.Response(failure)
                value=entity(OUR)
                if version:
                    value['navn']='Example Renamed AS'
                    value['forretningsadresse']['adresse']=['New address 12']
                return httpx.Response(200,json=value)
            if version and '/regnskapsregisteret/' in request.url.path:
                return httpx.Response(200,json=[{'regnskapstype':'SELSKAP','virksomhet':{'organisasjonsnummer':OUR},
                    'regnskapsperiode':{'fraDato':'2026-01-01','tilDato':'2026-12-31'},'valuta':'NOK',
                    'resultatregnskapResultat':{'aarsresultat':123}}])
            return base(request)
        return dispatch
    async def one(label,dispatch,previous=None):
        cfg=config(tmp_path/label,[OUR,OUR],previous=previous)
        async with httpx.AsyncClient(transport=httpx.MockTransport(dispatch)) as client:
            report=await run(cfg,client)
        rows=[json.loads(x) for x in cfg.output.read_text(encoding='utf8').splitlines()]
        assert [r['organisation_number'] for r in rows]==[OUR,OUR]
        assert rows[0]['claims']==rows[1]['claims']
        for row in rows:validate(row,'union')
        return cfg,report,rows[0]
    async def scenario():
        first,_,baseline=await one('baseline',source())
        changed,_,row=await one('changed',source(1),first.output)
        events={e['field']:e for e in row['changes']}
        assert events['identity.legal_name']['new_value']=='Example Renamed AS'
        assert events['identity.legal_name']['old_value']==next(c['value'] for c in baseline['claims'] if c['field']=='identity.legal_name')
        assert events['identity.registered_address']['new_value']['adresse']==['New address 12']
        assert events['accounts.net_result']['new_value']==123
        assert events['accounts.net_result']['old_value']==0
        for e in events.values():
            assert e['old_evidence_ids'] and e['new_evidence_ids']
            assert e['old_content_sha256'] and e['new_content_sha256']
            assert e['last_observed_at'].endswith('Z')
        _,report,unchanged=await one('unchanged',source(1),changed.output)
        assert report['changes']==report['observation_changes']==0
        for failure in [429,503,'dns','timeout']:
            failed,report,row=await one(str(failure),source(1,failure),changed.output)
            assert not any(e['field'].startswith('identity.') for e in row['changes'])
            carried=next(c for c in row['claims'] if c['field']=='identity.legal_name')
            previous_row=json.loads(changed.output.read_text(encoding='utf8').splitlines()[0])
            original=next(c for c in previous_row['claims'] if c['field']==carried['field'])
            assert carried['carried_forward'] and carried['value']==original['value']
            assert carried['last_observed_at']==original['last_observed_at']
            assert carried['evidence_ids']==original['evidence_ids']
            # Identity failure deliberately blocks dependent registry calls.
            assert row['run']['sections']['accounts'] in {'blocked','failed'}
            _,report,recovered=await one(str(failure)+'-recovered',source(1),failed.output)
            assert report['changes']==0 and report['observation_changes']>0
            assert not next(c for c in recovered['claims'] if c['field']=='identity.legal_name')['carried_forward']
        def partial(request):
            if request.url.path.endswith('/roller'):return httpx.Response(503)
            return source(1)(request)
        partial_cfg,_,row=await one('partial-roles',partial,changed.output)
        assert row['run']['sections']['roles']=='failed'
        assert row['run']['sections']['accounts']=='available'
        assert not any(e['field']=='roles.roles' for e in row['changes'])
        _,report,_=await one('partial-recovery',source(1),partial_cfg.output)
        assert report['changes']==0 and report['observation_changes']>0
    asyncio.run(scenario())


def test_changed_website_contact_then_dns_failure_and_recovery(tmp_path,monkeypatch):
    from signalpost.web import policy
    from signalpost.budget import SourceFailure
    dns_failed=False
    async def resolve(host,port=443):
        if dns_failed:raise SourceFailure('dns_error')
        return ['93.184.216.34']
    monkeypatch.setattr(policy,'resolve_public',resolve)
    async def one(label,domain,contact,previous=None):
        cfg=config(tmp_path/label,[OUR],websites=True,previous=previous)
        def dispatch(request):
            if request.url.host=='data.brreg.no':
                if request.url.path=='/enhetsregisteret/api/enheter/'+OUR:
                    body=entity(OUR);body['hjemmeside']='https://'+domain+'/';return httpx.Response(200,json=body)
                return handler()(request)
            if request.url.path=='/robots.txt':return httpx.Response(200,text='User-agent: *\nAllow: /')
            assert request.url.host==domain
            return httpx.Response(200,text=html(extra=f'<a href="mailto:{contact}">Office</a>'))
        async with httpx.AsyncClient(transport=httpx.MockTransport(dispatch)) as client:report=await run(cfg,client)
        return cfg,report,json.loads(cfg.output.read_text(encoding='utf8'))
    async def scenario():
        nonlocal dns_failed
        first,_,_=await one('first','example.no','office@example.no')
        second,report,row=await one('second','changed-example.no','office@changed-example.no',first.output)
        event=next(e for e in row['changes'] if e['field']=='official_website')
        assert event['old_value']['final_url']=='https://example.no'
        assert event['new_value']['final_url']=='https://changed-example.no'
        assert any(e['field'].startswith('contact.email.') and e['type']=='added' for e in row['changes'])
        dns_failed=True
        failed,_,row=await one('failed','changed-example.no','office@changed-example.no',second.output)
        assert not any(e['field']=='official_website' or e['field'].startswith('contact.') for e in row['changes'])
        assert any(c['carried_forward'] for c in row['claims'] if c['family']=='website')
        dns_failed=False
        _,report,_=await one('recovered','changed-example.no','office@changed-example.no',failed.output)
        assert report['changes']==0
    asyncio.run(scenario())


def test_cancelled_runner_restart_preserves_input_multiplicity(tmp_path):
    cfg=config(tmp_path,[OUR,OUR])
    async def scenario():
        entered=asyncio.Event();release=asyncio.Event()
        async def blocked(request):entered.set();await release.wait();return handler()(request)
        async with httpx.AsyncClient(transport=httpx.MockTransport(blocked)) as client:
            task=asyncio.create_task(run(cfg,client));await entered.wait();task.cancel()
            try:await task
            except asyncio.CancelledError:pass
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler())) as client:
            report=await run(cfg,client)
        rows=[json.loads(x) for x in cfg.output.read_text(encoding='utf8').splitlines()]
        assert report['emitted_envelopes']==2
        assert [r['organisation_number'] for r in rows]==[OUR,OUR]
        assert rows[0]['claims']==rows[1]['claims']
        assert all(not r['changes'] for r in rows)
        for row in rows:validate(row,'union')
    asyncio.run(scenario())
