"""Explicit publisher identity tiers. No body-name or fuzzy-name acceptance."""
import re
import unicodedata
import hashlib
from functools import lru_cache
from urllib.parse import urlsplit

from .policy import domain, normalize_url
from .publisher import extract_publisher

DECLARED = 'registry_declared_publisher_name'
RARE = 'publisher_name_rare_contact'


def normalize_name(value):
    # Keep punctuation, word order, suffix and every other accent significant.
    # Only the three Norwegian letters have spelling-normalisation equivalents.
    text = unicodedata.normalize('NFC', str(value or '')).casefold()
    return ' '.join(text.replace('æ', 'ae').replace('ø', 'o').replace('å', 'a').split())


def name_fragment(page, name):
    expected = normalize_name(name)
    if not expected:
        return None
    pattern = re.compile(r'(?<!\w)' + re.escape(expected) + r'(?!\w)')
    return next((f for f in extract_publisher(page).fragments
                 if f.location != 'logo' and pattern.search(normalize_name(f.text))), None)


def host(value):
    url = normalize_url(value)
    return (urlsplit(url).hostname or '').removeprefix('www.') if url else None


def declared_match(page, org, context):
    declared = normalize_url(context.get('website'))
    nominated = normalize_url(context.get('candidate_url'))
    if not declared or not nominated or host(nominated)!=host(declared):
        return False
    if domain(page.url)==domain(declared):
        return True
    # A cross-domain redirect needs another explicit company registry domain,
    # or this company's exact number in the destination publisher context.
    email = str(context.get('email') or '')
    email_domain = email.rsplit('@',1)[1] if re.fullmatch(r'[^\s@]+@[^\s@]+',email) else None
    if email_domain and domain(page.url)==domain(email_domain):
        return True
    from .proof import orgnrs
    return org in orgnrs(extract_publisher(page).text)


def declared_receipt(page, org, context):
    fragment = name_fragment(page,context.get('name'))
    if not fragment or not declared_match(page,org,context):
        return None
    return {'tier': DECLARED, 'legal_name': context['name'], 'publisher_location':fragment.location,
            'publisher_excerpt':fragment.text, 'registry_homepage':context['website'],
            'candidate_url':context['candidate_url'], 'proof_page_url':page.url}


@lru_cache(maxsize=1)
def rarity_provenance():
    from .rarity import DEFAULT_PATH,load
    table=load()
    return {'bundle_sha256':hashlib.sha256(DEFAULT_PATH.read_bytes()).hexdigest(),
            'built_at':table['built_at'],'entity_count':table['entity_count'],
            'sources':table['sources'],'attribution':table['attribution'],'licence_url':table['licence_url']}


def rare_receipt(page,org,context):
    """One full publisher-name group plus one rare footer/contact group."""
    fragment=name_fragment(page,context.get('name'))
    if not fragment:return None
    from .rarity import phone_key,email_key,domain_key,load
    try:
        table=load();provenance=rarity_provenance()
    except (OSError,ValueError,KeyError):
        return None
    expected=[]
    for field in ('phone','mobile'):
        if key:=phone_key(context.get(field)):expected.append((field,'phone',key))
    if key:=email_key(context.get('email')):expected.append(('email','email',key))
    if (key:=domain_key(context.get('email'))) and key==domain(page.url):
        expected.append(('email','domain',key))
    for field,kind,key in expected:
        frequency=table['counts'][kind].get(key,0)
        if not 1<=frequency<=2:continue
        for contact in extract_publisher(page).fragments:
            if contact.location not in {'footer','imprint-kontakt'}:continue
            if kind=='phone':
                matches=[m.group() for m in re.finditer(r'(?<![\w+])(?:\+47|0047)?[ .()\d-]{8,24}(?!\w)',contact.text)]
                token=next((m for m in matches if phone_key(m)==key),None)
            else:
                emails=[m.group() for m in re.finditer(r'[^\s@<>;,():]+@[^\s@<>;,():]+\.[^\s@<>;,():]+',contact.text)]
                token=next((m for m in emails if (email_key(m.rstrip('.!?')) if kind=='email' else domain_key(m.rstrip('.!?')))==key),None)
                if not token and kind=='domain':
                    match=re.search(r'(?<![\w.-])'+re.escape(key)+r'(?![\w.-])',contact.text,re.I)
                    token=match.group() if match else None
            if not token:continue
            return {'tier':RARE,'legal_name':context['name'],'publisher_location':fragment.location,
                'publisher_excerpt':fragment.text,'candidate_url':context.get('candidate_url'),'proof_page_url':page.url,
                'contact':{'registry_field':field,'registry_value':context[field],'kind':kind,'normalized_value':key,
                    'publisher_location':contact.location,'publisher_excerpt':contact.text,'matched_text':token,
                    'rarity_count':frequency},'rarity_table':provenance}
    return None


def localized_span(page, receipt):
    # The receipt stores the complete, independently reconstructed publisher
    # fragment. Evidence also retains the entire hashed response; a verbatim
    # raw span anchors it even when markup splits the full name across nodes.
    span = page.name_span(receipt['legal_name'])
    if span:
        return span
    for token in re.findall(r'\w+',receipt['publisher_excerpt']):
        if len(token)>=4 and normalize_name(token) in normalize_name(receipt['legal_name']):
            if span := page.name_span(token):
                return span
    return None
