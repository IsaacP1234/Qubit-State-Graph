import networkx as nx
import itertools as its
import helpers as hp
import copy
import math

#hash that distinguishes between isomporphic graphs with same nodes
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
    megagraph.add_nodes_from([(new_hash(graph), {"graph" : hp.fullcopy(graph), "combo" : (())})])
    combinations = pair_partitions(node_pairs(len(graph.nodes())))
    blank = hp.fullcopy(graph)
    for i in range(len(combinations)):
        for j in range(1, graph.number_of_nodes()+1):
            graph.add_nodes_from([(j, {"neighbors": []})])
        for j in range(len(combinations[i])):
            graph.add_edge(combinations[i][j][0], combinations[i][j][1])
        for j in graph.nodes():
            """ if len(list(graph.neighbors(j))) > 0: """
            #print(list(graph.neighbors(j)))
            #graph.nodes[j].get("neighbors").remove([])
            for k in graph.neighbors(j):
                graph.nodes[j].get("neighbors").append(k)
            """ else:
                graph.nodes[j].get("neighbors").append([]) """
        state = hp.fullcopy(graph)
        megagraph.add_nodes_from([(new_hash(state), {"graph" : hp.fullcopy(state), "combo": combinations[i]})])
        graph = hp.fullcopy(blank)  
    return megagraph


def add_edges(megagraph, n):
    num_lc_edges= 0
    num_cnot_edges = 0
    num_flip_edges = 0
    num_cw_edges = 0
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
            #cw
            new_graph = new_hash(do_cw(megagraph.nodes[i].get("combo"), j[0], j[1], n))
            if new_graph != i and not megagraph.nodes[i].get("graph").has_edge(j[0], j[1]):
                if not(megagraph.has_edge(i, new_graph)):
                    megagraph.add_edges_from([(i, new_graph, {"operation(s)" : [], 
                    "edge delta": abs(len(megagraph.nodes[new_graph].get("combo"))-len(megagraph.nodes[i].get("combo")))})]) 
                    megagraph.edges[(i, new_graph)]["operation(s)"].append("cw"+str((j[0], j[1])))
                    num_cw_edges +=1
                else:
                    try:
                        megagraph.edges[(i, new_graph)]["operation(s)"].index("cw"+str((j[0], j[1])))
                    except:
                        megagraph.edges[(i, new_graph)]["operation(s)"].append("cw"+str((j[0], j[1])))
                        num_cw_edges +=1
                   
    print("edges created by flipping: " + str(num_flip_edges))
    print("egdes created by lc: " + str(num_lc_edges))
    print("edges created by cnot: " + str(num_cnot_edges))
    print("edges created by cw: " + str(num_cw_edges))


#returns a graph with an lc done on the given node in the graph represented by the given combo
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

#returns the graph of the given combo, but with the given ca preformed
def do_flip(combo, node1, node2, n):
    graph= nx.Graph()
    for i in range(1, n+1):
        graph.add_node(i)
    for i in combo:
        graph.add_edge(i[0], i[1])
    graph.add_edge(node1, node2)
    return graph

#sim megagraph
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

def do_cw(combo, node1, node2, n):
    graph = hp.graph_from_combo(combo, n)
    to_cz = []
    for i in graph.neighbors(node1):
        for j in graph.neighbors(node2):
            #check if i,j are each in both neighborhoods
            if not(i in graph.neighbors(node2) and j in graph.neighbors(node1)) and (i, j) not in to_cz:
                to_cz.append((i, j))
    for i in to_cz:
        graph.add_edge(i[0], i[1])
    return graph

#creates a partial graph to use in tree creation
def create_partial_graph(graph, nodes):
    partial_graph = copy.deepcopy(graph)
    """ partial_graph = nx.Graph()
    for i in graph.nodes():
        partial_graph.add_nodes_from([(i, {"neighbors" : graph.nodes[i].get("neighbors")})])
    partial_graph.add_edges_from(hp.combo(graph)) """
    for i in nodes:
        partial_graph.remove_node(i)
    return partial_graph

#trying new mehtod
def new_unique_pairs(sets_of_pairs, pairs, nodes, n):
    if len(nodes) > 1:
        for i in its.combinations(nodes, 2):
            pairs.append(i)
            #print(pairs)
            partial_nodes = nodes.copy()
            for j in i:
                partial_nodes.remove(j)
            #new_pairs = pairs.copy()
            new_unique_pairs(sets_of_pairs, pairs, partial_nodes, n)
            pairs.remove(i)
    else:
        if not(sorted(pairs) in sets_of_pairs) and len(pairs) == n //2:
            #to avoid clearing problems
            """ real_pairs =[]
            real_pairs.append(pairs[len(pairs)-2])
            real_pairs.append(pairs[len(pairs)-1]) """
            sets_of_pairs.append(pairs.copy())
        #pairs.clear()


