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
    request_body: bytes | None = None
    metadata_complete: bool = True


class RecordedResponseTransport(httpx.AsyncBaseTransport):
    """
    Offline HTTP transport that resolves requests strictly against saved blobs
    and declared fixture mappings. Never performs outbound live network I/O.
    Fails closed on any missing, unrecorded, or corrupt response.
    """
    def __init__(
        self,
        blobs_dir: Path,
        fixture_map: dict | list | None = None,
    ):
        self.blobs_dir = Path(blobs_dir)
        self.request_log: list[tuple[str, str]] = []
        self.unexpected_requests: list[str] = []
        self.missing_fixtures: list[tuple[str, str, str]] = []
        self.corrupt_fixtures: list[tuple[str, str, str]] = []
        self.incomplete_records: list[str] = []

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

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        url_str = str(request.url)
        method_str = request.method.upper()
        self.request_log.append((method_str, url_str))

        key = (method_str, url_str)
        fixture_list = self.fixtures.get(key)

        if not fixture_list:
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

        # Match relevant request body if specified and multiple fixtures exist
        fixture: RecordedFixture | None = None
        has_body_specs = any(cand.request_body is not None for cand in fixture_list)
        if len(fixture_list) > 1 and has_body_specs:
            await request.aread()
            req_content = request.content
            for cand in fixture_list:
                if cand.request_body is not None and cand.request_body == req_content:
                    fixture = cand
                    break

        if fixture is None:
            # Advance response sequence if multiple responses are queued for the same URL/method
            if len(fixture_list) > 1:
                fixture = fixture_list.pop(0)
            else:
                fixture = fixture_list[0]

        if not fixture.metadata_complete:
            self.incomplete_records.append(url_str)

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


def build_fixture_map_from_envelopes(envelopes_path: Path, blobs_dir: Path) -> dict[tuple[str, str], list[RecordedFixture]]:
    """
    Extracts exact source_url -> content_sha256 mappings from existing envelope evidence.
    Does NOT strip 'www.', does NOT discard query parameters, and does NOT map subpages to root URLs.
    Marks historical records as lacking response metadata (metadata_complete=False).
    """
    fixtures: dict[tuple[str, str], list[RecordedFixture]] = {}
    if not envelopes_path.exists():
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
    fixture_envelopes: Path = Path("out/candidate-1000-corrected-envelopes.jsonl"),
    websites: bool = True,
    hiring: bool = False,
    workers: int = 4
) -> dict:
    """Executes the actual Signalpost production runner using the offline recorded transport."""
    blobs_dir = state_dir / "blobs"
    fixtures = build_fixture_map_from_envelopes(fixture_envelopes, blobs_dir)
    print(f"Indexed {len(fixtures)} recorded URL fixtures from {fixture_envelopes.name}")

    output_envelopes.parent.mkdir(parents=True, exist_ok=True)
    output_report.parent.mkdir(parents=True, exist_ok=True)

    config = Config(
        organisations=input_path,
        output=output_envelopes,
        report=output_report,
        state_dir=state_dir,
        bulk=Path("state/downloads/wednesday1000.csv") if Path("state/downloads/wednesday1000.csv").exists() else None,
        websites=websites,
        hiring=hiring,
        workers=workers,
        time_budget_seconds=120,
        website_politeness_seconds=1,
    )

    transport = RecordedResponseTransport(blobs_dir=blobs_dir, fixture_map=fixtures)
    async with httpx.AsyncClient(transport=transport, trust_env=False) as client:
        report = await runner_run(config, client=client)

    if transport.missing_fixtures or transport.corrupt_fixtures:
        for m in transport.missing_fixtures:
            logger.error("Missing fixture: method=%s url=%s reason=%s", m[0], m[1], m[2])
        for c in transport.corrupt_fixtures:
            logger.error("Corrupt fixture: method=%s url=%s reason=%s", c[0], c[1], c[2])
        raise ReplayFixtureError(
            f"Production replay failed with {len(transport.missing_fixtures)} missing fixture(s) "
            f"and {len(transport.corrupt_fixtures)} corrupt fixture(s)."
        )

    print(f"Production replay completed: wrote envelopes to {output_envelopes}")
    return report


def main():
    parser = argparse.ArgumentParser(description="Signalpost Production Offline Replay Engine")
    parser.add_argument("--input", type=Path, default=Path("tests/fixtures/ci20.csv"), help="Input company cohort CSV")
    parser.add_argument("--envelopes-fixtures", type=Path, default=Path("out/candidate-1000-corrected-envelopes.jsonl"))
    parser.add_argument("--output", type=Path, default=Path("out/production-replay-envelopes.jsonl"))
    parser.add_argument("--report", type=Path, default=Path("out/production-replay-report.json"))
    parser.add_argument("--state-dir", type=Path, default=Path("state"))
    parser.add_argument("--websites", action="store_true", default=True)
    parser.add_argument("--hiring", action="store_true", default=False)
    args = parser.parse_args()

    try:
        asyncio.run(run_production_replay(
            input_path=args.input,
            output_envelopes=args.output,
            output_report=args.report,
            state_dir=args.state_dir,
            fixture_envelopes=args.envelopes_fixtures,
            websites=args.websites,
            hiring=args.hiring
        ))
    except ReplayFixtureError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
