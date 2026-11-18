"""Prepare, run and audit the fresh seed-20261121 qualification cohort."""

import argparse
import gzip
import hashlib
import html
import importlib.util
import json
import os
import re
import sys
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

from signalpost.identity.orgnr import valid
from signalpost.portable_paths import portable_text
from signalpost.sources.text import decode_body

DEST = Path(__file__).resolve().parent
ROOT = DEST.parents[2]
WORK = ROOT / ".data/r5/final500-clean"
SEED = 20261121
COUNT = 500
SAMPLE = re.compile(
    r"^(?:companies|company_numbers|batch|sample|selection|registry|pilot|ci20|cohort|"
    r"orgs|orgnrs|organisations|organizations)[^.]*\.(?:jsonl|json|csv|txt)(?:\.gz)?$",
    re.I,
)
SKIP = {".git", ".venv", ".aws", ".codex", "node_modules", "__pycache__", "blobs", "state", "site"}

spec = importlib.util.spec_from_file_location(
    "signalpost_scale_measurement", ROOT / "reports/r5/stageP3/P3g/check_scale.py")
scale = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scale)
scale.DEST = DEST
scale.CLONE = WORK / "repo"
scale.CLONE_PY = scale.CLONE / ".venv/Scripts/python.exe"
scale.SEED = SEED
scale.COUNT = COUNT
scale.ENV["UV_CACHE_DIR"] = str(ROOT / ".data/r5/final500-uv-cache")
scale.work_dir = lambda label: WORK / f"run-{label}"


def excluded_sample_numbers():
    tracked = {ROOT / file for file in scale.git("ls-files").splitlines()
               if SAMPLE.fullmatch(Path(file).name)}
    local = set()
    for directory, subdirs, files in os.walk(ROOT):
        parent = Path(directory)
        subdirs[:] = [name for name in subdirs if name not in SKIP
                      and parent / name != WORK and parent / name != DEST
                      and parent / name != ROOT / ".data/r5/inputs"]
        local.update(parent / name for name in files if SAMPLE.fullmatch(name))
    per_file = {}
    orgs = set()
    for sample in sorted(tracked | local):
        with (gzip.open(sample, "rt", encoding="utf-8-sig", errors="replace")
              if sample.suffix == ".gz" else sample.open(encoding="utf-8-sig", errors="replace")) as source:
            values = {number for line in source
                      for number in re.findall(r"(?<!\d)\d{9}(?!\d)", line) if valid(number)}
        if values:
            per_file[sample.relative_to(ROOT).as_posix()] = len(values)
            orgs.update(values)
    for name in (
        "tests/fixtures/ci20.jsonl", "reports/r5/baseline/companies.jsonl",
        "reports/r5/scale500/companies500.jsonl", "reports/r5/stageP3/P3e/companies500.jsonl",
        "reports/r5/stageP3/P3g/companies500.jsonl",
    ):
        assert name in per_file, name
    return per_file, orgs


scale.committed_sample_numbers = excluded_sample_numbers


def tests():
    (scale.CLONE / ".data").mkdir(exist_ok=True)
    env = dict(scale.ENV)
    for name in ("SIGNALPOST_SEARCH_PROVIDER", "SIGNALPOST_SEARCH_MOCK"):
        env.pop(name)
    outcome = scale.command("pytest-clone", [
        scale.CLONE_PY, "reports/r5/stage4_7/run_tests.py", "-q", "-p", "no:cacheprovider",
        "--basetemp", ".data/pytest", "--tb=short",
    ], cwd=scale.CLONE, env=env)
    return outcome["exit_code"]


