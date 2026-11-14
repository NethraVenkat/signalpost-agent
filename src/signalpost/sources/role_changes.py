"""Public exact-company role-update CloudEvents; no inferred role/person changes."""
import asyncio
import json
from urllib.parse import urlencode

from ..budget import SourceFailure
from ..models.evidence import digest
from ..workers import offload
from .extract import Section,add,missing,response_source
from .registry_changes import BASE,CHUNK,PAGE_SIZE,DATE_LABEL,timestamp

METHOD='signalpost.role_changes.v1'
ENDPOINT=BASE+'oppdateringer/roller'


def validate(event,numbers):
    if not isinstance(event,dict) or isinstance(event.get('specversion'),bool) or event.get('specversion') not in {'1.0',1}:
        raise SourceFailure('role_change_invalid_event')
    ident=event.get('id')
    if isinstance(ident,bool) or not str(ident).isdigit() or int(ident)<1:
        raise SourceFailure('role_change_invalid_id')
    data=event.get('data')
    org=data.get('organisasjonsnummer') if isinstance(data,dict) else None
    if org not in numbers or event.get('source')!=BASE+'enheter/'+org+'/roller':
        raise SourceFailure('role_change_wrong_company')
    if not isinstance(event.get('type'),str) or not event['type'].startswith('no.brreg.enhetsregisteret.rolle.'):
        raise SourceFailure('role_change_invalid_type')
    try:timestamp(event['time'])
    except (KeyError,ValueError,TypeError,AttributeError):raise SourceFailure('role_change_invalid_date') from None
    return org,int(ident)


async def pages(http,numbers,since,until):
    since=timestamp(since).isoformat(timespec='milliseconds').replace('+00:00','Z')
    seen={};cursor=None
    while True:
        params={'organisasjonsnummer':','.join(numbers),'size':PAGE_SIZE}
        if cursor is None:params['afterTime']=since
        else:params['afterId']=cursor
        response=await http.get(ENDPOINT+'?'+urlencode(params),'__role_changes__')
        if response.status!=200:raise SourceFailure('role_change_http_'+str(response.status))
        rows=json.loads(response.body)
        if not isinstance(rows,list) or len(rows)>PAGE_SIZE:raise SourceFailure('role_change_invalid_page')
        maximum=0
        for index,event in enumerate(rows):
            org,ident=validate(event,numbers);maximum=max(maximum,ident)
            if cursor is not None and ident<cursor:raise SourceFailure('role_change_pagination_repeated')
            canonical=json.dumps(event,sort_keys=True,ensure_ascii=False)
            if ident in seen:
                if seen[ident]!=canonical:raise SourceFailure('role_change_conflicting_event')
                continue
            seen[ident]=canonical
            published=timestamp(event['time'])
            if published<timestamp(since):raise SourceFailure('role_change_date_outside_window')
            # No documented upper-bound query exists. Concurrently published
            # events after our run start are outside this snapshot, not facts.
            if published<=timestamp(until):yield event,response,'/'+str(index)
        if len(rows)<PAGE_SIZE:return
        if not maximum or cursor is not None and maximum<=cursor:raise SourceFailure('role_change_pagination_repeated')
        # The documented afterId cursor is exclusive. Reusing the maximum
        # avoids skipping a consecutive ID; exact boundary duplicates are
        # also harmless if a server returns the boundary inclusively.
        cursor=maximum


def extract(event,response,locator,org):
    _,ident=validate(event,{org})
    kind=event['type'].rsplit('.',1)[-1]
    value={'company_orgnr':org,'record_orgnr':org,'event_id':ident,'event_source':'roles',
        'date':event['time'],'date_source':DATE_LABEL,'event_type':event['type'],
        'change_type':{'oppdatert':'updated','opprettet':'created','slettet':'deleted'}.get(kind,kind),
        'title':{'oppdatert':'Registry roles updated','opprettet':'Registry roles created','slettet':'Registry roles deleted'}.get(kind,'Registry role event'),
        'changed_fields':[],'role_type':None,'role_type_state':'not_supplied_by_public_feed',
        'person_name':None,'person_name_state':'not_supplied_by_public_feed',
        'url':ENDPOINT+'?'+urlencode({'organisasjonsnummer':org,'afterId':max(1,ident-1),'size':2})}
    section=Section(state='available');source=response_source(response)
    add(section,source,org,'activity','registry_change.roles.'+digest([org,ident])[:24],value,locator,method=METHOD)
    claim=section.claims[-1]
    for key in ('data/organisasjonsnummer','id','source','type','time'):
        data=event
        for token in key.split('/'):data=data[token]
        receipt=Section();add(receipt,source,org,'activity','receipt',data,locator+'/'+key,method=METHOD)
        section.evidence.extend(receipt.evidence);claim.evidence_ids.extend(e.id for e in receipt.evidence)
    return section


async def collect(envelopes,http,since,until):
    results={o:Section(state='not_available') for o in envelopes}
    numbers=sorted(envelopes)
    for start in range(0,len(numbers),CHUNK):
        chunk=numbers[start:start+CHUNK]
        try:
            async for event,response,locator in pages(http,chunk,since,until):
                org=event['data']['organisasjonsnummer']
                section=await offload(extract,event,response,locator,org)
                results[org].claims.extend(section.claims);results[org].evidence.extend(section.evidence)
                if results[org].state!='failed':results[org].state='available'
        except asyncio.CancelledError:raise
        except Exception as exc:
            for org in chunk:
                results[org].state='failed';results[org].errors.extend(missing('activity',getattr(exc,'code','role_change_invalid_payload')).errors)
    return results
