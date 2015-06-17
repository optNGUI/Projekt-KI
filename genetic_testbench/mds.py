##### Contains diverse algorithms for minimum dominating set-problem (optimizing problem) #####
from . import graphs, util
import BitVector
import copy, functools, itertools, operator, random, time, types

#@functools.lru_cache()
def is_covered(graph, vertex, solution):
    """Returns True if and only if the given vertex is covered
    by the given solution."""
    if vertex in solution:
        return True
    for v in graph.get_neighbours(vertex):
        if v in solution:
            return True
    return False


class _to_frozenset_Dom():
    def __init__(self, func):
        self.func = func
        self.cache = {}
    
    def __call__(self, arg0, arg1):
        arg1 = frozenset(arg1)
        if (arg0, arg1) in self.cache:
            return self.cache[(arg0,arg1)]
        else:
            tmp = self.func(arg0, arg1)
            self.cache[(arg0, arg1)] = tmp
            return tmp
        return self.func(arg0, arg1)

@_to_frozenset_Dom
def is_dominating(graph, solution):
    """Input: Graph (must be instance of Graph)
    and a solution (i.e. a set of vertices).
    Returns True if and only if vertices in solution are dominating
    the input graph."""
    for v in graph.get_vertices():
        if not is_covered(graph, v, solution):
            return False
    return True

    
#@functools.lru_cache()
def coverage(covering, graph):
    """Returns the set of vertices that are covered by the given vertex/vertices.
    In particular, this set contains exactly the given vertex and its neighbours"""
    cov = set()
    try: # assume covering is a set of vertices
        if type(covering) is str:
            raise TypeError
        for v in covering:
            #print("## v = {v}".format(v=v))
            cov.add(v)
            for n in graph.get_neighbours(v):
                cov.add(n)
    except TypeError: # covering is not iterable, is a single vertex instead
        cov.add(covering)
        for n in graph.get_neighbours(covering):
            cov.add(n)
    return cov
    
#@functools.lru_cache()
def dominating_number(solution, graph):
    sol_cov = set()
    for v in solution:
        sol_cov |= coverage(v, graph)
    return len(sol_cov)

    


def simple_search(graph, all=False):
    """Realizes a naive brute-force algorithm."""
    
    necessary=kernelize(graph)
    remaining = set(graph.get_vertices()) - necessary
    n = len(remaining)
    print('Necessary: '+str(necessary))
    s = []

    #print("Beginning naive search, input size n = {n}".format(n=n))
    for i in range(n+1):
        if s:
            return s
        for partial in itertools.combinations(remaining, i):
            solution = set(partial) | necessary
            if is_dominating(graph, solution):
                if not all:
                    return solution
                s.append(solution)

###########################
#####  Kernelization  #####
###########################

@functools.lru_cache()
def kernelize(graph):
    """
    Performs a kernelization.
    Returns a set of vertices which are necessary for a MDS
    """
    necessary = set()
    for v in graph.get_vertices():
        if graph.degree(v) == 0:
            necessary.add(v)
        if graph.degree(v) == 1:
            n, = graph.get_neighbours(v)
            if v not in necessary:  # in case deg(v) = deg(n) = 1
                necessary.add(n)
    return necessary


###############################
#####  Greedy algorithms  #####
###############################


def value(graph, vertex, partial_solution):
    neighbours = graph.get_neighbours(vertex)
    cov = coverage(partial_solution, graph)
    return len(neighbours - cov)


def value_degree(graph, vertex, partial_solution):
    return graph.degree(vertex)


def greedy_det(graph, valueFunc, necessary=None):
    """Calculates a dominating set which is not necessarily a MDS."""
    if necessary is None:
        solution = set()
    else:
        solution = copy.copy(necessary)
    remaining = graph.get_vertices() - solution
    second = operator.itemgetter(1)
    while not is_dominating(graph, solution):
        # Select the vertex with the highest value
        best = max([(v, valueFunc(graph, v, solution)) for v in remaining], key=second)[0]
        solution.add(best)
        remaining.remove(best)
    return solution


def greedy_random(graph, necessary=None):
    if necessary is None:
        solution = set()
    else:
        solution = copy.copy(necessary)
    remaining = graph.get_vertices() - solution
    while not is_dominating(graph, solution):
        v, = random.sample(remaining,1)
        remaining.remove(v)
        solution.add(v)
    return solution

###############################
###############################


def test_algorithm(graph, algorithm, n=1, verbose=False):
    duration = [0 for i in range(n)]
    for i in range(n):
        start = time()
        try:
            s = algorithm(graph)
        except TypeError:  # algorithm is recursive
            s = algorithm(graph, set())
        duration[i] = time() - start
        if verbose:
            print(s)
    d = sum(duration) / n
    return d

if __name__ == "__main__":
    print("\n### Testing Algorithms... ###")
    print("First, a very simple graph with five vertices...")
    a = graphs.SimpleGraph()
    for i in range(5):
        a.add_vertex(i)
    a.add_edge(0, 2)
    a.add_edge(1, 2)
    a.add_edge(2, 3)
    a.add_edge(3, 4)
    print("Correct answer is 2.")
    print(("Brute-force: {}".format(simple_search(a))))
    #print("Recursion with Preproc: {}".format(recursive_preproc(a, set())))

    #for i in range(3, 500):
        #a = graphs.construct_random_graph(n=i, p=0.05)
        #print("\nN = {}".format(i))
        ##d = test_algorithm(a, simple_search, n=1, verbose=True)
        ##print("\tw/o Preprocessing:  avg: {d:.5f} seconds".format(d=d))
        #d1 = test_algorithm(a, search_pre, n=1, verbose=True)
        #print("\twith Preprocessing: avg: {d:.5f} seconds".format(d=d1))
        ##print("\t\tAcceleration factor: {:.2f}".format(d/d1))
        ##print("\tNaive recursion: avg: {d:.5f} seconds".format(d=test_algorithm(a, recursive_naive, n=10, verbose=False)))
        ##print("\tRecursion with Preproc: avg: {d:.5f} seconds".format(d=test_algorithm(a, recursive_preproc, n=1, verbose=True)))

#

