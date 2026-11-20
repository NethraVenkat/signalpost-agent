"""Company event headers from saved Brreg entity update receipts; no new crawl."""
import hashlib,json,re
from urllib.parse import urlsplit,parse_qs
from ..budget import SourceFailure
from ..models.evidence import digest
from .extract import Section,add,missing,response_source
from .http import Response
from .registry_changes import timestamp

FAMILY='status_events'
METHOD='signalpost.status_events.v1'
ENDPOINT='https://data.brreg.no/enhetsregisteret/api/oppdateringer/enheter'
DOC='https://data.brreg.no/enhetsregisteret/api/dokumentasjon/no/index.html'
# Translations of the API's Endringstyper table, not legal-announcement labels.
LABELS={'Ny':'Entity added to Enhetsregisteret','Endring':'Entity changed in Enhetsregisteret',
        'Sletting':'Entity deleted from Enhetsregisteret',
        'Fjernet':'Entity removed from Open Data; copies must remove the entity',
        'Ukjent':'Unknown change type'}
# Only documented entity status keys; no person/name/free-text patch values.
STATUS_PATHS={'/konkurs','/konkursdato','/underAvvikling','/underAvviklingDato',
              '/underTvangsavviklingEllerTvangsopplosning','/slettedato',
              '/tvangsavvikletPgaManglendeSlettingDato'}


def label(code):return LABELS.get(code,'Registry change event (undocumented code)')


def approved(url,org):
 p=urlsplit(url)
 if p.scheme!='https' or p.netloc!='data.brreg.no' or p.path!='/enhetsregisteret/api/oppdateringer/enheter':return False
 query=parse_qs(p.query);numbers=','.join(query.get('organisasjonsnummer',[])).split(',')
 return org in numbers or 'oppdateringsid' in query


