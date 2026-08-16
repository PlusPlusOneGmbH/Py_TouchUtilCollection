from td import *  # pyright: ignore[reportMissingImports]
from typing import Dict, Callable, Tuple, List, Set
from .operator import iter_parents

def _empty_callback(_source:OP, emitter:OP, event_name:str, bubbled:bool, *args, **kwargs):
    pass

EventCallbackType = Callable[[OP, OP, str, bool, Tuple[any, ...], Dict[any, any]], None]


_subscriptions:Dict[str, Dict[str, Set[EventCallbackType]]] = {} 


def subscribe( emitter:OP, event:str, callback:EventCallbackType):
    _subscriptions.setdefault( emitter.path , {}).setdefault(event,  set()).add( callback )

def unsubscribe( emitter:OP, event:str, callback:EventCallbackType):
    _subscriptions.setdefault( emitter.path , {}).setdefault(event,  set()).remove( callback )

def emit( _emitter:OP, _event:str, *args, _bubble = True, **kwargs):
    for _bubble in [_emitter] + list(iter_parents( _emitter )):
        for callback in _subscriptions.get( _bubble.path, {} ).get( _event, []):
            try:
                callback( _emitter, _bubble, _event, _emitter != _bubble, *args, **kwargs )
            except Exception as e:
                debug("Encountered exception during event emitting.", _emitter, _bubble, _event, e)
