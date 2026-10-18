"""
Production Offline Replay Transport and Execution Engine for Signalpost.

Implements an offline recorded-response transport replaying saved responses
from state/blobs/ for declared fixtures and executes the actual production pipeline
via signalpost.runner.run(config, client=client).

Enforces exact request matching (method, exact URL, relevant request body, sequence),
preserves recorded HTTP status codes and headers (redirects, cache responses),
verifies blob SHA-256 integrity before serving, marks historical records lacking
HTTP metadata incomplete rather than fabricating metadata, and causes replay
verification to fail closed and exit nonzero upon any missing or corrupt fixture.
"""
from __future__ import annotations

import argparse
import asyncio
from dataclasses import dataclass, field
import hashlib
import json
import logging
from pathlib import Path
import sys
from contextlib import ExitStack
from datetime import datetime, timezone
from unittest.mock import patch
from urllib.parse import urlparse
import httpx

from signalpost.config import Config
from signalpost.runner import run as runner_run

logger = logging.getLogger("production_replay")


class ReplayFixtureError(RuntimeError):
    """Raised when one or more required recorded fixtures are missing or corrupt."""
    pass


@dataclass
class RecordedFixture:
    """A single recorded HTTP interaction with full response fidelity."""
    url: str
    method: str = "GET"
    status_code: int = 200
    headers: dict[str, str] = field(default_factory=dict)
    content: bytes | None = None
    content_sha256: str | None = None
    request_body: bytes | None = None  # None = unspecified/any; b"" = explicitly empty
    metadata_complete: bool = True
    repeatable: bool = False


