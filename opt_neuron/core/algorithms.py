### Contains base class for algorithms ###
from threading import Thread
from .main import send_msg
import types, inspect, logging, sys
from enum import IntEnum
from .. import util
from . import net

logger = logging.getLogger(__name__)
algs = []

def __add_alg(func):
    global algs
    algs.append(func)
    return func

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
        try:
            self.__return_value = self.func(*args, **kwargs)
        except Exception as e:
            print(e)            
            return None
        self.__status = Status.RETURNED
        send_msg(util.StatusMessage(content='terminated ' + self.func.__name__))
    
    def __init__(self, host, net, analysis, func):
        
        # Bind the func object as instance method
        self.func = types.MethodType(func, self)
        
        self.host = host
        self.net = net
        self.analysis = analysis
 
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
    
    
    def fitness(self, *args):
        ret = net.start_net(self.host, self.net, self.analysis, args)
        if ret is None:
            raise(Exception("error running net. maybe wrong SSH password?"))
        return ret


@__add_alg
def genetic_alg(self):
    
    t = self

    def fit_net(self, individuum):
        arg0= str(individuum[0:4])
        arg1= str(individuum[4:8])
        arg2= str(individuum[8:12])
        arg3= str(individuum[12:16])
        return t.fitness(arg0,arg1,arg2,arg3)


    import genetic_testbench as gt

    g = gt.genetic.Genetic_Algorithm(first = gt.genetic.get_first('zero', '2'),
                                terminate = gt.genetic.get_terminate('max_generation', '10'),
                                select = gt.genetic.get_select('roulette', '1'),
                                mutate = gt.genetic.get_mutate('uniform', '0.001'),
                                crossover = gt.genetic.get_crossover('spread', '1'),
                                replace = gt.genetic.get_replace('append'),
                                fitness = fit_net)
    
    g.set_outputstream(sys.stdout)

    class Foo():
        pass

    graph = Foo()
    graph.size = 16

    ret = g(graph)
    return (fit_net(None, ret), ret[0:4], ret[4:8], ret[8:12], ret[12:16])

@__add_alg
def dummy_algorithm(self, arg=5, blub = 7, *args, **kwargs):
    import time
    send_msg(util.StatusMessage(content='Going to sleep for five seconds...'))
    time.sleep(5)
    send_msg(util.StatusMessage(content='Waking up...'))

@__add_alg
def lassDasMalDenMoritzMachen(self):
    ## Deprecated Function calls!
    pass
    #import genetic_testbench.genetic as ga
    #send_msg(util.StatusMessage(content=str(ga)))
    #alg = ga.Genetic_Algorithm(first =     ga.get_init_from_greedy(), 
        #terminate = ga.terminate_at_optimum, 
        #select =    ga.select, 
        #crossover = ga.get_spread_crossover(n=1), 
        #mutate =    ga.get_mutate_uniform(p=1/10), 
        #replace =   ga.replace_append, 
        #fitness =   ga.fitness)
    #import genetic_testbench.graphs as graphs
    #graph = graphs.construct_star_graph(c=4, d=5)
    #send_msg(util.StatusMessage(content=str(alg(graph))+' <- Der Moritz macht das gut.'))


def list_of_algorithms():
    return [(i.__name__, i, inspect.getargspec(i)) for i in algs]
