import time
from collections import Counter


class SourceFailure(Exception):
    def __init__(self, code: str, message: str = ""):
        self.code = code
        super().__init__(message or code)


# Seconds of terminal work per company after the crawl stops: output write and
# verification, finalisation, synthesis, profiles and report. Calibrated on the
# 1,000-company capacity runs (reports/step1a-finalisation.md).
FINALISE_SECONDS_PER_COMPANY = 0.03
# Static site generation, which is optional and skipped when it cannot fit.
SITE_SECONDS_PER_COMPANY = 0.025
MIN_RESERVE_FRACTION = 0.10
# Keep at least this share of the budget for crawling before dropping the site reserve.
MIN_WORK_FRACTION = 0.25
# Never reserve more than this share without the site; small budgets must still crawl.
MAX_RESERVE_FRACTION = 0.6


def finalisation_estimates(companies, site):
    return FINALISE_SECONDS_PER_COMPANY * companies, (SITE_SECONDS_PER_COMPANY * companies if site else 0.0)


class Budget:
    def __init__(self, config):
        self.start = time.monotonic()
        self.total_seconds = config.time_budget_seconds
        companies = 0
        try:
            from .io.input_adapter import read
            companies = len(read(config.organisations).unique)
        except (OSError, ValueError):
            pass
        self.finalise_estimate, self.site_estimate = finalisation_estimates(companies, config.site_dir is not None)
        # Crawl until budget - max(finalisation + site, 10%). If that leaves too
        # little time to crawl, drop the optional site reserve first, then cap
        # the reserve so a small budget still crawls (finalisation shrinks with
        # the evidence actually gathered).
        total = self.total_seconds
        full = max(self.finalise_estimate + self.site_estimate, MIN_RESERVE_FRACTION * total)
        self.site_reserved = total - full >= MIN_WORK_FRACTION * total
        if self.site_reserved:
            reserve = full
        else:
            reserve = min(max(self.finalise_estimate, MIN_RESERVE_FRACTION * total), MAX_RESERVE_FRACTION * total)
        crawl_seconds = max(0.0, min(total - reserve, total * config.deadline_fraction))
        self.deadline = self.start + crawl_seconds
        self.cap = config.max_requests if config.max_requests is not None else 20 * companies
        self.events = []
        self.by_host = Counter()

    def seconds_left(self):
        return self.start + self.total_seconds - time.monotonic()

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
