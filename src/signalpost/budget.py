import time
import math
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
SITE_SECONDS_PER_COMPANY = 0.05
# After the required outputs exist, allow for twice P3g's observed
# 38.91-second site build at 500 companies.
SLOW_SITE_SECONDS_PER_COMPANY = 0.18
MIN_RESERVE_FRACTION = 0.10
# Keep at least this share of the budget for crawling before dropping the site reserve.
MIN_WORK_FRACTION = 0.25
# Never reserve more than this share without the site; small budgets must still crawl.
MAX_RESERVE_FRACTION = 0.6
HTTP_PER_100 = 1850
SECONDS_PER_100 = 35 * 60
WEBSITE_MARGIN_SECONDS = 150
# The latest F2 spent about 192 seconds after the crawl, including the site
# attempt. Allow 250 seconds for the required outputs and optional site.
WEBSITE_FINALISATION_SECONDS = 250


def finalisation_estimates(companies, site):
    return FINALISE_SECONDS_PER_COMPANY * companies, (SITE_SECONDS_PER_COMPANY * companies if site else 0.0)


class Budget:
    def __init__(self, config):
        self.start = time.monotonic()
        companies = 0
        try:
            from .io.input_adapter import read
            companies = len(read(config.organisations).unique)
        except (OSError, ValueError):
            pass
        self.companies = companies
        self.hard_request_cap = math.floor(HTTP_PER_100 * companies / 100)
        self.hard_seconds = SECONDS_PER_100 * companies / 100
        # The evaluator runs under a fixed time budget, so the default total never
        # grows with batch size: min(--time-budget-seconds, 21 s per unique input).
        # The scaled limit (35 min per 100 inputs) is an explicit opt-in only.
        if companies and getattr(config, 'scaled_time_budget', False):
            self.total_seconds = self.hard_seconds
        elif companies:
            self.total_seconds = min(config.time_budget_seconds, self.hard_seconds)
        else:
            self.total_seconds = config.time_budget_seconds
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
        self.crawl_limit = self.deadline  # No later phase may extend this deadline.
        self.website_deadline = self.deadline
        if companies >= 100 and config.time_budget_seconds == SECONDS_PER_100 and not getattr(config, 'scaled_time_budget', False):
            window = SECONDS_PER_100 - WEBSITE_MARGIN_SECONDS - WEBSITE_FINALISATION_SECONDS
            # The total default is fixed at 2,100 s for both 100 and 500 inputs.
            # Scaling this window down to 340 s at 100 discarded queued proof
            # checks while most of the actual budget was still available.
            self.website_deadline = min(self.deadline, self.start + window)
        self.cap = min(config.max_requests, self.hard_request_cap) if config.max_requests is not None else self.hard_request_cap
        self.events = []
        self.by_host = Counter()

    def check_website(self):
        if time.monotonic() >= self.website_deadline:
            raise SourceFailure('deadline')

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
        event['pass'] = 'pass1'
        self.events.append(event)
        self.by_host[host] += 1
        return event
