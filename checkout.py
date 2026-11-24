def total_cents(unit_price: str, quantity: int) -> int:
    return round(float(unit_price) * quantity * 100)
