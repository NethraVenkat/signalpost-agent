"""
Tests proving the production offline replay transport fidelity and runner execution.
Covers regression cases for:
- Missing accounts/subunits (fails closed without fabricating empty lists)
- Query collisions (different query parameters do not collide)
- WWW differences (www.example.no != example.no)
- Homepage / subpage confusion (/ != /subpage)
- Wrong methods (POST != GET)
- Corrupt hashes (SHA-256 verification catches mismatch and rejects)
- Non-200 responses (status code and headers preserved)
- Redirects (301/302 and Location header preserved)
- Runner replay exits nonzero on missing fixtures
"""
import asyncio
import hashlib
import json
import pytest
from pathlib import Path
import httpx

from scripts.production_replay import (
    RecordedResponseTransport,
    RecordedFixture,
    ReplayFixtureError,
    build_fixture_map_from_envelopes,
    run_production_replay,
)
from signalpost.config import Config
from signalpost.runner import run as runner_run


def test_recorded_response_transport_serves_blobs(tmp_path):
    blobs_dir = tmp_path / "blobs"
    blobs_dir.mkdir(parents=True)
    body_bytes = json.dumps({"organisasjonsnummer": "999592236", "navn": "TEST AS"}).encode("utf-8")
    blob_sha = hashlib.sha256(body_bytes).hexdigest()
    (blobs_dir / blob_sha).write_bytes(body_bytes)

    robots_bytes = b"User-agent: *\nDisallow: /admin\n"
    robots_sha = hashlib.sha256(robots_bytes).hexdigest()
    (blobs_dir / robots_sha).write_bytes(robots_bytes)

    fixture_map = {
        "https://data.brreg.no/enhetsregisteret/api/enheter/999592236": blob_sha,
        "https://example.no/robots.txt": robots_sha,
    }
    transport = RecordedResponseTransport(blobs_dir, fixture_map)

    async def check():
        async with httpx.AsyncClient(transport=transport) as client:
            # 1. Recorded Robots.txt served faithfully
            r_robots = await client.get("https://example.no/robots.txt")
            assert r_robots.status_code == 200
            assert "Disallow: /admin" in r_robots.text

            # 2. Known fixture
            r_fixture = await client.get("https://data.brreg.no/enhetsregisteret/api/enheter/999592236")
            assert r_fixture.status_code == 200
            data = r_fixture.json()
            assert data["navn"] == "TEST AS"

            # 3. Unknown URL fails closed
            r_unknown = await client.get("https://evil.test/unrecorded")
            assert r_unknown.status_code == 404
            assert "https://evil.test/unrecorded" in transport.unexpected_requests
            assert any(m[1] == "https://evil.test/unrecorded" for m in transport.missing_fixtures)

    asyncio.run(check())


def test_missing_accounts_and_subunits_fail_closed(tmp_path):
    """Proves missing accounts and subunit requests do NOT return fabricated empty responses."""
    blobs_dir = tmp_path / "blobs"
    blobs_dir.mkdir(parents=True)
    transport = RecordedResponseTransport(blobs_dir, {})

    async def check():
        async with httpx.AsyncClient(transport=transport) as client:
            r_subunits = await client.get("https://data.brreg.no/enhetsregisteret/api/underenheter?overordnetEnhet=999592236")
            assert r_subunits.status_code == 404
            assert b"empty_subunits" not in r_subunits.content
            assert b"_embedded" not in r_subunits.content

            r_accounts = await client.get("https://data.brreg.no/regnskapsregisteret/regnskap/999592236")
            assert r_accounts.status_code == 404
            assert r_accounts.content != b"[]"

            assert len(transport.missing_fixtures) == 2

    asyncio.run(check())


