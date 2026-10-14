"""Seed only declared discovery metadata from existing local official bodies."""
import json
from pathlib import Path
from signalpost.sources.nav import BASE,timestamp,allowed
from signalpost.identity.orgnr import valid


def detail_value(data,modified):
    uuid=data['uuid'];ad=data.get('ad_content') or {}
    if data.get('status') not in {'ACTIVE','INACTIVE','DELETED'}:raise ValueError('unknown status')
    if data['status']!='ACTIVE':return None
    if ad.get('uuid')!=uuid:raise ValueError('wrong uuid')
    org=str((ad.get('employer') or {}).get('orgnr') or '').strip()
    if not valid(org):return None
    value={'uuid':uuid,'employer_orgnr':org,'status':'ACTIVE','published':ad.get('published'),
           'expires':ad.get('expires'),'last_modified':data.get('sistEndret') or ad.get('updated') or modified,'etag':None}
    if any(value[k] is not None and timestamp(value[k]) is None for k in ('published','expires','last_modified')):
        raise ValueError('invalid date')
    return value


def seed(db,state_root,reports_root):
    roots=[state_root/'blobs']+[p/'blobs' for p in state_root.iterdir() if p.is_dir() and (p/'blobs').is_dir()]
    locations={p.name:p for root in roots if root.exists() for p in root.iterdir() if p.is_file()}
    detail_shas=set();best=None
    for report_path in reports_root.rglob('*report.json'):
        try:report=json.loads(report_path.read_bytes())
        except (OSError,ValueError):continue
        events=report.get('request_log',[])
        for e in events:
            if e.get('content_sha256') in locations and e.get('status') in {200,304} and e.get('url','').startswith(BASE+'/api/v1/feedentry/'):
                detail_shas.add(e['content_sha256'])
        nav=report.get('hiring_prefetch',{})
        if not nav.get('feed_complete') or nav.get('lookback_days',185)<185:continue
        pages=[e for e in events if e.get('content_sha256') in locations and e.get('status') in {200,304}
               and e.get('url','').startswith(BASE+'/api/v1/feed') and '/feedentry/' not in e['url']]
        if not pages:continue
        try:
            tail=json.loads(locations[pages[-1]['content_sha256']].read_bytes())
            if tail.get('next_url') or tail.get('next_id'):continue
            newest=max((timestamp(i.get('date_modified') or (i.get('_feed_entry') or {}).get('sistEndret')) for i in tail['items']),default=None)
            if newest is not None and (best is None or newest>best[0]):best=(newest,pages,tail,report_path)
        except (ValueError,KeyError,TypeError):continue
    if best is None:raise ValueError('No complete saved official NAV baseline; cannot seed a forward cursor')
    _,pages,tail,report_path=best
    for e in pages:
        page=json.loads(locations[e['content_sha256']].read_bytes())
        for item in page['items']:
            entry=item.get('_feed_entry') or {};uuid=entry.get('uuid') or item.get('id')
            at=timestamp(item.get('date_modified') or entry.get('sistEndret'))
            if at is None or entry.get('status') not in {'ACTIVE','INACTIVE','DELETED'}:raise ValueError('bad saved header')
            old=db.execute('SELECT modified FROM headers WHERE uuid=?',(uuid,)).fetchone()
            if old is None or at>=timestamp(old[0]):
                source_modified=timestamp(entry.get('sistEndret')) or at
                db.execute('INSERT OR REPLACE INTO headers VALUES (?,?,?,?)',(uuid,at.isoformat(),entry['status'],source_modified.isoformat()))
        db.commit()
    cursor=allowed(tail['feed_url'])
    for k,v in [('cursor',cursor),('next_url',cursor),('feed_done','false')]:
        db.execute('INSERT OR REPLACE INTO meta VALUES (?,?)',(k,v))
    seeded=0
    for sha in sorted(detail_shas):
        try:
            data=json.loads(locations[sha].read_bytes());uuid=data['uuid']
            header=db.execute('SELECT modified,status,source_modified FROM headers WHERE uuid=?',(uuid,)).fetchone()
            if header is None or header[1]!='ACTIVE':continue
            old=db.execute('SELECT modified,error FROM details WHERE uuid=?',(uuid,)).fetchone()
            if old and old[0]==header[0] and not old[1]:continue
            value=detail_value(data,header[0])
            if value is None:continue
            db.execute('INSERT OR REPLACE INTO details VALUES (?,?,?,?,?)',
                (uuid,header[0],json.dumps(value) if value else None,None,'disk'))
            seeded+=1
            if seeded%200==0:db.commit();print(json.dumps({'phase':'disk_seed','seeded':seeded}),flush=True)
        except (ValueError,KeyError,TypeError):continue
    db.commit()
    result={'seeded_details':seeded,'saved_feed_pages':len(pages),
            'saved_baseline_report':str(report_path),'cursor':cursor,'unique_saved_detail_bodies':len(detail_shas)}
    print(json.dumps({'phase':'disk_seed_complete',**result}),flush=True)
    return result
