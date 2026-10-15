from signalpost.web.html import Page
from signalpost.web.proof import score


def test_customer_heading_does_not_cancel_independent_footer_ownership():
    body=('<html><head><title>Example AS</title></head><h2>Våre kunder</h2>'+'<p>Reported services and customer information.</p>'*15+
          '<footer>© Example AS. Organisasjonsnummer: 923609016</footer></html>')
    assert score(Page(body.encode('utf8'),'https://example.no/'),'923609016',{'name':'Example AS'},'legal_name_slug',[]).level=='VERIFIED'


def test_foreign_footer_does_not_authorize_partner_mention():
    body=('<html><head><title>Example AS</title></head><h2>Our partners</h2><p>Example AS 923609016</p>'+
          '<p>Directory entries describing clients.</p>'*15+'<footer>© Other AS. Org.nr. 988258229</footer></html>')
    assert score(Page(body.encode('utf8'),'https://example.no/'),'923609016',{'name':'Example AS'},'legal_name_slug',[]).level=='REJECT'


def test_script_only_copyright_does_not_override_partner_rejection():
    from signalpost.web.proof import has_copyright_owner
    page=Page(b'<head><title>Example AS</title></head><footer><script>"copyright Example AS 923609016"</script></footer>','https://example.no/')
    assert not has_copyright_owner(page,'923609016','Example AS')
