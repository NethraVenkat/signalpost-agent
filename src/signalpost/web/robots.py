"""Match robots rules across every group applicable to the crawler."""

from dataclasses import dataclass, field
import re
from urllib.parse import quote, urlsplit


UNRESERVED = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
)
ESCAPE = re.compile(r"%([0-9a-fA-F]{2})")


def _path_octets(value):
    """Preserve escaped reserved bytes and normalize unreserved equivalents."""
    def normalize_escape(match):
        char = chr(int(match[1], 16))
        return char if char in UNRESERVED else match[0].upper()

    return ESCAPE.sub(normalize_escape, quote(value, safe="/?:@!$&'()*+,;=%[]"))


@dataclass
class _Group:
    agents: set[str] = field(default_factory=set)
    rules: list[tuple[bool, int, tuple[str, ...], bool]] = field(default_factory=list)
    has_directive: bool = False
    delay: int | None = None


def _matches(path, pieces, terminal):
    prefix, *rest = pieces
    if not rest:
        return path == prefix if terminal else path.startswith(prefix)
    if not path.startswith(prefix):
        return False
    cursor = len(prefix)
    if terminal:
        suffix = rest.pop()
        if not path.endswith(suffix):
            return False
        limit = len(path) - len(suffix)
    else:
        limit = len(path)
    # Check the literals in order without regex backtracking over wildcards.
    for literal in filter(None, rest):
        start = path.find(literal, cursor, limit)
        if start == -1:
            return False
        cursor = start + len(literal)
    return cursor <= limit


class RobotsPolicy:
    def __init__(self, lines):
        self._groups = []
        self._sitemaps = []
        group = _Group()
        for line in lines:
            key, sep, value = line.partition("#")[0].partition(":")
            if not sep:
                continue
            key, value = key.strip().lower(), value.strip()
            if key == "sitemap" and value:
                self._sitemaps.append(value)
            elif key == "user-agent":
                if not value:
                    continue
                if group.has_directive:
                    group = _Group()
                if not group.agents:
                    self._groups.append(group)
                group.agents.add(value.lower())
            elif group.agents and key in {"allow", "disallow"}:
                # An empty directive sets no rule but ends the agent list.
                group.has_directive = True
                if not value.startswith("/"):
                    continue
                terminal = value.endswith("$")
                path = _path_octets(value.removesuffix("$") if terminal else value)
                specificity = len(ESCAPE.sub("x", path.replace("*", "")))
                group.rules.append((
                    key == "allow", specificity, tuple(path.split("*")), terminal,
                ))
            elif group.agents and key == "crawl-delay" and value.isascii() and value.isdigit():
                # Nonstandard extension retained for the official-source clients.
                try:
                    group.delay = int(value)
                except ValueError:
                    pass

    @classmethod
    def from_bytes(cls, body):
        return cls(body.decode("utf-8-sig", errors="replace").splitlines())

    def _applicable(self, user_agent):
        token = user_agent.split("/", 1)[0].strip().lower()
        return ([group for group in self._groups if token in group.agents]
                or [group for group in self._groups if "*" in group.agents])

    def can_fetch(self, user_agent, url):
        parts = urlsplit(url)
        path = parts.path or "/"
        if path == "/robots.txt":
            return True
        if parts.query:
            path += "?" + parts.query
        path = _path_octets(path)
        # Longest match wins. Prefer allow when specificity is equal.
        return max(
            ((length, allow) for group in self._applicable(user_agent)
             for allow, length, pieces, terminal in group.rules
             if _matches(path, pieces, terminal)),
            default=(0, True),
        )[1]

    def crawl_delay(self, user_agent):
        return max(
            (group.delay for group in self._applicable(user_agent)
             if group.delay is not None),
            default=None,
        )

    def site_maps(self):
        return self._sitemaps.copy()
