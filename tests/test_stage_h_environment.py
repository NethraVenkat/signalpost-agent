from reports.r5.stageH.run_checks import execution_environment
from reports.r5.stageH.run_checks import validate_subset
import pytest


def test_live_runs_disable_paid_search_but_offline_tests_control_their_mocks(monkeypatch):
    monkeypatch.setenv('PYTHONPATH','synthetic-host-path')
    monkeypatch.setenv('SIGNALPOST_SEARCH_PROVIDER','brave')
    monkeypatch.setenv('BRAVE_SEARCH_API_KEY','synthetic-not-a-real-key')
    live=execution_environment()
    assert live['SIGNALPOST_SEARCH_PROVIDER']=='disabled' and live['SIGNALPOST_SEARCH_MOCK']=='0'
    assert 'PYTHONPATH' not in live
    offline=execution_environment(test_mode=True)
    assert 'SIGNALPOST_SEARCH_PROVIDER' not in offline and 'SIGNALPOST_SEARCH_MOCK' not in offline
    assert 'BRAVE_SEARCH_API_KEY' not in offline and 'PYTHONPATH' not in offline
    assert offline['PYTHONUTF8']=='1'


def test_missing_snapshot_row_keeps_original_input_for_live_identity_lookup():
    sample=['923609016','993578843']
    assert validate_subset({'expected':2,'rows':1,'missing_organisation_numbers':['993578843']},sample)==['993578843']
    assert sample==['923609016','993578843']
    with pytest.raises(AssertionError):validate_subset({'expected':2,'rows':1,'missing_organisation_numbers':[]},sample)
    with pytest.raises(AssertionError):validate_subset({'expected':2,'rows':1,'missing_organisation_numbers':['other']},sample)