def measure(label):
    clone_receipt = json.loads((DEST / "clean_clone.json").read_text(encoding="utf8"))
    assert scale.git("rev-parse", "HEAD", cwd=scale.CLONE) == clone_receipt["clone_head"]
    assert scale.git("status", "--porcelain", cwd=scale.CLONE) == ""
    work = scale.work_dir(label)
    work.mkdir(exist_ok=False)
    prefix = "" if label == "final" else "trials/retry/"
    (DEST / prefix).mkdir(parents=True, exist_ok=True)
    batch, bulk = DEST / "companies500.jsonl", DEST / "registry500.csv"
    assert scale.sha(batch) == clone_receipt["sample_sha256"]
    assert scale.sha(bulk) == clone_receipt["subset_sha256"]
    argv = [
        scale.CLONE_PY, "-m", "signalpost.cli", "run",
        "--organisations", batch, "--bulk", bulk, "--output", work / "envelopes.jsonl",
        "--profiles-output", work / "profiles.jsonl", "--report", work / "report.json",
        "--run-id", f"r5-f2-seed{SEED}-{label}", "--expected-count", COUNT,
    ]
    assert sum(str(arg).startswith("--") for arg in argv) == 7
    print(f"Starting final qualification {label}", flush=True)
    scale.command(prefix + "run", argv, cwd=work)
    scale.evaluate(label, "check_live_run")
    summary_path = DEST / prefix / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf8"))
    report = json.loads((work / "report.json").read_text(encoding="utf8"))
    snapshot_used = report.get("bulk_snapshot_sha256") == clone_receipt["subset_sha256"]
    summary["gates"]["frozen_registry_snapshot_used"] = snapshot_used
    summary["all_gates_pass"] &= snapshot_used
    scale.save(prefix + "summary.json", summary)


