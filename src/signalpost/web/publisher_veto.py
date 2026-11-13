"""Conflict-first vetoes; no positive evidence or new proof tier."""
import re
import unicodedata
from .candidates import legal_name
from .publisher import extract_publisher

_FORMS = r'as|asa|iks|sa|ans|da|nuf|ba|ks|enk|sti'
_GROUP = re.compile(r'\b(?:group|gruppen|konsern|holding|parent company|morselskap|our companies|our subsidiaries|våre selskaper|konsernselskaper|datterselskap)\b', re.I)
_ROLE = re.compile(r'\b(?:regnskapsbyrå|regnskapskontor|regnskapsfører|accountants?|accounting|advokat(?:firma)?|law firm|webbyrå|web agency|digitalbyrå|eiendomsforvalt(?:er|ning)|property manag(?:er|ement))\b', re.I)
_PLACEHOLDER = re.compile(r'(?:this domain is for sale|domenet er til salgs|domain is parked|buy this domain|under construction|under utvikling|nettsiden kommer|website coming soon|welcome to nginx|apache2? (?:debian|ubuntu) default|iis windows server|default web site|hosting default|account suspended)', re.I)


def _fold(value):
    return ' '.join(re.findall(r'\w+', unicodedata.normalize('NFKC', str(value or '')).casefold()))


def conflict(page, org, context):
    """Return (rule, foreign IDs) before scoring, or no conflict.

    Proven subunits arrive from the existing exact-parent registry collector.
    A list of arbitrary page identifiers never becomes an affiliation proof.
    """
    from .proof import orgnrs
    from ..identity.orgnr import valid
    publisher = extract_publisher(page)
    text = publisher.text
    ids = orgnrs(text)
    ids.update(number for number in re.findall(r'(?<!\d)\d{9}(?!\d)', text) if valid(number))
    allowed = {org, str(context.get('publisher_company_orgnr') or org)}
    allowed.update(str(u['orgnr']) for u in context.get('subunits', []) if u.get('orgnr'))
    others = sorted(ids - allowed)
    if others:
        return 'publisher_foreign_orgnr', others
    folded = _fold(text)
    name = str(context.get('name') or '')
    stem = _fold(legal_name(name))
    expected = re.search(r'\b(' + _FORMS + r')\s*[.,]*$', name, re.I)
    if expected and stem:
        form = expected.group(1).casefold()
        for other in re.findall(r'(?<!\w)' + re.escape(stem) + r'\s+(' + _FORMS + r')(?!\w)', folded):
            if other != form and {other, form} != {'as', 'asa'}:
                return 'publisher_conflicting_legal_form', []
    if _PLACEHOLDER.search(text):
        return 'publisher_placeholder', []
    if org not in ids and _GROUP.search(text):
        return 'publisher_group_without_exact_orgnr', []
    branding = ' '.join(f.text for f in publisher.fragments if f.location in {'title', 'og:site_name', 'header', 'logo', 'copyright'})
    own_brand = bool(stem and re.search(r'(?<!\w)' + re.escape(stem) + r'(?!\w)', _fold(branding)))
    # An accountant's own website is allowed. A third-party service publisher
    # does not become our company through a client mention or shared contact.
    if _ROLE.search(text) and not own_brand:
        return 'publisher_service_provider', []
    return None, []
