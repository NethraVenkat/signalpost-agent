import asyncio
import threading
from signalpost.workers import offload
from signalpost.monitor import LoopMonitor
from tests.test_registry import config,execute


def test_report_build_and_disk_write_are_off_loop(tmp_path,monkeypatch):
    import signalpost.runner as runner
    main=threading.get_ident();seen=[]
    for name in ['build','write_report']:
        original=getattr(runner,name)
        def checked(*args,_original=original,_name=name,**kwargs):
            assert threading.get_ident()!=main
            seen.append(_name)
            return _original(*args,**kwargs)
        monkeypatch.setattr(runner,name,checked)
    report,_=execute(config(tmp_path,['923609016']))
    assert set(seen)=={'build','write_report'}
    assert report['event_loop']['workers']


def test_worker_metrics_distinguish_wall_and_cpu_and_keep_context():
    async def gate():
        monitor=LoopMonitor();monitor.start()
        thread=await offload(threading.get_ident)
        assert thread!=threading.get_ident()
        metrics=await monitor.stop()
        rows=metrics['workers'].values()
        assert sum(row['calls'] for row in rows)==1
        assert all(row['queue_seconds']>=0 and row['wall_seconds']>=0 and row['cpu_seconds']>=0 for row in rows)
    asyncio.run(gate())
