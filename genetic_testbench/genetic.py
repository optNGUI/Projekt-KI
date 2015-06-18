##### Contains the genetic algorithm and its components. #####

import BitVector
import copy, math, operator, types, random
from functools import lru_cache
from collections import OrderedDict
from . import util,  mds, mds

class Genetic_Algorithm:
    def __init__(self, first, terminate, select, crossover, mutate, replace, fitness):
        """
        Initializes the genetic algorithm.
        Make sure the methods will work together!
        """
        self.__gen_cnt, self.__graph, self.population = None, None, None
        self.set_crossover(crossover)
        self.set_first(first)
        self.set_fitness(fitness)
        self.set_mutate(mutate)
        self.set_replace(replace)
        self.set_select(select)
        self.set_terminate(terminate)
        self.out = None
        self._runs = 1
    
    def print_population(self):
        self.out.write("\nGeneration {gen}\n".format(gen=self.gen_cnt))
        for ind in self.population:
            self.out.write(str(ind)+ ' length: '+ str(ind.count_bits())+ ' fit: '+ str(self.fitness(ind))+'\n')
        self.out.write("\n")
        self.out.flush()
        
    @property
    def graph(self):
        # Read-only access to graph object
        return self.__graph
    
    @property
    def gen_cnt(self):
        # Read-only access to generation counter
        return self.__gen_cnt
        
    def __call__(self, graph):
        self.initialize(graph)
        return self.run()
    
    def initialize(self, graph):
        self.__graph = graph  # Initialization of graph object
        self.__gen_cnt = 0  # Initialization of generation counter
        self.population = self.first()
        if self.out:
            self.out.write('############################\n')
            self.out.write('Run #{i}\n'.format(i=self._runs))
    
    def run(self):
        """Runs the genetic algorithm on the given graph object.
        The algorithm runs until termination specified in the 
        terminate() method. The best individuum (according to its
        fitness value) is extracted after termination.
        """
        self._runs += 1
        if self.out:
            self.print_population()
        while not self.terminate():
            self.next_gen()
            if self.out:
                self.print_population()
        best = self.extract_best()
        #return util.subset_from_bitv(best, self.graph)
        return best
    
    def next_gen(self):
        """Moves on to the next generation."""
        parents = self.select()
        children = []
        for parent in parents:
            children.extend(self.crossover(parent))
        
                
        # Removes the children which are the same as a parent
        children[:] = [child for child in children if child not in (p for pairs in parents for p in pairs)]
        self.replace(children, self.population)
        
        
        for i, ind in enumerate(self.population):
            new_ind = ind.deep_copy()
            self.mutate(new_ind)
            if self.fitness(new_ind) >= self.fitness(ind) and new_ind not in self.population:
                self.population[i] = new_ind
        
        self.__gen_cnt += 1 # Modify counter only here
        
    def first(self):
        """Returns a population"""
        raise NotImplementedError
    
    def terminate(self):
        """Returns if the algorithm shall terminate"""
        raise NotImplementedError
    
    def select(self):
        """Returns a list of sets of individuals which have been
        selected to reproduce themselves"""
        raise NotImplementedError
    
    def crossover(self, individua):
        """Performs a crossover and returns a list of children."""
        raise NotImplementedError
    
    def mutate(self, individuum):
        """Mutates the given individuum and returns the mutated one."""
        raise NotImplementedError
    
    def replace(self, individua, population):
        """Returns a new population based upon the given population and
        the given individua."""
        raise NotImplementedError
    
    def fitness(self, individuum): 
        raise NotImplementedError
    
    def extract_best(self):
        """Returns the best individuum in the population, according to the fitness function"""
        second = operator.itemgetter(1)
        best = max([(i, self.fitness(i)) for i in self.population], key=second)[0]
        return best
    
    def set_first(self, func):
        self.first = types.MethodType(func, self)
        
    def set_terminate(self, func):
        self.terminate = types.MethodType(func, self)
    
    def set_select(self, func):
        self.select = types.MethodType(func, self)
        
    def set_crossover(self, func):
        self.crossover = types.MethodType(func, self)
        
    def set_mutate(self, func):
        self.mutate = types.MethodType(func, self)
    
    def set_replace(self, func):
        self.replace = types.MethodType(func, self)
        
    def set_fitness(self, func):
        self.fitness = types.MethodType(func, self)
    
    def set_outputstream(self, stream):
        self.out = stream
    
