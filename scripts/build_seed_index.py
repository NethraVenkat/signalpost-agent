"""Build local website nominations from bulk CDXJ/WARC and an OSM PBF extract."""

import argparse
import gzip
import hashlib
import json
import re
import sqlite3
import time
from datetime import date, datetime, timezone
from io import BytesIO
from pathlib import Path
from urllib.parse import unquote, urlsplit

import httpx

from signalpost.identity.orgnr import normalize, valid
from signalpost.web.html import Page
from signalpost.web.policy import DIRECTORIES, FREE_MAIL, MARKETPLACES, SOCIAL, domain, normalize_url


DATA_HOST = "https://data.commoncrawl.org/"
BUILD_SECONDS = 4 * 60 * 60
PATH = re.compile(
    r"(?:(?:nb|nn|no|en)/)?(?:(?:kontakt(?:-oss)?|contact(?:-us)?|om(?:-oss)?|"
    r"about(?:-us)?|personvern(?:erklaering)?|privacy(?:-policy)?|"
    r"vilkar|vilkår|terms(?:-of-(?:use|service))?)(?:\.html?)?)?",
    re.I,
)
NUMBER = r"(?<!\d)(?:[0-9][ .\u00a0]?){8}[0-9](?!\d)"
LABELLED = re.compile(
    rf"\b(?:org\.?\s*nr\.?|organisasjonsnummer|foretaksregisteret|mva)"
    rf"\s*[:.#-]?\s*(?:NO\s*)?({NUMBER})|({NUMBER})\s*(?:MVA|Foretaksregisteret)\b",
    re.I,
)
CREDIT = re.compile(
    r"(?:utviklet|designet|levert|laget)\s+av|(?:designed|developed|powered)\s+by|"
    r"webdesign\s*[:–-]",
    re.I,
)
PORTAL = re.compile(r"\b(?:bedriftskatalog|bedriftssøk|company directory|business directory)\b", re.I)


class BuildDeadline(Exception):
    pass


class Downloads:
    def __init__(self, client, deadline):
        self.client = client
        self.deadline = deadline
        self.last_start = 0.0
        self.deferred = set()

    def check(self):
        if time.monotonic() >= self.deadline:
            raise BuildDeadline

    def chunks(self, path, byte_range=None):
        time.sleep(max(0, self.last_start + 1 - time.monotonic()))
        self.check()
        self.last_start = time.monotonic()
        headers = {}
        if byte_range:
            start, length = byte_range
            headers["Range"] = f"bytes={start}-{start + length - 1}"
        with self.client.stream("GET", DATA_HOST + path, headers=headers) as response:
            response.raise_for_status()
            if byte_range and (
                response.status_code != 206
                or not response.headers.get("Content-Range", "").startswith(
                    f"bytes {start}-{start + length - 1}/"
                )
            ):
                raise ValueError("Bulk server did not return the requested byte range")
            for chunk in response.iter_bytes(chunk_size=64 * 1024):
                self.check()
                yield chunk

    def read_range(self, path, offset, length):
        try:
            return b"".join(self.chunks(path, (offset, length)))
        except httpx.RequestError:
            time.sleep(2)
            return b"".join(self.chunks(path, (offset, length)))


def root_domain(value):
    try:
        url = normalize_url(value)
        root = domain(url) if url else ""
    except ValueError:
        return ""
    if not root or root in DIRECTORIES | FREE_MAIL | MARKETPLACES | SOCIAL:
        return ""
    return root


def norwegian_blocks(cluster):
    """A block immediately before the prefix may straddle its start."""
    previous = None
    for line in cluster:
        key, name, offset, length, _ = line.rstrip().split("\t")
        block = name, int(offset), int(length)
        if key.startswith(("no,", "no)")):
            if previous:
                yield previous
                previous = None
            yield block
        elif key >= "no-":
            break
        else:
            previous = block


def read_captures(block, crawl_id):
    for line in gzip.decompress(block).splitlines():
        key, _, raw = line.split(b" ", 2)
        if not key.startswith(b"no,"):
            continue
        record = json.loads(raw)
        if record.get("status") != "200" or record.get("mime-detected") != "text/html":
            continue
        url = record["url"]
        try:
            parts = urlsplit(url)
        except ValueError:
            continue
        if parts.query or not PATH.fullmatch(unquote(parts.path).strip("/")):
            continue
        root = root_domain(url)
        if not root.endswith(".no"):
            continue
        filename = record["filename"]
        if not re.fullmatch(rf"crawl-data/{crawl_id}/segments/[0-9.]+/warc/[\w.-]+\.warc\.gz", filename):
            continue
        offset, length = int(record["offset"]), int(record["length"])
        if 0 <= offset and 0 < length <= 512_000:
            yield url, root, filename, offset, length


