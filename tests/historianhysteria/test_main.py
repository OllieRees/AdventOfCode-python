from unittest import TestCase

import pytest

from historianhysteria.main import HistoriansLists


class TestHistorianLists(TestCase):
    def test_from_input(self) -> None:
        lists = HistoriansLists.from_input(iter(["3 4", "4 3", "2 5", "1 3", "3 9", "3 3"]))
        assert lists.left == [3, 4, 2, 1, 3, 3]
        assert lists.right == [4, 3, 5, 3, 9, 3]

    def test_from_input_inconsistent_whitespaces(self) -> None:
        lines = ["3    4", "4   3   ", "  2 5  ", "  1        3", "3   9", "3           3       "]
        lists = HistoriansLists.from_input(iter(lines))
        assert lists.left == [3, 4, 2, 1, 3, 3]
        assert lists.right == [4, 3, 5, 3, 9, 3]

    def test_from_no_input(self) -> None:
        lists = HistoriansLists.from_input(iter([]))
        assert lists.left == []
        assert lists.right == []

    def test_from_input_1_bad_row(self) -> None:
        with pytest.raises(ValueError):
            HistoriansLists.from_input(iter(["3 4", "4 3", "2 5", "1", "3 9", "3 3"]))

    def test_from_input_1_col(self) -> None:
        with pytest.raises(ValueError):
            HistoriansLists.from_input(iter(["3    ", "4      ", "  2   ", "  1        ", "3   ", "3                  "]))

    def test_from_input_3_col(self) -> None:
        with pytest.raises(ValueError):
            HistoriansLists.from_input(iter(["3 4 1", "4 3 2", "2 5 3", "1 3 4", "3 9 5", "3 3 6"]))

    def test_total_distance(self) -> None:
        assert HistoriansLists(left=[3, 4, 2, 1, 3, 3], right=[4, 3, 5, 3, 9, 3]).total_distance == 11

    def test_similarity_score(self) -> None:
        assert HistoriansLists(left=[3, 4, 2, 1, 3, 3], right=[4, 3, 5, 3, 9, 3]).similarity_score == 31
