"""Extract only requested public registry records for reproducible fixtures."""
import argparse
import csv
import gzip
import json
from pathlib import Path
from signalpost.io.input_adapter import read


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--bulk", type=Path, required=True)
    p.add_argument("--batch", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    wanted = set(read(args.batch).unique)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    found = 0
    matched = set()
    with args.bulk.open("rb") as check:
        compressed = check.read(2) == b"\x1f\x8b"
    opener = gzip.open if compressed else open
    with opener(args.bulk, "rt", encoding="utf-8-sig", newline="") as f, args.output.open("w", encoding="utf8", newline="") as o:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(o, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            if row["organisasjonsnummer"] in wanted:
                writer.writerow(row)
                matched.add(row["organisasjonsnummer"])
                found += 1
                if found == len(wanted):
                    break
    print(json.dumps({"rows": found, "expected": len(wanted), "bytes": args.output.stat().st_size, "missing_organisation_numbers": sorted(wanted - matched)}))


if __name__ == "__main__":
    main()
