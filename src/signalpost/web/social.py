import re
from urllib.parse import urlsplit, urlunsplit
from .policy import SOCIAL, domain
from .html import json_values


def profile_url(url):
    p = urlsplit(url)
    root = domain(url)
    if p.scheme not in {"http", "https"} or root not in SOCIAL:
        return None
    bits = [x for x in p.path.split("/") if x]
    if not bits:
        return None
    lowered = [x.lower() for x in bits]
    if any(x in {"share", "sharer", "sharer.php", "intent", "login", "explore", "hashtag", "search", "privacy", "watch", "p", "reel", "reels", "profile.php", "l.php", "dialog", "status", "statuses"} for x in lowered):
        return None
    allowed = False
    if root == "linkedin.com":
        allowed = len(bits) == 2 and lowered[0] == "company"
    elif root in {"instagram.com", "x.com", "twitter.com"}:
        allowed = len(bits) == 1 and lowered[0] not in {"home", "i", "settings", "tos"}
    elif root == "facebook.com":
        allowed = len(bits) == 1 or (len(bits) == 3 and lowered[0] == "pages")
    elif root == "youtube.com":
        allowed = (len(bits) == 1 and bits[0].startswith("@")) or (len(bits) == 2 and lowered[0] in {"channel", "c", "user"})
    elif root == "tiktok.com":
        allowed = len(bits) == 1 and bits[0].startswith("@")
    return urlunsplit((p.scheme, (p.hostname or "").lower(), "/" + "/".join(bits), "", "")) if allowed else None


def discover(page):
    found = {}
    for link in page.links:
        url = profile_url(link.href)
        if url and link.owned_context:
            found.setdefault(url, link.span)
    for body in page.jsonld:
        for values in json_values(body, "sameAs", exclude_person=True):
            for value in values if isinstance(values, list) else [values]:
                if isinstance(value, str) and (url := profile_url(value)):
                    found.setdefault(url, page.span_for(value))
    return found
