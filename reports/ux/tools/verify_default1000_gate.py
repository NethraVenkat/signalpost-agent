"""Record the explicitly permitted network-loss exception for the two 1,000 runs."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GATES = ROOT / "gates"
BULK = Path(r"C:\Users\Manish\Downloads\Signalpost-v5\out\capacity-inputs\bulk1000.csv")
TARGET = "827248592"
MISSING_FIELDS = {"identity.legal_name", "identity.organisation_form", "identity.deleted"}


def check_run(name: str) -> dict:
    directory = GATES / name
    path = directory / "envelopes.jsonl"
    envelopes = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    available_ids = {
        claim["id"]
        for envelope in envelopes
        for claim in envelope["claims"]
        if claim["family"] == "identity" and claim["availability"] == "available"
    }
    target = next(envelope for envelope in envelopes if envelope["organisation_number"] == TARGET)
    report = json.loads((directory / "report.json").read_text(encoding="utf-8"))
    failures = [
        {key: request.get(key) for key in ("url", "organisation_number", "status", "error", "runtime_ms")}
        for request in report["request_log"]
        if request.get("organisation_number") == TARGET and request.get("error")
    ]
    return {
        "envelopes": len(envelopes),
        "distinct_organisation_numbers": len({row["organisation_number"] for row in envelopes}),
        "available_identity_ids": len(available_ids),
        "envelopes_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "target_identity_section": target["run"]["sections"]["identity"],
        "target_errors": [error for error in target["errors"] if error["section"] == "identity"],
        "target_available_identity_fields": [
            claim["field"] for claim in target["claims"]
            if claim["family"] == "identity" and claim["availability"] == "available"
        ],
        "target_failed_requests": failures,
        "identity_ids": available_ids,
    }


def main() -> None:
    first = check_run("default1000")
    retry = check_run("default1000-retry")
    bulk_text = BULK.read_text(encoding="utf-8-sig")
    missing_ids = sorted(first["identity_ids"] - retry["identity_ids"])
    added_ids = sorted(retry["identity_ids"] - first["identity_ids"])
    for run in (first, retry):
        run.pop("identity_ids")
    result = {
        "baseline_identity_ids_required": 28726,
        "target": TARGET,
        "target_absent_from_frozen_bulk_csv": TARGET not in bulk_text,
        "first": first,
        "retry": retry,
        "retry_lost_ids_relative_to_first": missing_ids,
        "retry_added_ids_relative_to_first": added_ids,
        "accepted_under_user_exception": all(
            run["envelopes"] == 1000
            and run["available_identity_ids"] == 28723
            and run["target_identity_section"] == "failed"
            and any(e["code"] == "network_error" for e in run["target_errors"])
            and any(e["error"] == "ConnectError" and e["status"] is None for e in run["target_failed_requests"])
            and not run["target_available_identity_fields"]
            for run in (first, retry)
        ) and TARGET not in bulk_text and not missing_ids and not added_ids,
    }
    path = ROOT / "default1000-gate.json"
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    assert result["accepted_under_user_exception"]


if __name__ == "__main__":
    main()
