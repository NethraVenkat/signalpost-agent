"""Publisher-only HTML context. This is a veto input, never identity proof."""
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from urllib.parse import urlsplit

_EXCLUDED = re.compile(r'\b(?:clients?|customers?|partners?|references?|kunder|kundeliste|partnere|referanser|news|nyheter|articles?|blog|credits?|agency|staff|team|employees|personnel|ansatte|medarbeidere|menneskene)\b', re.I)
_CREDIT = re.compile(r'\b(?:design(?:et)?|levert|utviklet|powered|developed|website|webdesign)\s+(?:av|by)\b', re.I)
_CONTACT_PATH = re.compile(r'(?:kontakt|contact|impressum|personvern|privacy|om[-_]oss|about)', re.I)
_CONTACT_SIGNAL = re.compile(r'(?:\b(?:org\.?\s*(?:nr|nummer)|organisasjonsnummer|telefon|phone|tlf|adresse|address)\b|\b\d{4}\s+[A-ZÆØÅ][\wÆØÅæøå -]+|@)', re.I)
_VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}


@dataclass
class _Node:
    tag: str
    attrs: dict
    children: list = field(default_factory=list)


@dataclass(frozen=True)
class PublisherFragment:
    location: str
    text: str


@dataclass(frozen=True)
class PublisherContext:
    fragments: tuple[PublisherFragment, ...]

    @property
    def text(self):
        return '\n'.join(f.text for f in self.fragments)


class _Tree(HTMLParser):
    def __init__(self, raw):
        super().__init__(convert_charrefs=True)
        self.root = _Node('root', {})
        self.stack = [self.root]
        self.feed(raw)

    def handle_starttag(self, tag, attrs):
        node = _Node(tag, dict(attrs))
        self.stack[-1].children.append(node)
        if tag not in _VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in _VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def _hidden(node):
    a = node.attrs
    return (node.tag in {'script', 'style', 'template', 'noscript', 'article'} or 'hidden' in a
            or str(a.get('aria-hidden', '')).lower() == 'true'
            or bool(re.search(r'display\s*:\s*none|visibility\s*:\s*hidden', a.get('style') or '', re.I)))


def _excluded(node):
    marker = re.sub(r'[_-]', ' ', (node.attrs.get('id') or '') + ' ' + (node.attrs.get('class') or ''))
    if _hidden(node) or _EXCLUDED.search(marker):
        return True
    # A heading can identify an otherwise unmarked client/partner list. Only
    # its own section is excluded, never the surrounding document or footer.
    if node.tag in {'section', 'div', 'ul', 'aside'}:
        headings = [c for c in node.children if isinstance(c, _Node) and c.tag in {'h1', 'h2', 'h3', 'h4'}]
        if any(_EXCLUDED.search(_text(h)) for h in headings):
            return True
    return False


def _text(node, cut_credit=True):
    if isinstance(node, str):
        # Agency credits do not identify the publishing legal entity, including
        # when they share one text node with the owner's copyright notice.
        return _CREDIT.split(node, maxsplit=1)[0] if cut_credit else node
    if _excluded(node):
        return ''
    if node.tag == 'img':
        return node.attrs.get('alt') or ''
    # Preserve the credit marker across child boundaries until the complete
    # region has been joined. Removing it first can leave the agency name
    # behind as a false publisher ("Utviklet av" + sibling agency link).
    parts = [_text(c, False) for c in node.children]
    text = ' '.join(' '.join(parts).split())
    # A small credit wrapper can split "levert av" across text/link nodes.
    return (_CREDIT.split(text, maxsplit=1)[0] if cut_credit else text).strip()


def _region(node):
    if node.tag == 'title':
        return 'title'
    for region, role in (('header', 'banner'), ('footer', 'contentinfo')):
        if node.tag == region or node.attrs.get('role') == role:
            return region
        markers = ((node.attrs.get('class') or '') + ' ' + (node.attrs.get('id') or '')).split()
        for marker in markers:
            # Match an actual region component, not layout modifiers such as
            # header-over-content/hasStickyHeader on a whole-page wrapper.
            if (re.fullmatch(r'(?:[a-z0-9]+[-_])?' + region + r'(?:[-_](?:container|wrapper|inner|content|row|main|top|bottom|desktop|mobile))?', marker, re.I)
                    or marker.casefold() in {'dm' + region, 'f' + region, 'dm' + region + 'container'}):
                return region
    return None


def extract_publisher(page):
    """Extract visible own branding/contact blocks, excluding third-party lists.

    ``page`` is a parsed HTML Page; extraction is local and performs no requests.
    Contact-page bodies are not wholesale publisher blocks: only bounded blocks
    containing an address, phone, email or organisation-number marker qualify.
    """
    tree = _Tree(page.raw)
    fragments = []
    contact_page = bool(_CONTACT_PATH.search(urlsplit(page.url).path))

    def add(location, text):
        text = ' '.join(text.split())
        fragment = PublisherFragment(location, text)
        if text and fragment not in fragments:
            fragments.append(fragment)

    def walk(node, inherited=False):
        if isinstance(node, str):
            if not inherited and re.search(r'©|copyright', node, re.I):
                add('copyright', _text(node))
            return
        if _excluded(node):
            return
        a = node.attrs
        marker = ((a.get('class') or '') + ' ' + (a.get('id') or '')).lower()
        block_children = any(isinstance(c, _Node) and c.tag in {'div', 'p', 'address', 'header', 'footer', 'main', 'section', 'aside', 'article', 'nav', 'ul', 'li', 'table'} for c in node.children)
        location = _region(node)
        if node.tag == 'meta' and (a.get('property') or a.get('name')) == 'og:site_name':
            add('og:site_name', a.get('content') or '')
        if location:
            add(location, _text(node))
        if re.search(r'(?:^|[ _-])logo(?:$|[ _-])', marker):
            add('logo', _text(node))
        if 'copyright' in marker and not block_children:
            add('copyright', _text(node))
        if not inherited and node.tag in {'p', 'address', 'small', 'div'}:
            text = _text(node)
            if not block_children and len(text) <= 1200 and re.search(r'©|copyright', text, re.I):
                add('copyright', text)
            is_contact = contact_page or node.tag == 'address' or bool(re.search(r'contact|kontakt|imprint', marker))
            if is_contact and len(text) <= 2000 and _CONTACT_SIGNAL.search(text):
                # Prefer the smallest complete block: parent blocks containing
                # the same signals are redundant and can include unrelated copy.
                smaller = any(isinstance(c, _Node) and c.tag in {'div', 'p', 'address', 'header', 'footer', 'main', 'section', 'aside', 'ul', 'li', 'table'} and _CONTACT_SIGNAL.search(_text(c)) for c in node.children)
                if not smaller:
                    add('imprint-kontakt', text)
        prefix = ''
        for child in node.children:
            uncut = _text(child, False)
            combined = prefix + ' ' + uncut
            if _CREDIT.search(combined):
                # Traverse only a child's own pre-credit content. If the
                # marker spans siblings, this child and all following nodes
                # are inside the credit, including logos/copyright fragments.
                if _CREDIT.search(uncut) and not _CREDIT.match(uncut.strip()):
                    walk(child, inherited or bool(location))
                break
            walk(child, inherited or bool(location))
            prefix = combined

    walk(tree.root)
    return PublisherContext(tuple(fragments))
