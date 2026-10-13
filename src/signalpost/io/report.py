import math
from collections import Counter


def statistics(values):
    ordered = sorted(values)
    def percentile(p):
        return ordered[max(0, math.ceil(len(ordered) * p) - 1)] if ordered else 0
    return {"p50_ms": percentile(.5), "p95_ms": percentile(.95), "max_ms": max(ordered, default=0)}


def build(envelopes, inputs, budget, config, warnings, runtime):
    unique = {e.organisation_number: e for e in envelopes}
    company_events=[e for e in budget.events if e['organisation_number'] in unique]
    by_org = Counter(e["organisation_number"] for e in company_events)
    completed = [e.get("attempt_started", 0) + e.get("runtime_ms", 0)/1000 for e in budget.events]
    starts = [e.get("attempt_started", 0) for e in budget.events]
    active_seconds = max(completed, default=0) - min(starts, default=0)
    return {"run_id": config.run_id, "input_rows": len(inputs.rows), "unique_inputs": len(inputs.unique),
            'emit_duplicates':config.emit_duplicates,
            "emitted_envelopes": len(envelopes), "duplicates": inputs.duplicates, "invalid_inputs": inputs.invalid,
            "counts_by_state": dict(Counter(e.state for e in envelopes)),
            "counts_by_availability": dict(Counter(s for e in envelopes for s in e.run.sections.values())),
            "requests": len(budget.events), "requests_per_company": len(company_events) / len(unique) if unique else 0,
            'shared_requests':len(budget.events)-len(company_events),
            'amortized_requests_per_company':len(budget.events)/len(unique) if unique else 0,
            "requests_by_host": dict(budget.by_host), "request_log": budget.events,
            "request_rate_per_second": len(budget.events) / active_seconds if active_seconds > 0 else 0,
            "http_429_count": sum(e.get("status") == 429 for e in budget.events),
            "max_requests_per_company": max(by_org.values(), default=0),
            "runtime_ms": round(runtime * 1000), "company_runtime": statistics([e.operations.runtime_ms for e in unique.values()]),
            "total_cost_usd": 0, "cost_per_100_companies_usd": 0, "cost_per_official_batch_usd": 0,
            "official_batch_size": config.official_batch_size,
            "deadline_hits": sum(any(x.code == "deadline" for x in e.errors) for e in unique.values()),
            "handled_exceptions": sum(x.code in {"section_exception", "company_exception"} for e in unique.values() for x in e.errors),
            "unhandled_exceptions": 0, "changes": sum(len(e.changes) for e in unique.values()),
            'observation_changes':sum(len(e.run.refresh.get('observation_changes',[])) for e in unique.values()),
            "warnings": warnings, "limits": {k: getattr(config, k) for k in ("max_requests", "max_cost_usd", "time_budget_seconds", "deadline_fraction", "request_timeout", "host_concurrency")},
            "schema_validated": True, "membership_validated": True}
