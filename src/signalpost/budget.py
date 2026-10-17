import time
from collections import Counter


class SourceFailure(Exception):
    def __init__(self, code: str, message: str = ""):
        self.code = code
        super().__init__(message or code)


# Seconds of terminal work per company after the crawl stops: output write and
# verification, finalisation, synthesis, profiles and report. Calibrated on the
# 1,000-company capacity runs (reports/step1a-finalisation.md).
FINALISE_SECONDS_PER_COMPANY = 0.01
# Static site generation, which is optional and skipped when it cannot fit.
SITE_SECONDS_PER_COMPANY = 0.05
OUTPUT_MARGIN_SECONDS = 5.0
MIN_WORK_FRACTION = 0.80


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
        # Measured 1,000-company short-run mandatory output work takes ~9 s.
        # Reserve that per-company cost plus a fixed margin, never a percentage
        # of a long budget. Optional rendering yields before mandatory output.
        total = self.total_seconds
        full = self.finalise_estimate + self.site_estimate + OUTPUT_MARGIN_SECONDS
        self.site_reserved = total - full >= MIN_WORK_FRACTION * total
        reserve = full if self.site_reserved else self.finalise_estimate + OUTPUT_MARGIN_SECONDS
        # A sub-five-second diagnostic still gets a bounded opportunity to
        # perform a live lookup rather than expiring before the first request.
        reserve = min(reserve, max(self.finalise_estimate, total - 1.0))
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
