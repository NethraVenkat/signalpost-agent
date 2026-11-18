"""Measure one frozen cohort with the evaluator's seven flags."""

import argparse
import hashlib
import html
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from signalpost.io.input_adapter import read as read_organisations
from signalpost.portable_paths import expand, portable_text, sanitize_file
from signalpost.web.seed_index import load as load_seeds

DEST = Path(__file__).resolve().parent
ROOT = DEST.parents[2]
P3 = DEST.parent / "stageP3" / "samples"
WORK = ROOT / ".data/r5/stageW-measurements"
RECEIPTS = DEST / "seed_index_measurements"
SEEDS = (20261017, 20261113, 20261114, 20261115, 20261116, 20261117)


def read(path):
    return json.loads(path.read_text(encoding="utf8"))


def save(path, data):
    text = portable_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    path.write_text(text, encoding="utf8", newline="\n")


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def runtime_sha():
    source = ROOT / "src"
    digest = hashlib.sha256()
    for path in sorted(source.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            digest.update(path.relative_to(source).as_posix().encode())
            digest.update(bytes.fromhex(sha(path)))
    return digest.hexdigest()


def p3_directory(seed):
    return P3 / ("trials/seed20261117-retry" if seed == 20261117 else f"seed{seed}")


def measure(seed, retry):
    settings = read(p3_directory(seed) / "settings.json")
    command = settings["command_argv"]
    batch, bulk = (
        Path(expand(command[command.index(flag) + 1])) for flag in ("--organisations", "--bulk")
    )
    assert sha(batch) == settings["input_sha256"] and sha(bulk) == settings["bulk_sha256"]
    label = f"seed{seed}" + ("-retry" if retry else "")
    work = WORK / label
    out = RECEIPTS / label
    work.mkdir(parents=True, exist_ok=False)
    out.mkdir(parents=True, exist_ok=False)
    argv = [
        sys.executable, "-m", "signalpost.cli", "run",
        "--organisations", str(batch), "--bulk", str(bulk),
        "--output", str(work / "envelopes.jsonl"),
        "--profiles-output", str(work / "profiles.jsonl"),
        "--report", str(work / "report.json"), "--run-id", "r5-stageW-" + label,
        "--expected-count", "100",
    ]
    assert sum(arg.startswith("--") for arg in argv) == 7
    env = dict(os.environ, PYTHONUTF8="1", SIGNALPOST_SEARCH_PROVIDER="disabled", SIGNALPOST_SEARCH_MOCK="0")
    source_sha = runtime_sha()
    print(f"Starting {label}", flush=True)
    started = time.monotonic()
    with (out / "execution.txt").open("w", encoding="utf8", newline="\n") as log:
        execution = subprocess.run(argv, cwd=work, env=env, stdout=log, stderr=subprocess.STDOUT)
    wall = time.monotonic() - started
    sanitize_file(out / "execution.txt")
    save(out / "execution.json", {"argv": argv, "cwd": work.as_posix(), "wall_seconds": wall,
                                  "exit_code": execution.returncode, "runtime_sha256": source_sha})
    if execution.returncode:
        return execution.returncode
    args = [
        sys.executable, str(ROOT / "scripts/check_live_run.py"),
        "--output", str(work / "envelopes.jsonl"), "--organisations", str(batch),
        "--state", str(work / "state"), "--report", str(work / "report.json"),
        "--site", str(work / "site"), "--count", "100",
    ]
    checked = subprocess.run(args, cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf8")
    (out / "verification.txt").write_text(portable_text(checked.stdout + checked.stderr), encoding="utf8")
    if checked.returncode:
        return checked.returncode
    verified = json.loads(checked.stdout)
    assert runtime_sha() == source_sha, "Runtime files changed during the measurement"
    save(out / "result.json", {
        "verification": verified,
        "indexed_input_companies": len(load_seeds().keys() & set(read_organisations(batch).unique)),
        "envelopes_sha256": sha(work / "envelopes.jsonl"),
        "profiles_sha256": sha(work / "profiles.jsonl"),
        "seed_bundles": {p.name: sha(p) for p in
                         sorted((ROOT / "src/signalpost/data/website_seeds").glob("*.json.gz"))},
    })
    print(f"Verified {label} in {wall:.1f} s, {verified['http_requests']} HTTP requests", flush=True)
    return 0


def websites(path):
    result = {}
    with path.open(encoding="utf8") as stream:
        for line in stream:
            row = json.loads(line)
            org = row["organisation_number"]
            evidence = {e["id"]: e for e in row["evidence"]}
            for claim in row["claims"]:
                if claim["field"] != "official_website" or claim["availability"] != "available":
                    continue
                value = claim["value"]
                receipts = [
                    evidence[ref] for ref in claim["evidence_ids"]
                    if evidence[ref]["source_url"] == value["proof_page_url"]
                    or evidence[ref]["locator"].split(":", 3)[-1].lstrip("/") in {
                        "forretningsadresse", "forretningsadresse.*", "hjemmeside",
                        "navn", "telefon", "epostadresse", "mobil",
                    }
                ]
                assert any(e["source_url"] == value["proof_page_url"] for e in receipts), (
                    f"Website proof receipt missing for {org}"
                )
                result[org, value["final_url"]] = value, receipts
    return result


def compare():
    table = ["| Seed | Indexed companies | P3 websites | W websites | P3 HTTP | W HTTP | P3 wall s | W wall s |",
             "|---|---:|---:|---:|---:|---:|---:|---:|"]
    changes = []
    runtimes = set()
    for seed in SEEDS:
        label = f"seed{seed}"
        if (RECEIPTS / (label + "-retry") / "result.json").exists():
            label += "-retry"
        result = read(RECEIPTS / label / "result.json")
        check = result["verification"]
        before_exec = read(p3_directory(seed) / "execution.json")
        before_run = Path(expand(before_exec["cwd"]))
        after_run = WORK / label
        before = websites(before_run / "envelopes.jsonl")
        after = websites(after_run / "envelopes.jsonl")
        prior = read(p3_directory(seed) / "counts.json")
        assert len(before) == prior["counts"]["websites"]
        measured = read(RECEIPTS / label / "execution.json")
        runtimes.add(measured["runtime_sha256"])
        table.append(f"| {seed} | {result['indexed_input_companies']} | {len(before)} | {len(after)} | {prior['HTTP']} | "
                     f"{check['http_requests']} | {before_exec['wall_seconds']:.1f} | {measured['wall_seconds']:.1f} |")
        for action, primary, other in (("Added", after, before), ("Removed", before, after)):
            for org, url in sorted(primary.keys() - other.keys()):
                value, receipts = primary[org, url]
                changes.append(f"### {action} · {seed} · {org}\n\n"
                               f"`{url}` · `{value['candidate_origin']}` · `{value['proof_type']}`\n")
                for e in receipts:
                    span = html.escape(e["claim_span"]).replace("\r", "&#13;").replace("\n", "&#10;")
                    changes.append(f"\n{e['retrieved_at']} UTC · SHA-256 `{e['content_sha256']}` · "
                                   f"`{e['locator']}` · [Source](<{e['source_url']}>)\n\n"
                                   f"<pre>{span}</pre>\n")
    assert len(runtimes) == 1, "Measurements used different runtime files"
    heading = "## Stage W seed-index measurement"
    text = (heading + "\n\n"
            "Each cohort used the seven evaluator flags and a fresh working directory. "
            "The comparison uses the verified P3 run of the same cohort.\n\n"
            + "\n".join(table) + "\n\n"
            + ("\n".join(changes) if changes else "No website URL changes across the six cohorts.\n"))
    path = DEST / "new_websites.md"
    prior = path.read_bytes().decode("utf8").partition("\n" + heading)[0].rstrip()
    path.write_bytes((prior + "\n\n" + portable_text(text)).encode("utf8"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("seed", nargs="?", type=int, choices=SEEDS)
    parser.add_argument("--retry", action="store_true")
    options = parser.parse_args()
    if options.seed is None:
        compare()
    else:
        raise SystemExit(measure(options.seed, options.retry))
