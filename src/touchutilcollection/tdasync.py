from td import * # pyright: ignore[reportMissingImports]
from timing import Ticker, Timer
from typing import Union, List, Awaitable

import asyncio
from asyncio import Task, _CoroutineLike

loop = asyncio.new_event_loop()
loop.stop()

def _async_tick( timer:Timer):
    loop.stop()
    loop.run_forever()

_async_ticker = Ticker([ _async_tick ])


def execute(coroutines:Union[ List[_CoroutineLike], _CoroutineLike]) -> List[Task]:
	"""
		Runs all routines concurrently and returns a list of tasks.
	"""
	returnTasks = []
	if not isinstance( coroutines, list): coroutines = [coroutines]
		
	for coroutine in coroutines:
		returnTasks.append( 
			loop.create_task(coroutine)
		)
	return returnTasks

def cancel(killList:List[Task] = [] ):
	"""
		Cancels all tasks currently active or the defines task in the list.
	"""
	for task in killList or asyncio.all_tasks(loop):
		task.cancel()