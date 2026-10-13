import time
from collections import Counter


class SourceFailure(Exception):
    def __init__(self, code: str, message: str = ""):
        self.code = code
        super().__init__(message or code)


class Budget:
    def __init__(self, config):
        self.start = time.monotonic()
        self.deadline = self.start + config.time_budget_seconds * config.deadline_fraction
        self.cap = config.max_requests
        self.events = []
        self.by_host = Counter()

    def check(self):
        if time.monotonic() >= self.deadline:
            raise SourceFailure("deadline")

    def reserve(self, url: str, host: str, org: str):
        self.check()
        if len(self.events) >= self.cap:
            raise SourceFailure("budget_exhausted")
        event = {"url": url, "host": host, "organisation_number": org, "attempt_started": time.monotonic() - self.start, "status": None, "error": None}
        self.events.append(event)
        self.by_host[host] += 1
        return event
