### Contains base class for algorithms ###
from threading import Thread
from .main import send_msg
import types, inspect, logging, sys
from enum import IntEnum
from .. import util

logger = logging.getLogger(__name__)

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
    # TODO : HEAVY Refactoring!
    
    def __callWrapper(self, *args, **kwargs):
        self.__status = Status.RUNNING
        self.__return_value = self.func(*args, **kwargs)
        self.__status = Status.RETURNED
        send_msg(util.StatusMessage(content='terminated ' + self.func.__name__))
    
    def __init__(self, func):
        
        # Bind the func object as instance method
        self.func = types.MethodType(func, self)
        
        self.__status = Status.NOT_STARTED
        self.__return_value = None
        # You may extend this feature to support requesting 
        # some values, e.g. the current fitness
    
    @property
    def name(self):
        return self.__name
    
    def arguments(self):
        return self.__arguments
    
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


def dummy_algorithm(self, arg=5, blub = 7, *args, **kwargs):
    import time
    send_msg(util.StatusMessage(content='Going to sleep for five seconds...'))
    time.sleep(5)
    send_msg(util.StatusMessage(content='Waking up...'))




def list_of_algorithms():
    list_names = [i[0] for i in inspect.getmembers(sys.modules[__name__], predicate=inspect.isfunction)]
    list_names.remove('list_of_algorithms')
    list_names.remove('send_msg')
    logger.warning(str(list_names))
    return [(alg, eval(alg), inspect.getargspec(eval(alg))) for alg in list_names]
    
    
    
