import csv
import json

import httpx
import pytest

from signalpost.io.provenance import registry_provenance
from signalpost.sources import bulk_registry
from signalpost.sources.blobstore import BlobStore
from signalpost.budget import Budget
from tests.test_registry import config, execute, handler, numbers


def bulk_file(tmp_path, orgs):
    path = tmp_path / 'bulk.csv'
    with path.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.writer(stream, delimiter=';')
        writer.writerow(['organisasjonsnummer', 'navn'])
        writer.writerows((org, 'CSV Old Name') for org in orgs)
    return path


def test_bulk_thousand_rows_preserves_raw_evidence(tmp_path):
    orgs = numbers(1000)
    path = bulk_file(tmp_path, orgs)
    cfg = config(tmp_path, orgs)
    blobs = BlobStore(cfg.state_dir)
    rows, sha = bulk_registry.load(path, set(orgs), blobs, Budget(cfg))
    assert len(rows) == 1000
    assert len(sha) == 64
    for org, (row, source) in rows.items():
        assert row['navn'] == 'CSV Old Name'
        assert org.encode() in source.body
        assert (blobs.directory / source.sha).read_bytes() == source.body


@pytest.mark.parametrize('verify', [False, True])
def test_bulk_verification_and_attribution(tmp_path, verify):
    org = numbers(1)[0]
    cfg = config(tmp_path, [org], bulk=bulk_file(tmp_path, [org]), verify_bulk=verify)
    report, rows = execute(cfg)
    name = next(c for c in rows[0]['claims'] if c['field'] == 'identity.legal_name')
    assert (name['value'] == 'CSV Old Name') is (not verify)
    provenance = report['registry_provenance']
    record = next(c for c in provenance['claims'] if c['field'] == 'identity.legal_name')
    assert record['source_types'] == ['live_verified' if verify else 'csv_cache']
    assert provenance['requests_by_family'].get('identity', 0) == int(verify)
    assert provenance['requests_by_family']['roles'] == 1
    assert provenance['requests_by_family']['subunits'] == 1


@pytest.mark.parametrize('failure', [403, 404, 'wrong_company'])
def test_verification_failure_never_publishes_csv_or_prior_identity(tmp_path, failure):
    org = numbers(1)[0]
    cfg = config(tmp_path, [org], bulk=bulk_file(tmp_path, [org]))
    _, baseline = execute(cfg)
    previous = tmp_path / 'previous.jsonl'
    previous.write_text(json.dumps(baseline[0]) + '\n', encoding='utf-8')
    cfg.verify_bulk = True
    cfg.previous = previous
    original = handler()

    def response(request):
        if request.url.path == '/enhetsregisteret/api/enheter/' + org:
            if failure == 'wrong_company':
                return httpx.Response(200, json={'organisasjonsnummer': '999999999', 'navn': 'Wrong'})
            return httpx.Response(failure)
        return original(request)

    report, rows = execute(cfg, response)
    assert not any(c['family'] == 'identity' and c['availability'] == 'available' for c in rows[0]['claims'])
    assert not report['registry_provenance']['counts_by_source_type'].get('csv_cache')


def test_injected_transport_is_never_labelled_live(tmp_path):
    from signalpost.runner import placeholder, update
    from signalpost.sources.brreg_enhet import extract
    from signalpost.sources.extract import Source
    import hashlib

    org = numbers(1)[0]
    url = 'https://data.brreg.no/enhetsregisteret/api/enheter/' + org
    body = json.dumps({'organisasjonsnummer': org, 'navn': 'API Name'}).encode()
    sha = hashlib.sha256(body).hexdigest()
    envelope = placeholder(org, 'test', '2026-10-17T00:00:00Z')
    update(envelope, 'identity', extract(org, json.loads(body), Source(url, body, sha, envelope.started_at)))
    events = [{'url': url, 'status': 200, 'content_sha256': sha}]
    report = registry_provenance([envelope], events, injected_client=True)
    assert report['counts_by_source_type']['api_checked'] > 0
    assert 'live_verified' not in report['counts_by_source_type']
    events[0]['content_sha256'] = '0' * 64
    report = registry_provenance([envelope], events)
    assert 'live_verified' not in report['counts_by_source_type']
