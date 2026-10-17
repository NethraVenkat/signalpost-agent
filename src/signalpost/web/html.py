import html
import json
import re
from html.parser import HTMLParser
from dataclasses import dataclass
from urllib.parse import urljoin


@dataclass
class Link:
    href: str
    text: str
    span: str
    owned_context: bool


def decode_html(body: bytes) -> str:
    """Decodes HTML body bytes, honoring declared charset (<meta charset> / Content-Type) with UTF-8 priority."""
    from ..sources.text import decode_body
    return decode_body(body)


class Page(HTMLParser):
    def __init__(self, body: bytes, url: str):
        super().__init__(convert_charrefs=True)
        self.body = body
        self.raw = decode_html(body)
        self.url = url
        self.stack = []
        self.visible_parts = []
        self.owner_parts = []
        self.brand_parts = []
        self.title = ""
        self.meta = {}
        self.jsonld = []
        self.links = []
        self._anchor = None
        self._script = None
        self._scripts = []
        self._line_offsets = [0]
        # HTMLParser increments line numbers only on LF. Unicode separators
        # inside script strings are not parser newlines.
        for line in self.raw.split('\n')[:-1]:
            self._line_offsets.append(self._line_offsets[-1] + len(line) + 1)
        self.segments = []
        self.paragraphs = []
        self._paragraph = None
        self.feed(self.raw)
        for text in self._scripts:
            try:
                self.jsonld.append(json.loads(text))
            except (ValueError, TypeError):
                pass
        self.visible = " ".join(self.visible_parts)
        self.owner_text = " ".join(self.owner_parts)

    def handle_starttag(self, tag, attrs):
        attrs = {key: value or "" for key, value in attrs}
        context = tag in {"header", "footer", "nav"} or attrs.get("role") in {"contentinfo", "banner", "navigation"} or any(word in (attrs.get("id", "") + " " + attrs.get("class", "")).lower() for word in ("footer", "header", "navigation"))
        if tag not in {"meta", "link", "img", "br", "hr", "input", "source", "area", "base", "embed", "wbr"}:
            hidden = "hidden" in attrs or attrs.get("aria-hidden") == "true" or any(x in attrs.get("style", "").replace(" ", "").lower() for x in ("display:none", "visibility:hidden"))
            self.stack.append((tag, context, hidden))
        if tag == "meta":
            self.meta[attrs.get("property") or attrs.get("name") or ""] = attrs.get("content", "")
        if tag == "a":
            self._anchor = Link(urljoin(self.url, attrs.get("href", "")), "", self.get_starttag_text()[:300], any(x[1] for x in self.stack) and not any(x[0] == "article" or x[2] for x in self.stack))
        if tag == "script" and attrs.get("type", "").lower() == "application/ld+json":
            self._script = ""
        if tag == 'p' and not any(x[2] for x in self.stack):
            line,col=self.getpos()
            self._paragraph={'start':self._line_offsets[line-1]+col,'parts':[]}

    def handle_endtag(self, tag):
        if tag == 'p' and self._paragraph:
            line,col=self.getpos();end=self._line_offsets[line-1]+col+4
            text=''.join(self._paragraph['parts']).strip()
            if text:
                self.paragraphs.append((text,self.raw[self._paragraph['start']:end][:300]))
            self._paragraph=None
        if tag == "a" and self._anchor:
            self.links.append(self._anchor)
            self._anchor = None
        if tag == "script" and self._script is not None:
            self._scripts.append(self._script)
            self._script = None
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                self.stack = self.stack[:i]
                break

    def handle_data(self, data):
        if self._script is not None:
            self._script += data
        if any(x[0] == "title" for x in self.stack) and any(x[0] == "head" for x in self.stack):
            self.title += data
        if not any(x[0] in {"script", "style", "noscript", "template", "head"} or x[2] for x in self.stack):
            if self._paragraph:
                self._paragraph['parts'].append(data)
            self.visible_parts.append(data)
            if not any(x[0] in {"article", "pre", "code"} for x in self.stack):
                self.owner_parts.append(data)
                if any(x[0] in {'header','footer'} or x[1] for x in self.stack):
                    self.brand_parts.append(data)
            line, col = self.getpos()
            self.segments.append((data, self._line_offsets[line - 1] + col))
        if self._anchor:
            self._anchor.text += data

    def span_for(self, token):
        pattern = re.compile(r"\s+".join(re.escape(part) for part in str(token).split()), re.I) if token else None
        if pattern:
            match = pattern.search(self.raw)
            if match:
                return self.raw[max(0, match.start() - 40):max(0, match.start() - 40) + 300]
        for data, offset in self.segments:
            if token in data:
                index = offset + data.find(token)
                return self.raw[max(0, index - 50):max(0, index - 50) + 300]
        index = self.raw.find(token)
        if index >= 0:
            return self.raw[max(0, index - 50):max(0, index - 50) + 300]
        if isinstance(token, str) and token.startswith(('https://', 'http://')):
            # JSON-LD may escape slashes or Unicode. Localize the original JSON
            # string rather than quoting unrelated document-opening markup.
            for match in re.finditer(r'"(?:\\.|[^"\\])*"', self.raw):
                try:
                    decoded = json.loads(match.group())
                except (ValueError, TypeError):
                    continue
                if decoded == token:
                    return self.raw[match.start():match.start() + 300]
        return self.raw[:300]

    def name_span(self, token):
        if not token:
            return None
        pattern=re.compile(r"\s+".join(re.escape(part) for part in token.split()),re.I)
        # Prefer the document title or actual visible data over script metadata.
        for title in re.finditer(r'<title\b[^>]*>(.*?)</title\s*>',self.raw,re.I|re.S):
            match=pattern.search(title.group(1))
            if match:
                index=title.start(1)+match.start()
                return self.raw[max(0,index-40):max(0,index-40)+300]
        for data,offset in self.segments:
            match=pattern.search(data)
            if match:
                index=offset+match.start()
                return self.raw[max(0,index-40):max(0,index-40)+300]
        match = pattern.search(self.raw)
        if not match:
            return None
        return self.raw[max(0, match.start() - 40):max(0, match.start() - 40) + 300]

    def proof_span(self, org):
        pattern = re.compile(r"(?<!\d)" + r"[ .\u00a0]*".join(org) + r"(?!\d)")
        for data, offset in self.segments:
            match = pattern.search(data)
            if match:
                index = offset + match.start()
                span = self.raw[max(0, index - 40):max(0, index - 40) + 150]
                if pattern.search(html.unescape(span)):
                    return span
        match = pattern.search(self.raw)
        if match:
            return self.raw[max(0, match.start() - 40):max(0, match.start() - 40) + 150]
        return None


def json_values(value, key, exclude_person=False):
    if isinstance(value, list):
        for item in value:
            yield from json_values(item, key, exclude_person)
    elif isinstance(value, dict):
        if exclude_person and value.get("@type") == "Person":
            return
        if key in value:
            yield value[key]
        for name, item in value.items():
            if name != "leiCode":
                yield from json_values(item, key, exclude_person)
