from unittest import TestCase

import pytest

from cafeteria.main import Document, FreshRange, Report


class TestDocument(TestCase):
    def setUp(self) -> None:
        lines = ["3-5", "10-14", "16-20", "12-18", "", "1", "5", "8", "11", "17", "32"]
        self.document = Document(lines=lines)

    def test_get_ranges(self) -> None:
        ranges = list(self.document.fresh_ingredient_ranges)
        self.assertIn(FreshRange(start=3, end=5), ranges)
        self.assertIn(FreshRange(start=10, end=14), ranges)
        self.assertIn(FreshRange(start=16, end=20), ranges)
        self.assertIn(FreshRange(start=12, end=18), ranges)

    def test_get_ingredient_ids(self) -> None:
        self.assertEqual(self.document.ingredient_ids, [1, 5, 8, 11, 17, 32])

    def test_get_report(self) -> None:
        self.assertListEqual(self.document.report._ingredient_ids, self.document.ingredient_ids)
        self.assertEqual(self.document.report._fresh_ranges, set(self.document.fresh_ingredient_ranges))


class TestFreshRange(TestCase):
    def test_range(self) -> None:
        range = FreshRange(start=10, end=16)
        self.assertEqual(range.start, 10)
        self.assertEqual(range.end, 16)

    def test_range_start_larger_than_end(self) -> None:
        with pytest.raises(ValueError):
            FreshRange(start=10, end=9)

    def test_is_in_range(self) -> None:
        range = FreshRange(start=10, end=16)
        self.assertTrue(range.is_in_range(10))
        self.assertTrue(range.is_in_range(11))
        self.assertTrue(range.is_in_range(15))
        self.assertTrue(range.is_in_range(16))

    def test_is_not_in_range(self) -> None:
        range = FreshRange(start=10, end=16)
        self.assertFalse(range.is_in_range(9))
        self.assertFalse(range.is_in_range(17))

    def test_range_size(self) -> None:
        self.assertEqual(FreshRange(start=10, end=11).range_size, 2)

    def test_range_size_singleton(self) -> None:
        self.assertEqual(FreshRange(start=10, end=10).range_size, 1)

    def test_superset_range_from_overlapping_ranges(self) -> None:
        pass

    def test_superset_range_from_subset_ranges(self) -> None:
        pass

    def test_superset_range_from_equal_ranges(self) -> None:
        pass

    def test_superset_range_when_no_superset_exists(self) -> None:
        pass


class TestReport(TestCase):
    def setUp(self) -> None:
        self.report = Report(fresh_ranges=[FreshRange(start=10, end=16)], ingredient_ids={1, 10, 13, 16, 18})

    def test_ingredient_is_fresh(self) -> None:
        self.assertTrue(self.report.is_fresh(10))

    def test_ingredient_is_not_fresh(self) -> None:
        self.assertFalse(self.report.is_fresh(17))

    def test_fresh_ingredients(self) -> None:
        self.assertEqual(self.report.fresh_ingredients, {10, 13, 16})
