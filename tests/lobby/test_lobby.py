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
    def test_bank_size(self) -> None:
        bank = Bank([Battery(int(x)) for x in "234234234234287"])
        self.assertEqual(bank.size, 15)

    def test_bank_tree_no_left_branch(self) -> None:
        bank = Bank([Battery(int(x)) for x in "234334334334387"])
        self.assertEqual(bank.bank_heap.root.voltage, 2)
        self.assertEqual(bank.bank_heap.right.root.voltage, 3)
        self.assertIsNone(bank.bank_heap.left)

    def test_bank_tree_no_right_branch(self) -> None:
        bank = Bank([Battery(int(x)) for x in "911111111111118"])
        self.assertEqual(bank.bank_heap.root.voltage, 9)
        self.assertEqual(bank.bank_heap.left.root.voltage, 1)
        self.assertEqual(bank.bank_heap.left.right.root.voltage, 8)
        self.assertIsNone(bank.bank_heap.right)

    def test_bank_tree_full_branches(self) -> None:
        bank = Bank([Battery(int(x)) for x in "5136438"])
        self.assertEqual(bank.bank_heap.root.voltage, 5)
        self.assertEqual(bank.bank_heap.left.root.voltage, 1)
        self.assertEqual(bank.bank_heap.right.root.voltage, 6)

    def test_bank_tree_right_branch_has_battery_with_same_voltage(self) -> None:
        bank = Bank([Battery(int(x)) for x in "55356438"])
        self.assertEqual(bank.bank_heap.root.voltage, 5)
        self.assertEqual(bank.bank_heap.left.root.voltage, 5)
        self.assertEqual(bank.bank_heap.right.root.voltage, 6)
