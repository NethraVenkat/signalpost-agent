from signalpost.web.html import Page
from signalpost.web.social import discover


def test_long_anchor_attributes_do_not_truncate_profile_url_from_evidence():
    url = 'https://www.facebook.com/skedsmonaprapatklinikk'
    body = '<footer><a class="' + 'x' * 450 + '" href="' + url + '">Facebook</a></footer>'
    page = Page(body.encode(), 'https://example.no/')
    assert page.links[0].href == url
    span = discover(page)[url]
    assert len(span) <= 300 and span in body and url in span
