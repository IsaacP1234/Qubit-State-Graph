import networkx as nx
import itertools as its
import helpers as hp
import copy

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
    blank = copy.deepcopy(graph)
    for i in range(len(combinations)):
        for j in range(len(combinations[i])):
            graph.add_edge(combinations[i][j][0], combinations[i][j][1])
        for j in graph.nodes():
            """ if len(list(graph.neighbors(j))) > 0: """
            print(list(graph.neighbors(j)))
            #graph.nodes[j].get("neighbors").remove([])
            graph.nodes[j].get("neighbors").append(list(graph.neighbors(j)))
            """ else:
                graph.nodes[j].get("neighbors").append([]) """
        state = copy.deepcopy(graph)
        megagraph.add_nodes_from([(new_hash(state), {"graph" : state, "combo": combinations[i]})])
        graph = copy.deepcopy(blank)  
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
    partial_graph = graph.copy()
    """ partial_graph = nx.Graph()
    for i in graph.nodes():
        partial_graph.add_nodes_from([(i, {"neighbors" : graph.nodes[i].get("neighbors")})])
    partial_graph.add_edges_from(hp.combo(graph)) """
    for i in nodes:
        partial_graph.remove_node(i)
    return partial_graph

#create a tree megagraph where shortest paths to end node represent sets of gate(s) that be done simulatenously 
def create_simultaneous_gate_megatree(graph, megatree):
    #stop if at leaf
    #print(megatree.adj)
    #print(graph.adj)
    if graph.number_of_nodes() > 0:
    #iterate through all possible gates
        #lc
        for j in graph.nodes():
            print(graph.nodes[j].get("neighbors"))
            to_remove = copy.deepcopy(graph.nodes[j].get("neighbors")[len(graph.nodes[j].get("neighbors"))-1])
            print(to_remove)
            to_remove.append(j)
            #p_g =create_partial_graph(graph, to_remove)
            try: 
                partial_graph = create_partial_graph(graph, to_remove)
            except:
                print("lc blocked")
            else:
                megatree.add_nodes_from([(newer_hash(partial_graph), {"graph": partial_graph, "combo": hp.combo(partial_graph)})])
                if not(megatree.has_edge(newer_hash(graph), newer_hash(partial_graph))):
                    megatree.add_edges_from([(newer_hash(graph), newer_hash(partial_graph), {"operation(s)": []})])
                megatree.edges[newer_hash(graph), newer_hash(partial_graph)]["operation(s)"].append("lc("+ str(j)+")")
                print(partial_graph.adj)
                print("lc")
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
            print(partial_graph.adj)
            print("cz")
            create_simultaneous_gate_megatree(partial_graph, megatree)
            #cnot
            to_remove=copy.deepcopy(graph.nodes[j[1]].get("neighbors")[len(graph.nodes[j[1]].get("neighbors"))-1])
            if len(to_remove) < 1:
                to_remove.append(j[0])
            elif not j[0] in to_remove:
                to_remove.append(j[0])
            to_remove.append(j[1])
            try:
                partial_graph = create_partial_graph(graph, to_remove)
            except:
                print("cnot blocked")
            else:
                #add partial graph as nodes
                megatree.add_nodes_from([(newer_hash(graph), {"graph": graph, "combo": hp.combo(graph)}), 
                    (newer_hash(partial_graph), {"graph": partial_graph, "combo": hp.combo(partial_graph)})])
                #add edge and gate to edge
                if not(megatree.has_edge(newer_hash(graph), newer_hash(partial_graph))):
                    megatree.add_edges_from([(newer_hash(graph), newer_hash(partial_graph), {"operation(s)": []})])
                megatree.edges[newer_hash(graph), newer_hash(partial_graph)]["operation(s)"].append("cnot"+ str((j[0],j[1])))
                print(partial_graph.adj)
                print("cn")
                create_simultaneous_gate_megatree(partial_graph, megatree)
            #opposite cnot
            print(type(graph.nodes[j[0]].get("neighbors")))
            to_remove=copy.deepcopy(graph.nodes[j[0]].get("neighbors")[len(graph.nodes[j[0]].get("neighbors"))-1])
            if len(to_remove) < 1:
                to_remove.append(j[1])
            elif not j[1] in to_remove:
                to_remove.append(j[1])
            to_remove.append(j[0])
            try:
                partial_graph = create_partial_graph(graph, to_remove)
            except:
                print("cnot blocked")
            else:
                #add partial graph as nodes
                megatree.add_nodes_from([(newer_hash(graph), {"graph": graph, "combo": hp.combo(graph)}), 
                    (newer_hash(partial_graph), {"graph": partial_graph, "combo": hp.combo(partial_graph)})])
                #add edge and gate to edge
                if not(megatree.has_edge(newer_hash(graph), newer_hash(partial_graph))):
                    megatree.add_edges_from([(newer_hash(graph), newer_hash(partial_graph), {"operation(s)": []})])
                megatree.edges[newer_hash(graph), newer_hash(partial_graph)]["operation(s)"].append("cnot"+ str((j[1],j[0])))
                print(partial_graph.adj)
                print("cno")
                create_simultaneous_gate_megatree(partial_graph, megatree)
