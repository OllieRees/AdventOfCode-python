from unittest import TestCase

import pytest

from secret_entrance.main import Dial, Direction, Step, StepsConverter


class TestDial(TestCase):
    def setUp(self) -> None:
        self.dial = Dial(current_position=0)

    def test_set_position_too_small(self) -> None:
        with pytest.raises(ValueError):
            self.dial.current_position = -1

    def test_set_position_too_large(self) -> None:
        with pytest.raises(ValueError):
            self.dial.current_position = 100

    def test_set_position_is_0(self) -> None:
        self.assertEqual(self.dial.stops_at_origin, 0)
        self.dial.current_position = 0
        self.assertEqual(self.dial.stops_at_origin, 1)


class TestLeftRotation(TestCase):
    def setUp(self) -> None:
        self.dial = Dial(current_position=0)

    def test_rotate_left_passes_origin(self) -> None:
        self.dial.current_position = 1
        self.dial.rotate(Step(direction=Direction.LEFT, magnitude=2))
        self.assertEqual(self.dial.current_position, 99)
        self.assertEqual(self.dial.count_dial_passed_origin, 1)

    def test_rotate_left_ends_on_origin(self) -> None:
        self.dial.current_position = 1
        self.dial.rotate(Step(direction=Direction.LEFT, magnitude=1))
        self.assertEqual(self.dial.current_position, 0)
        self.assertEqual(self.dial.count_dial_passed_origin, 1)

    def test_rotate_left_passes_origin_multiple_times(self) -> None:
        self.dial.current_position = 1
        self.dial.rotate(Step(direction=Direction.LEFT, magnitude=201))
        self.assertEqual(self.dial.current_position, 0)
        self.assertEqual(self.dial.count_dial_passed_origin, 3)

    def test_rotate_left_starts_at_0(self) -> None:
        self.dial.current_position = 0
        self.dial.rotate(Step(direction=Direction.LEFT, magnitude=1))
        self.assertEqual(self.dial.current_position, 99)
        self.assertEqual(self.dial.count_dial_passed_origin, 0)

    def test_rotate_left_starts_ends_passes_origin(self) -> None:
        self.dial.current_position = 0
        self.dial.rotate(Step(direction=Direction.LEFT, magnitude=200))
        self.assertEqual(self.dial.current_position, 0)
        self.assertEqual(self.dial.count_dial_passed_origin, 2)


class TestRightRotation(TestCase):
    def setUp(self) -> None:
        self.dial = Dial(current_position=0)

    def test_rotate_right_passes_origin(self) -> None:
        self.dial.current_position = 99
        self.dial.rotate(Step(direction=Direction.RIGHT, magnitude=2))
        self.assertEqual(self.dial.current_position, 1)
        self.assertEqual(self.dial.count_dial_passed_origin, 1)

    def test_rotate_right_ends_on_origin(self) -> None:
        self.dial.current_position = 99
        self.dial.rotate(Step(direction=Direction.RIGHT, magnitude=1))
        self.assertEqual(self.dial.current_position, 0)
        self.assertEqual(self.dial.count_dial_passed_origin, 1)

    def test_rotate_right_passes_origin_multiple_times(self) -> None:
        self.dial.current_position = 99
        self.dial.rotate(Step(direction=Direction.RIGHT, magnitude=201))
        self.assertEqual(self.dial.current_position, 0)
        self.assertEqual(self.dial.count_dial_passed_origin, 3)

    def test_rotate_right_starts_at_0(self) -> None:
        self.dial.current_position = 0
        self.dial.rotate(Step(direction=Direction.RIGHT, magnitude=1))
        self.assertEqual(self.dial.current_position, 1)
        self.assertEqual(self.dial.count_dial_passed_origin, 0)


class StepsConvertor(TestCase):
    def test_from_lines(self) -> None:
        lines = ["L10", "R20", "L30"]
        steps = list(StepsConverter().from_lines(iter(lines)))
        self.assertEqual(
            steps,
            [
                Step(direction=Direction.LEFT, magnitude=10),
                Step(direction=Direction.RIGHT, magnitude=20),
                Step(direction=Direction.LEFT, magnitude=30),
            ],
        )
