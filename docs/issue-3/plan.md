# Implementation Plan: Issue #3 批量订单报价 CLI

## Overview
以 `checkout.py` 的 Decimal 精确金额方案为基础，新增批量订单报价函数和 CLI。实现采用测试先行：先提交会失败的契约测试，再提交最小实现。

## Architecture Decisions
- `Decimal` 必须直接从字符串构造，避免二进制浮点误差。
- 每行金额精确计算并累加，只对整单执行一次 `ROUND_HALF_UP`，避免 0.005+0.005 被逐行舍入成 2 分。
- `quantity` 拒绝 bool：Python 中 bool 是 int 子类，必须先检查。
- CLI 输出单一 JSON 行，所有失败路径写入 stderr 并返回退出码 1。

## Task List
### Phase 1: Contract tests (RED)
- [ ] 编写不少于 8 项独立测试，覆盖金额、校验、CLI 和 checkout 回归。

### Checkpoint: RED
- [ ] `python3 -m unittest discover -v` 因缺少 `order_quote` 失败。

### Phase 2: Minimal implementation (GREEN)
- [ ] 实现 `quote_order` 与 CLI，使全部测试通过。

### Checkpoint: GREEN
- [ ] 全部 unittest 通过。
- [ ] `python3 order_quote.py examples/order.json` 输出 `{"total_cents": 705}`。

### Phase 3: Documentation
- [ ] 新增 `examples/order.json`，README 追加使用示例。

### Checkpoint: Complete
- [ ] 敏感信息增量扫描通过。
- [ ] 变更仅限 Issue #3 范围，`checkout.py` 无改动。

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| Decimal 接受 NaN/Infinity | High | 解析后调用 `is_finite()` |
| bool 被当作 int | Med | 先检查 bool 再检查 int |
| 错误实现逐行舍入 | High | 用 0.005+0.005 用例锁定 |

## Open Questions
无。
