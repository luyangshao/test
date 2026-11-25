"""Quote an order in integer cents using exact decimal arithmetic."""

import json
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


class InvalidItemError(ValueError):
    """Raised when an order or one of its items is invalid."""


def _invalid(message: str) -> InvalidItemError:
    return InvalidItemError(message)


def _parse_unit_price(raw: object) -> Decimal:
    if not isinstance(raw, str):
        raise _invalid("unit_price must be a string")

    try:
        price = Decimal(raw)
    except InvalidOperation as exc:
        raise _invalid(f"unit_price is not a valid decimal: {raw!r}") from exc

    if not price.is_finite():
        raise _invalid("unit_price must be a finite number")
    if price < 0:
        raise _invalid("unit_price must not be negative")
    return price


def _validate_quantity(raw: object) -> int:
    if isinstance(raw, bool) or not isinstance(raw, int):
        raise _invalid("quantity must be an integer")
    if raw < 0:
        raise _invalid("quantity must not be negative")
    return raw


def quote_order(items: list[dict[str, object]]) -> int:
    """Return the total order amount in integer cents.

    Line totals are accumulated exactly; rounding happens once for the
    complete order, using ROUND_HALF_UP.
    """
    if not isinstance(items, list):
        raise _invalid("items must be a list")

    total = Decimal("0")
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise _invalid(f"item at index {index} must be an object")

        if "unit_price" not in item:
            raise _invalid(f"item at index {index} is missing unit_price")
        if "quantity" not in item:
            raise _invalid(f"item at index {index} is missing quantity")

        unit_price = _parse_unit_price(item["unit_price"])
        quantity = _validate_quantity(item["quantity"])
        total += unit_price * quantity

    cents = (total * Decimal("100")).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return int(cents)


def _main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: order_quote.py INPUT_JSON", file=sys.stderr)
        return 1

    input_path = argv[1]
    try:
        with open(input_path, "r", encoding="utf-8") as handle:
            items = json.load(handle)
    except OSError as exc:
        print(f"cannot read input file: {exc}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"input is not valid JSON: {exc}", file=sys.stderr)
        return 1

    try:
        total_cents = quote_order(items)
    except (InvalidItemError, ValueError) as exc:
        print(f"invalid order: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"total_cents": total_cents}))
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
