import networkx as nx
import itertools as its
import helpers as hp
import megagraph as mg
import copy

#hash that distinhuished between isomorphic graphs with different nodes
def newer_hash(G):
    return hash(frozenset([frozenset(e) for e in G.edges()]+[e for e in G.nodes()]))

#create a list of lists unique pairs nodes in a graph to do gates on
def unique_pairs(sets_of_pairs, pairs, graph):
    if graph.number_of_nodes > 1:
        for i in its.combinations(graph.nodes):
            pairs.append(i)
            partial_graph = create_partial_graph(graph, i)
            unique_pairs(sets_of_pairs, pairs, partial_graph)
    else:
        sets_of_pairs.append(pairs)
        for i in pairs:
            pairs.remove(0)
def convert_pairs_to_gates(pairs, graph):
    possible_gates = []
    for i in pairs:
        gates = []
        #check cnot
        if len(graph.nodes[pairs[i][0]].get("neighborhood")) > 0:
            gates.append(("cnot", pairs[i]))
        #check opposite cnot
        if len(graph.nodes[pairs[i][0]].get("neighborhood")) > 0:
            gates.append(("cnot", pairs[i]))

#add sim edges for two-node ops
def add_two_node_sim_edges(megagraph):
    for i in megagraph.nodes():
        sets_of_pairs = []
        unique_pairs(sets_of_pairs, [], megagraph.nodes[i])
        #lots of gate sets---preprocessing? remove dead gates?


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
""" def create_simultaneous_gate_megatree(graph, megatree):
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
                megagraph.edges[node, new_hash(new_graph)].get("gate_sets").append(gate_set) """
