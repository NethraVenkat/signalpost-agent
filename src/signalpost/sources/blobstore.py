import base64
import hashlib
import threading
from pathlib import Path


class BlobStore:
    def __init__(self, state_dir: Path):
        self.directory = state_dir / "blobs"
        self.directory.mkdir(parents=True, exist_ok=True)
        self._lock=threading.RLock()

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
        return sha

    def restore(self, evidence):
        # Legacy envelopes can still supply embedded data. New envelopes
        # carry metadata only; an absent prior blob is not a fetch instruction.
        if evidence.snapshot_body_base64:
            return self.put(base64.b64decode(evidence.snapshot_body_base64, validate=True))
        return evidence.content_sha256
