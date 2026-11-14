"""Explicit publisher identity tiers. No body-name or fuzzy-name acceptance."""
import re
import unicodedata
from urllib.parse import urlsplit

from .policy import domain, normalize_url
from .publisher import extract_publisher

DECLARED = 'registry_declared_publisher_name'


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
