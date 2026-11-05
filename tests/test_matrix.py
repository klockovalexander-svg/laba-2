import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from matrix import calculate_diagonals  # noqa: E402


class TestMatrix(unittest.TestCase):
    def test_side_diagonal_is_greater(self):
        matrix = [[2, 4], [3, 1]]

        result = calculate_diagonals(matrix)

        self.assertEqual(result, (3, 7))

    def test_equal_diagonals(self):
        matrix = [[5]]

        result = calculate_diagonals(matrix)

        self.assertEqual(result, (5, 5))


if __name__ == "__main__":
    unittest.main()
