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


class TestBankBinaryTree(TestCase):
    def test_all_ascending_voltage(self) -> None:
        bank = Bank([Battery(int(x)) for x in "234"])
        self.assertEqual(bank.bank_binary_tree.root.voltage, 2)
        self.assertEqual(bank.bank_binary_tree.right.root.voltage, 3)
        self.assertEqual(bank.bank_binary_tree.right.right.root.voltage, 4)
        self.assertIsNone(bank.bank_binary_tree.left)

    def test_all_descending_voltage(self) -> None:
        bank = Bank([Battery(int(x)) for x in "432"])
        self.assertEqual(bank.bank_binary_tree.root.voltage, 4)
        self.assertEqual(bank.bank_binary_tree.left.root.voltage, 3)
        self.assertEqual(bank.bank_binary_tree.left.left.root.voltage, 2)
        self.assertIsNone(bank.bank_binary_tree.right)

    def test_same_voltage(self) -> None:
        bank = Bank([Battery(int(x)) for x in "44"])
        self.assertEqual(bank.bank_binary_tree.root.voltage, 4)
        self.assertEqual(bank.bank_binary_tree.left.root.voltage, 4)
        self.assertIsNone(bank.bank_binary_tree.right)

    def test_largest_voltage_in_middle(self) -> None:
        bank = Bank([Battery(int(x)) for x in "4981"])
        self.assertEqual(bank.bank_binary_tree.root.voltage, 4)
        self.assertEqual(bank.bank_binary_tree.left.root.voltage, 1)
        self.assertEqual(bank.bank_binary_tree.right.root.voltage, 9)
        self.assertEqual(bank.bank_binary_tree.right.left.root.voltage, 8)
