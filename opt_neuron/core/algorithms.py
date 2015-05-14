### Contains base class for algorithms ###
from threading import Thread
from . import send_msg
import types
from enum import IntEnum

class Status(IntEnum):
    NOT_STARTED = -1
    RUNNING = 0
    TERMINATED = 1


class ThreadedAlgorithm():
    """
    This class represents a threaded algorithm.
    The constructor takes a func object which should hold the algorithm's code.
    This func object can write into self.__status to provide status during the calculation
    IMPORTANT: While binding the function object, the first argument will
    be converted to implicit self argument!
    """
    # TODO : Refactoring!
    
    def __init__(self, func):
        
        # Bind the func object as instance method
        self.func = types.MethodType(func, self)
        
        self.__status = Status.NOT_STARTED
        # You may extend this feature to support requesting 
        # some values, e.g. the current fitness
    
    @property
    def status(self):
        return self.__status
        
    
    def __call__(self, *args, **kwargs):
        t = Thread(target=self.func, args=args, kwargs=kwargs)
        t.start()
        return t


def dummy_algorithm(self, arg):
    print("I'm a dummy algorithm and doing nothing other than printing this little message.")
    print("Given arg: {arg}".format(arg=arg))
    send_msg("RETURNED: Dummy algorithm")
