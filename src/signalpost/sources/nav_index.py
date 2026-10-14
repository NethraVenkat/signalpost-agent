"""Declared official-feed discovery metadata; never publication evidence."""
import gzip
import json
from datetime import datetime,timezone
from pathlib import Path
from uuid import UUID
from urllib.parse import urlsplit
from ..budget import SourceFailure
from ..identity.orgnr import valid
from .nav import BASE,allowed,timestamp

DEFAULT_PATH=Path(__file__).resolve().parents[1]/'data'/'nav_index.json.gz'
HEADER={'schema_version','index_version','built_at','cursor','source_urls','ads_count',
        'employer_count','failed_details','seeded_from_disk','fresh_fetched_ads','ads'}
AD_FIELDS={'uuid','employer_orgnr','status','published','expires','last_modified','etag'}


def validate(data):
    if not isinstance(data,dict) or set(data)!=HEADER or data.get('schema_version')!=1:
        raise SourceFailure('index_version_invalid')
    if not isinstance(data['index_version'],str) or not data['index_version'] or timestamp(data['built_at']) is None:
        raise SourceFailure('index_metadata_invalid')
    cursor=urlsplit(allowed(data['cursor']))
    try:UUID(cursor.path.removeprefix('/api/v1/feed/'))
    except (ValueError,TypeError,AttributeError):raise SourceFailure('index_cursor_invalid') from None
    if not cursor.path.startswith('/api/v1/feed/') or cursor.query:raise SourceFailure('index_cursor_invalid')
    if not isinstance(data['source_urls'],list) or data['source_urls']!=[BASE+'/api/v1/feed',BASE+'/api/v1/feedentry/{uuid}']:
        raise SourceFailure('index_source_invalid')
    if any(type(data[k]) is not int or data[k]<0 for k in ('ads_count','employer_count','failed_details','seeded_from_disk','fresh_fetched_ads')):
        raise SourceFailure('index_counts_invalid')
    if not isinstance(data['ads'],list):raise SourceFailure('index_ads_invalid')
    seen=set()
    for ad in data['ads']:
        if not isinstance(ad,dict) or set(ad)!=AD_FIELDS:raise SourceFailure('index_ad_schema_invalid')
        try:uuid=str(UUID(ad['uuid']))
        except (ValueError,TypeError,AttributeError):raise SourceFailure('index_uuid_invalid') from None
        if uuid!=ad['uuid'] or uuid in seen or not valid(ad['employer_orgnr']) or ad['status']!='ACTIVE':
            raise SourceFailure('index_ad_invalid')
        seen.add(uuid)
        if any(ad[k] is not None and timestamp(ad[k]) is None for k in ('published','expires','last_modified')):
            raise SourceFailure('index_date_invalid')
        if ad['etag'] is not None and not isinstance(ad['etag'],str):raise SourceFailure('index_etag_invalid')
    if len(seen)!=data['ads_count'] or len({a['employer_orgnr'] for a in data['ads']})!=data['employer_count']:
        raise SourceFailure('index_counts_invalid')
    return data


def load(path=DEFAULT_PATH,max_age_days=21,now=None):
    try:
        # Bound both compressed and expanded input before parsing untrusted files.
        if path.stat().st_size>2_000_000:raise SourceFailure('index_size_invalid')
        with gzip.open(path,'rb') as f:
            body=f.read(8_000_001)
        if len(body)>8_000_000:raise SourceFailure('index_size_invalid')
        data=validate(json.loads(body))
    except FileNotFoundError:raise SourceFailure('index_missing') from None
    except (OSError,ValueError,TypeError,KeyError):raise SourceFailure('index_invalid') from None
    age=((now or datetime.now(timezone.utc))-timestamp(data['built_at'])).total_seconds()/86400
    if age<-.01 or age>max_age_days:raise SourceFailure('index_stale')
    if data['failed_details']:raise SourceFailure('index_incomplete')
    return data,age


def write(path,data):
    validate(data)
    body=json.dumps(data,ensure_ascii=True,separators=(',',':'),sort_keys=True).encode()
    packed=gzip.compress(body,mtime=0)
    if len(packed)>=1_000_000:raise SourceFailure('index_compressed_size_target_exceeded')
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_suffix(path.suffix+'.tmp')
    temporary.write_bytes(packed);temporary.replace(path)
    return len(packed)
