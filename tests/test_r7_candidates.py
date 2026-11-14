from signalpost.web.candidates import legal_name_slugs,legal_name,generate,Candidate
from signalpost.web.collector import candidate_proof
from signalpost.web.html import Page

def test_both_foldings_and_filler_free_joined_hyphenated_variants():
    name='Kj'+chr(248)+'l Holding Eiendom Invest Gruppen Norge AS'
    slugs=legal_name_slugs(legal_name(name))
    assert {'kjoel.no','kjol.no','kjoel.com','kjol.com'}<=set(slugs)
    assert 'kjoel-holding-eiendom-invest-gruppen-norge.no' in slugs
    assert 'kjolholdingeiendominvestgruppennorge.no' in slugs
    assert slugs==sorted(slugs,key=lambda v:not v.endswith('.no'))
    assert len(set(slugs))==len(slugs)

def test_registry_priority_and_candidate_ceiling_unchanged():
    ctx={'name':'Example Holding Norge AS','website':'declared.no','email':'post@email.no'}
    candidates=generate(ctx)
    assert [c.origin for c in candidates[:2]]==['registry_website','registry_email']
    assert len(candidates)<=8 and len(generate(ctx,limit=1000))<=32
    assert any(c.domain=='example.no' for c in generate(ctx,limit=32))

def test_filler_free_guess_is_never_identity_proof():
    p=Page(('<header>Example</header><main>'+'Company information. '*30+'</main>').encode(),'https://example.no/')
    proof=candidate_proof(p,'923609016',{'name':'Example Holding Norge AS'},Candidate(p.url,'example.no','legal_name_slug'),[])
    assert proof.level not in {'HIGH','VERIFIED'}
