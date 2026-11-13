"""Extract saved DIGITALIQ responses from seed-20261113, without network calls."""
import base64,csv,gzip,hashlib,io,json,sys
from pathlib import Path
from urllib.parse import urlsplit,parse_qs

ORG='918266917'
ROOT=Path(__file__).resolve().parents[1]

def main():
    source=ROOT/'.data/r5/stageC-daily-run-recovery'
    destination=ROOT/'tests/fixtures/refresh_proof';destination.mkdir(parents=True,exist_ok=True)
    rows=[json.loads(x) for x in (source/'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
    row=next(r for r in rows if r['organisation_number']==ORG)
    website=next(c for c in row['claims'] if c['field']=='official_website' and c['availability']=='available')
    job=next(c for c in row['claims'] if c['field'].startswith('hiring.job.') and c['availability']=='available')
    report=json.loads((source/'report.json').read_text(encoding='utf8'));routes={};bodies={}
    source_events=[]
    for event in report['request_log']:
        url=event['url'];p=urlsplit(url)
        include=(p.hostname=='data.brreg.no' and (ORG in p.path or ORG in parse_qs(p.query).get('overordnetEnhet',[]) or '/oppdateringer/' in p.path))
        include=include or p.hostname=='pam-stilling-feed.nav.no' or (p.hostname or '').removeprefix('www.')=='digitaliq.no'
        if not include or not event.get('content_sha256') or event.get('status') is None:continue
        body=(source/'state/blobs'/event['content_sha256']).read_bytes()
        assert hashlib.sha256(body).hexdigest()==event['content_sha256']
        assert event['status'] not in range(300,400),'Redirect metadata must not be guessed'
        if not body.lstrip().startswith((b'{',b'[')):content='text/plain' if p.path=='/robots.txt' else 'text/html'
        else:content='application/json'
        # Repeated URLs represent the last complete saved response; no ETag or
        # unsupported header is invented. The fixture never fetches live.
        routes[url]={'status':event['status'],'sha256':event['content_sha256'],'content_type':content}
        bodies[event['content_sha256']]=base64.b64encode(body).decode('ascii')
        source_events.append({'url':url,'status':event['status'],'sha256':event['content_sha256']})
    with (ROOT/'reports/r5/release-v4/registry100.csv').open(encoding='utf8',newline='') as f:
        reader=csv.DictReader(f);fields=reader.fieldnames;selected=[r for r in reader if r['organisasjonsnummer']==ORG]
    assert len(selected)==1
    csvout=io.StringIO(newline='');writer=csv.DictWriter(csvout,fieldnames=fields);writer.writeheader();writer.writerows(selected)
    table=csvout.getvalue().encode('utf8');(destination/'registry.csv').write_bytes(table)
    (destination/'companies.jsonl').write_text(json.dumps({'organisation_number':ORG})+'\n',encoding='utf8',newline='\n')
    packed=gzip.compress(json.dumps(bodies,sort_keys=True,separators=(',',':')).encode(),mtime=0)
    (destination/'bodies.json.gz').write_bytes(packed)
    from signalpost.sources.nav_index import load,write
    index,_=load();index=dict(index)
    index['ads']=[ad for ad in index['ads'] if ad['uuid']==job['value']['uuid']]
    assert len(index['ads'])==1
    index.update(ads_count=1,employer_count=1,seeded_from_disk=0,fresh_fetched_ads=1)
    write(destination/'nav_index.json.gz',index)
    manifest={'fixture_version':1,'organisation_number':ORG,'source_sample_seed':20261113,
        'source_run_id':row['run']['run_id'],'source_envelopes_sha256':hashlib.sha256((source/'envelopes.jsonl').read_bytes()).hexdigest(),
        'source_report_sha256':hashlib.sha256((source/'report.json').read_bytes()).hexdigest(),
        'observation_time':'2026-11-13T12:34:07Z','routes':routes,'source_events':source_events,
        'bodies_sha256':hashlib.sha256(packed).hexdigest(),'registry_sha256':hashlib.sha256(table).hexdigest(),
        'nav_index_sha256':hashlib.sha256((destination/'nav_index.json.gz').read_bytes()).hexdigest(),
        'website':website['value']['final_url'],'nav_uuid':job['value']['uuid'],
        'scope':'One exact-identity company from saved seed-20261113 responses, seven isolated mutation types plus unchanged/idempotence/transient checks; not a 100-company generalization.',
        'normalization':'CSV subset reserialized without changing field values. Body bytes are original. Last complete response per URL; absent HTTP headers are not invented. Synthetic auth is offline only and not publication evidence.'}
    (destination/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'routes':len(routes),'body_bytes':len(packed),'org':ORG}))

if __name__=='__main__':main()
