"""Run unchanged pytest checks with less scheduling contention on Windows."""
import ctypes
import json
import os
import sys
import pytest

def main():
    priority_set = False
    if os.name == 'nt':
        # Only this process and its threads; no machine-wide or persistent change.
        kernel = ctypes.windll.kernel32
        kernel.GetCurrentProcess.restype = ctypes.c_void_p
        kernel.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint]
        priority_set = bool(kernel.SetPriorityClass(kernel.GetCurrentProcess(), 0x8000))
    print(json.dumps({'command': [sys.executable, __file__, *sys.argv[1:]],
                      'priority': 'above_normal' if priority_set else 'unchanged',
                      'mutates_test_assertions_or_timeouts': False}), flush=True)
    return pytest.main(sys.argv[1:])


if __name__ == '__main__':
    raise SystemExit(main())
