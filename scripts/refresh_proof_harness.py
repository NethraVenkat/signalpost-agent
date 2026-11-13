"""Offline seven-flag CLI replay of saved source bodies and isolated mutations.

Only this harness replaces transport/clock/politeness. Production proof, budgets,
extraction, refresh, synthesis and site code run unchanged. No network fallback.
"""
import asyncio,base64,copy,csv,gzip,hashlib,importlib,io,json,os,pkgutil,sys
from contextlib import ExitStack,redirect_stdout
from datetime import datetime,timezone
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urlsplit
import httpx
from signalpost import cli
from signalpost.runner import run as production_run
from signalpost.budget import SourceFailure
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from scripts.verify_output import verify
FIXTURE=ROOT/'tests/fixtures/refresh_proof'
CASES=('employees','address','accounts_year','name','subunit','nav_removed','website_404')


def fixture(path=FIXTURE):
    manifest=json.loads((path/'manifest.json').read_text(encoding='utf8'))
    packed=(path/'bodies.json.gz').read_bytes();assert hashlib.sha256(packed).hexdigest()==manifest['bodies_sha256']
    bodies={sha:base64.b64decode(body) for sha,body in json.loads(gzip.decompress(packed)).items()}
    assert all(hashlib.sha256(body).hexdigest()==sha for sha,body in bodies.items())
    assert hashlib.sha256((path/'registry.csv').read_bytes()).hexdigest()==manifest['registry_sha256']
    assert hashlib.sha256((path/'nav_index.json.gz').read_bytes()).hexdigest()==manifest['nav_index_sha256']
    return manifest,bodies


def mutate_table(body,case):
    reader=csv.DictReader(io.StringIO(body));rows=list(reader);fields=reader.fieldnames
    for row in rows:
        if case=='employees':row['antallAnsatte']='42';row['harRegistrertAntallAnsatte']='true'
        if case=='address':row['forretningsadresse.adresse']='Refresh proof test address 17'
        if case=='name':row['navn']='DIGITALIQ REFRESH PROOF AS'
        if case=='accounts_year':row['sisteInnsendteAarsregnskap']='2026'
    out=io.StringIO(newline='');writer=csv.DictWriter(out,fieldnames=fields);writer.writeheader();writer.writerows(rows)
    return out.getvalue()


def reply(body,url,case,manifest):
    """Plant labelled source mutations; never edit the output to pass a check."""
    org=manifest['organisation_number'];p=urlsplit(url)
    if case=='timezone_equivalent' and '/oppdateringer/' in p.path:
        data=json.loads(body)
        for events in data.get('_embedded',{}).values():
            if not isinstance(events,list):continue
            for event in events:
                if isinstance(event,dict) and isinstance(event.get('dato'),str):
                    at=datetime.fromisoformat(event['dato'].replace('Z','+00:00'))
                    if at.tzinfo is not None:event['dato']=at.astimezone(timezone.utc).isoformat().replace('+00:00','Z')
        return 200,json.dumps(data,ensure_ascii=False).encode()
    if case=='website_404' and (p.hostname or '').removeprefix('www.')=='digitaliq.no' and p.path!='/robots.txt':return 404,b'Not found: planted offline website removal'
    if case=='transient' and p.hostname=='data.brreg.no' and (p.path.endswith('/roller') or '/regnskapsregisteret/' in p.path):
        raise httpx.ReadTimeout('planted offline transient failure')
    if case=='transient' and (p.hostname or '').removeprefix('www.')=='digitaliq.no' and p.path!='/robots.txt':
        raise httpx.ReadTimeout('planted offline transient website failure')
    if case=='accounts_year' and p.path=='/regnskapsregisteret/regnskap/'+org:
        data=json.loads(body);new=copy.deepcopy(next(r for r in data if r['regnskapstype']=='SELSKAP'))
        new['regnskapsperiode']={'fraDato':'2026-01-01','tilDato':'2026-12-31'};data.insert(0,new)
        return 200,json.dumps(data,ensure_ascii=False).encode()
    if case=='accounts_year' and '/aarsregnskap/kopi/' in p.path:
        data=json.loads(body);return 200,json.dumps(sorted(set(data+['2026']))).encode()
    if case=='subunit' and p.path.endswith('/underenheter'):
        data=json.loads(body);data.setdefault('_embedded',{}).setdefault('underenheter',[]).append(
            {'organisasjonsnummer':'993578843','overordnetEnhet':org,'navn':'Offline planted proven workplace',
             'beliggenhetsadresse':{'adresse':['Refresh proof workplace 8'],'poststed':'BERGEN','postnummer':'5014','land':'Norge','landkode':'NO'},
             'harRegistrertAntallAnsatte':False})
        return 200,json.dumps(data,ensure_ascii=False).encode()
    if case=='nav_removed' and p.path.endswith('/feedentry/'+manifest['nav_uuid']):
        data=json.loads(body);data['status']='INACTIVE';return 200,json.dumps(data,ensure_ascii=False).encode()
    return None,body


