import BitVector, itertools
import subprocess, os, tempfile, sys

def filter_edges(edges):
    """Input: List of edges (Pairs of integers)
    Output: List of edges (v1,v2) where v2 > v1
    Useful for edges of undirected graphs"""
    return [(v1,v2) for (v1,v2) in edges if v2 > v1]


def generate_tex_code(graph):
    s = []
    s.append(r"""\documentclass[margin=5mm]{standalone}
\usepackage{tikz}
\usetikzlibrary{graphs, graphdrawing}
\usegdlibrary{layered,force}

\begin{document}
\begin{tikzpicture}[
    every node/.style={circle,draw},
    node distance=2cm]

\graph [spring layout, 
%minimum layers=2
 ]
 {
""")
    for edge in filter_edges(graph.get_edges()):
        s.append(str(edge[0]) + " -- " + str(edge[1]) + ",\n")
    for v in graph.get_vertices():
        if graph.degree(v) == 0:
            s.append(str(v) + ",\n")
    s.append("};\n")
    s.append(r"""\end{tikzpicture}
\end{document}""")
    return ''.join(s)

def write_tex_to_file(texcode, out_dir=None, file_=None):
    if file_ is None:
        file_ = tempfile.NamedTemporaryFile(mode='w', suffix='.tex')
    print("Writing into {fn}...".format(fn=file_.name))
    
    if out_dir is None:
        out_dir = os.getcwd()
    
    file_.write(texcode)
    file_.flush()
    tempdir = tempfile.TemporaryDirectory()
    print("Compiling with lualatex...")
    print("Calling: {c}".format(c="lualatex"" ""-interaction=batchmode"" ""-output-directory="+out_dir+" "+os.path.realpath(file_.name)))
    subprocess.call(["lualatex","-interaction=batchmode", "-output-directory="+out_dir, os.path.realpath(file_.name)])
    print("Opening file... {f}".format(f=os.path.join(out_dir, os.path.splitext(os.path.basename(file_.name))[0]+".pdf")))
    
    os.remove(os.path.join(out_dir, os.path.splitext(os.path.basename(file_.name))[0]+".aux"))
    os.remove(os.path.join(out_dir, os.path.splitext(os.path.basename(file_.name))[0]+".log"))
    #subprocess.call(["xdg-open",os.path.join(out_dir, os.path.splitext(os.path.basename(file_.name))[0]+".pdf")])
    file_.close()

def subset_from_bitv(ind, graph):
    solution = set()
    for i, v in enumerate(graph.get_vertices()):
        if ind[i]:
            solution.add(v)
    return solution

def bitv_from_subset(subset, graph):
    bitv = BitVector.BitVector(size=graph.size)
    vertices = list(graph.get_vertices())
    for v in subset:
        try:
            bitv[vertices.index(v)]=1
        except ValueError:
            pass
    return bitv

def time_measure( func, *args, genetic=True):
    """Calls the given function and returns the used CPU time. 
    Time during sleep is not evaluated.
    This procedure is repeated ten times and the average value is returned."""
    from time import process_time
    a = 0
    tmp = process_time()
    ret = func(*args)
    if genetic:
        gen = func.gen_cnt
   
    a += process_time() - tmp
    result = {}
    result['Elapsed time'] = a
    if genetic:
        result['Generation counts'] = gen
    else:
        result['Solution length'] = len(ret)
        result['Solution'] = ret
    return result


def result_to_str(result):
    list = []
    for key in result:
        list.append("\t{key}: {value}\n".format(key=key, value=result[key]))
    return ''.join(list)

def graph01(c=2, d=3):
    g  = graphs.SimpleGraph()
    # Add center
    for i in range(c):
        g.add_vertex(i)
    # Add the neighbours of the center nodes and connect them to their centers
    for i in range(c):
        for n in range(d):
            g.add_vertex(c*(i+1)+n)
            g.add_edge(i, c*(i+1)+n)
    return g


def display_graph(graph):
    tex = generate_tex_code(graph)
    fn = "graph.tex"
    print("Writing into {fn}...".format(fn=fn))
    tmp_path = tempfile.gettempdir()
        
    fo = open(os.path.join(tmp_path,fn), "w")
    fo.write(tex)
    fo.close()
    print(tmp_path)
    print("Compiling with lualatex...")
    print("lualatex","-interaction=batchmode", os.path.join(tmp_path,fn))
    subprocess.call(["lualatex","-interaction=batchmode", os.path.join(tmp_path,fn)])
    print("Opening file...")
    pf = sys.platform
    if pf.startswith('linux'):
        # Linux-specific code here
        subprocess.call(["xdg-open","graph.pdf"])
    elif pf == 'win32':
        # Windows-specific code here
        print(os.path.join(os.getcwd(),"graph.pdf"))
        subprocess.call([os.path.join(os.getcwd(),"graph.pdf")], shell=True)
    elif pf == 'cygwin':
        # Cygwin-specific code here
        subprocess.call(["explorer","graph.pdf"])
    elif pf == 'darwin':
        # Mac OS X-specific code here
        subprocess.call(["open", "graph.pdf"])
    else:
        print("OS not supported: " + pf)
        print("pdf-file located at " + "graph.pdf")
    
