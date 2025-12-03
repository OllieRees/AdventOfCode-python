from typing import List, Tuple
from unittest import TestCase

import pytest

from lobby.main import Bank, Battery


class TestBattery(TestCase):
    def setUp(self) -> None:
        self.battery = Battery(voltage=5)

    def test_equal_batteries(self) -> None:
        other: Battery = Battery(voltage=5)
        self.assertTrue(self.battery == other)
        self.assertFalse(self.battery != other)
        self.assertTrue(self.battery <= other)
        self.assertTrue(self.battery >= other)
        self.assertFalse(self.battery < other)
        self.assertFalse(self.battery > other)

    def test_larger_battery(self) -> None:
        other: Battery = Battery(voltage=6)
        self.assertFalse(self.battery == other)
        self.assertTrue(self.battery != other)
        self.assertTrue(self.battery <= other)
        self.assertFalse(self.battery >= other)
        self.assertTrue(self.battery < other)
        self.assertFalse(self.battery > other)

    def test_smaller_battery(self) -> None:
        other: Battery = Battery(voltage=4)
        self.assertFalse(self.battery == other)
        self.assertTrue(self.battery != other)
        self.assertFalse(self.battery <= other)
        self.assertTrue(self.battery >= other)
        self.assertFalse(self.battery < other)
        self.assertTrue(self.battery > other)

    def test_voltage_too_small(self) -> None:
        with pytest.raises(ValueError, match=r"Voltage must be between 1-9 \(inclusive\).Voltage=0"):
            Battery(voltage=0)

    def test_voltage_too_large(self) -> None:
        with pytest.raises(ValueError, match=r"Voltage must be between 1-9 \(inclusive\).Voltage=10"):
            Battery(voltage=10)


class TestBank(TestCase):
    def test_battery_positions_largest_battery_at_end(self) -> None:
        bank = Bank([Battery(int(x)) for x in "811111111111119"])
        positions: List[Tuple[int, Battery]] = list(bank.sorted_battery_positions())
        self.assertEqual(positions[0], (14, Battery(9)))
        self.assertEqual(positions[1], (0, Battery(8)))

    def test_battery_positions_multiple_largest_battery(self) -> None:
        bank = Bank([Battery(int(x)) for x in "991111111111119"])
        positions: List[Tuple[int, Battery]] = list(bank.sorted_battery_positions())
        self.assertEqual(positions[0], (0, Battery(9)))
        self.assertEqual(positions[1], (1, Battery(9)))
        self.assertEqual(positions[2], (14, Battery(9)))

    def test_battery_positions_largest_batteries_at_end(self) -> None:
        bank = Bank([Battery(int(x)) for x in "234234234234287"])
        positions: List[Tuple[int, Battery]] = list(bank.sorted_battery_positions())
        self.assertEqual(positions[0], (13, Battery(8)))
        self.assertEqual(positions[1], (14, Battery(7)))
