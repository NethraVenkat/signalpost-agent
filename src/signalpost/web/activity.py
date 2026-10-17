"""Bounded dated news discovery on an already accepted company domain."""
from ..workers import offload

import html
import asyncio
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from urllib.parse import urljoin, urlsplit, unquote

from ..budget import SourceFailure
from ..models.evidence import digest
from ..sources.extract import Section, add, response_source, missing
from .policy import domain, normalize_url

NEWS = re.compile(r'(?:nyheter|news|aktuelt|presse|blogg|blog|artikler|artikkel|arkiv)', re.I)
NON_ITEM = re.compile(r'/(?:author|authors|forfatter|kirjoittaja|category|kategori|tag|tags|page|feed)(?:/|$)', re.I)


def local(tag):
    return tag.rsplit('}', 1)[-1].split(':')[-1]


def dated(value, now):
    try:
        try: date = datetime.fromisoformat(value.strip().replace('Z', '+00:00'))
        except ValueError: date = parsedate_to_datetime(value)
        if date.tzinfo is None: date = date.replace(tzinfo=timezone.utc)
        date = date.astimezone(timezone.utc)
        return date.date().isoformat() if datetime(2000, 1, 1, tzinfo=timezone.utc) <= date <= now + timedelta(days=2) else None
    except (ValueError, TypeError, OverflowError, AttributeError):
        return None


def parse(body, source_url, now):
    raw = body.decode('utf8', errors='replace')
    if re.search(r'<!\s*(?:DOCTYPE|ENTITY)', raw, re.I):
        raise ValueError('XML declarations refused')
    root = ET.fromstring(raw)
    kind = local(root.tag)
    if kind not in {'urlset', 'sitemapindex', 'rss', 'feed'}: raise ValueError('Unknown activity XML')
    items, children = [], []
    if kind == 'sitemapindex':
        for child in root:
            url = next((e.text for e in child if local(e.tag) == 'loc'), None)
            url = normalize_url(urljoin(source_url, url or '')) if url else None
            if url and domain(url) == domain(source_url): children.append(url)
        return [], sorted(set(children))
    tag = 'url' if kind == 'urlset' else 'item' if kind == 'rss' else 'entry'
    blocks = re.findall(r'<(?:[\w.-]+:)?' + tag + r'\b[^>]*>.*?</(?:[\w.-]+:)?' + tag + r'\s*>', raw, re.S)
    elements = [e for e in root.iter() if local(e.tag) == tag]
    # Unknown namespace/layout cannot invent a locator or snippet.
    if len(blocks) != len(elements): return [], []
    for n, (entry, block) in enumerate(zip(elements, blocks)):
        values = {local(e.tag): (e.text or '').strip() for e in entry}
        url = values.get('loc') if tag == 'url' else values.get('link')
        if tag == 'entry':
            url = next((e.get('href') for e in entry if local(e.tag) == 'link' and e.get('rel', 'alternate') == 'alternate'), None)
        url = normalize_url(urljoin(source_url, url or '')) if url else None
        if not url or domain(url) != domain(source_url) or not NEWS.search(urlsplit(url).path) or NON_ITEM.search(urlsplit(url).path): continue
        if re.fullmatch(r'/(?:[a-z]{2}/)?(?:nyheter|news|aktuelt|presse|blogg|blog|artikler|artikkel|arkiv)/?', urlsplit(url).path, re.I): continue
        field = next((f for f in ('lastmod', 'pubDate', 'published', 'updated') if values.get(f)), None)
        date = dated(values.get(field), now) if field else None
        if date is None: continue
        title = values.get('title')
        origin = 'feed title'
        if tag == 'url':
            title = re.sub(r'[-_]+', ' ', unquote(urlsplit(url).path.rstrip('/').rsplit('/', 1)[-1]))
            origin = 'title from URL'
        if not title or len(title) > 200: continue
        # Conservatively require one bounded verbatim span containing every
        # reported item token. Long or transformed values are abstentions.
        needles = [html.escape(url, quote=False), values[field]]
        if tag != 'url': needles.append(html.escape(title, quote=False))
        ranges = []
        for token in needles:
            position = block.find(token)
            if position < 0: break
            ranges.append((position, position + len(token)))
        if len(ranges) != len(needles): continue
        start, end = min(a for a, _ in ranges), max(b for _, b in ranges)
        if end-start > 300: continue
        span = block[start:end]
        items.append(({'title': title, 'title_source': origin, 'url': url, 'date': date,
                       'date_source': field, 'identity_level': None}, f'/{tag}/{n}', span))
    unique = {item[0]['url']: item for item in sorted(items, key=lambda x: (x[0]['date'], x[0]['url']))}
    return sorted(unique.values(), key=lambda x: (x[0]['date'], x[0]['url']), reverse=True)[:10], []


