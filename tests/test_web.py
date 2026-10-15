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


def test_public_brand_extraction_filters_orgnr_and_legal_matches():
    from signalpost.web.collector import publish_result
    from signalpost.web.html import Page
    from signalpost.sources.extract import Section
    from types import SimpleNamespace

    def make_choice(url, html_bytes, page_obj):
        resp = SimpleNamespace(url=url, body=html_bytes, sha="0"*64, retrieved_at="2026-10-15T00:00:00Z")
        cand = SimpleNamespace(origin="nom", subunit_orgnr=None)
        proof = SimpleNamespace(level="HIGH", token="Velkommen", proof_type="signals", signals=[], points=100, other_orgnrs=[])
        return (cand, proof, resp, page_obj, [(resp, page_obj)])

    # Case 1: Org nr suffix and legal name match (A&A REGNSKAP AS)
    html1 = b"""<!DOCTYPE html><html><head>
    <title>A&amp;A REGNSKAP AS - Org. nr. : 936494285</title>
    <meta property="og:site_name" content="A&amp;A REGNSKAP AS - Org. nr.  : 936494285">
    </head><body><p>Velkommen til oss</p></body></html>"""
    page1 = Page(html1, "https://aandaregnskap.no/")
    section1 = Section("website")
    envelope1 = SimpleNamespace(claims=[], evidence=[], run=SimpleNamespace(refresh={}))
    http_mock = SimpleNamespace(accepted_pages={}, attempts={})
    publish_result(
        "936494285", envelope1, http_mock, section1,
        choices=[make_choice("https://aandaregnskap.no/", html1, page1)],
        attempts=[], context={"name": "A&A REGNSKAP AS"},
    )
    # Brand matching legal name must be withheld
    brand_claims1 = [c for c in section1.claims if c.field == "public_brand"]
    assert len(brand_claims1) == 0

    # Case 2: Storefront tagline title structure (Sealine Products AS)
    html2 = b"""<!DOCTYPE html><html><head>
    <title>Nettbutikk For Fiskeutstyr og B&aring;tutstyr - Sealine Products</title>
    <meta property="og:sitename" content="Sealine Products AS - Nettbutikk">
    </head><body><p>Velkommen til butikken</p></body></html>"""
    page2 = Page(html2, "https://sealine-products.no/")
    section2 = Section("website")
    envelope2 = SimpleNamespace(claims=[], evidence=[], run=SimpleNamespace(refresh={}))
    publish_result(
        "881238292", envelope2, http_mock, section2,
        choices=[make_choice("https://sealine-products.no/", html2, page2)],
        attempts=[], context={"name": "SEALINE PRODUCTS AS"},
    )
    brand_claims2 = [c for c in section2.claims if c.field == "public_brand"]
    assert len(brand_claims2) == 0

    # Case 3: Genuine distinct public brand (Fastcharge by Hafslund for FASTCHARGE AS)
    html3 = b"""<!DOCTYPE html><html><head>
    <title>Fastcharge by Hafslund | Ladel\xc3\xb8sninger for bedrifter</title>
    <meta property="og:site_name" content="Fastcharge by Hafslund">
    </head><body><p>Velkommen til Fastcharge by Hafslund.</p></body></html>"""
    page3 = Page(html3, "https://fastcharge.no/")
    section3 = Section("website")
    envelope3 = SimpleNamespace(claims=[], evidence=[], run=SimpleNamespace(refresh={}))
    publish_result(
        "928807908", envelope3, http_mock, section3,
        choices=[make_choice("https://fastcharge.no/", html3, page3)],
        attempts=[], context={"name": "FASTCHARGE AS"},
    )
    brand_claims3 = [c for c in section3.claims if c.field == "public_brand"]
    assert len(brand_claims3) == 1
    assert brand_claims3[0].value == "Fastcharge by Hafslund"


def test_descriptions_filters_legal_pages_forms_and_address_blocks():
    import hashlib
    from signalpost.web.descriptions import extract
    from signalpost.web.html import Page
    from signalpost.sources.extract import Section
    from types import SimpleNamespace

    proof_claim = SimpleNamespace(
        id="proof_123",
        field="official_website",
        value={"identity_level": "VERIFIED"},
        availability="available",
        confidence=1.0,
        evidence_ids=["ev1"],
    )

    # 1. Terms & Conditions page must be skipped entirely
    html_terms = b"""<html><head>
    <meta name="description" content="Formelle vilk\xc3\xa5r for bruk av nettsiden Galleri M.">
    </head><body><p>Disse vilk\xc3\xa5rene gjelder kj\xc3\xb8p.</p></body></html>"""
    page_terms = Page(html_terms, "https://gallerim.no/om-galleri-m/vilkar-og-betingelser/")
    resp_terms = SimpleNamespace(url="https://gallerim.no/om-galleri-m/vilkar-og-betingelser/", body=html_terms, sha=hashlib.sha256(html_terms).hexdigest(), retrieved_at="2026-10-15T00:00:00Z")

    sec1 = Section("website")
    extract(sec1, "912134784", proof_claim, [(resp_terms, page_terms)])
    assert len(sec1.claims) == 0

    # 2. Short contact form title must be skipped
    html_form = b"""<html><head>
    <meta name="description" content="Kontakt Oss Sp\xc3\xb8rreskjema">
    <meta property="og:description" content="Kontakt Oss Sp\xc3\xb8rreskjema">
    </head><body><h1>Kontakt oss</h1></body></html>"""
    page_form = Page(html_form, "https://aktivit.no/kontakt-oss/")
    resp_form = SimpleNamespace(url="https://aktivit.no/kontakt-oss/", body=html_form, sha=hashlib.sha256(html_form).hexdigest(), retrieved_at="2026-10-15T00:00:00Z")

    sec2 = Section("website")
    extract(sec2, "994813560", proof_claim, [(resp_form, page_form)])
    assert len(sec2.claims) == 0

    # 3. Address paragraph skipped in favor of real about prose
    html_about = b"""<html><head>
    <meta name="description" content="BoilerTECH er en ledende spesialist p\xc3\xa5 industrielle kjeler i Norge.">
    </head><body>
    <p>Lasta 50<br />4405 Flekkefjord</p>
    <p>+47 383 752 00</p>
    <p>BoilerTECH AS er et selskap med solid kompetanse og ti\xc3\xa5r av erfaring innen industrielle dampkjeler.</p>
    </body></html>"""
    page_about = Page(html_about, "https://boilertech.no/om-oss")
    resp_about = SimpleNamespace(url="https://boilertech.no/om-oss", body=html_about, sha=hashlib.sha256(html_about).hexdigest(), retrieved_at="2026-10-15T00:00:00Z")

    sec3 = Section("website")
    extract(sec3, "917803498", proof_claim, [(resp_about, page_about)])
    about_claims = [c for c in sec3.claims if "about_paragraph" in c.field]
    assert len(about_claims) == 1
    assert "BoilerTECH AS er et selskap" in about_claims[0].value["text"]
    assert "Lasta 50" not in about_claims[0].value["text"]
