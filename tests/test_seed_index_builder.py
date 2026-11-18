import gzip
import json

from scripts.build_seed_index import capture_result, norwegian_blocks, read_captures, write_index


def test_reads_norwegian_boundary_block():
    lines = [
        "nl,one)/ x\tcdx-001.gz\t0\t100\t1",
        "no,one)/ x\tcdx-001.gz\t100\t100\t2",
        "nz,one)/ x\tcdx-001.gz\t200\t100\t3",
    ]
    assert list(norwegian_blocks(lines)) == [("cdx-001.gz", 0, 100), ("cdx-001.gz", 100, 100)]


def test_cdx_limits_capture_paths_and_sources():
    crawl = "CC-MAIN-2026-43"
    filename = f"crawl-data/{crawl}/segments/123.45/warc/CC-MAIN-test.warc.gz"
    urls = ["https://example.no/kontakt", "https://example.no/store", "https://proff.no/"]
    captures = [
        b"no,example)/ 20261001 " + json.dumps({
            "url": url, "mime-detected": "text/html", "status": "200",
            "filename": filename, "offset": "50", "length": "100",
        }).encode()
        for url in urls
    ]
    block = gzip.compress(b"\n".join(captures))
    assert list(read_captures(block, crawl)) == [(urls[0], "example.no", filename, 50, 100)]


def test_only_labelled_valid_numbers_become_nominations(tmp_path):
    url = "https://example.no/"
    header = (
        f"WARC/1.1\r\nWARC-Target-URI: {url}\r\nWARC-Date: 2026-10-06T03:00:00Z"
        "\r\n\r\nHTTP/1.1 200 OK\r\n\r\n"
    ).encode()
    body = (
        b"<html><footer><p>Org.nr: 991 853 995</p><p>912766349</p>"
        b"<p>Organisasjonsnummer: 123456789</p>"
        b'<p>Utviklet av <a href="https://design.no/">Design</a></p></footer></html>'
    )
    stamp, digest, labelled, observed, credits, portal = capture_result(gzip.compress(header + body), url)
    assert labelled == {"991853995"}
    assert observed == {"991853995", "912766349"}
    assert credits == {"design.no"}
    assert not portal
    output = tmp_path / "seeds.json.gz"
    write_index(output, [("991853995", "example.no", url, stamp, digest)], "commoncrawl", {})
    assert json.loads(gzip.decompress(output.read_bytes()))["entries"]["991853995"] == [
        ["example.no", url, "2026-10-06T03:00:00Z", digest]
    ]
