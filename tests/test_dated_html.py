from datetime import datetime, timezone
from signalpost.web.activity import parse_html


def test_dated_article_has_local_verbatim_evidence():
    body = b'<article><a href="/nyheter/opening">New office</a><time datetime="2026-10-15">15 October</time></article>'
    items = parse_html(body, 'https://example.no/nyheter', datetime(2026, 10, 17, tzinfo=timezone.utc))
    assert len(items) == 1
    value, locator, span = items[0]
    assert value['date'] == '2026-10-15' and value['url'] == 'https://example.no/nyheter/opening'
    assert value['title'] == 'New office' and locator == '/article/0'
    assert span in body.decode() and len(span) <= 300
    from scripts.accuracy_audit import audit_activity_claim
    evidence = {'source_url': 'https://example.no/nyheter', 'locator': locator,
                'extraction_method': 'signalpost.activity.html.v1'}
    assert audit_activity_claim('923609016', {'value': value}, evidence, body.decode())[0] == 'CORRECT'
    assert audit_activity_claim('923609016', {'value': {**value, 'date': '2026-10-14'}}, evidence, body.decode())[0] == 'INCORRECT'
    for invalid in (body.replace(b'2026-10-15', b'2099-10-15'),
                    body.replace(b'/nyheter/opening', b'https://other.no/nyheter/opening'),
                    body.replace(b'<time', b'<div').replace(b'</time>', b'</div>'),
                    body.replace(b'</article>', b'<a href="/nyheter/other">Other</a></article>')):
        assert not parse_html(invalid, 'https://example.no/nyheter', datetime(2026, 10, 17, tzinfo=timezone.utc))
