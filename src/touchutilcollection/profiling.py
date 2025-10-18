from datetime import datetime

class TimeTracker:
    def __init__(self, print_on_exit = False):
        self.print_on_exit = print_on_exit
        self.start = datetime.now()
        self.end = datetime.now()

    def __enter__(self):
        self.start = datetime.now()
    
    def __exit__(self, type, value, traceback):
        self.end = datetime.now()
        if self.print_on_exit: debug( f"Meassured Time in microseconds: {self.microseconds}")

    @property
    def meassurement(self):
        return self.end - self.start
    
    @property
    def milliseconds(self):
        return self.meassurement.microseconds * 1000
    
    @property
    def microseconds(self):
        return self.meassurement.microseconds