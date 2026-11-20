"""Build once from the measured run; replay audit using committed data, offline."""
import argparse,base64,csv,gzip,hashlib,io,json,math,random,re,socket,sys
from collections import Counter,defaultdict
from pathlib import Path
from urllib.parse import urlsplit

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SEED=2026112601
RUN=ROOT/'out/g1-api-standard100-normal-network'


def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def kind(c):
 f=c['field'];fam=c['family']
 if f=='official_website':return 'website'
 if f.startswith('social_profile.'):return 'social'
 if f=='public_brand' or f.startswith('brand.'):return 'brand'
 if f.startswith('website_description.'):return 'website_description'
 if f.startswith('contact.'):return 'website_contact'
 if f.startswith('identity.registered_website'):return 'registry_website'
 if f.startswith('accounts.consolidated.'):return 'consolidated_accounts'
 if f.startswith('accounts.filed_year'):return 'filing_years'
 if fam in ('signature','prokura'):return fam+('_rule' if f.endswith('.rule') else '_combination')
 if fam=='group':return 'group_'+c['value']['relationship']
 return {'accounts':'entity_accounts','roles':'people_roles','subunits':'locations_subunits','activity':'public_activity','gleif':'lei'}.get(fam,fam)


def allocation(population):
 groups=defaultdict(list)
 for item in population:groups[item['type']].append(item)
 n={k:(len(v) if k in {'website','social','brand'} else 1) for k,v in groups.items()}
 while sum(n.values())<200:
  # Divisor allocation, sqrt population weights, deterministic tie-breaking.
  k=min((k for k in groups if n[k]<len(groups[k])),key=lambda k:(-(math.sqrt(len(groups[k]))/(n[k]+1)),k))
  n[k]+=1
 return groups,n


def draw(population):
 groups,n=allocation(population);rng=random.Random(SEED);selected=[]
 for k in sorted(groups):selected.extend(rng.sample(sorted(groups[k],key=lambda x:(x['org'],x['id'])),n[k]))
 rng.shuffle(selected)
 return selected,n


def build():
 raw=(RUN/'envelopes.jsonl').read_bytes();rows=[json.loads(l) for l in raw.decode('utf8').splitlines()]
 report=json.loads((RUN/'report.json').read_text(encoding='utf8'))
 assert sha(raw)=='3c7a410c9459cafa79e1c3a22b20c31db4384d3df2096b22311c7dea78dccc3b'
 lookup={};population=[]
 for row in rows:
  for c in row['claims']:
   if c['availability']=='available':
    record={'org':row['organisation_number'],'id':c['id'],'field':c['field'],'type':kind(c),'value_sha256':sha(json.dumps(c['value'],sort_keys=True,ensure_ascii=False).encode())}
    population.append(record);lookup[(record['org'],record['id'])]=(row,c)
 selected,n=draw(population);packet={'bodies':{},'items':[],'request_receipts':[]}
 for index,item in enumerate(selected):
  row,c=lookup[(item['org'],item['id'])]
  context=[x for x in row['claims'] if x['availability']=='available' and (x['field'].startswith('identity.') or x['field']=='official_website')]
  refs={eid for x in [c]+context for eid in x['evidence_ids']}
  records=[e for e in row['evidence'] if e['id'] in refs]
  for e in records:
   h=e['content_sha256']
   if h not in packet['bodies']:
    body=(RUN/'state/blobs'/h).read_bytes();assert sha(body)==h
    packet['bodies'][h]=base64.b64encode(body).decode()
  packet['items'].append(dict(item,seed=SEED,index=index,claim=c,context=context,evidence=records))
 hashes=set(packet['bodies'])
 packet['request_receipts']=[{k:e.get(k) for k in ('url','organisation_number','status','content_sha256')} for e in report['request_log'] if e.get('content_sha256') in hashes]
 packet['bulk_input_sha256']=sha((ROOT/'reports/r5/baseline/registry100.csv').read_bytes())
 (HERE/'population.json.gz').write_bytes(gzip.compress(json.dumps(population,ensure_ascii=False,separators=(',',':')).encode(),mtime=0))
 (HERE/'proof.json.gz').write_bytes(gzip.compress(json.dumps(packet,ensure_ascii=False,separators=(',',':')).encode(),mtime=0))
 (HERE/'sample.jsonl').write_text(''.join(json.dumps({k:v for k,v in x.items() if k not in ('context','evidence')},ensure_ascii=False)+'\n' for x in packet['items']),encoding='utf8',newline='\n')
 dump(HERE/'manifest.json',{'seed':SEED,'code_commit':'4ca3443','source_envelopes_sha256':sha(raw),'population_claims':len(population),'sample_claims':len(selected),'allocation':n,'weights':'sqrt(type population), minimum one per available type; census of website/social/brand; divisor allocation for remainder','empty_types':['procurement','research','hiring/jobs','website people/contacts beyond published contacts','ticker/ISIN'],'files_sha256':{p.name:sha(p.read_bytes()) for p in [HERE/'population.json.gz',HERE/'proof.json.gz',HERE/'sample.jsonl']},'proof_scope':'Original saved response bytes needed for hashes, including public business-role source records; no local filesystem receipts or credentials. No redaction or normalization of proof bodies. Public source birth-date fields can occur in original role/authority receipts; they are not sampled claim values.'})


