# test

## 批量订单报价

`order_quote.py` 使用 Python 标准库，金额通过 `Decimal` 字符串直构并精确汇总，最后对整单执行一次 `ROUND_HALF_UP` 舍入到分。

```bash
python3 order_quote.py examples/order.json
# {"total_cents": 705}
```

也可以在 Python 中直接调用：

```python
from order_quote import quote_order

quote_order([{"unit_price": "2.35", "quantity": 3}])
# 705
```

输入是一个商品对象数组，每个对象必须包含 `unit_price`（字符串）和 `quantity`（非负整数，不允许布尔值）。CLI 失败时向 stderr 输出错误并以非 0 状态退出。
