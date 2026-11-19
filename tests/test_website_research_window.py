import pytest

from signalpost import budget as meter
from signalpost.budget import Budget, SourceFailure
from tests.test_registry import config, numbers


def test_queued_proof_after_old_cutoff_can_use_remaining_budget(tmp_path, monkeypatch):
    now = [1000.0]
    monkeypatch.setattr(meter.time, 'monotonic', lambda: now[0])
    budget = Budget(config(tmp_path, numbers(100)))
    original_deadline, original_cap = budget.deadline, budget.cap
    budget.phase = 'pass2'
    now[0] += 600  # A slow pass 1; the old 340-second cutoff lost all remaining proof walks.
    budget.check_website()
    event = budget.reserve('https://proof.example.no/privacy', 'proof.example.no', '923609016')
    assert event['pass'] == 'pass2'
    assert budget.deadline == original_deadline
    assert budget.cap == original_cap == 1850
    now[0] = budget.start + 1700
    with pytest.raises(SourceFailure, match='deadline'):
        budget.check_website()
    assert budget.deadline - now[0] == pytest.approx(85)