#############################################
##### Crossover #####
#####################

def get_crossover(alg='spread', *args):
    if alg == 'simple':
        def simple(self, individua):
            """Simple crossover method"""
            point = random.randint(0, self.graph.size)
            # Expecting exactly two parents!!!
            parent0, parent1 = individua
            child0 = parent0[:point] + parent1[point:]
            child1 = parent1[:point] + parent0[point:]
            return (child0, child1)
        return simple
            
    elif alg == 'two_point':
        def two_point_crossover(self, individua):
            point1, point2 = 0, self.graph.size-1
            while point1 == 0:
                point1 = random.randint(0,self.graph.size)
            while point2 == self.graph.size-1:
                point2 = random.randint(0,self.graph.size)
            if point1 > point2: # make sure point1 <= point2
                point1, point2 = point2, point1
            
            parent0, parent1 = individua
            
            child0 = parent0[:point1] + parent1[point1:point2] + parent0[point2:]
            child1 = parent1[:point1] + parent0[point1:point2] + parent1[point2:]
            return (child0,child1)
        return two_point_crossover
    
    elif alg == 'spread':
        n = int(args[0])
        def spread_crossover(self, individua):
            parent0, parent1 = individua
            indices = random.sample(range(len(parent0)), n)
            child0 = parent0[:]
            child1 = parent1[:]
            for i in indices:
                child0[i] = parent1[i]
                child1[i] = parent0[i]
            return (child0, child1)
            
        return spread_crossover


######################
##### SELECT #####
##################

def get_select(alg, *args):
    if alg == 'random':
        def select_rand(self):
            # Only for populations of size > 4 !!!
            pop = self.population[:]
            a = []
            for i in range(4):
                tmp = random.choice(pop)
                pop.remove(tmp)
                a.append(tmp)
            return [[a[0],a[1]],[a[2],a[3]]]
        return select_rand
    
    elif alg == 'four_best':
        def select(self):
            """Simply chooses the four best individua"""
            
            tmp = sorted(self.population, key=self.fitness, reverse=True)
            return [(tmp[0], tmp[1]), 
                    (tmp[2], tmp[3])]
        return select
    
    elif alg == 'roulette':
        cnt = int(args[0])
        def roulette(self):
            sum_fit = sum([self.fitness(ind) for ind in self.population])
            pop = self.population[:]
            random.shuffle(pop)
            pairs = []
            for i in range(cnt):
                n = random.uniform(0, sum_fit)
                m = random.uniform(0, sum_fit)
                tmp_sum = 0
                first, second = None, None
                for ind in pop:
                    tmp_sum += self.fitness(ind)
                    if tmp_sum >= n:
                        first = ind
                        break
                tmp_sum = 0
                for ind in pop:
                    tmp_sum += self.fitness(ind)
                    if tmp_sum >= m:
                        second = ind
                        break
                if first is None or second is None:
                    print("FAILED")
                pairs.append((first, second))
            return pairs
        return roulette


##################
##### FIRST #####
##################

def get_first(alg, *args):
    if alg == 'zero':
        size = int(args[0])
        def func(self):
            pop = [BitVector.BitVector(size=self.graph.size) for i in range(size)]
            return pop
        return func
    
    if alg =='degree':
        size = int(args[0])
        def func(self):
            pop = [BitVector.BitVector(size=self.graph.size) for i in range(size)]
            p  = self.graph.avg_degree()/self.graph.size    
            # Now set some vertices to selected
            for ind in pop:
                for v in range(ind.length()):
                    if random.random() < p:
                        ind[v] = 1
            return pop
        return func   
    
    elif alg == 'uniform':
        size = int(args[0])
        p = float(args[1])
        def func(self):
            pop = [BitVector.BitVector(size=self.graph.size) for i in range(size)]
            
            # Now set some vertices to selected
            for ind in pop:
                for v in range(ind.length()):
                    if random.random() < p:
                        ind[v] = 1
            return pop
            
        return func   
    
    elif alg == 'necessary':
        size = int(args[0])
        p = float(args[1])

        def func(self):
            # Get the necessary nodes
            nec = mds.kernelize(self.graph)
            
            # Generate the bit vectors
            val = str(util.bitv_from_subset(nec, self.graph))
            pop = [BitVector.BitVector(bitstring=val) for i in range(size)]
            
            # Now set some vertices to selected
            for ind in pop:
                for v in range(ind.length()):
                    if ind[v] == 0:
                        if random.random() < p:
                            ind[v] = 1
            return pop
        
        return func
    
    elif alg == 'greedy':
        size = int(args[0])
        kernelize = (args[1].lower() == 'true' or args[1].lower() == 'yes')

        def func(self):
            if kernelize:
                nec = mds.kernelize(self.graph)
            else:
                nec = None
                
            solution = mds.greedy_det(self.graph, mds.value, nec)
            ind = util.bitv_from_subset(solution, self.graph)
            pop = [ind for i in range(size)]
            
            return pop
            
        return func
    print("ERROR")
    exit(-1)

