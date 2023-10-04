import networkx as nx
import itertools as its
import matplotlib.pyplot as plt
import megagraph as mg


nodes = [1,2,3,4]
G = nx.Graph()
G.add_nodes_from(nodes)
megagraph = mg.create_megagraph(G)
print(megagraph)
mg.add_edges(megagraph, 4)
print(megagraph) # correct num edges and nodes
#print(mg.flip_check(((1,2),(3,4)), ((1,2), (3,4),(2,3))))
#print(mg.pair_partitions(mg.node_pairs(4)))
#attemping to draw the graph
pos = nx.spring_layout(megagraph, seed = 1)
nx.draw(megagraph, pos=pos, with_labels=True)
plt.show()
rug = [(1,2), (2,3), (1,3)]
print(sorted(rug))