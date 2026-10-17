from signalpost.web.html import Page
from signalpost.web.social import discover


def test_long_anchor_attributes_do_not_truncate_profile_url_from_evidence():
    url = 'https://www.facebook.com/skedsmonaprapatklinikk'
    body = '<footer><a class="' + 'x' * 450 + '" href="' + url + '">Facebook</a></footer>'
    page = Page(body.encode(), 'https://example.no/')
    assert page.links[0].href == url
    span = discover(page)[url]
    assert len(span) <= 300 and span in body and url in span


def test_unquoted_long_link_ignores_href_text_inside_another_attribute():
    url = 'https://www.instagram.com/example'
    body = '<footer><a class=\'href="https://wrong.invalid/" ' + 'x' * 450 + '\' href=' + url + '>Instagram</a></footer>'
    span = discover(Page(body.encode(), 'https://example.no/'))[url]
    assert url in span and span in body and len(span) <= 300
