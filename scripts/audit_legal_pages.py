"""Offline legal-page and builder audit over accepted six-sample receipts."""
from signalpost.portable_paths import expand, portable, portable_text  # saved paths stay repo-relative
import hashlib,json,re,sys
from pathlib import Path
from collections import Counter
from urllib.parse import urlsplit,unquote
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from signalpost.web.html import Page
from signalpost.web.policy import domain

ROOT=Path.cwd()
SEEDS=(20261017,20261113,20261114,20261115,20261116,20261117)
LEGAL=re.compile(r'salgsbetingelser|kj.psbetingelser|kj.psvilk.r|handelsbetingelser|vilk.r|betingelser|personvern|personvernerkl.ring|cookies|angrerett|impressum|juridisk|om[-_ ]nettstedet|terms|privacy|conditions',re.I)
BUILDERS={'wix':r'wixBiSession|warmupData|viewerModel|wix-warmup-data','squarespace':r'SQUARESPACE_CONTEXT|Static\.SQUARESPACE_CONTEXT','next':r'__NEXT_DATA__','nuxt':r'__NUXT__|__NUXT_DATA__'}

def main():
    stage=sys.argv[1] if len(sys.argv)>1 else 'R7'
    dest=ROOT/'reports/r5/stageL';dest.mkdir(exist_ok=True)
    records=[];counts=Counter();seen=set();provenance=[]
    for seed in SEEDS:
        path=ROOT/f'reports/r5/stage{stage}/{stage}/seed{seed}'
        settings=json.loads((path/'settings.json').read_text(encoding='utf8'));work=Path(expand(settings['working_directory']))
        rows={r['organisation_number']:r for r in map(json.loads,(work/'envelopes.jsonl').read_text(encoding='utf8').splitlines())}
        report=json.loads((work/'report.json').read_text(encoding='utf8'))
        provenance.append({'seed':seed,'work':str(work),'envelopes_sha256':hashlib.sha256((work/'envelopes.jsonl').read_bytes()).hexdigest()})
        matched_companies=set();legal_companies=set();pdf_companies=set()
        for e in report['request_log']:
            org=e['organisation_number'];row=rows.get(org)
            if not row or e.get('section')!='website' or e.get('status')!=200 or not e.get('content_sha256'):continue
            if any(c['field']=='official_website' and c['availability']=='available' for c in row['claims']):continue
            key=(seed,org,e['url'],e['content_sha256'])
            if key in seen:continue
            seen.add(key);body=(work/'state/blobs'/e['content_sha256']).read_bytes()
            page=Page(body,e['url']);matched_companies.add(org)
            links=[]
            for link in page.links:
                if domain(link.href)!=domain(page.url) or not LEGAL.search(unquote(urlsplit(link.href).path)+' '+link.text):continue
                footer_nav=link.owned_context
                from_legal=bool(LEGAL.search(unquote(urlsplit(page.url).path)))
                if not (footer_nav or from_legal):continue
                pdf=bool(re.search(r'\.pdf$',urlsplit(link.href).path,re.I))
                links.append({'url':link.href,'text':link.text,'exact_anchor':link.span,'pdf':pdf,'footer_nav':footer_nav,'from_legal_page':from_legal})
                (pdf_companies if pdf else legal_companies).add(org)
                counts['linked_pdf_terms' if pdf else 'linked_legal_html']+=1
            sitemap=[]
            if re.search(r'<(?:\w+:)?(?:urlset|sitemapindex)\b',page.raw):
                import xml.etree.ElementTree as ET
                if not re.search(r'<!\s*(?:DOCTYPE|ENTITY)',page.raw,re.I):
                    try:
                        xml=ET.fromstring(page.raw)
                        sitemap=[n.text.strip() for n in xml.iter() if n.tag.rsplit('}',1)[-1]=='loc' and n.text and LEGAL.search(unquote(n.text)) and domain(n.text)==domain(page.url)]
                    except ET.ParseError:pass
            builders=[]
            pattern=re.compile(r'(?<!\d)'+r'[\s.]*'.join(org)+r'(?!\d)')
            for script in re.finditer(r'<script\b[^>]*>.*?</script\s*>',page.raw,re.I|re.S):
                for builder,marker in BUILDERS.items():
                    if re.search(marker,script.group(),re.I) and pattern.search(script.group()):
                        builders.append({'builder':builder,'exact_target_orgnr':org,'script_sha256':hashlib.sha256(script.group().encode()).hexdigest()});counts['builder_'+builder]+=1
            if links or sitemap or builders:records.append({'seed':seed,'orgnr':org,'name':next(c['value'] for c in row['claims'] if c['field']=='identity.legal_name' and c['availability']=='available'),'page':page.url,'page_sha256':e['content_sha256'],'links':links,'sitemap':sitemap,'builder_orgnr_patterns':builders})
        counts['fetched_without_proof_companies']+=len(matched_companies);counts['companies_with_legal_html_links']+=len(legal_companies);counts['companies_with_pdf_links']+=len(pdf_companies)
    for key in ('builder_wix','builder_squarespace','builder_next','builder_nuxt'):counts.setdefault(key,0)
    counts['sitemap_legal_entries']=sum(len(r['sitemap']) for r in records)
    counts['unique_legal_html_targets']=len({(r['seed'],r['orgnr'],l['url']) for r in records for l in r['links'] if not l['pdf']})
    counts['unique_linked_pdf_targets']=len({(r['seed'],r['orgnr'],l['url']) for r in records for l in r['links'] if l['pdf']})
    doc={'network_requests':0,'method':'Saved accepted response bodies only; same-site publisher/footer/nav/legal links; builder marker plus exact target orgnr is an audit hit, not proof','counts':dict(counts),'sources':provenance,'items':records}
    (dest/'audit.json').write_text(portable_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n'),encoding='utf8')
    lines=['# L0 offline legal-disclosure audit','','Zero network requests. Audit hits nominate pages or builder inspection; they do not establish identity.','', '```json',json.dumps(dict(counts),indent=2),'```','']
    for r in records:lines += [f"## {r['seed']} / {r['orgnr']} / {r['name']}",'',r['page'],'','```json',json.dumps(r,ensure_ascii=False,indent=2),'```','']
    (dest/'audit.md').write_text(portable_text('\n'.join(lines)),encoding='utf8')
    print(json.dumps(dict(counts)))

if __name__=='__main__':main()
