import unittest
from engine import create_cosine_matrix


class TestEngine(unittest.TestCase):
    def test_cosine_similarity(self):
        cs = create_cosine_matrix(["anakin", "kenobi"])
        self.assertEqual(cs.tolist(), [[1, 0], [0, 1]])
        cs = create_cosine_matrix(["anakin"])
        self.assertEqual(cs.tolist(), [[1]])


if __name__ == "__main__":
    unittest.main()
