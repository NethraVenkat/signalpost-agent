"""Owner declarations supplement existing strict social links on proven sites."""
import json,re
from urllib.parse import urlsplit,urljoin
from .social import profile_url as _profile_url,numeric_linkedin,shared_group_context
from .publisher_identity import normalize_name
from .publisher import _Tree,_Node,_excluded,_text,_CREDIT,extract_publisher
from .policy import domain

EXCLUDE=re.compile(r'founder|grunnlegger|agency|designer|designbyr.|webbyr.|group|gruppen|konsern|holding',re.I)


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


def declared_profiles(page,company_name,org,context=None):
    from .publisher_veto import conflict
    if shared_group_context(page) or conflict(page,org,{**(context or {}),'name':company_name})[0]:return {}
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
            exact_name=normalize_name(node.get('name'))==normalize_name(company_name)
            exact_id=exact_identifier(vat,org) or exact_identifier(identifier,org)
            if not (exact_name or exact_id):continue
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
                found.setdefault(url,{'span':span,'tier':'owner_jsonld_sameas_v1','owner_match':'exact_orgnr' if exact_id else 'exact_legal_name',
                    'owner_name':node.get('name'),'vatID':vat,'identifier':identifier,'sameAs':value})
    if not re.search(r'kontakt|contact|impressum|imprint',urlsplit(page.url).path,re.I):return found
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
                    found.setdefault(url,{'span':span,'tier':'own_contact_follow_us_v1','publisher_excerpt':text})
        for child in node.children:
            if isinstance(child,_Node):walk(child)
    walk(tree.root)
    return found
