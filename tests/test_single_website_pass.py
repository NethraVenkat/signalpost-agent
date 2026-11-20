import httpx

from tests.test_websites import execute_web, html


def test_single_website_pass_does_not_return_to_pending_legal_page(tmp_path, monkeypatch):
    def response(request):
        if request.url.path == '/robots.txt':
            return httpx.Response(200, text='User-agent: *\nAllow: /')
        if request.url.host == 'example.no' and request.url.path == '/':
            homepage = html('', title='Service information', extra='<footer><a href="/salgsbetingelser">Terms</a></footer>')
            return httpx.Response(200, text=homepage.replace('<header>Example AS</header>', ''))
        if request.url.host == 'example.no' and request.url.path == '/salgsbetingelser':
            return httpx.Response(200, text=html())
        return httpx.Response(404)

    report, row, urls, _ = execute_web(tmp_path, monkeypatch, response=response,
                                       website_request_cap=2)

    assert [event['pass'] for event in report['request_log'] if event.get('section') == 'website'] == ['pass1', 'pass1']
    assert 'adaptive_websites' not in report
    assert not any(url.endswith('/salgsbetingelser') for url in urls)
    assert not any(claim['field'] == 'official_website' for claim in row['claims'])
