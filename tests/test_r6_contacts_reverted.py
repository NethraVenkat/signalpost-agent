from signalpost.web.collector import candidate_proof
from signalpost.web.candidates import Candidate
from signalpost.web.html import Page

def test_shared_registry_contacts_do_not_prove_another_publisher():
    page=Page(('<header>Example Broadband AS</header><main>'+'Company information. '*40+'</main><footer>Example Broadband AS Telefon: 22 33 44 55 Adresse: Eksempelgata 12, 0123 Oslo</footer>').encode(),'https://example.no/')
    proof=candidate_proof(page,'923609016',{'name':'Example Holding AS','phone':'22334455','street':'Eksempelgata 12','postcode':'0123'},Candidate(page.url,'example.no','legal_name_slug'),[])
    assert proof.level not in {'HIGH','VERIFIED'}
