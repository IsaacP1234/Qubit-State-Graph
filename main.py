import networkx as nx
import itertools as its
import matplotlib.pyplot as plt
import megagraph as mg
import test 

#for testing. can handle  up to 5 nodes in reasonable amount of time(like 10 mins for 5, quickly for 4). 
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

#worst case big O
shortest_paths = nx.shortest_path_length(megagraph, G)
worst_cases = {}
for i in shortest_paths:
    if shortest_paths[i] == max(shortest_paths.values()):
        worst_cases[i] = shortest_paths[i]
for i in worst_cases:
    #nx.draw(i) shows them in different orders everytime and shows square twice, x once, should be vice versa
    #plt.show()
    print(i.adj)
    print(worst_cases[i])#3 is longest for 4 nodes, 5 is longest for 5

#tests(just lc for now)
test.ut.main()

#attemping to draw the graph
pos = nx.spring_layout(megagraph, seed = 1)
nx.draw(megagraph, pos=pos, with_labels=True)
plt.show()
