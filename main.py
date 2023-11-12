import networkx as nx
import itertools as its
import matplotlib.pyplot as plt
import megagraph as mg
import analytics as ats
import test 



nx.Graph().__hash__ = mg.new_hash(nx.Graph())
A = nx.Graph()
A.add_edges_from([(1,2), (2,3)])
B = nx.Graph()
B.add_edge(2,3)
for c in sorted(nx.connected_components(A), key=len, reverse=True):
    print(len(c))
print(nx.weisfeiler_lehman_graph_hash(A))
print(nx.weisfeiler_lehman_graph_hash(B))

diction = {"foo": "bar"}
diction["foo"] +="bar"
print(diction.get("foo"))


#for testing. can handle  up to 5 nodes in reasonable amount of time(about 7 seccs for 5, instant for 4). 
# can create a 6 node megagraph quickly, but adding edges takes a while.(2 mins total)
# likely cant handle anything higher within reasonable amount of time

num_nodes = 7
G = nx.Graph()
for i in range(1, num_nodes+1):
    G.add_node(i)
print(G)
megagraph = mg.create_megagraph(G)
print(megagraph)
# has self edges
mg.add_edges(megagraph, num_nodes)
print(megagraph) # correct num edges and nodes



#prints all edge operations
""" for i in megagraph.edges():
    print(megagraph.edges[i].get("operation(s)")) """
#special states
if num_nodes == 6:
    print("\nshortest path to hourglass")
    for i in ats.shortest_path_to_hourglass(megagraph):
        print(i[0])
        print(i[1].get("combo"))

if num_nodes == 7:
    print("\nshortest path to hourglass")
    for i in ats.shortest_path_to_open_envelope(megagraph):
        print(i[0])
        print(i[1].get("combo"))

print("\nshortest path to star")
for i in ats.shortest_path_to_star(megagraph, mg.new_hash(nx.Graph()), num_nodes):
    print(i[0])
    print(i[1].get("combo"))


#4 is longest for 4 nodes, 6 is longest for 5
print("\nshortest path to a worst case")
shortest_paths_of_worst_cases = ats.find_shortest_paths_of_worst_cases(megagraph, mg.new_hash(G))
for i in shortest_paths_of_worst_cases[0]:
    print(i[0])
    print(i[1].get("combo"))


#equivalence classes(only for cnot)
#for i in ats.find_equivalence_classes(megagraph):
    #print(len(i.keys()))
    
#tests(just lc and cnot for now)
#test.ut.main()

#attemping to draw the graph
""" pos = nx.spring_layout(megagraph, seed = 1)
nx.draw(megagraph, pos=pos, with_labels=True)
plt.show() """
