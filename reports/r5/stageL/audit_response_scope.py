"""Clarify L0 scan denominator without changing links, source bytes or proof rules."""
import json,re,hashlib
from pathlib import Path
from urllib.parse import urlsplit
from collections import Counter
ROOT=Path(__file__).resolve().parents[3]
def main():
    samples=[]
    for seed in (20261017,20261113,20261114,20261115,20261116,20261117):
        base=ROOT/f'reports/r5/stageR7/R7/seed{seed}';work=Path(json.loads((base/'settings.json').read_text(encoding='utf8'))['working_directory'])
        rows={r['organisation_number']:r for r in map(json.loads,(work/'envelopes.jsonl').read_text(encoding='utf8').splitlines())}
        all_orgs=set();html_orgs=set();seen=set();types=Counter()
        for e in json.loads((base/'report.json').read_text(encoding='utf8'))['request_log']:
            org=e['organisation_number'];r=rows.get(org)
            if not r or e.get('section')!='website' or e.get('status')!=200 or not e.get('content_sha256'):continue
            if any(c['field']=='official_website' and c['availability']=='available' for c in r['claims']):continue
            key=(org,e['url'],e['content_sha256'])
            if key in seen:continue
            seen.add(key);all_orgs.add(org);body=(work/'state/blobs'/e['content_sha256']).read_bytes();assert hashlib.sha256(body).hexdigest()==e['content_sha256']
            path=urlsplit(e['url']).path.casefold().rstrip('/')
            kind='robots' if path=='/robots.txt' else 'sitemap_xml' if re.search(br'<(?:[a-zA-Z]+:)?(?:urlset|sitemapindex)\b',body[:1500],re.I) else 'pdf' if body.startswith(b'%PDF-') else 'html_site_page' if re.search(br'<(?:html|head|body|title|header|footer|main|div|section)\b',body[:10000],re.I) else 'other_response'
            types[kind]+=1
            if kind=='html_site_page':html_orgs.add(org)
        samples.append({'seed':seed,'successful_website_section_companies':len(all_orgs),'html_site_companies':len(html_orgs),'without_html_site_page':len(all_orgs-html_orgs),'unique_successful_responses':len(seen),'response_types':dict(types)})
    result={'network_requests':0,'scope':'Same six saved R7 inputs/hashes as L0. Website-section HTTP200 includes robots; HTML site-page definition excludes robots/sitemap/PDF and requires HTML document/structural tags in the first10kbytes. This clarifies denominators; original exact link receipts remain unchanged.','samples':samples,'totals':{k:sum(r[k] for r in samples) for k in ('successful_website_section_companies','html_site_companies','without_html_site_page','unique_successful_responses')}}
    (ROOT/'reports/r5/stageL/response_scope.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(result['totals']))
if __name__=='__main__':main()
