from unittest import TestCase

import numpy as np

from ceres.main import WordSearchGrid


class TestWordSearchGrid(TestCase):
    def setUp(self):
        self.even_grid = np.array([list("abc"), list("def"), list("hij")])
        self.uneven_grid = np.array([list("abcd"), list("efgh"), list("ijkl")])   

    def test_horizontals_square_grid(self) -> None:
        WordSearchGrid(grid=self.even_grid).horizontals == ["abc", "def", "hij"]

    def test_horizontals_uneven_grid(self) -> None:
        WordSearchGrid(grid=self.uneven_grid).horizontals == ["abcd", "efgh", "ijkl"]

    def test_verticals_square_grid(self) -> None:
        WordSearchGrid(grid=self.even_grid).verticals == ["adh", "bei", "cfj"]

    def test_verticals_uneven_grid(self) -> None:
        WordSearchGrid(grid=self.uneven_grid).verticals == ["aei", "bfj", "cgk", "dhl"]

    def test_diagonals_even_grid(self) -> None:
        assert WordSearchGrid(grid=self.even_grid).diagonals == ["h", "di", "aej", "bf", "c"]

    def test_diagonals_uneven_grid(self) -> None:
        assert WordSearchGrid(grid=self.uneven_grid).diagonals == ["i", "ej", "afk", "bgl", "ch", "d"]