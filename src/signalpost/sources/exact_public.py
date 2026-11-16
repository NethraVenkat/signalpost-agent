"""Free official GLEIF/TED sources; IDs nominate, source records prove.

No names, domains or parent identity are used to widen company scope.
"""
import asyncio
import json
import re
import time
from datetime import date, datetime, timezone
from urllib.parse import urlencode, urlsplit
from urllib.robotparser import RobotFileParser
from xml.etree import ElementTree as ET

import httpx
from ..budget import SourceFailure
from ..models.evidence import utc_now, digest
from ..workers import offload
from .extract import Section, add, missing, response_source
from .http import Response
from .official_resilience import check_source,DNS_FAILURES,pause,retry_after

GLEIF='https://api.gleif.org/api/v1/'
TED='https://api.ted.europa.eu/v3/notices/search'
METHOD='signalpost.exact_public.v1'
HOSTS={'api.gleif.org','api.ted.europa.eu','ted.europa.eu'}
MAX_PAGES=10
POLITENESS_SECONDS=1


def org_id(value):
    """Only the two Norwegian registry renderings; never strip arbitrary text."""
    if not isinstance(value,str):return None
    return value.replace(' ','') if re.fullmatch(r'[0-9]{9}|[0-9]{3} [0-9]{3} [0-9]{3}',value) else None


def variants(org):return [org,org[:3]+' '+org[3:6]+' '+org[6:]]


class PublicHttp:
    def __init__(self,client,config,budget,blobs,hosts=None,sections=None,robots_unserved=(),politeness=None):
        self.client,self.config,self.budget,self.blobs=client,config,budget,blobs
        self.hosts=set(hosts or HOSTS);self.sections=dict(sections or {})
        # Hosts that serve no robots.txt at all (connection reset on that path):
        # treated like 404 (no rules), with the reason kept on the request log.
        self.robots_unserved=set(robots_unserved);self.politeness=politeness
        self.robots={};self.robots_failures={};self.last={};self.delays={};self.locks={h:asyncio.Lock() for h in self.hosts}

    def section(self,host):
        return self.sections.get(host) or ('gleif' if host=='api.gleif.org' else 'procurement')

    async def raw(self,url,org,payload=None,headers=None):
        check_source(self.budget,url)
        for attempt in range(3):
            event=None;minimum=0.0
            try:
                response=await self._raw(url,org,payload,headers)
                event=response.request_event
                event['official_retry_attempt']=attempt
                if response.status<500:return response
                event['official_transient']=True
                minimum=response.retry_after_seconds
                if attempt==2:return response
            except SourceFailure as exc:
                event=getattr(exc,'request_event',None)
                if exc.code not in DNS_FAILURES|{'public_timeout','public_connect'} or event is None:raise
                event.update(official_transient=True,official_retry_attempt=attempt)
                if attempt==2:raise
            await pause(self.budget,event,attempt,minimum=minimum)

    async def _raw(self,url,org,payload=None,headers=None):
        p=urlsplit(url)
        if p.scheme!='https' or p.hostname not in self.hosts or p.port not in (None,443) or p.username or p.password:
            raise SourceFailure('public_url_refused')
        host=p.hostname
        async with self.locks[host]:
            politeness=POLITENESS_SECONDS if self.politeness is None else self.politeness
            delay=max(0,self.last.get(host,0)+max(politeness,self.delays.get(host,0))-time.monotonic())
            if time.monotonic()+delay>=self.budget.deadline:raise SourceFailure('deadline')
            if delay:await asyncio.sleep(delay)
            event=self.budget.reserve(url,host,org);event['section']=self.section(host)
            if payload is not None:event['request_json']=payload;event['method']='POST'
            began=time.monotonic()
            try:
                timeout=min(self.config.request_timeout,max(.001,self.budget.deadline-time.monotonic()))
                r=await self.client.request('POST' if payload is not None else 'GET',url,json=payload,timeout=timeout,
                    follow_redirects=False,headers={**(headers or {}),'User-Agent':self.config.website_user_agent})
                event['status']=r.status_code
                sha=await offload(self.blobs.put,r.content);event['content_sha256']=sha
                if len(r.content)>8_000_000:raise SourceFailure('public_body_limit')
                response=Response(r.content,r.status_code,url,utc_now(),sha)
                response.request_event=event
                response.retry_after_seconds=retry_after(r.headers.get('Retry-After'))
                return response
            except (httpx.TimeoutException,httpx.NetworkError,httpx.ProtocolError) as exc:
                event['error']=type(exc).__name__
                failure=SourceFailure('public_timeout' if isinstance(exc,httpx.TimeoutException) else 'public_connect')
                failure.request_event=event;raise failure from exc
            except SourceFailure as exc:
                event['error']=exc.code;exc.request_event=event;raise
            finally:
                self.last[host]=time.monotonic();event['runtime_ms']=round((time.monotonic()-began)*1000)

    async def request(self,url,org,payload=None,headers=None):
        host=urlsplit(url).hostname
        if host not in self.hosts:raise SourceFailure('public_url_refused')
        if host not in self.robots:
            try:
                robots='https://'+host+'/robots.txt'
                # A host known to serve no robots file gets one attempt, no retry loop.
                r=await (self._raw(robots,org) if host in self.robots_unserved else self.raw(robots,org))
            except SourceFailure as exc:
                if host not in self.robots_unserved or exc.code!='public_connect':raise
                event=getattr(exc,'request_event',None)
                if event is not None:event['robots_unserved']='connection reset on /robots.txt; treated as no rules (like 404)'
                self.robots[host]=None
                r=None
            if r is None:pass
            elif r.status in {404,410}:self.robots[host]=None
            elif r.status==200:
                parser=RobotFileParser();parser.parse(r.body.decode('utf8',errors='replace').splitlines());self.robots[host]=parser
                self.delays[host]=parser.crawl_delay(self.config.website_user_agent) or parser.crawl_delay('*') or 0
            else:
                self.robots[host]=False
                if r.status>=500:self.robots_failures[host]="public_robots_unavailable_http"+str(r.status)
        parser=self.robots[host]
        if parser is False or (parser is not None and not parser.can_fetch(self.config.website_user_agent,url)):
            raise SourceFailure(self.robots_failures.get(host,'public_robots_blocked'))
        r=await self.raw(url,org,payload,headers)
        if r.status in {401,403,429}:self.robots[host]=False  # No further calls to a refused/rate-limited host this run.
        if r.status!=200:raise SourceFailure('public_http_'+str(r.status))
        return r


