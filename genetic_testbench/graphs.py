##### Contains important graph classes ######
import collections
import itertools
import pickle
import random
from . import util
from abc import abstractmethod, ABCMeta

class Graph(metaclass=ABCMeta):
    """Defines important methods for graphs"""

    @abstractmethod
    def get_vertices(self):
        """Returns a list of all vertices."""
        pass

    @abstractmethod
    def get_edges(self):
        """Returns a list/set of all edges."""
        pass

    @staticmethod
    @abstractmethod
    def is_directed():
        pass

    @abstractmethod
    def add_vertex(self, vertex):
        """Adds the given vertex to the graph object.
        It is recommended to use integer values as vertices.
        Returns False if the vertex is already existing and True otherwise."""
        pass

    @abstractmethod
    def add_edge(self, v1, v2):
        """Connects the two given vertices with each other.
        Returns False if the edge already exists, and true otherwise.
        Throws a RuntimeError if the two vertices don't exist."""
        pass

    def degree(self, vertex):
        """Returns the number of vertices the given vertex is connected to."""
        return len(self.get_neighbours(vertex))

    @abstractmethod
    def get_neighbours(self, vertex):
        """Returns a list/set of vertices the given vertex is connected to."""
        pass

    @abstractmethod
    def subgraph(self, vertices):
        """Creates a graph object with the given vertices
        and connects the vertices as they already were."""
        pass


class SimpleGraph(Graph):
    """
    Implements a simple graph.
    A simple graph is undirected, has no loops and no multiple edges.
    """

    def __init__(self):
        self.__graph = collections.OrderedDict()
        self.__size = 0
        self.__dom_number = None
        self.descr = "n/a"

    @staticmethod
    def is_directed():
        return False

    @classmethod
    def from_file(cls, filename):
        """
        Loads a graph object from the given filename.
        Accepts only graphs with nodes as integers.
        """
        #g = cls()
        if not filename.endswith('.SimpleGraph'):
            filename += '.SimpleGraph'
        with open(filename, "rb") as handle:
            g = pickle.load(handle)

        return g

    def to_file(self, filename):
        """
        Saves the graph into the given file. Will overwrite the file,
        if already existing.
        """
        if not filename.endswith('.SimpleGraph'):
            filename += '.SimpleGraph'
        with open(filename, "wb") as handle:
            pickle.dump(self, handle)

    def to_tex(self, filename="graph.tex"):
        """
        Generates a .tex file which can be compiled via lualatex.
        It utilizes the TikZ library and its graphdrawing library.
        """
        with open(filename, "w") as handle:
            handle.write(util.generate_tex_code(self))
    
    
    @property
    def dom_number(self):
        return self.__dom_number
    
    @dom_number.setter
    def dom_number(self, value):
        self.__dom_number = value

    @property
    def size(self):
        return self.__size

    def get_vertices(self):  # O(|V|)
        return self.__graph.keys()

    def get_edges(self):  # O(|V| + |E|)
        edges = set()
        for v1 in self.__graph.keys():
            for v in self.__graph[v1]:
                edges.add((v1, v))
        return edges

    #def degree(self, vertex):  # O(1) -- except for amortized worst case
        #return len(self.get_neighbours(vertex))

    def add_vertex(self, vertex):  # O(1) -- except for amortized worst case
        if vertex not in self.__graph:
            self.__graph[vertex] = set()
            self.__size += 1
            self.__dom_number = None
            return True
        return False

    def avg_degree(self):
        d = [len(v) for v in self.__graph.values()]
        return sum(d)/len(d)
    
    def add_edge(self, v1, v2):  # O(1) -- except for amortized worst case
        if v1 == v2:
            return False
        if v1 not in self.__graph:
            raise RuntimeError("Vertex {vertex} not found."
                                    .format(vertex=str(v1)))
        if v2 not in self.__graph:
            raise RuntimeError("Vertex {vertex} not found."
                                    .format(vertex=str(v2)))
        self.__graph[v1].add(v2)
        self.__graph[v2].add(v1)
        self.__dom_number = None
        return True
    
    def remove_edge(self, v1, v2):
        if v1 not in self.__graph:
            raise RuntimeError("Vertex {vertex} not found."
                                    .format(vertex=str(v1)))
        if v2 not in self.__graph:
            raise RuntimeError("Vertex {vertex} not found."
                                    .format(vertex=str(v2)))
        ret = True
        try:
            self.__graph[v1].remove(v2)
        except KeyError:
            ret = False
        
        try:
            self.__graph[v2].remove(v1)
        except KeyError:
            ret = False
            
        self.__dom_number = None
        return True

    def get_neighbours(self, vertex):  # O(1) -- except for amortized worst case
        #print(self.__graph)
        return self.__graph[vertex]

    def subgraph(self, vertices):  # O(|vertices|+|E|)
        s = SimpleGraph()
        for v in vertices:
            if v not in self.__graph:
                raise RuntimeError("Vertex {vertex} not found."
                                        .format(vertex=str(v)))
            s.add_vertex(v)
        for v1, v2 in self.get_edges():
            try:
                s.add_edge(v1, v2)
            except RuntimeError:
                pass
        return s

