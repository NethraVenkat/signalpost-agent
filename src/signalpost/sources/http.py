from ..workers import offload
import asyncio
import email.utils
import random
import time
from urllib.parse import urlsplit
from dataclasses import dataclass
import httpx
from ..budget import SourceFailure
from ..models.evidence import utc_now

ALLOWED_HOSTS = {"data.brreg.no"}
FILING_YEAR_INTERVAL = 2.1  # conservative <30 starts/minute for the copy-years API


def allow(url):
    parts = urlsplit(url)
    if parts.scheme != "https" or parts.hostname not in ALLOWED_HOSTS or parts.username or parts.password or parts.port not in (None, 443):
        raise SourceFailure("url_refused", "Only HTTPS data.brreg.no:443 is permitted")
    return parts.hostname


@dataclass
class Response:
    body: bytes
    status: int
    url: str
    retrieved_at: str
    sha: str


class Http:
    def __init__(self, client, config, budget, blobs):
        self.client, self.config, self.budget, self.blobs = client, config, budget, blobs
        self.semaphores = {host: asyncio.Semaphore(config.host_concurrency) for host in ALLOWED_HOSTS}
        self.year_lock=asyncio.Lock()
        self.year_next=0
        self.year_clock=time.monotonic
        self.year_sleep=asyncio.sleep

    async def get(self, url, org):
        if '/aarsregnskap/kopi/' not in url:return await self._get(url,org)
        async with self.year_lock:
            delay=max(0,self.year_next-self.year_clock())
            if delay>=self.budget.deadline-time.monotonic():raise SourceFailure('deadline')
            if delay:await self.year_sleep(delay)
            self.budget.check()
            try:return await self._get(url,org)
            finally:self.year_next=max(self.year_next,self.year_clock()+FILING_YEAR_INTERVAL)

    async def _get(self,url,org):
        host = allow(url)
        attempts = 3 if "/regnskapsregisteret/" in url else 2
        for attempt in range(attempts):
            self.budget.check()
            response = None
            async with self.semaphores[host]:
                event = self.budget.reserve(url, host, org)
                begin = time.monotonic()
                try:
                    timeout = min(self.config.request_timeout, max(0.001, self.budget.deadline - time.monotonic()))
                    response = await self.client.get(url, timeout=timeout, follow_redirects=False)
                    event["status"] = response.status_code
                    sha = await offload(self.blobs.put,response.content)
                    event["content_sha256"] = sha
                    result = Response(response.content, response.status_code, url, utc_now(), sha)
                    if '/aarsregnskap/kopi/' in url and response.status_code==429:
                        # Do not hammer this separately rate-limited service
                        # through the generic registry retry loop. Cool down all
                        # queued companies, honoring a longer Retry-After.
                        delay=60.0
                        retry=response.headers.get('Retry-After')
                        if retry:
                            try:delay=max(delay,float(retry))
                            except ValueError:
                                try:delay=max(delay,email.utils.parsedate_to_datetime(retry).timestamp()-time.time())
                                except (ValueError,TypeError,OverflowError):pass
                        event['rate_limit_backoff_seconds']=delay
                        self.year_next=self.year_clock()+delay
                        return result
                    if response.is_redirect:
                        raise SourceFailure("url_refused", "Redirects are refused; target not requested")
                    if response.status_code not in {429, 500, 502, 503, 504} and response.status_code < 500:
                        return result
                    if attempt == attempts - 1:
                        return result
                except (httpx.TimeoutException, httpx.NetworkError) as exc:
                    event["error"] = type(exc).__name__
                    if attempt == attempts - 1:
                        raise SourceFailure("timeout" if isinstance(exc, httpx.TimeoutException) else "network_error") from exc
                except asyncio.CancelledError:
                    event["error"] = "deadline"
                    raise
                finally:
                    event["runtime_ms"] = round((time.monotonic() - begin) * 1000)
            delay = random.uniform(0.1, 0.3) * (2 ** attempt)
            if response is not None:
                retry = response.headers.get("Retry-After")
                if retry:
                    try:
                        delay = max(delay, float(retry))
                    except ValueError:
                        try:
                            delay = max(delay, email.utils.parsedate_to_datetime(retry).timestamp() - time.time())
                        except (ValueError, TypeError, OverflowError):
                            pass
            if time.monotonic() + delay >= self.budget.deadline:
                raise SourceFailure("deadline")
            await asyncio.sleep(delay)
