from unittest import TestCase

from gift_shop.main import ProductID


class TestProductID(TestCase):
    def test_is_repeating_for_single_digit_even_digits(self) -> None:
        self.assertTrue(ProductID(11).is_repeating)

    def test_is_repeating_for_single_digit_odd_digits(self) -> None:
        self.assertTrue(ProductID(22222).is_repeating)

    def test_is_repeating_for_noise_in_middle(self) -> None:
        self.assertFalse(ProductID(22322).is_repeating)

    def test_repeating_number_multi_digits(self) -> None:
        self.assertTrue(ProductID(446446).is_repeating)

    def test_repeating_number_multi_digits_with_noise_at_end(self) -> None:
        self.assertFalse(ProductID(4464467).is_repeating)

    def test_is_repeating_with_noise_at_both_ends(self) -> None:
        self.assertFalse(ProductID(74464467).is_repeating)

    def test_single_digit_count(self) -> None:
        self.assertEqual(ProductID(1).digit_count, 1)

    def test_even_digit_count(self) -> None:
        self.assertEqual(ProductID(11).digit_count, 2)
