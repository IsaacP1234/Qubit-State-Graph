import networkx as nx
import itertools as its
import helpers as hp

#hash that distinguishes between isomporphic graphs with same nodes
def new_hash(G):
    return hash(frozenset([frozenset(e) for e in G.edges()]))

#hash that distinhuished between isomorphic graphs with different nodes
def newer_hash(G):
    return hash(frozenset([frozenset(e) for e in G.edges()]+[e for e in G.nodes()]))
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
                        megagraph.edges[(i, new_graph)]["operation(s)"].append("flip"+str((j[0], j[1])))
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

#creates a partial graph to use in tree creation
def create_partial_graph(graph, nodes):
    partial_graph = nx.Graph()
    for i in graph.nodes():
        partial_graph.add_node(i)
    for i in nodes:
        partial_graph.remove_node(i)
    return partial_graph

#create a tree megagraph where shortest paths to end node represent sets of gate(s) that be done simulatenously 
def create_simultaneous_gate_megatree(graph, megatree):
    #stop if at leaf
    #print(megatree.adj)
    if graph.number_of_nodes() > 1:
    #iterate through all possible gates
        #lc
        for j in graph.nodes():
            to_remove = list(nx.neighbors(graph, j))
            to_remove.append(j)
            partial_graph = create_partial_graph(graph, to_remove)
            print(partial_graph.adj)
            megatree.add_nodes_from([(newer_hash(partial_graph), {"graph": partial_graph, "combo": hp.combo(partial_graph)})])
            if not(megatree.has_edge(newer_hash(graph), newer_hash(partial_graph))):
                megatree.add_edges_from([(newer_hash(graph), newer_hash(partial_graph), {"operation(s)": []})])
            megatree.edges[newer_hash(graph), newer_hash(partial_graph)]["operation(s)"].append("lc("+ str(j)+")")
            create_simultaneous_gate_megatree(partial_graph, megatree)
        for j in its.combinations(graph.nodes(), 2):
            #cz
            to_remove=[j[0], j[1]]
            partial_graph = create_partial_graph(graph, to_remove)
            #add partial graph as nodes
            megatree.add_nodes_from([(newer_hash(graph), {"graph": graph, "combo": hp.combo(graph)}), 
                (newer_hash(partial_graph), {"graph": partial_graph, "combo": hp.combo(partial_graph)})])
            #add edge and gate to edge
            if not(megatree.has_edge(newer_hash(graph), newer_hash(partial_graph))):
                megatree.add_edges_from([(newer_hash(graph), newer_hash(partial_graph), {"operation(s)": []})])
            megatree.edges[newer_hash(graph), newer_hash(partial_graph)]["operation(s)"].append("cz"+ str((j[0],j[1])))
            create_simultaneous_gate_megatree(partial_graph, megatree)
            #cnot
            to_remove=list(nx.neighbors(graph, j[1]))
            to_remove.append(j[0])
            to_remove.append(j[1])
            partial_graph = create_partial_graph(graph, to_remove)
            #add partial graph as nodes
            megatree.add_nodes_from([(newer_hash(graph), {"graph": graph, "combo": hp.combo(graph)}), 
                (newer_hash(partial_graph), {"graph": partial_graph, "combo": hp.combo(partial_graph)})])
            #add edge and gate to edge
            if not(megatree.has_edge(newer_hash(graph), newer_hash(partial_graph))):
                megatree.add_edges_from([(newer_hash(graph), newer_hash(partial_graph), {"operation(s)": []})])
            megatree.edges[newer_hash(graph), newer_hash(partial_graph)]["operation(s)"].append("cnot"+ str((j[0],j[1])))
            create_simultaneous_gate_megatree(partial_graph, megatree)
            #opposite cnot
            to_remove=list(nx.neighbors(graph, j[0]))
            to_remove.append(j[0])
            to_remove.append(j[1])
            partial_graph = create_partial_graph(graph, to_remove)
            #add partial graph as nodes
            megatree.add_nodes_from([(newer_hash(graph), {"graph": graph, "combo": hp.combo(graph)}), 
                (newer_hash(partial_graph), {"graph": partial_graph, "combo": hp.combo(partial_graph)})])
            #add edge and gate to edge
            if not(megatree.has_edge(newer_hash(graph), newer_hash(partial_graph))):
                megatree.add_edges_from([(newer_hash(graph), newer_hash(partial_graph), {"operation(s)": []})])
            megatree.edges[newer_hash(graph), newer_hash(partial_graph)]["operation(s)"].append("cnot"+ str((j[1],j[0])))
            create_simultaneous_gate_megatree(partial_graph, megatree)

def find_gate_sets(gate_sets, gates):
    new_gate_sets = []
    for gate_set in gate_sets:
        for gate in gates:
            new_gate_set = gate_set
            new_gate_set.append(gate)
            new_gate_sets.append(new_gate_set)
    return new_gate_sets
            
#converts a shortest path to a list of lists, where each sublist is a set of gates,  
def convert_path_to_gates(megatree, path, n):
    gates = []
    for i in range(len(path)-1):
        edge_gates = megatree.edges[path[i], path[+1]].get("operation(s)")
        for gate in edge_gates:
            # see if gate does anything
            if gate[2] == "z":
                if megatree.nodes[path[i]].get("combo") == hp.combo(do_flip(megatree.nodes[path[i]].get("combo"), gate[len(gate)-3], gate[len(gate)-2], n)):
                    edge_gates.remove(gate)
            elif gate[2] == "c":
                if megatree.nodes[path[i]].get("combo") == hp.combo(do_lc(megatree.nodes[path[i]].get("combo"), gate[len(gate)-2]), n):
                    edge_gates.remove(gate)
            elif gate[2] == "n":
                if megatree.nodes[path[i]].get("combo") == hp.combo(do_cnot(megatree.nodes[path[i]].get("combo"), gate[len(gate)-3], gate[len(gate)-2], n)):
                    edge_gates.remove(gate)
            gates.append(edge_gates)
    #convert into list of lists, where each sublist is a set of gates
    gate_sets = [gates[0]]
    for i in range(1, len(gates)):
        gate_sets = find_gate_sets(gate_sets, gates[i])
    return gate_sets

#adds edges which can include multiple gates preformed simultaneously
def add_simultaneous_edges(megagraph, n):
    for node in megagraph.nodes():
        megatree = nx.Graph()
        megatree.add_node(newer_hash(node))
        create_simultaneous_gate_megatree(node, megatree)
        #find root node
        for j in megatree.nodes():
            if len(j.get("graph").number_of_nodes) == n:
                root = j
        #find 0 node
        for j in megatree.nodes():
            if len(j.get("graph").number_of_nodes) == 0:
                leaf = j
        paths = nx.all_shortest_paths(megatree, root, leaf)
        for path in paths:
            gates = convert_path_to_gates(path)
            for 

        
        
        


