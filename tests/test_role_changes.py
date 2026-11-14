import asyncio
import hashlib
import json
from types import SimpleNamespace
from urllib.parse import urlsplit,parse_qs
import pytest

from signalpost.sources import role_changes as roles,registry_changes as rc
from signalpost.sources.http import Response
from signalpost.budget import SourceFailure
from signalpost.runner import placeholder
from signalpost.models.evidence import Evidence
from scripts.verify_output import verify_registry_events

ORG='923609016';OTHER='993578843';SINCE='2023-11-14T00:00:00Z';NOW='2026-11-14T00:00:00Z'


def event(ident=10,org=ORG,**extra):
    return {'specversion':'1.0','id':str(ident),'source':rc.BASE+'enheter/'+org+'/roller',
        'type':'no.brreg.enhetsregisteret.rolle.oppdatert','time':'2026-10-01T12:30:00Z','data':{'organisasjonsnummer':org},**extra}


def response(rows,url=roles.ENDPOINT+'?size=1000'):
    body=json.dumps(rows).encode();return Response(body,200,url,NOW,hashlib.sha256(body).hexdigest())


def test_exact_event_unknown_role_person_and_stable_refresh_identity():
    raw=event(data={'organisasjonsnummer':ORG,'personnavn':'Unpublished person','rolletype':'DAGL'})
    first=roles.extract(raw,response([raw]),'/0',ORG)
    second=roles.extract(raw,response([raw]),'/0',ORG)
    c=first.claims[0]
    assert c.id==second.claims[0].id and c.value==second.claims[0].value
    assert c.value['role_type'] is None and c.value['person_name'] is None
    assert 'Unpublished person' not in json.dumps(c.value)
    assert c.value['change_type']=='updated' and c.value['date']==raw['time']
    assert 'not effective date' in rc.sentence(c.value)
    assert all(e.effective_at is None for e in first.evidence)
    data={'claims':[c.model_dump(mode='json')],'evidence':[e.model_dump(mode='json') for e in first.evidence]}
    verify_registry_events({'organisation_number':ORG},data,{e['id']:e for e in data['evidence']},lambda _:response([raw]).body.decode())
    data['claims'][0]['value']['role_type']='DAGL'
    with pytest.raises(AssertionError):verify_registry_events({'organisation_number':ORG},data,{e['id']:e for e in data['evidence']},lambda _:response([raw]).body.decode())


@pytest.mark.parametrize('change',[{'data':{'organisasjonsnummer':OTHER}}, {'source':rc.BASE+'enheter/'+OTHER+'/roller'},
    {'id':True},{'id':'0'},{'time':'unknown'},{'specversion':True},{'type':'some.other.event'}])
def test_invalid_or_foreign_events_rejected(change):
    with pytest.raises(SourceFailure):roles.extract(event(**change),response([]),'/0',ORG)


def test_pagination_uses_exact_max_cursor_without_skipping_consecutive_ids(monkeypatch):
    monkeypatch.setattr(roles,'PAGE_SIZE',2)
    calls=[]
    class Http:
        async def get(self,url,org):
            calls.append(url);query=parse_qs(urlsplit(url).query)
            assert query['organisasjonsnummer']==[ORG]
            return response([event(10),event(11)] if 'afterTime' in query else [event(12)],url)
    async def run():return [e async for e,_,_ in roles.pages(Http(),[ORG],SINCE,NOW)]
    assert [e['id'] for e in asyncio.run(run())]==['10','11','12']
    assert parse_qs(urlsplit(calls[1]).query)['afterId']==['11']


def test_duplicate_event_dedup_and_conflicting_duplicate_rejected():
    class Http:
        async def get(self,url,org):return response([event(),event()],url)
    async def run(http):return [e async for e,_,_ in roles.pages(http,[ORG],SINCE,NOW)]
    assert len(asyncio.run(run(Http())))==1
    class Bad:
        async def get(self,url,org):return response([event(),event(time='2026-09-01T00:00:00Z')],url)
    with pytest.raises(SourceFailure,match='role_change_conflicting_event'):asyncio.run(run(Bad()))


def test_repeated_cursor_page_stops_and_future_event_does_not_publish(monkeypatch):
    monkeypatch.setattr(roles,'PAGE_SIZE',1)
    class Http:
        async def get(self,url,org):return response([event()],url)
    async def run():return [e async for e,_,_ in roles.pages(Http(),[ORG],SINCE,NOW)]
    with pytest.raises(SourceFailure,match='role_change_pagination_repeated'):asyncio.run(run())
    monkeypatch.setattr(roles,'PAGE_SIZE',1000)
    class Future:
        async def get(self,url,org):return response([event(time='2027-01-01T00:00:00Z')],url)
    async def future():return [e async for e,_,_ in roles.pages(Future(),[ORG],SINCE,NOW)]
    assert asyncio.run(future())==[]


def test_shared_cap_and_source_namespace_prevent_id_collision():
    env=placeholder(ORG,'roles-test',NOW,('identity','roles','activity'))
    env.claims=[]
    for i in range(1,65):
        section=roles.extract(event(i),response([event(i)]),'/0',ORG)
        env.claims.extend(section.claims);env.evidence.extend(section.evidence)
    entity={'organisasjonsnummer':ORG,'oppdateringsid':64,'dato':'2026-10-01T12:30:00Z','endringstype':'Endring'}
    section=rc.extract(entity,response({'x':entity}),'/x',ORG,'enheter')
    env.claims.extend(section.claims);env.evidence.extend(section.evidence)
    rc.cap_envelope(env)
    assert len(env.claims)==50 and sum(c.value['event_id']==64 for c in env.claims)==2
    first=[c.id for c in env.claims];rc.cap_envelope(env);assert [c.id for c in env.claims]==first
    assert [c.value['event_id'] for c in env.claims]==sorted((c.value['event_id'] for c in env.claims),reverse=True)


def test_budget_failure_explicit_and_never_changes_other_family():
    class Http:
        async def get(self,*args):raise SourceFailure('budget_exhausted')
    result=asyncio.run(roles.collect({ORG:object()},Http(),SINCE,NOW))
    assert result[ORG].state=='failed' and result[ORG].errors[0].code=='budget_exhausted'
