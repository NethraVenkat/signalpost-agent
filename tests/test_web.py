import pytest
from signalpost.web.candidates import extract_sitemap_domains, Candidates
from signalpost.web.search import brave_search_mock

SAMPLE_SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://acmesolutions.no/</loc></url>
  <url><loc>https://acmesolutions.no/om-oss</loc></url>
  <url><loc>https://acme-shop.no/produkter</loc></url>
  <url><loc>https://partner-portal.com/irrelevant</loc></url>
  <url><loc>https://facebook.com/acme</loc></url>
</urlset>
"""

def test_sitemap_extraction(monkeypatch):
    # 1. Test parsing from raw XML string
    domains = extract_sitemap_domains(SAMPLE_SITEMAP, legal_name_str="Acme Solutions AS", brand_name="Acme")
    assert "acmesolutions.no" in domains
    assert "acme-shop.no" in domains
    assert "partner-portal.com" not in domains  # filtered out by identity token
    assert "facebook.com" not in domains        # filtered out by SOCIAL policy
    assert len(domains) <= 3

    # 2. Test fetching via mock HTTP response
    import httpx
    def handler(request):
        if "sitemap.xml" in request.url.path:
            return httpx.Response(200, text=SAMPLE_SITEMAP)
        return httpx.Response(404)
    
    real_get = httpx.get
    def mock_get(url, **kwargs):
        transport = httpx.MockTransport(handler)
        with httpx.Client(transport=transport) as client:
            return client.get(url, **kwargs)
    
    monkeypatch.setattr("httpx.get", mock_get)
    fetched_domains = extract_sitemap_domains("acmesolutions.no", legal_name_str="Acme Solutions AS", brand_name="Acme")
    assert "acmesolutions.no" in fetched_domains
    assert len(fetched_domains) <= 3


def test_brave_search_mock():
    company = "Acme Solutions AS"
    brand = "Acme"
    orgnr = "912345678"

    results = brave_search_mock(company, brand=brand, orgnr=orgnr, limit=5)
    assert len(results) > 0
    assert len(results) <= 5

    for res in results:
        assert "domain" in res
        assert "title" in res
        assert "snippet" in res
        assert "score" in res
        # Verify identity scoring threshold >= 60 pts
        assert res["score"] >= 60
        # Generic directory proff.no and unrelated news should be excluded
        assert res["domain"] not in ("proff.no", "dagensnyheter.no")


def test_candidates_add_company_scope():
    context = {
        "name": "Acme Solutions AS",
        "brand": "Acme",
        "orgnr": "912345678",
        "website": "https://acmesolutions.no"
    }
    candidates, report = Candidates.add_company_scope(context)
    assert len(candidates) > 0
    assert "sitemap_domains" in report
    assert "brave_domains" in report
    assert "total_new" in report
    assert any(c.origin == "search_brave" for c in candidates)


def test_activity_xml_fallbacks_and_malformed():
    from datetime import datetime, timezone
    from signalpost.web.activity import parse

    now = datetime(2026, 10, 14, tzinfo=timezone.utc)
    base_url = "https://example.no/news"

    # 1. Valid RSS with pubDate
    rss_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
      <channel>
        <title>Example News</title>
        <item>
          <title>Annual Product Launch</title>
          <link>https://example.no/news/product-launch</link>
          <pubDate>Wed, 14 Oct 2026 12:00:00 GMT</pubDate>
          <description>We launched our new product today.</description>
        </item>
      </channel>
    </rss>"""
    items, children = parse(rss_xml, base_url, now)
    assert len(items) == 1
    assert items[0][0]["title"] == "Annual Product Launch"
    assert items[0][0]["date"] == "2026-10-14"
    assert items[0][0]["date_source"] == "pubDate"
    assert children == []

    # 2. Sitemap index with child sitemaps
    sitemap_index_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
    <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <sitemap>
        <loc>https://example.no/news-sitemap.xml</loc>
        <lastmod>2026-10-14</lastmod>
      </sitemap>
    </sitemapindex>"""
    items, children = parse(sitemap_index_xml, base_url, now)
    assert items == []
    assert children == ["https://example.no/news-sitemap.xml"]

    # 3. Empty feed/sitemap
    empty_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    </urlset>"""
    items, children = parse(empty_xml, base_url, now)
    assert items == []
    assert children == []

    # 4. Malformed XML handling
    with pytest.raises(Exception):
        parse(b"<not valid xml at all", base_url, now)

    # 5. DTD entity injection refusal
    dtd_xml = b"""<?xml version="1.0"?>
    <!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
    <rss version="2.0"><channel><item></item></channel></rss>"""
    with pytest.raises(ValueError, match="XML declarations refused"):
        parse(dtd_xml, base_url, now)

