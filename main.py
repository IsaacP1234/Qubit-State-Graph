import networkx as nx
import itertools as its
import matplotlib.pyplot as plt
import megagraph as mg
import test 

#for testing. can handle 5 nodes in reasonable amount of time. 
# can create a 6 node megagraph quickly, but adding edges takes a while. 
# likely cant handle anything higher
num_nodes = 4
G = nx.Graph()
for i in range(1, num_nodes+1):
    G.add_node(i)
print(G)
megagraph = mg.create_megagraph(G)
print(megagraph)
mg.add_edges(megagraph, num_nodes)
print(megagraph) # correct num edges and nodes

test.ut.main()
#attemping to draw the graph
pos = nx.spring_layout(megagraph, seed = 1)
nx.draw(megagraph, pos=pos, with_labels=True)
plt.show()
