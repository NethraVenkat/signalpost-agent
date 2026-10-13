from typing import Literal

Availability = Literal["available", "not_available", "blocked", "not_applicable", "ambiguous", "failed"]
TerminalState = Literal["complete", "not_applicable", "not_found", "blocked_policy", "blocked_robots", "source_error", "budget_exhausted", "submission_error"]
STATE_MAP = {"available": "complete", "not_available": "not_found", "blocked": "blocked_policy", "not_applicable": "not_applicable", "ambiguous": "submission_error", "failed": "source_error"}


def reference_state(availability, errors=()):
    codes = {e.code for e in errors}
    if "budget_exhausted" in codes:
        return "budget_exhausted"
    if codes & {"invalid_orgnr", "not_started", "deadline", "input_error"}:
        return "submission_error"
    if availability == "blocked" and "robots" in codes:
        return "blocked_robots"
    return STATE_MAP[availability]
