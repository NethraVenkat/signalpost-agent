"""Research-loop responsiveness measured with a 100 ms heartbeat."""
import asyncio,time,statistics,gc,threading
from .workers import METRICS,WorkerMetrics


class LoopMonitor:
    def __init__(self):
        self.samples=[];self.task=None;self.gc_samples=[];self.gc_starts={};self.main_thread=threading.get_ident()
    def gc_callback(self,phase,info):
        key=threading.get_ident()
        if phase=='start':self.gc_starts[key]=(time.monotonic(),time.thread_time())
        elif key in self.gc_starts:
            began,cpu=self.gc_starts.pop(key)
            elapsed=(time.monotonic()-began)*1000
            self.gc_samples.append({'generation':info['generation'],'duration_ms':elapsed,'cpu_ms':(time.thread_time()-cpu)*1000,'main_thread':key==self.main_thread})
    async def heartbeat(self):
        while True:
            expected=time.monotonic()+.1
            await asyncio.sleep(.1)
            self.samples.append(max(0,time.monotonic()-expected)*1000)
    def start(self):
        self.worker_metrics=WorkerMetrics();self.metrics_token=METRICS.set(self.worker_metrics)
        self.cpu_start=time.process_time();self.wall_start=time.monotonic()
        gc.callbacks.append(self.gc_callback)
        self.task=asyncio.create_task(self.heartbeat())
    async def stop(self):
        gc.callbacks.remove(self.gc_callback)
        self.task.cancel()
        await asyncio.gather(self.task,return_exceptions=True)
        values=sorted(self.samples)
        METRICS.reset(self.metrics_token)
        return {'process_cpu_seconds':time.process_time()-self.cpu_start,'observed_wall_seconds':time.monotonic()-self.wall_start,
                'workers':self.worker_metrics.snapshot(),
                'heartbeat_interval_ms':100,'samples':len(values),'scope':'whole run after input entry; includes source processing and output generation',
                'lag_p95_ms':values[min(len(values)-1,int(.95*len(values)))] if values else 0,
                'lag_max_ms':max(values,default=0),'lag_mean_ms':statistics.mean(values) if values else 0,
                'gc_collections':len(self.gc_samples),'gc_total_ms':sum(s['duration_ms'] for s in self.gc_samples),
                'gc_max_ms':max((s['duration_ms'] for s in self.gc_samples),default=0),
                'gc_slow_collections':[s for s in self.gc_samples if s['duration_ms']>=50]}
