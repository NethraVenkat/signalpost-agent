import json
from pathlib import Path
import httpx
import pytest
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


@pytest.mark.parametrize('mutation',['missing_site','missing_profile','order','schema','unsupported_value','bad_blob'])
def test_live_gate_rejects_broken_artifacts(tmp_path,mutation):
    cfg,rows=fixture(tmp_path)
    if mutation=='missing_site':(cfg.site_dir/'index.html').unlink()
    elif mutation=='missing_profile':(cfg.site_dir/'c/923609016.html').unlink()
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
    assert '--require-clean' not in source and '--time-budget-seconds' not in run
    assert 'timeout-minutes: 10' in source and 'actions/upload-artifact@v4' in source and 'if: always()' in source


def test_large_profile_defers_only_duplicate_explorer_rows_under_same_gate(tmp_path,monkeypatch):
    from signalpost import site
    cfg,rows=fixture(tmp_path)
    original=site.profile
    # Model a large fact body just under the gate without its duplicate audit
    # table. Vary only that existing table's initial row count.
    def large(row,title,explorer_rows=site.EXPLORER_VISIBLE_ROWS):
        rendered=original(row,title,explorer_rows)
        return rendered+' '*(210000)+(' '*(explorer_rows*600))
    monkeypatch.setattr(site,'profile',large)
    before=cfg.output.read_bytes()
    metrics=site.generate_site(cfg.output,tmp_path/'deferred')
    assert metrics['largest_profile_bytes']<250000
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
