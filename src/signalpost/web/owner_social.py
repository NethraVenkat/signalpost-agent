"""Owner declarations supplement existing strict social links on proven sites."""
import json,re
import unicodedata
from urllib.parse import unquote,urlsplit,urljoin
from .social import profile_url as _profile_url,discover_strict,numeric_linkedin,shared_group_context
from .publisher_identity import normalize_name
from .publisher import _Tree,_Node,_excluded,_text,_CREDIT,extract_publisher
from .policy import domain

EXCLUDE=re.compile(r'founder|grunnlegger|agency|designer|designbyr.|webbyr.|group|gruppen|konsern|holding',re.I)
SAME_AS = 'owner_jsonld_sameas_v1'
FOLLOW_US = 'own_contact_follow_us_v1'
SAME_AS_POLICY = 'strict_header_footer_or_exact_owner_declaration_v4'
SOCIAL_POLICY = 'strict_header_footer_or_exact_owner_declaration_v5'
STRICT_NAME = 'own_header_footer_exact_name_v1'
STRICT_NUMERIC = 'own_header_footer_numeric_linkedin_v1'


def profile_key(url):
    """Compare profile identities without changing the URL that was published."""
    platform = domain(url)
    if platform == 'twitter.com':
        platform = 'x.com'
    path = unquote(urlsplit(url).path).strip('/')
    if platform == 'facebook.com' and re.fullmatch(r'pages/[^/]+/\d+', path, re.I):
        path = path.rsplit('/', 1)[1]
    if platform == 'youtube.com' and path.lower().startswith('channel/'):
        return platform, 'channel/' + path.split('/', 1)[1]
    return platform, path.casefold()


def visible_profiles(pages):
    visible = {}
    for page in pages:
        for link in page.links:
            if link.rendered and (url := profile_url(link.href)):
                platform, key = profile_key(url)
                visible.setdefault(platform, set()).add(key)
    return visible


def _handle_tokens(value):
    text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', value)
    text = text.casefold().replace('ø', 'o').replace('æ', 'ae')
    folded = ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))
    return re.findall(r'[a-z0-9]+', folded)


def _distinctive_handle(url, names):
    from .candidates import GENERIC
    from .rarity import FILLERS, FORMS

    path = unquote(urlsplit(url).path).strip('/').split('/')
    if domain(url) == 'youtube.com' and path[0].casefold() == 'channel':
        return False  # The opaque YouTube channel ID is not a name-bearing slug.
    handle = path[1] if len(path) > 1 else path[0]
    parts = _handle_tokens(handle)
    compact = ''.join(parts)
    generic = GENERIC | FILLERS | FORMS | {'cluster', 'express', 'group', 'gruppen',
                                          'konsern', 'norge', 'norway', 'terrasse'}
    for name in names:
        tokens = [token for token in _handle_tokens(name) if token not in FORMS]
        distinctive = {token for token in tokens if len(token) >= 4 and token.isalpha() and token not in generic}
        if distinctive & set(parts):
            return True
        if distinctive and compact.startswith(stem := ''.join(tokens)):
            if re.fullmatch(r'(?:as|asa|no)?\d*', compact[len(stem):]):
                return True
    return False


def same_as_veto(url, visible, company_name, former_names=()):
    platform, key = profile_key(url)
    linked = visible.get(platform, set())
    if linked - {key}:
        return 'same_as_visible_profile_conflict'
    if key not in linked and not _distinctive_handle(url, (company_name, *former_names)):
        return 'same_as_no_distinctive_name'
    return None


def former_names(records):
    return tuple(dict.fromkeys(record['navn'] for record in records if isinstance(record, dict)
                              and isinstance(record.get('navn'), str) and record['navn'].strip()))


