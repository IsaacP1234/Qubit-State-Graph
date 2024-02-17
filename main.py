import networkx as nx
import itertools as its
import matplotlib.pyplot as plt
import megagraph as mg
import analytics as ats
import helpers as hp
import test 
import copy



nx.Graph().__hash__ = mg.new_hash(nx.Graph())
A = nx.Graph()
A.add_edges_from([(1,2)])
B = nx.Graph()
B.add_edge(2,3)
#print(hp.combo(B))
for c in sorted(nx.connected_components(A), key=len, reverse=True):
    print(len(c))
C = nx.Graph()
C.add_node(1)
D = nx.Graph()
D.add_node(2)
print(mg.newer_hash(C))
print(mg.newer_hash(D))
print(mg.newer_hash(nx.Graph()))

diction = {"foo": "bar"}
diction["foo"] +="bar"
print(diction.get("foo"))


#for testing. can handle  up to 5 nodes in reasonable amount of time(about 7 seccs for 5, instant for 4). 
# can create a 6 node megagraph quickly, but adding edges takes a while.(2 mins total)
# likely cant handle anything higher within reasonable amount of time

num_nodes = 3
G = nx.Graph()
for i in range(1, num_nodes+1):
    G.add_nodes_from([(i, {"neighbors": [[]]})])
print(G)
print(hp.max_degree(G))
megagraph = mg.create_megagraph(G)
print(megagraph)
# has self edges
mg.add_edges(megagraph, num_nodes)
print(megagraph) # correct num edges and nodes

#test 
""" G = nx.Graph()
for i in range(1, num_nodes+1):
    G.add_nodes_from([(i, {"neighbors": [[]]})])
print(G)
print(list(G.neighbors(1)))
megatree = nx.Graph()
megatree.add_node(mg.newer_hash(copy.deepcopy(G)))
print(G.adj)
mg.create_simultaneous_gate_megatree(G, megatree)
print(megatree.adj)
pos = nx.spring_layout(megatree, seed = 1)
nx.draw(megatree, pos=pos, with_labels=True)
plt.show()

sim_megagraph = mg.create_megagraph(G)
mg.add_simultaneous_edges(sim_megagraph, num_nodes) """


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
print("# of worst cases: " + str(len(shortest_paths_of_worst_cases)))
for i in shortest_paths_of_worst_cases[0]:
    print(i[0])
    print(i[1].get("combo"))
for i in shortest_paths_of_worst_cases:
    print(len(i[len(i)-1][1].get("combo")))
    print(i[len(i)-1][1].get("combo"))
    


#equivalence classes(only for cnot)
""" for i in ats.find_equivalence_classes(megagraph):
    print("class"+ "size: " + str(len(i.keys())))
    for j in i.keys():
        if len(j) < 4:
            print(j) """

#find long cnots: 2 for 4, 3 for 5, 4 for 6, 5 for 7
""" for i in ats.find_large_edges(megagraph, ["cnot"]):
    print(i) """
#tests(just lc and cnot for now)
test.ut.main()

#attemping to draw the graph
pos = nx.spring_layout(sim_megagraph, seed = 1)
nx.draw(sim_megagraph, pos=pos, with_labels=True)
plt.show()