def json_claim(section,response,org,family,field,value,paths):
    """One bounded verbatim receipt per scalar; full value is re-extracted in audit."""
    source=response_source(response);start=len(section.claims)
    for path,scalar in paths:
        add(section,source,org,family,field,value,path,source_class='official_gleif' if family=='gleif' else 'official_ted',method=METHOD)
    created=section.claims[start:]
    if created:
        created[0].evidence_ids=list(dict.fromkeys(c.evidence_ids[0] for c in created))
        section.claims=section.claims[:start]+[created[0]]


def lei_record(item,org):
    a=item.get('attributes',{});e=a.get('entity',{});lei=a.get('lei')
    if (org_id(e.get('registeredAs'))!=org or e.get('registeredAt',{}).get('id')!='RA000472'
        or e.get('jurisdiction')!='NO' or e.get('legalAddress',{}).get('country')!='NO'
        or not isinstance(lei,str) or not re.fullmatch('[A-Z0-9]{20}',lei) or item.get('id')!=lei):return None
    registration=a.get('registration',{})
    fields={'lei':lei,'entity_status':e.get('status'),'legal_form':e.get('legalForm',{}).get('id'),
        'initial_registration_date':registration.get('initialRegistrationDate'),'next_renewal_date':registration.get('nextRenewalDate'),
        'registration_status':registration.get('status')}
    return {k:v for k,v in fields.items() if isinstance(v,str) and v}


def parent_record(item,child,kind):
    a=item.get('attributes',{});r=a.get('relationship',{})
    expected='IS_DIRECTLY_CONSOLIDATED_BY' if kind=='direct' else 'IS_ULTIMATELY_CONSOLIDATED_BY'
    if (r.get('status')!='ACTIVE' or r.get('type')!=expected or r.get('startNode')!={'id':child,'type':'LEI'}
        or r.get('endNode',{}).get('type')!='LEI'):return None
    parent=r['endNode'].get('id')
    if not isinstance(parent,str) or not re.fullmatch('[A-Z0-9]{20}',parent) or parent==child:return None
    return {'child_lei':child,'parent_lei':parent,'relationship_status':'ACTIVE','relationship_type':expected}


