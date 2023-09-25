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
    megagraph.add_nodes_from([(graph, {"perm" : (())})])
    permuations = pair_partitions(node_pairs(len(graph.nodes())))
    for i in range(len(permuations)):
        for j in range(len(permuations[i])):
            graph.add_edge(permuations[i][j][0], permuations[i][j][1])
        state = graph.copy()
        megagraph.add_nodes_from([(state, {"perm" : permuations[i]})])
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

def add_flip_edges(megagraph):
    for i in megagraph.nodes():
        #print(megagraph.nodes[i].get("perm"))
        for j in megagraph.nodes():
            
            if flip_check(megagraph.nodes[i].get("perm"), megagraph.nodes[j].get("perm")):
                #print("b")
                megagraph.add_edge(i, j)