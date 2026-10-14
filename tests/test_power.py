from types import SimpleNamespace
from signalpost.power import SystemAwake,CONTINUOUS,SYSTEM_REQUIRED


def test_windows_request_restores_previous_state_without_display_flag(monkeypatch):
    import ctypes
    calls=[]
    class Call:
        def __call__(self,flags):calls.append(flags);return CONTINUOUS
    call=Call()
    monkeypatch.setattr('signalpost.power.os',SimpleNamespace(name='nt'))
    monkeypatch.setattr(ctypes,'WinDLL',lambda *a,**kw:SimpleNamespace(SetThreadExecutionState=call),raising=False)
    with SystemAwake() as power:assert power.result['state']=='requested'
    assert calls==[CONTINUOUS|SYSTEM_REQUIRED,CONTINUOUS]
    assert power.result['restored'] and not power.result['display_request']


def test_disabled_or_non_windows_makes_no_os_request(monkeypatch):
    monkeypatch.setattr('signalpost.power.os',SimpleNamespace(name='posix'))
    with SystemAwake() as power:assert power.result['state']=='not_applicable'
    with SystemAwake(False) as power:assert power.result['state']=='disabled'
