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


from html.parser import HTMLParser


class EntityCard:
    """Represents a discrete corporate entity or department container on a web page."""
    def __init__(self, start: int, end: int, raw: str, text: str, tag: str, attrs: dict):
        self.start = start
        self.end = end
        self.raw = raw
        self.text = text
        self.tag = tag
        self.attrs = attrs
        self.orgnrs = orgnrs(text) | orgnrs(raw)

    def matches_org(self, org: str, context: dict | None = None, subunits: set[str] | None = None) -> bool:
        org_pat = re.compile(r'\b' + org[:3] + r'[\s.]?' + org[3:6] + r'[\s.]?' + org[6:9] + r'\b')
        if org in self.orgnrs or org_pat.search(self.raw):
            return True
        if subunits:
            for sub in subunits:
                sub_pat = re.compile(r'\b' + sub[:3] + r'[\s.]?' + sub[3:6] + r'[\s.]?' + sub[6:9] + r'\b')
                if sub in self.orgnrs or sub_pat.search(self.raw):
                    return True
        if context and context.get("name"):
            subj_tokens = [t.lower() for t in re.findall(r'[a-zA-ZæøåÆØÅ]{3,}', context["name"]) if t.lower() not in {"as", "asa", "holding", "group", "norge", "nordic", "the"}]
            if subj_tokens and all(t in self.text.lower() for t in subj_tokens) and not any(sib in self.text.lower() for sib in ["group", "gruppe", "holding"]):
                if not any(o != org for o in self.orgnrs if not (subunits and o in subunits)):
                    return True
        return False

    def is_sibling(self, org: str, other_orgnrs: set[str] | list[str] | None = None, subunits: set[str] | None = None) -> bool:
        other_set = set(other_orgnrs or [])
        if other_set and any(o in self.orgnrs for o in other_set if o != org):
            return True
        if any(o != org for o in self.orgnrs if not (subunits and o in subunits)):
            return True
        # Foreign corporate entity registration identifiers (Swedish 556xxx-xxxx, Danish CVR 8 digits, Polish REGON/NIP 10 digits)
        if re.search(r'\b(?:556\d{3}-\d{4}|\d{8}|\d{10})\b', self.text) and not bool(re.search(r'\b' + org[:3] + r'[\s.]?' + org[3:6] + r'[\s.]?' + org[6:9] + r'\b', self.text)):
            return True
        return False


def extract_entity_cards(raw_html: str) -> list[EntityCard]:
    """
    Partitions HTML into discrete corporate entity card/container elements
    (e.g. elements with classes matching card, entity, unit, company, box, invoice, contact).
    """
    cards = []
    line_offsets = [0]
    for line in raw_html.split('\n')[:-1]:
        line_offsets.append(line_offsets[-1] + len(line) + 1)

    class Parser(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.stack = []

        def _offset(self):
            line, col = self.getpos()
            return line_offsets[line - 1] + col

        def handle_starttag(self, tag, attrs):
            attrs_dict = {k.lower(): v or '' for k, v in attrs}
            cls = attrs_dict.get('class', '')
            tag_id = attrs_dict.get('id', '')
            is_card = bool(re.search(r'\b(?:card|entity|unit|company|box|invoice|contact-card|contact-box)\b', cls + ' ' + tag_id, re.I)) or tag in ('section', 'article')
            offset = self._offset()
            self.stack.append({'tag': tag, 'is_card': is_card, 'start': offset, 'attrs': attrs_dict, 'text_parts': []})

        def handle_data(self, data):
            for s in self.stack:
                s['text_parts'].append(data)

        def handle_endtag(self, tag):
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i]['tag'] == tag:
                    entry = self.stack[i]
                    if entry['is_card']:
                        parent_is_card = any(s['is_card'] for s in self.stack[:i])
                        if not parent_is_card:
                            end_offset = self._offset() + len(tag) + 3
                            card_raw = raw_html[entry['start']:end_offset]
                            card_text = ' '.join(''.join(entry['text_parts']).split())
                            cards.append(EntityCard(entry['start'], end_offset, card_raw, card_text, entry['tag'], entry['attrs']))
                    self.stack = self.stack[:i]
                    break

    p = Parser()
    try:
        p.feed(raw_html)
    except Exception:
        pass
    return cards


def find_containing_card(cards: list[EntityCard], pos: int) -> EntityCard | None:
    """Finds the entity card enclosing the character offset pos."""
    for c in cards:
        if c.start <= pos <= c.end:
            return c
    return None


def is_dedicated_entity_card(raw_html: str, org: str, name: str = "") -> bool:
    """Checks whether org appears inside a dedicated corporate entity card/block rather than an arbitrary directory table."""
    cards = extract_entity_cards(raw_html)
    for c in cards:
        if c.matches_org(org, context={"name": name}):
            return True
    pat = re.compile(r"\b" + org[0:3] + r"[\s.]?" + org[3:6] + r"[\s.]?" + org[6:9] + r"\b")
    for m in pat.finditer(raw_html):
        start = max(0, m.start() - 350)
        end = min(len(raw_html), m.end() + 250)
        window = raw_html[start:end]

        has_id_label = bool(re.search(r"(?:organisation\s+number|organisasjonsnummer|org\.?\s*nr|faktura|invoice|mva|vat)", window, re.I))
        if not has_id_label:
            continue

        is_partner = bool(re.search(r"\b(?:kunder|våre\s+kunder|partnere|våre\s+partnere|partners|clients|referanser|portfolio|directory|leverandører)\b", window, re.I))
        if is_partner:
            continue

        has_card_or_heading = bool(re.search(r'<(?:h[1-6]|div|section|article|p)[^>]*class=[\'"][^\'"]*(?:card|entity|unit|company|box|contact|invoice)[^\'"]*[\'"]', window, re.I))
        has_heading = bool(re.search(r"<h[1-6][^>]*>[^<]+</h[1-6]>", window, re.I))

        name_match = False
        if name:
            tokens = [t.lower() for t in re.findall(r"[a-zA-ZæøåÆØÅ]{3,}", name) if t.lower() not in {"as", "asa", "holding", "group", "norge", "nordic", "the"}]
            if any(t in window.lower() for t in tokens):
                name_match = True

        if (has_card_or_heading or has_heading) and (name_match or not name):
            return True
    return False


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
        # A listed partner/customer is not the operator of the page. Exact
        # identifiers in directory text need an independent entity card or
        # structured owner identifier before they can establish ownership.
        if len(others) < 2 and org not in json_ids and re.search(
            r'\b(?:our\s+partners|our\s+clients|our\s+customers|directory|våre\s+partnere|våre\s+kunder)\b',
            page.visible, re.I,
        ) and not is_dedicated_entity_card(page.raw, org, context.get('name', '')):
            return Proof("REJECT", other_orgnrs=others, reason="partner_directory_mention")
        if len(others) >= 2 and org not in json_ids:
            # Multi-entity group site check: requires registry-origin domain and dedicated entity card
            is_valid_group = False
            if origin == "registry_website":
                if is_dedicated_entity_card(page.raw, org, context.get("name", "")):
                    is_valid_group = True
            if not is_valid_group:
                return Proof("REJECT", other_orgnrs=others, reason="unverified_multi_entity_site")
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
        # Postcode/city alone can be shared by a different group company.
        if any(s and len(str(s)) > 4 and legal_name(s) in text for s in streets):
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
