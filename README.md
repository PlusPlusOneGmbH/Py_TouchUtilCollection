# TouchUtilCollection
A collection of (hopefully) useful python-functions, methods and other trinkets.

Install via PIP, UV, Conda or whatever you like. 

## Extensions
Utilities to makes live with extensions easier.
### EnsureExtension
Allows to ensure a certain state of the extension and its component in a declarative way. The Values will be set when ```super().__init__(ownerComp)``` is called.

- Existing parameters with the given name will be overwritten. 
- Parameters that are removed from the extension will continue to exist.
- Supports full auto-complete and additional type hinting.

```python
from touchutilcollection.extensions import partyoes, parfield, EnsureExtension
class extExample( EnsureExtension ):
    class par:
        Foo = parfield(partypes.ParFloat)
        Bar = parfield(partypes.ParFloat, page ="Different", min = 0, max = 10)
        Baba = parfield( partypes.ParMenu, menuLabels=["Eins", "Zwei", "Drei" ], bindExpr="Hello World")

    def __init__(self, ownerComp) -> None:
        super().__init__(ownerComp)
        # Use self.par to access the paraeters directly, without a call to self.ownerComp.par

        self.par.Foo.val = 23
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

## TDAsync
A simple wrapper arround pythons asyncio to work directly in TD.
```python
from touchutilcollection.tdasync import execute
from asyncio import sleep

async def wait_for_timer( timer_op ):
    while timer_op["running"].eval():
        # Do not forget the await, otherwise it will freeze.
        await sleep(0)

async def example(timer_op):
    debug("Starting timer")
    timer_op.par.start.pulse()   
    await wait_for_timer( timer_op )
    debug("Done")

execute(example( op("timer1")) )
```

## Profiling
Helps is measuring python scripts. 
```python
from touchutilcollection.profiling import TimeTracker
with TimeTracker as _tracker:
    op("top1").save("Foobar.png")
    print( _tracker.measured )
```

## External
Handling external files.
### better_import
An actual better importer. It is highly opininated. Has to be implemented by hand. 

When used, will import the files with the apropiate Operators and link them directly using relative pathin if possible.
