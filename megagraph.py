import networkx as nx
import itertools as its


#these functions are used to create a "megagraph" of all possible graph states based on a graph with n nodes
#function that returns list of unordered pairs  
def node_pairs(n):
    pairs = []
    for i in its.combinations(range(n), 2):
        pairs.append(i)

    return pairs


#function that returns a list of all possible permutations of a set of pairs(a list of tuples of tuples)
def pair_permutations(pairs):
    perms = []
    for i in its.permutations(pairs):
        perms.append(i)

    return perms


#for each permutation, create a node in a megagraph of that permuation of node-pairs having edges between them
def create_megagraph(graph):
    megagraph = nx.Graph()
    megagraph.add_node(graph)
    permuations = pair_permutations(node_pairs(len(graph.nodes())))
    for i in range(len(permuations)):
        for j in range(len(permuations[i])):
            for k in range(len(permuations[i][j])-1):
                graph.add_edge(permuations[i][j][k], permuations[i][j][k+1])
        state = graph.copy()
        megagraph.add_node(state)
        graph.clear_edges()    
    return megagraph