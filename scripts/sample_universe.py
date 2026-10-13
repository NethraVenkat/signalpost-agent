"""Hash-check the public corpus and uniformly sample with a fixed seed."""
import argparse
import gzip
import hashlib
import json
import random
from pathlib import Path

ARCHIVE_SHA = "1c89710e5b01f8617e86d09fbdff4a52f2f8dbbba297e74f7164b5984f5a0384"
CONTENT_SHA = "b82d6a3e7231d1759a958c282bc4366b80ec2fab8095053d8ed7fa9cd01bc838"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--universe", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20261013)
    args = parser.parse_args()
    with args.universe.open("rb") as f:
        archive_sha = hashlib.file_digest(f, "sha256").hexdigest()
    assert archive_sha == ARCHIVE_SHA, archive_sha
    sha, corpus = hashlib.sha256(), []
    with gzip.open(args.universe, "rb") as f:
        for line in f:
            sha.update(line)
            corpus.append(json.loads(line))
    assert sha.hexdigest() == CONTENT_SHA, sha.hexdigest()
    assert len(corpus) == 411160
    sample = random.Random(args.seed).sample(corpus, args.count)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps({"organisation_number": str(x["organisation_number"])}) + "\n" for x in sample), encoding="utf-8")
    print(json.dumps({"archive_sha256": archive_sha, "content_sha256": sha.hexdigest(), "rows": len(corpus), "sample_count": len(sample), "seed": args.seed, "sample_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest()}))


if __name__ == "__main__":
    main()
