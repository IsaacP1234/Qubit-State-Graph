import unittest as ut
import megagraph as mg
import networkx as nx
import itertools as its


class test_megagraph(ut.TestCase):
    def test_do_lc(self):
        self.assertEqual(sorted(mg.do_lc([(1,4), (1,2)], 1, 4)), sorted([(1,4),(2,4),(1,2)]))
    def test_do_lc_star(self):
        self.assertEqual(sorted(mg.do_lc([(1,2),(1,3),(1,4)], 1, 4)), sorted([(1,2),(1,3),(1,4), (2,3), (2,4), (3,4)]))
    def test_do_cnot(self):
        self.assertEqual(sorted(mg.do_cnot([(1,4), (2,4), (3,4)], 1, 4, 4)), sorted([(1,4), (2,4), (3,4), (1,2), (1,3)]))

if __name__ == "__main__":
    ut.main()
        

