"""Development-only, resumable official NAV index build. No ad text is exported."""
import argparse,asyncio,json,os,sqlite3,time
from datetime import datetime,timedelta,timezone
from email.utils import format_datetime
from pathlib import Path
from uuid import UUID
import httpx
from signalpost.budget import Budget,SourceFailure
from signalpost.config import Config
from signalpost.identity.orgnr import valid
from signalpost.models.evidence import utc_now
from signalpost.sources.blobstore import BlobStore
from signalpost.sources.nav import BASE,Index,NavHttp,allowed,timestamp,token_from
from signalpost.sources.nav_index import DEFAULT_PATH,write
from signalpost.web.policy import safe_transport
from nav_disk_seed import seed,detail_value


async def build(args):
    args.state_dir.mkdir(parents=True,exist_ok=True)
    db=sqlite3.connect(args.state_dir/'nav-index-checkpoint.sqlite3')
    db.execute('CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY,value TEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS headers (uuid TEXT PRIMARY KEY,modified TEXT,status TEXT)')
    if 'source_modified' not in {r[1] for r in db.execute('PRAGMA table_info(headers)')}:
        db.execute('ALTER TABLE headers ADD COLUMN source_modified TEXT')
    db.execute('CREATE TABLE IF NOT EXISTS details (uuid TEXT PRIMARY KEY,modified TEXT,value TEXT,error TEXT)')
    if 'origin' not in {r[1] for r in db.execute('PRAGMA table_info(details)')}:
        db.execute('ALTER TABLE details ADD COLUMN origin TEXT')
    def get(key):
        row=db.execute('SELECT value FROM meta WHERE key=?',(key,)).fetchone()
        return row[0] if row else None
    def put(key,value):db.execute('INSERT OR REPLACE INTO meta VALUES (?,?)',(key,value))
    if args.seed_from_disk and get('disk_seed_version')!='4':
        seeded=seed(db,args.seed_state_root,args.seed_reports_root)
        put('disk_seed_version','4');put('disk_seed_summary',json.dumps(seeded));db.commit()
    if get('feed_done')=='true':
        # Rebuilding a completed checkpoint resumes at its last page, as NAV
        # documents for polling the tail, then follows newly appended pages.
        put('next_url',get('cursor'));put('feed_done','false');db.commit()
    cfg=Config(organisations=Path('unused'),output=Path('unused'),report=Path('unused'),
        state_dir=args.state_dir,max_requests=args.max_requests,time_budget_seconds=args.time_budget_seconds,
        deadline_fraction=1,nav_concurrency=args.concurrency,nav_max_details=args.max_requests)
    budget=Budget(cfg);index=Index();index.metrics['detail_request_cap']=args.max_requests
    http=None;began=time.monotonic()
    try:
        async with httpx.AsyncClient(transport=safe_transport(args.concurrency+1),trust_env=False) as client:
            http=NavHttp(client,cfg,budget,BlobStore(args.state_dir),index)
            http.polite_backoff=True
            token=token_from(os.environ.get('NAV_API_TOKEN')) or await http.public_token()
            if not token:raise SourceFailure('token_unavailable')
            url=get('next_url') or BASE+'/api/v1/feed'
            cutoff=get('cutoff') or format_datetime((datetime.now(timezone.utc)-timedelta(days=185)).replace(hour=0,minute=0,second=0,microsecond=0),usegmt=True)
            put('cutoff',cutoff);db.commit()
            seen=set()
            if get('feed_done')!='true':
                while url:
                    budget.check();url=allowed(url)
                    if url in seen:raise SourceFailure('nav_paging_loop')
                    seen.add(url)
                    _,body,_,_=await http.get(url,token,{'If-Modified-Since':cutoff} if url==BASE+'/api/v1/feed' else None,persist=False)
                    page=json.loads(body)
                    if not isinstance(page.get('items'),list):raise SourceFailure('nav_malformed_page')
                    for item in page['items']:
                        entry=item.get('_feed_entry') or {};uuid=str(UUID(entry.get('uuid') or item.get('id')))
                        at=timestamp(item.get('date_modified') or entry.get('sistEndret'))
                        if at is None or entry.get('status') not in {'ACTIVE','INACTIVE','DELETED'}:raise SourceFailure('nav_malformed_header')
                        at=at.isoformat()
                        old=db.execute('SELECT modified FROM headers WHERE uuid=?',(uuid,)).fetchone()
                        if old is None or timestamp(at)>=timestamp(old[0]):
                            source_modified=timestamp(entry.get('sistEndret')) or timestamp(at)
                            db.execute('INSERT OR REPLACE INTO headers VALUES (?,?,?,?)',(uuid,at,entry['status'],source_modified.isoformat()))
                    next_url=page.get('next_url')
                    if not next_url and page.get('next_id'):raise SourceFailure('nav_missing_next_url')
                    cursor=allowed(page.get('feed_url') or url)
                    put('cursor',cursor);put('next_url',allowed(next_url) if next_url else '')
                    if not next_url:put('feed_done','true');put('built_at',utc_now())
                    db.commit();index.metrics['pages']+=1
                    if index.metrics['pages']%25==0:print(json.dumps({'phase':'feed','pages_this_attempt':index.metrics['pages']}),flush=True)
                    url=next_url
            queue=asyncio.Queue()
            for uuid,modified in db.execute("SELECT uuid,modified FROM headers WHERE status='ACTIVE' ORDER BY uuid"):
                prior=db.execute('SELECT modified,error FROM details WHERE uuid=?',(uuid,)).fetchone()
                if prior is None or prior[0]!=modified or prior[1]:queue.put_nowait((uuid,modified))
            total=queue.qsize();completed=0
            print(json.dumps({'phase':'details','pending':total,'concurrency':args.concurrency}),flush=True)
            async def worker():
                nonlocal completed
                while not queue.empty():
                    uuid,modified=queue.get_nowait();value=None;error=None
                    try:
                        detail_url=BASE+'/api/v1/feedentry/'+uuid
                        _,body,_,_=await http.get(detail_url,token,persist=False)
                        data=json.loads(body);ad=data.get('ad_content') or {}
                        if data.get('uuid')!=uuid or data.get('status') not in {'ACTIVE','INACTIVE','DELETED'}:raise SourceFailure('nav_wrong_ad')
                        if data['status']=='ACTIVE':
                            if ad.get('uuid')!=uuid:raise SourceFailure('nav_wrong_ad')
                            org=str((ad.get('employer') or {}).get('orgnr') or '').strip()
                            # A successful response without an exact employer cannot nominate any company.
                            if valid(org):
                                value={'uuid':uuid,'employer_orgnr':org,'status':'ACTIVE',
                                    'published':ad.get('published'),'expires':ad.get('expires'),
                                    'last_modified':ad.get('updated') or modified,
                                    'etag':http.cache.get(detail_url+'|',{}).get('etag')}
                                for k in ('published','expires','last_modified'):
                                    if value[k] is not None and timestamp(value[k]) is None:raise SourceFailure('nav_invalid_dates')
                    except Exception as exc:
                        error=exc.code if isinstance(exc,SourceFailure) else type(exc).__name__
                        if error in {'deadline','budget_exhausted','token_unavailable'}:raise
                    db.execute('INSERT OR REPLACE INTO details VALUES (?,?,?,?,?)',
                        (uuid,modified,json.dumps(value) if value else None,error,'fresh'))
                    completed+=1
                    if completed%200==0:
                        db.commit()
                        print(json.dumps({'phase':'details','completed_this_attempt':completed,'pending':queue.qsize()}),flush=True)
            async with asyncio.TaskGroup() as group:
                for _ in range(args.concurrency):group.create_task(worker())
            failures=db.execute("SELECT COUNT(*) FROM headers h LEFT JOIN details d ON h.uuid=d.uuid WHERE h.status='ACTIVE' AND (d.uuid IS NULL OR d.error IS NOT NULL OR d.modified!=h.modified)").fetchone()[0]
            ads=[]
            for raw, in db.execute("SELECT d.value FROM details d JOIN headers h ON h.uuid=d.uuid WHERE h.status='ACTIVE' AND d.error IS NULL AND d.modified=h.modified AND d.value IS NOT NULL ORDER BY h.uuid"):
                ad=json.loads(raw)
                if ad['expires'] is None or timestamp(ad['expires'])>datetime.now(timezone.utc):ads.append(ad)
            origins=dict(db.execute('SELECT uuid,origin FROM details'))
            built=get('built_at')
            data={'schema_version':1,'index_version':'nav-'+built.replace(':','').replace('-','')+'-v1',
                'built_at':built,'cursor':get('cursor'),'source_urls':[BASE+'/api/v1/feed',BASE+'/api/v1/feedentry/{uuid}'],
                'ads_count':len(ads),'employer_count':len({a['employer_orgnr'] for a in ads}),'failed_details':failures,
                'seeded_from_disk':sum(origins.get(a['uuid'])=='disk' for a in ads),
                'fresh_fetched_ads':sum(origins.get(a['uuid'])=='fresh' for a in ads),
                'ads':ads}
            size=write(args.output,data)
            result={k:v for k,v in data.items() if k!='ads'}
            result.update({'compressed_bytes':size,'runtime_seconds':time.monotonic()-began,'requests_this_attempt':len(budget.events),
                'checkpoint':str(args.state_dir/'nav-index-checkpoint.sqlite3'),'request_log':budget.events})
            args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(result,indent=2),encoding='utf8')
            print(json.dumps({k:v for k,v in result.items() if k!='request_log'}),flush=True)
            if failures:raise SourceFailure('index_incomplete: rerun with same state-dir to retry failed details')
    finally:
        if http:http.save()
        db.commit()
        db.close()


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--state-dir',type=Path,default=Path('state/nav-index-build'))
    p.add_argument('--output',type=Path,default=DEFAULT_PATH)
    p.add_argument('--report',type=Path,default=Path('out/nav-index-build-report.json'))
    p.add_argument('--concurrency',type=int,choices=range(1,5),default=4)
    p.add_argument('--time-budget-seconds',type=float,default=7200)
    p.add_argument('--max-requests',type=int,default=30000)
    p.add_argument('--seed-from-disk',action=argparse.BooleanOptionalAction,default=True)
    p.add_argument('--seed-state-root',type=Path,default=Path('state'))
    p.add_argument('--seed-reports-root',type=Path,default=Path('dev-notes'))
    p.add_argument('--allow-system-sleep',action='store_true')
    args=p.parse_args()
    from signalpost.power import SystemAwake
    with SystemAwake(not args.allow_system_sleep):asyncio.run(build(args))