async def gleif_batch(orgs,http):
    result={o:Section(state='not_available') for o in orgs}
    for offset in range(0,len(orgs),25):
        chunk=orgs[offset:offset+25];found={o:[] for o in chunk};responses=[]
        url=GLEIF+'lei-records?'+urlencode({'filter[entity.registeredAs]':','.join(v for o in chunk for v in variants(o)),
            'filter[entity.registeredAt]':'RA000472','page[size]':100})
        try:
            seen=set()
            for page in range(MAX_PAGES):
                if url in seen:raise SourceFailure('gleif_pagination_cycle')
                seen.add(url);response=await http.request(url,chunk[0]);data=json.loads(response.body);responses.append(response)
                if not isinstance(data.get('data'),list):raise SourceFailure('gleif_schema')
                for i,item in enumerate(data['data']):
                    org=org_id(item.get('attributes',{}).get('entity',{}).get('registeredAs'))
                    if org in found and lei_record(item,org):found[org].append((item,response,i))
                url=data.get('links',{}).get('next')
                if not url:break
                if not url.startswith(GLEIF+'lei-records?'):raise SourceFailure('gleif_pagination_url')
            else:raise SourceFailure('gleif_pagination_limit')
        except (SourceFailure,ValueError,TypeError) as exc:
            for org in chunk:result[org]=missing('gleif',getattr(exc,'code','gleif_schema'))
            continue
        for org,items in found.items():
            unique={item['id']:(item,r,i) for item,r,i in items}
            if len(unique)>1:result[org]=missing('gleif','gleif_ambiguous_id',state='ambiguous');continue
            if not unique:continue
            item,r,i=next(iter(unique.values()));value=lei_record(item,org);section=Section();prefix=f'/data/{i}/attributes'
            paths=[(prefix+'/entity/registeredAs',org),(prefix+'/entity/registeredAt/id','RA000472'),
                (prefix+'/entity/jurisdiction','NO'),(prefix+'/entity/legalAddress/country','NO'),(prefix+'/lei',value['lei'])]
            mapping={'entity_status':'entity/status','legal_form':'entity/legalForm/id','initial_registration_date':'registration/initialRegistrationDate',
                'next_renewal_date':'registration/nextRenewalDate','registration_status':'registration/status'}
            paths += [(prefix+'/'+mapping[k],v) for k,v in value.items() if k in mapping]
            json_claim(section,r,org,'gleif','gleif.record',value,paths)
            identity_ids=list(section.claims[0].evidence_ids)
            for kind in ('direct','ultimate'):
                link=item.get('relationships',{}).get(kind+'-parent',{}).get('links',{}).get('relationship-record')
                if not link:continue  # Reporting exceptions are not parent proof.
                try:
                    if link!=GLEIF+'lei-records/'+value['lei']+'/'+kind+'-parent-relationship':raise SourceFailure('gleif_relationship_url')
                    rr=await http.request(link,org);parent=parent_record(json.loads(rr.body).get('data',{}),value['lei'],kind)
                    if parent:
                        p='/data/attributes/relationship'
                        json_claim(section,rr,org,'gleif','gleif.parent.'+kind,parent,[(p+'/startNode/id',value['lei']),
                            (p+'/endNode/id',parent['parent_lei']),(p+'/status','ACTIVE'),(p+'/type',parent['relationship_type'])])
                        section.claims[-1].evidence_ids+=identity_ids
                except (SourceFailure,ValueError,TypeError) as exc:
                    section.errors+=missing('gleif',getattr(exc,'code','gleif_relationship_schema')).errors
            result[org]=section
    return result


def local(element):return element.tag.rsplit('}',1)[-1]
def nodes(element,name):return [e for e in element.iter() if local(e)==name]
def texts(element,name):return [(e.text or '').strip() for e in nodes(element,name) if (e.text or '').strip()]


