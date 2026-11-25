# Task Breakdown: Issue #3

## Task 1: Define the public contract with failing tests
- [ ] Description: 在 `tests/test_order_quote.py` 中定义 `quote_order` 与 CLI 的可观察行为。
- Acceptance: 测试数量不少于 8 项，覆盖验收标准与非法输入。
- Verify: RED 阶段运行测试，确认失败原因为 `order_quote` 尚不存在。
- Files: `tests/test_order_quote.py`
- Estimated scope: Small

## Task 2: Implement exact order quoting
- [ ] Description: 新增 `order_quote.py`，实现校验、整单舍入和 CLI。
- Acceptance: `quote_order([])=0`；`1.005×1=101`；两行 `0.005×1` 合计 1；`2.35×3=705`；非法输入抛错，CLI 失败退出码非 0。
- Verify: `python3 -m unittest discover -v`
- Files: `order_quote.py`
- Estimated scope: Small

## Task 3: Add example and README usage
- [ ] Description: 新增示例 JSON，并在 README 追加 Python API 与 CLI 示例。
- Acceptance: README 示例可直接复制执行。
- Verify: `python3 order_quote.py examples/order.json`
- Files: `examples/order.json`, `README.md`
- Estimated scope: Small
