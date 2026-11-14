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
CORE = 'registry_declared_publisher_core_name'
REDIRECT = 'registry_declared_redirect_publisher_name'
TWO_CONTACTS = 'two_registry_contacts'


def service_publisher(page):
    text=normalize_name(extract_publisher(page).text)
    return bool(re.search(r"regnskap|accountant|accounting|webbyra|digitalbyra|web agency|property manag|eiendomsforvalt|designbyra",text))


def two_contacts_receipt(page,org,context):
    from .rarity import phone_key,load
    from .publisher_veto import conflict
    if conflict(page,org,context)[0] or service_publisher(page):return None
    street=context.get('street');streets=street if isinstance(street,list) else [street]
    postcode=str(context.get('postcode') or '')
    if not re.fullmatch(r'\d{4}',postcode):return None
    fragments=[f for f in extract_publisher(page).fragments if f.location in {'footer','imprint-kontakt'}]
    address=None
    for f in fragments:
        for street in streets:
            if not street or len(str(street))<5:continue
            if (re.search(r'(?<!\w)'+re.escape(normalize_name(street))+r'(?!\w)',normalize_name(f.text))
                and re.search(r'(?<!\d)'+postcode+r'(?!\d)',f.text)):
                address={'street':street,'postcode':postcode,'publisher_location':f.location,'publisher_excerpt':f.text}
                break
        if address:break
    if not address:return None
    try:counts=load()['counts']['phone']
    except (OSError,ValueError,KeyError):return None
    for field in ('phone','mobile'):
        key=phone_key(context.get(field));frequency=counts.get(key,0)
        if not key or not 1<=frequency<=2:continue
        for f in fragments:
            matches=re.finditer(r'(?<![\w+])(?:\+47|0047)?[ .()\d-]{8,24}(?!\w)',f.text)
            token=next((m.group() for m in matches if phone_key(m.group())==key),None)
            if token:
                return {'tier':TWO_CONTACTS,'legal_name':context.get('name'),'publisher_location':f.location,
                    'publisher_excerpt':f.text,'candidate_url':context.get('candidate_url'),'proof_page_url':page.url,
                    'proof_token':token,'phone':{'registry_field':field,'registry_value':context[field],
                    'normalized_value':key,'rarity_count':frequency},'address':address,'rarity_table':rarity_provenance()}
    return None


def redirect_receipt(page,org,context):
    declared=context.get('website');candidate=context.get('candidate_url')
    if not host(declared) or host(candidate)!=host(declared) or domain(page.url)==domain(declared):return None
    from .publisher_veto import conflict
    if conflict(page,org,context)[0]:return None
    fragment=name_fragment(page,context.get('name'))
    if not fragment:return None
    return {'tier':REDIRECT,'legal_name':context['name'],'publisher_location':fragment.location,
        'publisher_excerpt':fragment.text,'registry_homepage':declared,'candidate_url':candidate,'proof_page_url':page.url}


def core_receipt(page,org,context):
    """R6a: declared hostname plus a distinctive, rare registered name core."""
    if not host(context.get('website')) or host(context.get('candidate_url'))!=host(context.get('website')):
        return None
    if domain(page.url)!=domain(context['website']):return None
    from .rarity import name_key,load,FORMS,FILLERS
    from .candidates import GENERIC
    from .publisher_veto import conflict
    if conflict(page,org,context)[0]:return None
    key=name_key(context.get('name'))
    try:frequency=load()['counts']['name'].get(key,0)
    except (OSError,ValueError,KeyError):return None
    tokens=[t for t in re.findall(r'[a-z0-9]+',normalize_name(context.get('name'))) if t not in FORMS|FILLERS]
    if not tokens or not 1<=frequency<=2:return None
    if not any(len(t)>=4 and t.isalpha() and t not in GENERIC|{'norge','norsk','norske','gruppen','group','selskap','selskapet'} for t in tokens):return None
    pattern=re.compile(r'(?<!\w)'+r'\s+'.join(re.escape(t) for t in tokens)+r'(?!\w)')
    for fragment in extract_publisher(page).fragments:
        if pattern.search(normalize_name(fragment.text)):
            return {'tier':CORE,'legal_name':context['name'],'publisher_location':fragment.location,
                'publisher_excerpt':fragment.text,'registry_homepage':context['website'],
                'candidate_url':context['candidate_url'],'proof_page_url':page.url,
                'name_key':key,'name_rarity_count':frequency,'core_name':' '.join(tokens),'rarity_table':rarity_provenance()}
    return None


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
    span = page.name_span(receipt.get('proof_token') or receipt['legal_name'])
    if span:
        return span
    for token in re.findall(r'\w+',receipt['publisher_excerpt']):
        if len(token)>=4 and normalize_name(token) in normalize_name(receipt['legal_name']):
            if span := page.name_span(token):
                return span
    return None
