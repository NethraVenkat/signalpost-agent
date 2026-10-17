import pytest
from signalpost.web.candidates import Candidate,generate
from signalpost.web.collector import candidate_proof
from signalpost.web.html import Page
from tests.test_websites import html,OUR,OTHER


def test_candidate_order_subunit_before_bounded_slugs():
    rows=generate({'name':'Distinctive Name AS','website':'parent.no','email':'office@email.no',
                  'subunits':[{'orgnr':OTHER,'website':'workplace.no','email':'contact@unit.no'}]})
    assert [c.origin for c in rows[:4]]==['registry_website','registry_email','subunit_registry_website','subunit_registry_email']
    assert len(rows)==8 and rows[2].subunit_orgnr==OTHER
    assert not any(c.domain=='gmail.com' for c in generate({'subunits':[{'orgnr':OTHER,'email':'office@gmail.com'}]}))


@pytest.mark.parametrize('origin', ['subunit_registry_website', 'subunit_registry_email'])
@pytest.mark.parametrize('owner,accepted',[(OUR,True),(OTHER,True),('988258229',False),('',False)])
def test_subunit_candidate_requires_exact_parent_or_that_subunit(owner,accepted,origin):
    candidate=Candidate('https://workplace.no/','workplace.no',origin,OTHER)
    page=Page(html('Org nr '+owner).encode(),candidate.url)
    proof=candidate_proof(page,OUR,{'name':'Example AS'},candidate,[])
    assert (proof.level=='VERIFIED')==accepted
    if accepted:assert proof.token==owner


@pytest.mark.parametrize('email', ['office@online.no', 'name@yahoo.co.uk', 'name@broadpark.no'])
def test_isp_email_never_nominates_a_company_website(email):
    assert not generate({'email': email})


@pytest.mark.parametrize('owner', [OUR, OTHER])
def test_published_subunit_relationship_preserves_claim_identity_and_evidence(monkeypatch, owner):
    import hashlib
    from types import SimpleNamespace
    from signalpost.web import collector, descriptions
    from signalpost.sources.extract import Section, Source, add
    from signalpost.models.claim import Claim
    from signalpost.models.evidence import canonical, digest
    from signalpost.site import fact

    candidate=Candidate('https://workplace.no/','workplace.no','subunit_registry_website',OTHER)
    raw=html('Org nr '+owner).encode()
    page=Page(raw,candidate.url)
    proof=candidate_proof(page,OUR,{'name':'Example AS'},candidate,[])
    now='2026-10-17T00:00:00Z'
    response=SimpleNamespace(url=candidate.url,body=raw,sha=hashlib.sha256(raw).hexdigest(),retrieved_at=now)
    registry=Section()
    body=b'{"organisasjonsnummer":"993578843","overordnetEnhet":"923609016"}'
    source=Source('https://data.brreg.no/enhetsregisteret/api/underenheter',body,hashlib.sha256(body).hexdigest(),now)
    add(registry,source,OUR,'subunits','subunits.unit.'+OTHER,{'organisation_number':OTHER},'/organisasjonsnummer')
    envelope=SimpleNamespace(claims=registry.claims,evidence=registry.evidence,run=SimpleNamespace(refresh={}))
    http=SimpleNamespace(accepted_pages={},attempts={})
    monkeypatch.setattr(descriptions,'extract',lambda *args:None)
    monkeypatch.setattr(collector,'extract_contacts_and_social',lambda *args,**kwargs:None)
    monkeypatch.setattr(collector,'extract_public_brand',lambda *args:None)
    result=collector.publish_result(OUR,envelope,http,Section(),
        [(candidate,proof,response,page,[(response,page)])],[],{'name':'Example AS'})
    claim=result.claims[0]
    expected=digest([OUR,'official_website',canonical(claim.value),'available',None])
    assert claim.id==expected
    assert len(result.claims)==1 and claim.availability=='available'
    Claim.model_validate(claim.model_dump(mode='json'))
    records={e.id:e.model_dump(mode='json') for e in result.evidence}
    markup=fact(claim.model_dump(mode='json'),records)
    if owner==OTHER:
        assert claim.reasons['relationship']=='Website of registered subunit '+OTHER
        assert claim.value['matched_via_subunit']==OTHER
        assert registry.evidence[0].id in claim.evidence_ids
        assert 'Website of registered subunit '+OTHER in markup
        # Saved pre-revision claims get the same visible label without rewriting facts.
        historical=claim.model_dump(mode='json');historical['reasons']={}
        assert 'Website of registered subunit '+OTHER in fact(historical,records)
    else:
        assert 'relationship' not in claim.reasons
        assert 'matched_via_subunit' not in claim.value
        assert 'Website of registered subunit' not in markup
