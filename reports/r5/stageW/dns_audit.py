"""One public-resolver query per unique non-NXDOMAIN candidate; diagnostic only."""
import asyncio
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import httpx

DEST = Path(__file__).resolve().parent


async def main():
    source = json.loads((DEST / 'rejections.json').read_text(encoding='utf8'))
    names = sorted({r['host'] for r in source['dns_records'] if r['recorded_reason'] != 'no_such_domain' and r['host']})
    results = []
    async with httpx.AsyncClient(timeout=8, trust_env=False, follow_redirects=False, headers={'User-Agent': 'Signalpost/1.3.0 (one-off DNS audit)'}) as client:
        # API use, not HTML crawling; fixed official resolver origin, DNSSEC enabled,
        # zero ECS disclosure. Never fetch an address returned by this diagnostic.
        for name in names:
            entry = {'host': name, 'retrieved_at': datetime.now(timezone.utc).isoformat()}
            try:
                response = await client.get('https://dns.google/resolve', params={'name': name.encode('idna').decode(), 'type': 'A', 'edns_client_subnet': '0.0.0.0/0'})
                entry.update(url=str(response.url), http_status=response.status_code, body=response.text,
                             content_sha256=hashlib.sha256(response.content).hexdigest())
                response.raise_for_status()
                data = response.json()
                status = data.get('Status')
                entry['rcode'] = status
                entry['state'] = 'exists_A' if status == 0 and any(a.get('type') == 1 for a in data.get('Answer', [])) else 'NOERROR_no_A' if status == 0 else 'NXDOMAIN' if status == 3 else 'SERVFAIL' if status == 2 else 'other_rcode'
            except httpx.TimeoutException:
                entry['state'] = 'timeout'
            except (httpx.HTTPError, ValueError, UnicodeError) as exc:
                entry.update(state='request_failed', error=type(exc).__name__)
            results.append(entry)
            # Persist after each once-only query; restarting must not repeat it.
            output = {'provider': 'Google Public DNS', 'documentation': 'https://developers.google.com/speed/public-dns/docs/doh/json',
                      'terms': 'https://developers.google.com/speed/public-dns/terms', 'privacy': 'https://developers.google.com/speed/public-dns/privacy',
                      'input_audit_sha256': hashlib.sha256((DEST / 'rejections.json').read_bytes()).hexdigest(),
                      'unique_names': len(names), 'completed': len(results), 'http_requests': len(results), 'cost_usd': 0,
                      'counts': dict(Counter(r['state'] for r in results)), 'results': results,
                      'limits': 'A query only: NOERROR without A does not prove nonexistence. Generic historical errors include nomination cutoffs. Diagnostic results never publish identity claims.'}
            (DEST / 'dns_recheck.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
            await asyncio.sleep(.3)
    print(json.dumps(output['counts']))


if __name__ == '__main__':
    if (DEST / 'dns_recheck.json').exists():
        raise SystemExit('Refusing to repeat queries: existing once-only results retained.')
    asyncio.run(main())
