from signalpost.web.html import Page
from signalpost.web.publisher import extract_publisher


def publisher(body, path='/'):
    return extract_publisher(Page(body.encode(), 'https://example.no' + path))


def test_publisher_locations_and_contact_block():
    p = publisher('<title>Example AS</title><meta property="og:site_name" content="Example">'
                  '<header><img alt="Example logo"></header><div><h2>Kontakt</h2>'
                  '<p>Example AS Org.nr 923609016 Telefon 12345678</p></div>'
                  '<footer>© Example AS</footer>', '/kontakt')
    assert {'title', 'og:site_name', 'header', 'footer', 'imprint-kontakt'} <= {f.location for f in p.fragments}
    assert '923609016' in p.text and 'Example logo' in p.text


def test_customer_partner_reference_and_article_mentions_excluded():
    p = publisher('<header>Example AS</header><section><h2>Our clients</h2>Foreign AS 993578843</section>'
                  '<footer><div class="partner-logos">Partner AS 993578843</div>'
                  '<div class="references">Other AS 993578843</div>Example AS</footer>'
                  '<article>News about Foreign AS 993578843</article>')
    assert 'Example AS' in p.text
    assert '993578843' not in p.text


def test_agency_credit_and_hidden_content_excluded():
    p = publisher('<footer>© Example AS <span>Levert av <a>Agency AS 993578843</a></span>'
                  '<div class="credits">Design av Agency AS 993578843</div>'
                  '<p hidden>Hidden AS 993578843</p><script>993578843</script></footer>')
    assert 'Example AS' in p.text
    assert '993578843' not in p.text and 'Agency' not in p.text


def test_body_mention_is_not_publisher_and_no_whole_contact_page():
    p = publisher('<title>Example</title><main><p>We helped Foreign AS yesterday.</p>'
                  '<p>Example AS Org.nr 923609016</p></main>', '/kontakt')
    assert 'Foreign' not in p.text and '923609016' in p.text


def test_inline_credit_keeps_own_copyright_prefix():
    p = publisher('<footer>© Example AS. Utviklet av Agency AS 993578843</footer>')
    assert 'Example AS' in p.text and '993578843' not in p.text


def test_news_and_hidden_logo_are_not_publisher():
    p = publisher('<div class="news"><img class="logo" alt="Foreign AS"></div>'
                  '<img class="logo" hidden alt="Hidden AS"><header>Example AS</header>')
    assert 'Foreign' not in p.text and 'Hidden' not in p.text


def test_text_logo_and_copyright_outside_semantic_footer():
    p = publisher('<a class="site-logo">Example AS</a><span class="copyright">© Example AS</span>')
    assert {'logo', 'copyright'} <= {f.location for f in p.fragments}


def test_header_layout_modifier_does_not_turn_biographies_into_publisher():
    p = publisher('<div class="header-over-content dmPageBody hasStickyHeader">'
                  '<div class="d-header-wrapper">Example AS</div>'
                  '<main><h2>Team</h2><p>Our employee formerly worked at Foreign Financial Group.</p></main>'
                  '<footer>Example AS</footer></div>')
    assert 'Example AS' in p.text
    assert 'Foreign Financial Group' not in p.text


def test_underscore_region_component_is_supported():
    p = publisher('<div class="site_header">Example AS</div><div id="site_footer">Org.nr 923609016</div>')
    assert {'header', 'footer'} <= {f.location for f in p.fragments}


def test_footer_copyright_does_not_turn_body_into_copyright_publisher():
    p = publisher('<div><main><p>Employee formerly worked at Foreign Financial Group.</p></main>'
                  '<footer>© Example AS</footer></div>', '/about')
    assert 'Example AS' in p.text and 'Foreign Financial Group' not in p.text