def test_query_collisions_rejected(tmp_path):
    """Proves different query parameters do NOT collide or match each other."""
    blobs_dir = tmp_path / "blobs"
    blobs_dir.mkdir(parents=True)

    page1_content = b'{"page": 1, "data": ["item1"]}'
    sha1 = hashlib.sha256(page1_content).hexdigest()
    (blobs_dir / sha1).write_bytes(page1_content)

    fixture_map = {
        "https://example.no/api?page=1": sha1
    }
    transport = RecordedResponseTransport(blobs_dir, fixture_map)

    async def check():
        async with httpx.AsyncClient(transport=transport) as client:
            r1 = await client.get("https://example.no/api?page=1")
            assert r1.status_code == 200
            assert r1.json()["page"] == 1

            # Request for page=2 must NOT match page=1
            r2 = await client.get("https://example.no/api?page=2")
            assert r2.status_code == 404
            assert any("page=2" in m[1] for m in transport.missing_fixtures)

            # Request without query must NOT match page=1
            r_bare = await client.get("https://example.no/api")
            assert r_bare.status_code == 404

    asyncio.run(check())


def test_www_differences_rejected(tmp_path):
    """Proves www.example.no and example.no are treated as distinct exact URLs."""
    blobs_dir = tmp_path / "blobs"
    blobs_dir.mkdir(parents=True)

    content = b"<html><body>Welcome to example.no</body></html>"
    sha = hashlib.sha256(content).hexdigest()
    (blobs_dir / sha).write_bytes(content)

    fixture_map = {
        "https://example.no/": sha
    }
    transport = RecordedResponseTransport(blobs_dir, fixture_map)

    async def check():
        async with httpx.AsyncClient(transport=transport) as client:
            # Naked domain matches
            r1 = await client.get("https://example.no/")
            assert r1.status_code == 200

            # www. variant does NOT match and fails closed
            r_www = await client.get("https://www.example.no/")
            assert r_www.status_code == 404
            assert any("www.example.no" in m[1] for m in transport.missing_fixtures)

    asyncio.run(check())


def test_subpage_homepage_confusion_rejected(tmp_path):
    """Proves root URLs do NOT automatically alias or serve subpages like /om-oss."""
    blobs_dir = tmp_path / "blobs"
    blobs_dir.mkdir(parents=True)

    root_content = b"<html><head><title>Home</title></head><body>Home</body></html>"
    root_sha = hashlib.sha256(root_content).hexdigest()
    (blobs_dir / root_sha).write_bytes(root_content)

    fixture_map = {
        "https://example.no/": root_sha
    }
    transport = RecordedResponseTransport(blobs_dir, fixture_map)

    async def check():
        async with httpx.AsyncClient(transport=transport) as client:
            r_root = await client.get("https://example.no/")
            assert r_root.status_code == 200

            # Subpage /om-oss must NOT match root URL
            r_sub = await client.get("https://example.no/om-oss")
            assert r_sub.status_code == 404
            assert any("/om-oss" in m[1] for m in transport.missing_fixtures)

    asyncio.run(check())


def test_wrong_method_rejected(tmp_path):
    """Proves POST request does NOT match recorded GET response."""
    blobs_dir = tmp_path / "blobs"
    blobs_dir.mkdir(parents=True)

    content = b'{"status": "ok"}'
    sha = hashlib.sha256(content).hexdigest()
    (blobs_dir / sha).write_bytes(content)

    fixtures = [
        RecordedFixture(url="https://example.no/submit", method="GET", content_sha256=sha)
    ]
    transport = RecordedResponseTransport(blobs_dir, fixtures)

    async def check():
        async with httpx.AsyncClient(transport=transport) as client:
            r_get = await client.get("https://example.no/submit")
            assert r_get.status_code == 200

            r_post = await client.post("https://example.no/submit", json={"key": "val"})
            assert r_post.status_code == 404
            assert any(m[0] == "POST" and "https://example.no/submit" in m[1] for m in transport.missing_fixtures)

    asyncio.run(check())


