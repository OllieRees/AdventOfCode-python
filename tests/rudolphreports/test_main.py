from unittest import TestCase

from rudolphruports.main import Report


class TestReport(TestCase):
    def test_levels_difference_constant(self) -> None:
        report = Report(levels=list(range(3, 16, 3)))
        assert report._levels_difference == [3, 3, 3, 3] 

    def test_levels_difference_alternate(self) -> None:
        report = Report(levels=[4, 9, 6, 12, 15, 13])
        assert report._levels_difference == [5, -3, 6, 3, -2]

    def test_levels_difference_inconsistent_increase(self) -> None:
        report = Report(levels=[1, 3, 6, 10, 15])
        assert report._levels_difference == [2, 3, 4, 5] 

    def test_levels_difference_inconsistent_decrease(self) -> None:
        report = Report(levels=[20, 15, 8, 2, 1])
        assert report._levels_difference == [-5, -7, -6, -1]
