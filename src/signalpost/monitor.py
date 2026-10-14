"""Research-loop responsiveness measured with a 100 ms heartbeat."""
import asyncio,time,statistics


class LoopMonitor:
    def __init__(self):self.samples=[];self.task=None
    async def heartbeat(self):
        while True:
            expected=time.monotonic()+.1
            await asyncio.sleep(.1)
            self.samples.append(max(0,time.monotonic()-expected)*1000)
    def start(self):self.task=asyncio.create_task(self.heartbeat())
    async def stop(self):
        self.task.cancel()
        await asyncio.gather(self.task,return_exceptions=True)
        values=sorted(self.samples)
        return {'heartbeat_interval_ms':100,'samples':len(values),'scope':'whole run after input entry; includes source processing and output generation',
                'lag_p95_ms':values[min(len(values)-1,int(.95*len(values)))] if values else 0,
                'lag_max_ms':max(values,default=0),'lag_mean_ms':statistics.mean(values) if values else 0}
