import networkx as nx
import itertools as its
import matplotlib.pyplot as plt
import megagraph as mg
import test 

nodes = [1,2,3,4]
G = nx.Graph()
G.add_nodes_from(nodes)
print(G)
megagraph = mg.create_megagraph(G)
print(megagraph)
mg.add_edges(megagraph, 4)
print(megagraph) # correct num edges and nodes

test.ut.main()
#attemping to draw the graph
pos = nx.spring_layout(megagraph, seed = 1)
nx.draw(megagraph, pos=pos, with_labels=True)
plt.show()
