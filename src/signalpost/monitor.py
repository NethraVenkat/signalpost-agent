"""Research-loop responsiveness measured with a 100 ms heartbeat."""
import asyncio,time,statistics,gc,threading


class LoopMonitor:
    def __init__(self):
        self.samples=[];self.task=None;self.gc_samples=[];self.gc_starts={};self.main_thread=threading.get_ident()
    def gc_callback(self,phase,info):
        key=threading.get_ident()
        if phase=='start':self.gc_starts[key]=time.monotonic()
        elif key in self.gc_starts:
            elapsed=(time.monotonic()-self.gc_starts.pop(key))*1000
            self.gc_samples.append({'generation':info['generation'],'duration_ms':elapsed,'main_thread':key==self.main_thread})
    async def heartbeat(self):
        while True:
            expected=time.monotonic()+.1
            await asyncio.sleep(.1)
            self.samples.append(max(0,time.monotonic()-expected)*1000)
    def start(self):
        gc.callbacks.append(self.gc_callback)
        self.task=asyncio.create_task(self.heartbeat())
    async def stop(self):
        gc.callbacks.remove(self.gc_callback)
        self.task.cancel()
        await asyncio.gather(self.task,return_exceptions=True)
        values=sorted(self.samples)
        return {'heartbeat_interval_ms':100,'samples':len(values),'scope':'whole run after input entry; includes source processing and output generation',
                'lag_p95_ms':values[min(len(values)-1,int(.95*len(values)))] if values else 0,
                'lag_max_ms':max(values,default=0),'lag_mean_ms':statistics.mean(values) if values else 0,
                'gc_collections':len(self.gc_samples),'gc_total_ms':sum(s['duration_ms'] for s in self.gc_samples),
                'gc_max_ms':max((s['duration_ms'] for s in self.gc_samples),default=0),
                'gc_slow_collections':[s for s in self.gc_samples if s['duration_ms']>=50]}