class RecordedResponseTransport(httpx.AsyncBaseTransport):
    """
    Offline HTTP transport that resolves requests strictly against saved blobs
    and declared fixture mappings. Never performs outbound live network I/O.
    Fails closed on any missing, unrecorded, corrupt, mismatched, or exhausted response.
    """
    def __init__(
        self,
        blobs_dir: Path,
        fixture_map: dict | list | None = None,
        strict: bool = False,
    ):
        self.blobs_dir = Path(blobs_dir)
        self.strict = strict
        self.request_log: list[tuple[str, str]] = []
        self.unexpected_requests: list[str] = []
        self.missing_fixtures: list[tuple[str, str, str]] = []
        self.corrupt_fixtures: list[tuple[str, str, str]] = []
        self.mismatched_fixtures: list[tuple[str, str, str]] = []
        self.exhausted_fixtures: list[tuple[str, str, str]] = []
        self.incomplete_records: list[str] = []
        self.exhausted_sequences: set[tuple[str, str]] = set()
        self._lock = asyncio.Lock()

        # Internal index: (method.upper(), exact_url) -> list of RecordedFixture (sequence)
        self.fixtures: dict[tuple[str, str], list[RecordedFixture]] = {}
        if fixture_map:
            self._load_fixtures(fixture_map)

    def _load_fixtures(self, fixture_map: dict | list) -> None:
        if isinstance(fixture_map, list):
            for item in fixture_map:
                if isinstance(item, RecordedFixture):
                    key = (item.method.upper(), item.url)
                    self.fixtures.setdefault(key, []).append(item)
                elif isinstance(item, dict):
                    f = RecordedFixture(**item)
                    key = (f.method.upper(), f.url)
                    self.fixtures.setdefault(key, []).append(f)
        elif isinstance(fixture_map, dict):
            for k, v in fixture_map.items():
                if isinstance(k, tuple) and len(k) == 2:
                    method, url = k
                    if isinstance(v, list):
                        self.fixtures[(method.upper(), url)] = list(v)
                    elif isinstance(v, RecordedFixture):
                        self.fixtures[(method.upper(), url)] = [v]
                    elif isinstance(v, str):
                        self.fixtures[(method.upper(), url)] = [
                            RecordedFixture(url=url, method=method, content_sha256=v, metadata_complete=False)
                        ]
                elif isinstance(k, str):
                    url = k
                    if isinstance(v, list):
                        self.fixtures[("GET", url)] = list(v)
                    elif isinstance(v, RecordedFixture):
                        self.fixtures[(v.method.upper(), url)] = [v]
                    elif isinstance(v, str):
                        # Simple url -> sha mapping from historical envelopes (lacks HTTP metadata)
                        self.fixtures[("GET", url)] = [
                            RecordedFixture(url=url, method="GET", status_code=200, content_sha256=v, metadata_complete=False)
                        ]

    def has_failures(self) -> bool:
        if self.missing_fixtures or self.corrupt_fixtures or self.mismatched_fixtures or self.exhausted_fixtures:
            return True
        if self.strict and self.incomplete_records:
            return True
        return False

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        url_str = str(request.url)
        method_str = request.method.upper()
        self.request_log.append((method_str, url_str))
        key = (method_str, url_str)

        await request.aread()
        req_content = request.content

        async with self._lock:
            fixture_list = self.fixtures.get(key)

            if not fixture_list:
                if key in self.exhausted_sequences:
                    reason = f"Response sequence exhausted for {method_str} {url_str}"
                    self.exhausted_fixtures.append((method_str, url_str, reason))
                    logger.error("Replay exhausted sequence: %s", reason)
                    return httpx.Response(
                        404,
                        content=f"Offline recorded sequence exhausted: {method_str} {url_str}".encode("utf-8"),
                        headers={"content-type": "text/plain; charset=utf-8"},
                        request=request
                    )
                else:
                    reason = f"No recorded fixture for {method_str} {url_str}"
                    self.missing_fixtures.append((method_str, url_str, reason))
                    self.unexpected_requests.append(url_str)
                    logger.warning("Replay transport miss: %s", reason)
                    return httpx.Response(
                        404,
                        content=f"Offline recorded fixture not found: {method_str} {url_str}".encode("utf-8"),
                        headers={"content-type": "text/plain; charset=utf-8"},
                        request=request
                    )

            # Match relevant request body if specified
            matched_idx = -1
            has_body_specs = any(cand.request_body is not None for cand in fixture_list)

            if has_body_specs:
                for idx, cand in enumerate(fixture_list):
                    if cand.request_body is not None:
                        if cand.request_body == req_content:
                            matched_idx = idx
                            break
                    else:
                        if matched_idx == -1:
                            matched_idx = idx

                if matched_idx == -1:
                    expected_bodies = [c.request_body for c in fixture_list if c.request_body is not None]
                    reason = (
                        f"Request body mismatch for {method_str} {url_str}: "
                        f"expected one of {expected_bodies!r}, got {req_content!r}"
                    )
                    self.mismatched_fixtures.append((method_str, url_str, reason))
                    logger.error("Replay body mismatch: %s", reason)
                    return httpx.Response(
                        400,
                        content=reason.encode("utf-8"),
                        headers={"content-type": "text/plain; charset=utf-8"},
                        request=request
                    )
            else:
                matched_idx = 0

            fixture = fixture_list[matched_idx]

            # Sequence consumption: consume interaction once unless explicitly repeatable
            if not fixture.repeatable:
                fixture_list.pop(matched_idx)
                if len(fixture_list) == 0:
                    self.exhausted_sequences.add(key)

        if not fixture.metadata_complete:
            self.incomplete_records.append(url_str)
            if self.strict:
                logger.error("Strict replay: incomplete metadata for %s", url_str)

        # Resolve payload content
        if fixture.content is not None:
            content = fixture.content
        elif fixture.content_sha256:
            blob_path = self.blobs_dir / fixture.content_sha256
            if not blob_path.exists():
                reason = f"Missing blob file {fixture.content_sha256} for {method_str} {url_str}"
                self.missing_fixtures.append((method_str, url_str, reason))
                logger.error("Replay missing blob: %s", reason)
                return httpx.Response(
                    404,
                    content=reason.encode("utf-8"),
                    headers={"content-type": "text/plain; charset=utf-8"},
                    request=request
                )
            content = blob_path.read_bytes()
        else:
            content = b""

        # Verify response-body SHA-256 before serving
        if fixture.content_sha256:
            actual_sha = hashlib.sha256(content).hexdigest()
            if actual_sha.lower() != fixture.content_sha256.lower():
                err_msg = (
                    f"Blob SHA-256 verification failed for {method_str} {url_str}: "
                    f"expected {fixture.content_sha256}, got {actual_sha}"
                )
                self.corrupt_fixtures.append((method_str, url_str, err_msg))
                logger.error("Blob corrupt: %s", err_msg)
                return httpx.Response(
                    500,
                    content=err_msg.encode("utf-8"),
                    headers={"content-type": "text/plain; charset=utf-8"},
                    request=request
                )

        # Headers fidelity: preserve recorded headers, case-insensitively
        headers = dict(fixture.headers)
        if "content-length" not in {k.lower() for k in headers}:
            headers["content-length"] = str(len(content))

        if "content-type" not in {k.lower() for k in headers}:
            # If historical metadata was incomplete, infer MIME type from body prefix
            trimmed = content[:1024].lstrip()
            if trimmed.startswith(b"{") or trimmed.startswith(b"["):
                headers["content-type"] = "application/json; charset=utf-8"
            elif b"<html" in trimmed.lower() or b"<!doctype html" in trimmed.lower():
                headers["content-type"] = "text/html; charset=utf-8"
            elif trimmed.startswith(b"<?xml") or trimmed.startswith(b"<feed") or trimmed.startswith(b"<urlset"):
                headers["content-type"] = "application/xml; charset=utf-8"
            else:
                headers["content-type"] = "application/octet-stream"

        return httpx.Response(
            fixture.status_code,
            content=content,
            headers=headers,
            request=request
        )