def site_scope(site, pages, org, company_name, historical_names=()):
    """Return the first shared-site signal and the page where it appeared."""
    from .proof import IDENTIFIER_META, orgnrs, owner_identifiers
    from .social_registry import LEGAL_FORMS, foreign_name, legal_words, load, shared_domain_name

    if site.get('other_orgnrs') or site.get('relationship_note') == 'group_site':
        return 'website_group_proof', None, None
    if not pages:
        return None, None, None
    try:
        index = load()
    except (OSError, ValueError, KeyError, TypeError, EOFError):
        return 'registry_name_index_unavailable', None, None

    own_names = {legal_words(name) for name in (company_name, *historical_names) if name}
    own_stems = {words[:-1] if words[-1] in LEGAL_FORMS else words for words in own_names if words}
    registrations = index.shared_domains.get(domain(site.get('final_url') or pages[0].url), [])
    stems = {}
    if any(number == org for number, _, _ in registrations):
        for number, size, key in registrations:
            if number != org:
                stems.setdefault(size, set()).add(key)

    for page in pages:
        blocks = list(page.visible_blocks())
        numbers = {number for block in blocks for number in orgnrs(block)}
        for key, value in page.meta.items():
            if key.casefold() in IDENTIFIER_META:
                numbers.update(orgnrs(value))
        for body in page.jsonld:
            try:
                for value in owner_identifiers(body):
                    numbers.update(orgnrs(value))
            except TypeError:
                continue  # Broken structured type does not override visible identifiers.
        if other := sorted(numbers - {org}):
            return 'other_orgnr_on_page', page, other[0]
        for block in blocks:
            if name := foreign_name(block, index, own_names):
                return 'other_registered_name_on_page', page, name
            if stems and (name := shared_domain_name(block, stems, own_stems)):
                return 'other_registered_entity_on_shared_domain', page, name
    return None, None, None


def page_profiles(page, site, org, context, visible, shared):
    name = context.get('name') or ''
    profiles = {} if shared else {
        url: {'span': span, 'tier': STRICT_NUMERIC if numeric_linkedin(url) else STRICT_NAME}
        for url, span in discover_strict(page, name).items()
    }
    if name and site.get('identity_level') in {'HIGH', 'VERIFIED'}:
        for url, receipt in declared_profiles(page, name, org, context, exact_org_only=shared).items():
            if receipt['tier'] == SAME_AS and same_as_veto(url, visible, name, context.get('former_names', ())):
                continue
            profiles.setdefault(url, receipt)
    return profiles


def profile_url(value):
    try:return _profile_url(value)
    except (ValueError,TypeError):return None


def safe_domain(value):
    try:return domain(value)
    except (ValueError,TypeError):return None


def exact_identifier(value,org):
    if isinstance(value,dict):
        if value.get('country') not in (None,'NO') or value.get('addressCountry') not in (None,'NO'):return False
        prop=str(value.get('propertyID') or '').casefold()
        if prop and prop not in {'orgnr','organisasjonsnummer','organization number','organisation number','no','vat','vatid'}:return False
        value=value.get('value')
    if type(value) is int:value=str(value)
    if not isinstance(value,str):return False
    if not re.fullmatch(r'\s*(?:NO\s*)?(?:\d[\s.]*){9}(?:MVA)?\s*',value,re.I):return False
    return re.sub(r'\D','',value)==org


