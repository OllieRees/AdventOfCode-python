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

    def test_is_safe(self) -> None:
        assert Report(levels=[7, 6, 4, 2, 1]).is_safe

    def test_is_unsafe_down_and_up(self) -> None:
        assert not Report(levels=[1, 3, 2, 4, 5]).is_safe

    def test_is_unsafe_too_low_diff(self) -> None:
        assert not Report(levels=[8, 6, 4, 4, 1]).is_safe

    def test_is_unsafe_too_high_diff(self) -> None:
        assert not Report(levels=[1, 2, 7, 8, 9]).is_safe
