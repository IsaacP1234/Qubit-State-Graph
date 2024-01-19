import networkx as nx

def is_isomorphic(graphs, graph):
    for i in graphs:
        if nx.is_isomorphic(i, graph):
            return True
    return False

def max_degree():
    return None