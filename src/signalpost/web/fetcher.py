import asyncio
import time
from dataclasses import dataclass
from urllib.parse import urlsplit, urljoin, urlunsplit
from urllib.robotparser import RobotFileParser
import httpx
from ..budget import SourceFailure
from ..models.evidence import utc_now
from ..sources.http import Response
from . import policy


@dataclass
class DomainGate:
    semaphore: asyncio.Semaphore
    start_lock: asyncio.Lock
    next_start: float = 0


class WebsiteHttp:
    def __init__(self, client, config, budget, blobs, resolver=None):
        self.client, self.config, self.budget, self.blobs = client, config, budget, blobs
        self.resolver = resolver
        self.counts = {}
        self.gates = {}
        self.robots = {}
        self.robot_locks = {}
        self.attempts = {}

    async def raw(self, url, org, domains, xml=False, obey_robots=False):
        url = policy.validate_url(url, domains)
        for hop in range(4):
            parts = urlsplit(url)
            if obey_robots:
                await self.ensure_robots(url, org, domains)
            policy.check_ips(await (self.resolver or policy.resolve_public)(parts.hostname, parts.port or (443 if parts.scheme == "https" else 80)))
            root = policy.domain(url)
            gate = self.gates.setdefault(root, DomainGate(asyncio.Semaphore(2), asyncio.Lock()))
            async with gate.semaphore:
                async with gate.start_lock:
                    delay = gate.next_start - time.monotonic()
                    if delay > 0:
                        await asyncio.sleep(delay)
                    self.budget.check()
                    gate.next_start = time.monotonic() + self.config.website_politeness_seconds
                registry_requests = sum(e['organisation_number']==org and e.get('section')!='website' for e in self.budget.events)
                company_cap = min(self.config.website_request_cap,max(0,self.config.website_total_request_cap-registry_requests))
                if self.counts.get(org, 0) >= company_cap:
                    raise SourceFailure("website_budget_exhausted")
                event = self.budget.reserve(url, parts.hostname, org)
                event["section"] = "website"
                self.counts[org] = self.counts.get(org, 0) + 1
                began = time.monotonic()
                response = None
                chunks = []
                try:
                    remaining = self.budget.deadline - time.monotonic()
                    async with asyncio.timeout(min(8, max(.001, remaining))):
                        async with self.client.stream("GET", url, headers={"User-Agent": self.config.website_user_agent, "Accept": "text/html,application/xhtml+xml,text/plain"}, timeout=min(8, max(.001, remaining)), follow_redirects=False) as stream:
                            chunks = []
                            size = 0
                            event["status"] = stream.status_code
                            async for chunk in stream.aiter_bytes():
                                size += len(chunk)
                                if size > 2 * 1024 * 1024:
                                    event["error"] = "body_cap"
                                    partial = (b"".join(chunks) + chunk)[:2 * 1024 * 1024]
                                    event["content_sha256"] = self.blobs.put(partial)
                                    event["truncated"] = True
                                    raise SourceFailure("body_cap")
                                chunks.append(chunk)
                            body = b"".join(chunks)
                            sha = self.blobs.put(body)
                            event["content_sha256"] = sha
                            response = Response(body, stream.status_code, url, utc_now(), sha)
                            content_type = stream.headers.get("content-type", "").split(";", 1)[0].strip().lower()
                            if stream.is_redirect:
                                if hop == 3:
                                    raise SourceFailure("redirect_limit")
                                target = urljoin(url, stream.headers.get("location", ""))
                                url = policy.validate_url(target, domains)
                                continue
                            permitted = {"text/html", "application/xhtml+xml", "text/plain"}
                            if xml:
                                permitted |= {"application/xml", "text/xml", "application/rss+xml", "application/atom+xml"}
                            if stream.status_code == 200 and content_type not in permitted:
                                raise SourceFailure("content_type", content_type)
                            return response
                except (TimeoutError, httpx.TimeoutException) as exc:
                    event["error"] = type(exc).__name__
                    raise SourceFailure("website_timeout") from exc
                except (httpx.NetworkError, httpx.ProtocolError) as exc:
                    event["error"] = type(exc).__name__
                    raise SourceFailure("website_connect_error") from exc
                except asyncio.CancelledError:
                    event["error"] = "deadline"
                    raise
                finally:
                    if chunks and "content_sha256" not in event:
                        event["content_sha256"] = self.blobs.put(b"".join(chunks)[:2 * 1024 * 1024])
                        event["truncated"] = True
                    event["runtime_ms"] = round((time.monotonic() - began) * 1000)

    async def ensure_robots(self, url, org, domains):
        p = urlsplit(url)
        origin = urlunsplit((p.scheme, p.netloc, "", "", ""))
        lock = self.robot_locks.setdefault(origin, asyncio.Lock())
        async with lock:
            if origin not in self.robots:
                response = await self.raw(origin + "/robots.txt", org, domains)
                parser = RobotFileParser(origin + "/robots.txt")
                if response.status in (404, 410):
                    parser.parse([])
                elif response.status == 200:
                    parser.parse(response.body.decode("utf8", errors="replace").splitlines())
                else:
                    if response.status >= 500:
                        raise SourceFailure('website_http_5xx')
                    raise SourceFailure("robots_unavailable", f"HTTP {response.status}")
                self.robots[origin] = parser
                final = urlsplit(response.url)
                self.robots[urlunsplit((final.scheme, final.netloc, "", "", ""))] = parser
            if not self.robots[origin].can_fetch(self.config.website_user_agent, url):
                raise SourceFailure("robots")

    async def get(self, url, org, candidate_domain, proven=(), xml=False):
        domains = {candidate_domain, *proven}
        # Robots are checked again on the effective redirect authority. raw()
        # can follow only already permitted domains; content is not extracted
        # until the final authority's policy has also been checked.
        return await self.raw(url, org, domains, xml, obey_robots=True)

    async def candidate(self, candidate, org, proven=()):
        """Try hostname variants with verified TLS, then permitted plaintext."""
        p = urlsplit(candidate.url)
        host = p.hostname
        other = host[4:] if host.startswith('www.') else 'www.' + host
        hosts = [host, other]
        trials = [urlunsplit(('https', h, p.path or '/', '', '')) for h in hosts]
        notes = self.attempts.setdefault(org, [])
        last = None
        connect_hosts = []
        retried = False
        for target in trials:
            while True:
                try:
                    response = await self.get(target, org, candidate.domain, proven)
                    notes.append({'domain':candidate.domain,'origin':candidate.origin,'url':target,'status':response.status})
                    if 200 <= response.status < 300 or response.status in {401,403,429}:
                        return response
                    if response.status >= 500:
                        last = SourceFailure('website_http_5xx')
                    else:
                        last = SourceFailure('http_' + str(response.status))
                    break
                except SourceFailure as exc:
                    notes.append({'domain':candidate.domain,'origin':candidate.origin,'url':target,'reason':exc.code})
                    last = exc
                    if exc.code in {'robots','robots_unavailable','block_page','ssrf','url_refused','budget_exhausted','website_budget_exhausted','deadline'}:
                        raise
                    if exc.code == 'website_connect_error':
                        connect_hosts.append(urlsplit(target).hostname)
                    if exc.code in {'website_timeout','dns_timeout'} and candidate.origin == 'registry_website' and not retried and self.counts.get(org,0) < self.config.website_request_cap:
                        retried = True
                        continue
                    break
        # Plain HTTP is permitted only after actual TLS/connect failure.
        for host in dict.fromkeys(connect_hosts):
            target = urlunsplit(('http',host,p.path or '/','',''))
            try:
                response = await self.get(target,org,candidate.domain,proven)
                notes.append({'domain':candidate.domain,'origin':candidate.origin,'url':target,'status':response.status})
                if 200 <= response.status < 300 or response.status in {401,403,429}: return response
                last = SourceFailure('website_http_5xx' if response.status>=500 else 'http_'+str(response.status))
            except SourceFailure as exc:
                notes.append({'domain':candidate.domain,'origin':candidate.origin,'url':target,'reason':exc.code})
                last=exc
                if exc.code in {'robots','robots_unavailable','ssrf','url_refused','budget_exhausted','website_budget_exhausted','deadline'}: raise
        history=[n for n in notes if n['domain']==candidate.domain]
        if not any(400 <= n.get('status',0) < 500 for n in history):
            error=next((n['reason'] for n in history if n.get('reason') in {'website_timeout','website_connect_error','dns_timeout','dns_error'}),None)
            if error: raise SourceFailure(error)
        raise last or SourceFailure('no_such_domain')
