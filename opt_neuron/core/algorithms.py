### Contains base class for algorithms ###
from threading import Thread
from .main import send_msg
import types, inspect, logging, sys
from enum import IntEnum
from .. import util
from . import net
from random import Random
from inspyred import ec
from inspyred.ec import terminators
from time import time, sleep

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
            send_msg(util.MESSAGE_FAILURE(self.__msg, "optimization died: "+str(e)))            
            return None
        self.__status = Status.RETURNED
        #send_msg(util.StatusMessage(content='terminated ' + self.func.__name__))
        send_msg(util.RetValMessage(self.__msg, appendix = self.__return_value))
    
    def __init__(self, msg, host, net, analysis, func):
        
        # Bind the func object as instance method
        self.func = types.MethodType(func, self)
        
        self.host = host
        self.net = net
        self.analysis = analysis
 
        self.__status = Status.NOT_STARTED
        self.__return_value = None
        self.__msg = msg
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
    def msg(self):
        return self.__msg
        
    @property
    def return_value(self):
        return self.__return_value
    
    def __call__(self, *args, **kwargs):
        t = Thread(target=self.__callWrapper, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
        return t
    
    
    def fitness(self, *args):
        sum = 0
        for x in args:
            sum += x
        ret = -abs(30-sum)        
        sleep(0.025)
        #ret = net.start_net(self.host, self.net, self.analysis, *args)
        #if ret is None:
        #    raise(Exception("error running net. maybe wrong SSH password?"))
        return float(ret)


@__add_alg
def simple_genetic(self, i_length, p_count = 100, generations = 100, i_min = 0, i_max = 100):
    
    # code stolen from http://lethain.com/genetic-algorithms-cool-name-damn-simple/
    
    t = self
   
    from random import randint, random
    from operator import add

    def individual(length, min, max):
        'Create a member of the population.'
        return [ randint(min,max) for x in range(length) ]

    def population(count, length, min, max):
        """
        Create a number of individuals (i.e. a population).

        count: the number of individuals in the population
        length: the number of values per individual
        min: the minimum possible value in an individual's list of values
        max: the maximum possible value in an individual's list of values

        """
        return [ individual(length, min, max) for x in range(count) ]

    def fitness(individual):
        """
        Determine the fitness of an individual. Higher is better.

        individual: the individual to evaluate
        """
        return t.fitness(*individual)
        
    def grade(pop):
        'Find average fitness for a population.'
        summed = 0
        for x in (fitness(x) for x in pop):
            summed += x
        return summed / (len(pop) * 1.0)

    def evolve(pop, retain=0.2, random_select=0.05, mutate=0.01):
        graded = [ (fitness(x), x) for x in pop]
        graded = [ x[1] for x in sorted(graded, reverse=True)]
        retain_length = int(len(graded)*retain)
        parents = graded[:retain_length]
        # randomly add other individuals to
        # promote genetic diversity
        for individual in graded[retain_length:]:
            if random_select > random():
                parents.append(individual)
        # mutate some individuals
        for individual in parents:
            if mutate > random():
                pos_to_mutate = randint(0, len(individual)-1)
                # this mutation is not ideal, because it
                # restricts the range of possible values,
                # but the function is unaware of the min/max
                # values used to create the individuals,
                individual[pos_to_mutate] = randint(
                    min(individual), max(individual))
        # crossover parents to create children
        parents_length = len(parents)
        desired_length = len(pop) - parents_length
        children = []
        while len(children) < desired_length:
            male = randint(0, parents_length-1)
            female = randint(0, parents_length-1)
            if male != female:
                male = parents[male]
                female = parents[female]
                half = int(len(male) / 2)
                child = male[:half] + female[half:]
                children.append(child)
        parents.extend(children)
        return parents
    
    p = population(int(p_count), int(i_length), int(i_min), int(i_max))
    fitness_history = [grade(p),]
    for i in range(int(generations)):
        logger.debug("simple_genetic generation "+str(i))
        print("simple_genetic generation "+str(i))
        p = evolve(p)
        fitness_history.append(grade(p))

    #for datum in fitness_history:
    #    print(datum)
    best = p[0]
    bestfit = fitness(best)
    for individuum in p:
        if(fitness(individuum) > bestfit):
            best = individuum
            bestfit = fitness(individuum)
    return [best,bestfit]

@__add_alg
def random_search(self, i_length, step_size=5, steps=100, i_min=0, i_max=100):
    
    from random import randint, random
    t = self
  
    best = [randint(int(i_min),int(i_max)) for i in range(int(i_length))]
    bestfit = t.fitness(*best)
    for i in range(int(steps)):
        logger.debug("random_search step "+str(i))
        print("random_search step "+str(i))
        new = [min(int(i_max),max(int(i_min),(i+(2*random()-1)*int(step_size)))) for i in best]
        if(bestfit < t.fitness(*new)):
            best = new
            bestfit = t.fitness(*new)
    return [best,bestfit]
     

def list_of_algorithms():
    return [(i.__name__, i, inspect.getargspec(i)) for i in algs]
