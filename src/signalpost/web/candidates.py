import re
from functools import lru_cache
from dataclasses import dataclass
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
        for replacements in (("ae", "o", "aa"), ("a", "oe", "a")):
            converted = " ".join(tokens).replace("æ", replacements[0]).replace("ø", replacements[1]).replace("å", replacements[2])
            words = re.findall(r"[a-z0-9]+", converted)
            for separator in ("", "-"):
                slug = separator.join(words)
                if len(slug) >= 4:
                    for suffix in ("no", "com"):
                        slugs.append(slug + "." + suffix)
    return slugs


def context_from_bulk(row):
    return {"name": column(row, "navn")[0], "website": column(row, "hjemmeside")[0],
            "email": column(row, "epostadresse")[0], "phone": column(row, "telefon")[0],
            "municipality": column(row, "forretningsadresse.kommune")[0],
            "street": column(row, "forretningsadresse.adresse")[0],
            "postcode": column(row, "forretningsadresse.postnummer")[0], "city": column(row, "forretningsadresse.poststed")[0]}


def generate(context):
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
    for unit in context.get('subunits',[]):
        add(unit.get('website'),'subunit_registry_website',unit['orgnr'])
        email=str(unit.get('email') or '')
        if '@' in email:add(email.rsplit('@',1)[1],'subunit_registry_email',unit['orgnr'])
    name = legal_name(context.get("name"))
    for slug in legal_name_slugs(name):
        add(slug, "legal_name_slug")
    return output[:4]


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


class Candidates:
    @staticmethod
    def add_company_scope(context, existing_candidates=None, timeout=5):
        from .search import brave_search_mock
        base = list(existing_candidates if existing_candidates is not None else generate(context))
        seen = {c.domain for c in base}
        sitemap_domains = []
        brave_domains = []
        legal_nm = context.get('name') or ''
        brand_nm = context.get('brand') or ''
        orgnr = context.get('orgnr') or ''

        for c in list(base):
            if c.origin in ('registry_website', 'subunit_registry_website'):
                for d in extract_sitemap_domains(c.domain, legal_name_str=legal_nm, brand_name=brand_nm, timeout=timeout):
                    if d not in seen:
                        seen.add(d)
                        sitemap_domains.append(d)
                        base.append(Candidate(f"https://{d}", d, 'sitemap_discovery'))

        for item in brave_search_mock(legal_nm, brand=brand_nm, orgnr=orgnr, limit=5):
            d = item.get('domain')
            if d and d not in seen:
                seen.add(d)
                brave_domains.append(d)
                base.append(Candidate(item.get('url', f"https://{d}"), d, 'search_brave'))

        report = {
            'sitemap_domains': len(sitemap_domains),
            'brave_domains': len(brave_domains),
            'total_new': len(sitemap_domains) + len(brave_domains)
        }
        return base, report

