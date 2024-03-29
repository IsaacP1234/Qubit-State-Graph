import networkx as nx

def is_isomorphic(graphs, graph):
    for i in graphs:
        if nx.is_isomorphic(i, graph):
            return True
    return False

def max_degree(graph):

    return max(graph.degree)[1]

def combo(graph):
    combo = []
    for i in graph.edges():
        combo.append((i[0], i[1]))
    return combo

def graph_from_combo(combo, n):
    graph= nx.Graph()
    for i in range(1, n+1):
        graph.add_node(i)
    for i in combo:
        graph.add_edge(i[0], i[1])
    return graph

# copies graph formatted for megagraph inculding attributes, hopefully faster than deepcopy
def fullcopy(graph):
    copy = nx.Graph()
    for i in graph.nodes():
        copy.add_nodes_from([(i, {"neighbors": graph.nodes[i].get("neighbors")})])
    for i in graph.edges():
        copy.add_edge(i[0], i[1])
    return copy