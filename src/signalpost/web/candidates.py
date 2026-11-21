import json
import re
from datetime import datetime, timezone
from functools import lru_cache
from dataclasses import dataclass
from urllib.parse import urlsplit
from .policy import domain, normalize_url, SOCIAL, DIRECTORIES, FREE_MAIL
from ..sources.bulk_registry import column

FORMS = r"\b(?:as|asa|ans|da|enk|nuf|sa|ba|ks|iks|sti)\b$"
GENERIC = {"holding", "invest", "eiendom", "bygg", "service", "consult", "regnskap", "transport", "og"}


@dataclass(frozen=True)
class Candidate:
    url: str
    domain: str
    origin: str
    subunit_orgnr: str | None = None


@lru_cache(maxsize=8192)
def legal_name(value):
    text = str(value or "").casefold().strip(" .,-")
    while re.search(FORMS, text):
        text = re.sub(FORMS, "", text).strip(" .,-")
    return " ".join(re.findall(r"\w+", text))


@lru_cache(maxsize=8192)
def legal_name_slugs(name):
    tokens = [t for t in name.split() if t != "og"]
    slugs = []
    if tokens and not all(t in GENERIC for t in tokens):
        # Preserve existing nominations first, then add the requested spelling
        # and native IDNA variants. These are nominations, never identity proof.
        for replacements in (("ae", "oe", "aa"), ("a", "o", "a"), ("ae", "o", "aa"), ("a", "oe", "a"), ("ae", "o", "a")):
            converted = " ".join(tokens).replace("æ", replacements[0]).replace("ø", replacements[1]).replace("å", replacements[2])
            words = re.findall(r"[a-z0-9]+", converted)
            for separator in ("", "-"):
                slug = separator.join(words)
                if len(slug) >= 4:
                    for suffix in ("no", "com"):
                        slugs.append(slug + "." + suffix)
        for separator in ('', '-'):
            native = separator.join(tokens)
            try:
                label = native.encode('idna').decode('ascii')
            except UnicodeError:
                continue
            if len(label) >= 4:
                slugs.extend(label + '.' + suffix for suffix in ('no', 'com'))
    # Additional reported-name spellings nominate only. Keep the original
    # strongest joined/hyphenated spellings first, then filler-free variants.
    fillers={'holding','eiendom','invest','gruppen','norge'}
    reduced=[t for t in tokens if t not in fillers]
    if reduced and reduced!=tokens and not all(t in GENERIC for t in reduced):
        for ae,oe,aa in [('ae','oe','aa'),('a','o','a')]:
            converted=' '.join(reduced).replace(chr(230),ae).replace(chr(248),oe).replace(chr(229),aa)
            words=re.findall(r'[a-z0-9]+',converted)
            for separator in ('','-'):
                label=separator.join(words)
                if len(label)>=4:slugs.extend(label+'.'+suffix for suffix in ('no','com'))
    # All .no nominations precede .com; existing DNS prechecks and nomination
    # caps still apply. A DNS lookup does not spend an HTTP request.
    return sorted(dict.fromkeys(slugs),key=lambda value:not value.endswith('.no'))


def context_from_bulk(row):
    return {"name": column(row, "navn")[0], "website": column(row, "hjemmeside")[0],
            "email": column(row, "epostadresse")[0], "phone": column(row, "telefon")[0], "mobile":column(row,'mobil')[0],
            "municipality": column(row, "forretningsadresse.kommune")[0],
            "street": column(row, "forretningsadresse.adresse")[0],
            "postcode": column(row, "forretningsadresse.postnummer")[0], "city": column(row, "forretningsadresse.poststed")[0]}


def candidate_key(candidate):
    parts = urlsplit(candidate.url)
    return (parts.hostname.removeprefix('www.'), parts.path or '/')


