"""Temporary Windows idle-sleep request; never changes persistent power settings."""
import os

CONTINUOUS=0x80000000
SYSTEM_REQUIRED=0x00000001


class SystemAwake:
    def __init__(self,enabled=True):
        self.enabled=enabled;self.call=None;self.previous=None
        self.result={'state':'disabled' if not enabled else 'not_applicable','display_request':False}
    def __enter__(self):
        if not self.enabled or os.name!='nt':return self
        try:
            import ctypes
            self.call=ctypes.WinDLL('kernel32',use_last_error=True).SetThreadExecutionState
            self.call.argtypes=[ctypes.c_uint32];self.call.restype=ctypes.c_uint32
            self.previous=self.call(CONTINUOUS|SYSTEM_REQUIRED)
            self.result={'state':'requested' if self.previous else 'unavailable','display_request':False,
                         'scope':'active batch only; idle sleep request; no persistent setting changes'}
        except (OSError,AttributeError):self.result['state']='unavailable'
        return self
    def __exit__(self,*args):
        if self.call is not None and self.previous:
            try:self.result['restored']=bool(self.call(self.previous))
            except (OSError,AttributeError):self.result['restored']=False
