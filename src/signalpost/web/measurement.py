"""Measure website discovery and bound each company's combined active time."""

import asyncio
from collections import Counter, defaultdict
from contextlib import asynccontextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
import time

from ..budget import SourceFailure


CAP = 'website_company_deadline'


@dataclass
class _Attempt:
    requests: int = 0
    interrupted_phase: str | None = None
    request_timeouts: Counter = field(default_factory=Counter)


_current = ContextVar('website_measurement', default=None)


@asynccontextmanager
async def phase(name):
    try:
        yield
    except asyncio.CancelledError:
        if attempt := _current.get():
            attempt.interrupted_phase = name
        raise


@asynccontextmanager
async def timed_slot(slot, name):
    async with phase(name):
        await slot.acquire()
    try:
        yield
    finally:
        slot.release()


def count_request():
    if attempt := _current.get():
        attempt.requests += 1


def count_request_timeout(name):
    if attempt := _current.get():
        attempt.request_timeouts[name] += 1
        # This individual timeout was handled. A later cancellation may occur
        # while processing proof or waiting on a different request.
        attempt.interrupted_phase = None


class WebsiteMeasurement:
    def __init__(self, company_seconds):
        self.company_seconds = company_seconds
        self.active_seconds = defaultdict(float)
        self.queue_seconds = {}
        self.queue_interrupted = set()
        self.attempts = defaultdict(list)
        self.capped = set()

    @asynccontextmanager
    async def company_slot(self, org, semaphore):
        start = time.monotonic()
        try:
            await semaphore.acquire()
        except asyncio.CancelledError:
            self.queue_interrupted.add(org)
            raise
        finally:
            self.queue_seconds[org] = time.monotonic() - start
        try:
            yield
        finally:
            semaphore.release()

    async def collect(self, org, pass_name, call):
        attempt = _Attempt()
        token = _current.set(attempt)
        start = time.monotonic()
        remaining = self.company_seconds - self.active_seconds[org]
        timeout = asyncio.timeout(max(0, remaining))
        state = 'finished'
        try:
            if remaining <= 0:
                attempt.interrupted_phase = 'prior_website_work'
                raise SourceFailure(CAP)
            async with timeout:
                return await call()
        except TimeoutError as exc:
            if not timeout.expired():
                state = 'failed'
                raise
            state = CAP
            self.capped.add(org)
            raise SourceFailure(CAP) from exc
        except SourceFailure as exc:
            state = exc.code
            if state == CAP:
                self.capped.add(org)
            raise
        except asyncio.CancelledError:
            state = 'batch_deadline'
            raise
        except Exception:
            state = 'failed'
            raise
        finally:
            elapsed = time.monotonic() - start
            self.active_seconds[org] += elapsed
            self.attempts[org].append({
                'pass': pass_name, 'active_seconds': round(elapsed, 3),
                'requests': attempt.requests, 'state': state,
                'waiting_on': (attempt.interrupted_phase or 'collector_phase_unclassified'
                               if state in {CAP, 'batch_deadline', 'deadline'} else None),
                'request_timeouts': dict(attempt.request_timeouts),
            })
            _current.reset(token)

    def report(self, organisations):
        return {
            'company_time_cap_seconds': self.company_seconds,
            'companies_hitting_cap': len(self.capped),
            'per_company': {
                org: {
                    'queue_seconds': round(self.queue_seconds.get(org, 0), 3),
                    'queue_interrupted': org in self.queue_interrupted,
                    'active_seconds': round(self.active_seconds.get(org, 0), 3),
                    'requests': sum(a['requests'] for a in self.attempts.get(org, ())),
                    'company_cap_hit': org in self.capped,
                    'attempts': self.attempts.get(org, []),
                }
                for org in sorted(organisations)
            },
        }
