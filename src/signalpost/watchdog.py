import asyncio
import time


async def finish_before_deadline(tasks, budget):
    if not tasks:
        return 0
    _, pending = await asyncio.wait(tasks, timeout=max(0, budget.deadline - time.monotonic()))
    for task in pending:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    return len(pending)
