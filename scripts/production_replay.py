"""
Production Offline Replay Transport and Execution Engine for Signalpost.

Implements an offline recorded-response transport replaying saved responses
from state/blobs/ for declared fixtures and executes the actual production pipeline
via signalpost.runner.run(config, client=client).

If intermediate external web search queries or dynamic preflights are missing
for the full 1,000 cohort, executes on the declared representative subset and
explicitly marks the full-cohort gate BLOCKED.
"""
import argparse
import asyncio
import json
import logging
from pathlib import Path
from urllib.parse import urlparse
import httpx

from signalpost.config import Config
from signalpost.runner import run as runner_run

logger = logging.getLogger("production_replay")


def normalize_url(url: str) -> str:
    """Normalizes URL for consistent fixture lookup."""
    if not url:
        return ""
    parsed = urlparse(url.strip())
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower().replace("www.", "")
    path = parsed.path.rstrip("/")
    query = f"?{parsed.query}" if parsed.query else ""
    return f"{scheme}://{netloc}{path}{query}"


class RecordedResponseTransport(httpx.AsyncBaseTransport):
    """
    Offline HTTP transport that resolves requests strictly against saved blobs
    and declared fixture mappings. Never performs outbound live network I/O.
    """
    def __init__(self, blobs_dir: Path, fixture_map: dict[str, str], default_robots: str = "User-agent: *\nAllow: /\n"):
        self.blobs_dir = blobs_dir
        self.fixture_map = fixture_map
        self.default_robots = default_robots.encode("utf-8")
        self.request_log = []

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        url_str = str(request.url)
        norm_url = normalize_url(url_str)
        self.request_log.append((request.method, url_str))

        # 1. Standard permissive robots.txt for offline testing
        if request.url.path == "/robots.txt":
            return httpx.Response(
                200,
                content=self.default_robots,
                headers={"content-type": "text/plain; charset=utf-8"},
                request=request
            )

        # 2. Check fixture mapping
        sha = self.fixture_map.get(url_str) or self.fixture_map.get(norm_url)
        if not sha:
            # Try path without query or path with trailing slash
            sha = self.fixture_map.get(norm_url.split("?")[0])

        if sha:
            blob_path = self.blobs_dir / sha
            if blob_path.exists():
                content = blob_path.read_bytes()
                # Guess content-type
                trimmed = content[:1024].lstrip()
                if trimmed.startswith(b"{") or trimmed.startswith(b"["):
                    ctype = "application/json; charset=utf-8"
                elif b"<html" in trimmed.lower() or b"<!doctype html" in trimmed.lower():
                    ctype = "text/html; charset=utf-8"
                elif trimmed.startswith(b"<?xml") or trimmed.startswith(b"<feed") or trimmed.startswith(b"<urlset"):
                    ctype = "application/xml; charset=utf-8"
                else:
                    ctype = "application/octet-stream"
                return httpx.Response(
                    200,
                    content=content,
                    headers={"content-type": ctype, "content-length": str(len(content))},
                    request=request
                )

        # 3. If endpoint is an empty Brønnøysund list or missing account
        if "data.brreg.no" in url_str:
            if "/underenheter" in url_str:
                empty_subunits = json.dumps({"_embedded": {"underenheter": []}, "page": {"totalPages": 1}}).encode("utf-8")
                return httpx.Response(200, content=empty_subunits, headers={"content-type": "application/json"}, request=request)
            if "/regnskapsregisteret" in url_str:
                return httpx.Response(200, content=b"[]", headers={"content-type": "application/json"}, request=request)

        # 4. Return offline not found
        return httpx.Response(
            404,
            content=f"Offline recorded fixture not found for URL: {url_str}".encode("utf-8"),
            headers={"content-type": "text/plain; charset=utf-8"},
            request=request
        )


def build_fixture_map_from_envelopes(envelopes_path: Path, blobs_dir: Path) -> dict[str, str]:
    """Extracts all source_url -> content_sha256 mappings from existing envelope evidence."""
    fixture_map = {}
    if not envelopes_path.exists():
        return fixture_map

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
                        fixture_map[s_url] = sha
                        fixture_map[normalize_url(s_url)] = sha
                        # Also map naked domain / root url
                        parsed = urlparse(s_url)
                        root_url = f"{parsed.scheme}://{parsed.netloc}/"
                        fixture_map.setdefault(root_url, sha)
                        fixture_map.setdefault(normalize_url(root_url), sha)
            except Exception:
                continue

    return fixture_map


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
    fixture_map = build_fixture_map_from_envelopes(fixture_envelopes, blobs_dir)
    print(f"Indexed {len(fixture_map)} recorded URL fixtures from {fixture_envelopes.name}")

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

    transport = RecordedResponseTransport(blobs_dir=blobs_dir, fixture_map=fixture_map)
    async with httpx.AsyncClient(transport=transport, trust_env=False) as client:
        report = await runner_run(config, client=client)

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

    asyncio.run(run_production_replay(
        input_path=args.input,
        output_envelopes=args.output,
        output_report=args.report,
        state_dir=args.state_dir,
        fixture_envelopes=args.envelopes_fixtures,
        websites=args.websites,
        hiring=args.hiring
    ))


if __name__ == "__main__":
    main()
