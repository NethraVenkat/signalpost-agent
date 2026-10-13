import json
import pytest
from scripts.verify_output import verify
from tests.test_registry import config, execute


def test_verification_rejects_missing_membership_and_corrupt_sources(tmp_path):
    cfg = config(tmp_path, ['923609016'])
    execute(cfg)
    verify(cfg.output, cfg.state_dir, 1, cfg.organisations, cfg.report, True)
    with pytest.raises(AssertionError):
        verify(cfg.output, cfg.state_dir, 2)
    row = json.loads(cfg.output.read_text().splitlines()[0])
    sha = next(e['content_sha256'] for e in row['evidence'])
    (cfg.state_dir / 'blobs' / sha).write_bytes(b'corrupted')
    with pytest.raises(AssertionError):
        verify(cfg.output, cfg.state_dir, 1)
