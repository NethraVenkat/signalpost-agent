from signalpost.web.candidates import generate
from signalpost.web.collector import candidate_proof
from signalpost.web.html import Page

def test_former_names_nominate_after_strong_current_origins():
    context={'name':'Current Workshop AS','website':'declared.no','email':'post@email.no','former_names':['Former Workshop AS'], 'subunits':[{'orgnr':'993578843','name':'Registered Workplace AS'}]}
    candidates=generate(context)
    assert [c.origin for c in candidates[:4]]==['registry_website','registry_email','legal_name_slug','legal_name_slug']
    assert any(c.domain=='formerworkshop.no' and c.origin=='former_registered_name' for c in candidates)
    assert any(c.domain=='registeredworkplace.no' and c.subunit_orgnr=='993578843' for c in candidates)
    assert len(candidates)<=8
    assert len(generate(context,limit=100))<=32

def test_historical_candidate_name_never_substitutes_current_identity():
    candidate=next(c for c in generate({'name':'Current AS','former_names':['Previous Workshop AS']}) if c.origin=='former_registered_name')
    page=Page(('<header>Previous Workshop AS</header><main>'+'Company information. '*40+'</main>').encode(),candidate.url)
    assert candidate_proof(page,'923609016',{'name':'Current AS'},candidate,[]).level not in {'HIGH','VERIFIED'}

def test_duplicate_former_name_domains_share_once_only_nomination():
    candidates=generate({'name':'Example AS','former_names':['Example AS','Example AS']},limit=32)
    assert len({c.domain for c in candidates})==len(candidates)