def extract(org,event,response,locator):
 if not approved(response.url,org) or event.get('organisasjonsnummer')!=org:
  raise SourceFailure('wrong_company','Status event does not match exact entity/API source')
 code=event.get('endringstype');date=event.get('dato');number=event.get('oppdateringsid')
 if not isinstance(code,str) or not code or type(number)is not int or number<0:
  raise SourceFailure('status_event_invalid_header')
 try:timestamp(date)
 except (ValueError,TypeError,AttributeError):raise SourceFailure('status_event_invalid_date') from None
 value={'company_orgnr':org,'event_id':number,'date':date,
        'date_scope':'API publication time; not legal effective date',
        'change_type':code,'label':label(code),'documented_type':code in LABELS}
 if code in {'Sletting','Fjernet'}:value['status_scope']='Registry deletion/removal only; no dissolution inferred'
 patches=[];paths=[('/organisasjonsnummer',org),('/oppdateringsid',number),('/dato',date),('/endringstype',code)]
 changes=event.get('endringer') or []
 if not isinstance(changes,list):raise SourceFailure('status_event_invalid_changes')
 for i,change in enumerate(changes):
  if not isinstance(change,dict) or change.get('path') not in STATUS_PATHS:continue
  op=change.get('op');raw=change.get('value')
  if op not in {'add','replace','remove'}:continue
  item={'path':change['path'],'operation':op,'label':'Registered status field changed'}
  if op!='remove':
   # A code is not an arbitrary free-text/person field. Only boolean/date
   # values can be projected from status paths; never derive a legal event.
   if type(raw)is not bool and not(isinstance(raw,str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}',raw)):continue
   item['value']=raw;paths.append((f'/endringer/{i}/value',raw))
  patches.append(item);paths.extend([(f'/endringer/{i}/path',change['path']),(f'/endringer/{i}/op',op)])
 if patches:value['status_field_changes']=patches
 section=Section();source=response_source(response);field=FAMILY+'.event.'+str(number)
 text=response.body.decode('utf-8-sig')
 def scalar_span(scalar):
  for ascii_only in (False,True):
   token=json.dumps(scalar,ensure_ascii=ascii_only,separators=(',',':'))
   if token in text:return token
  raise SourceFailure('status_event_missing_scalar_span')
 add(section,source,org,FAMILY,field,value,locator+'/endringstype',method=METHOD,span=scalar_span(code))
 for suffix,scalar in paths:
  receipt=Section();add(receipt,source,org,FAMILY,'receipt',scalar,locator+suffix,method=METHOD,span=scalar_span(scalar))
  section.evidence.extend(receipt.evidence);section.claims[0].evidence_ids.extend(e.id for e in receipt.evidence)
 section.claims[0].evidence_ids=list(dict.fromkeys(section.claims[0].evidence_ids))
 return section


def pointer(doc,path):
 for token in path.strip('/').split('/'):
  token=token.replace('~1','/').replace('~0','~');doc=doc[int(token)] if isinstance(doc,list) else doc[token]
 return doc


def from_activity(org,section,blobs,cache=None):
 """Reuse only original exact-entity receipts; this function performs no HTTP."""
 cache={} if cache is None else cache
 result=Section(state='not_available');records={e.id:e for e in section.evidence};seen=set()
 try:
  for claim in section.claims:
   if not claim.field.startswith('registry_change.') or claim.availability!='available':continue
   receipt=next((records[eid] for eid in claim.evidence_ids if eid in records and
                 records[eid].extraction_method=='signalpost.registry_changes.v3' and approved(records[eid].source_url,org)),None)
   if receipt is None:continue
   h=receipt.content_sha256
   if h not in cache:
    raw=blobs.read(h)
    if raw is None or hashlib.sha256(raw).hexdigest()!=h:raise SourceFailure('status_event_receipt_unavailable')
    cache[h]=(raw,json.loads(raw))
   raw,doc=cache[h];event=pointer(doc,receipt.locator)
   key=event.get('oppdateringsid')
   if key in seen:continue
   response=Response(raw,200,receipt.source_url,receipt.retrieved_at,h)
   part=extract(org,event,response,receipt.locator);seen.add(key)
   result.claims.extend(part.claims);result.evidence.extend(part.evidence)
  result.state='available' if result.claims else 'not_available'
 except (SourceFailure,KeyError,ValueError,TypeError,IndexError,OSError) as exc:
  result.state='failed';result.errors=missing(FAMILY,getattr(exc,'code','status_event_receipt_invalid')).errors
 if section.state in {'failed','blocked','ambiguous'}:
  result.state=section.state
  result.errors.extend(missing(FAMILY,'status_event_upstream_incomplete').errors)
 return result


async def live_preflight(http,org):
 """Only for direct S1 acquisition: robots + reachability before a data call.

 Normal integration reuses original registry payloads and never invokes this
 live path. RFC9309 retries/politeness/fail-closed come from PublicHttp.
 """
 from .exact_public import PublicHttp
 probe=PublicHttp(http.client,http.config,http.budget,http.blobs,hosts={'data.brreg.no'},
                  sections={'data.brreg.no':FAMILY})
 from ..web.robots import RobotsPolicy
 try:response=await probe.raw('https://data.brreg.no/robots.txt',org)
 except SourceFailure as exc:raise SourceFailure('status_robots_unavailable') from exc
 # This counted, bounded robots exchange is also the network preflight.
 if 200<=response.status<300:
  parser=RobotsPolicy.from_bytes(response.body)
  if not parser.can_fetch(http.config.website_user_agent,ENDPOINT):raise SourceFailure('status_robots_blocked')
  probe.robots['data.brreg.no']=parser
  probe.delays['data.brreg.no']=parser.crawl_delay(http.config.website_user_agent) or parser.crawl_delay('*') or 0
 elif 400<=response.status<500:probe.robots['data.brreg.no']=None
 else:raise SourceFailure('status_robots_unavailable')
 return probe


async def fetch_live(org,http):
 """Explicit direct mode, unused by runner: at most one page, preflight first."""
 try:
  probe=await live_preflight(http,org)
  response=await probe.request(ENDPOINT+'?organisasjonsnummer='+org+'&includeChanges=true&size=50&sort=id,DESC',org)
  doc=json.loads(response.body);result=Section(state='not_available')
  for i,event in enumerate(doc.get('_embedded',{}).get('oppdaterteEnheter',[])):
   part=extract(org,event,response,f'/_embedded/oppdaterteEnheter/{i}')
   result.claims.extend(part.claims);result.evidence.extend(part.evidence)
  result.state='available' if result.claims else 'not_available';return result
 except SourceFailure as exc:return missing(FAMILY,exc.code,state='blocked' if 'robots' in exc.code else 'failed')


def verify(org,data,evidence,stored_body):
 cache={};count=0
 for claim in data['claims']:
  if claim['family']!=FAMILY or claim['availability']!='available':continue
  refs=[evidence[eid] for eid in claim['evidence_ids']]
  assert refs and all(e['extraction_method']==METHOD for e in refs),'Missing own status evidence'
  e=next(e for e in refs if e['locator'].endswith('/endringstype'))
  h=e['content_sha256']
  if h not in cache:cache[h]=json.loads(stored_body(h))
  locator=e['locator'].rsplit('/',1)[0];event=pointer(cache[h],locator)
  text=stored_body(h);raw=text.encode('utf8') if isinstance(text,str) else text
  section=extract(org,event,Response(raw,200,e['source_url'],e['retrieved_at'],h),locator)
  expected=section.claims[0]
  assert claim['field']==expected.field and claim['value']==expected.value,'Unsupported status event value'
  assert set(claim['evidence_ids'])==set(expected.evidence_ids),'Incomplete status event scalar evidence'
  for ref in refs:
   original=next(x for x in section.evidence if x.id==ref['id'])
   assert all(ref[k]==getattr(original,k) for k in ('source_url','content_sha256','locator','claim_span','retrieved_at')),'Status event receipt differs'
  count+=1
 return count