def declared_profiles(page,company_name,org,context=None,*,exact_org_only=False):
    from .publisher_veto import conflict
    if conflict(page,org,{**(context or {}),'name':company_name})[0]:return {}
    if not exact_org_only and shared_group_context(page):return {}
    class Tree(_Tree):
        def handle_starttag(self,tag,attrs):
            super().handle_starttag(tag,attrs)
            # Preserve the exact owner anchor, including its original escaping.
            parent=self.stack[-2] if tag not in {'area','base','br','embed','hr','img','input','link','meta','param','source','track','wbr'} else self.stack[-1]
            parent.children[-1].raw_tag=self.get_starttag_text()
    tree=Tree(page.raw);found={}
    def nodes(value):
        if isinstance(value,list):
            for child in value:yield from nodes(child)
        elif isinstance(value,dict):
            yield value
            graph=value.get('@graph',[])
            for child in graph if isinstance(graph,list) else [graph]:yield from nodes(child)
    def scripts(node):
        if isinstance(node,str):return
        a=node.attrs
        if (node.tag!='script' and _excluded(node)) or (node.tag in {'article','template','noscript'} or 'hidden' in a or a.get('aria-hidden')=='true'
            or re.search(r'display\s*:\s*none|visibility\s*:\s*hidden',a.get('style') or '',re.I)
            or re.search(r'founder|agency|credit|client|partner|customer|staff|news|article|blog|reference|team|ansatte', (a.get('class') or '')+' '+(a.get('id') or ''),re.I)):return
        if node.tag=='script' and (a.get('type') or '').lower()=='application/ld+json':
            yield ''.join(c for c in node.children if isinstance(c,str));return
        for child in node.children:
            if isinstance(child,_Node):yield from scripts(child)
    documents=[]
    for raw in scripts(tree.root):
        try:documents.append((raw,json.loads(raw)))
        except (TypeError,ValueError,RecursionError):continue
    people=set()
    for _,document in documents:
        pending=[document]
        while pending:
            value=pending.pop()
            if isinstance(value,list):pending.extend(value)
            elif isinstance(value,dict):
                types=value.get('@type',[]);types=types if isinstance(types,list) else [types]
                if 'Person' in types:
                    same=value.get('sameAs',[]);same=same if isinstance(same,list) else [same]
                    people.update(profile_url(x) for x in same if isinstance(x,str))
                pending.extend(v for v in value.values() if isinstance(v,(dict,list)))
    for raw,document in documents:
        for node in nodes(document):
            types=node.get('@type',[]);types=types if isinstance(types,list) else [types]
            if 'Person' in types or not set(t for t in types if isinstance(t,str))&{'Organization','LocalBusiness'}:continue
            if EXCLUDE.search(str(node.get('name') or '')) or node.get('parentOrganization'):continue
            if isinstance(node.get('url'),str) and safe_domain(urljoin(page.url,node['url']))!=domain(page.url):continue
            vat=node.get('vatID');identifier=node.get('identifier')
            if any(isinstance(v,dict) and (v.get('country') not in (None,'NO') or v.get('addressCountry') not in (None,'NO')) for v in (vat,identifier)):continue
            address=node.get('address')
            if isinstance(address,dict):
                country=address.get('addressCountry')
                if isinstance(country,dict):country=country.get('name') or country.get('@id')
                if country and str(country).casefold() not in {'no','norway','norge'}:continue
            if isinstance(vat,str) and re.match(r'\s*[A-Z]{2}',vat,re.I) and not re.match(r'\s*NO\b|\s*NO\d',vat,re.I):continue
            exact_name=bool(company_name) and isinstance(node.get('name'),str) and normalize_name(node['name'])==normalize_name(company_name)
            exact_id=exact_identifier(vat,org) or exact_identifier(identifier,org)
            if not exact_id and (exact_org_only or not exact_name):continue
            # A different explicit nine-digit registered ID vetoes a name match.
            values=[v.get('value') if isinstance(v,dict) else v for v in (vat,identifier)]
            values=[str(v) if type(v) is int else v for v in values]
            if any(isinstance(v,str) and re.fullmatch(r'\s*(?:NO\s*)?(?:\d[\s.]*){9}(?:MVA)?\s*',v,re.I) and not exact_identifier(v,org) for v in values):continue
            same=node.get('sameAs',[]);same=same if isinstance(same,list) else [same]
            for value in same:
                if not isinstance(value,str) or not (url:=profile_url(value)) or numeric_linkedin(url) or url in people:continue
                # Localize within this JSON-LD script, never an unrelated earlier link.
                encoded=json.dumps(value,ensure_ascii=False)[1:-1]
                options=(value,encoded,value.replace('/','\\/'))
                token=next((x for x in options if x in raw),None)
                if token is None:continue
                start=raw.index(token);span=raw[max(0,start-60):start+len(token)+60]
                if len(span)>300:span=token[:300]
                if not span or span not in page.raw:continue
                found.setdefault(url,{'span':span,'tier':SAME_AS,'owner_match':'exact_orgnr' if exact_id else 'exact_legal_name',
                    'owner_name':node.get('name'),'vatID':vat,'identifier':identifier,'sameAs':value})
    if exact_org_only or not re.search(r'kontakt|contact|impressum|imprint',urlsplit(page.url).path,re.I):return found
    publisher=extract_publisher(page)
    def anchors(node):
        if isinstance(node,str) or _excluded(node):return
        if node.tag=='a':yield node
        prefix=''
        for child in node.children:
            uncut=_text(child,False)
            if _CREDIT.search(prefix+' '+uncut):break
            if isinstance(child,_Node):yield from anchors(child)
            prefix+=' '+uncut
    def walk(node):
        if isinstance(node,str) or _excluded(node):return
        text=_text(node)
        if (node.tag in {'address','div','section','footer'} and len(text)<=2000 and re.search(r'f.lg oss|follow us',text,re.I)
            and not EXCLUDE.search(text) and any(f.text==text and f.location in {'imprint-kontakt','footer'} for f in publisher.fragments)):
            for anchor in anchors(node):
                url=profile_url(urljoin(page.url,anchor.attrs.get('href') or ''))
                if not url or numeric_linkedin(url) or EXCLUDE.search(_text(anchor)):continue
                span=getattr(anchor,'raw_tag','')
                if span and len(span)<=300 and span in page.raw:
                    found.setdefault(url,{'span':span,'tier':FOLLOW_US,'publisher_excerpt':text})
        for child in node.children:
            if isinstance(child,_Node):walk(child)
    walk(tree.root)
    return found
