"""Compare a site-only rebuild with the fixed Phase 1 site."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BEFORE = ROOT / "sample" / "site"
AFTER = ROOT / "sample" / "site-after"
ENVELOPES = ROOT / "sample" / "out" / "envelopes.jsonl"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    before = {p.relative_to(BEFORE).as_posix(): p for p in BEFORE.rglob("*") if p.is_file()}
    after = {p.relative_to(AFTER).as_posix(): p for p in AFTER.rglob("*") if p.is_file()}
    # progress.json is a run-time snapshot; `signalpost site` does not regenerate it.
    before.pop("progress.json", None)
    names_match = set(before) == set(after)
    data_files = sorted(name for name in before if name.endswith(".data.js"))
    data_mismatches = [name for name in data_files if digest(before[name]) != digest(after[name])]
    growth = [
        {"path": name, "before": before[name].stat().st_size, "after": after[name].stat().st_size,
         "ratio": round(after[name].stat().st_size / before[name].stat().st_size, 6)}
        for name in sorted(set(before) & set(after))
    ]
    oversized_html = [item for item in growth if item["path"].endswith(".html") and item["after"] > 250_000]
    over_ten_percent = [item for item in growth if item["after"] > item["before"] * 1.1]
    envelope_count = sum(1 for _ in ENVELOPES.open("rb"))
    result = {
        "before_file_count_excluding_progress": len(before),
        "after_file_count": len(after),
        "file_names_match": names_match,
        "data_file_count": len(data_files),
        "data_file_byte_mismatches": data_mismatches,
        "claim_ids_and_values_identical": len(data_files) == 49 and not data_mismatches,
        "fixed_envelopes": envelope_count,
        "fixed_envelopes_sha256": digest(ENVELOPES),
        "max_html_bytes": max(item["after"] for item in growth if item["path"].endswith(".html")),
        "largest_growth": sorted(growth, key=lambda x: x["ratio"], reverse=True)[:5],
        "oversized_html": oversized_html,
        "over_ten_percent": over_ten_percent,
    }
    (ROOT / "site-gate.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    assert names_match and result["claim_ids_and_values_identical"] and envelope_count == 50
    assert not oversized_html and not over_ten_percent


if __name__ == "__main__":
    main()
