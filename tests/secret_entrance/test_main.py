from unittest import TestCase

import pytest

from secret_entrance.main import Dial, Direction, Rotation, StepsConverter


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
        self.dial.rotate(Rotation(direction=Direction.LEFT, magnitude=2))
        self.assertEqual(self.dial.current_position, 99)
        self.assertEqual(self.dial.passed_origin, 1)

    def test_rotate_left_ends_on_origin(self) -> None:
        self.dial.current_position = 1
        self.dial.rotate(Rotation(direction=Direction.LEFT, magnitude=1))
        self.assertEqual(self.dial.current_position, 0)
        self.assertEqual(self.dial.passed_origin, 1)

    def test_rotate_left_passes_origin_multiple_times(self) -> None:
        self.dial.current_position = 1
        self.dial.rotate(Rotation(direction=Direction.LEFT, magnitude=201))
        self.assertEqual(self.dial.current_position, 0)
        self.assertEqual(self.dial.passed_origin, 3)

    def test_rotate_left_starts_at_origin(self) -> None:
        self.dial.current_position = 0
        self.dial.rotate(Rotation(direction=Direction.LEFT, magnitude=1))
        self.assertEqual(self.dial.current_position, 99)
        self.assertEqual(self.dial.passed_origin, 0)

    def test_rotate_left_starts_and_passes_origin(self) -> None:
        self.dial.current_position = 0
        self.dial.rotate(Rotation(direction=Direction.LEFT, magnitude=101))
        self.assertEqual(self.dial.current_position, 99)
        self.assertEqual(self.dial.passed_origin, 1)

    def test_rotate_left_starts_ends_passes_origin(self) -> None:
        self.dial.current_position = 0
        self.dial.rotate(Rotation(direction=Direction.LEFT, magnitude=200))
        self.assertEqual(self.dial.current_position, 0)
        self.assertEqual(self.dial.passed_origin, 2)

    def test_rotate_left_magnitude_larger_than_100(self) -> None:
        self.dial.current_position = 50
        self.dial.rotate(Rotation(direction=Direction.LEFT, magnitude=1000))
        self.assertEqual(self.dial.current_position, 50)
        self.assertEqual(self.dial.passed_origin, 10)


class TestRightRotation(TestCase):
    def setUp(self) -> None:
        self.dial = Dial(current_position=0)

    def test_rotate_right_passes_origin(self) -> None:
        self.dial.current_position = 99
        self.dial.rotate(Rotation(direction=Direction.RIGHT, magnitude=2))
        self.assertEqual(self.dial.current_position, 1)
        self.assertEqual(self.dial.passed_origin, 1)

    def test_rotate_right_ends_on_origin(self) -> None:
        self.dial.current_position = 99
        self.dial.rotate(Rotation(direction=Direction.RIGHT, magnitude=1))
        self.assertEqual(self.dial.current_position, 0)
        self.assertEqual(self.dial.passed_origin, 1)

    def test_rotate_right_passes_origin_multiple_times(self) -> None:
        self.dial.current_position = 99
        self.dial.rotate(Rotation(direction=Direction.RIGHT, magnitude=201))
        self.assertEqual(self.dial.current_position, 0)
        self.assertEqual(self.dial.passed_origin, 3)

    def test_rotate_right_starts_at_origin(self) -> None:
        self.dial.current_position = 0
        self.dial.rotate(Rotation(direction=Direction.RIGHT, magnitude=1))
        self.assertEqual(self.dial.current_position, 1)
        self.assertEqual(self.dial.passed_origin, 0)

    def test_rotate_right_starts_and_passes_origin(self) -> None:
        self.dial.current_position = 0
        self.dial.rotate(Rotation(direction=Direction.RIGHT, magnitude=101))
        self.assertEqual(self.dial.current_position, 1)
        self.assertEqual(self.dial.passed_origin, 1)

    def test_rotate_right_starts_ends_passes_origin(self) -> None:
        self.dial.current_position = 0
        self.dial.rotate(Rotation(direction=Direction.RIGHT, magnitude=200))
        self.assertEqual(self.dial.current_position, 0)
        self.assertEqual(self.dial.passed_origin, 2)

    def test_rotate_right_magnitude_larger_than_100(self) -> None:
        self.dial.current_position = 50
        self.dial.rotate(Rotation(direction=Direction.RIGHT, magnitude=1000))
        self.assertEqual(self.dial.current_position, 50)
        self.assertEqual(self.dial.passed_origin, 10)


class TestDirection(TestCase):
    def test_left_move_not_past_origin(self) -> None:
        self.assertEqual(Direction.LEFT.move(10, 9), 1)
        self.assertFalse(Direction.LEFT.passes_origin_once(10, 9))

    def test_left_move_past_origin(self) -> None:
        self.assertEqual(Direction.LEFT.move(10, 11), 99)
        self.assertTrue(Direction.LEFT.passes_origin_once(10, 11))

    def test_left_move_to_origin(self) -> None:
        self.assertEqual(Direction.LEFT.move(10, 10), 0)
        self.assertTrue(Direction.LEFT.passes_origin_once(10, 10))

    def test_right_move_not_past_origin(self) -> None:
        self.assertEqual(Direction.RIGHT.move(90, 9), 99)
        self.assertFalse(Direction.RIGHT.passes_origin_once(90, 9))

    def test_right_move_past_origin(self) -> None:
        self.assertEqual(Direction.RIGHT.move(90, 11), 1)
        self.assertTrue(Direction.RIGHT.passes_origin_once(90, 11))

    def test_right_move_to_origin(self) -> None:
        self.assertEqual(Direction.RIGHT.move(90, 10), 0)
        self.assertTrue(Direction.RIGHT.passes_origin_once(90, 10))


class TestRotation:
    def test_negative_magnitude(self) -> None:
        with pytest.raises(ValueError):
            Rotation(direction=Direction.LEFT, magnitude=-1)


class StepsConvertor(TestCase):
    def test_from_lines(self) -> None:
        lines = ["L10", "R20", "L30"]
        steps = list(StepsConverter().from_lines(iter(lines)))
        self.assertEqual(
            steps,
            [
                Rotation(direction=Direction.LEFT, magnitude=10),
                Rotation(direction=Direction.RIGHT, magnitude=20),
                Rotation(direction=Direction.LEFT, magnitude=30),
            ],
        )