def capture_result(member, url):
    # One gzip member contains a WARC record and the archived HTTP message.
    with gzip.GzipFile(fileobj=BytesIO(member)) as block:
        record = block.read(2_000_001)
    if len(record) > 2_000_000:
        return None
    warc, _, message = record.partition(b"\r\n\r\n")
    _, _, body = message.partition(b"\r\n\r\n")
    target = re.search(rb"(?im)^WARC-Target-URI: <?([^\r\n>]+)", warc)
    stamp = re.search(rb"(?im)^WARC-Date: ([0-9T:Z.-]+)", warc)
    if not body or not target or target[1].decode("utf-8", "replace") != url or not stamp:
        return None
    page = Page(body.removesuffix(b"\r\n\r\n"), url)
    numbers = {
        re.sub(r"\D", "", match[1] or match[2]) for match in LABELLED.finditer(page.visible)
    }
    labelled = set(filter(valid, numbers))
    observed = set(filter(valid, (
        re.sub(r"\D", "", match.group()) for match in re.finditer(NUMBER, page.visible)
    )))
    credit_names = {
        page.visible[match.end():match.end() + 80].lstrip().casefold()
        for match in CREDIT.finditer(page.visible)
    }
    credits = {
        root_domain(link.href) for link in page.links
        if CREDIT.search(link.text) or (
            link.text.strip()
            and any(name.startswith(link.text.strip().casefold()) for name in credit_names)
        )
    }
    return (
        stamp[1].decode("ascii"),
        hashlib.sha256(page.body).hexdigest(),
        labelled,
        observed | labelled,
        credits - {""},
        bool(PORTAL.search(page.title)),
    )


def crawl_index(db, downloads, directory, crawl_id):
    prefix = f"cc-index/collections/{crawl_id}/indexes/"
    cluster = directory / "cluster.idx"
    if not cluster.exists():
        partial = cluster.with_suffix(".part")
        with partial.open("wb") as stream:
            for chunk in downloads.chunks(prefix + "cluster.idx"):
                stream.write(chunk)
        partial.replace(cluster)
    with cluster.open(encoding="ascii") as lines:
        blocks = list(norwegian_blocks(lines))
    # Spread the first blocks across the namespace when the build is time-limited.
    blocks.sort(key=lambda block: hashlib.sha256(str(block).encode()).digest())
    for name, offset, length in blocks:
        if db.execute("SELECT 1 FROM blocks WHERE name=? AND offset=?", (name, offset)).fetchone():
            continue
        if not re.fullmatch(r"cdx-\d+\.gz", name) or not 0 < length <= 4_000_000:
            raise ValueError("Unexpected bulk index block")
        try:
            content = downloads.read_range(prefix + name, offset, length)
        except httpx.RequestError as exc:
            print(f"Index block deferred ({type(exc).__name__}): {name} at {offset}")
            continue
        with db:
            db.executemany("INSERT OR IGNORE INTO captures VALUES (?, ?, ?, ?, ?, 0)",
                           read_captures(content, crawl_id))
            db.execute("INSERT INTO blocks VALUES (?, ?)", (name, offset))
        scan_captures(db, downloads, capture_limit=8)


def scan_captures(db, downloads, capture_limit=-1):
    pending = db.execute("""
        SELECT url, root, filename, offset, length FROM (
            SELECT *, row_number() OVER (
                PARTITION BY root ORDER BY length(url), url
            ) AS position FROM captures WHERE done=0
        ) ORDER BY position, root
    """)
    checked = 0
    for url, root, filename, offset, length in pending:
        if url in downloads.deferred:
            continue
        try:
            member = downloads.read_range(filename, offset, length)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code not in {404, 410}:
                raise
            member = None
        except httpx.RequestError as exc:
            print(f"Archive record deferred ({type(exc).__name__}): {root}")
            downloads.deferred.add(url)
            continue
        result = None
        if member:
            try:
                result = capture_result(member, url)
            except (ValueError, EOFError, gzip.BadGzipFile) as exc:
                print(f"Archive record skipped ({type(exc).__name__}): {root}")
        with db:
            if result:
                stamp, digest, labelled, observed, credits, portal = result
                db.executemany("INSERT OR IGNORE INTO observed VALUES (?, ?)",
                               ((root, org) for org in observed))
                excluded = credits | ({root} if portal else set())
                db.executemany("INSERT OR IGNORE INTO excluded VALUES (?)", ((d,) for d in excluded))
                db.executemany("INSERT OR IGNORE INTO seeds VALUES (?, ?, ?, ?, ?)",
                               ((org, root, url, stamp, digest) for org in labelled))
            db.execute("UPDATE captures SET done=1 WHERE url=?", (url,))
        checked += 1
        if checked == capture_limit:
            break


def write_index(path, rows, source, provenance):
    entries = {}
    for org, root, *receipt in rows:
        entries.setdefault(org, []).append([root, *receipt])
    payload = {"version": 1, "source": source, "provenance": provenance, "entries": entries}
    partial = path.with_suffix(".part")
    partial.write_bytes(gzip.compress(json.dumps(payload, separators=(",", ":")).encode(), mtime=0))
    partial.replace(path)


