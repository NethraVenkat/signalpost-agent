"""Run the W3 fresh-state, paired seed-index measurement on its pinned cohort."""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from signalpost.portable_paths import portable_text, sanitize_file

ROOT = Path(__file__).resolve().parents[3]
DEST = Path(__file__).resolve().parent
PYTHON = ROOT / ".venv/Scripts/python.exe"
BATCH = DEST / "seed_recall_100.jsonl"
BULK = DEST / "seed_recall_100_registry.csv"
ENV = dict(os.environ, PYTHONUTF8="1", SIGNALPOST_SEARCH_PROVIDER="disabled",
           SIGNALPOST_SEARCH_MOCK="0")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    Path(path).write_text(portable_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n"),
                          encoding="utf8", newline="\n")


def run(enabled):
    label = "on" if enabled else "off"
    work = ROOT / f".data/r5/seed-recall-{label}"
    receipt = DEST / f"seed_recall_{label}"
    work.mkdir(parents=True, exist_ok=False)
    receipt.mkdir(parents=True, exist_ok=False)
    assert sha(BATCH) == "86ad22303145a2efca1980dcc63678cb3192afcbd4dc9e3959e633a1ed02b79a"
    assert sha(BULK) == "9613083ec10d124ff6f0a009ec210e2a26ca7a9a4ec0ef4890653e11146e2331"
    argv = [str(PYTHON), "-m", "signalpost.cli", "run", "--organisations", str(BATCH),
            "--bulk", str(BULK), "--output", str(work / "envelopes.jsonl"),
            "--profiles-output", str(work / "profiles.jsonl"), "--report", str(work / "report.json"),
            "--run-id", f"r5-w3-seed-recall-{label}", "--expected-count", "100"]
    assert sum(arg.startswith("--") for arg in argv) == 7
    env = dict(ENV, SIGNALPOST_WEBSITE_SEEDS="1" if enabled else "0")
    started = time.monotonic()
    with (receipt / "execution.txt").open("w", encoding="utf8", newline="\n") as log:
        completed = subprocess.run(argv, cwd=work, env=env, stdout=log, stderr=subprocess.STDOUT,
                                   timeout=2100)
    wall = time.monotonic() - started
    sanitize_file(receipt / "execution.txt")
    assert completed.returncode == 0, (label, completed.returncode)
    checker = [str(PYTHON), str(ROOT / "scripts/check_live_run.py"), "--output",
                str(work / "envelopes.jsonl"), "--organisations", str(BATCH), "--state",
                str(work / "state"), "--report", str(work / "report.json"), "--site",
                str(work / "site"), "--count", "100"]
    result = subprocess.run(checker, cwd=ROOT, env=ENV, text=True, capture_output=True,
                            encoding="utf8", check=True)
    (receipt / "verification.txt").write_text(portable_text(result.stdout + result.stderr),
                                                encoding="utf8", newline="\n")
    verification = json.loads(result.stdout)
    save(receipt / "execution.json", {
        "label": label, "seeds_enabled": enabled, "argv": argv, "exactly_seven_flags": True,
        "cwd": work.as_posix(), "environment_override": "SIGNALPOST_WEBSITE_SEEDS=" + ("1" if enabled else "0"),
        "exit_code": completed.returncode, "wall_seconds": wall,
        "input_sha256": sha(BATCH), "bulk_sha256": sha(BULK),
        "envelopes_sha256": sha(work / "envelopes.jsonl"),
        "profiles_sha256": sha(work / "profiles.jsonl"), "report_sha256": sha(work / "report.json"),
        "verification": verification,
    })
    shutil.copyfile(work / "report.json", receipt / "report.json")
    sanitize_file(receipt / "report.json")
    print(json.dumps({"label": label, "wall_seconds": wall, "verification": verification}), flush=True)


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in {"on", "off"}:
        raise SystemExit("usage: run_seed_recall.py on|off")
    run(sys.argv[1] == "on")
