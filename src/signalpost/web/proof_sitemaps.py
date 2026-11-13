"""Bounded same-site sitemaps nominate proof pages, never news or evidence."""
import re
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit,urljoin,unquote
from ..budget import SourceFailure
from ..workers import offload
from .policy import domain,normalize_url

PROOF=re.compile(r'(?:^|/)(?:kontakt(?:[-_]oss)?|om(?:[-_]oss)?|personvern(?:erklaering)?|impressum|about(?:[-_]us)?|contact(?:[-_]us)?|privacy)(?:[/_.-]|$)',re.I)
NEWS=re.compile(r'(?:^|/)(?:news|nyheter|aktuelt|presse|blog|blogg|artikler|posts?)(?:[/_.-]|$)',re.I)


def parse(body,source_url,homepage):
    raw=body.decode('utf8',errors='replace')
    if re.search(r'<!\s*(?:DOCTYPE|ENTITY)',raw,re.I):raise ValueError('XML declarations refused')
    root=ET.fromstring(raw);kind=root.tag.rsplit('}',1)[-1]
    if kind not in {'urlset','sitemapindex'}:return [],[]
    pages=[];children=[]
    for element in root.iter():
        if element.tag.rsplit('}',1)[-1]!='loc' or not element.text:continue
        raw_url=urljoin(source_url,element.text.strip())
        if urlsplit(raw_url).query:continue
        url=normalize_url(raw_url)
        if not url or domain(url)!=domain(homepage):continue
        path=unquote(urlsplit(url).path)
        if NEWS.search(path):continue
        if kind=='urlset' and PROOF.search(path) and not re.search(r'\.(?:pdf|xml|docx?|zip|jpe?g|png)$',path,re.I):pages.append(url)
        elif kind=='sitemapindex' and re.search(r'(?:page|kontakt|contact|about|privacy|personvern)',path,re.I):children.append(url)
    return list(dict.fromkeys(pages))[:2],list(dict.fromkeys(children))[:1]


async def discover(org,http,homepage,seen):
    metrics={'homepage':homepage,'maps':[],'targets':[],'state':'not_available'}
    http.proof_sitemap_attempts=getattr(http,'proof_sitemap_attempts',{})
    http.proof_sitemap_attempts.setdefault(org,[]).append(metrics)
    http.proof_sitemap_targets=getattr(http,'proof_sitemap_targets',{})
    nominated=http.proof_sitemap_targets.setdefault(org,set())
    if len(nominated)>=2:
        metrics.update(state='cut_off',reason='proof_sitemap_page_cap');return []
    declared=[]
    for origin,parser in http.robots.items():
        if urlsplit(origin).netloc==urlsplit(homepage).netloc:
            declared.extend(parser.site_maps() or [])
    maps=[]
    for value in declared or [urljoin(homepage,'/sitemap.xml')]:
        url=normalize_url(value)
        if url and domain(url)==domain(homepage) and not NEWS.search(urlsplit(url).path):maps.append(url)
    if not maps:return []
    url=maps[0]
    try:
        for depth in range(2):
            if url in seen:return []
            seen.add(url)
            response=await http.get(url,org,domain(homepage),xml=True)
            metrics['maps'].append({'url':response.url,'status':response.status})
            if response.status in {401,403,429}:raise SourceFailure('http_blocked')
            if response.status!=200:return []
            from .html import Page
            from .challenge import detected
            if detected(await offload(Page,response.body,response.url)):raise SourceFailure('block_page')
            pages,children=await offload(parse,response.body,response.url,homepage)
            targets=[page for page in pages if page not in seen]
            if targets:
                targets=targets[:2-len(nominated)];nominated.update(targets)
                metrics.update(state='nominated',targets=targets)
                return targets
            if depth or not children:return []
            url=children[0]
    except SourceFailure as exc:
        metrics.update(state='failed',reason=exc.code)
        if exc.code in {'website_budget_exhausted','budget_exhausted','deadline','robots','robots_unavailable','http_blocked','block_page'}:raise
    except (ValueError,ET.ParseError):metrics.update(state='failed',reason='malformed_proof_sitemap')
    return []
