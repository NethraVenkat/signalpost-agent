import asyncio
import ipaddress
import socket
from urllib.parse import urlsplit, urlunsplit
import httpx
import tldextract
from httpcore._backends.auto import AutoBackend
from ..budget import SourceFailure

extract = tldextract.TLDExtract(suffix_list_urls=(), cache_dir=None, include_psl_private_domains=True)
SOCIAL = {"facebook.com", "instagram.com", "linkedin.com", "x.com", "twitter.com", "youtube.com", "tiktok.com"}
DIRECTORIES = {"proff.no", "proff.com", "proff.dk", "proff.se", "gulesider.no", "1881.no", "purehelp.no", "finn.no", "fb.me", "fb.com", "youtu.be", "lnkd.in", "t.co", "threads.net"}
FREE_MAIL = {"gmail.com", "googlemail.com", "hotmail.com", "hotmail.no", "outlook.com", "live.com", "live.no", "yahoo.com", "yahoo.no", "online.no", "icloud.com", "me.com", "protonmail.com", "proton.me", "aol.com", "msn.com", "mail.com"}


def domain(url):
    host = (urlsplit(url if "://" in url else "https://" + url).hostname or "").lower().rstrip(".")
    result = extract(host)
    return result.top_domain_under_public_suffix


def normalize_url(value):
    value = str(value or "").strip()
    if not value:
        return None
    parts = urlsplit(value if "://" in value else "https://" + value)
    if parts.scheme not in {"http", "https"} or not parts.hostname or parts.username or parts.password:
        return None
    try:
        if parts.port not in (None, 80, 443):
            return None
        host = parts.hostname.encode("idna").decode("ascii").lower().rstrip(".")
        if not extract(host).suffix:
            return None
    except (ValueError, UnicodeError):
        return None
    port = f":{parts.port}" if parts.port and parts.port != (443 if parts.scheme == "https" else 80) else ""
    return urlunsplit((parts.scheme, host + port, parts.path or "/", "", ""))


def validate_url(url, domains):
    normalized = normalize_url(url)
    if normalized is None or domain(normalized) not in domains or domain(normalized) in SOCIAL | DIRECTORIES:
        raise SourceFailure("url_refused", "URL lies outside this company's permitted candidate domains")
    return normalized


def check_ips(ips):
    if not ips:
        raise SourceFailure("no_such_domain")
    for value in ips:
        address = ipaddress.ip_address(value)
        if not address.is_global or address.is_multicast or address.is_reserved or address.is_unspecified:
            raise SourceFailure("ssrf", "Destination is not a public unicast address")
    return ips


async def resolve_public(host, port=443):
    try:
        records = await asyncio.wait_for(asyncio.get_running_loop().getaddrinfo(host, port, type=socket.SOCK_STREAM), timeout=8)
    except asyncio.TimeoutError as exc:
        raise SourceFailure("dns_timeout") from exc
    except socket.gaierror as exc:
        if exc.errno in {socket.EAI_NONAME, getattr(socket, 'EAI_NODATA', socket.EAI_NONAME)}:
            raise SourceFailure("no_such_domain") from exc
        raise SourceFailure("dns_error") from exc
    except OSError as exc:
        raise SourceFailure("dns_error") from exc
    return check_ips(list(dict.fromkeys(item[4][0] for item in records)))


class PublicNetworkBackend:
    """Validate at connection time and pin TCP to the vetted IP; TLS keeps SNI."""
    def __init__(self):
        self.backend = AutoBackend()

    async def connect_tcp(self, host, port, timeout=None, local_address=None, socket_options=None):
        if isinstance(host, bytes):
            host = host.decode("ascii")
        if port not in (80, 443):
            raise SourceFailure("ssrf", "Non-web port refused")
        ips = await resolve_public(host, port)
        ips.sort(key=lambda ip: ipaddress.ip_address(ip).version)
        last = None
        for ip in ips:
            try:
                return await self.backend.connect_tcp(ip, port, timeout, local_address, socket_options)
            except Exception as exc:
                last = exc
        raise last

    async def connect_unix_socket(self, *args, **kwargs):
        raise SourceFailure("ssrf", "Unix sockets refused")

    async def sleep(self, seconds):
        await self.backend.sleep(seconds)


def safe_transport(max_connections):
    transport = httpx.AsyncHTTPTransport(limits=httpx.Limits(max_connections=max_connections, max_keepalive_connections=max_connections))
    # The locked httpx/httpcore versions expose this connection backend. DNS is
    # checked again here, so preflight checks cannot be bypassed by rebinding.
    transport._pool._network_backend = PublicNetworkBackend()
    return transport
