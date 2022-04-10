# -*- coding: utf-8 -*-


from snowland.gis_tool.nds import get_lon_lat_of_tile

# -*- coding: utf-8 -*-

import time
from asyncio.coroutines import iscoroutinefunction

import wrapt

from astartool.project import is_windows

time_clock = time.time if is_windows() else time.clock


@wrapt.decorator
def coast_time(func, instacne, args, kwargs):
    def fun(*args, **kwargs):
        t = time.perf_counter()
        result = func(*args, **kwargs)
        print("func %s coast time:%.8f s" % (func.__name__, time.perf_counter() - t))
        return result

    async def func_async(*args, **kwargs):
        t = time.perf_counter()
        result = await func(*args, **kwargs)
        print("func %s coast time:%.8f s" % (func.__name__, time.perf_counter() - t))
        return result

    if iscoroutinefunction(func):
        return func_async(*args, **kwargs)
    else:
        return fun(*args, **kwargs)

@coast_time
def t():
    tile = 557468949
    print(get_lon_lat_of_tile(tile, 13))

t()