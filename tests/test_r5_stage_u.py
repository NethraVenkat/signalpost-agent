import json
import sys
import httpx
import respx
import pytest
from signalpost import cli
from tests.test_registry import handler
from tests.test_hybrid_registry import bulk_file

ORG = '923609016'


@pytest.mark.parametrize('disabled', [False, True])
def test_evaluator_seven_flags_build_site_by_default_or_explicitly_disable(tmp_path, monkeypatch, disabled):
    monkeypatch.chdir(tmp_path)
    organisations = tmp_path/'companies.jsonl'
    organisations.write_text(json.dumps({'organisation_number': ORG})+'\n')
    bulk = bulk_file(tmp_path, [ORG])
    output = tmp_path/'out/envelopes.jsonl'
    report = tmp_path/'out/report.json'
    args = ['signalpost', 'run', '--organisations', str(organisations), '--bulk', str(bulk),
            '--output', str(output), '--profiles-output', str(output.with_name('profiles.jsonl')),
            '--report', str(report), '--run-id', 'evaluator-seven-flags', '--expected-count', '1']
    if disabled: args.append('--no-site')
    monkeypatch.setattr(sys, 'argv', args)
    from signalpost.web.fetcher import WebsiteHttp
    from signalpost.budget import SourceFailure
    async def no_dns(self, host, port, org):
        raise SourceFailure('no_such_domain')
    monkeypatch.setattr(WebsiteHttp, 'resolve', no_dns)
    registry = handler()
    def sources(request):
        if request.method=='HEAD':return httpx.Response(200)  # Reachability only; no company fact.
        return registry(request) if request.url.host == 'data.brreg.no' else httpx.Response(404)
    with respx.mock(assert_all_called=False) as router:
        router.route().mock(side_effect=sources)
        assert cli.main() == 0
    data = json.loads(report.read_text())
    assert data['site']['state'] == ('disabled' if disabled else 'available')
    assert output.exists() and output.with_name('profiles.jsonl').exists()
    assert (output.parent/'site/index.html').exists() is not disabled
    if not disabled:
        page = (output.parent/f'site/c/{ORG}.html').read_text(encoding='utf8')
        assert 'How to verify a fact' in page and 'Original source' in page


def test_explicit_site_directory_and_no_site_are_mutually_exclusive(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['signalpost','run','--organisations','a','--output','b',
        '--report','c','--site-dir','site','--no-site'])
    with pytest.raises(SystemExit): cli.main()
