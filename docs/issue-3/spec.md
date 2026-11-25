# Spec: Issue #3 — 批量订单报价 CLI 与输入校验

## Objective
新增仅使用 Python 标准库的 `order_quote.py`：
- `quote_order(items) -> int` 返回 `total_cents`。
- CLI `python3 order_quote.py input.json` 输出 `{"total_cents": <integer>}`。
- 保持 `checkout.py` 现有行为不变。

## Tech Stack
Python 3 标准库：`decimal`、`json`、`sys`；测试使用 `unittest`。

## Commands
- 运行全部测试：`python3 -m unittest discover -v`
- CLI 有效输入：`python3 order_quote.py examples/order.json`
- CLI 非法输入必须退出非 0。

## Project Structure
- `order_quote.py`：报价函数、输入校验、CLI。
- `tests/test_order_quote.py`：不少于 8 项独立用例，含 checkout 回归。
- `examples/order.json`：示例输入。
- `README.md`：追加使用说明。

## Code Style
金额从字符串直接构造 `Decimal`；先逐行精确累加，再整单一次性 `ROUND_HALF_UP` 到分。
```python
total = Decimal("1.005") * 1 + Decimal("0.005") * 1
int((total * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
```

## Testing Strategy
`unittest discover` 覆盖：
- 空数组、指定金额舍入、整单汇总舍入、常规订单。
- 非法价格、非法数量、缺字段、非法容器。
- CLI 成功输出与失败退出码。
- `checkout.py` 回归用例。

## Boundaries
- Always: 提交前运行测试；只提交需求相关文件。
- Ask first: 新增依赖、修改 `checkout.py`。
- Never: 使用 float 计算金额、逐行舍入、提交真实配置/密钥/日志。

## Success Criteria
- `quote_order([]) == 0`
- `1.005×1 == 101`
- 两行各 `0.005×1` 整单等于 `1`
- `2.35×3 == 705`
- 全部非法输入报错且 CLI 退出码非 0
- `python3 -m unittest discover -v` 全绿

## Open Questions
无。