def construct_random_graph(n=10, p=0.2):
    """Constructs a random simple graph where n is the number of vertices
    and p is the probability of two vertices being connected."""

    g = SimpleGraph()
    for i in range(n):
        g.add_vertex(i)

    for v1, v2 in itertools.combinations(g.get_vertices(), 2):
        if random.random() < p:
            g.add_edge(v1, v2)

    g.descr = "Random graph, n={c}, p={d}".format(n=n, p=p)
    return g

def construct_star_graph(c=2, d=3, p=1):
    if d <= c:
        print("d must be greater than c")
        return None
    g = SimpleGraph()
    for i in range(c):
        for j in range(d+1):
            a=g.add_vertex(i*(d+1)+j)
            if not a:
                print("ERROR")
    
    # Connect the center.
    for i in range(c):
        for j in range(1,d+1):
            g.add_edge(i*(d+1), i*(d+1)+j)
    
    ## Connect the periphere nodes to other periphere
    #for i1, i2 in itertools.permutations(range(c), 2):
        #for j1, j2 in itertools.permutations(range(1,d+1), 2):
            #if i1 == i2 and j1 == j2:
                #continue
            #print(i1*(d+1)+j1, i2*(d+1)+j2)
            ##if random.random() < p:
                ##print(g.add_edge(i1*(d+1)+j1, i2*(d+1)+j2))
    for v1, v2 in itertools.combinations(g.get_vertices(), 2):
        if v1 % (d+1) == 0 or v2 % (d+1) == 0:
            continue
        if random.random() < p:
            g.add_edge(v1, v2)
            
    g.dom_number = c   
    g.descr = "Star graph, c={c}, d={d}".format(c=c, d=d)     
    
    return g

        
def _graph02(c=3, d=3):
    g = graphs.SimpleGraph()
    # Generate the c complete subgraphs of size d
    for i in range(c):
        for j in range(d):
            g.add_vertex(i*c+j)
        for v1, v2 in itertools.combinations([v for v in range(i*c,i*c+d)], 2):
            g.add_edge(v1, v2)
    # Generate the remaining edges
    for i1, i2 in itertools.combinations([i for i in range(c)], 2):
        for j1, j2 in itertools.permutations([j for j in range(d)],2):
            g.add_edge(i1*c+j1, i2*c+j2)
    return g

def __graph02(c=3, d=3):
    g = graphs.SimpleGraph()
    # Generate the c complete subgraphs of size d
    for i in range(c):
        for j in range(d):
            g.add_vertex(str(i)+":"+str(j))
        #for v1, v2 in itertools.combinations([v for v in range(d)], 2):
            #g.add_edge(str(i)+":"+str(v1), str(i)+":"+str(v2))
    # Generate the remaining edges
    for i1, i2 in itertools.combinations([i for i in range(c)], 2):
        for j1, j2 in itertools.permutations([j for j in range(d)],2):
            g.add_edge(str(i1)+":"+str(j1), str(i2)+":"+str(j2))
    return g

def graph02(c=4, d=4):
    g = graphs.SimpleGraph()
    # Generate the nodes 
    for i in range(c):
        for j in range(d):
            g.add_vertex(str(i)+":"+str(j))
    # Generate set of missing edges
    
    missing = {}
    for i in range(c):
        for j in range(d):
            missing[str(i)+":"+str(j)] = set()
            for x in range(1, c):
                missing[str(i)+":"+str(j)].add(( str((i+x)%c)+":"+str((j+x)%d )))
    #print(missing)
    # Make the graph complete
    for v1, v2 in itertools.combinations(g.get_vertices(), 2):
        g.add_edge(v1, v2)
    
    # Remove the edges in 'missing'
    for v1 in missing.keys():
        for v2 in missing[v1]:
            g.remove_edge(v1, v2)
    return g

if __name__ == "__main__":
    g = construct_star_graph()
    util.display_graph(g)
