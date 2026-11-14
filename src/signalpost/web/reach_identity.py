"""R7 publisher receipts. All reconstruction is local and conflict-first."""
import re
from .publisher import extract_publisher
from .publisher_identity import host,normalize_name,name_fragment,rarity_provenance
from .policy import domain

DECLARED_LIVE='registry_declared_live'


def different_named_publisher(page,context):
    if name_fragment(page,context.get('name')):return False
    # An explicit other legal publisher outweighs shared contact details.
    return any(re.search(r'\b[A-Z\u00c6\u00d8\u00c5][\w&.-]*(?:\s+[\w&.-]+){0,5}\s+(?:AS|ASA|IKS|SA|ANS|DA|ENK|NUF|BA|KS|STI)\b',f.text)
               for f in extract_publisher(page).fragments)


def eligible(page,org,context):
    from .publisher_veto import conflict
    from .challenge import detected
    return (not conflict(page,org,context)[0] and not detected(page)
            and len(page.visible.strip())>=300 and not different_named_publisher(page,context)
            and not re.search(r'under arbeid|kommer snart|site under maintenance|domeneparkering|default hosting|expired domain|is parked',extract_publisher(page).text,re.I))


def person_contact(text):
    if re.search(r'\b(?:daglig leder|styreleder|contact person|kontaktperson|manager|director|driftssjef|eiendomssjef|vaktmester|sales representative|ansatt|medarbeider)\b',text,re.I):return True
    # A two-part capitalized personal-looking label directly before contacts
    # is conservatively excluded unless it explicitly names a legal company.
    return bool(re.search(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\s+(?:Epost|E-post|Email|Telefon|Phone|Tlf)\s*:',text)
                and not re.search(r'\b(?:AS|ASA|IKS|SA|ANS|DA)\b',text))


def contact_fragments(page):
    # R1 excludes marked staff containers. Also abstain from contact-page
    # staff cards whose layout has no machine-readable staff class.
    staff=bool(re.search(r'\b(?:our staff|our employees|staff directory|v.re ansatte|v.re medarbeidere)\b',page.visible,re.I))
    return [f for f in extract_publisher(page).fragments
            if f.location in {'footer','imprint-kontakt'} and not (staff and f.location=='imprint-kontakt')
            and not person_contact(f.text)]


def contacts(page,context,*,all_publisher=False):
    from .rarity import phone_key,email_key,domain_key
    fragments=list(extract_publisher(page).fragments) if all_publisher else contact_fragments(page)
    allowed=contact_fragments(page)
    for f in fragments:
        if f not in allowed:continue
        for field in ('phone','mobile'):
            key=phone_key(context.get(field))
            if not key:continue
            for m in re.finditer(r'(?<![\w+])(?:\+47|0047)?[ .()\d-]{8,24}(?!\w)',f.text):
                company_phone=(f.location=='footer' or bool(re.search(r'sentralbord|switchboard|hovednummer|company phone|main office',f.text,re.I)) or normalize_name(context.get('name')) in normalize_name(f.text))
                if company_phone and phone_key(m.group())==key:yield f,field,'phone',key,m.group().strip()
        key=email_key(context.get('email'))
        if key:
            for m in re.finditer(r'[^\s@<>;,():]+@[^\s@<>;,():]+\.[^\s@<>;,():]+',f.text):
                token=m.group().rstrip('.!?')
                local=key.split('@')[0]
                company_mail=local in {'post','firmapost','kontakt','info','office','mail','hei','hello','contact','kundeservice','administrasjon','admin'}
                if email_key(token)==key and (company_mail or f.location=='footer'):yield f,'email','email',key,token
        key=domain_key(context.get('email'))
        if key and (f.location=='footer' or name_fragment(page,context.get('name'))):
            m=re.search(r'(?<![\w.-])'+re.escape(key)+r'(?![\w.-])',f.text,re.I)
            if m:yield f,'email','domain',key,m.group()


def receipt(tier,page,context,fragment,token,signal):
    return {'tier':tier,'legal_name':context.get('name'),'publisher_location':fragment.location,
        'publisher_excerpt':fragment.text,'candidate_url':context.get('candidate_url'),'proof_page_url':page.url,
        'proof_token':token,'owner_signal':signal,'rarity_table':rarity_provenance()}


def single_company_root(page,context):
    from .publisher_identity import normalize_name
    from .candidates import legal_name
    own=normalize_name(legal_name(context.get('name')))
    fragments=extract_publisher(page).fragments
    # A different site-name/logo/footer owner is disqualifying, even when a
    # company appears in the page title or a portal profile heading.
    expected=normalize_name(context.get('name'))
    forms=r'AS|ASA|IKS|SA|ANS|DA|NUF|ENK|BA|KS|STI'
    word=r'(?!(?:'+forms+r')\b)[A-Z\u00c6\u00d8\u00c5][\w&.-]*'
    legal_publisher=re.compile(r'(?<!\w)'+word+r'\s+(?:(?:'+word+r'|og|&)\s+){0,6}(?:'+forms+r')\b')
    for f in fragments:
        if f.location in {'og:site_name','logo','footer','copyright'}:
            for match in legal_publisher.finditer(f.text):
                if not expected or not normalize_name(match.group()).endswith(expected):return False
        text=normalize_name(f.text)
        if f.location=='og:site_name' and own not in text:return False
        if f.location in {'logo','copyright'} and text and own not in text and len(text)>3:
            return False
    if re.search(r'\b(?:directory|marketplace|municipality|kommune|regional portal|finn akt|andre akt|search companies|find businesses)\w*',page.visible,re.I):return False
    return True


def rare_core(page,context):
    from .rarity import name_key,load,FORMS,FILLERS
    from .candidates import GENERIC
    key=name_key(context.get('name'))
    try:frequency=load()['counts']['name'].get(key,0)
    except (OSError,ValueError,KeyError):return None
    tokens=[t for t in re.findall(r'[a-z0-9]+',normalize_name(context.get('name'))) if t not in FORMS|FILLERS]
    if not tokens or not 1<=frequency<=2:return None
    if not any(len(t)>=4 and t.isalpha() and t not in GENERIC|{'norge','norsk','norske','gruppen','group'} for t in tokens):return None
    pattern=r'(?<!\w)'+r'\s+'.join(map(re.escape,tokens))+r'(?!\w)'
    for f in extract_publisher(page).fragments:
        if re.search(pattern,normalize_name(f.text)):
            return receipt(DECLARED_LIVE,page,context,f,' '.join(tokens),{'kind':'rare_name_core','name_key':key,'rarity_count':frequency})
    return None


def declared_live(page,org,context):
    from urllib.parse import urlsplit
    from .policy import normalize_url
    declared=context.get('website')
    url=normalize_url(declared)
    if not url or urlsplit(url).path not in {'','/'}:return None
    if urlsplit(page.url).path not in {'','/'}:return None
    if not host(declared) or host(context.get('candidate_url'))!=host(declared) or domain(page.url)!=domain(declared):return None
    if not eligible(page,org,context) or not single_company_root(page,context):return None
    if core:=rare_core(page,context):return {**core,'registry_homepage':declared}
    for f,field,kind,key,token in contacts(page,context,all_publisher=True):
        return {**receipt(DECLARED_LIVE,page,context,f,token,{'kind':kind,'registry_field':field,'registry_value':context[field],'normalized_value':key}), 'registry_homepage':declared}
    street=context.get('street');streets=street if isinstance(street,list) else [street]
    for f in extract_publisher(page).fragments:
        if f.location=='imprint-kontakt' and f not in contact_fragments(page):continue
        normalized=normalize_name(f.text)
        for street in streets:
            if street and len(str(street))>=5 and re.search(r'(?<!\w)'+re.escape(normalize_name(street))+r'(?!\w)',normalized):
                return {**receipt(DECLARED_LIVE,page,context,f,str(street),{'kind':'street','registry_street':street}),'registry_homepage':declared}
        postcode=str(context.get('postcode') or '');city=normalize_name(context.get('city'))
        if re.fullmatch(r'\d{4}',postcode) and city and re.search(r'(?<!\d)'+postcode+r'(?!\d)',normalized) and re.search(r'(?<!\w)'+re.escape(city)+r'(?!\w)',normalized):
            return {**receipt(DECLARED_LIVE,page,context,f,postcode,{'kind':'postcode_city','postcode':postcode,'city':context['city']}),'registry_homepage':declared}
    return None

RULES={DECLARED_LIVE:declared_live}

def unique_phone(page,org,context):
    from .rarity import load
    if not eligible(page,org,context) or not single_company_root(page,context):return None
    publisher=normalize_name(extract_publisher(page).text)
    if re.search(r'regnskap|accountant|accounting|webbyra|digitalbyra|agency|eiendomsforvalt|property manag|forvaltning',publisher):return None
    try:counts=load()['counts']['phone']
    except (OSError,ValueError,KeyError):return None
    for f,field,kind,key,token in contacts(page,context):
        if kind=='phone' and counts.get(key)==1:
            return receipt('unique_registry_phone',page,context,f,token,{'kind':kind,'registry_field':field,'registry_value':context[field],'normalized_value':key,'rarity_count':1})
    return None

RULES['unique_registry_phone']=unique_phone

def unique_email(page,org,context):
    from .rarity import load
    if not eligible(page,org,context) or not single_company_root(page,context):return None
    try:counts=load()['counts']['email']
    except (OSError,ValueError,KeyError):return None
    for f,field,kind,key,token in contacts(page,context,all_publisher=True):
        if kind=='email' and counts.get(key)==1:
            return receipt('unique_registry_email',page,context,f,token,{'kind':kind,'registry_field':field,'registry_value':context[field],'normalized_value':key,'rarity_count':1})
    return None

RULES['unique_registry_email']=unique_email

def registered_place(page,org,context):
    if not eligible(page,org,context) or not single_company_root(page,context):return None
    from .social import shared_group_context
    if shared_group_context(page):return None
    text=normalize_name(extract_publisher(page).text)
    if re.search(r'regnskap|accountant|accounting|advokat|law firm|webbyra|digitalbyra|agency|eiendomsforvalt|property manag|forvaltning',text):return None
    name=name_fragment(page,context.get('name'))
    if not name:return None
    # Full legal-form suffix must actually be in the exact registry name.
    if not re.search(r'\b(?:AS|ASA|SA|ANS|DA|IKS|NUF|ENK|BA|KS|STI)\s*$',str(context.get('name') or ''),re.I):return None
    postcode=str(context.get('postcode') or '');city=normalize_name(context.get('city'))
    if not re.fullmatch(r'\d{4}',postcode):return None
    street=context.get('street');streets=street if isinstance(street,list) else [street]
    for f in contact_fragments(page):
        folded=normalize_name(f.text)
        if not re.search(r'(?<!\d)'+postcode+r'(?!\d)',folded):continue
        street=next((s for s in streets if s and len(str(s))>=5 and re.search(r'(?<!\w)'+re.escape(normalize_name(s))+r'(?!\w)',folded)),None)
        city_match=bool(city and re.search(r'(?<!\w)'+re.escape(city)+r'(?!\w)',folded))
        if not street and not city_match:continue
        return {**receipt('publisher_name_registered_place',page,context,name,context['name'],{'kind':'exact_full_legal_name_and_registered_place'}),
            'place':{'publisher_location':f.location,'publisher_excerpt':f.text,'postcode':postcode,
                     'street':street,'city':context.get('city') if city_match else None}}
    return None

RULES['publisher_name_registered_place']=registered_place