def test_corrupt_hash_rejected(tmp_path):
    """Proves response-body SHA-256 verification catches corrupt blobs and fails closed."""
    blobs_dir = tmp_path / "blobs"
    blobs_dir.mkdir(parents=True)

    # Expected SHA vs actual content mismatch
    claimed_sha = "1111222233334444555566667777888899990000aaaabbbbccccddddeeeeffff"
    corrupt_content = b"TAMPERED CONTENT IN STORAGE"
    (blobs_dir / claimed_sha).write_bytes(corrupt_content)

    fixture_map = {
        "https://example.no/data": claimed_sha
    }
    transport = RecordedResponseTransport(blobs_dir, fixture_map)

    async def check():
        async with httpx.AsyncClient(transport=transport) as client:
            r = await client.get("https://example.no/data")
            assert r.status_code == 500
            assert b"Blob SHA-256 verification failed" in r.content
            assert len(transport.corrupt_fixtures) == 1
            assert "verification failed" in transport.corrupt_fixtures[0][2]

    asyncio.run(check())


def test_non_200_response_and_headers_preserved(tmp_path):
    """Proves non-200 responses (e.g. 404, 503) and custom headers are faithfully served."""
    blobs_dir = tmp_path / "blobs"
    blobs_dir.mkdir(parents=True)

    err_body = b"Rate limit exceeded. Please back off."
    sha = hashlib.sha256(err_body).hexdigest()
    (blobs_dir / sha).write_bytes(err_body)

    fixtures = [
        RecordedFixture(
            url="https://example.no/api/limited",
            method="GET",
            status_code=429,
            headers={"retry-after": "120", "content-type": "text/plain; charset=utf-8"},
            content_sha256=sha,
            metadata_complete=True,
        )
    ]
    transport = RecordedResponseTransport(blobs_dir, fixtures)

    async def check():
        async with httpx.AsyncClient(transport=transport) as client:
            r = await client.get("https://example.no/api/limited")
            assert r.status_code == 429
            assert r.headers["retry-after"] == "120"
            assert "Rate limit exceeded" in r.text

    asyncio.run(check())


def test_redirects_and_location_header_preserved(tmp_path):
    """Proves 301/302 redirects and Location headers are faithfully served."""
    blobs_dir = tmp_path / "blobs"
    blobs_dir.mkdir(parents=True)

    fixtures = [
        RecordedFixture(
            url="https://example.no/old-page",
            method="GET",
            status_code=301,
            headers={"location": "https://example.no/new-page"},
            content=b"",
            metadata_complete=True,
            repeatable=True,
        ),
        RecordedFixture(
            url="https://example.no/new-page",
            method="GET",
            status_code=200,
            headers={"content-type": "text/html"},
            content=b"<html><body>New Page</body></html>",
            metadata_complete=True,
            repeatable=True,
        )
    ]
    transport = RecordedResponseTransport(blobs_dir, fixtures)

    async def check():
        async with httpx.AsyncClient(transport=transport, follow_redirects=False) as client:
            r = await client.get("https://example.no/old-page")
            assert r.status_code == 301
            assert r.headers["location"] == "https://example.no/new-page"

        async with httpx.AsyncClient(transport=transport, follow_redirects=True) as client:
            r_followed = await client.get("https://example.no/old-page")
            assert r_followed.status_code == 200
            assert "New Page" in r_followed.text

    asyncio.run(check())


def test_production_replay_exits_nonzero_on_missing_fixture(tmp_path):
    """Proves missing fixture causes run_production_replay to raise ReplayFixtureError."""
    blobs_dir = tmp_path / "blobs"
    blobs_dir.mkdir(parents=True)

    input_file = tmp_path / "input.txt"
    input_file.write_text("999592236\n", encoding="utf-8")

    # Empty fixture map -> request for 999592236 will be missing!
    empty_fixtures_envelopes = tmp_path / "empty_env.jsonl"
    empty_fixtures_envelopes.write_text("", encoding="utf-8")

    out_env = tmp_path / "out.jsonl"
    out_rep = tmp_path / "rep.json"

    with pytest.raises(ReplayFixtureError) as exc_info:
        asyncio.run(run_production_replay(
            input_path=input_file,
            output_envelopes=out_env,
            output_report=out_rep,
            state_dir=tmp_path,
            fixture_envelopes=empty_fixtures_envelopes,
            websites=False,
            hiring=False,
            workers=1
        ))

    assert "missing fixture" in str(exc_info.value).lower()