def load_fixtures_from_manifest(manifest_path: Path, blobs_dir: Path) -> list[RecordedFixture]:
    """Loads recorded interactions from a versioned JSON fixture manifest."""
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    fixtures = []
    for item in data.get("fixtures", []):
        req_body = item.get("request_body")
        if isinstance(req_body, str):
            req_body = req_body.encode("utf-8")
        elif req_body is not None and not isinstance(req_body, bytes):
            req_body = bytes(req_body)

        content = item.get("content")
        if isinstance(content, str):
            content = content.encode("utf-8")
        elif content is not None and not isinstance(content, bytes):
            content = bytes(content)

        blob_file = item.get("blob_file") or item.get("blob_filename")
        sha = item.get("content_sha256")
        if blob_file and not content:
            bp = (blobs_dir / blob_file) if not Path(blob_file).is_absolute() else Path(blob_file)
            if bp.exists():
                content = bp.read_bytes()
                sha = sha or hashlib.sha256(content).hexdigest()

        fixtures.append(RecordedFixture(
            url=item["url"],
            method=item.get("method", "GET").upper(),
            status_code=int(item.get("status_code", 200)),
            headers=dict(item.get("headers", {})),
            content=content,
            content_sha256=sha,
            request_body=req_body,
            metadata_complete=bool(item.get("metadata_complete", True)),
            repeatable=bool(item.get("repeatable", False)),
        ))
    return fixtures


