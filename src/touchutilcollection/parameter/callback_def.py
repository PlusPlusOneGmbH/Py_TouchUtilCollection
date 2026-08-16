from typing import List, Any

def empty_callback(*args, **kwargs):
	pass

from functools import lru_cache

@lru_cache(maxsize=None)
def fetch_callback(extension:object, callback_name:str):
	return getattr( extension, callback_name, empty_callback )


def onValuesChanged(changes: List[ParChange]):
	for c in changes:
		par = c.par
		prev = c.prev
		for extension in parent().extensions:
			fetch_callback(extension, f"on_{par.name}_Value_Change")(par, prev)
	return

def onPulse(par: Par):
	for extension in parent().extensions:
		fetch_callback(extension, f"on_{par.name}_Pulse")(par)
	return