def test_replay_single_fixture_body_mismatch_fails_closed(tmp_path):
    """Proves single fixture with request_body requirement fails closed on mismatched request body."""
    blobs_dir = tmp_path / "blobs"
    blobs_dir.mkdir(parents=True)

    fixtures = [
        RecordedFixture(
            url="https://example.no/api/query",
            method="POST",
            request_body=b'{"org": "999592236"}',
            status_code=200,
            content=b'{"result": "success"}',
            metadata_complete=True,
        )
    ]
    transport = RecordedResponseTransport(blobs_dir, fixtures)

    async def check():
        async with httpx.AsyncClient(transport=transport) as client:
            # 1. Mismatched body fails closed (never falls back)
            r_bad = await client.post("https://example.no/api/query", content=b'{"org": "888888888"}')
            assert r_bad.status_code in (400, 404)
            assert len(transport.mismatched_fixtures) > 0

            # 2. Matching body succeeds
            r_ok = await client.post("https://example.no/api/query", content=b'{"org": "999592236"}')
            assert r_ok.status_code == 200

    asyncio.run(check())


def test_replay_multiple_fixture_body_mismatch_fails_closed(tmp_path):
    """Proves multiple body-specific fixtures reject unrecorded request body without fallback."""
    blobs_dir = tmp_path / "blobs"
    blobs_dir.mkdir(parents=True)

    fixtures = [
        RecordedFixture(
            url="https://example.no/api/search",
            method="POST",
            request_body=b'{"query": "alpha"}',
            status_code=200,
            content=b'{"results": ["alpha"]}',
            metadata_complete=True,
        ),
        RecordedFixture(
            url="https://example.no/api/search",
            method="POST",
            request_body=b'{"query": "beta"}',
            status_code=200,
            content=b'{"results": ["beta"]}',
            metadata_complete=True,
        )
    ]
    transport = RecordedResponseTransport(blobs_dir, fixtures)

    async def check():
        async with httpx.AsyncClient(transport=transport) as client:
            r_gamma = await client.post("https://example.no/api/search", content=b'{"query": "gamma"}')
            assert r_gamma.status_code in (400, 404)
            assert len(transport.mismatched_fixtures) > 0

    asyncio.run(check())


def test_replay_empty_body_distinction(tmp_path):
    """Proves explicit empty body (b'') is distinguished from unspecified body (None)."""
    blobs_dir = tmp_path / "blobs"
    blobs_dir.mkdir(parents=True)

    fixtures = [
        # Explicit empty body
        RecordedFixture(
            url="https://example.no/api/empty-only",
            method="POST",
            request_body=b"",
            status_code=200,
            content=b"ok",
            metadata_complete=True,
            repeatable=True,
        ),
        # Unspecified body (matches any)
        RecordedFixture(
            url="https://example.no/api/any-body",
            method="POST",
            request_body=None,
            status_code=200,
            content=b"any_ok",
            metadata_complete=True,
            repeatable=True,
        )
    ]
    transport = RecordedResponseTransport(blobs_dir, fixtures)

    async def check():
        async with httpx.AsyncClient(transport=transport) as client:
            # 1. Empty body to empty-only succeeds
            r1 = await client.post("https://example.no/api/empty-only", content=b"")
            assert r1.status_code == 200

            # 2. Non-empty body to empty-only fails closed
            r2 = await client.post("https://example.no/api/empty-only", content=b"payload")
            assert r2.status_code in (400, 404)

            # 3. Any body to any-body succeeds
            r3 = await client.post("https://example.no/api/any-body", content=b"payload")
            assert r3.status_code == 200

    asyncio.run(check())


