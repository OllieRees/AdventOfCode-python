from unittest import TestCase

from gift_shop.main import ProductID, ProductIDRange


class TestProductID(TestCase):
    def test_is_repeating_for_single_digit_even_digits(self) -> None:
        self.assertTrue(ProductID(11).repeats_once)

    def test_is_repeating_for_single_digit_odd_digits(self) -> None:
        self.assertFalse(ProductID(22222).repeats_once)

    def test_is_repeating_for_noise_in_middle(self) -> None:
        self.assertFalse(ProductID(22322).repeats_once)

    def test_repeating_number_multi_digits(self) -> None:
        self.assertTrue(ProductID(446446).repeats_once)

    def test_repeating_number_multi_digits_with_noise_at_end(self) -> None:
        self.assertFalse(ProductID(4464467).repeats_once)

    def test_is_repeating_with_noise_at_both_ends(self) -> None:
        self.assertFalse(ProductID(74464467).repeats_once)

    def test_is_repeating_for_id_that_repeats_twice(self) -> None:
        self.assertTrue(ProductID(446446).is_repeating)

    def test_is_repeating_for_odd_digit_single_number(self) -> None:
        self.assertTrue(ProductID(222).is_repeating)

    def test_is_repeating_for_even_digit_single_number(self) -> None:
        self.assertTrue(ProductID(22).is_repeating)

    def test_is_repeating_for_repeat_that_has_same_digit(self) -> None:
        self.assertTrue(ProductID(123212321232).is_repeating)

    def test_is_repeating_for_repeat_that_starts_and_ends_on_same_digit(self) -> None:
        self.assertTrue(ProductID(123211232112321).is_repeating)


class TestProductIDRange(TestCase):
    def test_product_ids_in_range(self) -> None:
        product_range = [int(id_) for id_ in ProductIDRange(start=ProductID(11), end=ProductID(22)).product_ids_in_range]
        self.assertEqual(product_range, [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22])

    def test_repeating_product_ids_at_range_terminals(self) -> None:
        product_range = [
            int(id_) for id_ in ProductIDRange(start=ProductID(11), end=ProductID(22)).repeat_once_product_ids_from_range
        ]
        self.assertEqual(product_range, [11, 22])

    def test_one_repeating_product_ids_in_range(self) -> None:
        start = ProductID(1188511880)
        end = ProductID(1188511890)
        product_range = [int(id_) for id_ in ProductIDRange(start=start, end=end).repeat_once_product_ids_from_range]
        self.assertEqual(product_range, [1188511885])

    def test_no_repeating_product_ids_in_range(self) -> None:
        start = ProductID(1698522)
        end = ProductID(1698528)
        product_range = [int(id_) for id_ in ProductIDRange(start=start, end=end).repeat_once_product_ids_from_range]
        self.assertEqual(product_range, [])

    def test_one_repeating_product_ids_in_singleton_range(self) -> None:
        start = ProductID(11)
        end = ProductID(11)
        product_range = [int(id_) for id_ in ProductIDRange(start=start, end=end).repeat_once_product_ids_from_range]
        self.assertEqual(product_range, [11])

    def test_no_repeating_product_ids_in_singleton_range(self) -> None:
        start = ProductID(12)
        end = ProductID(12)
        product_range = [int(id_) for id_ in ProductIDRange(start=start, end=end).repeat_once_product_ids_from_range]
        self.assertEqual(product_range, [])