async def fetch(org, envelope, http, pages):
    proof = next((c for c in envelope.claims if c.field == 'official_website' and c.availability == 'available'), None)
    if not proof or proof.carried_forward or proof.value.get('identity_level') not in {'VERIFIED', 'HIGH', 'REGISTRY_DECLARED'}:
        website_state=envelope.run.sections.get('website')
        if website_state in {'failed','blocked','ambiguous'}:
            return missing('activity','website_check_incomplete',state=website_state)
        return missing('activity', 'no_verified_website', state='not_applicable')
    homepage = proof.value['final_url']
    root = domain(homepage)
    feeds = []
    for response, page in pages:
        if domain(response.url) != root: continue
        head = re.search(r'<head\b[^>]*>(.*?)</head\s*>', page.raw, re.I | re.S)
        if not head: continue
        for tag in re.findall(r'<link\b[^>]*>', head.group(1), re.I):
            attrs = dict((k.lower(), html.unescape(v)) for k, _, v in re.findall(r'([\w-]+)\s*=\s*([\'"])(.*?)\2', tag, re.S))
            if attrs.get('type', '').lower() in {'application/rss+xml', 'application/atom+xml'} and 'alternate' in attrs.get('rel', '').lower():
                url = normalize_url(urljoin(response.url, attrs.get('href', '')))
                if url and domain(url) == root: feeds.append(url)
    maps = []
    for origin, parser in sorted(http.robots.items()):
        if domain(origin) == root:
            maps.extend(url for url in parser.site_maps() or [] if domain(url) == root)
    fallback_maps = [
        homepage.rstrip('/') + '/sitemap.xml',
        homepage.rstrip('/') + '/sitemap_index.xml',
        homepage.rstrip('/') + '/news-sitemap.xml',
        homepage.rstrip('/') + '/feed/'
    ]
    urls = sorted(set(feeds))[:1] or sorted(set(maps))[:1] or fallback_maps[:1]
    section = Section(state='not_available')
    checked=set()
    maximum = http.config.website_request_cap + 1
    http.activity_extra.add(org)
    try:
        for level in range(2):
            if not urls: break
            target = urls[0]
            if http.counts.get(org, 0) >= maximum: raise SourceFailure('website_budget_exhausted')
            response = await http.get(target, org, root, xml=True)
            if response.status in {200,404,410}:checked.add(response.url)
            if response.status in {404, 410}: break
            if response.status in {401, 403, 429}: raise SourceFailure('http_blocked')
            if response.status != 200: raise SourceFailure('activity_fetch_error')
            items, children = await offload(parse,response.body,response.url,datetime.now(timezone.utc))
            if children:
                urls = children[:1] if level == 0 else []
                if level == 1: raise SourceFailure('activity_sitemap_depth')
                continue
            for value, locator, span in items:
                value['identity_level'] = proof.value['identity_level']
                value['identity_claim_id'] = proof.id
                add(section, response_source(response), org, 'activity', 'dated_item.' + digest(value['url'])[:20],
                    value, locator, span=span, effective=value['date'], source_class='company_owned', method='signalpost.activity.v1')
            if section.claims: section.state = 'available'
            break
        if not section.claims:
            return await fetch_html(org, proof, http, pages, checked)
        return section
    except SourceFailure as exc:
        return missing('activity', exc.code, state='blocked' if exc.code in {'robots', 'robots_unavailable', 'http_blocked'} else 'failed')
    except (ValueError, ET.ParseError):
        return await fetch_html(org, proof, http, pages, checked)
    finally:
        http.activity_extra.discard(org)
        envelope.run.refresh['activity']={'checked_urls':sorted(checked)}


