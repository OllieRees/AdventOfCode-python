from unittest import TestCase

from printing_department.main import GridPosition, ToiletRoll, str2grid


class TestGrid(TestCase):
    def setUp(self) -> None:
        self.grid = str2grid(
            grid_str=[
                "..@@.@@@@.",
                "@@@.@.@.@@",
                "@@@@@.@.@@",
                "@.@@@@..@.",
                "@@.@@@@.@@",
                ".@@@@@@@.@",
                ".@.@.@.@@@",
                "@.@@@.@@@@",
                ".@@@@@@@@.",
                "@.@.@@@.@.",
            ],
            roll_str="@",
        )

    def test_num_rolls(self) -> None:
        self.assertEqual(self.grid.roll_count, 71)

    def test_num_rolls_all_rolls(self) -> None:
        grid = str2grid(grid_str=["@@@", "@@@", "@@@"], roll_str="@")
        self.assertEqual(grid.roll_count, 9)

    def test_num_rolls_none_rolls(self) -> None:
        grid = str2grid(grid_str=["...", "...", "..."], roll_str="@")
        self.assertEqual(grid.roll_count, 0)

    def test_middle_has_middle(self) -> None:
        grid = str2grid(grid_str=["@@@", "@@@", "@@@"], roll_str="@")
        self.assertEqual(grid.middle, GridPosition(roll=ToiletRoll(), x=1, y=1))

    def test_middle_even_row_count(self) -> None:
        grid = str2grid(grid_str=["@@@", "@@@"], roll_str="@")
        self.assertIsNone(grid.middle)

    def test_middle_even_column_count(self) -> None:
        grid = str2grid(grid_str=["@@", "@@", "@@"], roll_str="@")
        self.assertIsNone(grid.middle)

    def test_is_accessible_by_forklift(self) -> None:
        self.assertTrue(self.grid.accessible_by_forklift(x=1, y=0))

    def test_is_inaccessible_by_forklift_due_to_being_empty(self) -> None:
        self.assertFalse(self.grid.accessible_by_forklift(x=3, y=1))

    def test_is_inaccessible_by_forklift_on_side(self) -> None:
        self.assertFalse(self.grid.accessible_by_forklift(x=2, y=0))
