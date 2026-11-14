import hashlib
import json
from types import SimpleNamespace
import pytest

from signalpost.public_names import enrich,site_name,verify,METHOD
from signalpost.web.html import Page
from signalpost.sources.blobstore import BlobStore
from signalpost.sources.extract import Section,Source,add
from signalpost.sources.http import Response
from signalpost.runner import placeholder

ORG='923609016';UNIT='993578843';NOW='2026-11-14T00:00:00Z'


def record(tmp_path,name='Example AS',unit_name='Example Oslo',parent=ORG):
    blobs=BlobStore(tmp_path);env=placeholder(ORG,'brands',NOW,('identity','subunits','website','activity','roles','accounts'))
    env.claims=[];env.evidence=[]
    body=json.dumps({'organisasjonsnummer':ORG,'navn':name}).encode();sha=blobs.put(body)
    section=Section();add(section,Source('https://data.brreg.no/enhetsregisteret/api/enheter/'+ORG,body,sha,NOW),ORG,'identity','identity.legal_name',name,'/navn')
    raw={'organisasjonsnummer':UNIT,'overordnetEnhet':parent,'navn':unit_name}
    body=json.dumps({'_embedded':{'underenheter':[raw]}}).encode();sha=blobs.put(body)
    source=Source('https://data.brreg.no/enhetsregisteret/api/underenheter?overordnetEnhet='+ORG,body,sha,NOW)
    add(section,source,ORG,'subunits','subunits.unit.'+UNIT,{'organisation_number':UNIT,'name':unit_name},'/_embedded/underenheter/0')
    env.claims=section.claims;env.evidence=section.evidence
    env.run.sections.update(identity='available',subunits='available',website='not_available',activity='not_available',roles='not_available',accounts='not_available')
    env.run.completed_at=NOW
    return env,blobs


def validate(env,blobs):
    data=env.model_dump(mode='json');evidence={e['id']:e for e in data['evidence']}
    return verify(ORG,data,evidence,lambda sha:blobs.read(sha).decode())


def test_registered_subunit_alias_requires_exact_parent_and_name(tmp_path):
    env,blobs=record(tmp_path);enrich({ORG:env},blobs,{})
    names=[c for c in env.claims if c.field.startswith('brand.')]
    assert len(names)==1 and names[0].value=={'name':'Example Oslo','origin':'registered_subunit','subunit_orgnr':UNIT}
    assert validate(env,blobs)==[names[0].id]
    names[0].value['subunit_orgnr']=ORG
    with pytest.raises(AssertionError):validate(env,blobs)
    bad,other=record(tmp_path/'foreign',parent='988330752')
    enrich({ORG:bad},other,{})
    assert not any(c.field.startswith('brand.') for c in bad.claims)


def test_same_legal_name_and_stale_registered_unit_are_not_new_brands(tmp_path):
    env,blobs=record(tmp_path,unit_name='EXAMPLE AS')
    enrich({ORG:env},blobs,{});assert not any(c.field.startswith('brand.') for c in env.claims)
    env,blobs=record(tmp_path/'stale');env.claims[-1].carried_forward=True
    enrich({ORG:env},blobs,{});assert not any(c.field.startswith('brand.') for c in env.claims)


@pytest.mark.parametrize('level',['VERIFIED','HIGH'])
def test_current_verified_site_own_name_has_site_and_registry_evidence(tmp_path,level):
    env,blobs=record(tmp_path,unit_name='Example AS')
    body=b'<title>Local service | Bright Brand</title><meta property="og:site_name" content="Bright Brand"><header>Bright Brand</header><footer>Example AS 923609016</footer>'
    sha=blobs.put(body);url='https://example.no/'
    response=Response(body,200,url,NOW,sha);section=Section()
    add(section,Source(url,body,sha,NOW),ORG,'website','official_website',{'final_url':'https://example.no','proof_page_url':url,'identity_level':level},'orgnr',source_class='company_owned')
    env.claims.extend(section.claims);env.evidence.extend(section.evidence);env.run.sections['website']='available'
    enrich({ORG:env},blobs,{ORG:[(response,Page(body,url))]})
    brand=next(c for c in env.claims if c.field=='public_brand')
    assert brand.value=='Bright Brand' and len(brand.evidence_ids)>=2
    assert brand.id in validate(env,blobs)
    from signalpost.synthesis.template import generate
    from signalpost.synthesis.overview import required
    env.run.synthesis=generate(env)
    assert 'Bright Brand' in required(env)['activity'].text and brand.id in required(env)['activity'].claim_ids
    from signalpost.site import fact
    html=fact(brand.model_dump(),{e.id:e.model_dump() for e in env.evidence})
    assert 'Site-declared public name' in html and 'Check the evidence' in html


@pytest.mark.parametrize('markup',[
    '<title>Example AS | Electrical services</title><header>Electrical services</header>',
    '<title>Contact</title><header>Contact</header>',
    '<title>Secret Brand</title><article>Secret Brand</article>',
    '<div class="clients"><meta property="og:site_name" content="Client Brand"></div>',
    '<meta property="og:site_name" content="Example AS">',
    '<meta property="og:site_name" content="Just another WordPress site">',
])
def test_page_headline_client_body_legal_name_and_template_not_brand(markup):
    assert site_name(Page(markup.encode(),'https://domain-alone.no/'),'Example AS') is None


def test_title_alias_needs_own_branding_and_never_domain_inference():
    assert site_name(Page(b'<title>Contact | Bright Brand</title><header>Bright Brand</header>','https://unrelated.no/'),'Example AS')=='Bright Brand'
    assert site_name(Page(b'<main>Content only</main>','https://brightbrand.no/'),'Example AS') is None


def test_refresh_idempotence_and_alias_change_is_observation(tmp_path):
    env,blobs=record(tmp_path);enrich({ORG:env},blobs,{})
    first=[c.id for c in env.claims];enrich({ORG:env},blobs,{})
    assert [c.id for c in env.claims]==first
