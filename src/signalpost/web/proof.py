import re
from dataclasses import dataclass, field
from ..identity.orgnr import valid
from .candidates import legal_name
from .html import json_values
from .candidates import GENERIC


def orgnrs(text):
    result = set()
    for match in re.finditer(r"(?<!\w)[0-9](?:[0-9 .\u00a0]*[0-9])?(?!\w)", str(text)):
        digits = re.sub(r"[^0-9]", "", match.group())
        if valid(digits):
            result.add(digits)
    return result


def phone(value):
    text = str(value or "").strip()
    if text.startswith("+") and not text.startswith("+47"):
        return None
    number = re.sub(r"\D", "", str(value or ""))
    if number.startswith("0047"):
        number = number[4:]
    elif len(number) == 10 and number.startswith("47"):
        number = number[2:]
    return "+47" + number if len(number) == 8 else None


@dataclass
class Proof:
    level: str
    proof_type: str = ""
    signals: list[str] = field(default_factory=list)
    points: int = 0
    other_orgnrs: list[str] = field(default_factory=list)
    reason: str = ""
    token: str = ""


def score(page, org, context, origin, leaders):
    raw = page.raw.lower()
    if any(x in raw for x in ("cf-chl-", "verify you are human", "checking your browser")) or ('captcha' in raw and (len(page.visible.strip())<1000 or re.search('captcha|challenge',page.title,re.I))):
        return Proof("BLOCKED", reason="block_page")
    if any(x in raw for x in ("this domain is for sale", "domenet er til salgs", "domain is parked", "buy this domain", "sedo.com/search")):
        return Proof("REJECT", reason="parked")
    if len(page.visible.strip()) < 300:
        return Proof("LOW", reason="short_or_js_shell")
    visible = orgnrs(page.owner_text)
    meta = orgnrs(" ".join(page.meta.values()))
    json_ids = set()
    for body in page.jsonld:
        for key in ("vatID", "taxID", "identifier"):
            for value in json_values(body, key, exclude_person=True):
                # NO123456789MVA is permitted only inside an explicit identifier
                # field. Never search leiCode or arbitrary script contents.
                if isinstance(value, str):
                    normalized = re.sub(r"^\s*NO\s*|\s*MVA\s*$", " ", value, flags=re.I).strip()
                    json_ids |= orgnrs(normalized)
                elif isinstance(value, dict):
                    json_ids |= orgnrs(value.get("value", ""))
    all_ids = visible | meta | json_ids
    others = sorted(all_ids - {org})
    if org in all_ids:
        return Proof("VERIFIED", "jsonld_vatid" if org in json_ids else "orgnr_on_page", other_orgnrs=others, token=org)
    if others:
        return Proof("REJECT", other_orgnrs=others, reason="foreign_orgnr")
    text = legal_name(page.title + " " + page.meta.get("og:site_name", "") + " " + page.owner_text)
    signals = []
    points = 0
    name = legal_name(context.get("name"))
    if name and re.search(r"(?<!\w)" + re.escape(name) + r"(?!\w)", text):
        signals.append("legal_name"); points += 2
    street = context.get("street")
    streets = street if isinstance(street, list) else [street]
    address = any(s and len(str(s)) > 4 and legal_name(s) in text for s in streets)
    if not address and context.get("postcode") and context.get("city"):
        address = str(context["postcode"]) in page.visible and legal_name(context["city"]) in text
    if address:
        signals.append("address"); points += 2
    expected_phone = phone(context.get("phone"))
    page_phones = {phone(link.href[4:]) for link in page.links if link.href.startswith("tel:")}
    for match in re.finditer(r"(?:\+47|0047)[ .()0-9-]{8,20}", page.visible):
        page_phones.add(phone(match.group()))
    if expected_phone and expected_phone in page_phones:
        signals.append("phone"); points += 2
    if any(legal_name(name) and legal_name(name) in text for name in leaders):
        signals.append("leader"); points += 2
    if origin == "registry_website":
        signals.append("registry_website"); points += 2
    municipality = legal_name(context.get("municipality"))
    if municipality and municipality in text:
        signals.append("municipality"); points += 1
    # Tightened precision policy: name/source/municipality alone cannot establish
    # ownership. Guessed slug/email domains require an exact orgnr.
    # A subsidiary name in a group navigation/list is insufficient. Signal-only
    # publication also requires the page's own title/site name to identify it.
    branding = legal_name(page.title + " " + page.meta.get("og:site_name", ""))
    own_brand = bool(name and re.search(r"(?<!\w)" + re.escape(name) + r"(?!\w)", branding))
    high = points >= 5 and "legal_name" in signals and own_brand and len(signals) >= 2 and bool(set(signals) & {"address", "phone", "leader"}) and origin == "registry_website"
    if high:
        return Proof('HIGH','signals',signals,points,reason='corroboration',token=name)
    if origin == 'registry_website':
        branded = legal_name(page.title+' '+page.meta.get('og:site_name','')+' '+' '.join(page.brand_parts))
        generic = GENERIC | {'norsk','norske','norge','stiftelsen','selskap','gruppen','group','nasjonalt','ressurssenter','foreningen'}
        tokens = [t for t in name.split() if len(t)>=4 and t.isalpha() and t not in generic]
        token = next((t for t in tokens if re.search(r'(?<!\w)'+re.escape(t)+r'(?!\w)',branded)),None)
        declared=[]
        proof_token=None
        if token and page.name_span(token):
            declared.append('distinctive_legal_name'); proof_token=token
        if address:
            token = next((str(s) for s in streets if s and page.name_span(str(s))),None)
            token = token or (str(context.get('postcode')) if context.get('postcode') and page.name_span(str(context['postcode'])) else None)
            if token:
                declared.append('address'); proof_token=proof_token or token
        if expected_phone and expected_phone in page_phones:
            link = next((x for x in page.links if x.href.startswith('tel:') and phone(x.href[4:])==expected_phone),None)
            if link:
                declared.append('phone'); proof_token=proof_token or link.href
        # Audit found a housing association pointing to its management provider;
        # their shared phone alone was insufficient. Require two signal types.
        if len(declared)>=2:
            return Proof('REGISTRY_DECLARED','registry_declared_live',declared,2*len(declared),reason='registry_and_live_corroboration',token=proof_token)
    return Proof("HIGH" if high else "MEDIUM" if points >= 3 else "LOW", "signals", signals, points, reason="corroboration", token=name)
