from td import * # pyright: ignore[reportMissingImports]


from typing import Callable, List

Timer_Callback = Callable[["Timer"], None]

class Timer:
    def __init__(self, callbacks:list[Timer_Callback] = [], stepsize:int = 1, loop = True) -> None:
        self.stepsize = stepsize
        self.loop = loop
        self.callbacks = list() + callbacks
        self.start()

    callbacks:List[Timer_Callback] = list()

    def start(self):
        run( "args[0]()", self.tick, delayFrames=self.stepsize )

    def tick(self):
        for callback in self.callbacks:
            try:
                callback(self)
            except Exception as e:
                debug("Error during timer callback", callback, e)
        if self.loop: self.start()

class Ticker(Timer):
    def __init__(self, callbacks: List[Timer_Callback] = [], stepsize: int = 1) -> None:
        super().__init__(callbacks, stepsize, True)