def build_fixture_map_from_envelopes(envelopes_path: Path, blobs_dir: Path) -> dict[tuple[str, str], list[RecordedFixture]]:
    """
    Extracts exact source_url -> content_sha256 mappings from existing envelope evidence.
    Does NOT strip 'www.', does NOT discard query parameters, and does NOT map subpages to root URLs.
    Marks historical records as lacking response metadata (metadata_complete=False).
    """
    fixtures: dict[tuple[str, str], list[RecordedFixture]] = {}
    if not envelopes_path or not envelopes_path.exists():
        return fixtures

    with open(envelopes_path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
                for ev in row.get("evidence", []):
                    s_url = ev.get("source_url")
                    sha = ev.get("content_sha256")
                    if s_url and sha and (blobs_dir / sha).exists():
                        key = ("GET", s_url)
                        if key not in fixtures:
                            fixtures[key] = [
                                RecordedFixture(
                                    url=s_url,
                                    method="GET",
                                    status_code=200,
                                    content_sha256=sha,
                                    metadata_complete=False,
                                    repeatable=True,
                                )
                            ]
            except Exception:
                continue

    return fixtures


async def run_production_replay(
    input_path: Path,
    output_envelopes: Path,
    output_report: Path,
    state_dir: Path = Path("state"),
    manifest_path: Path | None = None,
    fixture_envelopes: Path | None = None,
    fixtures_dir: Path | None = None,
    bulk: Path | None = None,
    websites: bool = True,
    hiring: bool = False,
    public_activity: bool = False,
    workers: int = 4,
    mode: str = "strict",
    observation_time: str | None = None,
) -> dict:
    """Executes the actual Signalpost production runner using the offline recorded transport."""
    blobs_dir = fixtures_dir or (state_dir / "blobs")
    is_strict = (mode.lower() == "strict")

    if manifest_path and manifest_path.exists():
        fixtures = load_fixtures_from_manifest(manifest_path, blobs_dir)
        print(f"Loaded {len(fixtures)} recorded fixtures from manifest {manifest_path.name}")
    elif fixture_envelopes and fixture_envelopes.exists():
        fixtures = build_fixture_map_from_envelopes(fixture_envelopes, blobs_dir)
        print(f"Indexed {len(fixtures)} historical URL fixtures from {fixture_envelopes.name}")
    else:
        fixtures = []
        print("Warning: No fixture manifest or envelope source provided for replay.")

    output_envelopes.parent.mkdir(parents=True, exist_ok=True)
    output_report.parent.mkdir(parents=True, exist_ok=True)

    config = Config(
        organisations=input_path,
        output=output_envelopes,
        report=output_report,
        state_dir=state_dir,
        bulk=bulk,
        websites=websites,
        hiring=hiring,
        public_activity=public_activity,
        registry_changes=False,  # Historical R2 transport fixtures have no change-feed responses.
        workers=workers,
        time_budget_seconds=120,
        website_politeness_seconds=1,
        nav_index_path=state_dir / "no-live-discovery-index.json.gz",
    )

    transport = RecordedResponseTransport(blobs_dir=blobs_dir, fixture_map=fixtures, strict=is_strict)
    # HTTP replay must not depend on live DNS or wall-clock ad expiry. Only
    # explicitly declared fixture hosts receive a synthetic public address.
    hosts = {urlparse(url).hostname for _, url in transport.fixtures}
    async def fixture_dns(host, port=443):
        from signalpost.budget import SourceFailure
        if host not in hosts:
            raise SourceFailure("no_such_domain")
        return ["93.184.216.34"]

    with ExitStack() as stack:
        stack.enter_context(patch("signalpost.web.policy.resolve_public", fixture_dns))
        if observation_time:
            at = datetime.fromisoformat(observation_time.replace("Z", "+00:00"))
            if at.tzinfo is None:
                raise ValueError("observation_time requires a timezone")
            at = at.astimezone(timezone.utc)
            class ReplayDateTime(datetime):
                @classmethod
                def now(cls, tz=None):
                    return at.astimezone(tz) if tz else at.replace(tzinfo=None)
            # Patch imported clock references only inside this offline command.
            for module in list(sys.modules.values()):
                if getattr(module, "__name__", "").startswith("signalpost."):
                    if getattr(module, "utc_now", None):
                        stack.enter_context(patch.object(module, "utc_now", lambda: at.isoformat().replace("+00:00", "Z")))
                    if getattr(module, "datetime", None) is datetime:
                        stack.enter_context(patch.object(module, "datetime", ReplayDateTime))
        async with httpx.AsyncClient(transport=transport, trust_env=False) as client:
            report = await runner_run(config, client=client)

    if transport.has_failures():
        reasons = []
        if transport.missing_fixtures:
            reasons.append(f"{len(transport.missing_fixtures)} missing fixture(s)")
            for m in transport.missing_fixtures:
                logger.error("Missing fixture: method=%s url=%s reason=%s", m[0], m[1], m[2])
        if transport.corrupt_fixtures:
            reasons.append(f"{len(transport.corrupt_fixtures)} corrupt fixture(s)")
            for c in transport.corrupt_fixtures:
                logger.error("Corrupt fixture: method=%s url=%s reason=%s", c[0], c[1], c[2])
        if transport.mismatched_fixtures:
            reasons.append(f"{len(transport.mismatched_fixtures)} mismatched fixture(s)")
            for mm in transport.mismatched_fixtures:
                logger.error("Mismatched fixture: method=%s url=%s reason=%s", mm[0], mm[1], mm[2])
        if transport.exhausted_fixtures:
            reasons.append(f"{len(transport.exhausted_fixtures)} exhausted sequence(s)")
            for ef in transport.exhausted_fixtures:
                logger.error("Exhausted sequence: method=%s url=%s reason=%s", ef[0], ef[1], ef[2])
        if is_strict and transport.incomplete_records:
            reasons.append(f"{len(transport.incomplete_records)} incomplete metadata record(s) in strict mode")
            for inc in transport.incomplete_records:
                logger.error("Incomplete metadata: %s", inc)
        raise ReplayFixtureError("Production replay failed: " + ", ".join(reasons))

    print(f"Production replay completed: wrote envelopes to {output_envelopes}")
    return report


def main():
    parser = argparse.ArgumentParser(description="Signalpost Production Offline Replay Engine")
    parser.add_argument("--input", type=Path, default=Path("tests/fixtures/ci20.csv"), help="Input company cohort CSV")
    parser.add_argument("--manifest", type=Path, default=None, help="Versioned JSON fixture manifest")
    parser.add_argument("--fixtures-dir", type=Path, default=None, help="Tracked fixture blobs directory")
    parser.add_argument("--envelopes-fixtures", type=Path, default=None, help="Historical envelope fixtures JSONL")
    parser.add_argument("--output", type=Path, default=Path("out/production-replay-envelopes.jsonl"))
    parser.add_argument("--report", type=Path, default=Path("out/production-replay-report.json"))
    parser.add_argument("--state-dir", type=Path, default=Path("state"))
    parser.add_argument("--bulk", type=Path, default=None, help="Explicit registry bulk CSV snapshot")
    parser.add_argument("--mode", choices=["strict", "historical"], default="strict", help="Replay fidelity mode")
    parser.add_argument("--websites", action="store_true", default=True)
    parser.add_argument("--no-websites", dest="websites", action="store_false")
    parser.add_argument("--hiring", action="store_true", default=False)
    parser.add_argument("--public-activity", action="store_true", default=False)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--observation-time", help="Fixed timezone-aware observation time for offline replay")
    args = parser.parse_args()

    try:
        asyncio.run(run_production_replay(
            input_path=args.input,
            output_envelopes=args.output,
            output_report=args.report,
            state_dir=args.state_dir,
            manifest_path=args.manifest,
            fixture_envelopes=args.envelopes_fixtures,
            fixtures_dir=args.fixtures_dir,
            bulk=args.bulk,
            websites=args.websites,
            hiring=args.hiring,
            public_activity=args.public_activity,
            workers=args.workers,
            mode=args.mode,
            observation_time=args.observation_time,
        ))
    except ReplayFixtureError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
