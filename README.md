# TouchUtilCollection
A collection of (hopefully) useful python-functions, methods and other trinkets.

Install via PIP, UV, Conda or whatever you like. 

Not all are isted in the readme, see this as a list of "highlights"

## tdasync
Bring asyncio to TD in this minimal wrapper.
```python
from touchutilcollection.tdasync import execute
from asyncio import sleep
async def coro( waittime ):
    op("text1").text = "Starting Coro"
    await sleep(waittime)
    op("text1").text = "Done"
execute( coro(5) )
```
Powerfull with TauCetiTweener and the .Resolve() functionality.

## Extension
Makes your live with extensions easier by allowing for autocreation of custompars.
```python

from touchutilcollection.extensions import EnsureExtension, partypes, parfield, pargrouptypes, pargroupfield

class extExample( 
    EnsureExtension # Required
     ):
    class par:
        Foo = parfield(partypes.ParFloat)
        Bar = parfield(partypes.ParFloat, page ="Different", min = 0, max = 10)
        Baba = parfield( 
            partypes.ParMenu, 
            menuLabels=["Eins", "Zwei", "Drei" ], 
            menuNames=["1", "2", "3"], 
            bindExpr="op.Settings.par.Baba" 
        )

    class parGroup:
        Somergb = pargroupfield( pargrouptypes.ParGroupRGBA, size = 3, default = (2,2,2) )

    def __init__(self, ownerComp) -> None:
        super().__init__(ownerComp) # Also required
        self.par.Foo.val = 23
        self.parGroup.Somergb[0].val = 2 # access pars using index
        self.parGroup.default = (1,2,3) # same members as pars, but as touples. size needs to be considered!
```
Alost helps with the autocallback-system for parameters.

```python
from touchutilcollection.extensions import auto_callback_system

def my_extensions:
    def __init__(self, ownerComp:COMP):
        auto_callback_system( ownerComp )

    def on_Foobar_Value_Change( self, par:Par, prev_val:str):
        """ Gets called when the value of the parameter Foobar changes,"""
        debug("Foobar")
```


## Ensure
Ensure existence of components without having to manualy create them (or even see them. )
### Ensure Tox
Ensure the existence of the given TOX-COMP using a global op shortcut.
```python
from touchutilcollection.ensure import ensure_global_tox
from TauCeti import Tweener
TweenerComp = ensure_global_tox( Tweener.ToxFile, "TAUCETI_TWEENER" )
```
### Ensure TDP
Takes values from a TDP and applies the same Logic.
```python
from touchutilcollection.ensure import ensure_global_tox
from TauCeti import Tweener
TweenerComp = ensure_global_tox( Tweener )
```


## Network
```python
from touchutilcollection.network import get_free_port
# Will return any free port currently available on the system
```

## Events
A pruely python approach to event-handling similiar to how it is handled in the DOM/HTML.
You can subscribe to any operator and any event. Events will bubble up the path. 

```python
from touchutilcollection.events import subscribe, emit

def example_handler(_source:OP, emitter:OP, event_name:str, bubbled:bool, *args, **kwargs):
    debug( _source, emitter, event_name, bubbled, args, kwargs)
    pass

subscribe( root, "foobar", example_handler)
emit( me, "foobar", "example_arg")
# note that bubbled will be true in the event-handler as we emittet the event from a child-component.
```