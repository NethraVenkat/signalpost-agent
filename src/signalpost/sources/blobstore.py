import base64
import hashlib
import threading
from pathlib import Path


class BlobStore:
    # Blobs written during this run stay readable from memory: re-opening
    # freshly created files is slow on Windows (on-access scanning), which
    # dominated output verification. Beyond the cap, reads fall back to disk.
    RECENT_LIMIT_BYTES = 256 * 1024 * 1024

    def __init__(self, state_dir: Path):
        self.directory = state_dir / "blobs"
        self.directory.mkdir(parents=True, exist_ok=True)
        self._lock=threading.RLock()
        self._recent = {}
        self._recent_bytes = 0

    def read(self, sha: str):
        """Blob bytes, or None when absent. Bytes are verified when first stored."""
        body = self._recent.get(sha)
        if body is not None:
            return body
        try:
            return (self.directory / sha).read_bytes()
        except FileNotFoundError:
            return None

    def put(self, body: bytes):
        with self._lock:return self._put(body)

    def _put(self,body):
        sha = hashlib.sha256(body).hexdigest()
        target = self.directory / sha
        if target.exists():
            if hashlib.sha256(target.read_bytes()).hexdigest() != sha:
                raise ValueError("Existing blob is corrupt")
        else:
            # All calls are within one event loop or serial bulk preparation.
            with target.open("xb") as handle:
                handle.write(body)
        if sha not in self._recent and self._recent_bytes + len(body) <= self.RECENT_LIMIT_BYTES:
            self._recent[sha] = body
            self._recent_bytes += len(body)
        return sha

    def restore(self, evidence):
        # Legacy envelopes can still supply embedded data. New envelopes
        # carry metadata only; an absent prior blob is not a fetch instruction.
        if evidence.snapshot_body_base64:
            return self.put(base64.b64decode(evidence.snapshot_body_base64, validate=True))
        return evidence.content_sha256
