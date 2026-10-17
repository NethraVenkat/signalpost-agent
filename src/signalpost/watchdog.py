import asyncio
import time


async def finish_before_deadline(tasks, budget, grace=10):
    """Wait until the deadline, cancel stragglers, then wait at most `grace` seconds.

    Returns (tasks pending at the deadline, tasks still running after the grace
    period). Callers always continue to terminal output, even if some never stop.
    """
    if not tasks:
        return 0, 0
    _, pending = await asyncio.wait(tasks, timeout=max(0, budget.deadline - time.monotonic()))
    for task in pending:
        task.cancel()
    stuck = set()
    if pending:
        _, stuck = await asyncio.wait(pending, timeout=grace)
    for task in tasks:
        if task.done() and not task.cancelled():
            task.exception()  # Retrieved; company code records its own failures.
    return len(pending), len(stuck)