def test_replay_sequence_429_followed_by_200(tmp_path):
    """Proves sequential interactions: 429 rate limit followed by 200 success."""
    blobs_dir = tmp_path / "blobs"
    blobs_dir.mkdir(parents=True)

    fixtures = [
        RecordedFixture(
            url="https://example.no/api/stream",
            method="GET",
            status_code=429,
            headers={"retry-after": "1"},
            content=b"rate limited",
            metadata_complete=True,
        ),
        RecordedFixture(
            url="https://example.no/api/stream",
            method="GET",
            status_code=200,
            content=b"stream data",
            metadata_complete=True,
        )
    ]
    transport = RecordedResponseTransport(blobs_dir, fixtures)

    async def check():
        async with httpx.AsyncClient(transport=transport) as client:
            r1 = await client.get("https://example.no/api/stream")
            assert r1.status_code == 429

            r2 = await client.get("https://example.no/api/stream")
            assert r2.status_code == 200
            assert r2.content == b"stream data"

    asyncio.run(check())


def test_replay_exhausted_sequence_fails_closed(tmp_path):
    """Proves exhausting a response sequence fails closed with exhausted_sequence error."""
    blobs_dir = tmp_path / "blobs"
    blobs_dir.mkdir(parents=True)

    fixtures = [
        RecordedFixture(
            url="https://example.no/api/once",
            method="GET",
            status_code=200,
            content=b"single use",
            metadata_complete=True,
            repeatable=False,
        )
    ]
    transport = RecordedResponseTransport(blobs_dir, fixtures)

    async def check():
        async with httpx.AsyncClient(transport=transport) as client:
            r1 = await client.get("https://example.no/api/once")
            assert r1.status_code == 200

            # Second call must NOT silently repeat; must fail closed
            r2 = await client.get("https://example.no/api/once")
            assert r2.status_code == 404
            assert len(transport.exhausted_fixtures) > 0

    asyncio.run(check())


def test_replay_repeatable_fixture_reusable(tmp_path):
    """Proves explicit repeatable=True fixtures can be reused without exhaustion."""
    blobs_dir = tmp_path / "blobs"
    blobs_dir.mkdir(parents=True)

    fixtures = [
        RecordedFixture(
            url="https://example.no/robots.txt",
            method="GET",
            status_code=200,
            content=b"User-agent: *\nAllow: /",
            metadata_complete=True,
            repeatable=True,
        )
    ]
    transport = RecordedResponseTransport(blobs_dir, fixtures)

    async def check():
        async with httpx.AsyncClient(transport=transport) as client:
            for _ in range(5):
                r = await client.get("https://example.no/robots.txt")
                assert r.status_code == 200
            assert len(transport.exhausted_fixtures) == 0

    asyncio.run(check())


def test_replay_concurrent_requests_no_duplicate_consumption(tmp_path):
    """Proves concurrent requests to sequential fixtures consume items safely without race conditions."""
    blobs_dir = tmp_path / "blobs"
    blobs_dir.mkdir(parents=True)

    fixtures = [
        RecordedFixture(url="https://example.no/seq", method="GET", status_code=200, content=f"item_{i}".encode(), metadata_complete=True)
        for i in range(10)
    ]
    transport = RecordedResponseTransport(blobs_dir, fixtures)

    async def check():
        async with httpx.AsyncClient(transport=transport) as client:
            tasks = [client.get("https://example.no/seq") for _ in range(10)]
            responses = await asyncio.gather(*tasks)
            assert all(r.status_code == 200 for r in responses)
            contents = {r.content.decode() for r in responses}
            assert len(contents) == 10  # Each consumed exactly once!

    asyncio.run(check())


def test_replay_strict_mode_fails_on_incomplete_metadata(tmp_path):
    """Proves strict mode exits nonzero when required fixtures have incomplete metadata."""
    blobs_dir = tmp_path / "blobs"
    blobs_dir.mkdir(parents=True)

    fixtures = [
        RecordedFixture(
            url="https://example.no/api/incomplete",
            method="GET",
            content=b"data",
            metadata_complete=False,  # Historical extraction without full HTTP status/headers
        )
    ]
    transport = RecordedResponseTransport(blobs_dir, fixtures, strict=True)

    async def check():
        async with httpx.AsyncClient(transport=transport) as client:
            r = await client.get("https://example.no/api/incomplete")
            # In strict mode, accessing incomplete record must trigger failure
            assert transport.incomplete_records
            assert transport.has_failures()

    asyncio.run(check())
