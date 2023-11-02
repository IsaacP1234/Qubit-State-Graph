import networkx as nx
import megagraph as mg
#takes in completed megagraph and node to start at
#returns list of tuples containing a worst case graph and the number of operations it takes to get there
def find_worst_cases(megagraph, start):
    shortest_path_lengths = nx.shortest_path_length(megagraph, start)
    worst_cases = []
    for i in shortest_path_lengths:
        if shortest_path_lengths[i] == max(shortest_path_lengths.values()):
            worst_cases.append((i, shortest_path_lengths[i]))
    return worst_cases


#returns list of tuples containing an operation and the graph that operation leads to 
def find_shortest_path(megagraph, start, target):
    shortest_path = []
    for j in range(len(nx.shortest_path(megagraph, start, target))-1):
        shortest_path.append((megagraph.edges[nx.shortest_path(megagraph, start, target)[j], 
                                             nx.shortest_path(megagraph, start, target)[j+1]].get("operation(s)"), nx.shortest_path(megagraph, start, target)[j+1],))
    return shortest_path

#returns list of lists of tuples containing an operation and the graph that operation leads to)
def find_shortest_paths_of_worst_cases(megagraph, start):
    megalist = []
    worst_cases = find_worst_cases(megagraph, start)
    for i in worst_cases:
        megalist.append(find_shortest_path(megagraph, start, i[0]))
    return megalist


#for only cnot graph--returns two lists of graphs represent the two groups of graphs that are connected by cnots
def find_groups(megagraph):
    groups = [[],[]]
    # find a valid start node
    start_node = None
    for i in megagraph.nodes():
        if megagraph.nodes[i].get("combo") != (()):
            start_node = i
            break
    #sort nodes
    for i in megagraph.nodes():
        try:
            nx.shortest_path_length(megagraph, start_node, i)
        except:
            groups[1].append(i)
        else:
            groups[0].append(i)
    return groups

def shortest_path_to_star(megagraph, start, n):
    star_graph = nx.Graph()
    for i in range(2, n+1):
        star_graph.add_edge(1,i)
    return find_shortest_path(megagraph, start, mg.new_hash(star_graph))

def find_equivalence_classes(megagraph):
    class_graph = nx.connected_components(megagraph)
    classes = []
    index = 0
    for i in class_graph:
        classes.append({})
        for j in i:
            iso_hash = nx.weisfeiler_lehman_graph_hash(megagraph.nodes[j].get("graph"))
            try:
                classes[index].values().index(iso_hash)
            except:
                classes[index][megagraph.nodes[j].get("combo")] = iso_hash
        index+=1
    return classes