def generate(context, limit=8):
    output = []
    seen = set()
    def add(value, origin, subunit_orgnr=None):
        url = normalize_url(value)
        root = domain(url) if url else ""
        if root and root not in seen and root not in SOCIAL | DIRECTORIES | FREE_MAIL:
            output.append(Candidate(url, root, origin,subunit_orgnr))
            seen.add(root)
    add(context.get("website"), "registry_website")
    email = str(context.get("email") or "")
    if "@" in email:
        add(email.rsplit("@", 1)[1], "registry_email")

    def add_subunit_contacts():
        for unit in context.get('subunits', []):
            add(unit.get('website'), 'subunit_registry_website', unit['orgnr'])
            email = str(unit.get('email') or '')
            if '@' in email:
                add(email.rsplit('@', 1)[1], 'subunit_registry_email', unit['orgnr'])

    name_slugs = legal_name_slugs(legal_name(context.get('name')))
    # Preserve the measured first-pass priority: strongest exact-name spellings
    # precede branch/provider contacts, which can consume the entire allowance.
    for slug in sorted(name_slugs, key=lambda value: not value.endswith('.no'))[:2]:
        add(slug, 'legal_name_slug')
    add_subunit_contacts()
    for item in context.get('nav_homepages', []):
        add(item['url'], 'nav_employer_homepage', item.get('subunit_orgnr'))
    # Brands/aliases nominate only. They never modify the legal identity used
    # by the proof layer or imply a unique-name/domain ownership relationship.
    for brand in context.get('brands', []):
        for slug in legal_name_slugs(legal_name(brand)):
            add(slug, 'brand_variant')
    # One strongest nomination from each documented former/workplace name
    # precedes weaker spelling variants. Current registry contacts stay first.
    for former in context.get('former_names', []):
        slugs=legal_name_slugs(legal_name(former))
        if slugs:add(slugs[0], 'former_registered_name')
    for unit in context.get('subunits', []):
        slugs=legal_name_slugs(legal_name(unit.get('name')))
        if slugs:add(slugs[0], 'registry_subunit_name', unit['orgnr'])
    for slug in name_slugs:
        add(slug, "legal_name_slug")
    for unit in context.get('subunits', []):
        for slug in legal_name_slugs(legal_name(unit.get('name'))):
            add(slug, 'registry_subunit_name', unit['orgnr'])
    for former in context.get('former_names', []):
        for slug in legal_name_slugs(legal_name(former)):
            add(slug, 'former_registered_name')
    return output[:min(32, limit)]



def nav_homepages(envelope, index, blobs):
    """Saved live detail employer.homepage nominates only; cache/header names do not."""
    from ..sources.nav import timestamp
    scope={envelope.organisation_number} | {c.value['organisation_number'] for c in envelope.claims
        if c.field.startswith('subunits.unit.') and c.availability=='available'
        and isinstance(c.value,dict) and c.value.get('organisation_number')}
    result={}; now=datetime.now(timezone.utc)
    for owner in sorted(scope):
        for ad in index.ads.get(owner,[]):
            try:
                if ad.value['uuid'] in index.closed: continue
                body=blobs.read(ad.sha)
                entry=json.loads(body) if body else {}
                if not isinstance(entry,dict):continue
                raw=entry.get('ad_content') or {}
                if not isinstance(raw,dict):continue
                employer=raw.get('employer') or {}
                if not isinstance(employer,dict):continue
                if (entry.get('status')!='ACTIVE' or entry.get('uuid')!=ad.value['uuid']
                        or raw.get('uuid')!=ad.value['uuid']
                        or str(employer.get('orgnr'))!=owner
                        or ad.value.get('employer_orgnr')!=owner): continue
                if not timestamp(raw.get('expires')) or timestamp(raw['expires'])<=now: continue
                if not timestamp(raw.get('published')) or timestamp(raw['published'])>now: continue
                homepage=employer.get('homepage')
                if not isinstance(homepage,str): continue
                url=normalize_url(homepage)
                if url: result[url]={'url':url, 'subunit_orgnr':owner if owner!=envelope.organisation_number else None,
                    'source_url':ad.url, 'content_sha256':ad.sha, 'locator':'/ad_content/employer/homepage'}
            except (KeyError,TypeError,ValueError): continue
    return [result[key] for key in sorted(result)]


def extract_sitemap_domains(target, legal_name_str="", brand_name="", timeout=5):
    raw = None
    if isinstance(target, bytes):
        raw = target.decode('utf-8', errors='replace')
    elif isinstance(target, str):
        if target.strip().startswith('<'):
            raw = target
        else:
            target_url = target if target.startswith(('http://', 'https://')) else f"https://{target}"
            if not target_url.endswith('.xml'):
                target_url = target_url.rstrip('/') + '/sitemap.xml'
            try:
                import httpx
                resp = httpx.get(target_url, timeout=timeout, follow_redirects=True)
                if resp.status_code == 200:
                    raw = resp.text
            except Exception:
                return []
    if not raw:
        return []
    if re.search(r'<!\s*(?:DOCTYPE|ENTITY)', raw, re.I):
        return []
    try:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(raw)
    except Exception:
        return []
    tokens = []
    if legal_name_str:
        ln = legal_name(legal_name_str)
        tokens.extend([t.lower() for t in ln.split() if t not in GENERIC and len(t) >= 4])
    if brand_name:
        tokens.append(brand_name.lower())
    
    urls = []
    for elem in root.iter():
        tag = elem.tag.rsplit('}', 1)[-1]
        if tag == 'loc' and elem.text:
            urls.append(elem.text.strip())
            
    discovered = []
    seen = set()
    for u in urls:
        norm = normalize_url(u)
        d = domain(norm) if norm else ''
        if not d or d in seen or d in SOCIAL | DIRECTORIES | FREE_MAIL:
            continue
        d_clean = re.sub(r'[^a-z0-9]', '', d.lower().split('.')[0])
        if not tokens or any(tok in d_clean for tok in tokens):
            seen.add(d)
            discovered.append(d)
            if len(discovered) >= 3:
                break
    return discovered