def ted_xml(body,org,notice,now):
    """Structured eForms links only; flattened search arrays never prove attribution.

    Amounts intentionally abstain: no notice/consortium total is allocated.
    """
    if b'<!DOCTYPE' in body.upper() or b'<!ENTITY' in body.upper():return []
    root=ET.fromstring(body)
    if root.tag!='{urn:oasis:names:specification:ubl:schema:xsd:ContractAwardNotice-2}ContractAwardNotice':return []
    organisations={};duplicate_ids=set()
    for organisation in nodes(root,'Organization'):
        companies=[e for e in organisation if local(e)=='Company']
        if len(companies)!=1:continue
        company=companies[0];ids=texts(company,'ID');countries=texts(company,'IdentificationCode')
        # PartyIdentification references ORG-*; PartyLegalEntity has national ID.
        refs=[x for e in nodes(company,'PartyIdentification') for x in texts(e,'ID') if re.fullmatch('ORG-[0-9]+',x)]
        national=[x for e in nodes(company,'PartyLegalEntity') for x in texts(e,'CompanyID')]
        names=texts(company,'RegistrationName') or [n for party in nodes(company,'PartyName') for n in texts(party,'Name')]
        if len(refs)==len(national)==1 and len(set(countries))==1 and names:
            if refs[0] in organisations or refs[0] in duplicate_ids:
                organisations.pop(refs[0],None);duplicate_ids.add(refs[0]);continue
            organisations[refs[0]]={'id':org_id(national[0]),'country':countries[0],'name':names[0]}
    buyers=[]
    for party in nodes(root,'ContractingParty'):
        refs=[x for x in texts(party,'ID') if x in organisations]
        if len(set(refs))==1:buyers.append(organisations[refs[0]])
    buyer_names=sorted({x['name'] for x in buyers})
    if not buyer_names:return []
    titles=[]
    for project in list(root):
        if local(project)=='ProcurementProject':titles=texts(project,'Name')
    if not titles:return []
    title=titles[0];tenders={};parties={}
    for party in nodes(root,'TenderingParty'):
        ids=[e.text for e in party if local(e)=='ID' and e.text]
        refs=[x for tenderer in nodes(party,'Tenderer') for x in texts(tenderer,'ID') if x in organisations]
        if len(ids)==1 and refs:parties[ids[0]]=refs
    for tender in nodes(root,'LotTender'):
        ids=[e.text for e in tender if local(e)=='ID' and e.text]
        lot=[x for e in tender if local(e)=='TenderLot' for x in texts(e,'ID')]
        refs=[orgref for e in tender if local(e)=='TenderingParty' for ref in texts(e,'ID') for orgref in parties.get(ref,[])]
        if len(ids)==len(lot)==1 and refs:tenders[ids[0]]=(lot[0],refs)
    results=set()
    for result in nodes(root,'LotResult'):
        if texts(result,'TenderResultCode')!=['selec-w']:continue
        tender_ids=[x for e in result if local(e)=='LotTender' for x in texts(e,'ID')]
        contract_ids=[x for e in result if local(e)=='SettledContract' for x in texts(e,'ID')]
        lot_ids=[x for e in result if local(e)=='TenderLot' for x in texts(e,'ID')]
        if len(lot_ids)!=1:continue
        results.update((contract_id,tender_id,lot_ids[0]) for contract_id in contract_ids for tender_id in tender_ids)
    items=[]
    for contract in nodes(root,'SettledContract'):
        dates=texts(contract,'AwardDate');refs=[x for e in nodes(contract,'LotTender') for x in texts(e,'ID') if x in tenders]
        contract_ids=[e.text for e in contract if local(e)=='ID' and e.text]
        if len(set(dates))!=1 or len(set(refs))!=1:continue
        if len(contract_ids)!=1 or (contract_ids[0],refs[0],tenders[refs[0]][0]) not in results:continue
        try:day=date.fromisoformat(dates[0][:10])
        except ValueError:continue
        try:since=now.date().replace(year=now.year-3)
        except ValueError:since=now.date().replace(year=now.year-3,day=28)
        if not since<=day<=now.date():continue
        lot,refs=tenders[refs[0]]
        winner=any(organisations[r]['id']==org and organisations[r]['country']=='NOR' for r in refs)
        buyer=any(x['id']==org and x['country']=='NOR' for x in buyers)
        if not (winner or buyer):continue
        value={'company_orgnr':org,'title':title,'buyer':'; '.join(buyer_names),'date':day.isoformat(),
            'date_source':'contract award date as reported','url':'https://ted.europa.eu/en/notice/-/detail/'+notice,
            'notice_id':notice,'lot_id':lot,'matched_role':'winner' if winner else 'buyer','label':'Public procurement award'}
        items.append(value)
    return list({digest(v):v for v in items}.values())


