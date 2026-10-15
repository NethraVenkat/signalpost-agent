"""Small bounded pools: source CPU work cannot queue ahead of NAV parsing/I/O."""
import asyncio,contextvars,functools,time,threading
from concurrent.futures import ThreadPoolExecutor

SOURCE_POOL=ThreadPoolExecutor(max_workers=4,thread_name_prefix='source-work')
NAV_POOL=ThreadPoolExecutor(max_workers=2,thread_name_prefix='nav-io')
METRICS=contextvars.ContextVar('signalpost_worker_metrics',default=None)


class WorkerMetrics:
    def __init__(self):
        self.rows={};self.lock=threading.Lock()
    def record(self,name,queued,wall,cpu):
        with self.lock:
            row=self.rows.setdefault(name,dict(calls=0,queue_seconds=0,wall_seconds=0,cpu_seconds=0,max_queue_seconds=0,max_wall_seconds=0))
            row['calls']+=1
            row['queue_seconds']+=queued;row['wall_seconds']+=wall;row['cpu_seconds']+=cpu
            row['max_queue_seconds']=max(row['max_queue_seconds'],queued)
            row['max_wall_seconds']=max(row['max_wall_seconds'],wall)
    def snapshot(self):
        with self.lock:return {key:dict(value) for key,value in sorted(self.rows.items())}


async def _run(pool,fn,args,kwargs):
    context=contextvars.copy_context()
    metrics=METRICS.get();submitted=time.monotonic()
    def call():
        began=time.monotonic();cpu=time.thread_time()
        try:return fn(*args,**kwargs)
        finally:
            if metrics is not None:
                name=getattr(fn,'__module__','')+'.'+getattr(fn,'__qualname__',type(fn).__name__)
                metrics.record(name,began-submitted,time.monotonic()-began,time.thread_time()-cpu)
    return await asyncio.get_running_loop().run_in_executor(pool,context.run,call)


async def offload(fn,*args,**kwargs):return await _run(SOURCE_POOL,fn,args,kwargs)


async def nav_offload(fn,*args,**kwargs):return await _run(NAV_POOL,fn,args,kwargs)
