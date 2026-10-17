"""Tests for dashboard analytics from verified envelope data."""

import json
import pytest
from pathlib import Path
from src.signalpost.dashboard import analyze_envelopes


@pytest.fixture
def sample_envelopes_file(tmp_path):
    """Create a sample envelopes file for testing."""
    envelopes_path = tmp_path / "envelopes.jsonl"

    envelopes = [
        {
            "orgnr": "123456789",
            "status": "complete",
            "company": {
                "name": "Test Company 1",
                "industry": {"code": "70.22"}
            },
            "sources": {
                "identity": {"state": "complete"},
                "accounts": {"state": "complete"},
                "roles": {"state": "complete"},
                "subunits": {
                    "state": "complete",
                    "subunits": [{"orgnr": "111111111"}, {"orgnr": "222222222"}]
                },
                "websites": {"state": "complete"},
                "hiring": {"state": "not_available"},
                "public_activity": {"state": "partial"}
            }
        },
        {
            "orgnr": "987654321",
            "status": "complete",
            "company": {
                "name": "Test Company 2",
                "industry": {"code": "70.22"}
            },
            "sources": {
                "identity": {"state": "complete"},
                "accounts": {"state": "not_available"},
                "roles": {"state": "partial"},
                "subunits": {"state": "not_available"},
                "websites": {"state": "not_available"},
                "hiring": {"state": "complete"},
                "public_activity": {"state": "not_available"}
            }
        },
        {
            "orgnr": "555555555",
            "status": "submission_error",
            "error": "website_required"
        }
    ]

    with open(envelopes_path, 'w') as f:
        for envelope in envelopes:
            f.write(json.dumps(envelope) + '\n')

    return envelopes_path


def test_analyze_envelopes_counts(sample_envelopes_file):
    stats = analyze_envelopes(sample_envelopes_file)

    assert stats['total_companies'] == 3
    assert stats['complete'] == 2
    assert stats['errors'] == 1


def test_analyze_envelopes_coverage(sample_envelopes_file):
    stats = analyze_envelopes(sample_envelopes_file)
    coverage = stats['coverage_percent']

    # All 3 have identity (complete or partial)
    assert coverage['identity'] == 100.0

    # 2 out of 3 have accounts
    assert coverage['accounts'] == pytest.approx(66.7, 0.1)

    # 2 out of 3 have websites
    assert coverage['websites'] == pytest.approx(66.7, 0.1)

    # 1 out of 3 have hiring
    assert coverage['hiring'] == pytest.approx(33.3, 0.1)


def test_analyze_envelopes_industries(sample_envelopes_file):
    stats = analyze_envelopes(sample_envelopes_file)
    industries = stats['industries_top']

    # Both complete companies are in industry 70.22
    assert '70.22' in industries
    assert industries['70.22'] == 2


def test_analyze_envelopes_subunit_footprint(sample_envelopes_file):
    stats = analyze_envelopes(sample_envelopes_file)
    footprint = stats['subunit_footprint']

    # Company 1: 2 subunits
    assert '2' in footprint
    # Company 2: not_available
    assert 'unknown' in footprint
    # Company 3: no subunits section (error)

    # 1 out of 3 has 2 subunits
    assert footprint['2'] == pytest.approx(33.3, 0.1)


def test_analyze_envelopes_empty_file(tmp_path):
    empty_path = tmp_path / "empty.jsonl"
    empty_path.write_text("")

    stats = analyze_envelopes(empty_path)
    assert stats['total_companies'] == 0


def test_analyze_envelopes_nonexistent_file():
    nonexistent = Path("/nonexistent/path/envelopes.jsonl")
    stats = analyze_envelopes(nonexistent)
    assert stats == {}


def test_analyze_envelopes_malformed_lines(tmp_path):
    """Test that malformed JSON lines are skipped."""
    bad_path = tmp_path / "bad.jsonl"

    with open(bad_path, 'w') as f:
        f.write(json.dumps({"status": "complete", "company": {"name": "Good"}}) + '\n')
        f.write("this is not json\n")
        f.write(json.dumps({"status": "complete", "company": {"name": "Also Good"}}) + '\n')

    stats = analyze_envelopes(bad_path)
    # Should skip the bad line and count 2
    assert stats['total_companies'] == 2


def test_subunit_footprint_explicit_empty_claim(tmp_path):
    """Test that explicit empty-collection claim is counted, not missing data."""
    envelopes_path = tmp_path / "envelopes.jsonl"

    envelopes = [
        {
            "orgnr": "111111111",
            "status": "complete",
            "sources": {
                "subunits": {
                    "state": "complete",
                    "subunits": []  # Explicit: no subunits
                }
            }
        },
        {
            "orgnr": "222222222",
            "status": "complete",
            "sources": {
                "subunits": {
                    "state": "not_available"  # Unknown, not zero
                }
            }
        }
    ]

    with open(envelopes_path, 'w') as f:
        for envelope in envelopes:
            f.write(json.dumps(envelope) + '\n')

    stats = analyze_envelopes(envelopes_path)
    footprint = stats['subunit_footprint']

    # First should be counted as 0 subunits
    assert '0' in footprint
    assert footprint['0'] == 50.0

    # Second should be unknown
    assert 'unknown' in footprint
    assert footprint['unknown'] == 50.0
