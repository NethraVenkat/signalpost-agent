"""Small bounded pools: source CPU work cannot queue ahead of NAV parsing/I/O."""
import asyncio,contextvars,functools
from concurrent.futures import ThreadPoolExecutor

SOURCE_POOL=ThreadPoolExecutor(max_workers=4,thread_name_prefix='source-work')
NAV_POOL=ThreadPoolExecutor(max_workers=2,thread_name_prefix='nav-io')


async def _run(pool,fn,args,kwargs):
    context=contextvars.copy_context()
    call=functools.partial(fn,*args,**kwargs)
    return await asyncio.get_running_loop().run_in_executor(pool,context.run,call)


async def offload(fn,*args,**kwargs):return await _run(SOURCE_POOL,fn,args,kwargs)


async def nav_offload(fn,*args,**kwargs):return await _run(NAV_POOL,fn,args,kwargs)
