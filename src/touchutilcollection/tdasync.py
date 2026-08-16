from td import * # pyright: ignore[reportMissingImports]

from .timing import Ticker, Timer

from typing import Union, List, Coroutine, Dict, Tuple

import asyncio
from asyncio import Task, AbstractEventLoop


_loops:Dict[str, Tuple[Ticker, AbstractEventLoop]] = {}

DEFAULT_LOOP_NAME = "_default"

def _create_loop():
	_loop = asyncio.new_event_loop()
	_loop.stop()

	def _async_tick( timer:Timer):
		_loop.stop()
		_loop.run_forever()

	_async_ticker = Ticker([ _async_tick ])
	return _async_ticker, _loop


def use_loop(name:str = DEFAULT_LOOP_NAME):
	"""
		Creates a new loop if does not yet exist under the curent name, otherwise return it.
	"""
	if existing_loop:=_loops.get(name): return existing_loop[1]
	_loops[name] = _create_loop()
	return _loops[name][1]

def destroy_loop(name:str):
	"""
		Destroy the loop of the given name. Will raise KeyError if it does not exist!
	"""
	ticker, loop =_loops[name]
	ticker.stop()
	loop.close()
	del _loops[name]
	

def execute(coroutines:Union[ List[Coroutine], Coroutine], loop_name = DEFAULT_LOOP_NAME) -> List[Task]:
	"""
		Runs all routines concurrently and returns a list of tasks.
	"""
	returnTasks = []
	if not isinstance( coroutines, list): coroutines = [coroutines]
		
	for coroutine in coroutines:
		returnTasks.append( 
			use_loop(loop_name).create_task(coroutine)
		)
	return returnTasks

def cancel(killList:List[Task] = [], loop_name = DEFAULT_LOOP_NAME ):
	"""
		Cancels all tasks currently active or the defines task in the list.
		Only pass loop_name if killlist is empty.
	"""
	for task in killList or asyncio.all_tasks(use_loop(loop_name)):
		task.cancel()

