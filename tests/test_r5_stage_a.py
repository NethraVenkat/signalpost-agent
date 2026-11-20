import json
from datetime import datetime, timedelta, timezone

import pytest

from signalpost.sources import nav
from signalpost.web.candidates import generate, nav_homepages
from tests.test_websites import OUR, OTHER

UUID='00000000-0000-4000-8000-000000000001'

@pytest.mark.parametrize('mutation',['owner','expired','inactive','missing_body'])
def test_nav_index_or_foreign_stale_detail_alone_cannot_nominate(tmp_path,mutation):
    from tests.test_synthesis import envelope
    from signalpost.sources.blobstore import BlobStore
    row,cfg=envelope(tmp_path);blobs=BlobStore(cfg.state_dir);index=nav.Index()
    now=datetime.now(timezone.utc);body={'uuid':UUID,'status':'ACTIVE','ad_content':{
        'uuid':UUID,'published':(now-timedelta(days=1)).isoformat(),
        'expires':(now+timedelta(days=1)).isoformat(),'employer':{'orgnr':OUR,'homepage':'https://good.no'}}}
    if mutation=='owner':body['ad_content']['employer']['orgnr']=OTHER
    elif mutation=='expired':body['ad_content']['expires']=(now-timedelta(days=1)).isoformat()
    elif mutation=='inactive':body['status']='INACTIVE'
    sha=blobs.put(json.dumps(body).encode()) if mutation!='missing_body' else '0'*64
    index.ads[OUR]=[nav.Ad({'uuid':UUID,'employer_orgnr':OUR},sha,'https://nav.invalid',
        '2026-11-13T00:00:00Z',None,None,None,None)]
    assert nav_homepages(row,index,blobs)==[]


def test_candidates_rank_authoritative_nomination_above_name_and_preserve_eight_first_pass_limit():
    context={'name':'Example Business AS','website':'registered.no','email':'x@email.no',
        'subunits':[{'orgnr':OTHER,'website':'branch.no'}],
        'nav_homepages':[{'url':'https://navnominee.no'}]}
    candidates=generate(context)
    assert [c.origin for c in candidates[:6]]==['registry_website','registry_email','legal_name_slug','legal_name_slug','subunit_registry_website','nav_employer_homepage']
    assert len(candidates)<=8 and len(generate(context,limit=32))<=32
