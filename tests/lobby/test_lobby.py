from unittest import TestCase

import pytest

from lobby.main import Battery


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
