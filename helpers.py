import networkx as nx

def is_isomorphic(graphs, graph):
    iso_hash = nx.weisfeiler_lehman_graph_hash(graph)
    for i in graphs:
        if nx.weisfeiler_lehman_graph_hash(i) == iso_hash:
            return True
    return False