####################
##### REPLACE #####
######################

def get_replace(alg = 'append', *args):
    if alg == 'naive':
        def replace_naive(self, children, population):
            """
            Replaces the worst individua in population with the given children.
            """
            for c in children:
                population[population.index(min(population, key=self.fitness))] = c
        return replace_naive
        
    elif alg == 'append':
        def replace_append(self, children, population):
            """
            Appends the given children to the population and the removes the 
            worst individua so that the population size remains constant.
            """
            n = len(population)
            for child in children:
                if child not in population:
                    population.append(child)
            #population.extend(children)  # O(|children|)
            while len(population) > n:  # O(|children|)
                population.remove(min(population, key=self.fitness))  # O(|population|)
        return replace_append

####################
##### MUTATE #####
##################

def get_mutate(alg, *args):
    if alg == 'uniform_graph':
        def mutate_uniform(self, individuum):
            for v in range(individuum.length()):
                if random.random() < 1/self.graph.size:
                    individuum[v] ^= 1  # flips the bit
        return mutate_uniform
    elif alg == 'uniform':
        p = float(args[0])
        def mutate_uniform(self, individuum):
            for v in range(individuum.length()):
                if random.random() < p:
                    individuum[v] ^= 1  # flips the bit
        return mutate_uniform

###################
##### FITNESS #####
###################

class _Cached_Fitness():
    def __init__(self, func):
        self.func = func
        self.cache = {}
    
    def __call__(self, arg0, arg1):
        if (arg0, str(arg1)) in self.cache:
            return self.cache[(arg0,str(arg1))]
        else:
            tmp = self.func(arg0, arg1)
            self.cache[(arg0, str(arg1))] = tmp
            return tmp

def get_fitness(alg, *args):
    if alg == 'default':
        
        @_Cached_Fitness
        def fitness(self, individuum):
            # First, create subset from bitvector
            solution = util.subset_from_bitv(individuum, self.graph)
            dom_num = mds.dominating_number(solution, self.graph)
            if dom_num == 0:
                return 0
            return dom_num + 1/individuum.count_bits()
        return fitness
        
    if alg == 'other':
    
        @_Cached_Fitness
        def fitness2(self, individuum):
            # First, create subset from bitvector
            solution = util.subset_from_bitv(individuum, self.graph)
            dom_num = mds.dominating_number(solution, self.graph)
            if dom_num == 0:
                return 0
            return dom_num * 1/individuum.count_bits()
        return fitness2

################################################################################
##### TERMINATE ######
#####################

def get_terminate(alg, *args):
    if alg == 'at_optimum':
        
        def terminate_at_optimum(self):
            best = self.extract_best()
            if mds.is_dominating(self.graph, util.subset_from_bitv(best, self.graph)) and best.count_bits() == self.graph.dom_number:
                    return True
            return False
        return terminate_at_optimum
    
    
    elif alg == 'max_generation':
        gen = int(args[0])
        
        def terminate_at_gen(self):
            return self.gen_cnt < gen   
        return terminate_at_gen
        
    elif alg == 'number':
        num = int(args[0])
        def terminate_at_num(self):
            best = self.extract_best()
            if mds.is_dominating(self.graph, util.subset_from_bitv(best, self.graph)) and best.count_bits() <= num:
                    return True
            return False
        return terminate_at_num




