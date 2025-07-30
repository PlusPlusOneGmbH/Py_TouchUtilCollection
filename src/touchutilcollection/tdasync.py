from td import * # pyright: ignore[reportMissingImports]
from timing import Ticker, Timer

import asyncio
from asyncio import AbstractEventLoop, Task

loop = asyncio.new_event_loop()
loop.stop()

def _async_tick( timer:Timer):
    loop.stop()
    loop.run_forever()

_async_ticker = Ticker([ _async_tick ])




