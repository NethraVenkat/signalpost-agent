import pytest
from signalpost.web.candidates import Candidate,generate
from signalpost.web.collector import candidate_proof
from signalpost.web.html import Page
from tests.test_websites import html,OUR,OTHER


def test_candidate_order_subunit_before_slugs_with_unchanged_cap():
    rows=generate({'name':'Distinctive Name AS','website':'parent.no','email':'office@email.no',
                  'subunits':[{'orgnr':OTHER,'website':'workplace.no','email':'contact@unit.no'}]})
    assert [c.origin for c in rows]==['registry_website','registry_email','subunit_registry_website','subunit_registry_email']
    assert len(rows)==4 and rows[2].subunit_orgnr==OTHER
    assert not any(c.domain=='gmail.com' for c in generate({'subunits':[{'orgnr':OTHER,'email':'office@gmail.com'}]}))


@pytest.mark.parametrize('owner,accepted',[(OUR,True),(OTHER,True),('988258229',False),('',False)])
def test_subunit_candidate_requires_exact_parent_or_that_subunit(owner,accepted):
    candidate=Candidate('https://workplace.no/','workplace.no','subunit_registry_website',OTHER)
    page=Page(html('Org nr '+owner).encode(),candidate.url)
    proof=candidate_proof(page,OUR,{'name':'Example AS'},candidate,[])
    assert (proof.level=='VERIFIED')==accepted
    if accepted:assert proof.token==owner