def audit(label):
    sys.path.insert(0, str(ROOT))
    from scripts.precision_ledger import kind, recheck

    prefix = "" if label == "final" else "trials/retry/"
    path = DEST / prefix / "summary.json"
    summary = json.loads(path.read_text(encoding="utf8"))
    report = json.loads((DEST / prefix / "report.json").read_text(encoding="utf8"))
    assert report["limits"]["effective_time_budget_seconds"] == 2100
    assert report["limits"]["deadline_fraction"] == 0.85
    work = scale.work_dir(label)

    @lru_cache(maxsize=48)
    def read_body(digest):
        return (work / "state/blobs" / digest).read_bytes()

    records = []
    cutoffs = defaultdict(set)
    placeholders = 0
    with (work / "envelopes.jsonl").open(encoding="utf8") as stream:
        for line in stream:
            row = json.loads(line)
            org = row["organisation_number"]
            placeholders += row["state"] == "budget_exhausted"
            for error in row["errors"]:
                if error["code"] == "deadline":
                    cutoffs[error["section"]].add(org)
            evidence = {e["id"]: e for e in row["evidence"]}
            company = next((c["value"] for c in row["claims"] if c["field"] == "identity.legal_name"
                            and c["availability"] == "available"), org)
            site = next((c["value"] for c in row["claims"] if c["field"] == "official_website"
                         and c["availability"] == "available"), {})
            for claim in row["claims"]:
                if claim["availability"] != "available":
                    continue
                typ = kind(claim)
                is_registry_social = claim["field"].startswith("registry_social.")
                if is_registry_social:
                    typ = "social"
                if typ not in {"website", "social"}:
                    continue
                value = claim["value"]
                origin = value.get("candidate_origin")
                tier = value["proof_type"] if typ == "website" else value.get("proof_tier")
                if is_registry_social:
                    tier = "registry_asserted"
                    verdict, reasons = "registry assertion", ["The exact Brreg row declares this URL."]
                else:
                    verdict, reasons, _ = recheck(row, claim, read_body)
                category = verdict
                if verdict == "wrong":
                    legacy_social = (tier in {"owner_jsonld_sameas_v1", "own_contact_follow_us_v1"}
                                     and reasons == ["own header/footer/name/numeric-link policy no longer verifies"])
                    legacy_pdf = reasons == ["StopIteration"] and bool(site.get("pdf_proof"))
                    if summary['gates']['check_live_run_exit_0'] and (legacy_social or legacy_pdf):
                        category = "legacy verifier limitation"
                    else:
                        category = "unresolved wrong verdict"
                receipts = []
                for eid in claim["evidence_ids"]:
                    receipt = evidence[eid]
                    if (receipt["source_class"] == "official_registry"
                            and not is_registry_social
                            and receipt["locator"].split(":", 3)[-1].lstrip("/") not in {
                                "navn", "hjemmeside", "forretningsadresse", "forretningsadresse.*",
                                "telefon", "epostadresse", "mobil",
                            }):
                        continue
                    raw = read_body(receipt["content_sha256"])
                    assert hashlib.sha256(raw).hexdigest() == receipt["content_sha256"]
                    assert receipt["claim_span"] in decode_body(raw) and len(receipt["claim_span"]) <= 300
                    receipts.append({key: receipt[key] for key in (
                        "source_url", "retrieved_at", "content_sha256", "locator", "claim_span",
                    )})
                records.append({
                    "organisation_number": org, "company": company, "kind": typ,
                    "url": value["final_url"] if typ == "website" else value["url"],
                    "proof_tier": tier, "candidate_origin": origin, "ledger_verdict": verdict,
                    "category": category, "reasons": reasons, "receipts": receipts,
                })
    assert placeholders == len(report["output_limited_companies"])
    summary["gates"]["zero_placeholders"] = placeholders == 0
    summary["gates"]["wall_under_2100_seconds"] = summary["wall_seconds"] < 2100
    summary["gates"]["frozen_registry_snapshot_used"] = report.get("bulk_snapshot_sha256") == scale.sha(
        DEST / "registry500.csv")
    summary["all_gates_pass"] = all(summary["gates"].values())
    section_names = set(summary["section_states"]) | cutoffs.keys()
    summary["deadline_companies_by_section"] = {name: len(cutoffs[name]) for name in sorted(section_names)}
    summary["placeholders"] = placeholders
    summary["margin_seconds"] = 2100 - summary["wall_seconds"]
    summary["adaptive_website_pass2_deadline"] = report["adaptive_websites"]["pass2"]["states"].get("deadline", 0)
    counts = Counter(r["category"] for r in records)
    summary["url_inventory_categories"] = dict(counts)
    scale.save(prefix + "summary.json", summary)

    titles = {
        "unresolved wrong verdict": "Unresolved wrong ledger verdicts",
        "legacy verifier limitation": "Wrong labels caused by older ledger rules",
        "doubtful": "Doubtful ledger verdicts",
        "registry assertion": "Registry-declared social URLs",
        "correct": "Correct ledger verdicts",
    }
    order = {category: number for number, category in enumerate(titles)}
    records.sort(key=lambda x: (order[x["category"]], x["kind"], x["organisation_number"], x["url"]))
    text = ["# F2 published website and social URLs", "",
            "The legacy ledger labels appear alongside current saved-proof verification. "
            "Where the current validators passed, older-rule errors are listed under the corresponding heading.", ""]
    for category, heading in titles.items():
        text.extend((f"## {heading} ({counts[category]})", ""))
        for r in (item for item in records if item["category"] == category):
            text.extend((f"### {r['organisation_number']} · {r['company']} · {r['kind']}", "",
                         f"`{r['url']}` · `{r['proof_tier']}` · ledger {r['ledger_verdict']}", ""))
            if r["reasons"]:
                text.extend((" | ".join(r["reasons"]), ""))
            for e in r["receipts"]:
                span = html.escape(e["claim_span"]).replace("\r", "&#13;").replace("\n", "&#10;")
                text.extend((
                    f"{e['retrieved_at']} UTC · SHA-256 `{e['content_sha256']}` · "
                    f"`{e['locator']}` · [Source](<{e['source_url']}>)", "", f"<pre>{span}</pre>", "",
                ))
    (DEST / "urls.md").write_text(portable_text("\n".join(text)), encoding="utf8", newline="\n")
    scale.save("urls.json", {"run": label, "counts": dict(counts), "records": records})
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "tests", "run", "audit"))
    parser.add_argument("label", nargs="?", choices=("final", "retry"), default="final")
    args = parser.parse_args()
    if args.phase == "prepare":
        assert not scale.CLONE.exists(), "Initial qualification requires a fresh clone"
        scale.prepare()
    elif args.phase == "tests":
        raise SystemExit(tests())
    elif args.phase == "run":
        measure(args.label)
    else:
        print(json.dumps(audit(args.label), indent=2))
