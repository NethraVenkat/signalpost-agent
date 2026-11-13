"""Reports-only exact-ID NAV parent join using the approved official REST API."""
import asyncio
import gzip
import hashlib
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
import httpx
from audit import ROOT, DEST, DOWNLOADS
from signalpost.identity.orgnr import valid
from signalpost.budget import SourceFailure
from signalpost.web.policy import safe_transport

URL = 'https://data.brreg.no/enhetsregisteret/api/underenheter'
DOCS = 'https://data.brreg.no/enhetsregisteret/api/dokumentasjon/no/index.html'


async def main():
    storage = ROOT / '.data/r5/stageW/nav-parent-responses'
    storage.mkdir(parents=True, exist_ok=False)
    index_path = ROOT / 'src/signalpost/data/nav_index.json.gz'
    index = json.loads(gzip.decompress(index_path.read_bytes()))
    employers = sorted({a['employer_orgnr'] for a in index['ads']})
    assert len(employers) == 6012 and all(valid(org) for org in employers)
    with gzip.open(DOWNLOADS / 'universe.jsonl.gz', 'rt', encoding='utf8') as f:
        universe = {json.loads(line)['organisation_number'] for line in f}
    receipts, relations, missing, failures = [], {}, [], []
    started = time.monotonic()
    async with httpx.AsyncClient(transport=safe_transport(1), trust_env=False, follow_redirects=False,
                                timeout=httpx.Timeout(8, connect=4), headers={'Accept': 'application/json', 'User-Agent': 'SignalpostAgent/1.0'}) as client:
        for offset in range(0, len(employers), 200):
            if time.monotonic() - started >= 300 or len(receipts) >= 40:
                failures.append({'reason': 'audit_budget_stop', 'unstarted_employers': employers[offset:]})
                break
            batch = employers[offset:offset + 200]
            receipt = {'batch': offset // 200, 'requested_orgnrs': batch, 'requested_at': datetime.now(timezone.utc).isoformat()}
            try:
                # Documented <=2000 exact IDs; 200 avoids long URLs. One page
                # can hold the entire bounded batch. No name search or crawl.
                async with client.stream('GET', URL, params={'organisasjonsnummer': ','.join(batch), 'size': '1000', 'page': '0'}) as response:
                    body = bytearray()
                    async for chunk in response.aiter_bytes():
                        body.extend(chunk)
                        if len(body) > 4_000_000:
                            raise ValueError('response_size_limit')
                    raw = bytes(body); digest = hashlib.sha256(raw).hexdigest()
                    (storage / digest).write_bytes(raw)
                    receipt.update(url=str(response.url), status=response.status_code, headers=dict(response.headers),
                                   content_sha256=digest, body_path=str(storage / digest), bytes=len(raw),
                                   retrieved_at=datetime.now(timezone.utc).isoformat())
                    response.raise_for_status()
                data = json.loads(raw)
                entries = data.get('_embedded', {}).get('underenheter', [])
                assert isinstance(entries, list) and len(entries) <= len(batch), 'Unexpected result scope'
                assert data.get('page', {}).get('totalPages', 0) <= 1, 'Unexpected pagination; do not fabricate complete coverage'
                seen = set()
                for position, entity in enumerate(entries):
                    org = str(entity.get('organisasjonsnummer') or '')
                    parent = str(entity.get('overordnetEnhet') or '')
                    assert org in batch and org not in seen and valid(org) and valid(parent), 'Wrong/duplicate/missing exact IDs'
                    seen.add(org)
                    # Separate exact field clips plus JSON pointers establish
                    # the record pairing; full raw response stays hash-checked.
                    text = raw.decode('utf8')
                    org_clip = re.search(r'"organisasjonsnummer"\s*:\s*"' + org + '"', text)
                    parent_clip = re.search(r'"overordnetEnhet"\s*:\s*"' + parent + '"', text)
                    assert org_clip and parent_clip
                    relations[org] = {'employer_orgnr': org, 'parent_orgnr': parent, 'content_sha256': digest,
                                      'employer_locator': f'/_embedded/underenheter/{position}/organisasjonsnummer',
                                      'parent_locator': f'/_embedded/underenheter/{position}/overordnetEnhet',
                                      'employer_exact_excerpt': org_clip.group(), 'parent_exact_excerpt': parent_clip.group()}
                missing.extend(sorted(set(batch) - seen))
                receipt['returned_exact_records'] = len(seen)
            except (httpx.HTTPError, SourceFailure, ValueError, AssertionError) as exc:
                receipt['error'] = str(exc)
                failures.append({'batch': offset // 200, 'reason': type(exc).__name__, 'error': str(exc), 'orgnrs': batch})
            receipts.append(receipt)
            (DEST / 'nav_parent_progress.json').write_text(json.dumps({'state': 'running', 'http_requests': len(receipts),
                'mapped_employers': len(relations), 'receipts': receipts, 'relationships': list(relations.values()),
                'missing_employers': missing, 'failures': failures}, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
            # Respect access stops; no alternate host/path/credentials or retries.
            if receipt.get('error'):
                failures.append({'reason': 'source_access_stop', 'unstarted_employers': employers[offset + 200:]})
                break
            await asyncio.sleep(5)
    parents = {r['parent_orgnr'] for r in relations.values()}
    represented = (set(employers) | parents) & universe
    complete = len(relations) == len(employers) and not failures and not missing
    measured = json.loads((DEST / 'rejections.json').read_text(encoding='utf8'))['jobs']
    result = {'method': 'Documented exact-orgnr array REST lookup, current official overordnetEnhet, exact universe membership; never a name join.',
              'api_policy': 'Existing approved official registry REST source policy, NLOD 2.0. The failed optional bulk-download robots preflight is not used as an API permission test. No webpage crawl or refusal bypass.',
              'documentation': DOCS, 'attribution': 'Brønnøysundregistrene / Enhetsregisteret; NLOD 2.0',
              'index_sha256': hashlib.sha256(index_path.read_bytes()).hexdigest(), 'index_built_at': index['built_at'],
              'universe_archive_sha256': hashlib.sha256((DOWNLOADS / 'universe.jsonl.gz').read_bytes()).hexdigest(),
              'universe_count': len(universe), 'indexed_employers': len(employers), 'mapped_employers': len(relations),
              'distinct_parents': len(parents), 'direct_employers_in_universe': len(set(employers) & universe),
              'unique_index_companies_in_universe': len(represented), 'expected_rate_per_1000': len(represented) / len(universe) * 1000 if complete else None,
              'confirmed_rate_lower_bound_per_1000': len(represented) / len(universe) * 1000,
              'measured_rate_per_1000': measured['measured_per_1000'], 'measured_job_companies': measured['measured_job_companies'], 'measured_inputs': measured['measured_inputs'],
              'complete': complete, 'missing_employers': sorted(set(missing)), 'failures': failures,
              'http_requests': len(receipts), 'maximum_requests': 40, 'runtime_seconds': time.monotonic() - started, 'cost_usd': 0,
              'receipt_directory': str(storage), 'receipts': receipts, 'relationships': sorted(relations.values(), key=lambda r: r['employer_orgnr']),
              'limits': 'Index-based expected discovery coverage, not live-current job proof. Index and parent retrieval dates differ. Runtime profiles and rarity bundle are not modified; this is not a nationwide subunit snapshot.'}
    (DEST / 'nav_parent_join.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps({k: v for k, v in result.items() if k not in {'receipts', 'relationships'}}))


if __name__ == '__main__':
    asyncio.run(main())