def leaves(x):
 if isinstance(x,dict):
  for v in x.values():yield from leaves(v)
 elif isinstance(x,list):
  for v in x:yield from leaves(v)
 elif x is not None:yield x


def org_in(text,org):return re.search(r'(?<!\d)'+r'[\s\u00a0]*'.join(org)+r'(?!\d)',text) is not None


def identity(item,bodies):
 org=item['org'];claim=item['claim'];evidence={e['id']:e for e in item['evidence']};refs=[evidence[eid] for eid in claim['evidence_ids']]
 for e in refs:
  raw=bodies[e['content_sha256']];text=raw.decode('utf-8-sig',errors='replace');u=e['source_url'];loc=e['locator']
  if loc.startswith('row:'+org+'/'):
   records=list(csv.DictReader(io.StringIO(text)))
   if any(str(r.get('organisasjonsnummer',''))==org for r in records):return True,'exact CSV record'
  try:doc=json.loads(raw)
  except (ValueError,UnicodeError):doc=None
  if '/fullmakt/enheter/'+org+'/' in u:
   return isinstance(doc,dict) and (doc.get('enhet') or {}).get('organisasjonsnummer')==org,'exact authority owner'
  if '/regnskapsregisteret/regnskap/'+org in u and isinstance(doc,list):
   return any(str((r.get('virksomhet') or {}).get('organisasjonsnummer'))==org for r in doc if isinstance(r,dict)),'exact accounts owner'
  if '/api/enheter/'+org+'/roller' in u and isinstance(doc,dict):
   return doc.get('organisasjonsnummer')==org or (doc.get('_links',{}).get('enhet',{}).get('href')=='https://data.brreg.no/enhetsregisteret/api/enheter/'+org),'exact roles owner'
  if claim['family']=='group':
   v=claim['value'];return org in (v.get('parent_organisation_number'),v.get('subsidiary_organisation_number')) and org_in(text,org) and u.endswith('/'+org),'exact incident group edge'
  if claim['family']=='website':
   site=next((c for c in item['context'] if c['field']=='official_website'),None)
   if site and site['value'].get('identity_level')=='VERIFIED':
    for rid in site['evidence_ids']:
     proof=evidence[rid];t=bodies[proof['content_sha256']].decode('utf8',errors='replace')
     if org_in(t,org) and urlsplit(u).hostname==urlsplit(site['value']['final_url']).hostname:return True,'exact-orgnr website proof and same source host'
   continue
  # A scoped JSON record must contain the exact owner. Prefer the locator's
  # nearest ancestor, rather than any occurrence in a multi-company batch.
  if doc is not None and loc.startswith('/'):
   cur=doc;ancestors=[cur]
   try:
    for part in loc.strip('/').split('/'):
     part=part.replace('~1','/').replace('~0','~');cur=cur[int(part)] if isinstance(cur,list) else cur[part];ancestors.append(cur)
   except (KeyError,ValueError,TypeError,IndexError):pass
   for node in reversed(ancestors):
    if isinstance(node,dict):
     direct=[node.get(k) for k in ('organisasjonsnummer','organisasjonsNummer','company_orgnr','registeredAs')]
     direct += [(node.get('fields') or {}).get(k) for k in ('Organisasjonsnummer støttemottaker','Organisasjonsnummer st\ufffdttemottaker')] if isinstance(node.get('fields'),dict) else []
     linked=(node.get('_links') or {}).get('enhet',{}).get('href','')
     if any(isinstance(v,str) and re.sub(r'\s','',v)==org for v in direct) or linked.endswith('/enheter/'+org):return True,'exact scoped JSON owner'
   if claim['family'] in {'subunits','gleif','state_aid','licences','inspections'} and org_in(text,org):return None,'exact ID present but independent record-owner binding not established'
 return None,'identity not independently established from bounded receipts'


def wilson(k,n):
 if not n:return None
 z=1.959963984540054;p=k/n
 return max(0.0,(p+z*z/(2*n)-z*math.sqrt(p*(1-p)/n+z*z/(4*n*n)))/(1+z*z/n))


