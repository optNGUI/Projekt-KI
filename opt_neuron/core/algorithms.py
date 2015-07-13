### Contains base class for algorithms ###
from threading import Thread
from .main import send_msg
import types, inspect, logging, sys, traceback
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
            send_msg(util.MESSAGE_FAILURE(self.__msg, "optimization died: "+str(e)+traceback.format_exc()))            
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
        if sum == 100:
            ret = 1
        else:
            ret = 1/abs(100-sum)        
        sleep(0.001)
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
def genetic2(self, i_length, generations=50, pop_size=10):
    generations = int(generations)
    pop_size = int(pop_size)
    i_length = int(i_length)
    import binstr, random
    t = self
    logger.info("Started vernünftigen genetischen Algorithmus")
    
    
    def ind_to_params(ind):
        params = [None for i in range(i_length)]
        for i in range(i_length):
            params[i] = ind[8*i:8*(i+1)]
        return params
    
    def params_to_ind(params):
        ind = ''
        for i in params:
            ind+=binstr.b_bin_to_gray(binstr.int_to_b(i))
        return ind
    
    def individuum():
        return params_to_ind([random.randint(0,256) for i in range(i_length)])
    
    population = [individuum() for i in range(pop_size)]
    
    def mutate(ind):
        if len(ind) < 2:
            raise TypeError("Individuum too short")
        for i in range(len(ind)):
            if random.random() < 1/len(ind):
                if ind[i] == '0':
                    replace = '1'
                else:
                    replace = '0'
                ind = ind[:i] + replace + ind[i+1:]
    
    def crossover(ind1, ind2):
        point1, point2 = 0, 255
        while point1 == 0:
            point1 = random.randint(0,255)
        while point2 == 255:
            point2 = random.randint(0,255)
        if point1 > point2: # make sure point1 <= point2
            point1, point2 = point2, point1
        

        child0 = ind1[:point1] + ind2[point1:point2] + ind1[point2:]
        child1 = ind2[:point1] + ind1[point1:point2] + ind2[point2:]
        return (child0,child1)
    
    def select():
        cnt = 2
        sum_fit = sum([fitness(ind) for ind in population])
        pop = population[:]
        random.shuffle(pop)
        pairs = []
        for i in range(cnt):
            n = random.uniform(0, sum_fit)
            m = random.uniform(0, sum_fit)
            tmp_sum = 0
            first, second = None, None
            for ind in pop:
                tmp_sum += fitness(ind)
                if tmp_sum >= n:
                    first = ind
                    break
            tmp_sum = 0
            for ind in pop:
                tmp_sum += fitness(ind)
                if tmp_sum >= m:
                    second = ind
                    break
            if first is None or second is None:
                print("FAILED")
                raise RuntimeError("Ooops")
            pairs.append((first, second))
        print(str(pairs))
        return pairs
    
    def fitness(ind):
        params = ind_to_params(ind)
        params = [int(x) for x in params]
        return t.fitness(*params)
    
    for i in range(generations):
        logger.debug("Generation {i}".format(i=i))
        parents = select()
        children = []
        for p in parents:
            ind1, ind2 = p
            children.extend(crossover(ind1, ind2))
        n = len(population)
        for child in children:
            if child not in population:
                population.append(child)
        print(str(len(population)))
        while len(population) > n:  # O(|children|)
            population.remove(min(population, key=fitness))
        for i, ind in enumerate(population):
            new_ind = (ind+'.')[:-1]
            mutate(new_ind)
            if fitness(new_ind) >= fitness(ind) and new_ind not in population:
                population[i] = new_ind
        
    best = max(population, key=fitness)
    
    bestfit = fitness(best)
    best = ind_to_params(best)
    best = [binstr.b_to_int(i) for i in best]
    return (best,bestfit)
    

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
