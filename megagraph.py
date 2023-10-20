import networkx as nx
import itertools as its


#these functions are used to create a "megagraph" of all possible graph states based on a graph with n nodes
#function that returns list of unordered pairs  
def node_pairs(n):
    pairs = []
    for i in its.combinations(range(1, n+1), 2):
        pairs.append(i)
    return pairs


#function that returns a list of all possible permutations of a set of pairs(a list of tuples of tuples)
def pair_partitions(pairs):
    parts = []
    for i in range(1, len(pairs)+1):
        for j in its.combinations(pairs, i):
            parts.append(j)
    return parts


#for each permutation, create a node in a megagraph of that permuation of node-pairs having edges between them
def create_megagraph(graph):
    megagraph = nx.Graph()
    megagraph.add_nodes_from([(graph, {"hash" : nx.weisfeiler_lehman_graph_hash(graph), "combo" : (())})])
    combinations = pair_partitions(node_pairs(len(graph.nodes())))
    for i in range(len(combinations)):
        for j in range(len(combinations[i])):
            graph.add_edge(combinations[i][j][0], combinations[i][j][1])
        state = graph.copy()
        megagraph.add_nodes_from([(state, {"hash" : nx.weisfeiler_lehman_graph_hash(graph), "combo": combinations[i]})])
        graph.clear_edges()    
    return megagraph

#returns if two tuples of tuples have only one difference between them(so if 2 nodes should be connected)
def flip_check(node1, node2):
    diffs = 0
    # checks if its possible for them to be similar. unnecessary but increases efficency
    if len(node1) +1 == len(node2) or len(node1) -1 == len(node2):
        for i in node1:
            if node2.count(i) == 0:
                diffs +=1
        for i in node2:
            if node1.count(i) == 0:
                diffs +=1
    return diffs == 1

def add_edges(megagraph, n):
    num_lc_edges= 0
    num_cnot_edges = 0
    num_flip_edges = 0
    for i in its.combinations(megagraph.nodes(), 2):
        if flip_check(megagraph.nodes[i[0]].get("combo"), megagraph.nodes[i[1]].get("combo")):
            megagraph.add_edges_from([(i[0], i[1], {"type" : "flip"})])
            num_flip_edges+=1
        if lc_check(megagraph.nodes[i[0]].get("combo"), megagraph.nodes[i[1]].get("combo"), n):
            num_lc_edges +=1
            megagraph.add_edges_from([(i[0], i[1], {"type" : "lc"})])
        if cnot_check(megagraph.nodes[i[0]].get("combo"), megagraph.nodes[i[1]].get("combo"), n):
            num_cnot_edges+=1
            megagraph.add_edges_from([(i[0], i[1], {"type" : "cnot"})])
    print("edges created by flipping: " + str(num_flip_edges))
    print("egdes created by lc: " + str(num_lc_edges))
    print(num_cnot_edges)

def add_edges_alt(megagraph, n):
    num_flip_edges = 0
    num_lc_edges = 0
    num_cnot_edges = 0
    for i in megagraph.nodes():
        for j in megagraph.nodes():
            if i !=j:
                if flip_check(megagraph.nodes[i].get("combo"), megagraph.nodes[j].get("combo")):
                    megagraph.add_edges_from([(i, j, {"type" : "flip"})])
                    num_flip_edges+=1
                if lc_check(megagraph.nodes[i].get("combo"), megagraph.nodes[j].get("combo"), n):
                    num_lc_edges +=1
                    megagraph.add_edges_from([(i, j, {"type" : "lc"})])
                if cnot_check(megagraph.nodes[i].get("combo"), megagraph.nodes[j].get("combo"), n):
                    num_cnot_edges+=1
                    megagraph.add_edges_from([(i, j, {"type" : "cnot"})])

#returns a new combo representing a graph with an lc done on the given node in the graph represented by the given combo
def do_lc(combo, node, n):
    #make the graph the combo represents
    graph = nx.Graph()
    for i in range(1, n+1):
        graph.add_node(i)
    for i in combo:
        graph.add_edge(i[0], i[1])
    #print(graph)
    #sepearate list because neighbors may change
    for i in its.combinations(graph.neighbors(node), 2):
        #print(i)
        if graph.has_edge(i[0], i[1]):
            graph.remove_edge(i[0], i[1])
        else:
            graph.add_edge(i[0], i[1])
    new_combo = []
    for i in graph.edges:
        new_combo.append(i)
    return new_combo

#takes in to combos representing nodes in the megagraph
def lc_check(node1, node2, n):
    for i in range(1, n+1):
        #print(do_lc(node1, i, n))
        if sorted(do_lc(node1, i, n)) == sorted(node2):
            return True

#takes in a combo representing  a node in the megagraph and two nodes wihtin the minigraph(node1=control, node2=target) and returns a 
def do_cnot(combo, control, target, n):
    #make the graph the combo represents
    graph = nx.Graph()
    for i in range(1, n+1):
        graph.add_node(i)
    for i in combo:
        graph.add_edge(i[0], i[1])
    for i in graph.neighbors(target):
        if i != control:
        #flip egde between neighbor of tagret and control
            if graph.has_edge(control, i):
                graph.remove_edge(control, i)
            else:
                graph.add_edge(control, i)
    new_combo = []
    for i in graph.edges:
        new_combo.append(i)
    return new_combo

#takes in two combos and num nodes, returns if doing any cnot on graph1 will turn it into graph2
def cnot_check(graph1, graph2, n):
    for i in range(1, n+1):
        for j in range(1, n+1):
            if i !=j:
                if sorted(do_cnot(graph1, i, j, n)) == sorted(graph2):
                    return True