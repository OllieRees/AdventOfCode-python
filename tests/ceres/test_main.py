from unittest import TestCase

import numpy as np

from ceres.main import WordSearchGrid


class TestWordSearchGrid(TestCase):
    def setUp(self):
        self.even_grid = np.array([list("abc"), list("def"), list("ghi")])
        self.uneven_grid = np.array([list("abcd"), list("efgh"), list("ijkl")])

    def test_horizontals_square_grid(self) -> None:
        WordSearchGrid(grid=self.even_grid).horizontals == ["abc", "def", "ghi"]

    def test_horizontals_uneven_grid(self) -> None:
        WordSearchGrid(grid=self.uneven_grid).horizontals == ["abcd", "efgh", "ijkl"]

    def test_verticals_square_grid(self) -> None:
        WordSearchGrid(grid=self.even_grid).verticals == ["adg", "beh", "cfi"]

    def test_verticals_uneven_grid(self) -> None:
        WordSearchGrid(grid=self.uneven_grid).verticals == ["aei", "bfj", "cgk", "dhl"]

    def test_forward_diagonals_even_grid(self) -> None:
        assert WordSearchGrid(grid=self.even_grid).forward_diagonals == ["g", "dh", "aei", "bf", "c"]

    def test_forward_diagonals_uneven_grid(self) -> None:
        assert WordSearchGrid(grid=self.uneven_grid).forward_diagonals == ["i", "ej", "afk", "bgl", "ch", "d"]

    def test_backward_diagonals_even_grid(self) -> None:
        assert WordSearchGrid(grid=self.even_grid).backward_diagonals == ["i", "fh", "ceg", "bd", "a"]

    def test_backward_diagonals_uneven_grid(self) -> None:
        assert WordSearchGrid(grid=self.uneven_grid).backward_diagonals == ["l", "hk", "dgj", "cfi", "be", "a"]