async def ted_batch(orgs,http,now):
    result={o:Section(state='not_available') for o in orgs}
    for offset in range(0,len(orgs),25):
        chunk=orgs[offset:offset+25]
        ids=' '.join('"'+v+'"' for o in chunk for v in variants(o))
        since=now.replace(year=now.year-3,day=min(now.day,28)).strftime('%Y%m%d')
        query=f'notice-type IN (can-standard can-social can-desg can-tran) AND publication-date>={since} AND ((winner-identifier IN ({ids})) OR (buyer-identifier IN ({ids})))'
        seen=set();cache={}
        try:
            for page in range(1,MAX_PAGES+1):
                payload={'query':query,'fields':['publication-number','winner-identifier','buyer-identifier'],'limit':100,
                    'page':page,'scope':'ALL','paginationMode':'PAGE_NUMBER','checkQuerySyntax':False}
                r=await http.request(TED,chunk[0],payload);data=json.loads(r.body)
                notices=data.get('notices')
                if not isinstance(notices,list) or data.get('timedOut'):raise SourceFailure('ted_search_incomplete')
                fresh=0
                for notice in notices:
                    pub=notice.get('publication-number')
                    if not isinstance(pub,str) or not re.fullmatch('[0-9]+-[0-9]{4}',pub):raise SourceFailure('ted_notice_schema')
                    if pub in seen:continue
                    seen.add(pub);fresh+=1
                    matched={o for role in ('winner-identifier','buyer-identifier') for v in notice.get(role,[]) if (o:=org_id(v)) in chunk}
                    if not matched:continue
                    xml='https://ted.europa.eu/en/notice/'+pub+'/xml'
                    try:
                        if xml not in cache:cache[xml]=await http.request(xml,chunk[0])
                        document=cache[xml]
                        for org in matched:
                            values=ted_xml(document.body,org,pub,now)
                            if not values:raise SourceFailure('ted_structured_proof_unavailable')
                            section=result[org]
                            for value in values:
                                # One receipt per scalar so snippets never omit proof inputs.
                                for i,scalar in enumerate([org,value['title'],value['buyer'],value['date'],value['lot_id']]):
                                    source=response_source(document)
                                    add(section,source,org,'procurement','procurement.award.'+digest(value)[:24],value,
                                        'ted-xml:'+digest(value)[:24]+'/'+str(i),span=source.excerpt(scalar,''),source_class='official_ted',method=METHOD)
                                claims=section.claims[-5:];claims[0].evidence_ids=[c.evidence_ids[0] for c in claims];section.claims=section.claims[:-5]+[claims[0]]
                                section.state='available'
                    except (SourceFailure,ValueError,ET.ParseError) as exc:
                        for org in matched:
                            section=result[org];section.errors+=missing('procurement',getattr(exc,'code','ted_xml_schema')).errors
                            if not section.claims:section.state='blocked' if getattr(exc,'code','')=='public_robots_blocked' else 'failed'
                if len(notices)<100:break
                if not fresh:raise SourceFailure('ted_pagination_cycle')
            else:raise SourceFailure('ted_pagination_limit')
        except (SourceFailure,ValueError,TypeError) as exc:
            for org in chunk:
                section=result[org];section.errors+=missing('procurement',getattr(exc,'code','ted_schema')).errors
                if not section.claims:section.state='failed'
    return result


async def enrich(envelopes,client,config,budget,blobs,update):
    eligible=sorted(o for o,e in envelopes.items() if e.run.sections.get('identity')=='available')
    http=PublicHttp(client,config,budget,blobs)
    for family,enabled in [('gleif',config.gleif),('procurement',config.procurement)]:
        if not enabled:continue
        try:
            sections=await gleif_batch(eligible,http) if family=='gleif' else await ted_batch(eligible,http,datetime.now(timezone.utc))
        except Exception as exc:
            sections={o:missing(family,getattr(exc,'code','public_source_exception'),type(exc).__name__) for o in eligible}
        for org,section in sections.items():update(envelopes[org],family,section)
    from . import exact_official
    try:
        await exact_official.enrich(envelopes,client,config,budget,blobs,update)
    except Exception as exc:
        for family in exact_official.enabled_families(config):
            for org in eligible:
                if envelopes[org].run.sections.get(family) in (None,'pending'):
                    update(envelopes[org],family,missing(family,getattr(exc,'code','public_source_exception'),type(exc).__name__))


def briefing_sentences(envelope):
    from ..models.synthesis import Sentence
    claims=[c for c in envelope.claims if c.availability=='available' and not c.carried_forward]
    record=next((c for c in claims if c.field=='gleif.record'),None)
    result=[]
    if record:
        parents=[c for c in claims if c.field.startswith('gleif.parent.')]
        text='GLEIF LEI: '+record.value['lei']
        for parent in parents:
            text+='; '+parent.field.rsplit('.',1)[-1]+' parent LEI (ACTIVE): '+parent.value['parent_lei']
        result.append(Sentence(text=text+'.',claim_ids=[record.id]+[p.id for p in parents]))
    awards=[c for c in claims if c.field.startswith('procurement.award.')]
    for claim in sorted(awards,key=lambda c:(c.value['date'],c.id),reverse=True)[:3]:
        v=claim.value
        result.append(Sentence(text='Public procurement award: '+v['title']+'; buyer: '+v['buyer']+'; '+v['date']+'; matched as '+v['matched_role']+'.',claim_ids=[claim.id]))
    from .exact_official import briefing_sentences as official_sentences
    return result+official_sentences(envelope)
