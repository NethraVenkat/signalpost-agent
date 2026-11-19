import asyncio
import errno
from pathlib import Path
import time
from types import SimpleNamespace

import pytest

from signalpost.models.claim import Claim
from signalpost.portable_paths import HOME_PATH_PATTERNS
from signalpost.runner import placeholder, update
from signalpost.sources.extract import Section
from signalpost.web import adaptive
from signalpost.web.candidates import Candidate

BAD = '890136532'  # Final incomplete request in the saved 500 run.
GOOD = '923609016'
NOW = '2026-11-19T00:00:00Z'


@pytest.mark.parametrize('failure_phase', ['nomination', 'discovery', 'public_activity'])
def test_one_company_io_failure_preserves_metrics_and_other_companies(monkeypatch, failure_phase):
    envelopes = {org: placeholder(org, 'io-isolation', NOW, ('website', 'activity')) for org in (BAD, GOOD)}
    start = time.monotonic()
    budget = SimpleNamespace(start=start, deadline=start+30, website_deadline=start+30,
                             pass2_cutoff=start+30, cap=100, events=[], phase='pass1', check_website=lambda: None)
    cfg = SimpleNamespace(adaptive_extra_budget=False, dns_precheck=False, public_activity=failure_phase=='public_activity', hiring=False)
    sessions = {org: {'context': {'org': org}, 'attempted': set(), 'vetoed': set()} for org in envelopes}
    http = SimpleNamespace(budget=budget, config=cfg, discovery_sessions=sessions, blobs=None,
                            counts={}, company_cap=lambda org: 8, legal_resumable={})
    private = Path('C:/') / 'Users' / 'example-user' / 'private'
    def fail():
        raise OSError(errno.EIO, str(private))  # Injected cause, not an inferred historical errno.
    def nominations(envelope, index, blobs):
        if envelope.organisation_number == BAD and failure_phase == 'nomination': fail()
        return []
    monkeypatch.setattr(adaptive, 'nav_homepages', nominations)
    monkeypatch.setattr(adaptive, 'priority', lambda c: 0)
    monkeypatch.setattr(adaptive, 'generate', lambda context, limit: [
        Candidate('https://goldencolombia.org/kjopsbetingelser' if context['org']==BAD else 'https://example.no/',
                  'goldencolombia.org' if context['org']==BAD else 'example.no', 'registry_website')])
    called = []
    async def collect(org, *args, **kwargs):
        called.append(org)
        budget.events.append({'organisation_number': org, 'pass': 'pass2', 'section': 'website', 'status': 404, 'error': None})
        if org == BAD and failure_phase == 'discovery': fail()
        if org == BAD and failure_phase == 'public_activity':
            proof = Claim(id='proof', field='official_website', family='website', value={'identity_level':'VERIFIED'},
                          availability='available', evidence_ids=['receipt'], first_observed_at=NOW, last_observed_at=NOW)
            return Section(claims=[proof])
        return Section(state='not_available')
    monkeypatch.setattr(adaptive.collector, 'fetch', collect)
    async def refresh(org, envelope):
        if org == BAD: fail()
    result = asyncio.run(adaptive.run(envelopes, http, None, {}, {}, update, refresh))
    assert result['state'] == 'completed_with_errors' and result['company_errors'] == 1
    bad = result['pass2']['per_company'][BAD]
    assert bad['state'] == 'failed' and bad['error']['errno'] == errno.EIO
    assert bad['error']['phase'] == failure_phase and bad['error']['traceback']
    assert not any(p.search(bad['error']['message'] + bad['error']['traceback']) for p in HOME_PATH_PATTERNS)
    family = 'activity' if failure_phase == 'public_activity' else 'website'
    assert envelopes[BAD].run.sections[family] == 'failed'
    assert any(e.code == 'adaptive_os_error' and e.section == family for e in envelopes[BAD].errors)
    assert GOOD in called and result['pass2']['per_company'][GOOD]['state'] == 'checked_no_gain'
    assert result['pass2']['requests'] == len(budget.events)
    assert budget.phase == 'pass1'
    if failure_phase == 'public_activity':
        assert adaptive.exact(envelopes[BAD]) and envelopes[BAD].run.sections['website'] == 'available'


def test_response_receipt_storage_failure_is_company_local_and_keeps_request_diagnostics(tmp_path, monkeypatch):
    from signalpost.sources.blobstore import BlobStore
    from tests.test_r5_stage_a import exercise, OUR
    original = BlobStore.put
    def put(self, body):
        if b'linkedin.com/company/90123/' in body:
            raise OSError(errno.EIO, 'injected response receipt write failure')
        return original(self, body)
    monkeypatch.setattr(BlobStore, 'put', put)
    report, row, _, _ = exercise(tmp_path, monkeypatch)
    metrics = report['adaptive_websites']
    assert metrics['state'] == 'completed_with_errors' and metrics['company_errors'] == 1
    error = metrics['pass2']['per_company'][OUR]['error']
    assert error['phase'] == 'discovery' and error['errno'] == errno.EIO
    failed = [e for e in report['request_log'] if e.get('pass') == 'pass2' and e.get('error') == 'OSError']
    assert failed and failed[-1]['runtime_ms'] >= 0
    assert failed[-1]['os_error']['phase'] == 'receipt_storage'
    assert not failed[-1].get('content_sha256')
    assert row['run']['sections']['website'] == 'failed'
    assert any(e['code'] == 'adaptive_os_error' for e in row['errors'])
    assert any('company I/O failures' in warning for warning in report['warnings'])
