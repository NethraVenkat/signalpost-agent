import json
from pathlib import Path
import httpx
import pytest
import respx
from scripts.check_live_run import check
from scripts.verify_output import verify
from tests.test_registry import config,execute,handler


def fixture(tmp_path):
    cfg=config(tmp_path,['923609016','993578843'],site_dir=tmp_path/'site')
    def response(request):
        if request.url.path.endswith('/roller'):raise httpx.ReadTimeout('legitimate live source timeout')
        return handler()(request)
    report,rows=execute(cfg,response)
    assert any(r['run']['sections']['roles']=='failed' for r in rows)
    return cfg,rows


def test_live_gate_accepts_honest_source_failure_but_keeps_all_proof_checks(tmp_path):
    cfg,rows=fixture(tmp_path)
    result=check(cfg.output,cfg.organisations,cfg.state_dir,cfg.report,cfg.site_dir,2)
    assert result['site_verified'] and result['complete_briefing_contracts']==2
    with pytest.raises(AssertionError):verify(cfg.output,cfg.state_dir,2,cfg.organisations,cfg.report,require_clean=True)


@pytest.mark.parametrize('mutation',['missing_site','missing_profile','oversized_profile','size_report','order','schema','unsupported_value','bad_blob'])
def test_live_gate_rejects_broken_artifacts(tmp_path,mutation):
    cfg,rows=fixture(tmp_path)
    if mutation=='missing_site':(cfg.site_dir/'index.html').unlink()
    elif mutation=='missing_profile':(cfg.site_dir/'c/923609016.html').unlink()
    elif mutation=='oversized_profile':(cfg.site_dir/'c/923609016.html').write_bytes(b' ' * 250_000)
    elif mutation=='size_report':
        report=json.loads(cfg.report.read_text(encoding='utf8'))
        report['site']['largest_profile_bytes']-=1
        cfg.report.write_text(json.dumps(report),encoding='utf8')
    elif mutation=='order':
        cfg.output.write_text(''.join(json.dumps(r)+'\n' for r in reversed(rows)),encoding='utf8')
    elif mutation=='schema':
        rows[0]['claims'][0]['unexpected_schema_key']=True
        cfg.output.write_text(''.join(json.dumps(r)+'\n' for r in rows),encoding='utf8')
    elif mutation=='unsupported_value':
        rows[0]['run']['synthesis']['briefing'][0]['text']='Invented company value 999999999.'
        cfg.output.write_text(''.join(json.dumps(r)+'\n' for r in rows),encoding='utf8')
    else:
        e=next(e for e in rows[0]['evidence'] if any(e['id'] in c['evidence_ids'] for c in rows[0]['claims'] if c['availability']=='available'))
        (cfg.state_dir/'blobs'/e['content_sha256']).write_bytes(b'broken proof')
    with pytest.raises((AssertionError,ValueError)):
        check(cfg.output,cfg.organisations,cfg.state_dir,cfg.report,cfg.site_dir,2)


def test_workflow_runs_exact_seven_flags_fresh_default_budget_and_uploads():
    source=Path('.github/workflows/ci.yml').read_text(encoding='utf8')
    run=source.split('signalpost run \\',1)[1].split('| tee',1)[0]
    import re
    assert re.findall(r'--[a-z-]+',run)==['--organisations','--bulk','--output','--profiles-output','--report','--run-id','--expected-count']
    assert 'mkdir "$LIVE_WORK"' in source and 'cd "$LIVE_WORK"' in source
    assert '${{ runner.temp }}' not in source
    assert 'LIVE_WORK="$RUNNER_TEMP/signalpost-live20-${GITHUB_RUN_ID}-${GITHUB_RUN_ATTEMPT}"' in source
    assert '"LIVE_WORK=$LIVE_WORK" >> "$GITHUB_ENV"' in source
    assert '${{ env.LIVE_WORK }}/report.json' in source
    assert '--require-clean' not in source and '--time-budget-seconds' not in run
    assert 'timeout-minutes: 10' in source and 'actions/upload-artifact@v4' in source and 'if: always()' in source


