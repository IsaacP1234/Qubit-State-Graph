import networkx as nx
import itertools as its
import matplotlib.pyplot as plt
import megagraph as mg
import analytics as ats
import test 

#for testing. can handle  up to 5 nodes in reasonable amount of time(about 13 mins for 5, 2s  for 4). 
# can create a 6 node megagraph quickly, but adding edges takes a while. 
# likely cant handle anything higher

print(mg.lc_check([(1,4),(2,4),(1,2)],[(1,4), (1,2)], 4))
print(mg.lc_check([(1,4), (1,2)], [(1,4),(2,4),(1,2)], 4))
print(mg.cnot_check([(1,4), (2,4), (3,4)], [(1,4), (2,4), (3,4), (1,2), (1,3)], 4))
print(mg.cnot_check([(1,4), (2,4), (3,4), (1,2), (1,3)], [(1,4), (2,4), (3,4)], 4))

num_nodes = 4
G = nx.Graph()
for i in range(1, num_nodes+1):
    G.add_node(i)
print(G)
megagraph = mg.create_megagraph(G)
print(megagraph)
mg.add_edges(megagraph, num_nodes)
print(megagraph) # correct num edges and nodes
megagraph2 = mg.create_megagraph(G)
print(megagraph2)
# test for extra edges. num should be 58, is 70
mg.add_edges_alt(megagraph2, num_nodes)
print(megagraph2)
num =0
for i in megagraph2.edges():
    b = False
    #print(megagraph2.nodes[i[0]].get("combo"))
    for j in megagraph.edges():
        #print(j[1].adj)
        if (sorted(megagraph2.nodes[i[0]].get("combo")) == sorted(megagraph.nodes[j[0]].get("combo")) and sorted(megagraph2.nodes[i[1]].get("combo")) == sorted(megagraph.nodes[j[1]].get("combo"))) or (sorted(megagraph2.nodes[i[0]].get("combo")) == sorted(megagraph.nodes[j[1]].get("combo")) and sorted(megagraph2.nodes[i[1]].get("combo")) == sorted(megagraph.nodes[j[0]].get("combo"))):
            b = True
    if not(b):
        print(i[0].adj)
        print(i[1].adj)
        print(megagraph2.edges[i].get("type"))
        num +=1
print(num)


#4 is longest for 4 nodes, 6 is longest for 5
shortest_paths_of_worst_cases = ats.find_shortest_paths_of_worst_cases(megagraph, G)
for i in shortest_paths_of_worst_cases[0]:
    #print(i[0])
    print(megagraph.nodes[i[1]].get("combo"))
#tests(just lc and cnot for now)
test.ut.main()

#attemping to draw the graph
pos = nx.spring_layout(megagraph, seed = 1)
nx.draw(megagraph, pos=pos, with_labels=True)
plt.show()
