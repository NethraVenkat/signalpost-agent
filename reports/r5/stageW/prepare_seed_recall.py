"""Prepare the disjoint, source-proportional seed-index cohort from frozen data."""

import csv
import gzip
import hashlib
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEST = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "reports/r5/final500"))
import qualify  # noqa: E402
from signalpost.identity.orgnr import valid  # noqa: E402

SEED = 20261122
COUNT = 100
UNIVERSE = ROOT / ".data/r5/inputs/universe-20261116/universe.jsonl.gz"
SNAPSHOT = ROOT / ".data/r5/inputs/brreg-enheter-20261116/enheter_2026-11-16T04-25-21.340365166.csv.gz"
SEEDS = ROOT / "src/signalpost/data/website_seeds"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    assert sha(UNIVERSE) == "1c89710e5b01f8617e86d09fbdff4a52f2f8dbbba297e74f7164b5984f5a0384"
    assert sha(SNAPSHOT) == "56922f51839e7ed3f3c9adde50dbcfa375202d7bc5aa998d9572158e228693e1"
    excluded_by_file, excluded = qualify.excluded_sample_numbers()
    present = set()
    with gzip.open(SNAPSHOT, "rt", encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            present.add(row["organisasjonsnummer"])
    pools = {}
    bundles = {}
    for name in ("commoncrawl", "openstreetmap"):
        path = SEEDS / f"{name}.json.gz"
        bundles[path.name] = sha(path)
        payload = json.loads(gzip.open(path, "rt", encoding="utf8").read())
        pools[name] = set(payload["entries"]) & present - excluded
    assert not pools["commoncrawl"] & pools["openstreetmap"]
    weights = {source: len(orgs) for source, orgs in pools.items()}
    raw = {source: COUNT * size / sum(weights.values()) for source, size in weights.items()}
    quotas = {source: int(value) for source, value in raw.items()}
    remainder = COUNT - sum(quotas.values())
    for source in sorted(raw, key=lambda key: raw[key] - quotas[key], reverse=True)[:remainder]:
        quotas[source] += 1
    rng = random.Random(SEED)
    selected = []
    for source in ("commoncrawl", "openstreetmap"):
        selected.extend((org, source) for org in rng.sample(sorted(pools[source]), quotas[source]))
    orgs = [org for org, _ in selected]
    assert len(orgs) == len(set(orgs)) == COUNT and not set(orgs) & excluded
    sample = DEST / "seed_recall_100.jsonl"
    sample.write_text("".join(json.dumps({"organisation_number": org}) + "\n" for org in orgs),
                       encoding="utf8", newline="\n")
    mapping = {org: source for org, source in selected}
    (DEST / "seed_recall_100_sources.json").write_text(
        json.dumps(mapping, indent=2) + "\n", encoding="utf8", newline="\n")
    draw = {
        "method": "Uniform without replacement within each source stratum; source quotas by largest remainder over seed-index organization numbers also present in the frozen registry snapshot after exclusion.",
        "random_seed": SEED, "count": COUNT, "source_quotas": quotas,
        "source_pool_sizes_after_exclusions": {k: len(v) for k, v in pools.items()},
        "source_pool_sizes_before_exclusions": {k: len(json.loads(gzip.open(SEEDS / f"{k}.json.gz", "rt").read())["entries"].keys() & present) for k in pools},
        "snapshot_rows": len(present), "registry_snapshot": {"path": SNAPSHOT.relative_to(ROOT).as_posix(), "sha256": sha(SNAPSHOT)},
        "universe": {"path": UNIVERSE.relative_to(ROOT).as_posix(), "sha256": sha(UNIVERSE)},
        "seed_bundles": bundles, "excluded_sample_unique_orgnr_count": len(excluded),
        "excluded_sample_files": excluded_by_file, "excluded_overlap": 0,
        "sample_sha256": sha(sample), "source_map_sha256": sha(DEST / "seed_recall_100_sources.json"),
    }
    (DEST / "seed_recall_draw.json").write_text(json.dumps(draw, indent=2) + "\n",
                                                encoding="utf8", newline="\n")
    print(json.dumps({"quotas": quotas, "eligible": draw["source_pool_sizes_after_exclusions"],
                      "excluded": len(excluded), "sample_sha256": draw["sample_sha256"]}))


if __name__ == "__main__":
    main()
