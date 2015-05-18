### Contains base class for algorithms ###
from threading import Thread
from .main import send_msg
import types
from enum import IntEnum
from .. import util

class Status(IntEnum):
    NOT_STARTED = -1
    RUNNING = 0
    RETURNED = 1


class ThreadedAlgorithm():
    """
    This class represents a threaded algorithm.
    The constructor takes a func object which should hold the algorithm's code.
    This func object can write into self.__status to provide status during the calculation
    IMPORTANT: While binding the function object, the first argument will
    be converted to implicit self argument!
    """
    # TODO : Refactoring!
    
    def __callWrapper(self, *args, **kwargs):
        print("Call Wrapper: Initiated")
        self.__return_value = self.func(*args, **kwargs)
        self.__status = Status.RETURNED
    
    def __init__(self, func):
        
        # Bind the func object as instance method
        self.func = types.MethodType(func, self)
        
        self.__status = Status.NOT_STARTED
        self.__return_value = None
        # You may extend this feature to support requesting 
        # some values, e.g. the current fitness
    
    @property
    def status(self):
        return self.__status
        
    @property
    def return_value(self):
        return self.__return_value
    
    def __call__(self, *args, **kwargs):
        t = Thread(target=self.__callWrapper, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
        return t


def dummy_algorithm(self, arg):
    while True:
        pass

