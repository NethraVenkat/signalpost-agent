import copy
import gzip
import hashlib
import json
from pathlib import Path
import asyncio
import pytest
from signalpost.sources import brreg_corporate as bc
from signalpost.sources.http import Response
from signalpost.budget import SourceFailure

FIXTURE = Path(__file__).parent / 'fixtures/brreg_corporate'
MANIFEST = json.loads((FIXTURE / 'manifest.json').read_text(encoding='utf8'))


def response(org, family):
    kind = 'signatur' if family == 'signature' else family
    m = next(x for x in MANIFEST['responses'] if x['org'] == org and x['kind'] == kind)
    body = gzip.decompress((FIXTURE / m['fixture']).read_bytes())
    assert hashlib.sha256(body).hexdigest() == m['fixture_body_sha256']
    return Response(body, m['status'], bc.url(org, family), m['retrieved_at'], m['fixture_body_sha256'])


@pytest.mark.parametrize('org', ['923609016','984851006','914778271'])
@pytest.mark.parametrize('family', bc.FAMILIES)
def test_saved_real_responses_have_exact_replay_and_private_identifiers_absent(org, family):
    r = response(org, family); section = bc.extract(org, family, r)
    if org == '923609016' and family != 'group':
        assert section.state == 'not_available' and not section.claims
        assert section.errors[0].code == 'authority_lookup_unavailable'
        return
    assert section.state == 'available' and section.claims
    data = {'claims': [c.model_dump(mode='json') for c in section.claims]}
    evidence = {e.id: e.model_dump(mode='json') for e in section.evidence}
    assert bc.verify(org, data, evidence, lambda sha: r.body) == len(section.claims)
    assert 'REDACTED' not in json.dumps(data)
    assert 'fodselsdato' not in json.dumps(data)
    for c in section.claims:
        if family == 'group':
            assert org in (c.value['parent_organisation_number'], c.value['subsidiary_organisation_number'])
        bad = copy.deepcopy(data); bad['claims'][0]['value'] = 'invented value'
        with pytest.raises(AssertionError, match='Unsupported corporate'):
            bc.verify(org, bad, evidence, lambda sha: r.body)
        break


@pytest.mark.parametrize('family', bc.FAMILIES)
def test_wrong_company_and_url_never_publish(family):
    org = '984851006'; r = response(org, family)
    with pytest.raises(SourceFailure, match='exact request'):
        bc.extract('914778271', family, r)
    data = json.loads(r.body)
    if family == 'group':
        data['organisasjonsnummer'] = '914778271'; data['children'] = []
    else:
        data['enhet']['organisasjonsnummer'] = '914778271'
    r.body = json.dumps(data).encode()
    with pytest.raises(SourceFailure):
        bc.extract(org, family, r)


def test_real_group_edges_exclude_indirect_subsidiaries_and_support_exact_parent():
    org = '923609016'; r = response(org, 'group'); root = json.loads(r.body)
    direct = {n['organisasjonsnummer'] for n in root['children']}
    section = bc.extract(org, 'group', r)
    assert {c.value['subsidiary_organisation_number'] for c in section.claims} == direct
    child = next(n for n in root['children'] if n.get('children'))
    # Reuse real hierarchy to test a requested nested node; this constructed
    # response URL is a scope test, not an additional claimed live capture.
    nested_org = child['organisasjonsnummer']; r.url = bc.url(nested_org, 'group')
    section = bc.extract(nested_org, 'group', r)
    parent = [c for c in section.claims if c.value['relationship'] == 'parent']
    assert len(parent) == 1 and parent[0].value['parent_organisation_number'] == org
    root['children'][0]['parentOrganisasjonsnummer'] = '914778271'
    r.body = json.dumps(root).encode()
    with pytest.raises(SourceFailure, match='contradicts'):
        bc.extract(nested_org, 'group', r)


@pytest.mark.parametrize('status,state', [(404,'not_available'),(403,'blocked'),(500,'failed')])
def test_http_failure_is_explicit(status, state):
    r=response('984851006','signature');r.status=status
    result=bc.extract('984851006','signature',r)
    assert result.state == state and not result.claims and result.errors


def test_dnb_prokura_preserves_all_possible_combinations_without_birth_dates():
    r=response('984851006','prokura');section=bc.extract('984851006','prokura',r)
    raw=json.loads(r.body)['signeringsKombinasjon']['kombinasjon']
    assert len(section.claims) == len(raw) == 47
    assert all(c.value['people'] and 'possible' in c.value['scope'] for c in section.claims)


def test_uses_registry_client_exact_urls_and_preserves_sourcefailures():
    calls=[]
    class Http:
        async def get(self, url, org):
            calls.append((url,org));return response(org,'signature')
    section=asyncio.run(bc.fetch('984851006','signature',Http()))
    assert section.claims and calls == [(bc.url('984851006','signature'),'984851006')]
    with pytest.raises(SourceFailure):bc.url('984851007','signature')
    with pytest.raises(SourceFailure):bc.url('984851006','other')

def test_runner_and_site_keep_new_sources_and_large_local_payload(tmp_path):
    import httpx
    from signalpost.runner import run
    from signalpost.site import generate_site
    from tests.test_registry import config, handler
    org='984851006'
    cfg=config(tmp_path,[org],corporate_registry=True)
    calls=[]
    original=handler()
    def dispatch(request):
        calls.append(str(request.url))
        for family in bc.FAMILIES:
            if str(request.url) == bc.url(org,family):
                r=response(org,family)
                return httpx.Response(200,content=r.body)
        return original(request)
    async def execute():
        async with httpx.AsyncClient(transport=httpx.MockTransport(dispatch)) as client:
            return await run(cfg,client=client)
    asyncio.run(execute())
    row=json.loads(cfg.output.read_text(encoding='utf8'))
    assert all(row['run']['sections'][f] == 'available' for f in bc.FAMILIES)
    assert all(bc.url(org,f) in calls for f in bc.FAMILIES)
    assert not any('/robots.txt' in u for u in calls)
    result=generate_site(cfg.output,tmp_path/'site')
    assert result['largest_profile_bytes'] < 250000
    raw=(tmp_path/f'site/c/{org}.data.js').read_text(encoding='utf8')
    payload=json.loads(raw.split(' = ',1)[1].rstrip(';\n'))
    original_ids={c['id'][:16] for c in row['claims'] if c['availability']=='available'}
    assert original_ids <= {f['id'] for f in payload['facts']}
    assert len([f for f in payload['registry_details'] if f['field'].startswith('prokura.')]) == 39
    assert bc.verify(org,row,{e['id']:e for e in row['evidence']},lambda sha:(cfg.state_dir/'blobs'/sha).read_bytes()) > 47


def test_library_default_enables_official_corporate_sections(tmp_path):
    from signalpost.config import Config
    cfg=Config(organisations=tmp_path/'in', output=tmp_path/'out', report=tmp_path/'report')
    assert cfg.corporate_registry is True and cfg.time_budget_seconds == 2100
