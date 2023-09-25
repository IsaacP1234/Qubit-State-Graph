import networkx as nx
import itertools as its
import megagraph as mg


nodes = [1,2,3,4]
G = nx.Graph()
G.add_nodes_from(nodes)
megagraph = mg.create_megagraph(G)
print(megagraph)