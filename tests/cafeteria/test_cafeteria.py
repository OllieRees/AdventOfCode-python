from unittest import TestCase

from cafeteria.main import Document, FreshRange


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
        self.assertEqual(self.document.ingredient_ids, {1, 5, 8, 11, 17, 32})

    def test_get_report(self) -> None:
        self.assertEqual(self.document.report._ingredient_ids, self.document.ingredient_ids)
        self.assertListEqual(list(self.document.report._fresh_ranges), list(self.document.fresh_ingredient_ranges))


class TestFreshRange(TestCase):
    def test_range(self) -> None:
        pass

    def test_range_start_larger_than_end(self) -> None:
        pass

    def test_range_set(self) -> None:
        pass

    def test_is_in_range(self) -> None:
        pass

    def test_is_not_in_range(self) -> None:
        pass

    def test_superset_range_from_overlapping_ranges(self) -> None:
        pass

    def test_superset_range_from_subset_ranges(self) -> None:
        pass

    def test_superset_range_from_equal_ranges(self) -> None:
        pass

    def test_superset_range_when_no_superset_exists(self) -> None:
        pass


class TestReport(TestCase):
    def test_fresh_ingredients(self) -> None:
        pass
