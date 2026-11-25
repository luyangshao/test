import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from checkout import total_cents
from order_quote import InvalidItemError, quote_order


class TestQuoteOrder(unittest.TestCase):
    def test_empty_order_returns_zero(self):
        self.assertEqual(quote_order([]), 0)

    def test_half_cent_rounds_up_for_single_item(self):
        self.assertEqual(quote_order([{"unit_price": "1.005", "quantity": 1}]), 101)

    def test_total_is_rounded_once_not_per_line(self):
        items = [
            {"unit_price": "0.005", "quantity": 1},
            {"unit_price": "0.005", "quantity": 1},
        ]
        self.assertEqual(quote_order(items), 1)

    def test_regular_price_is_multiplied_exactly(self):
        self.assertEqual(quote_order([{"unit_price": "2.35", "quantity": 3}]), 705)

    def test_rejects_non_list_items(self):
        for invalid in (None, {}, "[]"):
            with self.assertRaises(ValueError):
                quote_order(invalid)

    def test_rejects_invalid_unit_price(self):
        invalid_prices = [-1, 1.0, True, None, [], {}, "-1", "NaN", "Infinity", "-Infinity"]
        for invalid in invalid_prices:
            with self.assertRaises(InvalidItemError):
                quote_order([{"unit_price": invalid, "quantity": 1}])

    def test_rejects_invalid_quantity(self):
        invalid_quantities = [-1, 1.5, True, None, "1", [], {}]
        for invalid in invalid_quantities:
            with self.assertRaises(InvalidItemError):
                quote_order([{"unit_price": "1.00", "quantity": invalid}])

    def test_rejects_missing_fields(self):
        with self.assertRaises(InvalidItemError):
            quote_order([{"quantity": 1}])
        with self.assertRaises(InvalidItemError):
            quote_order([{"unit_price": "1.00"}])


class TestQuoteOrderCli(unittest.TestCase):
    def test_cli_prints_total_cents_json(self):
        path = Path("examples/order.json")
        expected = 705
        if not path.exists():
            path = Path(tempfile.gettempdir()) / "order_quote_example.json"
            path.write_text(
                json.dumps([{"unit_price": "2.35", "quantity": 3}]),
                encoding="utf-8",
            )
            self.addCleanup(path.unlink)

        result = subprocess.run(
            [sys.executable, "order_quote.py", str(path)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, json.dumps({"total_cents": expected}) + "\n")

    def test_cli_rejects_invalid_input_with_nonzero_exit(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            json.dump([{"unit_price": "-1", "quantity": 1}], handle)
            path = handle.name
        self.addCleanup(Path(path).unlink)

        result = subprocess.run(
            [sys.executable, "order_quote.py", path],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unit_price", result.stderr)


class TestCheckoutRegression(unittest.TestCase):
    def test_checkout_half_cent_rounding_is_unchanged(self):
        self.assertEqual(total_cents("1.005", 1), 101)

    def test_checkout_regular_price_is_unchanged(self):
        self.assertEqual(total_cents("9.99", 3), 2997)


if __name__ == "__main__":
    unittest.main()