def one(work,label,case,previous=None,fixture_path=FIXTURE):
    manifest,bodies=fixture(fixture_path);target=work/label
    if target.exists():raise ValueError('Fresh replay state required')
    target.mkdir(parents=True);org=manifest['organisation_number']
    batch=target/'companies.jsonl';batch.write_bytes((fixture_path/'companies.jsonl').read_bytes())
    bulk=target/'registry.csv';bulk.write_text(mutate_table((fixture_path/'registry.csv').read_text(encoding='utf8'),case),encoding='utf8',newline='')
    if previous:
        # Immutable previous proof bodies only. No HTTP/NAV cache or candidate
        # result is copied; all current responses traverse the fresh transport.
        prior_rows=[json.loads(x) for x in previous.read_text(encoding='utf8').splitlines()]
        blobdir=target/'state/blobs';blobdir.mkdir(parents=True)
        for old in prior_rows:
            for e in old['evidence']:
                sha=e['content_sha256'];source=previous.parent/'state/blobs'/sha
                if source.exists():(blobdir/sha).write_bytes(source.read_bytes())
    requested=[];unrecorded=[];aliases=[];routes=manifest['routes']
    hosts={urlsplit(url).hostname for url in routes}
    def dispatch(request):
        url=str(request.url);requested.append(url);p=urlsplit(url);key=url
        if p.hostname=='pam-stilling-feed.nav.no' and p.path.startswith('/api/v1/feed/'):
            aliases.append({'requested':url,'synthetic':'empty completed forward-tail scaffold; original forward bodies were not persisted; no ad fact derives from this response'})
            return httpx.Response(200,json={'items':[],'next_url':None})
        if key not in routes and '/oppdateringer/' in p.path:
            # A saved batch response already covers this subset's company.
            # Its bytes are unchanged; this explicit query alias supplies no
            # invented event or publisher timestamp.
            key=next((u for u in routes if urlsplit(u).path==p.path),key)
            if key!=url:aliases.append({'requested':url,'saved':key})
        if key not in routes:
            unrecorded.append(url);raise SourceFailure('offline_unrecorded_url')
        item=routes[key];status,body=reply(bodies[item['sha256']],url,case,manifest)
        return httpx.Response(item['status'] if status is None else status,content=body,headers={'content-type':item['content_type']})
    async def resolve(host,port=443):
        if host not in hosts:raise SourceFailure('no_such_domain')
        return ['93.184.216.34']
    async def replay(config):
        config.gleif=False;config.procurement=False  # Saved Stage C fixture predates these sources.
        config.previous=previous;config.state_dir=target/'state';config.nav_index_path=fixture_path/'nav_index.json.gz'
        config.website_politeness_seconds=0  # no network exists in this harness
        async with httpx.AsyncClient(transport=httpx.MockTransport(dispatch),trust_env=False) as client:
            return await production_run(config,client=client)
    flags={'organisations':batch,'bulk':bulk,'output':target/'envelopes.jsonl','profiles-output':target/'profiles.jsonl',
           'report':target/'report.json','run-id':'offline-refresh-'+label,'expected-count':1}
    argv=['signalpost','run']
    for key,value in flags.items():argv.extend(['--'+key,str(value)])
    assert len([a for a in argv if a.startswith('--')])==7
    # Load all clock users before freezing their imported references.
    import signalpost
    for module in pkgutil.walk_packages(signalpost.__path__,'signalpost.'):
        if not module.name.endswith('__main__'):importlib.import_module(module.name)
    at=datetime.fromisoformat(manifest['observation_time'].replace('Z','+00:00'))
    class Clock(datetime):
        @classmethod
        def now(cls,tz=None):return at.astimezone(tz) if tz else at.replace(tzinfo=None)
    token='.'.join(base64.urlsafe_b64encode(part).decode().rstrip('=') for part in
                   [b'{"alg":"HS256"}',b'{"sub":"offline-refresh-fixture","exp":4102444800}',b'offline-signature'])
    with ExitStack() as stack:
        stack.enter_context(patch.object(sys,'argv',argv));stack.enter_context(patch.object(cli,'run',replay))
        stack.enter_context(patch('signalpost.web.policy.resolve_public',resolve))
        stack.enter_context(patch('signalpost.sources.http.FILING_YEAR_INTERVAL',0))
        stack.enter_context(patch.dict(os.environ,{'NAV_API_TOKEN':token,'SIGNALPOST_SEARCH_PROVIDER':'disabled','SIGNALPOST_SEARCH_MOCK':'0'}))
        for module in list(sys.modules.values()):
            if getattr(module,'__name__','').startswith('signalpost.'):
                if getattr(module,'datetime',None) is datetime:stack.enter_context(patch.object(module,'datetime',Clock))
                if hasattr(module,'utc_now'):stack.enter_context(patch.object(module,'utc_now',lambda:manifest['observation_time']))
        log=io.StringIO()
        with redirect_stdout(log):exit_code=cli.main()
        assert exit_code==0,log.getvalue()
        verification=verify(target/'envelopes.jsonl',target/'state',1,batch,target/'report.json')
    rows=[json.loads(x) for x in (target/'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
    record={'argv':argv[1:],'previous_injected_by_offline_harness':str(previous) if previous else None,'exit_code':exit_code,
        'case':case,'unrecorded_urls':sorted(set(unrecorded)),'batch_aliases':aliases,'requested_urls':requested,'verification':verification,
        'output_sha256':hashlib.sha256((target/'envelopes.jsonl').read_bytes()).hexdigest(),
        'snapshot_changes':rows[0]['changes'],'coverage_observations':rows[0]['run']['refresh'].get('observation_changes',[])}
    (target/'execution.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf8')
    return rows[0],target/'envelopes.jsonl',record


def belongs(case,event):
    field=event['field']
    return {'employees':field=='identity.employees','address':field in {'identity.location.business','identity.registered_address'},
        'accounts_year':field.startswith('accounts.') or field=='identity.latest_submitted_accounts',
        'name':field=='identity.legal_name','subunit':field.startswith('subunits.'),
        'nav_removed':field.startswith('hiring.job.') and event['type']=='closed_job',
        'website_404':field=='official_website' or field.startswith(('contact.','social_profile.','website_description.','public_brand'))}[case]


def run_suite(work,fixture_path=FIXTURE):
    work=Path(work).resolve();base,previous,base_record=one(work,'baseline','unchanged',fixture_path=fixture_path)
    same,same_path,same_record=one(work,'unchanged','unchanged',previous,fixture_path)
    twice,_,twice_record=one(work,'idempotent','unchanged',same_path,fixture_path)
    cases={};tp=fp=fn=0
    supported_events=0
    for case in CASES:
        row,path,record=one(work,case,case,previous,fixture_path)
        found=[e for e in row['changes'] if belongs(case,e)];unexpected=[e for e in row['changes'] if not belongs(case,e)]
        # Seven causal source interventions are the predeclared unit of recall;
        # ancillary field events from the same source intervention are counted
        # separately and are never silently treated as extra true positives.
        tp+=bool(found);fn+=not bool(found);fp+=len(unexpected)
        supported_events+=len(found)
        again,_,again_record=one(work,case+'-repeat',case,path,fixture_path)
        cases[case]={'detected':bool(found),'supported_field_events':len(found),'unexpected_changes':unexpected,
            'idempotent_changes':len(again['changes']),'execution':record,'repeat_execution':again_record}
    equivalent,_,equivalent_record=one(work,'timezone-equivalent','timezone_equivalent',previous,fixture_path)
    stale,_,stale_record=one(work,'transient','transient',previous,fixture_path)
    old={c['field']:c for c in base['claims'] if c['availability']=='available'}
    carried=[c for c in stale['claims'] if c['carried_forward']]
    preserved=all(c['evidence_ids']==old[c['field']]['evidence_ids'] and c['last_observed_at']==old[c['field']]['last_observed_at'] for c in carried)
    stale_evidence={e['id']:e for e in stale['evidence']}
    preserved=preserved and all(all(eid in stale_evidence for eid in c['evidence_ids']) for c in carried)
    result={'fixture':fixture_path.as_posix(),'scope':fixture(fixture_path)[0]['scope'],'baseline_execution':base_record,
        'nav_scaffold':'Synthetic empty forward tail only; no claims derive from it. Exact live ad detail from saved source is mandatory. This is not full-feed discovery coverage validation.',
        'planted_causal_changes':7,'true_positives':tp,'false_positives':fp,'false_negatives':fn,
        'precision':supported_events/(supported_events+fp) if supported_events+fp else 0,'recall':tp/7,
        'precision_unit':'supported field events / all emitted field events in seven isolated interventions',
        'recall_unit':'detected causal source interventions / seven predeclared interventions',
        'supported_field_events':supported_events,'unchanged_changes':len(same['changes']),
        'false_change_rate_unchanged':len(same['changes'])/max(1,len(base['claims'])),
        'idempotent_changes':len(twice['changes']),'cases':cases,'unchanged_execution':same_record,'idempotent_execution':twice_record,
        'transient':{'changes':len(stale['changes']),'carried_claims':len(carried),'prior_receipts_and_times_preserved':preserved,
            'stale_markers_present':bool(carried),'execution':stale_record},
        'equivalent_timestamp_changes':len(equivalent['changes']),'equivalent_timestamp_execution':equivalent_record,
        'network_access':False,'paid_cost_usd':0,'current_proof_never_reused':True}
    (work/'refresh_results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    return result

if __name__=='__main__':
    result=run_suite(Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'.data/r5/stageE-offline')
    print(json.dumps({k:v for k,v in result.items() if k not in {'cases','baseline_execution','unchanged_execution','idempotent_execution','transient'}}))
