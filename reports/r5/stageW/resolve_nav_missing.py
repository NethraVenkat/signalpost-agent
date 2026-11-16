"""Bounded exact-identifier follow-up for NAV IDs absent from batch search."""
from signalpost.portable_paths import expand, portable, portable_text  # saved paths stay repo-relative
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
from signalpost.web.policy import safe_transport
from signalpost.budget import SourceFailure


async def main():
    path = DEST / 'nav_parent_join.json'; original = path.read_bytes(); result = json.loads(original)
    backup = DEST / 'nav_parent_initial_join.json'
    if not backup.exists():backup.write_bytes(original)
    before_tombstones = DEST / 'nav_parent_before_tombstone_handling.json'
    if not before_tombstones.exists():before_tombstones.write_bytes(original)
    directory = ROOT / '.data/r5/stageW/nav-parent-direct'; directory.mkdir(parents=True, exist_ok=True)
    relations = {r['employer_orgnr']: r for r in result['relationships']}; mains = result.get('confirmed_main_employers', []); unresolved = []; deleted = []
    cache = {r['url']: r for r in result['receipts'] if r.get('kind', '').startswith('direct_') and r.get('content_sha256')}
    started = time.monotonic(); stopped = False
    async with httpx.AsyncClient(transport=safe_transport(1), trust_env=False, follow_redirects=False, timeout=8,
                                headers={'Accept': 'application/json', 'User-Agent': 'SignalpostAgent/1.0'}) as client:
        for org in result['missing_employers']:
            resolved = False
            for kind in ('underenheter', 'enheter'):
                url = f'https://data.brreg.no/enhetsregisteret/api/{kind}/{org}'
                cached = cache.get(url)
                if not cached and (len(result['receipts']) >= 40 or result['runtime_seconds'] + time.monotonic() - started >= 300):
                    stopped = True; break
                receipt = {'kind': 'direct_' + kind, 'requested_orgnrs': [org], 'requested_at': datetime.now(timezone.utc).isoformat(), 'url': url}
                try:
                    if cached:
                        receipt = dict(cached); raw = Path(expand(receipt['body_path'])).read_bytes(); sha = hashlib.sha256(raw).hexdigest()
                        assert sha == receipt['content_sha256']; status = receipt['status']
                    else:
                        async with client.stream('GET', url) as response:
                            body = bytearray()
                            async for chunk in response.aiter_bytes():
                                body.extend(chunk)
                                if len(body) > 4_000_000:raise ValueError('response_size_limit')
                            raw = bytes(body); sha = hashlib.sha256(raw).hexdigest(); (directory / sha).write_bytes(raw)
                            receipt.update(status=response.status_code, headers=dict(response.headers), content_sha256=sha,
                                           body_path=str(directory / sha), retrieved_at=datetime.now(timezone.utc).isoformat(), bytes=len(raw))
                            status = response.status_code
                            if status != 404:response.raise_for_status()
                    if status == 200:
                        entity = json.loads(raw); assert entity.get('organisasjonsnummer') == org
                        text = raw.decode('utf8'); org_clip = re.search(r'"organisasjonsnummer"\s*:\s*"' + org + '"', text); assert org_clip
                        if kind == 'underenheter':
                            parent = str(entity.get('overordnetEnhet') or '')
                            if not parent and entity.get('respons_klasse') == 'SlettetUnderEnhet' and entity.get('slettedato'):
                                deleted.append({'employer_orgnr': org, 'content_sha256': sha, 'locator': '/organisasjonsnummer',
                                    'exact_excerpt': org_clip.group(), 'registry_deleted_at': entity['slettedato'],
                                    'response_class': entity['respons_klasse'], 'parent_state': 'not_returned; no name-based inference'})
                            else:
                                assert valid(parent)
                                parent_clip = re.search(r'"overordnetEnhet"\s*:\s*"' + parent + '"', text); assert parent_clip
                                relations[org] = {'employer_orgnr': org, 'parent_orgnr': parent, 'content_sha256': sha,
                                    'employer_locator': '/organisasjonsnummer', 'parent_locator': '/overordnetEnhet',
                                    'employer_exact_excerpt': org_clip.group(), 'parent_exact_excerpt': parent_clip.group(),
                                    'registry_deleted_at': entity.get('slettedato'), 'method': 'Direct exact subunit record after absent search result; deletion state retained.'}
                        else:
                            assert (entity.get('organisasjonsform') or {}).get('kode') not in {'BEDR', 'AAFY'}
                            mains.append({'employer_orgnr': org, 'content_sha256': sha, 'locator': '/organisasjonsnummer',
                                          'exact_excerpt': org_clip.group(), 'registry_deleted_at': entity.get('slettedato'),
                                          'method': 'Exact main-entity endpoint record, not a physical-subunit parent inference.'})
                        resolved = True
                    elif status == 404:
                        receipt['outcome'] = 'not_found'
                except (httpx.HTTPError, SourceFailure, ValueError, AssertionError) as exc:
                    receipt['error'] = str(exc); stopped = True
                    result['failures'].append({'reason': 'direct_lookup_failure', 'orgnr': org, 'error': str(exc)})
                if not cached:result['receipts'].append(receipt)
                (DEST / 'nav_parent_direct_progress.json').write_text(portable_text(json.dumps({'receipts': result['receipts'], 'relations': list(relations.values()),
                    'confirmed_main_employers': mains, 'unresolved': unresolved}, ensure_ascii=False, indent=2) + '\n'), encoding='utf8', newline='\n')
                if not cached:await asyncio.sleep(5)
                if resolved or stopped:
                    break
            if not resolved:unresolved.append(org)
            if stopped:
                unresolved.extend(o for o in result['missing_employers'] if o not in relations and o not in {m['employer_orgnr'] for m in mains})
                break
    with gzip.open(DOWNLOADS / 'universe.jsonl.gz', 'rt', encoding='utf8') as f:
        universe = {json.loads(line)['organisation_number'] for line in f}
    employers = {a['employer_orgnr'] for a in json.loads(gzip.decompress((ROOT / 'src/signalpost/data/nav_index.json.gz').read_bytes()))['ads']}
    parents = {r['parent_orgnr'] for r in relations.values()}; represented = (parents | employers) & universe
    classified = set(relations) | {m['employer_orgnr'] for m in mains} | {d['employer_orgnr'] for d in deleted}
    tombstone_ids = {d['employer_orgnr'] for d in deleted}
    old_schema_failures = [f for f in result['failures'] if f.get('reason') == 'direct_lookup_failure' and f.get('orgnr') in tombstone_ids and f.get('error') == '']
    result['resolved_tombstone_schema_errors'] = old_schema_failures
    result['failures'] = [f for f in result['failures'] if f not in old_schema_failures]
    unresolved.extend(tombstone_ids)
    result.update(relationships=sorted(relations.values(), key=lambda r: r['employer_orgnr']), confirmed_main_employers=mains,
                  mapped_employers=len(relations), classified_employers=len(classified), distinct_parents=len(parents),
                  deleted_unmapped_employers=deleted, complete_employer_classification=classified == employers,
                  unique_index_companies_in_universe=len(represented), missing_employers=sorted(set(unresolved)),
                  complete=set(relations) | {m['employer_orgnr'] for m in mains} == employers and not result['failures'], http_requests=len(result['receipts']),
                  runtime_seconds=result['runtime_seconds'] + time.monotonic() - started,
                  runtime_scope='Sum of active audit tool wall times, excluding operator interval; original and follow-up UTC receipts retained.')
    result['expected_rate_per_1000'] = len(represented) / len(universe) * 1000 if result['complete'] else None
    result['confirmed_rate_lower_bound_per_1000'] = len(represented) / len(universe) * 1000
    result['possible_rate_upper_bound_per_1000'] = (len(represented) + len(result['missing_employers'])) / len(universe) * 1000
    path.write_text(portable_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n'), encoding='utf8', newline='\n')
    print(json.dumps({k: result[k] for k in ('complete', 'mapped_employers', 'classified_employers', 'unique_index_companies_in_universe', 'expected_rate_per_1000', 'missing_employers', 'http_requests', 'runtime_seconds')}))


if __name__ == '__main__':
    asyncio.run(main())
