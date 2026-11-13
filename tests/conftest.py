"""Offline fixtures need no wall-clock politeness delay; production is unchanged."""
import pytest


@pytest.fixture(autouse=True)
def offline_filing_year_spacing(monkeypatch):
    monkeypatch.setattr('signalpost.sources.http.FILING_YEAR_INTERVAL',0)
