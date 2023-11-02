import networkx as nx
import itertools as its
import matplotlib.pyplot as plt
import megagraph as mg
import analytics as ats
import test 



nx.Graph().__hash__ = mg.new_hash(nx.Graph())
A = nx.Graph()
A.add_edge(1,2)
B = nx.Graph()
B.add_edge(1,2)
for c in sorted(nx.connected_components(A), key=len, reverse=True):
    print(len(c))
print(nx.weisfeiler_lehman_graph_hash(A))
print(nx.weisfeiler_lehman_graph_hash(B))

#for testing. can handle  up to 5 nodes in reasonable amount of time(about 7 seccs for 5, instant for 4). 
# can create a 6 node megagraph quickly, but adding edges takes a while.(2 mins total)
# likely cant handle anything higher within reasonable amount of time

num_nodes = 6
G = nx.Graph()
for i in range(1, num_nodes+1):
    G.add_node(i)
print(G)
megagraph = mg.create_megagraph(G)
print(megagraph)
# has self edges
mg.add_edges(megagraph, num_nodes)
print(megagraph) # correct num edges and nodes

#4 is longest for 4 nodes, 6 is longest for 5
""" shortest_paths_of_worst_cases = ats.find_shortest_paths_of_worst_cases(megagraph, mg.new_hash(G))
for i in shortest_paths_of_worst_cases[0]:
    print(i[0])
    print(i[0])
    print(megagraph.nodes[i[1]].get("combo")) """
#only in 6 node megagraph
#hourglass = nx.Graph()
#hourglass.add_edges_from([(1,2), (2,3), (3,4), (4,5), (5,6), (6,1)])
#print(ats.find_shortest_path(megagraph, mg.new_hash(nx.Graph()), mg.new_hash(hourglass)))

#print(ats.shortest_path_to_star(megagraph, mg.new_hash(nx.Graph()), num_nodes))

#equivalence classes(only for cnot)
for i in ats.find_equivalence_classes(megagraph):
    print(len(i.keys()))
#groups = ats.find_groups(megagraph)
#for i in groups:
    #print(len(i))
    #for j in i:
        #print(megagraph.nodes[j].get("combo"))
    #print("break")
#tests(just lc and cnot for now)
#test.ut.main()

#attemping to draw the graph
""" pos = nx.spring_layout(megagraph, seed = 1)
nx.draw(megagraph, pos=pos, with_labels=True)
plt.show() """