def find_gate_sets(gate_sets, gates):
    print(len(gate_sets))
    new_gate_sets = []
    for gate_set in gate_sets:
        #print(len(gate_set))
        for gate in gates:
            new_gate_set = copy.deepcopy(gate_set)
            new_gate_set.append(gate)
            new_gate_sets.append(new_gate_set)
    return new_gate_sets
            
#converts a shortest path to a list of lists, where each sublist is a set of gates,  
def convert_path_to_gates(megagraph, node, megatree, path, n):
    gates = []
    for i in range(len(path)-1):
        edge_gates = megatree.edges[path[i], path[i+1]].get("operation(s)")
        print(edge_gates)
        for gate in edge_gates:
            # see if gate does anything
            if gate[1] == "z":
                if sorted(megagraph.nodes[node].get("combo")) == sorted(hp.combo(do_flip(megatree.nodes[path[i]].get("combo"), int(gate[len(gate)-5]), int(gate[len(gate)-2]), n))):
                    edge_gates.remove(gate)
                    print("zr")
            elif gate[1] == "c":
                if sorted(megagraph.nodes[node].get("combo")) == sorted(hp.combo(do_lc(megatree.nodes[path[i]].get("combo"), int(gate[len(gate)-2]), n))):
                    edge_gates.remove(gate)
                    print("cr")
            elif gate[1] == "n":
                if sorted(megagraph.nodes[node].get("combo")) == sorted(hp.combo(do_cnot(megatree.nodes[path[i]].get("combo"), int(gate[len(gate)-5]), int(gate[len(gate)-2]), n))):
                    edge_gates.remove(gate)
                    print("nr")
            print(edge_gates)
            gates.append(edge_gates)
    #convert into list of lists, where each sublist is a set of gates
    gate_sets = [gates[0]]
    print(len(gates))
    for i in range(1, len(gates)):
        gate_sets = find_gate_sets(gate_sets, gates[i])
    return gate_sets

#adds edges which can include multiple gates preformed simultaneously
def add_simultaneous_edges(megagraph, n):
    for node in megagraph.nodes():
        megatree = nx.Graph()
        graph = megagraph.nodes[node].get("graph")
        megatree.add_node(newer_hash(graph))
        create_simultaneous_gate_megatree(graph, megatree)
        #find root node
        #root = ""
        for j in megatree.nodes():
            if megatree.nodes[j].get("graph").number_of_nodes() == n:
                root = j
                print("r")
                print(root)
        #find 0 node
        #leaf = ""
        for j in megatree.nodes():
            if megatree.nodes[j].get("graph").number_of_nodes() == 0:
                leaf = j
                print("l")
        new_graph = hp.graph_from_combo(hp.combo(graph), n) #redunancy to ensure seperate object
        paths = nx.all_shortest_paths(megatree, root, leaf)
        for path in paths:
            print(path)
            gate_sets = convert_path_to_gates(megagraph, node, megatree, path, n)
            for gate_set in gate_sets:
                for gate in gate_set:
                    #print(gate)
                    if gate[1] == "z":
                        #print("z")
                        new_graph = do_flip(hp.combo(new_graph), int(gate[len(gate)-5]), int(gate[len(gate)-2]), n)
                    elif gate[1] == "c":
                        new_graph = do_lc(hp.combo(new_graph), int(gate[len(gate)-2]), n)
                        #print("n")
                    elif gate[1] == "n":
                        #print("n")
                        new_graph = do_cnot(hp.combo(new_graph), int(gate[len(gate)-5]), int(gate[len(gate)-2]), n)
                #print(new_graph.adj)
                megagraph.add_edges_from([(node, new_hash(new_graph), {"gate_sets": []})])
                megagraph.edges[node, new_hash(new_graph)].get("gate_sets").append(gate_set)


        
        
        