def test_large_profile_defers_only_duplicate_explorer_rows_under_same_gate(tmp_path,monkeypatch):
    from signalpost import site
    cfg,rows=fixture(tmp_path)
    original=site.profile
    # Model a large fact body just under the gate without its duplicate audit
    # table. Vary only that existing table's initial row count.
    def large(row,title,explorer_rows=site.EXPLORER_VISIBLE_ROWS,**kwargs):
        rendered=original(row,title,explorer_rows,**kwargs)
        return rendered+' '*(210000)+(' '*(explorer_rows*600))
    monkeypatch.setattr(site,'profile',large)
    before=cfg.output.read_bytes()
    metrics=site.generate_site(cfg.output,tmp_path/'deferred')
    assert metrics['largest_profile_bytes']<=site.PROFILE_HTML_BUDGET
    assert metrics['largest_profile_bytes']<site.PROFILE_HTML_REGRESSION_LIMIT
    assert all(p.stat().st_size<site.PROFILE_HTML_REGRESSION_LIMIT for p in (tmp_path/'deferred/c').glob('*.html'))
    assert cfg.output.read_bytes()==before
    for row in rows:
        org=row['organisation_number'];page=(tmp_path/'deferred/c'/f'{org}.html').read_text(encoding='utf8')
        payload=json.loads((tmp_path/'deferred/c'/f'{org}.data.js').read_text(encoding='utf8').split(' = ',1)[1].rsplit(';',1)[0])
        import re
        shown=int(re.search(r'Showing (\d+) of',page)[1])
        assert shown<site.EXPLORER_VISIBLE_ROWS
        assert shown+len(payload['explorer_rows'])==len(row['claims'])
        assert all(site.anchor(c) in page for c in row['claims'])
        assert len(payload['facts'])==sum(bool(c['evidence_ids']) or c['availability']=='available' for c in row['claims'])
        expected={c['id'][:16]:c for c in row['claims'] if c['evidence_ids'] or c['availability']=='available'}
        actual={fact['id']:fact for fact in payload['facts']}
        assert actual.keys()==expected.keys()
        assert all(actual[cid]['value']==c.get('value') and actual[cid]['evidence_ids']==c.get('evidence_ids',[]) for cid,c in expected.items())
        assert {record[1] for record in payload['records']}=={eid for c in expected.values() for eid in c.get('evidence_ids',[])}


def test_seven_flag_run_keeps_oversized_company_profile_under_html_cap(tmp_path, monkeypatch):
    from signalpost import cli, site
    from signalpost.web import policy
    from tests.test_websites import OTHER, OUR, html

    route = '/' + 'contact-' * 180
    source_url = 'https://example.no' + route
    addresses = [f'office{i}@example.no' for i in range(155)]
    contacts = ''.join(f'<p><a href="mailto:{address}">{address}</a></p>' for address in addresses)
    body = html('Org.nr ' + OUR, contacts)
    batch = tmp_path / 'companies.jsonl'
    bulk = tmp_path / 'registry.csv'
    batch.write_text(''.join(json.dumps({'organisation_number': org}) + '\n' for org in (OUR, OTHER)),
                     encoding='utf8')
    bulk.write_text(f'organisasjonsnummer,navn,hjemmeside\n{OUR},EXAMPLE AS,{source_url}\n'
                    f'{OTHER},OTHER AS,https://other.no/\n', encoding='utf8')
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr('sys.argv', ['signalpost', 'run', '--organisations', str(batch), '--bulk', str(bulk),
                                    '--output', 'envelopes.jsonl', '--profiles-output', 'profiles.jsonl',
                                    '--report', 'report.json', '--run-id', 'oversized-profile', '--expected-count', '2'])

    async def resolve_public(host, port=443):
        return ['93.184.216.34']

    monkeypatch.setattr(policy, 'resolve_public', resolve_public)

    def serve(request):
        if request.method == 'HEAD':
            return httpx.Response(200)
        if request.url.host == 'data.brreg.no' and any(org in str(request.url) for org in (OUR, OTHER)):
            return handler()(request)
        if request.url.host in {'example.no', 'other.no'}:
            if request.url.path == '/robots.txt':
                return httpx.Response(200, text='User-agent: *\nAllow: /')
            if request.url.host == 'example.no' and request.url.path == route:
                return httpx.Response(200, text=body)
            if request.url.host == 'other.no' and request.url.path == '/':
                return httpx.Response(200, text=html('Org.nr ' + OTHER, title='Other AS'))
        if request.url.path == '/robots.txt':
            return httpx.Response(200, text='User-agent: *\nDisallow: /')
        return httpx.Response(404)

    with respx.mock(assert_all_called=False) as router:
        router.route().mock(side_effect=serve)
        assert cli.main() == 0

    report = json.loads(Path('report.json').read_text(encoding='utf8'))
    row = json.loads(Path('envelopes.jsonl').read_text(encoding='utf8').split('\n')[0])
    with Path('profiles.jsonl').open(encoding='utf8') as profiles:
        assert [json.loads(line)['organisation_number'] for line in profiles] == [OUR, OTHER]
    # This response needs the same fallback as the oversized 500-run page.
    assert len(site.profile(row, 'Signalpost', 0, official_inline=0).encode('utf8')) >= 250_000
    assert report['site']['state'] == 'available'
    expected_size = Path(f'site/c/{OUR}.html').stat().st_size
    assert report['site']['largest_profile_bytes'] == expected_size <= site.PROFILE_HTML_BUDGET
    assert expected_size < site.PROFILE_HTML_REGRESSION_LIMIT
    checked = check('envelopes.jsonl', batch, 'state', 'report.json', 'site', 2)
    assert checked['site_verified'] and checked['largest_profile_bytes'] == expected_size
    payload = Path(f'site/c/{OUR}.data.js').read_text(encoding='utf8')
    assert all(address in payload for address in addresses)
    assert source_url in payload
