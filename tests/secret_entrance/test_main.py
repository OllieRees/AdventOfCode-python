from unittest import TestCase

import pytest

from secret_entrance.main import Dial, Direction, Step, StepsConverter


class TestDial(TestCase):
    def setUp(self) -> None:
        self.dial = Dial(current_position=0)

    def test_rotate_left(self):
        self.dial.rotate(Step(direction=Direction.LEFT, magnitude=1))
        self.assertEqual(self.dial.current_position, 99)

    def test_rotate_right(self):
        self.dial.rotate(Step(direction=Direction.RIGHT, magnitude=1))
        self.assertEqual(self.dial.current_position, 1)

    def test_rotate_left_past_0(self):
        self.dial.current_position = 10
        self.dial.rotate(Step(direction=Direction.LEFT, magnitude=15))
        self.assertEqual(self.dial.current_position, 95)

    def test_rotate_right_past_0(self):
        self.dial.current_position = 95
        self.dial.rotate(Step(direction=Direction.RIGHT, magnitude=15))
        self.assertEqual(self.dial.current_position, 10)

    def test_rotate_new_position(self):
        pos = self.dial.rotate_new_position(Step(direction=Direction.RIGHT, magnitude=1))
        self.assertEqual(pos, 1)

    def test_set_position_too_small(self):
        with pytest.raises(ValueError):
            self.dial.current_position = -1

    def test_set_position_too_large(self):
        with pytest.raises(ValueError):
            self.dial.current_position = 100


class StepsConvertor(TestCase):
    def test_from_lines(self):
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
