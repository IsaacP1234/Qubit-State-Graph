import networkx as nx
import itertools as its
import matplotlib.pyplot as plt
import megagraph as mg


nodes = [1,2,3,4]
G = nx.Graph()
G.add_nodes_from(nodes)
megagraph = mg.create_megagraph(G)
print(megagraph)
mg.add_flip_edges(megagraph)
print(megagraph)
print(mg.flip_check(((1,2),(3,4)), ((1,2), (3,4),(2,3))))
#print(mg.pair_partitions(mg.node_pairs(4)))
pos = nx.spring_layout(megagraph, seed = 1)
nx.draw(megagraph, pos=pos, with_labels=True)
plt.show()