##### Defines classes and functions which are useful for testing genetic algorithms #####
from . import util, genetic, graphs, mds
import BitVector
import random, time, os, tempfile, subprocess, configparser, threading, copy

BitVector = BitVector.BitVector

def start_ini(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    
    outpath = os.path.realpath(config.get('GENERAL', 'outpath', fallback = os.getcwd()))
    tex = config.getboolean('GENERAL', 'tex', fallback = False)
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    runs = config.sections()[2:]
    
    graph_list = []
    for key in config['GRAPHS']:
        graph_list.append(config['GRAPHS'][key])
   
    for g in graph_list: 
        graph = graphs.SimpleGraph.from_file(g)
        
        current = os.getcwd()
        path = os.path.realpath(os.path.join(outpath, g))
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)
        graph.to_file(g)
        if tex:
            tex = util.generate_tex_code(graph)
            fn = "graph.tex"
            # print("Writing into {fn}...".format(fn=fn))
            tmp_path = tempfile.gettempdir()
                
            fo = open(os.path.join(tmp_path,fn), "w")
            fo.write(tex)
            fo.close()
            # print("lualatex","-interaction=batchmode", 
                                # os.path.join(tmp_path,fn))
            subprocess.call(["lualatex","-interaction=batchmode", 
                                os.path.join(tmp_path,fn)])
            os.remove('graph.aux')
            os.remove('graph.log')
        os.chdir(current)
        counts = []
        
        for i, run in enumerate(runs):
            if i > graph.size:
                break
            name = config[run]['name']
            path = os.path.realpath(os.path.join(outpath, g, name))
            if not os.path.exists(path):
                os.makedirs(path)
            iterations = config[run]['iterations']
            first = config[run]['first']
            terminate = config[run]['terminate']
            select = config[run]['select']
            crossover = config[run]['crossover']
            mutate = config[run]['mutate']
            replace = config[run]['replace']
            fitness = config[run]['fitness']
            
            alg_descr = ("Genetic_Algorithm("
                        "\nfirst      = " + first + 
                        "\nterminate  = " + terminate + 
                        "\nselect     = " + select + 
                        "\ncrossover  = " + crossover + 
                        "\nmutate     = " + mutate + 
                        "\nreplace    = " + replace + 
                        "\nfitness    = " + fitness + ")\n")
            first = first.split()
            terminate = terminate.split()
            select = select.split()
            crossover = crossover.split()
            mutate = mutate.split()
            replace = replace.split()
            fitness = fitness.split()
            ga = genetic.Genetic_Algorithm(
                    first = getattr(genetic, 'get_first')(*first),
                    terminate = getattr(genetic, 'get_terminate')(*terminate),
                    select = getattr(genetic, 'get_select')(*select),
                    crossover = getattr(genetic, 'get_crossover')(*crossover),
                    mutate = getattr(genetic, 'get_mutate')(*mutate),
                    replace = getattr(genetic, 'get_replace')(*replace),
                    fitness = getattr(genetic, 'get_fitness')(*fitness)
                        )
            ret = test_session(graph, ga, path, 
                            alg_descr, iterations = int(iterations), tex=tex)
            counts.append(ret[2])
            print("---Run {i} finished".format(i=i))
            
        fo = open(os.path.join(outpath, g, 'result.txt'), 'w')
        for c in counts:
            fo.write(str(c)+'\n')
        fo.close()


def test_session(graph, alg, out_dir, alg_descr, iterations=10, tex=True):
    """
    Starts a test session.
    Calls the given algorithm on the given graph.
    The results will be both displayed on screen and saved in a file
    called 'result.txt'. The graph object will be saved to disk both 
    in binary and pdf format. You can use the binary file to get the graph
    via SimpleGraph.from_file('graph.SimpleGraph')
    """
    result = None
    # Save the current dir
    
   
    # Compute the dominating number of the given graph if not already done
    if graph.dom_number is None:
        print("Computing MDS of given graph...")
        graph.dom_number = len(mds.simple_search(graph))
    
    fo = open(os.path.join(os.getcwd(), out_dir, "result.txt"), "w")
    print("Hash value of tested graph: "+str(hash(graph)))
    print("Graph size: {v}, MDS: {m}".format(v=graph.size, m=graph.dom_number))
    print("{n} iterations per algorithm.".format(n=iterations))
    fo.write("Hash value of tested graph: "+str(hash(graph))+'\n')
    fo.write("Graph size: {v}, MDS: {m}, ".format(v=graph.size, m=graph.dom_number))
    fo.write("{n} iterations per algorithm.\n".format(n=iterations))
    
    fo.write(alg_descr+'\n')
    fo.flush()
    results = [None for _ in range(1,iterations+1)]
    t = [None for _ in range(1,iterations+1)]
    
    def worker(alg, i):
        alg.set_outputstream(open(os.path.join(os.getcwd(), out_dir, 'iter'+str(i).zfill(4)+'.txt'), 'w'))
        results[i-1] = util.time_measure(alg, graph, genetic=True)
        alg.out.close()
        
    for i in range(1,iterations+1):
        alg1 = copy.deepcopy(alg)
        t[i-1] = threading.Thread(target=worker, args=(alg1, i))
        t[i-1].start()
    
    for i in range(1,iterations+1):
        t[i-1].join()
    # Write average time and counts
    avg_time = sum((results[i]['Elapsed time'] for i in range(len(results))))/len(results)
    avg_cnts = sum((results[i]['Generation counts'] for i in range(len(results))))/len(results)
    fo.write("Average elapsed time: {avg_time}\n".format(avg_time=avg_time))
    fo.write("Average generations:  {avg_cnts}\n".format(avg_cnts=avg_cnts))
    
    for i in range(1,iterations+1):
        fo.write("Iteration {i}:\n".format(i=i))
        fo.write(util.result_to_str(results[i-1])+'\n')
        
    fo.close()
    return results, avg_time, avg_cnts
    
