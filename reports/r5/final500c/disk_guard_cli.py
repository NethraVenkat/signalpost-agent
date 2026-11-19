"""Execute the unchanged installed CLI with a free-space interrupt guard.

No evaluator flags or evidence rules are changed. SIGINT asks asyncio.run to
cancel its main task and close its clients instead of forcibly killing Python.
"""
import _thread
import json
import os
from pathlib import Path
import runpy
import shutil
import threading
import time

from signalpost.portable_paths import portable_text


def main():
    root = Path(os.environ['FINAL500C_GUARD_ROOT'])
    receipt = Path(os.environ['FINAL500C_GUARD_RECEIPT'])
    threshold = 3 * 1024**3
    initial = shutil.disk_usage(root).free
    state = dict(threshold_bytes=threshold, interval_seconds=2, initial_free_bytes=initial,
                 minimum_free_bytes=initial, stopped_for_low_space=False,
                 interrupt='Python SIGINT; asyncio cancellation and client cleanup')
    done = threading.Event()
    started = time.monotonic()

    def check():
        free = shutil.disk_usage(root).free
        state['minimum_free_bytes'] = min(state['minimum_free_bytes'], free)
        if free < threshold:
            state.update(stopped_for_low_space=True, stop_free_bytes=free,
                         stop_seconds=time.monotonic()-started)
            return False
        return True

    def monitor():
        while not done.wait(2):
            if not check():
                print('Disk guard: below 3 GiB free; requesting clean SIGINT shutdown.', flush=True)
                _thread.interrupt_main()
                return

    try:
        if not check():
            raise SystemExit(75)
        threading.Thread(target=monitor, name='disk-space-guard', daemon=True).start()
        runpy.run_module('signalpost.cli', run_name='__main__')
    except KeyboardInterrupt:
        raise SystemExit(75 if state['stopped_for_low_space'] else 130)
    finally:
        done.set()
        state['final_free_bytes'] = shutil.disk_usage(root).free
        state['minimum_free_bytes'] = min(state['minimum_free_bytes'], state['final_free_bytes'])
        state['wall_seconds'] = time.monotonic()-started
        receipt.write_text(portable_text(json.dumps(state, indent=2)+'\n'), encoding='utf8')


if __name__ == '__main__':
    main()
