import unittest
from search import SearchMaze, uniform_cost_search, limited_depth_search, iterative_deepening_search


class TestSearchAlgorithms(unittest.TestCase):

    def test_ucs_maze1(self):
        m = uniform_cost_search("maze1.txt")
        self.assertIsNotNone(m.solution)
        actions, cells = m.solution
        self.assertEqual(len(cells), 10)
        self.assertEqual(m.total_cost, 10)
        self.assertIsNotNone(m.execution_time)
        self.assertIsNotNone(m.peak_memory)
        self.assertGreaterEqual(m.execution_time, 0)
        self.assertGreater(m.peak_memory, 0)

    def test_dls_maze1(self):
        m = limited_depth_search("maze1.txt", 15)
        self.assertIsNotNone(m.solution)
        actions, cells = m.solution
        self.assertEqual(len(cells), 10)
        self.assertIsNotNone(m.execution_time)
        self.assertIsNotNone(m.peak_memory)

    def test_dls_cutoff(self):
        m = SearchMaze("maze1.txt")
        with self.assertRaises(Exception) as ctx:
            m.solve_limited_depth(5)
        self.assertEqual(str(ctx.exception), "cutoff")
        self.assertIsNotNone(m.execution_time)
        self.assertIsNotNone(m.peak_memory)

    def test_ids_maze1(self):
        m = iterative_deepening_search("maze1.txt")
        self.assertIsNotNone(m.solution)
        actions, cells = m.solution
        self.assertEqual(len(cells), 10)
        self.assertIsNotNone(m.execution_time)
        self.assertIsNotNone(m.peak_memory)

    def test_weighted_ucs_maze4(self):
        m = uniform_cost_search("maze4.txt")
        self.assertIsNotNone(m.solution)
        actions, cells = m.solution
        self.assertEqual(m.total_cost, 217)

    def test_weighted_ucs_maze5(self):
        m = uniform_cost_search("maze5.txt")
        self.assertIsNotNone(m.solution)
        actions, cells = m.solution
        self.assertEqual(m.total_cost, 58)

    def test_generic_solve(self):
        m = SearchMaze("maze3.txt")
        m.solve("ucs")
        self.assertEqual(len(m.solution[1]), 4)

        m2 = SearchMaze("maze3.txt")
        m2.solve("dls", limit=10)
        self.assertEqual(len(m2.solution[1]), 4)

        m3 = SearchMaze("maze3.txt")
        m3.solve("ids")
        self.assertEqual(len(m3.solution[1]), 4)


if __name__ == "__main__":
    unittest.main()
