import networkx as nx
import itertools as its
import megagraph as mg


nodes = [1,2,3,4]
G = nx.Graph()
G.add_nodes_from(nodes)
megagraph = mg.create_megagraph(G)
print(megagraph)

print(mg.similar_check(((1,2),(3,4)), ((1,2), (3,4),(2,3))))