def parse_html(body, source_url, now):
    """Accept only a dated, single-link article with a bounded verbatim span."""
    raw = body.decode('utf8', errors='replace')
    items = []
    seen = set()
    for n, match in enumerate(re.finditer(r'<article\b[^>]*>.*?</article\s*>', raw, re.I | re.S)):
        block = match.group()
        dates = re.findall(r'<time\b[^>]*\bdatetime\s*=\s*[\'"]([^\'"]+)[\'"]', block, re.I)
        links = re.findall(r'<a\b[^>]*\bhref\s*=\s*[\'"]([^\'"]+)[\'"][^>]*>(.*?)</a\s*>', block, re.I | re.S)
        if len(dates) != 1 or len(links) != 1:
            continue
        date = dated(dates[0], now)
        href, title_raw = links[0]
        url = normalize_url(urljoin(source_url, html.unescape(href)))
        title = html.unescape(title_raw.strip())
        if not date or not url or domain(url) != domain(source_url) or not NEWS.search(urlsplit(url).path) or NON_ITEM.search(urlsplit(url).path):
            continue
        if re.fullmatch(r'/(?:[a-z]{2}/)?(?:nyheter|news|aktuelt|presse|blogg|blog)/?', urlsplit(url).path, re.I):
            continue
        if '<' in title or not title or len(title) > 200:
            continue
        needles = [href, title_raw.strip(), dates[0]]
        ranges = [(block.find(t), block.find(t)+len(t)) for t in needles]
        start, end = min(a for a, _ in ranges), max(b for _, b in ranges)
        if start < 0 or end-start > 300:
            continue
        if url in seen:
            continue
        seen.add(url)
        items.append(({'title': title, 'title_source': 'article link', 'url': url,
                       'date': date, 'date_source': 'datetime', 'identity_level': None},
                      f'/article/{n}', block[start:end]))
    return items[:10]


async def fetch_html(org, proof, http, pages, checked):
    root = domain(proof.value['final_url'])
    section = Section(state='not_available')
    if proof.value.get('identity_level') != 'VERIFIED' or proof.value.get('other_orgnrs'):
        return section
    targets = []
    for response, page in pages:
        if domain(response.url) == root:
            targets.extend(link.href for link in page.links if NEWS.search(urlsplit(link.href).path))
    targets.extend(urljoin(proof.value['final_url']+'/', path) for path in ('nyheter', 'aktuelt', 'news', 'presse', 'blogg'))
    targets = [u for u in dict.fromkeys(map(normalize_url, targets)) if u and domain(u) == root]
    try:
        for target in targets[:2]:
            response = await http.get(target, org, root)
            if response.status != 200:
                continue
            checked.add(response.url)
            items = await offload(parse_html, response.body, response.url, datetime.now(timezone.utc))
            for value, locator, span in items:
                value['identity_level'] = proof.value['identity_level']
                value['identity_claim_id'] = proof.id
                add(section, response_source(response), org, 'activity', 'dated_item.'+digest(value['url'])[:20],
                    value, locator, span=span, effective=value['date'], source_class='company_owned', method='signalpost.activity.html.v1')
            if section.claims:
                section.state = 'available'
                break
        return section
    except SourceFailure as exc:
        return missing('activity', exc.code, state='blocked' if exc.code in {'robots', 'robots_unavailable', 'http_blocked'} else 'failed')
