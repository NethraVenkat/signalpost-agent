"""Count actual attempts separately from logical DNS nominations."""
import json
from collections import Counter
from pathlib import Path

root = Path('reports/r5/stage4_7')
result = {}
for step in ('budget', 'caps', 'order', 'singlehost', 'social'):
    folder = root / ('step'+step)
    if not (folder/'verification.json').exists(): continue
    report = json.loads((folder/'report.json').read_text())
    cfg = json.loads((folder/'settings.json').read_text())['resolved_config']
    companies = {r['organisation_number'] for r in json.loads((folder/'counts.json').read_text())['per_company']}
    website = Counter(e['organisation_number'] for e in report['request_log'] if e.get('section') == 'website')
    all_calls = Counter(e['organisation_number'] for e in report['request_log'])
    nominations = report['dns_candidates_by_company']
    maximum_website = max((website[o] for o in companies), default=0)
    maximum_total = max((all_calls[o] for o in companies), default=0)
    maximum_nominations = max(nominations.values(), default=0)
    assert maximum_website <= 8 and maximum_total <= 13 and maximum_nominations <= 8
    result[step] = dict(configured_website_cap=cfg['website_request_cap'], configured_total_cap=cfg['website_total_request_cap'],
        website_http_attempts=sum(website.values()), max_website_http_attempts=maximum_website,
        max_company_http_attempts=maximum_total, max_dns_nominations=maximum_nominations,
        dns_precheck_lookups=report['dns_precheck_lookups'],
        per_company={o:dict(website_http_attempts=website[o], all_http_attempts=all_calls[o],
                            dns_nominations=nominations.get(o,0)) for o in sorted(companies)})
(root/'resource_audit.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf8')
print(json.dumps({s:{k:v for k,v in values.items() if k!='per_company'} for s,values in result.items()}))