#create a list of lists unique pairs nodes in a graph to do gates on works for 4 5 and 6
def unique_pairs(sets_of_pairs, pairs, graph, n):
    #print(pairs)
    if graph.number_of_nodes() > 1:
        for i in its.combinations(graph.nodes(), 2):
            #print(f"for loop{pairs}")
            pairs.append(i)
            #print(i)
            partial_graph = create_partial_graph(graph, i)
            #print(partial_graph)
            unique_pairs(sets_of_pairs, pairs, partial_graph, n)
            pairs.remove(i)
    else:
        
        #correct for errors in function
        #print(f"else:{pairs}")
        """ true_pairs = []
        for i in range(n//2):
            true_pairs.append(pairs[len(pairs)-1-i]) """
        if not sorted(pairs) in sets_of_pairs and len(pairs) == n//2:
            #print("a")
            sets_of_pairs.append(sorted(pairs.copy()))
        #print("b")
        """ for i in range(len(pairs)):
            pairs.remove(pairs[0]) """

def convert_pairs_to_gates(pairs):
    #print(pairs)
    possible_gates = []
    for i in pairs:
        gates = []
        gates.append(("cnot",i))
        gates.append(("cnot", (i[1], i[0])))
        gates.append(("cw", i))
        gates.append(("cz", i))
        possible_gates.append(gates)
    print(possible_gates)
    return possible_gates

def convert_gates_to_sets(gate_sets, gate_set, possible_gates):
    if len(possible_gates) > 0:
        for i in possible_gates[0]:
            gate_set.append(i)
            partial_set = possible_gates[1 :len(possible_gates)]
            #add partially built partial set, will create duplicates--switch to set?
            #gate_sets.append(gate_set.copy())
            convert_gates_to_sets(gate_sets, gate_set, partial_set)
    else:
        gate_sets.append(gate_set.copy())
        for i in range(len(gate_set)):
            gate_set.remove(gate_set[0])

#cz compatible with sim gates
def do_sim_cz(graph, node1, node2):
    if graph.has_edge(node1, node2):
        graph.remove_edge(node1, node2)
    else:
        graph.add_edge(node1, node2)
    return graph
#cnot compatible with sim gates            
def do_sim_cnot(graph, control, target):
    for i in graph.nodes[target].get("neighbors"):
        if graph.has_edge(control, i) and i != control:
            graph.remove_edge(control, i)
        elif i != control:
            graph.add_edge(control, i)
    return graph

#cw compatible with sim gates            
def do_sim_cw(graph, node1, node2):
    to_cz = []
    for i in graph.nodes[node1].get("neighbors"):
        for j in graph.nodes[node2].get("neighbors"):
            #check if i,j are each in both neighborhoods
            if not(i in graph.neighbors(node2) and j in graph.neighbors(node1)) and (i, j) not in to_cz:
                to_cz.append((i, j))
    for i in to_cz:
        if graph.has_edge(i[0], i[1]):
            graph.remove_edge(i[0], i[1])
        else:
            graph.add_edge(i[0], i[1])
    return graph

#add sim edges for two-node ops
def add_two_node_sim_edges(megagraph, graph):
    sets_of_pairs = []
    unique_pairs(sets_of_pairs, [], graph, graph.number_of_nodes())
    print(sets_of_pairs)
    print(len(sets_of_pairs))
    possible_gate_sets = []
    for i in sets_of_pairs:
        #print(i)
        for j in range(1, len(i)):
            #print(j)
            for k in its.combinations(i, j):
                #print(k)
                possible_gates = convert_pairs_to_gates(k)
                possible_gate_sets.append(possible_gates)
        possible_gates = convert_pairs_to_gates(i)
        possible_gate_sets.append(possible_gates)
    print(possible_gate_sets)
    print(len(possible_gate_sets))
    sets_of_gates = []
    for gates in possible_gate_sets:
        gate_set = []
        convert_gates_to_sets(gate_set, [], gates)
        #print(len(gate_set))
        for i in gate_set:
            sets_of_gates.append(i)
    #sets_of_gates = set(sets_of_gates)
    print(sets_of_gates)
    print(len(sets_of_gates))
    for node in megagraph.nodes():
        for gate_set in sets_of_gates:
            #print(gate_set)
            #dummy = copy.deepcopy(megagraph.nodes[node].get("graph")) #taking too long
            dummy = hp.fullcopy(megagraph.nodes[node].get("graph"))
            for gate in gate_set:
                #print(gate)
                #do gate on dummy
                if gate[0][1] == "z":
                    dummy = do_sim_cz(dummy, gate[1][0],gate[1][1])
                    #print("z")
                if gate[0][1] == "n":
                    dummy = do_sim_cnot(dummy, gate[1][0],gate[1][1])
                    #print("n")
                """ if gate[0][1] == "n":
                    dummy = do_sim_cnot(dummy, gate[1][1], gate[1][0]) """
                    #print("n2")
                if gate[0][1] == "w" and not dummy.has_edge(gate[1][0], gate[1][1]):
                    dummy = do_sim_cw(dummy, gate[1][0],gate[1][1])
                    #print("w")
            """ print(dummy.adj)
            print(new_hash(dummy))
            print(node) """
            if node != new_hash(dummy):
                megagraph.add_edges_from([(node, new_hash(dummy), {"operation(s)": str(gate_set)})])
            """ print(megagraph) """

                
        #lots of gate sets---preprocessing? remove dead gates?





        
        
        