def check():
 def blocked(*a,**k):raise RuntimeError('Precision replay is offline')
 socket.create_connection=blocked;socket.socket.connect=blocked
 def audit(event,args):
  if event in {'socket.connect','socket.getaddrinfo','socket.gethostbyname','socket.sendto'}:blocked()
 sys.addaudithook(audit)
 m=json.loads((HERE/'manifest.json').read_text())
 for name,h in m['files_sha256'].items():assert sha((HERE/name).read_bytes())==h,name
 population=json.loads(gzip.decompress((HERE/'population.json.gz').read_bytes()));packet=json.loads(gzip.decompress((HERE/'proof.json.gz').read_bytes()))
 expected,n=draw(population);assert [(x['org'],x['id']) for x in expected]==[(x['org'],x['id']) for x in packet['items']]
 samples=[json.loads(l) for l in (HERE/'sample.jsonl').read_text(encoding='utf8').splitlines()]
 assert len(samples)==200 and len({(x['org'],x['id']) for x in samples})==200
 bodies={h:base64.b64decode(b) for h,b in packet['bodies'].items()};results=[]
 for item,sampled in zip(packet['items'],samples):
  assert sampled['claim']==item['claim'] and sampled['seed']==SEED
  c=item['claim'];ev={e['id']:e for e in item['evidence']};refs=[ev[x] for x in c['evidence_ids']];fail=[];unknown=[]
  assert sha(json.dumps(c['value'],sort_keys=True,ensure_ascii=False).encode())==item['value_sha256']
  spans=[]
  for e in refs:
   body=bodies[e['content_sha256']]
   if sha(body)!=e['content_sha256']:fail.append('source hash mismatch')
   text=body.decode('utf-8-sig',errors='replace')
   if e['claim_span'] not in text:fail.append('span not verbatim in source')
   spans.append(e['claim_span'])
   ledger=any(r['url']==e['source_url'] and r['content_sha256']==e['content_sha256'] and r['status']==200 for r in packet['request_receipts'])
   bundle=e['extraction_method']=='signalpost.exact_official.v1' and e['source_class'] in {'official_state_aid','official_research','official_inspection'}
   bulk=e['locator'].startswith('row:'+item['org']+'/') and e['source_url']=='https://data.brreg.no/enhetsregisteret/api/enheter/lastned/csv'
   if not (ledger or bundle or bulk):unknown.append('URL/hash binding not independently re-established')
  bound,reason=identity(item,bodies)
  if bound is False:fail.append(reason)
  elif bound is None:unknown.append(reason)
  missing=[]
  for value in leaves(c['value']):
   literal=json.dumps(value,ensure_ascii=False) if not isinstance(value,str) else value
   present = any(literal in span for span in spans) if isinstance(value,str) else any(re.search(r'(?<![\w.+-])'+re.escape(literal)+r'(?![\w.])', span) for span in spans)
   if not present:missing.append(literal)
  if missing:unknown.append('complete value not verbatim in cited span(s): '+str(len(missing))+' missing scalar leaves')
  status='incorrect' if fail else 'unverifiable' if unknown else 'correct'
  results.append({'index':item['index'],'seed':SEED,'org':item['org'],'claim_id':item['id'],'field':c['field'],'type':item['type'],'result':status,'reasons':fail+unknown,'identity_check':reason,'missing_verbatim_values':missing})
 totals=Counter(x['result'] for x in results);types={}
 for typ in sorted(n):
  subset=[x for x in results if x['type']==typ];ct=Counter(x['result'] for x in subset)
  types[typ]={'sampled':len(subset),**{k:ct[k] for k in ('correct','incorrect','unverifiable')},'wilson_95_lower':wilson(ct['correct'],len(subset))}
 result={'seed':SEED,'sampled':200,**{k:totals[k] for k in ('correct','incorrect','unverifiable')},'wilson_95_lower':wilson(totals['correct'],200),'per_type':types,'network_disabled':True,'interpretation':'Strict literal-span certification, not a factual-error estimate. Unverifiable counts as not verified in the nominal Wilson bound. Disproportionate stratification/census means pooled Wilson is descriptive of this sample, not a population-confidence guarantee.'}
 dump(HERE/'results.json',result);(HERE/'results.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in results),encoding='utf8',newline='\n')
 human=['# Website, social and brand sample: human review pending','', '| Org number | Type | Value | Source URL | Automated result |','|---|---|---|---|---|']
 for item,r in zip(packet['items'],results):
  if item['type'] in {'website','social','brand','registry_website','website_description','website_contact'}:
   e=next(e for e in item['evidence'] if e['id'] in item['claim']['evidence_ids']);v=json.dumps(item['claim']['value'],ensure_ascii=False).replace('|','\\|').replace('\n',' ')
   human.append(f"| {item['org']} | {item['type']} | {v} | {e['source_url']} | {r['result']} |")
 (HERE/'HUMAN_REVIEW.md').write_text('\n'.join(human)+'\n',encoding='utf8',newline='\n')
 print(json.dumps(result))


if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('action',choices=('build','check'));args=a.parse_args()
 if args.action=='build':build()
 check()
