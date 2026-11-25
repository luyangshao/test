import unittest

from checkout import total_cents


class TestTotalCents(unittest.TestCase):
    def test_half_cent_rounds_up_1_005(self):
        self.assertEqual(total_cents("1.005", 1), 101)

    def test_half_cent_rounds_up_1_005_qty_2(self):
        self.assertEqual(total_cents("1.005", 2), 201)

    def test_half_cent_rounds_up_2_005(self):
        self.assertEqual(total_cents("2.005", 1), 201)

    def test_half_cent_rounds_up_0_125(self):
        self.assertEqual(total_cents("0.125", 1), 13)

    def test_below_half_cent_keeps_floor(self):
        self.assertEqual(total_cents("1.004", 1), 100)

    def test_regular_price_0_01(self):
        self.assertEqual(total_cents("0.01", 1), 1)

    def test_regular_price_1_00(self):
        self.assertEqual(total_cents("1.00", 1), 100)

    def test_regular_price_9_99_qty_3(self):
        self.assertEqual(total_cents("9.99", 3), 2997)

    def test_regular_price_19_99_qty_7(self):
        self.assertEqual(total_cents("19.99", 7), 13993)


if __name__ == "__main__":
    unittest.main()
