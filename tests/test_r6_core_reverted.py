from signalpost.web.collector import candidate_proof
from signalpost.web.candidates import Candidate
from signalpost.web.html import Page

def test_regional_portal_profile_title_is_not_company_site_proof():
    page=Page(('<head><title>Example Brewery - Regional Portal</title><meta property="og:site_name" content="Regional Portal"></head><header>Regional Portal Find businesses</header><main>'+'Featured company information. '*30+'</main><footer>Copyright Regional Portal</footer>').encode(),'https://portal.no/firmaer/example-brewery/')
    context={'name':'Example Brewery AS','website':'https://portal.no/firmaer/example-brewery/'}
    proof=candidate_proof(page,'923609016',context,Candidate(page.url,'portal.no','registry_website'),[])
    assert proof.level not in {'HIGH','VERIFIED'}
