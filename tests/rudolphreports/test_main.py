from unittest import TestCase

import pytest

from rudolphreports.main import LevelChanges, LevelTrend, Report, UnsafeReport


class TestLevelTrend(TestCase):
    def test_all_incrementing(self) -> None:
        assert LevelTrend(levels=[1, 2, 3, 4, 5]).all_incrementing

    def test_some_incrementing(self) -> None:
        assert not LevelTrend(levels=[1, 2, -1, 4, 5]).all_incrementing

    def test_none_incrementing(self) -> None:
        assert not LevelTrend(levels=[5, 4, 3, 2, 1]).all_incrementing

    def test_all_decrementing(self) -> None:
        assert LevelTrend(levels=[5, 4, 3, 2, 1]).all_decrementing

    def test_some_decrementing(self) -> None:
        assert not LevelTrend(levels=[5, 4, 7, 2, 1]).all_decrementing

    def test_none_decrementing(self) -> None:
        assert not LevelTrend(levels=[1, 2, 3, 4, 5]).all_decrementing

    def test_is_consistent_incrementing(self) -> None:
        assert LevelTrend(levels=[1, 2, 3, 4, 5]).is_consistent

    def test_is_consistent_decrementing(self) -> None:
        assert LevelTrend(levels=[5, 4, 3, 2, 1]).is_consistent

    def test_is_not_consistent(self) -> None:
        assert not LevelTrend(levels=[1, 2, -1, 4, 5]).is_consistent


class TestLevelChanges(TestCase):
    def test_within_range(self) -> None:
        assert LevelChanges(levels=[3, 5, 6, 9]).within_range(1, 3)

    def test_below_range(self) -> None:
        assert not LevelChanges(levels=[3, 6, 6, 8]).within_range(1, 3)
        
    def test_above_range(self) -> None:
        assert not LevelChanges(levels=[3, 6, 10, 8]).within_range(1, 3)

    def test_below_range_initially(self) -> None:
        assert not LevelChanges(levels=[3, 3, 4, 6]).within_range(1, 3)

    def test_above_range_initially(self) -> None:
        assert not LevelChanges(levels=[3, 9, 11, 12]).within_range(1, 3)

class TestReport(TestCase):
    def test_levels_changes(self) -> None:
        assert Report(levels=[4, 9, 6, 12, 15, 13]).level_changes

    def test_levels_trend(self) -> None:
        assert Report(levels=[4, 9, 6, 12, 15, 13]).level_trend

    def test_is_safe(self) -> None:
        assert Report(levels=[7, 6, 4, 2, 1]).is_safe

    def test_is_unsafe_down_and_up(self) -> None:
        assert not Report(levels=[1, 3, 2, 4, 5]).is_safe

    def test_is_unsafe_too_low_diff(self) -> None:
        assert not Report(levels=[8, 6, 4, 4, 1]).is_safe

    def test_is_unsafe_too_high_diff(self) -> None:
        assert not Report(levels=[1, 2, 7, 8, 9]).is_safe

    def test_apply_dampener_on_safe_report(self) -> None:
        assert Report(levels=[7, 6, 4, 2, 1]).apply_dampener().levels == [7, 6, 4, 2, 1]

    def test_apply_dampener_due_to_inconsistent_trend(self) -> None:
        assert Report(levels=[1, 3, 2, 4, 5]).apply_dampener().levels == [1, 2, 4, 5]

    def test_apply_dampener_due_to_out_of_range_level(self) -> None:
        assert Report(levels=[8, 6, 4, 4, 1]).apply_dampener().levels == [8, 6, 4, 1]

    def test_apply_dampener_failure(self) -> None:
        with pytest.raises(UnsafeReport):
            Report(levels=[1, 2, 7, 8, 9]).apply_dampener()

    def test_dampener_is_safe_without_change(self) -> None:
        assert Report(levels=[7, 6, 4, 2, 1]).is_safe_with_dampener

    def test_dampener_is_safe_with_change(self) -> None:
        assert Report(levels=[1, 3, 2, 4, 5]).is_safe_with_dampener

    def test_dampener_is_not_safe(self) -> None:
        assert not Report(levels=[1, 2, 7, 8, 9]).is_safe_with_dampener