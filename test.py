import unittest as ut
import megagraph as mg
import networkx as nx
import itertools as its

# no longer works
class test_megagraph(ut.TestCase):
    def test_do_lc(self):
        graph = nx.Graph()
        graph.add_edges_from([(1,4),(2,4),(1,2)])
        self.assertEqual(mg.new_hash(mg.do_lc([(1,4), (1,2)], 1, 4)), mg.new_hash(graph))
    def test_do_lc_star(self):
        graph = nx.Graph()
        graph.add_edges_from([(1,2),(1,3),(1,4), (2,3), (2,4), (3,4)])
        self.assertEqual(mg.new_hash(mg.do_lc([(1,2),(1,3),(1,4)], 1, 4)), mg.new_hash(graph))
    def test_do_cnot(self):
        graph = nx.Graph()
        graph.add_edges_from([(1,4), (2,4), (3,4), (1,2), (1,3)])
        self.assertEqual(mg.new_hash(mg.do_cnot([(1,4), (2,4), (3,4)], 1, 4, 4)), mg.new_hash(graph))

if __name__ == "__main__":
    ut.main()
        

