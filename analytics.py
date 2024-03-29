import networkx as nx
import megagraph as mg
import helpers as hp

#takes in completed megagraph and node to start at
#returns list of tuples containing a worst case graph and the number of operations it takes to get there
def find_worst_cases(megagraph, start):
    shortest_path_lengths = nx.shortest_path_length(megagraph, start)
    worst_length = max(shortest_path_lengths.values())
    worst_cases = []
    for i in shortest_path_lengths:
        if shortest_path_lengths[i] == worst_length and not(hp.is_isomorphic(worst_cases, megagraph.nodes[i].get("graph"))):
            worst_cases.append(megagraph.nodes[i].get("graph"))
    return worst_cases


#returns list of tuples containing an operation and the graph that operation leads to 
def find_shortest_path(megagraph, start, target):
    shortest_path = nx.shortest_path(megagraph, start, target)
    #print(shortest_path)
    formatted_shortest_path = []
    for j in range(len(shortest_path)-1):
        formatted_shortest_path.append((megagraph.edges[shortest_path[j], shortest_path[j+1]].get("operation(s)"), megagraph.nodes[shortest_path[j+1]]))
    return formatted_shortest_path

#returns list of lists of tuples containing an operation and the graph that operation leads to)
def find_shortest_paths_of_worst_cases(megagraph, start):
    megalist = []
    worst_cases = find_worst_cases(megagraph, start)
    for i in worst_cases:
        megalist.append(find_shortest_path(megagraph, start, mg.new_hash(i)))
    return megalist

def shortest_path_to_star(megagraph, start, n):
    star_graph = nx.Graph()
    for i in range(2, n+1):
        star_graph.add_edge(1,i)
    return find_shortest_path(megagraph, start, mg.new_hash(star_graph))

#typically for only singe gate megagraphs
def find_equivalence_classes(megagraph):
    class_graph = nx.connected_components(megagraph)
    classes = []
    index = 0
    for i in class_graph:
        classes.append({})
        for j in i:
            #check for iso
            is_iso = False
            for k in classes[index].values():
                if nx.is_isomorphic(megagraph.nodes[j].get("graph"), k):
                    is_iso = True
                    break
            if not(is_iso):
                classes[index][megagraph.nodes[j].get("combo")] = megagraph.nodes[j].get("graph")
            # old way
            """ iso_hash = nx.weisfeiler_lehman_graph_hash(megagraph.nodes[j].get("graph"))
            try:
                list(classes[index].values()).index(iso_hash)
            except:
                classes[index][megagraph.nodes[j].get("combo")] = iso_hash """
        index+=1
    return classes

#only for 6 nodes
def shortest_path_to_hourglass(megagraph):
    hourglass = nx.Graph()#special graph state that looks like an hourglass
    hourglass.add_edges_from([(1,2), (2,3), (3,4), (4,5), (5,6), (6,1), (6,3)])
    return find_shortest_path(megagraph, mg.new_hash(nx.Graph()), mg.new_hash(hourglass))

#only for 7 nodes
def shortest_path_to_open_envelope(megagraph):
    open_envelope = nx.Graph() # special graph state that looks like an envelope open on the left
    open_envelope.add_edges_from([(1,2), (2,3), (3,4), (4,5), (5,6), (6,1), (6,7), (2,7), (3,7), (4,7)])
    return find_shortest_path(megagraph, mg.new_hash(nx.Graph()), mg.new_hash(open_envelope))

def find_large_edges(megagraph, operations = ["cnot", "lc", "flip"]):
    edges = megagraph.edges()
    #find max edge delta
    edge_deltas = []
    for i in edges:
        for j in operations:
            for k in edges[i].get("operation(s)"):
                if k.__contains__(j):
                    edge_deltas.append(edges[i].get("edge delta"))
    max_delta = max(edge_deltas)
    #create formatted list of edges
    large_edges = []
    for i in edges:
        for j in operations:
            for k in edges[i].get("operation(s)"):
                if k.__contains__(j):
                    if edges[i].get("edge delta") == max_delta:
                        edge = []
                        edge.append(megagraph.nodes[i[0]].get("combo"))
                        edge.append(megagraph.nodes[i[1]].get("combo"))
                        edge.append(edges[i].get("operation(s)"))
                        edge.append(max_delta)
                        large_edges.append(edge)
                        break
    return large_edges

