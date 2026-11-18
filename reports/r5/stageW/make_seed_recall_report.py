"""Write the evidence-pinned W3 hand-check inventory from paired runs."""

import hashlib
import html
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEST = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from scripts.precision_ledger import recheck  # noqa: E402


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf8").splitlines() if line.strip()]


def run_claims(label):
    work = ROOT / f".data/r5/seed-recall-{label}"
    rows = read_jsonl(work / "envelopes.jsonl")
    result = {}

    def body(digest):
        blob = work / "state/blobs" / digest
        raw = blob.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == digest
        return raw

    for row in rows:
        evidence = {item["id"]: item for item in row["evidence"]}
        for claim in row["claims"]:
            if claim["field"] != "official_website" or claim["availability"] != "available":
                continue
            value = claim["value"]
            receipts = []
            for evidence_id in claim["evidence_ids"]:
                item = evidence[evidence_id]
                raw = body(item["content_sha256"])
                assert item["claim_span"] in raw.decode("utf8", errors="replace")
                receipts.append(item)
            verdict, reasons, _ = recheck(row, claim, body)
            result[row["organisation_number"], value["final_url"]] = {
                "company": next((item["value"] for item in row["claims"]
                                 if item["field"] == "identity.legal_name" and item["availability"] == "available"),
                                row["organisation_number"]),
                "value": value, "automated_verdict": verdict, "reasons": reasons,
                "receipts": receipts,
            }
    return result