def scan_osm(db, pbf, extract_date, downloads, output):
    import osmium

    digest = hashlib.sha256()
    with pbf.open("rb") as source:
        while chunk := source.read(1024 * 1024):
            downloads.check()
            digest.update(chunk)

    class Tags(osmium.SimpleHandler):
        def collect(self, obj):
            downloads.check()
            org = normalize(obj.tags.get("ref:NO:orgnr"))
            if valid(org) and (root := root_domain(obj.tags.get("website"))):
                db.execute("INSERT OR IGNORE INTO osm VALUES (?, ?)", (org, root))

        node = way = relation = collect

    try:
        with db:
            db.execute("DELETE FROM osm")
            filters = [osmium.filter.KeyFilter("ref:NO:orgnr"), osmium.filter.KeyFilter("website")]
            Tags().apply_file(str(pbf), filters=filters)
            downloads.check()
    except BuildDeadline:
        # A partial traversal cannot reliably detect overloaded domains.
        return
    rows = db.execute("""
        SELECT org, root FROM osm WHERE root NOT IN (
            SELECT root FROM osm GROUP BY root HAVING count(*) >= 3
        ) AND root NOT IN (SELECT root FROM excluded)
        AND root NOT IN (SELECT root FROM observed GROUP BY root HAVING count(*) >= 3)
        ORDER BY org, root
    """)
    write_index(output, rows, "openstreetmap", {
        "date": extract_date.isoformat(), "sha256": digest.hexdigest(),
        "extract": pbf.name,
        "attribution": "© OpenStreetMap contributors",
        "copyright": "https://www.openstreetmap.org/copyright",
        "license": "https://opendatacommons.org/licenses/odbl/1-0/",
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--crawl-id", default="CC-MAIN-2026-43")
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--osm-pbf", type=Path)
    parser.add_argument("--osm-date", type=date.fromisoformat)
    parser.add_argument("--seconds", type=int, default=BUILD_SECONDS)
    args = parser.parse_args()
    if not re.fullmatch(r"CC-MAIN-\d{4}-\d{2}", args.crawl_id):
        parser.error("Invalid crawl ID")
    if not 0 < args.seconds <= BUILD_SECONDS:
        parser.error("Build time must be between 1 and 14400 seconds")
    if args.osm_pbf and not args.osm_date:
        parser.error("--osm-pbf requires --osm-date")
    directory = args.work / args.crawl_id
    directory.mkdir(parents=True, exist_ok=True)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(directory / "progress.sqlite") as db, httpx.Client(
        timeout=8, headers={"User-Agent": "SignalpostSeedIndex/1.0"}
    ) as client:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS blocks (name, offset, PRIMARY KEY (name, offset));
            CREATE TABLE IF NOT EXISTS captures (url PRIMARY KEY, root, filename, offset, length, done);
            CREATE TABLE IF NOT EXISTS observed (root, org, PRIMARY KEY (root, org));
            CREATE TABLE IF NOT EXISTS excluded (root PRIMARY KEY);
            CREATE TABLE IF NOT EXISTS seeds (org, root, url, stamp, digest, PRIMARY KEY (org, root));
            CREATE TABLE IF NOT EXISTS osm (org, root, PRIMARY KEY (org, root));
            CREATE TABLE IF NOT EXISTS elapsed (seconds);
        """)
        used = db.execute("SELECT coalesce(sum(seconds), 0) FROM elapsed").fetchone()[0]
        start = time.monotonic()
        # Leave a small reserve for the final export and one bounded read.
        downloads = Downloads(client, start + min(args.seconds, BUILD_SECONDS - used) - 15)
        try:
            if args.osm_pbf:
                scan_osm(db, args.osm_pbf, args.osm_date, downloads, args.output_dir / "openstreetmap.json.gz")
            crawl_index(db, downloads, directory, args.crawl_id)
            scan_captures(db, downloads)
        except BuildDeadline:
            print("Build deadline reached. Exporting completed records.")
        finally:
            rows = db.execute("""
                SELECT org, root, url, stamp, digest FROM seeds WHERE root NOT IN (
                    SELECT root FROM observed GROUP BY root HAVING count(*) >= 3
                ) AND root NOT IN (SELECT root FROM excluded)
                ORDER BY org, root
            """)
            write_index(args.output_dir / "commoncrawl.json.gz", rows, "commoncrawl", {
                "crawl_id": args.crawl_id, "date": datetime.now(timezone.utc).date().isoformat(),
                "index_blocks_read": db.execute("SELECT count(*) FROM blocks").fetchone()[0],
                "captures_checked": db.execute("SELECT count(*) FROM captures WHERE done=1").fetchone()[0],
                "captures_pending": db.execute("SELECT count(*) FROM captures WHERE done=0").fetchone()[0],
            })
            db.execute("INSERT INTO elapsed VALUES (?)", (time.monotonic() - start,))
            db.commit()


if __name__ == "__main__":
    main()
