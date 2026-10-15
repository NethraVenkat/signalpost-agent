"""Decode evidence text without rewriting bytes or repairing literal content."""
import re
from html.parser import HTMLParser


class CharsetParser(HTMLParser):
    def __init__(self):
        super().__init__();self.declared=None
    def handle_starttag(self, tag, attrs):
        if tag!='meta' or self.declared is not None:return
        attrs=dict(attrs)
        match=re.search(r'charset\s*=\s*([\w-]+)',attrs.get('content',''),re.I)
        self.declared=attrs.get('charset') or (match.group(1) if match else None)


def decode_body(body: bytes) -> str:
    codec = 'utf-8-sig'
    if not body.lstrip(b'\xef\xbb\xbf \t\r\n').startswith(b'<'):
        return body.decode(codec, errors='replace')
    parser=CharsetParser();parser.feed(body[:2048].decode('latin1'))
    if parser.declared and not body.startswith(b'\xef\xbb\xbf'):
        codec = {'utf-8':'utf-8-sig','utf8':'utf-8-sig',
                 'windows-1252':'cp1252','cp1252':'cp1252',
                 'iso-8859-1':'latin1','latin1':'latin1'}.get(parser.declared.lower(), 'utf-8-sig')
    return body.decode(codec, errors='replace')