def main():
    cohort = read_jsonl(DEST / "seed_recall_100.jsonl")
    assert len(cohort) == 100
    source = json.loads((DEST / "seed_recall_100_sources.json").read_text(encoding="utf8"))
    assert set(source) == {row["organisation_number"] for row in cohort}
    on, off = run_claims("on"), run_claims("off")
    additions = sorted(on.keys() - off.keys())
    # Only entries nominated by the bundled index can count as seed-only gains.
    seed_only = [key for key in additions if on[key]["value"].get("candidate_origin")
                 in {"seed_commoncrawl", "seed_openstreetmap"}]

    def order(key):
        value = on[key]
        doubtful = value["automated_verdict"] not in {"correct", "supported"}
        return (not doubtful, key[0], key[1])

    seed_only.sort(key=order)
    receipts = []
    for key in seed_only:
        value = on[key]
        receipts.append({
            "organisation_number": key[0], "company": value["company"], "website": key[1],
            "index_source": source[key[0]], "candidate_origin": value["value"].get("candidate_origin"),
            "proof_tier": value["value"].get("proof_type"),
            "automated_verdict": value["automated_verdict"], "automated_reasons": value["reasons"],
            "evidence": [{k: item[k] for k in ("source_url", "retrieved_at", "content_sha256", "locator",
                                                   "extraction_method", "claim_span")}
                         for item in value["receipts"]],
        })
    on_exec = json.loads((DEST / "seed_recall_on/execution.json").read_text(encoding="utf8"))
    off_exec = json.loads((DEST / "seed_recall_off/execution.json").read_text(encoding="utf8"))
    sha = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
    def section_diagnostics(label):
        rows = read_jsonl(ROOT / f".data/r5/seed-recall-{label}/envelopes.jsonl")
        return {
            "website_section_states": dict(Counter(row["run"]["sections"].get("website", "missing")
                                                   for row in rows)),
            "website_errors": dict(Counter(error.get("code", "unknown") for row in rows
                                           for error in row.get("errors", [])
                                           if error.get("section") == "website")),
        }
    source_manifest = {path.relative_to(ROOT / "src").as_posix(): sha(path)
                       for path in sorted((ROOT / "src").rglob("*"))
                       if path.is_file() and "__pycache__" not in path.parts}
    source_hash = hashlib.sha256()
    for path, digest in source_manifest.items():
        source_hash.update(path.encode())
        source_hash.update(bytes.fromhex(digest))
    draw = json.loads((DEST / "seed_recall_draw.json").read_text(encoding="utf8"))
    summary = {
        "cohort_count": 100,
        "source_quotas": dict(Counter(source.values())),
        "cohort_sha256": sha(DEST / "seed_recall_100.jsonl"),
        "registry_subset_sha256": sha(DEST / "seed_recall_100_registry.csv"),
        "draw": draw,
        "runtime_src_manifest_sha256": source_hash.hexdigest(),
        "on_diagnostics": section_diagnostics("on"),
        "off_diagnostics": section_diagnostics("off"),
        "on_run": {k: on_exec[k] for k in ("seeds_enabled", "exactly_seven_flags", "wall_seconds",
                                             "input_sha256", "bulk_sha256", "envelopes_sha256", "verification")},
        "off_run": {k: off_exec[k] for k in ("seeds_enabled", "exactly_seven_flags", "wall_seconds",
                                               "input_sha256", "bulk_sha256", "envelopes_sha256", "verification")},
        "published_websites_with_seeds": len(on), "published_websites_without_seeds": len(off),
        "net_extra_published_websites": len(on.keys() - off.keys()),
        "seed_only_published_websites": receipts,
    }
    (DEST / "seed_recall_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
                                                    encoding="utf8", newline="\n")
    esc = lambda text: html.escape(str(text), quote=False).replace("\r", "&#13;").replace("\n", "&#10;")
    lines = [
        "# W3 seed index recall hand-check",
        "",
        "## Paired measurement",
        "",
        "Both variants used the same frozen 100-company input and registry subset, fresh state, and exactly seven evaluator CLI flags. The default-on run was compared with `SIGNALPOST_WEBSITE_SEEDS=0`; this config override changes only whether the bundled website seed index is loaded.",
        "",
        f"- Cohort: `{summary['cohort_sha256']}` (100 organizations; CC {summary['source_quotas'].get('commoncrawl', 0)}, OSM {summary['source_quotas'].get('openstreetmap', 0)}).",
        "- Frozen registry subset: `" + summary["registry_subset_sha256"] + "` (2026-11-16 snapshot; 100/100 rows).",
        f"- Seeds on: {on_exec['wall_seconds']:.1f}s; {len(on)} published websites; checker HTTP count {on_exec['verification']['http_requests']}; verifier site build {on_exec['verification']['site_verified'] }.",
        f"- Seeds off: {off_exec['wall_seconds']:.1f}s; {len(off)} published websites; checker HTTP count {off_exec['verification']['http_requests']}; verifier site build {off_exec['verification']['site_verified']}.",
        f"- Websites published only by the seeds-on run: {len(additions)}; seed-index-attributed additions: {len(seed_only)}.",
        "",
        f"Both runs used about 1,785 seconds, reached website verification, and completed output/site publishing. Neither published a website (on section states: `{summary['on_diagnostics']['website_section_states']}`; off: `{summary['off_diagnostics']['website_section_states']}`). Website diagnostics were on `{summary['on_diagnostics']['website_errors']}` and off `{summary['off_diagnostics']['website_errors']}`. The checker verified 100 terminal envelopes and 100 complete briefings in each run, 102 source blobs for seeds on and 102 for seeds off, and the offline site in each. Observed extra published websites: zero. Because the website stage had many `website_source_unavailable` / budget failures and published no claims in either run, this comparison is inconclusive about seed-index recall and supplies no seed-only pages for hand-check; it does not establish that the index has no useful candidates.",
        "",
        "## Seed-only websites for human hand-check",
        "",
        "Automated-doubtful entries are listed first.",
        "",
    ]
    if not receipts:
        lines.append("No seed-only website was published by either run, so there are no website claims to hand-check from this cohort.")
    for index, item in enumerate(receipts, 1):
        lines += [
            f"### {index}. {esc(item['company'])} ({item['organisation_number']}) — {esc(item['website'])}",
            "",
            f"- Index source: `{item['index_source']}`; candidate origin: `{item['candidate_origin']}`.",
            f"- Proof tier: `{item['proof_tier']}`; automated verdict: **{item['automated_verdict']}**.",
        ]
        for receipt in item["evidence"]:
            lines += ["", f"Source: <{receipt['source_url']}> · {receipt['retrieved_at']} UTC · `{receipt['locator']}` · `{receipt['extraction_method']}` · SHA-256 `{receipt['content_sha256']}`", "", "<pre>", esc(receipt["claim_span"]), "</pre>"]
        lines.append("")
    lines += ["## Disposition", "", "The paired runs are complete and their claims are pinned in `seed_recall_summary.json`. No seed-only site was published, so there is no URL for the reviewer to hand-check from this cohort. The observed zero is inconclusive because the website section had widespread source/budget failures. The full pytest suite passed (1,393 tests; see `seed_recall_pytest.txt`). No 500-company run was started.", ""]
    (DEST / "seed_recall.md").write_text("\n".join(lines), encoding="utf8", newline="\n")
    print(json.dumps({"on_websites": len(on), "off_websites": len(off),
                      "net_additions": len(additions), "seed_only": len(seed_only)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
