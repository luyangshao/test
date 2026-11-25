from decimal import Decimal, ROUND_HALF_UP


def total_cents(unit_price: str, quantity: int) -> int:
    total = Decimal(unit_price) * quantity * 100
    return int(total.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
