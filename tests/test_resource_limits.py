import json
from tests.test_registry import config, execute


def test_no_embedded_bodies_and_verbatim_spans(tmp_path):
    cfg = config(tmp_path, ["923609016"])
    report, rows = execute(cfg)
    assert report["output_bytes"] == cfg.output.stat().st_size
    assert report["output_bytes_per_company"] < 60000
    assert "snapshot_body_base64" not in cfg.output.read_text()
    assert set(rows[0]["profile"]) == {"organisation_number", "values", "evidence_ids", "synthesis"}
    for evidence in rows[0]["evidence"]:
        assert len(evidence["claim_span"]) <= 300
        assert evidence["claim_span"] in (cfg.state_dir / "blobs" / evidence["content_sha256"]).read_text(encoding="utf8")


def test_previous_without_blobs(tmp_path):
    first = config(tmp_path / "first", ["923609016"])
    _, original = execute(first)
    second = config(tmp_path / "second", ["923609016"], previous=first.output)
    report, rows = execute(second)
    assert report["changes"] == 0
    assert [c["id"] for c in rows[0]["claims"]] == [c["id"] for c in original[0]["claims"]]
    assert report["requests"] == 4


def test_output_cap_preserves_membership(tmp_path):
    cfg = config(tmp_path, ["923609016"], max_output_mb=.003)
    report, rows = execute(cfg)
    assert len(rows) == 1
    assert report["output_limited_companies"] == ["923609016"]
    assert rows[0]["state"] == "budget_exhausted"
