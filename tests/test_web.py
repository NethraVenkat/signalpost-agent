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
