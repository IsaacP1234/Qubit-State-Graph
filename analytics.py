import networkx as nx

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
                                             nx.shortest_path(megagraph, start, target)[j+1]].get("type"), nx.shortest_path(megagraph, start, target)[j+1],))
    return shortest_path

#returns list of lists of tuples containing an operation and the graph that operation leads to)
def find_shortest_paths_of_worst_cases(megagraph, start):
    megalist = []
    worst_cases = find_worst_cases(megagraph, start)
    for i in worst_cases:
        megalist.append(find_shortest_path(megagraph, start, i[0]))
    return megalist
