import networkx as nx
import itertools as its

#hash that distinguishes between isomporphic graphs
def new_hash(G):
    return hash(frozenset([frozenset(e) for e in G.edges()]))

#these functions are used to create a "megagraph" of all possible graph states(as hashes) based on a graph with n nodes
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
    megagraph.add_nodes_from([(new_hash(graph), {"graph" : graph, "combo" : (())})])
    combinations = pair_partitions(node_pairs(len(graph.nodes())))
    for i in range(len(combinations)):
        for j in range(len(combinations[i])):
            graph.add_edge(combinations[i][j][0], combinations[i][j][1])
        state = graph.copy()
        megagraph.add_nodes_from([(new_hash(state), {"graph" : state, "combo": combinations[i]})])
        graph.clear_edges()    
    return megagraph


def add_edges(megagraph, n):
    num_lc_edges= 0
    num_cnot_edges = 0
    num_flip_edges = 0
    for i in megagraph.nodes():
        for j in range(1, n+1):
            new_graph = new_hash(do_lc(megagraph.nodes[i].get("combo"), j, n))
            if new_graph != i:
                if not(megagraph.has_edge(i, new_graph)):
                    megagraph.add_edges_from([(i, new_graph, {"operation(s)" : [], 
                    "edge delta": abs(len(megagraph.nodes[new_graph].get("combo"))-len(megagraph.nodes[i].get("combo")))})])
                    megagraph.edges[(i, new_graph)]["operation(s)"].append("lc("+str(j)+")")
                    num_lc_edges+=1
                else:
                    try:
                        megagraph.edges[(i, new_graph)]["operation(s)"].index("lc("+str(j)+")")
                    except:
                        megagraph.edges[(i, new_graph)]["operation(s)"].append("lc("+str(j)+")")
                        num_lc_edges+=1
        for j in its.combinations(range(1,n+1), 2):
            new_graph = new_hash(do_flip(megagraph.nodes[i].get("combo"), j[0], j[1], n))
            if new_graph != i:
                if not(megagraph.has_edge(i, new_graph)):
                    megagraph.add_edges_from([(i, new_graph, {"operation(s)" : [], 
                    "edge delta": abs(len(megagraph.nodes[new_graph].get("combo"))-len(megagraph.nodes[i].get("combo")))})]) 
                    megagraph.edges[(i, new_graph)]["operation(s)"].append("flip"+str((j[0], j[1])))
                    num_flip_edges +=1
                else:
                    try:
                        megagraph.edges[(i, new_graph)]["operation(s)"].index("flip"+str((j[0], j[1])))
                    except:
                        #megagraph.edges[(i, new_graph)]["operation(s)"].append("flip"+str((j[0], j[1])))
                        num_flip_edges +=1
            new_graph = new_hash(do_cnot(megagraph.nodes[i].get("combo"), j[0], j[1], n))
            if new_graph != i:
                if not(megagraph.has_edge(i, new_graph)):
                    megagraph.add_edges_from([(i, new_graph, {"operation(s)" : [], 
                    "edge delta": abs(len(megagraph.nodes[new_graph].get("combo"))-len(megagraph.nodes[i].get("combo")))})]) 
                    megagraph.edges[(i, new_graph)]["operation(s)"].append("cnot"+str((j[0], j[1])))
                    num_cnot_edges+=1
                else:
                    try:
                        megagraph.edges[(i, new_graph)]["operation(s)"].index("cnot"+str((j[0], j[1])))
                    except:
                        megagraph.edges[(i, new_graph)]["operation(s)"].append("cnot"+str((j[0], j[1])))
                        num_cnot_edges+=1
            new_graph = new_hash(do_cnot(megagraph.nodes[i].get("combo"), j[1], j[0], n))
            if new_graph != i:
                if not(megagraph.has_edge(i, new_graph)):
                    megagraph.add_edges_from([(i, new_graph, {"operation(s)" : [], 
                    "edge delta": abs(len(megagraph.nodes[new_graph].get("combo"))-len(megagraph.nodes[i].get("combo")))})]) 
                    megagraph.edges[(i, new_graph)]["operation(s)"].append("cnot"+str((j[1], j[0])))
                    num_cnot_edges+=1
                else:
                    try:
                        megagraph.edges[(i, new_graph)]["operation(s)"].index("cnot"+str((j[1], j[0])))
                    except:
                        megagraph.edges[(i, new_graph)]["operation(s)"].append("cnot"+str((j[1], j[0])))
                        num_cnot_edges+=1
                   
    print("edges created by flipping: " + str(num_flip_edges))
    print("egdes created by lc: " + str(num_lc_edges))
    print("edges created by cnot: " + str(num_cnot_edges))


#returns a new combo representing a graph with an lc done on the given node in the graph represented by the given combo
def do_lc(combo, node, n):
    graph= nx.Graph()
    for i in range(1, n+1):
        graph.add_node(i)
    for i in combo:
        graph.add_edge(i[0], i[1])
    for i in its.combinations(graph.neighbors(node), 2):
        if graph.has_edge(i[0], i[1]):
            graph.remove_edge(i[0], i[1])
        else:
            graph.add_edge(i[0], i[1])
    return graph

#returns if two tuples of tuples have only one difference between them(so if 2 nodes should be connected)
def do_flip(combo, node1, node2, n):
    graph= nx.Graph()
    for i in range(1, n+1):
        graph.add_node(i)
    for i in combo:
        graph.add_edge(i[0], i[1])
    graph.add_edge(node1, node2)
    return graph


#takes in a combo representing  a node in the megagraph and two nodes wihtin the minigraph(node1=control, node2=target) and returns a 
def do_cnot(combo, control, target, n):
    graph= nx.Graph()
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
    return graph

