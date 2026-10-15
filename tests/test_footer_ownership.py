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


def test_registered_name_spacing_does_not_change_published_identity():
    from signalpost.web.proof import has_copyright_owner
    page=Page('<head><title>TubingTec AS</title></head><footer>© 2024 TubingTec AS Organisasjonsnummer: 932 761 483</footer>'.encode('utf8'),'https://example.no/')
    context={'name':'TUBING TEC AS'}
    assert has_copyright_owner(page,'932761483',context['name'])
    assert not has_copyright_owner(page,'932761483','Tubing AS')
    assert context['name']=='TUBING TEC AS'


def test_independent_footer_runs_dependent_production_extraction(tmp_path,monkeypatch):
    from tests.test_websites import execute_web,html
    body=html('© Example AS. Organisasjonsnummer: 923609016 <a href="https://linkedin.com/company/example">LinkedIn</a>',
              '<h2>Our customers</h2><p>Example AS provides specialized services for customers across Norway.</p>'
              '<a href="mailto:office@example.no">Office</a><a href="https://linkedin.com/company/example">LinkedIn</a>')
    body=body.replace('</head>','<meta name="description" content="Example AS provides specialized services for customers across Norway."></head>')
    _,row,_,_=execute_web(tmp_path,monkeypatch,body)
    facts={c['field']:c['value'] for c in row['claims'] if c['availability']=='available'}
    assert facts['official_website']['identity_level']=='VERIFIED'
    assert any(k.startswith('website_description.') for k in facts)
    assert 'office@example.no' in facts.values()
    assert any(k.startswith('social_profile.') for k in facts)
