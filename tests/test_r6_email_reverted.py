from signalpost.web.collector import candidate_proof
from signalpost.web.candidates import Candidate
from signalpost.web.html import Page

def test_email_alone_does_not_prove_site_after_r6d_revert():
    page=Page(('<header>Another Property AS</header><main>'+'Company information. '*40+'</main><address>Staff contact: person@example.no</address>').encode(),'https://example.no/contact')
    proof=candidate_proof(page,'923609016',{'name':'Our Company AS','email':'person@example.no'},Candidate(page.url,'example.no','registry_email'),[])
    assert proof.level not in {'HIGH','VERIFIED'}
